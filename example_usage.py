#!/usr/bin/env python3
"""
Example Usage Script for OpenFDA Drug Data Analysis

This script demonstrates how to use the OpenFDA analysis functions
with sample data or mock data when the actual OpenFDA files are not available.
"""

import pandas as pd
import numpy as np
from openfda_functions import (
    calc_avg_ing, get_in_str, process_openfda_data,
    filter_by_manufacturer, analyze_ingredients_by_year,
    analyze_ingredients_by_route, create_prediction_model,
    generate_summary_report, create_visualizations
)


def create_sample_data():
    """Create sample data for demonstration purposes."""
    np.random.seed(42)  # For reproducible results
    
    # Create sample raw data similar to OpenFDA structure
    n_samples = 1000
    
    sample_data = {
        'openfda.generic_name': [
            [np.random.choice(['aspirin', 'ibuprofen', 'acetaminophen', 'naproxen', 'diclofenac'])]
            for _ in range(n_samples)
        ],
        'spl_product_data_elements': [
            [','.join([f'ingredient_{i}' for i in range(1, np.random.randint(1, 6))])]
            for _ in range(n_samples)
        ],
        'drug_interactions': [
            [f'interaction_text_{i}'] for i in range(n_samples)
        ],
        'openfda.manufacturer_name': [
            [np.random.choice(['AstraZeneca', 'Pfizer', 'Johnson & Johnson', 'Merck', 'Novartis'])]
            for _ in range(n_samples)
        ],
        'effective_time': [
            f"{np.random.randint(2015, 2023):04d}{np.random.randint(1, 13):02d}{np.random.randint(1, 29):02d}"
            for _ in range(n_samples)
        ],
        'openfda.route': [
            [np.random.choice(['ORAL', 'TOPICAL', 'INTRAVENOUS', 'INTRAMUSCULAR'])]
            for _ in range(n_samples)
        ]
    }
    
    return pd.DataFrame(sample_data)


def main():
    """Main function demonstrating the analysis workflow."""
    print("OpenFDA Drug Data Analysis - Example Usage")
    print("=" * 50)
    
    # Step 1: Create or load sample data
    print("\n1. Creating sample data...")
    raw_data = create_sample_data()
    print(f"   Created {len(raw_data)} sample records")
    
    # Step 2: Process the data
    print("\n2. Processing data...")
    processed_data = process_openfda_data(raw_data)
    print(f"   Processed data shape: {processed_data.shape}")
    print(f"   Columns: {list(processed_data.columns)}")
    
    # Step 3: Generate summary report
    print("\n3. Generating summary report...")
    summary = generate_summary_report(processed_data)
    
    print(f"   Dataset Info:")
    for key, value in summary['dataset_info'].items():
        print(f"     {key}: {value}")
    
    print(f"   Ingredient Statistics:")
    for key, value in summary['ingredient_statistics'].items():
        print(f"     {key}: {value:.2f}" if isinstance(value, float) else f"     {key}: {value}")
    
    # Step 4: Manufacturer-specific analysis (AstraZeneca)
    print("\n4. Analyzing AstraZeneca products...")
    az_analysis = analyze_ingredients_by_year(processed_data, 'AstraZeneca')
    print(f"   AstraZeneca analysis shape: {az_analysis.shape}")
    if len(az_analysis) > 0:
        print("   Sample results:")
        print(az_analysis.head())
    
    # Step 5: Route analysis
    print("\n5. Analyzing by delivery route...")
    route_analysis = analyze_ingredients_by_route(processed_data, top_n_routes=3)
    print(f"   Route analysis shape: {route_analysis.shape}")
    if len(route_analysis) > 0:
        print("   Sample results:")
        print(route_analysis.head())
    
    # Step 6: Prediction model
    print("\n6. Creating prediction model...")
    try:
        prediction_results = create_prediction_model(processed_data)
        print(f"   Model performance:")
        print(f"     MAE: {prediction_results['metrics']['mae']:.3f}")
        print(f"     RMSE: {prediction_results['metrics']['rmse']:.3f}")
        print(f"     Intercept: {prediction_results['coefficients']['intercept']:.3f}")
        print(f"     Slope: {prediction_results['coefficients']['slope']:.6f}")
    except Exception as e:
        print(f"   Error creating prediction model: {e}")
    
    # Step 7: Create visualizations (optional - requires display)
    print("\n7. Creating visualizations...")
    try:
        # Note: This will show plots if running in an environment with display
        plots = create_visualizations(processed_data, save_plots=True, output_dir='example_plots')
        print(f"   Created {len(plots)} visualizations")
        print("   Plots saved to 'example_plots' directory")
    except Exception as e:
        print(f"   Note: Visualization creation skipped: {e}")
    
    # Step 8: Advanced analysis example
    print("\n8. Advanced analysis examples...")
    
    # Filter by specific manufacturer
    pfizer_data = filter_by_manufacturer(processed_data, 'Pfizer')
    print(f"   Pfizer products: {len(pfizer_data)} records")
    
    # Analyze correlation
    correlation = processed_data[['year', 'num_ingredients']].corr().iloc[0, 1]
    print(f"   Year-Ingredient correlation: {correlation:.4f}")
    
    # Top manufacturers by product count
    top_manufacturers = processed_data['manufacturer'].value_counts().head(5)
    print(f"   Top 5 manufacturers:")
    for manufacturer, count in top_manufacturers.items():
        print(f"     {manufacturer}: {count} products")
    
    print("\n" + "=" * 50)
    print("Analysis complete! Check the generated files and plots.")


if __name__ == "__main__":
    main()