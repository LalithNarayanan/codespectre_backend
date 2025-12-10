## Analysis of SAS Programs

Here's an analysis of each SAS program, as requested:

### 01_transaction_data_import.sas

*   **PROC Steps:**
    *   `PROC IMPORT`: Imports data from a CSV file.
    *   `PROC SQL`: Used to count records after validation.
    *   `PROC PRINT`: Displays the first 10 validated transactions.
*   **Statistical Analysis Methods:**
    *   Basic data validation checks (missing values, invalid amounts).
*   **Predictive Modeling Logic:**
    *   None.
*   **Macro Variable Definitions and Usage:**
    *   `input_path`: Specifies the directory for input CSV files.
    *   `output_lib`: Defines the SAS library for output datasets.
    *   `transaction_file`: Specifies the name of the transaction CSV file.
    *   `IMPORT_TRANSACTIONS` macro: Imports CSV data and checks for import errors.
    *   `VALIDATE_DATA` macro: Performs data validation (missing values, invalid amounts).
*   **Report Generation and Formatting Logic:**
    *   `PROC PRINT` is used to display a sample of the validated data.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Initial data loading and validation of transaction data.

### 02_data_quality_cleaning.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts data to remove duplicates.
    *   `PROC SQL`: Used to count records before and after duplicate removal.
    *   `PROC MEANS`: Calculates percentiles for outlier handling.
    *   `PROC PRINT`: Displays descriptive statistics of the cleaned data.
*   **Statistical Analysis Methods:**
    *   Data cleaning and standardization (transaction type, merchant name, country code).
    *   Duplicate record removal.
    *   Outlier handling (Winsorizing and optionally removing).
    *   Descriptive statistics (mean, standard deviation, min, max).
*   **Predictive Modeling Logic:**
    *   None.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`:  Specifies the input SAS library.
    *   `output_lib`: Specifies the output SAS library.
    *   `CLEAN_TRANSACTIONS` macro: Standardizes and cleans various transaction fields.
    *   `REMOVE_DUPLICATES` macro: Removes duplicate records based on a specified key.
    *   `HANDLE_OUTLIERS` macro: Handles outliers using Winsorizing or removal, based on percentiles.
*   **Report Generation and Formatting Logic:**
    *   `PROC MEANS` is used to display descriptive statistics of the cleaned data.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Cleaning and standardizing transaction data to improve data quality.

### 03_feature_engineering.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts data for time-based calculations.
    *   `PROC MEANS`: Calculates customer-level statistics.
    *   `PROC SQL`: Calculates and merges data for feature engineering.
    *   `PROC PRINT`: Displays a sample of the engineered features.
*   **Statistical Analysis Methods:**
    *   Rolling window calculations (transaction velocity).
    *   Customer-level statistics (mean, standard deviation) for deviation calculations.
    *   Time-based feature creation (hour, day of week, month, time of day, weekend flag).
    *   Location-based feature creation (country transaction counts, rare country flag, international transaction flag).
*   **Predictive Modeling Logic:**
    *   The features created in this step will be used in the fraud detection model.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input SAS library.
    *   `output_lib`: Specifies the output SAS library.
    *   `CALCULATE_VELOCITY` macro: Calculates velocity features (transaction counts and amounts within a rolling window).
    *   `CALCULATE_AMOUNT_DEVIATION` macro: Calculates amount deviation features (z-score, percentage deviation).
    *   `CREATE_TIME_FEATURES` macro: Creates time-based features.
    *   `CREATE_LOCATION_FEATURES` macro: Creates location-based features.
*   **Report Generation and Formatting Logic:**
    *   `PROC PRINT` is used to display a sample of the engineered features.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Creating new features from existing data to improve fraud detection performance.

### 04_rule_based_detection.sas

*   **PROC Steps:**
    *   `PROC FREQ`: Generates frequency tables for alert counts.
    *   `PROC SQL`: Counts alerts and calculates alert rates.
    *   `PROC PRINT`: Displays a sample of alerts and a summary of triggered rules.
*   **Statistical Analysis Methods:**
    *   Rule-based fraud detection.
    *   Calculation of rule scores and risk levels.
    *   Frequency analysis of alerts.
*   **Predictive Modeling Logic:**
    *   Rule-based fraud detection is a form of predictive modeling.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input SAS library.
    *   `output_lib`: Specifies the output SAS library.
    *   `APPLY_FRAUD_RULES` macro: Implements fraud detection rules and calculates a rule score and risk level.
    *   `GENERATE_RULE_ALERTS` macro: Filters transactions based on the rule score and generates alerts.
    *   `RULE_SUMMARY_REPORT` macro: Summarizes the number of times each rule was triggered.
*   **Report Generation and Formatting Logic:**
    *   `PROC FREQ` is used to generate frequency tables of rule-based alerts.
    *   `PROC PRINT` is used to display the top alerts and the rule summary.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Implementing a rule-based fraud detection system.

### 05_ml_scoring_model.sas

*   **PROC Steps:**
    *   `PROC MEANS`: Calculates distribution statistics of fraud scores.
    *   `PROC FREQ`: Generates frequency tables for alert rates and risk bands.
    *   `PROC CORR`: Calculates the correlation between ML and rule scores.
    *   `PROC PRINT`: Displays a sample of ML-based alerts.
*   **Statistical Analysis Methods:**
    *   Simulated logistic regression (ML model).
    *   Calculation of an ML fraud score and risk band.
    *   Model performance metrics (distribution of scores, alert rate).
    *   Model comparison (ML vs. rule-based).
    *   Correlation analysis.
*   **Predictive Modeling Logic:**
    *   Simulated logistic regression model for fraud scoring.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input SAS library.
    *   `output_lib`: Specifies the output SAS library.
    *   `PREPARE_ML_DATA` macro: Prepares data for the ML model (feature creation, normalization, handling missing values).
    *   `CALCULATE_ML_SCORE` macro: Calculates the ML fraud score and risk band based on simulated logistic regression coefficients.
    *   `ML_PERFORMANCE_METRICS` macro: Generates performance metrics for the ML model (distribution of scores, alert rate).
    *   `COMPARE_MODELS` macro: Compares the ML model to the rule-based model.
*   **Report Generation and Formatting Logic:**
    *   `PROC MEANS`, `PROC FREQ`, and `PROC CORR` are used to generate model performance metrics.
    *   `PROC PRINT` is used to display the top ML-based alerts.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Implementing an ML-based fraud detection system.

### 06_case_management_output.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts data for the investigation queue.
    *   `PROC SQL`: Calculates statistics and creates tables for reporting.
    *   `PROC FREQ`: Generates frequency tables for daily summaries.
    *   `PROC EXPORT`: Exports the investigation queue to a CSV file.
    *   `PROC PRINT`: Displays the investigation queue and SAR cases.
*   **Statistical Analysis Methods:**
    *   Calculating a combined score based on ML and rule-based scores.
    *   Case prioritization.
    *   Daily summary statistics.
*   **Predictive Modeling Logic:**
    *   Combines the results of the ML and rule-based models to generate a final risk assessment.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input SAS library.
    *   `output_lib`: Specifies the output SAS library.
    *   `report_path`: Specifies the directory for report exports.
    *   `CREATE_INVESTIGATION_QUEUE` macro: Creates an investigation queue based on the final scores.
    *   `GENERATE_DAILY_SUMMARY` macro: Generates a daily fraud detection summary report.
    *   `EXPORT_INVESTIGATION_QUEUE` macro: Exports the investigation queue to a CSV file.
    *   `GENERATE_SAR_DATA` macro: Generates data for Suspicious Activity Reports (SARs).
*   **Report Generation and Formatting Logic:**
    *   `PROC FREQ`, `PROC PRINT` are used to generate the daily summary report.
    *   `PROC EXPORT` is used to export the investigation queue to a CSV file.
    *   Titles are used to describe the output.
*   **Business Application:**
    *   Generating a case management queue for fraud investigations.
    *   Creating reports and summaries of fraud detection activity.
    *   Generating data for SAR filings.
