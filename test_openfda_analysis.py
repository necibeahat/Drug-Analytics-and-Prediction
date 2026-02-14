import unittest
import pandas as pd
import numpy as np
import json
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import warnings

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

class TestCalcAvgIngComprehensive(unittest.TestCase):
    """Comprehensive tests for calc_avg_ing function"""
    
    def test_empty_string_in_list(self):
        """Test with empty string in list"""
        result = calc_avg_ing([''])
        self.assertEqual(result, 1)
    
    def test_single_ingredient(self):
        """Test with single ingredient"""
        result = calc_avg_ing(['aspirin'])
        self.assertEqual(result, 1)
    
    def test_multiple_ingredients(self):
        """Test with multiple ingredients"""
        result = calc_avg_ing(['ing1,ing2,ing3,ing4,ing5'])
        self.assertEqual(result, 5)
    
    def test_special_characters(self):
        """Test with special characters in ingredients"""
        result = calc_avg_ing(['ing@1,ing#2,ing$3'])
        self.assertEqual(result, 3)
    
    def test_whitespace_in_ingredients(self):
        """Test with whitespace in ingredients"""
        result = calc_avg_ing(['ingredient 1, ingredient 2'])
        self.assertEqual(result, 2)
    
    def test_unicode_characters(self):
        """Test with unicode characters"""
        result = calc_avg_ing(['café,naïve,résumé'])
        self.assertEqual(result, 3)
    
    def test_empty_list_raises_error(self):
        """Test that empty list raises IndexError"""
        with self.assertRaises(IndexError):
            calc_avg_ing([])
    
    def test_none_value_raises_error(self):
        """Test that None value raises TypeError"""
        with self.assertRaises(TypeError):
            calc_avg_ing(None)
    
    def test_none_in_list_raises_error(self):
        """Test that None in list raises AttributeError"""
        with self.assertRaises(AttributeError):
            calc_avg_ing([None])
    
    def test_large_ingredient_count(self):
        """Test with large number of ingredients"""
        ingredients = ','.join([f'ing{i}' for i in range(100)])
        result = calc_avg_ing([ingredients])
        self.assertEqual(result, 100)


class TestGetInStrComprehensive(unittest.TestCase):
    """Comprehensive tests for get_in_str function"""
    
    def test_simple_string_list(self):
        """Test with simple string in list"""
        result = get_in_str(['test_drug'])
        self.assertEqual(result, 'test_drug')
    
    def test_comma_separated_list(self):
        """Test with comma-separated values"""
        result = get_in_str(['drug1,drug2,drug3'])
        self.assertEqual(result, 'drug1,drug2,drug3')
    
    def test_nan_value_returns_original(self):
        """Test that NaN value returns original list"""
        nan_list = [np.nan]
        result = get_in_str(nan_list)
        self.assertTrue(isinstance(result, list))
    
    def test_empty_string_list(self):
        """Test with empty string in list"""
        result = get_in_str([''])
        self.assertEqual(result, '')
    
    def test_special_characters(self):
        """Test with special characters"""
        result = get_in_str(['drug@name,drug#2'])
        self.assertEqual(result, 'drug@name,drug#2')
    
    def test_none_value_handling(self):
        """Test handling of None value"""
        result = get_in_str(None)
        self.assertIsNone(result)
    
    def test_empty_list_handling(self):
        """Test handling of empty list"""
        result = get_in_str([])
        self.assertEqual(result, [])
    
    def test_numeric_values(self):
        """Test with numeric values in list"""
        result = get_in_str([123])
        self.assertEqual(result, [123])


class TestProcessOpenfdaDataComprehensive(unittest.TestCase):
    """Comprehensive tests for process_openfda_data function"""
    
    def setUp(self):
        """Set up valid test DataFrame"""
        self.valid_data = {
            'openfda.generic_name': [['aspirin'], ['ibuprofen']],
            'spl_product_data_elements': [['ing1,ing2'], ['ing1']],
            'drug_interactions': [['interaction1'], ['interaction2']],
            'openfda.manufacturer_name': [['Pfizer'], ['Bayer']],
            'effective_time': ['20200101', '20210315'],
            'openfda.route': [['ORAL'], ['TOPICAL']]
        }
        self.valid_df = pd.DataFrame(self.valid_data)
    
    def test_valid_dataframe_processing(self):
        """Test processing valid DataFrame"""
        result = process_openfda_data(self.valid_df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('year', result.columns)
        self.assertIn('num_ingredients', result.columns)
    
    def test_invalid_date_filtering(self):
        """Test that invalid dates are filtered out"""
        data = self.valid_data.copy()
        data['effective_time'] = ['20200101', '2021']  # Second date invalid
        df = pd.DataFrame(data)
        result = process_openfda_data(df)
        self.assertEqual(len(result), 1)
    
    def test_nan_filtering(self):
        """Test that NaN values are filtered"""
        data = self.valid_data.copy()
        data['spl_product_data_elements'] = [['ing1,ing2'], None]
        df = pd.DataFrame(data)
        result = process_openfda_data(df)
        self.assertEqual(len(result), 1)
    
    def test_output_dtypes(self):
        """Test output data types"""
        result = process_openfda_data(self.valid_df)
        self.assertEqual(result['year'].dtype, np.int64)
        self.assertEqual(result['num_ingredients'].dtype, np.int64)
    
    def test_year_extraction(self):
        """Test year is correctly extracted"""
        result = process_openfda_data(self.valid_df)
        self.assertIn(2020, result['year'].values)
        self.assertIn(2021, result['year'].values)


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


class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def test_calc_avg_ing_with_integer(self):
        """Test calc_avg_ing with integer input"""
        with self.assertRaises(TypeError):
            calc_avg_ing(123)
    
    def test_calc_avg_ing_with_dict(self):
        """Test calc_avg_ing with dict input"""
        with self.assertRaises(KeyError):
            calc_avg_ing({'key': 'value'})
    
    def test_get_in_str_with_nested_list(self):
        """Test get_in_str with nested list"""
        result = get_in_str([['nested', 'list']])
        self.assertIsNotNone(result)
    
    def test_process_openfda_missing_columns(self):
        """Test process_openfda_data with missing columns"""
        df = pd.DataFrame({'wrong_col': [1, 2, 3]})
        with self.assertRaises(KeyError):
            process_openfda_data(df)
    
    def test_filter_by_manufacturer_empty_result(self):
        """Test filter when no manufacturer matches"""
        df = pd.DataFrame({
            'manufacturer': ['Pfizer', 'Bayer'],
            'num_ingredients': [2, 3]
        })
        result = filter_by_manufacturer(df, 'NonExistent')
        self.assertEqual(len(result), 0)


class TestIntegrationPipeline(unittest.TestCase):
    """Integration tests for data processing pipeline"""
    
    def setUp(self):
        """Set up integration test data"""
        self.pipeline_data = {
            'openfda.generic_name': [['aspirin'], ['ibuprofen'], ['acetaminophen']],
            'spl_product_data_elements': [['a,b,c'], ['x,y'], ['p,q,r,s']],
            'drug_interactions': [['int1'], ['int2'], ['int3']],
            'openfda.manufacturer_name': [['Pfizer'], ['Pfizer'], ['Bayer']],
            'effective_time': ['20200101', '20200601', '20210101'],
            'openfda.route': [['ORAL'], ['ORAL'], ['TOPICAL']]
        }
        self.pipeline_df = pd.DataFrame(self.pipeline_data)
    
    def test_end_to_end_processing(self):
        """Test complete data processing pipeline"""
        processed = process_openfda_data(self.pipeline_df)
        self.assertEqual(len(processed), 3)
        self.assertTrue(all(col in processed.columns for col in 
                          ['year', 'drug_names', 'num_ingredients', 'route', 'manufacturer']))
    
    def test_processing_then_filtering(self):
        """Test processing followed by manufacturer filtering"""
        processed = process_openfda_data(self.pipeline_df)
        filtered = filter_by_manufacturer(processed, 'Pfizer')
        self.assertEqual(len(filtered), 2)
    
    def test_processing_then_analysis(self):
        """Test processing followed by yearly analysis"""
        processed = process_openfda_data(self.pipeline_df)
        analysis = analyze_ingredients_by_year(processed)
        self.assertIn('avg_ingredients', analysis.columns)
    
    def test_prediction_model_creation(self):
        """Test prediction model with processed data"""
        processed = process_openfda_data(self.pipeline_df)
        model_result = create_prediction_model(processed)
        self.assertIn('model', model_result)
        self.assertIn('metrics', model_result)
    
    def test_summary_report_generation(self):
        """Test summary report generation"""
        processed = process_openfda_data(self.pipeline_df)
        report = generate_summary_report(processed)
        self.assertIn('dataset_info', report)
        self.assertIn('ingredient_statistics', report)


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestOpenFDAAnalysis))
    test_suite.addTest(unittest.makeSuite(TestCalcAvgIngComprehensive))
    test_suite.addTest(unittest.makeSuite(TestGetInStrComprehensive))
    test_suite.addTest(unittest.makeSuite(TestProcessOpenfdaDataComprehensive))
    test_suite.addTest(unittest.makeSuite(TestDataIntegrity))
    test_suite.addTest(unittest.makeSuite(TestErrorHandling))
    test_suite.addTest(unittest.makeSuite(TestIntegrationPipeline))
    
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