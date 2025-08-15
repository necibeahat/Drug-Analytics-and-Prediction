"""
OpenFDA Drug Data Analysis Functions

This module contains the core functions extracted from the Jupyter notebook
for better testability and reusability.
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import OrderedDict, Counter


def calc_avg_ing(ingredient_list):
    """
    Calculate number of ingredients per drug based on 'spl_product_data_elements' variable.
    
    Args:
        ingredient_list (list): List containing ingredient string
        
    Returns:
        int: Number of ingredients
    """
    num_ing = len((ingredient_list[0]).split(','))
    return num_ing


def get_in_str(item_list):
    """
    Convert drug name, delivery route, and drug interactions from list to string.
    
    Args:
        item_list (list): List containing item data
        
    Returns:
        str or list: String representation of the item or original list if NaN
    """
    try:
        if (pd.isnull(item_list)).any():
            item = item_list
        else:
            item = ','.join((item_list[0]).split(','))
        return item
    except:
        item = item_list
        return item


def load_openfda_data(data_path, num_files=9):
    """
    Load OpenFDA data from multiple JSON files.
    
    Args:
        data_path (str): Path to the data directory
        num_files (int): Number of files to load (default: 9)
        
    Returns:
        pd.DataFrame: Combined dataframe with relevant columns
    """
    # Read the first file
    first_file = os.path.join(data_path, 'drug-label-0001-of-0009.json')
    
    with open(first_file) as json_file:
        data = json.load(json_file)
        results = pd.json_normalize(data['results'])
        # Only keep relevant columns
        results = results[['openfda.generic_name', 'spl_product_data_elements',
                          'drug_interactions', 'openfda.manufacturer_name',
                          'effective_time', 'openfda.route']].copy()
    
    # Load remaining files
    for i in range(2, num_files + 1):
        file_path = os.path.join(data_path, f'drug-label-{i:04d}-of-0009.json')
        
        with open(file_path) as json_file:
            data = json.load(json_file)
            results_partial = pd.json_normalize(data['results'])
            # Only keep relevant columns
            results_partial = results_partial[['openfda.generic_name', 'spl_product_data_elements',
                                             'drug_interactions', 'openfda.manufacturer_name',
                                             'effective_time', 'openfda.route']].copy()
            results = pd.concat([results, results_partial])
    
    return results


def process_openfda_data(df):
    """
    Process the raw OpenFDA data into a clean format for analysis.
    
    Args:
        df (pd.DataFrame): Raw OpenFDA dataframe
        
    Returns:
        pd.DataFrame: Processed dataframe with cleaned data
    """
    # Remove rows with incorrect date notation
    df = df[df['effective_time'].str.len() == 8]
    
    # Drop rows with NaN in spl_product_data_elements & effective_time
    df = df[pd.notnull(df['spl_product_data_elements'])]
    df = df[pd.notnull(df['effective_time'])]
    
    # Create new dataframe
    processed_df = pd.DataFrame(columns=['year', 'drug_names', 'num_ingredients', 'route', 'manufacturer'])
    
    # Get year from effective_time
    processed_df['year'] = pd.to_datetime(df['effective_time']).dt.year
    
    # Process each row
    ls_num_ing = []
    ls_route = []
    ls_drugname = []
    ls_manufacturer = []
    ls_druginteraction = []
    
    for i in range(len(df)):
        ls_num_ing.append(calc_avg_ing(df['spl_product_data_elements'].iloc[i]))
        ls_route.append(get_in_str(df['openfda.route'].iloc[i]))
        ls_drugname.append(get_in_str(df['openfda.generic_name'].iloc[i]))
        ls_manufacturer.append(get_in_str(df['openfda.manufacturer_name'].iloc[i]))
        ls_druginteraction.append(get_in_str(df['drug_interactions'].iloc[i]))
    
    processed_df['drug_names'] = ls_drugname
    processed_df['num_ingredients'] = ls_num_ing
    processed_df['route'] = ls_route
    processed_df['manufacturer'] = ls_manufacturer
    processed_df['interaction'] = ls_druginteraction
    
    # Data type conversion
    processed_df['num_ingredients'] = processed_df['num_ingredients'].astype(np.int64)
    processed_df['year'] = processed_df['year'].astype(np.int64)
    
    return processed_df


def filter_by_manufacturer(df, manufacturer_name):
    """
    Filter dataframe by manufacturer name.
    
    Args:
        df (pd.DataFrame): Input dataframe
        manufacturer_name (str): Name of manufacturer to filter by
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # Remove NaN rows
    df_filtered = df.dropna(subset=['manufacturer'])
    
    # Filter by manufacturer
    df_manufacturer = df_filtered[df_filtered['manufacturer'].str.match(manufacturer_name)]
    
    return df_manufacturer


def analyze_ingredients_by_year(df, manufacturer_name=None):
    """
    Analyze average number of ingredients by year.
    
    Args:
        df (pd.DataFrame): Input dataframe
        manufacturer_name (str, optional): Filter by manufacturer
        
    Returns:
        pd.DataFrame: Analysis results grouped by year
    """
    if manufacturer_name:
        df = filter_by_manufacturer(df, manufacturer_name)
    
    # Group by year and calculate mean
    yearly_analysis = df.groupby('year')['num_ingredients'].agg(['mean', 'count', 'std']).reset_index()
    yearly_analysis.columns = ['year', 'avg_ingredients', 'count', 'std_ingredients']
    
    return yearly_analysis


def analyze_ingredients_by_route(df, top_n_routes=3):
    """
    Analyze average number of ingredients by delivery route.
    
    Args:
        df (pd.DataFrame): Input dataframe
        top_n_routes (int): Number of top routes to analyze
        
    Returns:
        pd.DataFrame: Analysis results for top routes
    """
    # Get top routes by frequency
    top_routes = df['route'].value_counts().head(top_n_routes).index.tolist()
    
    # Filter data for top routes
    df_top_routes = df[df['route'].isin(top_routes)]
    
    # Group by year and route
    route_analysis = df_top_routes.groupby(['year', 'route'])['num_ingredients'].mean().reset_index()
    
    return route_analysis


def create_prediction_model(df, target_col='num_ingredients', feature_col='year', test_size=0.2):
    """
    Create a linear regression model to predict number of ingredients.
    
    Args:
        df (pd.DataFrame): Input dataframe
        target_col (str): Target variable column name
        feature_col (str): Feature variable column name
        test_size (float): Proportion of data for testing
        
    Returns:
        dict: Dictionary containing model, predictions, and metrics
    """
    # Prepare data
    X = df[feature_col].values.reshape(-1, 1)
    y = df[target_col].values.reshape(-1, 1)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    
    # Train model
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    
    # Make predictions
    y_pred = regressor.predict(X_test)
    
    # Calculate metrics
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    return {
        'model': regressor,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred,
        'metrics': {
            'mae': mae,
            'mse': mse,
            'rmse': rmse
        },
        'coefficients': {
            'intercept': regressor.intercept_[0],
            'slope': regressor.coef_[0][0]
        }
    }


def analyze_drug_interactions(df, manufacturer_name, drug_names_df):
    """
    Analyze drug interactions for a specific manufacturer.
    
    Args:
        df (pd.DataFrame): Input dataframe with drug interactions
        manufacturer_name (str): Manufacturer to analyze
        drug_names_df (pd.DataFrame): Dataframe with drug names for matching
        
    Returns:
        pd.DataFrame: Top drug interactions
    """
    # Filter by manufacturer
    df_manufacturer = df[df['manufacturer'].str.match(manufacturer_name)]
    
    # Get unique drug names for regex matching
    unique_drugs = drug_names_df['generic_name'].drop_duplicates()
    
    # Create regex pattern
    re_str = '|\\b'.join(unique_drugs)
    re_str = '\\b' + re_str
    
    # Find drug mentions in interactions
    drug_mentions = []
    for interaction in df_manufacturer['interaction']:
        if pd.notna(interaction):
            p = re.compile(re_str, re.IGNORECASE)
            result = p.findall(interaction.lower())
            result = list(OrderedDict.fromkeys(result))
            result = list(filter(None, result))
            drug_mentions.extend(result)
    
    # Count occurrences
    interaction_counts = pd.DataFrame(pd.Series(dict(Counter(drug_mentions)))).reset_index()
    interaction_counts.columns = ['drug_name', 'interaction_count']
    interaction_counts = interaction_counts.sort_values('interaction_count', ascending=False)
    
    return interaction_counts


def create_visualizations(df, save_plots=False, output_dir='plots'):
    """
    Create standard visualizations for the analysis.
    
    Args:
        df (pd.DataFrame): Input dataframe
        save_plots (bool): Whether to save plots to files
        output_dir (str): Directory to save plots
        
    Returns:
        dict: Dictionary of plot objects
    """
    if save_plots and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plots = {}
    
    # Correlation matrix
    plt.figure(figsize=(8, 6))
    correlation_data = df[['year', 'num_ingredients']].corr()
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix: Year vs Number of Ingredients')
    if save_plots:
        plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plots['correlation'] = plt.gcf()
    plt.show()
    
    # Distribution of ingredients
    plt.figure(figsize=(10, 6))
    sns.histplot(df['num_ingredients'], bins=30, kde=True)
    plt.title('Distribution of Number of Ingredients')
    plt.xlabel('Number of Ingredients')
    plt.ylabel('Frequency')
    if save_plots:
        plt.savefig(os.path.join(output_dir, 'ingredient_distribution.png'))
    plots['distribution'] = plt.gcf()
    plt.show()
    
    # Scatter plot: Year vs Ingredients
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='year', y='num_ingredients', alpha=0.6)
    plt.title('Year vs Number of Drug Ingredients')
    plt.xlabel('Year')
    plt.ylabel('Number of Ingredients')
    if save_plots:
        plt.savefig(os.path.join(output_dir, 'year_vs_ingredients.png'))
    plots['scatter'] = plt.gcf()
    plt.show()
    
    return plots


def generate_summary_report(df, manufacturer_analysis=None, route_analysis=None, prediction_results=None):
    """
    Generate a summary report of the analysis.
    
    Args:
        df (pd.DataFrame): Main dataframe
        manufacturer_analysis (pd.DataFrame, optional): Manufacturer-specific analysis
        route_analysis (pd.DataFrame, optional): Route analysis results
        prediction_results (dict, optional): Prediction model results
        
    Returns:
        dict: Summary statistics and insights
    """
    report = {
        'dataset_info': {
            'total_records': len(df),
            'date_range': f"{df['year'].min()} - {df['year'].max()}",
            'unique_manufacturers': df['manufacturer'].nunique() if 'manufacturer' in df.columns else 'N/A',
            'unique_routes': df['route'].nunique() if 'route' in df.columns else 'N/A'
        },
        'ingredient_statistics': {
            'mean_ingredients': df['num_ingredients'].mean(),
            'median_ingredients': df['num_ingredients'].median(),
            'std_ingredients': df['num_ingredients'].std(),
            'min_ingredients': df['num_ingredients'].min(),
            'max_ingredients': df['num_ingredients'].max()
        },
        'correlation': {
            'year_ingredient_correlation': df[['year', 'num_ingredients']].corr().iloc[0, 1]
        }
    }
    
    if manufacturer_analysis is not None:
        report['manufacturer_analysis'] = {
            'records_analyzed': len(manufacturer_analysis),
            'year_range': f"{manufacturer_analysis['year'].min()} - {manufacturer_analysis['year'].max()}",
            'avg_ingredients_trend': manufacturer_analysis['avg_ingredients'].tolist()
        }
    
    if route_analysis is not None:
        report['route_analysis'] = {
            'routes_analyzed': route_analysis['route'].unique().tolist(),
            'records_by_route': route_analysis.groupby('route').size().to_dict()
        }
    
    if prediction_results is not None:
        report['prediction_model'] = {
            'model_type': 'Linear Regression',
            'mae': prediction_results['metrics']['mae'],
            'rmse': prediction_results['metrics']['rmse'],
            'intercept': prediction_results['coefficients']['intercept'],
            'slope': prediction_results['coefficients']['slope']
        }
    
    return report


if __name__ == "__main__":
    # Example usage
    print("OpenFDA Analysis Functions Module")
    print("This module contains functions for analyzing OpenFDA drug data.")
    print("Import this module to use the functions in your analysis.")