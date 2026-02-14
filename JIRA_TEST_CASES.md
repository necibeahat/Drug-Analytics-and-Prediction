# JIRA Test Cases - Drug Analytics and Prediction

## Overview
This document contains test cases for the OpenFDA Drug Data Analysis functions in Jira-friendly acceptance criteria format.

---

## calc_avg_ing Function Tests

### TC-001: Empty String in List
**Description:** Verify calc_avg_ing handles empty string in list  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an ingredient list containing an empty string `['']`
- **When** calc_avg_ing is called with this input
- **Then** the function returns 1

**Expected Result:** Returns integer value 1  
**Validation:** Assert return value equals 1

---

### TC-002: Single Ingredient
**Description:** Verify calc_avg_ing counts single ingredient correctly  
**Priority:** High

**Acceptance Criteria:**
- **Given** an ingredient list with single item `['aspirin']`
- **When** calc_avg_ing is called
- **Then** the function returns 1

**Expected Result:** Returns integer value 1  
**Validation:** Assert return value equals 1

---

### TC-003: Multiple Ingredients
**Description:** Verify calc_avg_ing counts multiple comma-separated ingredients  
**Priority:** High

**Acceptance Criteria:**
- **Given** an ingredient list `['ing1,ing2,ing3,ing4,ing5']`
- **When** calc_avg_ing is called
- **Then** the function returns 5

**Expected Result:** Returns integer value 5  
**Validation:** Assert return value equals expected count

---

### TC-004: Special Characters in Ingredients
**Description:** Verify calc_avg_ing handles special characters  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an ingredient list with special characters `['ing@1,ing#2,ing$3']`
- **When** calc_avg_ing is called
- **Then** the function returns 3

**Expected Result:** Returns integer value 3  
**Validation:** Assert return value equals 3

---

### TC-005: Empty List Error Handling
**Description:** Verify calc_avg_ing raises IndexError for empty list  
**Priority:** High

**Acceptance Criteria:**
- **Given** an empty list `[]`
- **When** calc_avg_ing is called
- **Then** IndexError is raised

**Expected Result:** IndexError exception  
**Validation:** Assert IndexError is raised

---

### TC-006: None Value Error Handling
**Description:** Verify calc_avg_ing raises TypeError for None input  
**Priority:** High

**Acceptance Criteria:**
- **Given** None as input
- **When** calc_avg_ing is called
- **Then** TypeError is raised

**Expected Result:** TypeError exception  
**Validation:** Assert TypeError is raised

---

### TC-007: Unicode Characters
**Description:** Verify calc_avg_ing handles unicode characters  
**Priority:** Low

**Acceptance Criteria:**
- **Given** an ingredient list with unicode `['café,naïve,résumé']`
- **When** calc_avg_ing is called
- **Then** the function returns 3

**Expected Result:** Returns integer value 3  
**Validation:** Assert return value equals 3

---

### TC-008: Large Ingredient Count
**Description:** Verify calc_avg_ing handles large number of ingredients  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an ingredient list with 100 comma-separated items
- **When** calc_avg_ing is called
- **Then** the function returns 100

**Expected Result:** Returns integer value 100  
**Validation:** Assert return value equals 100

---

## get_in_str Function Tests

### TC-009: Simple String List
**Description:** Verify get_in_str returns string from simple list  
**Priority:** High

**Acceptance Criteria:**
- **Given** a list with single string `['test_drug']`
- **When** get_in_str is called
- **Then** the function returns 'test_drug'

**Expected Result:** Returns string 'test_drug'  
**Validation:** Assert return value equals expected string

---

### TC-010: NaN Value Handling
**Description:** Verify get_in_str returns original list for NaN values  
**Priority:** High

**Acceptance Criteria:**
- **Given** a list containing NaN value `[np.nan]`
- **When** get_in_str is called
- **Then** the function returns the original list

**Expected Result:** Returns list type  
**Validation:** Assert return type is list

---

### TC-011: None Value Handling
**Description:** Verify get_in_str handles None input gracefully  
**Priority:** High

**Acceptance Criteria:**
- **Given** None as input
- **When** get_in_str is called
- **Then** the function returns None

**Expected Result:** Returns None  
**Validation:** Assert return value is None

---

### TC-012: Empty List Handling
**Description:** Verify get_in_str handles empty list  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an empty list `[]`
- **When** get_in_str is called
- **Then** the function returns empty list

**Expected Result:** Returns empty list  
**Validation:** Assert return value equals []

---

### TC-013: Comma-Separated Values
**Description:** Verify get_in_str preserves comma-separated format  
**Priority:** High

**Acceptance Criteria:**
- **Given** a list with comma-separated string `['drug1,drug2,drug3']`
- **When** get_in_str is called
- **Then** the function returns 'drug1,drug2,drug3'

**Expected Result:** Returns preserved string  
**Validation:** Assert return value equals input string

---

## process_openfda_data Function Tests

### TC-014: Valid DataFrame Processing
**Description:** Verify process_openfda_data processes valid DataFrame  
**Priority:** Critical

**Acceptance Criteria:**
- **Given** a valid DataFrame with all required columns
- **When** process_openfda_data is called
- **Then** the function returns processed DataFrame with year and num_ingredients columns

**Expected Result:** DataFrame with expected columns  
**Validation:** Assert DataFrame contains 'year' and 'num_ingredients' columns

---

### TC-015: Invalid Date Filtering
**Description:** Verify process_openfda_data filters invalid dates  
**Priority:** High

**Acceptance Criteria:**
- **Given** a DataFrame with some invalid effective_time values (not 8 characters)
- **When** process_openfda_data is called
- **Then** rows with invalid dates are filtered out

**Expected Result:** Only valid date rows remain  
**Validation:** Assert result length matches valid date count

---

### TC-016: NaN Value Filtering
**Description:** Verify process_openfda_data filters NaN values  
**Priority:** High

**Acceptance Criteria:**
- **Given** a DataFrame with NaN values in spl_product_data_elements
- **When** process_openfda_data is called
- **Then** rows with NaN are filtered out

**Expected Result:** Only non-NaN rows remain  
**Validation:** Assert result excludes NaN rows

---

### TC-017: Output Data Types
**Description:** Verify process_openfda_data returns correct data types  
**Priority:** High

**Acceptance Criteria:**
- **Given** a valid input DataFrame
- **When** process_openfda_data is called
- **Then** year and num_ingredients columns are int64 type

**Expected Result:** int64 data types  
**Validation:** Assert dtypes match np.int64

---

### TC-018: Missing Columns Error
**Description:** Verify process_openfda_data raises error for missing columns  
**Priority:** High

**Acceptance Criteria:**
- **Given** a DataFrame missing required columns
- **When** process_openfda_data is called
- **Then** KeyError is raised

**Expected Result:** KeyError exception  
**Validation:** Assert KeyError is raised

---

## Integration Tests

### TC-019: End-to-End Processing Pipeline
**Description:** Verify complete data processing pipeline  
**Priority:** Critical

**Acceptance Criteria:**
- **Given** a raw OpenFDA-style DataFrame
- **When** process_openfda_data is called
- **Then** output contains all expected columns: year, drug_names, num_ingredients, route, manufacturer

**Expected Result:** Complete processed DataFrame  
**Validation:** Assert all required columns present

---

### TC-020: Processing Then Filtering
**Description:** Verify processing followed by manufacturer filtering  
**Priority:** High

**Acceptance Criteria:**
- **Given** processed DataFrame with multiple manufacturers
- **When** filter_by_manufacturer is called with specific manufacturer
- **Then** only matching manufacturer rows are returned

**Expected Result:** Filtered DataFrame  
**Validation:** Assert filtered count matches expected

---

### TC-021: Processing Then Analysis
**Description:** Verify processing followed by yearly analysis  
**Priority:** High

**Acceptance Criteria:**
- **Given** a processed DataFrame
- **When** analyze_ingredients_by_year is called
- **Then** result contains avg_ingredients column

**Expected Result:** Analysis DataFrame with avg_ingredients  
**Validation:** Assert 'avg_ingredients' in columns

---

### TC-022: Prediction Model Creation
**Description:** Verify prediction model creation from processed data  
**Priority:** High

**Acceptance Criteria:**
- **Given** a processed DataFrame
- **When** create_prediction_model is called
- **Then** result contains model and metrics keys

**Expected Result:** Dictionary with model and metrics  
**Validation:** Assert 'model' and 'metrics' keys present

---

### TC-023: Summary Report Generation
**Description:** Verify summary report generation  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** a processed DataFrame
- **When** generate_summary_report is called
- **Then** result contains dataset_info and ingredient_statistics

**Expected Result:** Report dictionary with expected keys  
**Validation:** Assert required keys present

---

## Error Handling Tests

### TC-024: Invalid Input Type - Integer
**Description:** Verify calc_avg_ing rejects integer input  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an integer value 123
- **When** calc_avg_ing is called
- **Then** TypeError is raised

**Expected Result:** TypeError exception  
**Validation:** Assert TypeError is raised

---

### TC-025: Invalid Input Type - Dictionary
**Description:** Verify calc_avg_ing rejects dictionary input  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** a dictionary {'key': 'value'}
- **When** calc_avg_ing is called
- **Then** KeyError is raised

**Expected Result:** KeyError exception  
**Validation:** Assert KeyError is raised

---

### TC-026: Empty Manufacturer Filter Result
**Description:** Verify filter_by_manufacturer handles no matches  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** a DataFrame with manufacturers Pfizer and Bayer
- **When** filter_by_manufacturer is called with 'NonExistent'
- **Then** empty DataFrame is returned

**Expected Result:** Empty DataFrame (length 0)  
**Validation:** Assert result length equals 0

---

## Data Integrity Tests

### TC-027: Empty DataFrame Handling
**Description:** Verify handling of empty DataFrames  
**Priority:** Medium

**Acceptance Criteria:**
- **Given** an empty DataFrame
- **When** length and columns are checked
- **Then** length is 0 and columns list is empty

**Expected Result:** Length 0, empty columns  
**Validation:** Assert len(df) == 0 and list(df.columns) == []

---

### TC-028: Date Format Validation
**Description:** Verify date format validation logic  
**Priority:** High

**Acceptance Criteria:**
- **Given** valid dates (8-digit strings) and invalid dates
- **When** validation is applied
- **Then** valid dates pass (length 8, all digits), invalid dates fail

**Expected Result:** Correct validation results  
**Validation:** Assert validation logic works correctly

---

## Test Summary

| Category | Test Cases | Priority Distribution |
|----------|------------|----------------------|
| calc_avg_ing | TC-001 to TC-008 | Critical: 0, High: 3, Medium: 4, Low: 1 |
| get_in_str | TC-009 to TC-013 | Critical: 0, High: 4, Medium: 1, Low: 0 |
| process_openfda_data | TC-014 to TC-018 | Critical: 1, High: 4, Medium: 0, Low: 0 |
| Integration | TC-019 to TC-023 | Critical: 1, High: 3, Medium: 1, Low: 0 |
| Error Handling | TC-024 to TC-026 | Critical: 0, High: 0, Medium: 3, Low: 0 |
| Data Integrity | TC-027 to TC-028 | Critical: 0, High: 1, Medium: 1, Low: 0 |

**Total Test Cases:** 28  
**Total Tests in Suite:** 45 (including subtests)
