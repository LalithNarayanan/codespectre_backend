## Analysis of SAS Programs

Here's an analysis of each SAS program, as requested:

### 01_transaction_data_import.sas

*   **PROC Steps:**
    *   `PROC IMPORT`: Imports data from a CSV file.
    *   `PROC SQL`: Used to count records after validation.
    *   `PROC PRINT`: Displays the first 10 validated transactions.
*   **Statistical Analysis Methods:**
    *   Basic validation checks for missing values and invalid amounts.
*   **Predictive Modeling Logic:**
    *   None.
*   **Macro Variable Definitions and Usage:**
    *   `input_path`: Specifies the directory for input files.
    *   `output_lib`: Specifies the output library.
    *   `transaction_file`: Specifies the input CSV filename.
    *   `IMPORT_TRANSACTIONS` macro: Takes `filepath` and `outds` as arguments, imports the CSV, and logs the results. Uses `&SYSERR` to check for errors.
    *   `VALIDATE_DATA` macro: Takes `inds` and `outds` as arguments, validates data (missing values, invalid amounts), and creates a `validation_status` variable.
*   **Report Generation and Formatting Logic:**
    *   `PROC PRINT` displays a sample of the validated data.
    *   Titles are used for the `PROC PRINT` step.
*   **Business Application:**
    *   Initial data import and validation of transaction data.

### 02_data_quality_cleaning.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts data for duplicate removal.
    *   `PROC SQL`: Counts records before and after duplicate removal. Used to calculate the count of removed duplicates.
    *   `PROC MEANS`: Calculates percentiles for outlier handling.
*   **Statistical Analysis Methods:**
    *   Data cleaning and standardization (e.g., `UPCASE`, `PROPCASE`, `STRIP`, `SUBSTR`).
    *   Duplicate removal using `NODUPKEY` option in `PROC SORT`.
    *   Outlier handling using Winsorization (capping values at percentiles) or removal (based on percentiles).
*   **Predictive Modeling Logic:**
    *   None.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input library.
    *   `output_lib`: Specifies the output library.
    *   `CLEAN_TRANSACTIONS` macro: Takes `inds` and `outds` as arguments, cleans and standardizes transaction data (e.g., `transaction_type`, `merchant_name`, `country_code`, handling missing amounts, converting date/time formats).
    *   `REMOVE_DUPLICATES` macro: Takes `inds`, `outds`, and `key` as arguments, sorts and removes duplicate records based on the specified key.
    *   `HANDLE_OUTLIERS` macro: Takes `inds`, `outds`, `var`, and `method` as arguments. Calculates percentiles and applies Winsorization or removal to handle outliers in the specified variable. Uses `SYMPUTX` to create macro variables for percentile values.
*   **Report Generation and Formatting Logic:**
    *   `PROC MEANS` displays descriptive statistics (N, MEAN, STD, MIN, MAX) of the `amount` variable after cleaning.
    *   Titles are used for the `PROC MEANS` step.
*   **Business Application:**
    *   Data cleaning, standardization, duplicate removal, and outlier handling to improve data quality.

### 03_feature_engineering.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts data for rolling window calculations.
    *   `PROC MEANS`: Calculates customer-level statistics (mean, standard deviation, count) for amount deviation.
    *   `PROC SQL`: Merges customer statistics back into the main dataset and creates new variables.
*   **Statistical Analysis Methods:**
    *   Rolling window calculations to compute transaction velocity features.
    *   Calculation of Z-scores and percentage deviation to identify anomalous transactions.
    *   Extraction of time-based features (hour, day of week, day of month, month).
    *   Creation of time-of-day categories and weekend flags.
    *   Creation of location-based features (country transaction counts, rare country flag, international transaction flag).
*   **Predictive Modeling Logic:**
    *   None.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input library.
    *   `output_lib`: Specifies the output library.
    *   `CALCULATE_VELOCITY` macro: Takes `inds`, `outds`, and `window_days` as arguments. Calculates rolling window features (transaction count, total amount, average amount) for a specified time window. Uses `RETAIN` and `FIRST.customer_id` for calculations.
    *   `CALCULATE_AMOUNT_DEVIATION` macro: Takes `inds` and `outds` as arguments. Calculates customer-level average amount, standard deviation, and count.  Calculates amount deviation features (Z-score, % deviation).
    *   `CREATE_TIME_FEATURES` macro: Takes `inds` and `outds` as arguments. Extracts time components and creates time-based features (time of day, weekend flag, unusual hour flag).
    *   `CREATE_LOCATION_FEATURES` macro: Takes `inds` and `outds` as arguments. Calculates country transaction counts and creates location-based features (rare country flag, international transaction flag).
*   **Report Generation and Formatting Logic:**
    *   `PROC PRINT` displays a sample of the engineered features.
    *   Titles are used for the `PROC PRINT` step.
*   **Business Application:**
    *   Feature engineering to create variables that can be used for fraud detection.

### 04_rule_based_detection.sas

*   **PROC Steps:**
    *   `PROC FREQ`: Used to generate frequency tables for risk levels.
    *   `PROC SQL`: Counts alerts and calculates alert rate. Used to generate rule summary report.
    *   `PROC PRINT`: Displays top alerts and rule summary.
*   **Statistical Analysis Methods:**
    *   Rule-based fraud detection using a scoring system.
    *   Rules are defined based on engineered features.
*   **Predictive Modeling Logic:**
    *   Rule-based model for fraud detection.
    *   Each rule triggers a score, and a final risk level is assigned based on the total score.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input library.
    *   `output_lib`: Specifies the output library.
    *   `APPLY_FRAUD_RULES` macro: Takes `inds` and `outds` as arguments. Applies fraud detection rules and calculates a rule score, risk level, and flags suspicious transactions. Uses `CATX` to concatenate rule triggers.
    *   `GENERATE_RULE_ALERTS` macro: Takes `inds`, `outds`, and `threshold` as arguments. Filters transactions based on the rule score and generates alerts.  Calculates alert rate.
    *   `RULE_SUMMARY_REPORT` macro: Takes `inds` as an argument. Creates a summary report of rule triggers using `PROC SQL`.
*   **Report Generation and Formatting Logic:**
    *   `PROC FREQ` generates frequency tables for the risk level.
    *   `PROC PRINT` displays the top alerts.
    *   Titles are used for the `PROC FREQ` and `PROC PRINT` steps.
*   **Business Application:**
    *   Implementation of rule-based fraud detection logic and alert generation.

### 05_ml_scoring_model.sas

*   **PROC Steps:**
    *   `PROC MEANS`: Calculates descriptive statistics for fraud score distribution.
    *   `PROC FREQ`: Generates frequency tables for risk band distribution and alert rate.
    *   `PROC CORR`: Calculates the correlation between ML fraud score and rule score.
    *   `PROC PRINT`: Displays top ML alerts.
*   **Statistical Analysis Methods:**
    *   Data preparation for ML scoring (normalization, handling missing values, creating interaction features).
    *   Simulated logistic regression to calculate an ML fraud score (using pre-defined coefficients).
    *   Score to probability conversion (sigmoid function).
    *   Model performance metrics (score distribution, alert rate, model agreement).
*   **Predictive Modeling Logic:**
    *   Simulated ML model (logistic regression) for fraud scoring.
    *   The model uses prepared features and pre-defined coefficients to calculate the fraud probability and score.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input library.
    *   `output_lib`: Specifies the output library.
    *   `PREPARE_ML_DATA` macro: Takes `inds` and `outds` as arguments. Creates binary flags, normalizes continuous variables, handles missing values, and creates interaction features.
    *   `CALCULATE_ML_SCORE` macro: Takes `inds` and `outds` as arguments. Calculates the logit score using simulated logistic regression coefficients, converts the logit to a fraud probability, and then converts the probability into a fraud score.
    *   `ML_PERFORMANCE_METRICS` macro: Takes `inds` as an argument. Generates ML performance metrics, including score distribution, risk band distribution, and alert rate.
    *   `COMPARE_MODELS` macro: Takes `inds` and `outds` as arguments. Compares ML and rule-based models and creates a model agreement analysis.
*   **Report Generation and Formatting Logic:**
    *   `PROC MEANS` displays descriptive statistics of the fraud score.
    *   `PROC FREQ` generates frequency tables for the risk band and alert rate.
    *   `PROC CORR` calculates the correlation between ML and rule scores.
    *   `PROC PRINT` displays the top ML alerts.
    *   Titles are used for the `PROC MEANS`, `PROC FREQ`, `PROC CORR`, and `PROC PRINT` steps.
    *   `FORMAT` statement is used to format the `ml_fraud_probability` variable.
*   **Business Application:**
    *   Implementation of a simulated ML model for fraud detection and comparison with rule-based detection.

### 06_case_management_output.sas

*   **PROC Steps:**
    *   `PROC SORT`: Sorts the investigation queue.
    *   `PROC SQL`: Counts cases, counts unique customers, generates hourly trend.
    *   `PROC EXPORT`: Exports the investigation queue to a CSV file.
    *   `PROC PRINT`: Displays the investigation queue and SAR cases.
*   **Statistical Analysis Methods:**
    *   Calculation of a final priority score for the investigation queue.
*   **Predictive Modeling Logic:**
    *   Combines ML and rule-based scores to determine the priority of cases.
*   **Macro Variable Definitions and Usage:**
    *   `input_lib`: Specifies the input library.
    *   `output_lib`: Specifies the output library.
    *   `report_path`: Specifies the directory for report exports.
    *   `CREATE_INVESTIGATION_QUEUE` macro: Takes `inds`, `outds`, and `priority_threshold` as arguments. Calculates a priority score, assigns case priority, filters for the investigation queue, generates a case ID, assigns to an investigator, sets the case status, and adds a timestamp.
    *   `GENERATE_DAILY_SUMMARY` macro: Takes `inds` as an argument. Generates a daily summary report with overall statistics, alerts by priority, top customers, and hourly trend.
    *   `EXPORT_INVESTIGATION_QUEUE` macro: Takes `inds` and `filepath` as arguments. Exports the investigation queue to a CSV file.
    *   `GENERATE_SAR_DATA` macro: Takes `inds`, `outds`, and `sar_threshold` as arguments. Filters high-priority cases for SAR filing, adds SAR-specific fields, and generates a SAR narrative.
*   **Report Generation and Formatting Logic:**
    *   `PROC PRINT` displays the investigation queue and SAR cases.
    *   `PROC SQL` generates a daily summary report.
    *   `PROC FREQ` generates frequency tables for the cases by priority level.
    *   `PROC EXPORT` exports the investigation queue to a CSV file.
    *   Titles are used for the `PROC PRINT` steps.
    *   `FORMAT` statement is used to format the `sar_deadline_date` variable.
*   **Business Application:**
    *   Creation of an investigation queue, generation of daily reports, and SAR case generation.
