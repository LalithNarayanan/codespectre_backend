## Analysis of SAS Programs

Here's an analysis of the provided SAS programs, addressing the requested details:

### List of SAS Programs Analyzed

1.  `01_transaction_data_import.sas`
2.  `02_data_quality_cleaning.sas`
3.  `03_feature_engineering.sas`
4.  `04_rule_based_detection.sas`
5.  `05_ml_scoring_model.sas`
6.  `06_case_management_output.sas`

### Execution Sequence and Step Descriptions

The programs are designed as a pipeline, with each program building upon the outputs of the previous ones. Here's the execution sequence, step by step:

1.  **01_transaction_data_import.sas:**
    *   **Macro `IMPORT_TRANSACTIONS`:** Imports transaction data from a CSV file into a SAS dataset. Performs basic import validation using `SYSERR`.
    *   **Macro `VALIDATE_DATA`:** Validates the imported data for missing values and invalid amounts. Keeps only valid records.
    *   **PROC PRINT:** Displays the first 10 validated transactions.

2.  **02_data_quality_cleaning.sas:**
    *   **Macro `CLEAN_TRANSACTIONS`:** Cleans and standardizes transaction data, including transaction type, merchant name, and country code. Handles missing amounts and converts the transaction date to the correct format. Creates a transaction timestamp.
    *   **Macro `REMOVE_DUPLICATES`:** Removes duplicate records based on the transaction ID.
    *   **Macro `HANDLE_OUTLIERS`:** Handles outliers in the amount variable using winsorization.
    *   **PROC MEANS:** Calculates and displays statistics on the amount variable after the cleaning process.

3.  **03_feature_engineering.sas:**
    *   **Macro `CALCULATE_VELOCITY`:** Calculates velocity features (transaction count and average amount) within a rolling window of specified days.
    *   **Macro `CALCULATE_AMOUNT_DEVIATION`:** Calculates amount deviation features, including customer average amount, standard deviation, Z-score, and percentage deviation.
    *   **Macro `CREATE_TIME_FEATURES`:** Creates time-based features like hour, day of the week, day of the month, month, time of day, and a weekend flag.
    *   **Macro `CREATE_LOCATION_FEATURES`:** Creates location-based features, including country transaction counts, a flag for rare countries, and a flag for international transactions.
    *   **PROC PRINT:** Displays a sample of the engineered features.

4.  **04_rule_based_detection.sas:**
    *   **Macro `APPLY_FRAUD_RULES`:** Applies rule-based fraud detection logic using a series of `IF` statements. Calculates a rule score and identifies triggered rules. Determines a rule-based risk level and a flag for investigation.
    *   **Macro `GENERATE_RULE_ALERTS`:** Filters transactions based on the rule score, sorts the data, and generates frequency tables to summarize alerts by risk level. Calculates and logs the alert rate.
    *   **Macro `RULE_SUMMARY_REPORT`:** Creates a summary table counting how many times each rule was triggered.
    *   **PROC PRINT:** Displays the top 20 rule-based fraud alerts.

5.  **05_ml_scoring_model.sas:**
    *   **Macro `PREPARE_ML_DATA`:** Prepares data for ML scoring, including creating binary flags, normalizing continuous variables, and handling missing values. Creates interaction features.
    *   **Macro `CALCULATE_ML_SCORE`:** Calculates an ML fraud score using a simulated logistic regression model. Converts logit to probability and then to a fraud score. Assigns an ML risk band and creates an ML alert flag.
    *   **Macro `ML_PERFORMANCE_METRICS`:** Generates performance metrics, including the distribution of scores, distribution by risk band, and the alert rate.
    *   **Macro `COMPARE_MODELS`:** Compares the ML model results with the rule-based results. Calculates a combined score, categorizes agreement, and performs correlation analysis.
    *   **PROC PRINT:** Displays the top 20 ML-based fraud alerts.

6.  **06_case_management_output.sas:**
    *   **Macro `CREATE_INVESTIGATION_QUEUE`:** Creates an investigation queue based on a combined score (ML and rule-based), adds urgency factors, assigns priorities, and filters the data. Generates a case ID, investigation reason, and assigns cases to investigators. Sets case status and adds timestamps.
    *   **Macro `GENERATE_DAILY_SUMMARY`:** Generates a daily fraud detection summary report, including overall statistics, alerts by priority, a list of top customers, and an hourly alert trend.
    *   **Macro `EXPORT_INVESTIGATION_QUEUE`:** Exports the investigation queue to a CSV file.
    *   **Macro `GENERATE_SAR_DATA`:** Generates data for Suspicious Activity Report (SAR) cases based on a threshold. Adds SAR-specific fields and creates a narrative.
    *   **PROC PRINT:** Displays the top 50 cases in the investigation queue and SAR cases requiring filing.

### Dataset Dependencies

*   `01_transaction_data_import.sas`:
    *   `raw_transactions` (output from `IMPORT_TRANSACTIONS`)
    *   `transactions_validated` (output from `VALIDATE_DATA`)
*   `02_data_quality_cleaning.sas`:
    *   `transactions_validated` (input), created in `01_transaction_data_import.sas`
    *   `transactions_cleaned` (output from `CLEAN_TRANSACTIONS`)
    *   `transactions_deduped` (output from `REMOVE_DUPLICATES`)
    *   `transactions_final` (output from `HANDLE_OUTLIERS`)
*   `03_feature_engineering.sas`:
    *   `transactions_final` (input), created in `02_data_quality_cleaning.sas`
    *   `txn_with_velocity` (output from `CALCULATE_VELOCITY`)
    *   `txn_with_deviation` (output from `CALCULATE_AMOUNT_DEVIATION`)
    *   `txn_with_time_features` (output from `CREATE_TIME_FEATURES`)
    *   `transactions_engineered` (output from `CREATE_LOCATION_FEATURES`)
*   `04_rule_based_detection.sas`:
    *   `transactions_engineered` (input), created in `03_feature_engineering.sas`
    *   `transactions_with_rules` (output from `APPLY_FRAUD_RULES`)
    *   `rule_based_alerts` (output from `GENERATE_RULE_ALERTS`)
*   `05_ml_scoring_model.sas`:
    *   `transactions_with_rules` (input), created in `04_rule_based_detection.sas`
    *   `ml_data_prepared` (output from `PREPARE_ML_DATA`)
    *   `transactions_ml_scored` (output from `CALCULATE_ML_SCORE`)
    *   `transactions_combined_score` (output from `COMPARE_MODELS`)
*   `06_case_management_output.sas`:
    *   `transactions_combined_score` (input), created in `05_ml_scoring_model.sas`
    *   `investigation_queue` (output from `CREATE_INVESTIGATION_QUEUE`)
    *   `sar_cases` (output from `GENERATE_SAR_DATA`)

### Macro Execution Order

The programs extensively use macros. The macros are executed in the order they are called within each program. The general flow is:

1.  Define macro variables (paths, file names, etc.).
2.  Define macros (e.g., `IMPORT_TRANSACTIONS`, `VALIDATE_DATA`).
3.  Call macros in a specific sequence to perform the data processing steps.

### RUN/QUIT Statement Trigger Points

*   `RUN` statements:  Appear at the end of `PROC IMPORT`, `DATA`, `PROC SORT`, `PROC SQL`, `PROC MEANS`, `PROC FREQ`, `PROC CORR`, and `PROC EXPORT` steps.  These trigger the execution of the respective procedures or data steps.
*   `QUIT` statements: Appear at the end of `PROC SQL` steps. These terminate the `PROC SQL` procedure.
*   `ABORT` statement: Is triggered within the `IMPORT_TRANSACTIONS` macro if `SYSERR` is greater than 0, which indicates that the import failed.

### List of Use Cases Addressed

The SAS programs together address the following use cases:

1.  **Data Import and Validation:** Importing transaction data from a CSV file and performing initial data validation to ensure data quality.
2.  **Data Cleaning and Standardization:** Cleaning and standardizing transaction data, including handling missing values, standardizing formats, and removing duplicates.
3.  **Feature Engineering:** Creating new features from the raw data to enhance fraud detection capabilities.  This includes velocity calculations, amount deviation analysis, time-based features, and location-based features.
4.  **Rule-Based Fraud Detection:** Implementing a rule-based system to identify potentially fraudulent transactions based on predefined rules and thresholds.
5.  **Machine Learning Scoring:** Applying a machine learning model (simulated in this case) to score transactions for fraud probability.
6.  **Model Comparison:** Comparing the performance of the rule-based system and the ML model.
7.  **Alert Generation and Prioritization:** Generating fraud alerts based on the rule-based system and the ML model, and then prioritizing those alerts for investigation.
8.  **Case Management and Reporting:** Creating an investigation queue, generating daily summary reports, and exporting data for case management.  Generating SAR (Suspicious Activity Report) data for regulatory compliance.
