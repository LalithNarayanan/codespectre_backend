## Analysis of SAS Programs

Here's a breakdown of each SAS program, as requested:

### 01_transaction_data_import.sas

*   **Description:** This program imports transaction data from a CSV file, performs initial validation checks, and creates a validated dataset.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `/data/raw/transactions.csv` (CSV file):  Input transaction data.  The file path is determined by the macro variable `input_path` and `transaction_file`.
    *   **Created:**
        *   `WORK.raw_transactions` (Temporary):  Dataset containing the raw, imported transaction data from the CSV.
        *   `WORK.transactions_validated` (Temporary):  Dataset containing only the validated transaction records (records passing the validation checks).

*   **Input Sources:**

    *   `PROC IMPORT`: Reads the `transactions.csv` file.

*   **Output Datasets:**

    *   `WORK.raw_transactions` (Temporary):  Created by `PROC IMPORT`.
    *   `WORK.transactions_validated` (Temporary):  Created by the `VALIDATE_DATA` macro.

*   **Key Variable Usage and Transformations:**

    *   `transaction_id`, `customer_id`, `amount`, `transaction_date`:  These are key variables from the input CSV file.
    *   `validation_status`: A character variable created to flag the validation status of each transaction.  Possible values: 'MISSING\_ID', 'MISSING\_CUSTOMER', 'MISSING\_AMOUNT', 'MISSING\_DATE', 'INVALID\_AMOUNT', 'VALID'.
    *   Missing value checks are performed on `transaction_id`, `customer_id`, `amount`, and `transaction_date`.
    *   Amount is checked to ensure it is greater than 0.

*   **RETAIN Statements and Variable Initialization:**

    *   None.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.
    *   `FILENAME`:  Not explicitly used. The `PROC IMPORT` statement uses a file path.

### 02_data_quality_cleaning.sas

*   **Description:** This program cleans and standardizes the validated transaction data, removes duplicates, and handles outliers in the `amount` variable.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_validated`:  Input dataset from the previous program (01\_transaction\_data\_import.sas).
    *   **Created:**
        *   `WORK.transactions_cleaned` (Temporary):  Dataset with standardized `transaction_type`, `merchant_name`, and `country_code`, missing amounts replaced with 0, and converted `transaction_date` to SAS date format.
        *   `WORK.transactions_deduped` (Temporary): Dataset with duplicate records removed, based on `transaction_id`.
        *   `WORK.transactions_final` (Temporary):  Dataset with outliers in the `amount` variable handled (Winsorized in the example).
        *   `WORK.percentiles` (Temporary):  Created internally within the `HANDLE_OUTLIERS` macro by `PROC MEANS`.  Used to store the 1st and 99th percentiles of the `amount` variable.

*   **Input Sources:**

    *   `SET`: Used within the `CLEAN_TRANSACTIONS`, `REMOVE_DUPLICATES`, and `HANDLE_OUTLIERS` macros to read from input datasets.
    *   `PROC SORT`:  Used within the `REMOVE_DUPLICATES` macro to sort the data and remove duplicates.
    *   `PROC MEANS`: Used within the `HANDLE_OUTLIERS` macro to calculate percentiles.

*   **Output Datasets:**

    *   `WORK.transactions_cleaned` (Temporary):  Created by the `CLEAN_TRANSACTIONS` macro.
    *   `WORK.transactions_deduped` (Temporary):  Created by the `REMOVE_DUPLICATES` macro.
    *   `WORK.transactions_final` (Temporary):  Created by the `HANDLE_OUTLIERS` macro.
    *   `WORK.percentiles` (Temporary):  Created internally within the `HANDLE_OUTLIERS` macro.

*   **Key Variable Usage and Transformations:**

    *   `transaction_type`: Standardized to uppercase using `UPCASE` and `STRIP`.
    *   `merchant_name`:  Converted to proper case using `PROPCASE` and `STRIP`.
    *   `country_code`: Standardized to uppercase and truncated to the first two characters using `UPCASE` and `SUBSTR`.
    *   `amount`: Missing values are replaced with 0.
    *   `transaction_date`: Converted to a SAS date format (`transaction_date_sas`) using `INPUT` and then formatted using `FORMAT`.
    *   `transaction_time`: Used with `transaction_date_sas` to create `transaction_datetime`.
    *   `transaction_datetime`: Created using `DHMS` function from `transaction_date_sas`, `HOUR`, `MINUTE`, and `SECOND` of `transaction_time`.
    *   `transaction_id`: Used to remove duplicates by sorting and using the `NODUPKEY` option in `PROC SORT`.
    *   `amount`:  Outliers are handled using the `HANDLE_OUTLIERS` macro, using Winsorizing (capping values at the 1st and 99th percentiles) or removing them.

*   **RETAIN Statements and Variable Initialization:**

    *   None.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.

### 03_feature_engineering.sas

*   **Description:** This program engineers new features from the cleaned transaction data to aid in fraud detection, including velocity features, amount deviation features, time-based features, and location-based features.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_final`:  Input dataset from the previous program (02\_data\_quality\_cleaning.sas).
    *   **Created:**
        *   `WORK.txn_with_velocity` (Temporary):  Dataset with calculated velocity features (transaction count and amount within a 7-day window).
        *   `WORK.customer_stats` (Temporary):  Created internally within the `CALCULATE_AMOUNT_DEVIATION` macro by `PROC MEANS`. Used to calculate customer-level statistics (mean, standard deviation, and transaction count) of the `amount` variable.
        *   `WORK.txn_with_deviation` (Temporary):  Dataset with amount deviation features (z-score and percentage deviation from the customer's average transaction amount).
        *   `WORK.txn_with_time_features` (Temporary):  Dataset with time-based features (hour, day of week, day of month, month, time of day, and weekend flag).
        *   `WORK.country_counts` (Temporary):  Created internally within the `CREATE_LOCATION_FEATURES` macro.  Used to calculate the number of transactions per country.
        *   `WORK.transactions_engineered` (Temporary):  Dataset with location-based features (country transaction count, rare country flag, and international transaction flag).

*   **Input Sources:**

    *   `SET`: Used within the macros to read data.
    *   `PROC SORT`:  Used within the `CALCULATE_VELOCITY` macro to sort data.
    *   `PROC MEANS`: Used within the `CALCULATE_AMOUNT_DEVIATION` macro.
    *   `PROC SQL`: Used within the `CALCULATE_AMOUNT_DEVIATION` and `CREATE_LOCATION_FEATURES` macros to create customer statistics and location features, respectively.

*   **Output Datasets:**

    *   `WORK.txn_with_velocity` (Temporary):  Created by the `CALCULATE_VELOCITY` macro.
    *   `WORK.txn_with_deviation` (Temporary):  Created by the `CALCULATE_AMOUNT_DEVIATION` macro.
    *   `WORK.txn_with_time_features` (Temporary):  Created by the `CREATE_TIME_FEATURES` macro.
    *   `WORK.transactions_engineered` (Temporary):  Created by the `CREATE_LOCATION_FEATURES` macro.
    *   `WORK.customer_stats` (Temporary):  Created internally within the `CALCULATE_AMOUNT_DEVIATION` macro.
    *   `WORK.country_counts` (Temporary):  Created internally within the `CREATE_LOCATION_FEATURES` macro.

*   **Key Variable Usage and Transformations:**

    *   `customer_id`: Used to calculate customer-level statistics and velocity features.
    *   `transaction_date_sas`: Used to calculate velocity features and time-based features.
    *   `transaction_time`: Used to create time-based features.
    *   `amount`: Used to calculate amount deviation features and velocity features.
    *   `txn_count_7d`, `txn_amount_7d`, `last_txn_date`, `days_since_last_txn`, `avg_txn_amount_7d`:  These are features created within the `CALCULATE_VELOCITY` macro to capture transaction velocity.
    *   `customer_avg_amount`, `customer_std_amount`, `customer_txn_count`, `amount_zscore`, `amount_pct_deviation`:  These are features created within the `CALCULATE_AMOUNT_DEVIATION` macro to capture deviations from a customer's typical spending.
    *   `txn_hour`, `txn_day_of_week`, `txn_day_of_month`, `txn_month`, `time_of_day`, `is_weekend`, `is_unusual_hour`:  These are time-based features created within the `CREATE_TIME_FEATURES` macro.
    *   `country_code_clean`, `country_txn_count`, `is_rare_country`, `is_international`:  These are location-based features created within the `CREATE_LOCATION_FEATURES` macro.

*   **RETAIN Statements and Variable Initialization:**

    *   `RETAIN txn_count_7d 0 txn_amount_7d 0 last_txn_date .`:  Used within the `CALCULATE_VELOCITY` macro to retain values across observations for calculating rolling window statistics.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.

### 04_rule_based_detection.sas

*   **Description:** This program applies rule-based fraud detection logic using the engineered features from the previous program. It assigns rule scores, identifies suspicious transactions, and generates alerts.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_engineered`:  Input dataset from the previous program (03\_feature\_engineering.sas).
    *   **Created:**
        *   `WORK.transactions_with_rules` (Temporary):  Dataset with rule-based fraud scores, rule triggers, and risk levels.
        *   `WORK.rule_summary` (Temporary):  Created internally within the `RULE_SUMMARY_REPORT` macro.  Summarizes the number of times each rule was triggered.
        *   `WORK.rule_based_alerts` (Temporary):  Dataset containing transactions that triggered fraud alerts.

*   **Input Sources:**

    *   `SET`: Used to read data.
    *   `PROC FREQ`: Used within the `GENERATE_RULE_ALERTS` macro to summarize alerts by risk level.
    *   `PROC SQL`: Used within the `RULE_SUMMARY_REPORT` macro to summarize rule triggers.

*   **Output Datasets:**

    *   `WORK.transactions_with_rules` (Temporary):  Created by the `APPLY_FRAUD_RULES` macro.
    *   `WORK.rule_based_alerts` (Temporary):  Created by the `GENERATE_RULE_ALERTS` macro.
    *   `WORK.rule_summary` (Temporary):  Created internally within the `RULE_SUMMARY_REPORT` macro.

*   **Key Variable Usage and Transformations:**

    *   `txn_count_7d`: Used in Rule 1.
    *   `amount_zscore`: Used in Rule 2.
    *   `amount`: Used in Rules 3 and 8.
    *   `is_unusual_hour`: Used in Rule 4.
    *   `is_international`: Used in Rule 5.
    *   `is_rare_country`: Used in Rule 6.
    *   `days_since_last_txn`: Used in Rule 7.
    *   `rule_triggered`:  Character variable that stores the names of the rules triggered.
    *   `rule_score`:  Numeric variable that represents the total score for the rules triggered.
    *   `rule_risk_level`:  Character variable that categorizes the risk level based on the `rule_score`. Possible values: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'.
    *   `is_suspicious`:  Binary flag indicating whether a transaction is suspicious based on the `rule_score`.

*   **RETAIN Statements and Variable Initialization:**

    *   `length rule_triggered $200; rule_triggered = ''; rule_score = 0;`:  Initializes rule-related variables.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.

### 05_ml_scoring_model.sas

*   **Description:** This program prepares the data for an ML model, calculates a simulated ML fraud score (using pre-defined coefficients), and generates performance metrics.  It also compares the results with the rule-based approach.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_with_rules`:  Input dataset from the previous program (04\_rule\_based\_detection.sas).
    *   **Created:**
        *   `WORK.ml_data_prepared` (Temporary):  Dataset with data prepared for ML scoring, including binary flags for categorical variables and normalized continuous variables.
        *   `WORK.transactions_ml_scored` (Temporary):  Dataset with ML fraud scores, probabilities, risk bands, and alert flags.
        *   `WORK.transactions_combined_score` (Temporary):  Dataset containing the combined score from ML and rule-based models, and model agreement analysis.

*   **Input Sources:**

    *   `SET`: Used to read the data.
    *   `PROC MEANS`: Used to generate the score distribution.
    *   `PROC FREQ`: Used to display the risk band distribution, and alert rate.
    *   `PROC CORR`: Used to find the correlation between ML and rule based scores.

*   **Output Datasets:**

    *   `WORK.ml_data_prepared` (Temporary): Created by the `PREPARE_ML_DATA` macro.
    *   `WORK.transactions_ml_scored` (Temporary): Created by the `CALCULATE_ML_SCORE` macro.
    *   `WORK.transactions_combined_score` (Temporary): Created by the `COMPARE_MODELS` macro.

*   **Key Variable Usage and Transformations:**

    *   `amount`: Used for normalization and creating interaction features.
    *   `txn_count_7d`: Used for normalization and creating interaction features.
    *   `amount_zscore`: Used for creating interaction features.
    *   `is_unusual_hour`, `is_international`: Used in the simulated logistic regression.
    *   `customer_txn_count`: Used in the simulated logistic regression.
    *   `is_high_amount`, `is_very_high_amount`: Binary flags created in the `PREPARE_ML_DATA` macro.
    *   `amount_normalized`, `txn_count_normalized`: Normalized continuous variables.
    *   `amount_x_velocity`, `amount_x_deviation`: Interaction features.
    *   `logit_score`: Calculated using simulated logistic regression coefficients.
    *   `ml_fraud_probability`: Calculated using the sigmoid function.
    *   `ml_fraud_score`: Scaled probability to a 0-100 score.
    *   `ml_risk_band`: Categorical risk level based on the `ml_fraud_score`. Possible values: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'VERY\_LOW'.
    *   `ml_alert`: Binary flag indicating an ML alert.
    *   `model_agreement`:  Categorical variable indicating the agreement between the ML model and the rule-based system.
    *   `combined_score`: Weighted average of the ML fraud score and the rule-based score.
    *   `combined_risk_level`: Risk level based on the `combined_score`.

*   **RETAIN Statements and Variable Initialization:**

    *   None.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.

### 06_case_management_output.sas

*   **Description:** This program generates an investigation queue, a daily summary report, exports the investigation queue to a CSV file, and generates SAR (Suspicious Activity Report) data.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_combined_score`:  Input dataset from the previous program (05\_ml\_scoring\_model.sas).
    *   **Created:**
        *   `WORK.investigation_queue` (Temporary):  Investigation queue with prioritized cases, case IDs, investigation reasons, and investigator assignments.
        *   `WORK.daily_summary` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.  Contains daily fraud detection summary statistics.
        *   `WORK.top_customers` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.  Lists top customers by alert count.
        *   `WORK.hourly_trend` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.  Shows hourly alert trends.
        *   `WORK.sar_cases` (Temporary):  Dataset containing cases that require SAR filing.
        *   `export_data` (Temporary):  Created internally within the `EXPORT_INVESTIGATION_QUEUE` macro. Contains selected variables to export to the CSV file.

*   **Input Sources:**

    *   `SET`: Used within the macros to read data.
    *   `PROC SORT`: Used to sort the investigation queue.
    *   `PROC SQL`: Used to create summary tables and generate reports.
    *   `PROC EXPORT`: Used to export the investigation queue to a CSV file.
    *   `PROC FREQ`: Used to display the alert distribution.
    *   `PROC PRINT`: Used to display the reports.

*   **Output Datasets:**

    *   `WORK.investigation_queue` (Temporary):  Created by the `CREATE_INVESTIGATION_QUEUE` macro.
    *   `WORK.sar_cases` (Temporary):  Created by the `GENERATE_SAR_DATA` macro.
    *   `WORK.daily_summary` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.
    *   `WORK.top_customers` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.
    *   `WORK.hourly_trend` (Temporary):  Created internally within the `GENERATE_DAILY_SUMMARY` macro.
    *   `export_data` (Temporary):  Created internally within the `EXPORT_INVESTIGATION_QUEUE` macro.
    *   `/output/reports/investigation_queue_&SYSDATE9..csv` (CSV file):  Created by the `EXPORT_INVESTIGATION_QUEUE` macro.

*   **Key Variable Usage and Transformations:**

    *   `combined_score`: Used to calculate the `priority_score` and assign `case_priority`.
    *   `amount`, `is_international`, `txn_count_7d`:  Used to calculate the `priority_score`.
    *   `ml_fraud_score`, `rule_score`, `rule_triggered`:  Used to generate the `investigation_reason`.
    *   `case_id`:  Unique identifier assigned to each case.
    *   `investigation_reason`:  Provides context for the investigation.
    *   `investigator_id`:  Assigned using a round-robin approach.
    *   `case_status`:  Set to 'PENDING\_REVIEW'.
    *   `case_created_datetime`: Timestamp of case creation.
    *   `priority_score`:  Final priority score for each case.
    *   `case_priority`: Categorical priority level based on the `priority_score`. Possible values: 'URGENT', 'HIGH', 'MEDIUM', 'LOW'.
    *   `sar_type`:  Fixed value,  identifying the type of SAR.
    *   `sar_narrative`:  Narrative for the SAR filing.
    *   `requires_sar`:  Flag indicating if a SAR filing is required.
    *   `sar_deadline_date`: Deadline for filing the SAR.

*   **RETAIN Statements and Variable Initialization:**

    *   None.

*   **LIBNAME and FILENAME Assignments:**

    *   `LIBNAME WORK`:  Implied, using the default `WORK` library for temporary datasets.
    *   `FILENAME`:  Used within the `EXPORT_INVESTIGATION_QUEUE` macro to create the CSV file in the directory specified by the `report_path` macro variable.  The file name includes the current date (`&SYSDATE9`).
