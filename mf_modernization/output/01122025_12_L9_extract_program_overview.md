## Analysis of SAS Programs

### Program: 01_transaction_data_import.sas

*   **Overview of the Program:**
    This program imports transaction data from a CSV file, performs initial data validation, and flags potentially invalid records. It uses macros for importing and validating the data, logging the results, and displaying the first 10 validated transactions.

*   **Business Functions Addressed:**
    *   Data Import: Reads transaction data from a CSV file.
    *   Data Validation: Checks for missing values and invalid amounts.
    *   Data Quality: Filters out invalid records based on validation rules.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `/data/raw/transactions.csv` (External CSV file)
    2.  **Creates:**
        *   `WORK.raw_transactions` (SAS dataset): Contains the raw, imported data from the CSV file.
        *   `WORK.transactions_validated` (SAS dataset): Contains the validated transaction data, with invalid records removed.
    3.  **Data Flow:**
        *   CSV file -> `raw_transactions` -> `transactions_validated`

### Program: 02_data_quality_cleaning.sas

*   **Overview of the Program:**
    This program cleans and standardizes transaction data, removes duplicates, and handles outliers. It uses macros for cleaning, removing duplicates, and handling outliers. The program standardizes data, removes duplicate records based on transaction ID, and handles outliers in the transaction amount by winsorizing.

*   **Business Functions Addressed:**
    *   Data Cleaning: Standardizes and cleans various transaction fields (transaction type, merchant name, country code).
    *   Data Standardization: Converts transaction date to a standard SAS format and creates a transaction datetime variable.
    *   Data Deduplication: Removes duplicate transactions based on transaction ID.
    *   Outlier Handling: Addresses outliers in the transaction amount using winsorization.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `WORK.transactions_validated` (SAS dataset): The validated transaction data from the previous program.
    2.  **Creates:**
        *   `WORK.transactions_cleaned` (SAS dataset): Contains the cleaned and standardized transaction data.
        *   `WORK.transactions_deduped` (SAS dataset): Contains the data after duplicate records are removed.
        *   `WORK.transactions_final` (SAS dataset): Contains the data after outlier handling.
        *   `WORK.percentiles` (SAS dataset): A temporary dataset created within the `HANDLE_OUTLIERS` macro to store percentiles.
    3.  **Data Flow:**
        *   `transactions_validated` -> `transactions_cleaned` -> `transactions_deduped` -> `transactions_final`

### Program: 03_feature_engineering.sas

*   **Overview of the Program:**
    This program engineers features for fraud detection, including velocity features, amount deviation features, time-based features, and location-based features. It uses macros for each type of feature engineering.

*   **Business Functions Addressed:**
    *   Feature Engineering: Creates new variables to enhance fraud detection. Includes velocity, amount deviation, time-based, and location-based features.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `WORK.transactions_final` (SAS dataset): The cleaned and preprocessed transaction data from the previous program.
    2.  **Creates:**
        *   `WORK.txn_with_velocity` (SAS dataset): Contains data with calculated velocity features.
        *   `WORK.txn_with_deviation` (SAS dataset): Contains data with amount deviation features.
        *   `WORK.txn_with_time_features` (SAS dataset): Contains data with time-based features.
        *   `WORK.transactions_engineered` (SAS dataset): Contains the final engineered features, including all the features created by the macros.
        *   `WORK.customer_stats` (SAS dataset): A temporary dataset created within the `CALCULATE_AMOUNT_DEVIATION` macro to store customer statistics.
        *   `WORK.country_counts` (SAS dataset): A temporary dataset created within the `CREATE_LOCATION_FEATURES` macro to store country counts.
    3.  **Data Flow:**
        *   `transactions_final` -> `txn_with_velocity` -> `txn_with_deviation` -> `txn_with_time_features` -> `transactions_engineered`

### Program: 04_rule_based_detection.sas

*   **Overview of the Program:**
    This program applies rule-based fraud detection logic to the engineered features. It defines fraud detection rules, calculates rule scores, generates alerts, and produces a rule summary report.

*   **Business Functions Addressed:**
    *   Fraud Detection: Implements a rule-based fraud detection system.
    *   Alert Generation: Flags suspicious transactions based on rule violations.
    *   Reporting: Generates a summary of triggered rules and alerts.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `WORK.transactions_engineered` (SAS dataset): The dataset containing engineered features.
    2.  **Creates:**
        *   `WORK.transactions_with_rules` (SAS dataset): Contains the data with rule-based scores, rule triggers, and risk levels.
        *   `WORK.rule_based_alerts` (SAS dataset): Contains the transactions that triggered alerts based on the defined rules.
        *   `WORK.rule_summary` (SAS dataset): A temporary dataset created to store the rule trigger summary.
    3.  **Data Flow:**
        *   `transactions_engineered` -> `transactions_with_rules` -> `rule_based_alerts`

### Program: 05_ml_scoring_model.sas

*   **Overview of the Program:**
    This program applies a machine learning (ML) model (simulated logistic regression) to score transactions for fraud probability. It prepares data for the ML model, calculates fraud scores, generates performance metrics, and compares the ML model's results with the rule-based system.

*   **Business Functions Addressed:**
    *   ML Scoring: Applies a machine learning model to predict fraud probability.
    *   Model Evaluation: Generates performance metrics to assess the model's effectiveness.
    *   Model Comparison: Compares the ML model's results with the rule-based system.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `WORK.transactions_with_rules` (SAS dataset): The dataset with rule-based scores and engineered features.
    2.  **Creates:**
        *   `WORK.ml_data_prepared` (SAS dataset): Contains the data prepared for the ML model, including normalized and interaction features.
        *   `WORK.transactions_ml_scored` (SAS dataset): Contains the data with ML fraud scores, probabilities, and risk bands.
        *   `WORK.transactions_combined_score` (SAS dataset): Contains the data with the combined score from ML and rule-based scores and the model agreement information.
    3.  **Data Flow:**
        *   `transactions_with_rules` -> `ml_data_prepared` -> `transactions_ml_scored` -> `transactions_combined_score`

### Program: 06_case_management_output.sas

*   **Overview of the Program:**
    This program generates a prioritized case management queue, creates daily summary reports, exports the investigation queue, and generates data for Suspicious Activity Reports (SARs).

*   **Business Functions Addressed:**
    *   Case Management: Creates a prioritized investigation queue.
    *   Reporting: Generates daily summary reports.
    *   Data Export: Exports the investigation queue to a CSV file.
    *   Compliance: Generates data for SAR filings.

*   **Datasets Created and Consumed:**

    1.  **Consumes:**
        *   `WORK.transactions_combined_score` (SAS dataset): The dataset containing the combined scores from ML and rule-based systems.
    2.  **Creates:**
        *   `WORK.investigation_queue` (SAS dataset): Contains the prioritized investigation queue.
        *   `WORK.daily_summary` (SAS dataset): A temporary dataset created to store the daily summary statistics.
        *   `WORK.top_customers` (SAS dataset): A temporary dataset created to store the top customers by alert count.
        *   `WORK.hourly_trend` (SAS dataset): A temporary dataset created to store the hourly alert trend.
        *   `WORK.sar_cases` (SAS dataset): Contains the cases that require SAR filing.
        *   `export_data` (SAS dataset): A temporary dataset used for exporting the investigation queue to a CSV file.
    3.  **Data Flow:**
        *   `transactions_combined_score` -> `investigation_queue` -> CSV file (exported)
        *   `investigation_queue` -> `daily_summary`
        *   `investigation_queue` -> `sar_cases`
