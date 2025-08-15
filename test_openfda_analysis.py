import unittest
import pandas as pd
import numpy as np
import json
from unittest.mock import patch, mock_open
import sys
import os

# Add the current directory to the path to import functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from our module
from openfda_functions import (
    calc_avg_ing, get_in_str, process_openfda_data, 
    filter_by_manufacturer, analyze_ingredients_by_year,
    analyze_ingredients_by_route, create_prediction_model,
    generate_summary_report
)

class TestOpenFDAAnalysis(unittest.TestCase):
    """
    Unit tests for OpenFDA Drug Data Analysis functions
    """
    
    def setUp(self):
        """Set up test data"""
        # Create sample data for testing
        self.sample_data = {
            'openfda.generic_name': [['aspirin'], ['ibuprofen'], ['acetaminophen']],
            'spl_product_data_elements': [['ingredient1,ingredient2'], ['ingredient1'], ['ing1,ing2,ing3']],
            'drug_interactions': [['interaction1'], ['interaction2'], ['interaction3']],
            'openfda.manufacturer_name': [['AstraZeneca'], ['Pfizer'], ['AstraZeneca']],
            'effective_time': ['20200101', '20210101', '20190101'],
            'openfda.route': [['ORAL'], ['TOPICAL'], ['INTRAVENOUS']]
        }
        self.df_sample = pd.DataFrame(self.sample_data)
    
    def test_calc_avg_ing_function(self):
        """Test the calc_avg_ing function"""
        # Test cases
        test_cases = [
            (['ingredient1,ingredient2'], 2),
            (['ingredient1'], 1),
            (['ing1,ing2,ing3'], 3),
            (['single'], 1)
        ]
        
        for ingredient_list, expected in test_cases:
            with self.subTest(ingredient_list=ingredient_list):
                result = calc_avg_ing(ingredient_list)
                self.assertEqual(result, expected)
    
    def test_get_in_str_function(self):
        """Test the get_in_str function"""
        # Test cases
        test_cases = [
            (['aspirin'], 'aspirin'),
            (['drug1,drug2'], 'drug1,drug2'),
            ([np.nan], [np.nan]),  # Should return the original list for NaN
        ]
        
        for item_list, expected in test_cases:
            with self.subTest(item_list=item_list):
                result = get_in_str(item_list)
                if isinstance(expected, list) and len(expected) == 1 and pd.isna(expected[0]):
                    self.assertTrue(isinstance(result, list) and len(result) == 1 and pd.isna(result[0]))
                else:
                    self.assertEqual(result, expected)
    
    def test_data_processing_pipeline(self):
        """Test the data processing pipeline"""
        # Test data cleaning steps
        df = self.df_sample.copy()
        
        # Test effective_time length filtering
        df_filtered = df[df['effective_time'].str.len() == 8]
        self.assertEqual(len(df_filtered), 3)  # All our test data has 8-character dates
        
        # Test dropping NaN values
        df_no_nan = df_filtered.dropna(subset=['spl_product_data_elements', 'effective_time'])
        self.assertEqual(len(df_no_nan), 3)  # No NaN values in our test data
        
        # Test year extraction
        years = pd.to_datetime(df_no_nan['effective_time']).dt.year
        expected_years = [2020, 2021, 2019]
        self.assertEqual(list(years), expected_years)
    
    def test_astrazeneca_filtering(self):
        """Test AstraZeneca manufacturer filtering"""
        df = self.df_sample.copy()
        
        # Apply manufacturer filtering logic
        df['manufacturer'] = df['openfda.manufacturer_name'].apply(lambda x: x[0])
        df_az = df[df['manufacturer'].str.match('AstraZeneca')]
        
        # Should have 2 AstraZeneca entries
        self.assertEqual(len(df_az), 2)
        
        # Check that all entries are AstraZeneca
        for manufacturer in df_az['manufacturer']:
            self.assertEqual(manufacturer, 'AstraZeneca')
    
    def test_route_analysis(self):
        """Test delivery route analysis"""
        df = self.df_sample.copy()
        
        # Extract routes
        df['route'] = df['openfda.route'].apply(lambda x: x[0])
        
        # Check unique routes
        unique_routes = df['route'].unique()
        expected_routes = ['ORAL', 'TOPICAL', 'INTRAVENOUS']
        
        for route in expected_routes:
            self.assertIn(route, unique_routes)
    
    def test_ingredient_count_calculation(self):
        """Test ingredient count calculation"""
        df = self.df_sample.copy()
        
        # Calculate ingredient counts
        ingredient_counts = []
        for i in range(len(df)):
            count = calc_avg_ing(df['spl_product_data_elements'].iloc[i])
            ingredient_counts.append(count)
        
        expected_counts = [2, 1, 3]  # Based on our test data
        self.assertEqual(ingredient_counts, expected_counts)
    
    def test_data_validation(self):
        """Test data validation and quality checks"""
        df = self.df_sample.copy()
        
        # Test that all required columns exist
        required_columns = ['openfda.generic_name', 'spl_product_data_elements', 
                          'drug_interactions', 'openfda.manufacturer_name', 
                          'effective_time', 'openfda.route']
        
        for col in required_columns:
            self.assertIn(col, df.columns)
        
        # Test data types
        self.assertTrue(df['effective_time'].dtype == 'object')
        
        # Test that effective_time has correct format
        for date_str in df['effective_time']:
            self.assertEqual(len(date_str), 8)
            self.assertTrue(date_str.isdigit())
    
    def test_correlation_analysis_data_structure(self):
        """Test that data structure supports correlation analysis"""
        # Create a sample processed dataframe
        processed_data = {
            'year': [2020, 2021, 2019, 2020, 2021],
            'num_ingredients': [2, 1, 3, 2, 4]
        }
        df_processed = pd.DataFrame(processed_data)
        
        # Test correlation calculation
        correlation = df_processed.corr()
        
        # Should have correlation between year and num_ingredients
        self.assertIn('year', correlation.columns)
        self.assertIn('num_ingredients', correlation.columns)
        
        # Correlation matrix should be symmetric
        self.assertAlmostEqual(
            correlation.loc['year', 'num_ingredients'],
            correlation.loc['num_ingredients', 'year']
        )
    
    def test_prediction_model_data_preparation(self):
        """Test data preparation for prediction model"""
        # Create sample data for prediction
        prediction_data = {
            'year': [2018, 2019, 2020, 2021, 2022],
            'num_ingredients': [2.5, 2.8, 2.9, 3.1, 3.0]
        }
        df_pred = pd.DataFrame(prediction_data)
        
        # Test data reshaping for sklearn
        X = df_pred['year'].values.reshape(-1, 1)
        y = df_pred['num_ingredients'].values.reshape(-1, 1)
        
        # Check shapes
        self.assertEqual(X.shape, (5, 1))
        self.assertEqual(y.shape, (5, 1))
        
        # Check data types
        self.assertTrue(isinstance(X, np.ndarray))
        self.assertTrue(isinstance(y, np.ndarray))

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and edge cases"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframes"""
        empty_df = pd.DataFrame()
        
        # Should handle empty dataframe gracefully
        self.assertEqual(len(empty_df), 0)
        self.assertEqual(list(empty_df.columns), [])
    
    def test_missing_data_handling(self):
        """Test handling of missing data"""
        data_with_nan = {
            'openfda.generic_name': [['aspirin'], None, ['acetaminophen']],
            'spl_product_data_elements': [['ingredient1,ingredient2'], ['ingredient1'], None],
            'effective_time': ['20200101', '20210101', '20190101']
        }
        df_nan = pd.DataFrame(data_with_nan)
        
        # Test dropna functionality
        df_clean = df_nan.dropna(subset=['openfda.generic_name'])
        self.assertEqual(len(df_clean), 2)  # Should remove the None entry
    
    def test_date_format_validation(self):
        """Test date format validation"""
        invalid_dates = ['2020-01-01', '20201', 'invalid', '202001011']
        valid_dates = ['20200101', '20210315', '19990101']
        
        # Test valid dates
        for date in valid_dates:
            self.assertEqual(len(date), 8)
            self.assertTrue(date.isdigit())
        
        # Test invalid dates
        invalid_count = 0
        for date in invalid_dates:
            if len(date) != 8 or not date.isdigit():
                invalid_count += 1
        
        self.assertEqual(invalid_count, len(invalid_dates))

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestOpenFDAAnalysis))
    test_suite.addTest(unittest.makeSuite(TestDataIntegrity))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")