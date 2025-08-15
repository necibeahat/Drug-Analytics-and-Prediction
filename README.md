# OpenFDA Drug Data Analysis and Prediction

A comprehensive data analytics project that analyzes pharmaceutical drug data from the OpenFDA database, focusing on drug ingredients, delivery routes, and manufacturer-specific insights with predictive modeling capabilities.

## Project Overview

This project performs in-depth analysis of OpenFDA drug label data to extract meaningful insights about pharmaceutical products, including:

- Analysis of drug ingredient complexity over time
- Manufacturer-specific drug composition analysis (with focus on AstraZeneca)
- Delivery route analysis across all manufacturers
- Predictive modeling for future drug ingredient trends
- Drug interaction analysis

## Features

### Core Analysis Components

**Part A: AstraZeneca Analysis**
- Average number of ingredients in AstraZeneca medicines per year
- Temporal trends in drug complexity
- Statistical analysis with descriptive statistics

**Part B: Cross-Manufacturer Analysis**
- Average number of ingredients per year across all manufacturers
- Analysis by delivery route (oral, topical, intravenous, etc.)
- Comparative analysis of administration methods

**Optional Advanced Analysis**
- Linear regression model for predicting ingredient counts
- Drug interaction analysis for AstraZeneca products
- Text processing and pattern matching for drug interactions

### Data Processing Pipeline

1. **Data Ingestion**: Loads multiple OpenFDA JSON files (9 files total)
2. **Data Cleaning**: 
   - Removes invalid date formats
   - Handles missing values
   - Converts list data to strings
   - Calculates ingredient counts from product data elements
3. **Feature Engineering**: Creates derived features like year extraction and ingredient counting
4. **Data Validation**: Ensures data quality and consistency

## Technical Stack

- **Python 3.7+**
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Machine Learning**: scikit-learn
- **Data Format**: JSON processing
- **Text Processing**: Regular expressions (re module)

## Installation and Setup

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd openfda-drug-analysis

# Run the setup script
python setup.py
```

### Manual Setup

#### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

#### Alternative using requirements.txt
```bash
pip install -r requirements.txt
```

### Data Requirements

The project expects OpenFDA drug label data files in the following format:
- `drug-label-0001-of-0009.json` through `drug-label-0009-of-0009.json`
- Files should be placed in a `Data Source/` directory

**Note**: If you don't have the actual OpenFDA data files, you can still run the example script which uses synthetic data for demonstration purposes.

### Running the Analysis

1. **With actual OpenFDA data**:
   ```bash
   # Place data files in 'Data Source' directory
   jupyter notebook OpenFDA_DrugEndPointAnalysis.ipynb
   ```

2. **With synthetic data (for testing/demo)**:
   ```bash
   python example_usage.py
   ```

3. **Running tests**:
   ```bash
   python test_openfda_analysis.py
   ```

## Key Insights and Findings

### Data Statistics
- **Total Records**: 162,807 drug entries
- **Date Range**: 1978-2022
- **Average Ingredients**: ~2.9 ingredients per drug
- **Correlation**: Weak negative correlation (-0.016) between year and ingredient count

### Visualization Outputs
- Correlation matrices showing relationships between variables
- Time series plots of ingredient trends
- Distribution histograms of ingredient counts
- Pie charts showing delivery route frequencies
- Scatter plots for predictive model validation

### Predictive Model Performance
- **Model**: Linear Regression
- **Features**: Year as predictor variable
- **Target**: Number of ingredients
- **Performance Metrics**:
  - Mean Absolute Error: ~2.07
  - Root Mean Squared Error: ~4.31

## File Structure

```
/workspace/
├── README.md                           # This file
├── OpenFDA_DrugEndPointAnalysis.ipynb  # Main analysis notebook
├── openfda_functions.py                # Core analysis functions module
├── test_openfda_analysis.py            # Unit tests for the functions
├── example_usage.py                    # Example script demonstrating usage
├── requirements.txt                    # Python dependencies
└── Data Source/                        # Data directory (not included)
    ├── drug-label-0001-of-0009.json
    ├── drug-label-0002-of-0009.json
    └── ... (additional data files)
```

## Usage Examples

### Running the Jupyter Notebook
The notebook provides step-by-step analysis with clear markdown explanations for each section.

### Using the Python Functions
```python
from openfda_functions import (
    load_openfda_data, process_openfda_data, 
    analyze_ingredients_by_year, create_prediction_model
)

# Load and process data
raw_data = load_openfda_data('path/to/data')
processed_data = process_openfda_data(raw_data)

# Analyze by manufacturer
az_analysis = analyze_ingredients_by_year(processed_data, 'AstraZeneca')

# Create prediction model
model_results = create_prediction_model(processed_data)
```

### Running the Example Script
```bash
python example_usage.py
```

### Running Tests
```bash
python -m pytest test_openfda_analysis.py -v
# or
python test_openfda_analysis.py
```

### Custom Analysis
Users can modify the analysis by:
- Changing the manufacturer filter (currently set to AstraZeneca)
- Adjusting the delivery route analysis parameters
- Modifying the prediction model features
- Customizing visualization parameters

## Data Sources

- **Primary Source**: OpenFDA Drug Labels API
- **Data Format**: JSON files containing drug label information
- **Key Fields**: 
  - `openfda.generic_name`: Drug generic names
  - `spl_product_data_elements`: Product composition data
  - `drug_interactions`: Drug interaction information
  - `openfda.manufacturer_name`: Manufacturer information
  - `effective_time`: Drug approval/effective dates
  - `openfda.route`: Administration routes

## Future Enhancements

- Integration with real-time OpenFDA API
- Advanced machine learning models (Random Forest, Neural Networks)
- Interactive dashboard development
- Automated report generation
- Extended manufacturer analysis beyond AstraZeneca
- Drug safety signal detection
- Regulatory compliance analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate tests and documentation
5. Submit a pull request

## License

This project is intended for educational and research purposes. Please ensure compliance with OpenFDA data usage policies.

## Contact

For questions or collaboration opportunities, please open an issue in the repository.

---

*Note: This analysis is based on publicly available OpenFDA data and is intended for research and educational purposes only. Results should not be used for medical decision-making without proper validation and expert consultation.*
