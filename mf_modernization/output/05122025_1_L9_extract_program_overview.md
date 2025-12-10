## Analysis of SAS Programs

Here's an analysis of each SAS program, as requested:

### 01_transaction_data_import.sas

*   **Overview of the Program:** This program imports transaction data from a CSV file, performs basic data validation, and filters out invalid records. It uses macros for importing and validating data.

*   **Business Functions Addressed:**
    *   Data Ingestion: Imports transaction data from a CSV file.
    *   Data Validation: Checks for missing values, invalid amounts, and applies basic data quality checks.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `/data/raw/transactions.csv` (CSV file):  Input transaction data.
    *   Creates:
        *   `WORK.raw_transactions`: Dataset created by importing the CSV file.
        *   `WORK.transactions_validated`: Dataset containing validated transactions, filtered from `WORK.raw_transactions`.

### 02_data_quality_cleaning.sas

*   **Overview of the Program:** This program cleans and standardizes the imported transaction data. It performs tasks like standardizing transaction types, cleaning merchant names, handling missing values, converting dates, removing duplicates, and handling outliers. It utilizes macros for each of these cleaning steps.

*   **Business Functions Addressed:**
    *   Data Cleaning: Standardizes and cleans transaction data.
    *   Data Standardization: Converts data into a consistent format.
    *   Data Quality: Addresses missing values, duplicates, and outliers.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `WORK.transactions_validated`: Output from `01_transaction_data_import.sas`.
    *   Creates:
        *   `WORK.transactions_cleaned`: Dataset with standardized transaction data.
        *   `WORK.transactions_deduped`: Dataset with duplicate records removed from `WORK.transactions_cleaned`.
        *   `WORK.transactions_final`: Dataset with outliers handled (winsorized or removed) from `WORK.transactions_deduped`.
        *   `WORK.percentiles`: Temporary dataset created and used within the `HANDLE_OUTLIERS` macro for percentile calculations.

### 03_feature_engineering.sas

*   **Overview of the Program:** This program engineers new features from the cleaned transaction data to be used for fraud detection. It calculates velocity features, amount deviation features, time-based features, and location-based features. It uses macros for each feature engineering step.

*   **Business Functions Addressed:**
    *   Feature Engineering: Creates new variables (features) from existing data to improve fraud detection.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `WORK.transactions_final`: Output from `02_data_quality_cleaning.sas`.
    *   Creates:
        *   `WORK.txn_with_velocity`: Dataset with velocity features calculated.
        *   `WORK.txn_with_deviation`: Dataset with amount deviation features calculated.
        *   `WORK.txn_with_time_features`: Dataset with time-based features.
        *   `WORK.transactions_engineered`: Dataset with location-based features.
        *   `WORK.customer_stats`: Temporary dataset created within the `CALCULATE_AMOUNT_DEVIATION` macro for calculating customer-level statistics.
        *   `WORK.country_counts`: Temporary dataset created within the `CREATE_LOCATION_FEATURES` macro for calculating country-level transaction counts.

### 04_rule_based_detection.sas

*   **Overview of the Program:** This program applies rule-based fraud detection logic using the engineered features. It defines fraud detection rules, calculates rule-based scores, generates alerts, and produces a summary report.  It utilizes macros for rule application, alert generation, and reporting.

*   **Business Functions Addressed:**
    *   Fraud Detection: Implements rule-based fraud detection.
    *   Alerting: Generates alerts based on rule violations.
    *   Reporting: Provides a summary of rule triggers and alert counts.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `WORK.transactions_engineered`: Output from `03_feature_engineering.sas`.
    *   Creates:
        *   `WORK.transactions_with_rules`: Dataset with rule flags, scores, and risk levels.
        *   `WORK.rule_based_alerts`: Dataset containing transactions that triggered alerts based on rule scores.
        *   `WORK.rule_summary`: Temporary dataset created within the `RULE_SUMMARY_REPORT` macro to summarize rule triggers.

### 05_ml_scoring_model.sas

*   **Overview of the Program:** This program applies a machine learning (ML) model (simulated logistic regression in this example) to score transactions for fraud probability. It prepares the data for ML scoring, calculates the ML fraud score, generates performance metrics, and compares the ML model's results with the rule-based system. It uses macros for data preparation, score calculation, metric generation, and model comparison.

*   **Business Functions Addressed:**
    *   Fraud Detection: Implements ML-based fraud detection.
    *   Scoring: Assigns fraud scores based on the ML model.
    *   Performance Analysis:  Evaluates the performance of the ML model.
    *   Model Comparison: Compares ML results with rule-based results.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `WORK.transactions_with_rules`: Output from `04_rule_based_detection.sas`.
    *   Creates:
        *   `WORK.ml_data_prepared`: Dataset with data prepared for ML scoring (e.g., normalization, feature interactions).
        *   `WORK.transactions_ml_scored`: Dataset with ML fraud scores, probabilities, and risk bands.
        *   `WORK.transactions_combined_score`: Dataset with a combined score from both ML and rule-based models.

### 06_case_management_output.sas

*   **Overview of the Program:** This program generates output for case management, including an investigation queue, daily summary reports, and data for Suspicious Activity Reports (SARs). It prioritizes cases, assigns them to investigators (simulated), and exports data for further action. It uses macros for queue creation, report generation, and data export.

*   **Business Functions Addressed:**
    *   Case Management: Creates and manages a queue of potential fraud cases.
    *   Reporting: Generates reports to summarize fraud activity.
    *   SAR Generation: Prepares data for SAR filings.
    *   Prioritization: Assigns priorities to cases.
    *   Alerting: Integrates ML and rule-based alerts to generate the investigation queue.

*   **Datasets Created and Consumed with Data Flow:**
    *   Consumes:
        *   `WORK.transactions_combined_score`: Output from `05_ml_scoring_model.sas`.
    *   Creates:
        *   `WORK.investigation_queue`: Dataset representing the prioritized investigation queue.
        *   `WORK.daily_summary`: Temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to summarize daily fraud activity.
        *   `WORK.top_customers`: Temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to list top customers by alert count.
        *   `WORK.hourly_trend`: Temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to show hourly alert trends.
        *   `WORK.sar_cases`: Dataset containing cases requiring SAR filings.
        *   `export_data`: Temporary dataset created within the `EXPORT_INVESTIGATION_QUEUE` macro to select data for export.
    *   Outputs:
        *   `/output/reports/investigation_queue_YYYYMMDD.csv`: CSV file containing the investigation queue, exported via the `EXPORT_INVESTIGATION_QUEUE` macro.
