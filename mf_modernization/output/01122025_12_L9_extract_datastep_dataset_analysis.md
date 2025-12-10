### Program: 01_transaction_data_import.sas

*   **Description:** This program imports transaction data from a CSV file, performs basic validation, and stores the validated data.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `/data/raw/transactions.csv`:  The raw transaction data in CSV format.
    *   **Created (Temporary):**
        *   `WORK.raw_transactions`:  A temporary SAS dataset containing the imported data from the CSV file.
        *   `WORK.transactions_validated`: A temporary SAS dataset containing the validated transaction data.

*   **Input Sources:**

    *   `PROC IMPORT`:
        *   `DATAFILE`:  `&input_path/&transaction_file` (resolves to `/data/raw/transactions.csv`). This specifies the input CSV file.
        *   `DBMS=CSV`:  Specifies that the input file is a CSV file.
        *   `OUT`:  `&outds` (resolves to `WORK.raw_transactions`).  Specifies the output SAS dataset.
        *   `REPLACE`:  If the output dataset already exists, it is replaced.
        *   `GETNAMES=YES`:  Reads the first row of the CSV file as variable names.
    *   `SET`:
        *   `SET &inds`: (resolves to `WORK.raw_transactions`) Used within the `VALIDATE_DATA` macro to read the imported data.

*   **Output Datasets:**

    *   `WORK.raw_transactions`: Temporary
    *   `WORK.transactions_validated`: Temporary

*   **Key Variable Usage and Transformations:**

    *   `validation_status`: A character variable created to flag the validity of each transaction based on missing values and amount.
    *   `transaction_id`, `customer_id`, `amount`, `transaction_date`:  These are the key variables used for validation.
    *   The program filters the dataset to include only valid records where `validation_status` is 'VALID'.

*   **RETAIN statements and Variable Initialization:**

    *   None

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_path = /data/raw;`: Defines the path to the input data.
    *   `%let output_lib = WORK;`: Specifies the library for output datasets (WORK).
    *   `%let transaction_file = transactions.csv;`:  Defines the filename of the transaction data.

### Program: 02_data_quality_cleaning.sas

*   **Description:** This program cleans and standardizes the transaction data, handles missing values, and removes duplicate records.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_validated`:  The validated transaction data from the previous program.
    *   **Created (Temporary):**
        *   `WORK.transactions_cleaned`:  The cleaned transaction data.
        *   `WORK.transactions_deduped`: The de-duplicated transaction data.
        *   `WORK.transactions_final`: The final transaction data after outlier handling.
        *   `percentiles`:  A temporary dataset created within the `HANDLE_OUTLIERS` macro to store percentile values.

*   **Input Sources:**

    *   `SET`:
        *   `SET &inds`: (resolves to `WORK.transactions_validated`, `WORK.transactions_cleaned`, `WORK.transactions_deduped`) Used within the macros to read the input datasets.
    *   `PROC SORT`:
        *   `DATA=&inds` (resolves to `WORK.transactions_cleaned`): Sorts the input dataset to remove duplicates.
        *   `OUT=&outds` (resolves to `WORK.transactions_deduped`): Specifies the output dataset.
        *   `NODUPKEY`:  Removes duplicate records based on the `key` variable.
    *   `PROC MEANS`:
        *   `DATA=&inds`: (resolves to `WORK.transactions_deduped`) Used within the `HANDLE_OUTLIERS` macro to calculate percentiles.
        *   `OUTPUT OUT=percentiles`:  Saves the output of the `MEANS` procedure to a dataset named `percentiles`.

*   **Output Datasets:**

    *   `WORK.transactions_cleaned`: Temporary
    *   `WORK.transactions_deduped`: Temporary
    *   `WORK.transactions_final`: Temporary
    *   `percentiles`: Temporary

*   **Key Variable Usage and Transformations:**

    *   `transaction_type_clean`: Standardized transaction type (uppercase and stripped).
    *   `merchant_name_clean`: Cleaned merchant name (proper case and stripped).
    *   `country_code_clean`: Standardized country code (uppercase and first two characters).
    *   `amount`: Missing amounts are replaced with 0.
    *   `transaction_date_sas`:  Transaction date converted to a SAS date format.
    *   `transaction_datetime`: Transaction date and time combined as a SAS datetime.
    *   Duplicate removal based on the `key` variable (transaction_id).
    *   Outlier handling using winsorization (capping values at the 1st and 99th percentiles) or removal, based on the `method` parameter.

*   **RETAIN statements and Variable Initialization:**

    *   None

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_lib = WORK;`: Specifies the input library (WORK).
    *   `%let output_lib = WORK;`: Specifies the output library (WORK).

### Program: 03_feature_engineering.sas

*   **Description:** This program engineers new features from the cleaned transaction data to aid in fraud detection.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_final`:  The cleaned and outlier-handled transaction data.
    *   **Created (Temporary):**
        *   `WORK.txn_with_velocity`:  Dataset with velocity features.
        *   `WORK.txn_with_deviation`:  Dataset with amount deviation features.
        *   `WORK.txn_with_time_features`: Dataset with time-based features.
        *   `WORK.transactions_engineered`:  Final dataset with all engineered features.
        *   `customer_stats`:  A temporary dataset created within the `CALCULATE_AMOUNT_DEVIATION` macro to store customer statistics.
        *   `country_counts`:  A temporary dataset created within the `CREATE_LOCATION_FEATURES` macro to store country transaction counts.

*   **Input Sources:**

    *   `SET`:
        *   `SET &inds;`: (resolves to `WORK.transactions_final`, `WORK.txn_with_velocity`, `WORK.txn_with_deviation`, `WORK.txn_with_time_features`) Used to read the input datasets within the macros.
    *   `PROC SORT`:
        *   `DATA=&inds`: (resolves to `WORK.transactions_final`)  Sorts the data by `customer_id` and `transaction_date_sas`.
    *   `PROC MEANS`:
        *   `DATA=&inds`: (resolves to `WORK.txn_with_velocity`) Used within the `CALCULATE_AMOUNT_DEVIATION` macro to calculate customer statistics.
    *   `PROC SQL`:
        *   `CREATE TABLE customer_stats`: Creates the `customer_stats` table by calculating statistics.
        *   `CREATE TABLE country_counts`: Creates the `country_counts` table by calculating counts.
        *   `CREATE TABLE &outds`: (resolves to `WORK.txn_with_deviation`, `WORK.transactions_engineered`)  Merges statistics back into the main dataset and calculates deviation features.

*   **Output Datasets:**

    *   `WORK.txn_with_velocity`: Temporary
    *   `WORK.txn_with_deviation`: Temporary
    *   `WORK.txn_with_time_features`: Temporary
    *   `WORK.transactions_engineered`: Temporary
    *   `customer_stats`: Temporary
    *   `country_counts`: Temporary

*   **Key Variable Usage and Transformations:**

    *   **Velocity Features:**
        *   `txn_count_&window_days.d`: Rolling count of transactions within a `window_days` window (default 7).
        *   `txn_amount_&window_days.d`:  Rolling sum of transaction amounts within the window.
        *   `avg_txn_amount_&window_days.d`: Average transaction amount within the window.
        *   `days_since_last_txn`: Days between current transaction and the last transaction.
    *   **Amount Deviation Features:**
        *   `customer_avg_amount`: Average transaction amount per customer.
        *   `customer_std_amount`: Standard deviation of transaction amounts per customer.
        *   `amount_zscore`: Z-score of the transaction amount, indicating how many standard deviations the amount is from the customer's average.
        *   `amount_pct_deviation`: Percentage deviation of the transaction amount from the customer's average.
    *   **Time-Based Features:**
        *   `txn_hour`: Hour of the transaction.
        *   `txn_day_of_week`: Day of the week of the transaction.
        *   `txn_day_of_month`: Day of the month of the transaction.
        *   `txn_month`: Month of the transaction.
        *   `time_of_day`: Categorical variable based on the hour (NIGHT, MORNING, AFTERNOON, EVENING).
        *   `is_weekend`: Flag indicating if the transaction occurred on a weekend.
        *   `is_unusual_hour`: Flag indicating if the transaction occurred during unusual hours (0-5).
    *   **Location-Based Features:**
        *   `country_txn_count`: Number of transactions per country.
        *   `is_rare_country`: Flag indicating if the country has a low transaction count.
        *   `is_international`: Flag indicating if the transaction is international (country code not 'US').

*   **RETAIN statements and Variable Initialization:**

    *   `RETAIN txn_count_&window_days.d 0 txn_amount_&window_days.d 0 last_txn_date .`:  Used within the `CALCULATE_VELOCITY` macro to retain variables for rolling window calculations.

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_lib = WORK;`: Specifies the input library (WORK).
    *   `%let output_lib = WORK;`: Specifies the output library (WORK).

### Program: 04_rule_based_detection.sas

*   **Description:** This program applies rule-based fraud detection logic to the engineered features and generates alerts.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_engineered`:  The dataset containing the engineered features.
    *   **Created (Temporary):**
        *   `WORK.transactions_with_rules`: Dataset with rule-based scores and flags.
        *   `WORK.rule_based_alerts`:  Dataset containing the transactions that triggered alerts.
        *   `rule_summary`:  A temporary dataset created within the `RULE_SUMMARY_REPORT` macro to summarize the rule triggers.

*   **Input Sources:**

    *   `SET`:
        *   `SET &inds;`: (resolves to `WORK.transactions_engineered`) Used to read the input dataset within the `APPLY_FRAUD_RULES` macro.
    *   `PROC SQL`:
        *   `CREATE TABLE rule_summary`: Creates the `rule_summary` table to summarize rule triggers.
        *   `CREATE TABLE &outds`: (resolves to `WORK.rule_based_alerts`) Filters the data based on the rule score.
    *   `PROC FREQ`:
        *   `DATA=&outds`: (resolves to `WORK.rule_based_alerts`) Used to generate frequency tables for the `rule_risk_level`.

*   **Output Datasets:**

    *   `WORK.transactions_with_rules`: Temporary
    *   `WORK.rule_based_alerts`: Temporary
    *   `rule_summary`: Temporary

*   **Key Variable Usage and Transformations:**

    *   `rule_triggered`:  A character variable that stores the names of the rules triggered for each transaction.
    *   `rule_score`:  A numeric variable that represents the total score based on the rules triggered.
    *   `rule_risk_level`: A categorical variable representing the risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the `rule_score`.
    *   `is_suspicious`: A binary flag indicating whether a transaction is suspicious based on the `rule_score`.
    *   Rule definitions and score assignments are implemented using `IF` statements.
    *   The `GENERATE_RULE_ALERTS` macro filters transactions based on a `threshold` for the `rule_score`.

*   **RETAIN statements and Variable Initialization:**

    *   `length rule_triggered $200; rule_triggered = ''; rule_score = 0;`: Initializes variables within the `APPLY_FRAUD_RULES` macro.

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_lib = WORK;`: Specifies the input library (WORK).
    *   `%let output_lib = WORK;`: Specifies the output library (WORK).

### Program: 05_ml_scoring_model.sas

*   **Description:** This program prepares data for an ML model, calculates a simulated ML fraud score, and compares the results with the rule-based approach.  Note that the ML model is simulated using coefficients, not trained.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_with_rules`:  Dataset with rule-based scores and flags.
    *   **Created (Temporary):**
        *   `WORK.ml_data_prepared`: Dataset with data prepared for ML scoring.
        *   `WORK.transactions_ml_scored`: Dataset with ML fraud scores.
        *   `WORK.transactions_combined_score`: Dataset with combined scores and model comparison.

*   **Input Sources:**

    *   `SET`:
        *   `SET &inds;`: (resolves to `WORK.transactions_with_rules`, `WORK.ml_data_prepared`, `WORK.transactions_ml_scored`) Used to read the input datasets within the macros.
    *   `PROC FREQ`:
        *   `DATA=&inds;`: (resolves to `WORK.transactions_ml_scored`) Used to generate frequency tables for the `ml_risk_band` and `ml_alert`.
    *   `PROC MEANS`:
        *   `DATA=&inds;`: (resolves to `WORK.transactions_ml_scored`) Used to calculate the distribution of the ML fraud scores.
    *   `PROC CORR`:
        *   `DATA=&outds;`: (resolves to `WORK.transactions_combined_score`) Used to find the correlation between ML and rule scores.

*   **Output Datasets:**

    *   `WORK.ml_data_prepared`: Temporary
    *   `WORK.transactions_ml_scored`: Temporary
    *   `WORK.transactions_combined_score`: Temporary

*   **Key Variable Usage and Transformations:**

    *   **Data Preparation:**
        *   `is_high_amount`, `is_very_high_amount`: Binary flags for amount thresholds.
        *   `amount_normalized`, `txn_count_normalized`: Normalized continuous variables using min-max scaling.
        *   Missing values in certain variables are imputed to 0.
        *   `amount_x_velocity`, `amount_x_deviation`: Interaction features are created.
    *   **ML Scoring (Simulated):**
        *   `logit_score`: Calculated using a linear combination of the prepared features and pre-defined coefficients (simulating a logistic regression).
        *   `ml_fraud_probability`:  The probability of fraud, calculated using the sigmoid function (1 / (1 + exp(-logit_score))).
        *   `ml_fraud_score`: The fraud score, calculated as probability \* 100.
        *   `ml_risk_band`: Categorical risk band based on the `ml_fraud_score`.
        *   `ml_alert`: Binary flag indicating an ML alert.
    *   **Model Comparison:**
        *   `model_agreement`: Categorical variable indicating the agreement between the ML model and the rule-based system (BOTH\_ALERT, ML\_ONLY, RULE\_ONLY, BOTH\_CLEAR).
        *   `combined_score`:  A combined score of the `ml_fraud_score` and `rule_score` (weighted average).
        *   `combined_risk_level`: A categorical risk level based on the `combined_score`.

*   **RETAIN statements and Variable Initialization:**

    *   None

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_lib = WORK;`: Specifies the input library (WORK).
    *   `%let output_lib = WORK;`: Specifies the output library (WORK).

### Program: 06_case_management_output.sas

*   **Description:** This program creates an investigation queue, generates reports, and exports data for case management.

*   **Datasets Created and Consumed:**

    *   **Consumed:**
        *   `WORK.transactions_combined_score`: Dataset with combined scores and model comparison.
    *   **Created (Temporary):**
        *   `WORK.investigation_queue`:  The investigation queue dataset.
        *   `WORK.sar_cases`:  Dataset containing transactions requiring SAR (Suspicious Activity Report) filing.
    *   **Created (Permanent):**
        *   `daily_summary`: A temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to summarize the data.
        *   `top_customers`: A temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to store the top customers.
        *   `hourly_trend`: A temporary dataset created within the `GENERATE_DAILY_SUMMARY` macro to store the hourly trend.

*   **Input Sources:**

    *   `SET`:
        *   `SET &inds;`: (resolves to `WORK.transactions_combined_score`) Used to read the input dataset within the `CREATE_INVESTIGATION_QUEUE` macro.
    *   `PROC SQL`:
        *   `CREATE TABLE daily_summary`: Creates the `daily_summary` table to summarize the data.
        *   `CREATE TABLE top_customers`: Creates the `top_customers` table to store the top customers.
        *   `CREATE TABLE hourly_trend`: Creates the `hourly_trend` table to store the hourly trend.
        *   `CREATE TABLE &outds`: (resolves to `WORK.investigation_queue`, `WORK.sar_cases`) Filters the data based on the score and calculates the final priority.
    *   `PROC FREQ`:
        *   `DATA=&inds;`: (resolves to `WORK.investigation_queue`) Used to generate frequency tables for the case priorities.
    *   `PROC EXPORT`:
        *   `DATA=export_data`: Exports the investigation queue to a CSV file.
    *   `PROC SORT`:
        *   `DATA=&outds`: (resolves to `WORK.investigation_queue`, `WORK.sar_cases`) Sorts the data based on the priority and the transaction date.

*   **Output Datasets:**

    *   `WORK.investigation_queue`: Temporary
    *   `WORK.sar_cases`: Temporary
    *   `daily_summary`: Temporary
    *   `top_customers`: Temporary
    *   `hourly_trend`: Temporary
    *   `investigation_queue_&SYSDATE9..csv`: CSV file exported to the specified `filepath`.

*   **Key Variable Usage and Transformations:**

    *   `priority_score`: Calculated based on `combined_score` and additional factors (amount, international transactions, velocity).
    *   `case_priority`: Categorical priority level (URGENT, HIGH, MEDIUM, LOW) based on the `priority_score`.
    *   `case_id`:  Unique case identifier.
    *   `investigation_reason`:  Provides context for the investigation (ML score, rule score, triggered rules).
    *   `investigator_id`:  Assigned to investigators using a round-robin approach.
    *   `case_status`:  Set to 'PENDING\_REVIEW'.
    *   `case_created_datetime`: Timestamp of case creation.
    *   The `GENERATE_SAR_DATA` macro filters cases based on a `sar_threshold` and adds SAR-specific fields.
    *   `sar_type`:  Type of SAR filing.
    *   `sar_narrative`:  Narrative for the SAR filing.
    *   `requires_sar`:  Flag indicating if a SAR filing is required.
    *   `sar_deadline_date`:  Date by which the SAR must be filed (30 days after creation).

*   **RETAIN statements and Variable Initialization:**

    *   None

*   **LIBNAME and FILENAME assignments:**

    *   `%let input_lib = WORK;`: Specifies the input library (WORK).
    *   `%let output_lib = WORK;`: Specifies the output library (WORK).
    *   `%let report_path = /output/reports;`: Defines the path for exporting reports.
