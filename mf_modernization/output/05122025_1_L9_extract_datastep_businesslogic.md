## Analysis of SAS Programs

### Program: 01_transaction_data_import.sas

#### 1. Macros and Steps Execution Order & Purpose

1.  **`%IMPORT_TRANSACTIONS`**:
    *   **Purpose**: Imports transaction data from a CSV file into a SAS dataset and performs basic error checking.
    *   **Steps**:
        1.  `PROC IMPORT`: Imports the CSV file specified by the `filepath` macro variable into a SAS dataset specified by the `outds` macro variable.
        2.  `%PUT`: Logs a note indicating the successful import.
        3.  `%IF`: Checks the `SYSERR` automatic macro variable. If greater than 0, indicating an error during import, it logs an error message and aborts the program.
2.  **`%VALIDATE_DATA`**:
    *   **Purpose**: Validates the imported transaction data, checking for missing values and amount validity.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `LENGTH`: Defines the length of the `validation_status` variable.
        4.  `IF/ELSE IF/ELSE`: Conditional logic to set the `validation_status` based on missing values in `transaction_id`, `customer_id`, `amount`, `transaction_date` or amount being less than or equal to 0.
        5.  `IF`: Filters the data, keeping only records where `validation_status` is 'VALID'.
        6.  `PROC SQL`: Calculates the number of valid records and total records using `COUNT(*)`, storing results in macro variables `valid_count` and `total_count`, respectively.
        7.  `%PUT`: Logs the validation results, displaying the number of valid records out of the total.
3.  **Macro Execution**:
    1.  `%IMPORT_TRANSACTIONS`: Called to import the CSV file (`transactions.csv`) from the specified input path (`/data/raw`) into a SAS dataset named `WORK.raw_transactions`.
    2.  `%VALIDATE_DATA`: Called to validate the data in `WORK.raw_transactions`, creating a validated dataset named `WORK.transactions_validated`.
4.  `PROC PRINT`: Displays the first 10 observations of the validated dataset (`WORK.transactions_validated`).

#### 2. Business Rules Implemented

*   **Data Validation:**
    *   Missing `transaction_id`: Record marked as invalid.
    *   Missing `customer_id`: Record marked as invalid.
    *   Missing `amount`: Record marked as invalid.
    *   Missing `transaction_date`: Record marked as invalid.
    *   `amount` <= 0: Record marked as invalid.
*   **Data Filtering**:
    *   Only records with `validation_status = 'VALID'` are kept.

#### 3. IF/ELSE Conditional Logic Breakdown

*   **`%IMPORT_TRANSACTIONS`**:
    *   `%IF &SYSERR > 0 %THEN %DO;`: Checks for import errors. If `SYSERR` is greater than 0, an error occurred.
*   **`%VALIDATE_DATA`**:
    *   `IF missing(transaction_id) THEN validation_status = 'MISSING_ID';`: Checks for missing `transaction_id`.
    *   `ELSE IF missing(customer_id) THEN validation_status = 'MISSING_CUSTOMER';`: Checks for missing `customer_id`.
    *   `ELSE IF missing(amount) THEN validation_status = 'MISSING_AMOUNT';`: Checks for missing `amount`.
    *   `ELSE IF missing(transaction_date) THEN validation_status = 'MISSING_DATE';`: Checks for missing `transaction_date`.
    *   `ELSE IF amount <= 0 THEN validation_status = 'INVALID_AMOUNT';`: Checks if the amount is invalid.
    *   `ELSE validation_status = 'VALID';`: If none of the above conditions are met, the record is considered valid.
    *   `IF validation_status = 'VALID';`: Keeps only the valid records.

#### 4. DO Loop Processing Logic

*   No DO loops are present in this program.

#### 5. Key Calculations and Transformations

*   **Data Validation**: Setting the `validation_status` based on missing or invalid data.

#### 6. Data Validation Logic

*   Missing value checks for key variables.
*   Amount validation (checking for non-positive values).
*   Filtering to retain valid records only.

### Program: 02_data_quality_cleaning.sas

#### 1. Macros and Steps Execution Order & Purpose

1.  **`%CLEAN_TRANSACTIONS`**:
    *   **Purpose**: Cleans and standardizes transaction data.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `LENGTH`: Defines the length of the `transaction_type_clean`, `merchant_name_clean`, and `country_code_clean` variables.
        4.  `transaction_type_clean = UPCASE(STRIP(transaction_type));`: Converts `transaction_type` to uppercase and removes leading/trailing spaces.
        5.  `merchant_name_clean = PROPCASE(STRIP(merchant_name));`: Converts `merchant_name` to proper case and removes leading/trailing spaces.
        6.  `country_code_clean = UPCASE(SUBSTR(country_code, 1, 2));`: Extracts the first two characters of `country_code`, converts them to uppercase, and standardizes the country code.
        7.  `IF missing(amount) THEN amount = 0;`: Handles missing `amount` values by replacing them with 0.
        8.  `IF NOT missing(transaction_date) THEN DO; ... END;`: Converts `transaction_date` to a SAS date value if not missing, and formats it.
        9.  `transaction_datetime = DHMS(transaction_date_sas, HOUR(transaction_time), MINUTE(transaction_time), SECOND(transaction_time));`: Creates `transaction_datetime` variable by combining date and time components.
        10. `FORMAT transaction_datetime DATETIME20.;`: Formats transaction datetime variable.
        11. `%PUT`: Logs a note indicating the cleaning process.
2.  **`%REMOVE_DUPLICATES`**:
    *   **Purpose**: Removes duplicate records based on a specified key.
    *   **Steps**:
        1.  `PROC SORT`: Sorts the input dataset by the specified `key` variable, and removes duplicate records using the `NODUPKEY` option.
        2.  `PROC SQL`: Counts the number of records before and after duplicate removal and stores the counts in macro variables `before_count` and `after_count`.
        3.  `%LET`: Calculates the number of removed duplicates.
        4.  `%PUT`: Logs a note indicating the number of duplicate records removed.
3.  **`%HANDLE_OUTLIERS`**:
    *   **Purpose**: Handles outliers in a specified variable using either Winsorization or removal.
    *   **Steps**:
        1.  `PROC MEANS`: Calculates the 1st and 99th percentiles of the specified `var` variable and outputs the results to a temporary dataset named `percentiles`.
        2.  `DATA _NULL_`: Uses a data step to read the `percentiles` dataset and store the percentile values in macro variables `p1_value` and `p99_value`.
        3.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        4.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        5.  `%IF &method = WINSORIZE %THEN %DO; ... %END;`: If the `method` macro variable is set to `WINSORIZE`, it caps the values of the `var` variable at the 1st and 99th percentiles.
        6.  `%ELSE %IF &method = REMOVE %THEN %DO; ... %END;`: If the `method` macro variable is set to `REMOVE`, it removes the outliers using the 1st and 99th percentiles.
        7.  `%PUT`: Logs a note indicating the outlier handling method used and the variable.
4.  **Macro Execution**:
    1.  `%CLEAN_TRANSACTIONS`: Called to clean the validated transactions dataset (`WORK.transactions_validated`) and creates `WORK.transactions_cleaned`.
    2.  `%REMOVE_DUPLICATES`: Called to remove duplicate transactions from `WORK.transactions_cleaned` based on the `transaction_id` and creates `WORK.transactions_deduped`.
    3.  `%HANDLE_OUTLIERS`: Called to handle outliers in the `amount` variable of `WORK.transactions_deduped` using the `WINSORIZE` method, creating `WORK.transactions_final`.
5.  `PROC MEANS`: Calculates and displays statistics (N, Mean, STD, MIN, MAX) for the `amount` variable in the `WORK.transactions_final` dataset.

#### 2. Business Rules Implemented

*   **Data Standardization**:
    *   `transaction_type`: Converted to uppercase.
    *   `merchant_name`: Converted to proper case.
    *   `country_code`: Standardized to uppercase, taking the first two characters.
*   **Missing Value Handling**:
    *   Missing `amount` values are replaced with 0.
*   **Date Conversion**:
    *   Converts `transaction_date` to SAS date format (`YYMMDD10.`).
*   **Duplicate Removal**:
    *   Removes duplicate records based on `transaction_id`.
*   **Outlier Handling**:
    *   `WINSORIZE`: Caps values at the 1st and 99th percentiles of the `amount` variable.
    *   `REMOVE`: Removes values outside the 1st and 99th percentiles of the `amount` variable.

#### 3. IF/ELSE Conditional Logic Breakdown

*   **`%CLEAN_TRANSACTIONS`**:
    *   `IF missing(amount) THEN amount = 0;`: Replaces missing `amount` values with 0.
    *   `IF NOT missing(transaction_date) THEN DO; ... END;`: Converts `transaction_date` to SAS date only if it's not missing.
*   **`%HANDLE_OUTLIERS`**:
    *   `%IF &method = WINSORIZE %THEN %DO;`: Conditional block for Winsorization.
        *   `IF &var < &p1_value then &var = &p1_value;`: Caps values below the 1st percentile.
        *   `ELSE IF &var > &p99_value then &var = &p99_value;`: Caps values above the 99th percentile.
    *   `%ELSE %IF &method = REMOVE %THEN %DO;`: Conditional block for outlier removal.
        *   `IF &var >= &p1_value AND &var <= &p99_value;`: Keeps only values within the 1st and 99th percentiles.

#### 4. DO Loop Processing Logic

*   No DO loops are present in this program.

#### 5. Key Calculations and Transformations

*   **Data Standardization**: Converting to uppercase, proper case, and extracting/standardizing parts of fields.
*   **Missing Value Imputation**: Replacing missing amounts with 0.
*   **Date Conversion**: Converting strings to SAS date values.
*   **Datetime Creation**: Combining date and time components.
*   **Percentile Calculation**: Used for outlier handling.

#### 6. Data Validation Logic

*   Missing amount imputation.
*   Outlier handling using Winsorization or Removal.

### Program: 03_feature_engineering.sas

#### 1. Macros and Steps Execution Order & Purpose

1.  **`%CALCULATE_VELOCITY`**:
    *   **Purpose**: Calculates rolling window transaction velocity features (transaction count, total amount, and average amount) for a given customer over a specified time window.
    *   **Steps**:
        1.  `PROC SORT`: Sorts the input dataset by `customer_id`, `transaction_date_sas`, and `transaction_time` to enable the rolling window calculations.
        2.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        3.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        4.  `BY`: Specifies the `customer_id` variable for processing.
        5.  `RETAIN`: Retains the rolling window calculation variables across observations within each customer.
        6.  `IF FIRST.customer_id THEN DO; ... END;`: Initializes rolling window variables at the beginning of each customer's transactions.
        7.  `IF NOT missing(last_txn_date) THEN ... ELSE ...`: Calculates `days_since_last_txn`.
        8.  `IF NOT missing(last_txn_date) THEN DO; ... END; ELSE DO; ... END;`: Updates rolling window counters, checking if the current transaction falls within the rolling window.
        9.  `last_txn_date = transaction_date_sas;`: Updates the `last_txn_date` for the next transaction.
        10. `avg_txn_amount_&window_days.d = txn_amount_&window_days.d / txn_count_&window_days.d;`: Calculates the average transaction amount within the window.
        11. `DROP last_txn_date;`: Drops the temporary variable.
        12. `%PUT`: Logs a note indicating the velocity features calculation.
2.  **`%CALCULATE_AMOUNT_DEVIATION`**:
    *   **Purpose**: Calculates statistical features related to the deviation of each transaction amount from a customer's average transaction amount.
    *   **Steps**:
        1.  `PROC MEANS`: Calculates the average amount, standard deviation of amount, and the number of transactions per customer.
        2.  `PROC SQL`: Merges the customer statistics with the transaction data and calculates the z-score and percentage deviation of the amount.
3.  **`%CREATE_TIME_FEATURES`**:
    *   **Purpose**: Creates time-based features from the `transaction_date_sas` and `transaction_time` variables.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `txn_hour = HOUR(transaction_time);`: Extracts the hour from the transaction time.
        4.  `txn_day_of_week = WEEKDAY(transaction_date_sas);`: Extracts the day of the week from the transaction date.
        5.  `txn_day_of_month = DAY(transaction_date_sas);`: Extracts the day of the month from the transaction date.
        6.  `txn_month = MONTH(transaction_date_sas);`: Extracts the month from the transaction date.
        7.  `IF/ELSE IF/ELSE`: Categorizes `time_of_day` based on the `txn_hour`.
        8.  `is_weekend = (txn_day_of_week IN (1, 7));`: Creates a weekend flag.
        9.  `is_unusual_hour = (txn_hour >= 0 AND txn_hour < 6);`: Creates a flag for unusual hours.
        10. `%PUT`: Logs a note indicating the time features creation.
4.  **`%CREATE_LOCATION_FEATURES`**:
    *   **Purpose**: Creates location-based features based on the `country_code_clean` variable.
    *   **Steps**:
        1.  `PROC SQL`: Calculates the transaction counts per country and stores the results in a temporary table `country_counts`.
        2.  `PROC SQL`: Merges the country counts with the transaction data and creates features like `is_rare_country` and `is_international`.
        3.  `%PUT`: Logs a note indicating the location features creation.
5.  **Macro Execution**:
    1.  `%CALCULATE_VELOCITY`: Calculates velocity features based on a 7-day window using `WORK.transactions_final` and stores the result in `WORK.txn_with_velocity`.
    2.  `%CALCULATE_AMOUNT_DEVIATION`: Calculates the amount deviation features using `WORK.txn_with_velocity` and stores the result in `WORK.txn_with_deviation`.
    3.  `%CREATE_TIME_FEATURES`: Creates time-based features using `WORK.txn_with_deviation` and stores the result in `WORK.txn_with_time_features`.
    4.  `%CREATE_LOCATION_FEATURES`: Creates location-based features using `WORK.txn_with_time_features` and stores the result in `WORK.transactions_engineered`.
6.  `PROC PRINT`: Displays a sample of the engineered features from `WORK.transactions_engineered`.

#### 2. Business Rules Implemented

*   **Velocity Features**: Rolling window calculations for transaction count, total amount, and average amount per customer.
*   **Amount Deviation**: Calculates z-score and percentage deviation of transaction amounts compared to customer averages.
*   **Time-Based Features**:
    *   Extraction of hour, day of the week, day of the month, and month.
    *   Categorization of time of day (NIGHT, MORNING, AFTERNOON, EVENING).
    *   Weekend flag.
    *   Unusual hour flag (0:00-06:00).
*   **Location-Based Features**:
    *   Counts of transactions per country.
    *   Rare country flag (transaction count < 10).
    *   International transaction flag (country code not 'US').

#### 3. IF/ELSE Conditional Logic Breakdown

*   **`%CALCULATE_VELOCITY`**:
    *   `IF FIRST.customer_id THEN DO; ... END;`: Initializes rolling window variables at the start of each customer's transactions.
    *   `IF NOT missing(last_txn_date) THEN ... ELSE ...`: Calculates `days_since_last_txn`.
    *   `IF NOT missing(last_txn_date) THEN DO; ... END; ELSE DO; ... END;`: Updates rolling window counters, checking if the current transaction falls within the rolling window.
*   **`%CREATE_TIME_FEATURES`**:
    *   `IF txn_hour >= 0 AND txn_hour < 6 THEN time_of_day = 'NIGHT';`: Categorizes the hour into time of day.
    *   `ELSE IF txn_hour >= 6 AND txn_hour < 12 THEN time_of_day = 'MORNING';`
    *   `ELSE IF txn_hour >= 12 AND txn_hour < 18 THEN time_of_day = 'AFTERNOON';`
    *   `ELSE time_of_day = 'EVENING';`
    *   `is_weekend = (txn_day_of_week IN (1, 7));`: Creates a weekend flag.
    *   `is_unusual_hour = (txn_hour >= 0 AND txn_hour < 6);`: Creates an unusual hour flag.
*   **`%CREATE_LOCATION_FEATURES`**:
    *   `CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END AS is_rare_country`: Creates rare country flag.
    *   `CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END AS is_international`: Creates international transaction flag.

#### 4. DO Loop Processing Logic

*   No explicit DO loops are used in this program. The rolling window calculations in the `%CALCULATE_VELOCITY` macro effectively implement a rolling window using `RETAIN` and `BY` statements.

#### 5. Key Calculations and Transformations

*   **Rolling Window Calculations**: Calculating transaction count, total amount, and average amount within a rolling window.
*   **Z-score Calculation**: Calculating the z-score for transaction amounts.
*   **Percentage Deviation Calculation**: Calculating the percentage deviation of transaction amounts.
*   **Time Component Extraction**: Extracting hour, day of the week, day of the month, and month.
*   **Categorical Variable Creation**: Creating `time_of_day`, `is_weekend`, `is_unusual_hour`, `is_rare_country`, and `is_international` features.

#### 6. Data Validation Logic

*   No explicit data validation logic is present in this program. The program focuses on feature engineering.

### Program: 04_rule_based_detection.sas

#### 1. Macros and Steps Execution Order & Purpose

1.  **`%APPLY_FRAUD_RULES`**:
    *   **Purpose**: Applies rule-based fraud detection logic and assigns a rule score and risk level to each transaction.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `LENGTH`: Defines the length of the `rule_triggered` variable.
        4.  Initializes `rule_triggered` to an empty string and `rule_score` to 0.
        5.  `IF` statements: Implements the fraud detection rules, and if a rule is triggered, the `rule_triggered` variable is updated, and the `rule_score` is incremented.
        6.  `IF/ELSE IF/ELSE`: Assigns `rule_risk_level` based on the `rule_score`.
        7.  `is_suspicious = (rule_score >= 50);`: Creates a flag to indicate suspicious transactions.
        8.  `%PUT`: Logs a note indicating the fraud rules application.
2.  **`%GENERATE_RULE_ALERTS`**:
    *   **Purpose**: Generates alerts based on a rule score threshold and provides summary statistics.
    *   **Steps**:
        1.  `DATA`: Filters transactions based on the `rule_score` and the specified `threshold`.
        2.  `PROC SORT`: Sorts the alert dataset in descending order of `rule_score` and `transaction_date_sas`.
        3.  `PROC FREQ`: Generates a frequency table of `rule_risk_level`.
        4.  `PROC SQL`: Calculates the number of alerts and the total number of transactions.
        5.  `%LET`: Calculates the alert rate.
        6.  `%PUT`: Logs a note indicating the number of generated alerts and the alert rate.
3.  **`%RULE_SUMMARY_REPORT`**:
    *   **Purpose**: Creates a summary report of the triggered rules.
    *   **Steps**:
        1.  `PROC SQL`: Creates a summary table (`rule_summary`) that counts the number of times each rule was triggered.
        2.  `PROC PRINT`: Displays the `rule_summary` table.
4.  **Macro Execution**:
    1.  `%APPLY_FRAUD_RULES`: Applies the fraud rules to the engineered transaction dataset (`WORK.transactions_engineered`) and stores the result in `WORK.transactions_with_rules`.
    2.  `%GENERATE_RULE_ALERTS`: Generates alerts based on a threshold of 50 for the `rule_score` using `WORK.transactions_with_rules` and stores the result in `WORK.rule_based_alerts`.
    3.  `%RULE_SUMMARY_REPORT`: Generates a summary report of triggered rules based on `WORK.transactions_with_rules`.
5.  `PROC PRINT`: Displays the top 20 fraud alerts from `WORK.rule_based_alerts`.

#### 2. Business Rules Implemented

*   **Fraud Rules**:
    1.  **HIGH_VELOCITY**: `txn_count_7d > 10` (Score: 25)
    2.  **AMOUNT_DEVIATION**: `ABS(amount_zscore) > 3` (Score: 30)
    3.  **HIGH_AMOUNT**: `amount > 5000` (Score: 20)
    4.  **UNUSUAL_HOUR**: `is_unusual_hour = 1` (Score: 15)
    5.  **INTERNATIONAL**: `is_international = 1` (Score: 10)
    6.  **RARE_COUNTRY**: `is_rare_country = 1` (Score: 15)
    7.  **RAPID_SUCCESSION**: `days_since_last_txn < 0.042` (less than 1 hour) (Score: 25)
    8.  **ROUND_AMOUNT**: `MOD(amount, 100) = 0 AND amount >= 1000` (Score: 10)
*   **Risk Level Assignment**:
    *   `CRITICAL`: `rule_score >= 75`
    *   `HIGH`: `rule_score >= 50`
    *   `MEDIUM`: `rule_score >= 25`
    *   `LOW`: Otherwise
*   **Suspicious Transaction Flag**:
    *   `is_suspicious = (rule_score >= 50)`

#### 3. IF/ELSE Conditional Logic Breakdown

*   **`%APPLY_FRAUD_RULES`**:
    *   `IF txn_count_7d > 10 THEN DO; ... END;`: Rule 1 - High Velocity.
    *   `IF ABS(amount_zscore) > 3 THEN DO; ... END;`: Rule 2 - High Amount Deviation.
    *   `IF amount > 5000 THEN DO; ... END;`: Rule 3 - High Amount.
    *   `IF is_unusual_hour = 1 THEN DO; ... END;`: Rule 4 - Unusual Hour.
    *   `IF is_international = 1 THEN DO; ... END;`: Rule 5 - International Transaction.
    *   `IF is_rare_country = 1 THEN DO; ... END;`: Rule 6 - Rare Country.
    *   `IF days_since_last_txn < 0.042 THEN DO; ... END;`: Rule 7 - Rapid Succession.
    *   `IF MOD(amount, 100) = 0 AND amount >= 1000 THEN DO; ... END;`: Rule 8 - Round Amount.
    *   `IF rule_score >= 75 THEN rule_risk_level = 'CRITICAL';`: Risk Level assignment.
    *   `ELSE IF rule_score >= 50 THEN rule_risk_level = 'HIGH';`
    *   `ELSE IF rule_score >= 25 THEN rule_risk_level = 'MEDIUM';`
    *   `ELSE rule_risk_level = 'LOW';`
    *   `is_suspicious = (rule_score >= 50);`: Sets suspicious flag.

#### 4. DO Loop Processing Logic

*   No DO loops are used in this program.

#### 5. Key Calculations and Transformations

*   **Rule Scoring**: Assigning scores based on triggered rules.
*   **Risk Level Assignment**: Categorizing risk levels based on the total rule score.
*   **Suspicious Flagging**: Setting a flag for transactions above a certain risk score threshold.

#### 6. Data Validation Logic

*   No explicit data validation logic is present in this program.

### Program: 05_ml_scoring_model.sas

#### 1. Macros and Steps Execution Order & Purpose

1.  **`%PREPARE_ML_DATA`**:
    *   **Purpose**: Prepares the data for ML model scoring, including feature creation and normalization.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `is_high_amount = (amount > 1000);`: Creates a binary flag for high amounts.
        4.  `is_very_high_amount = (amount > 5000);`: Creates a binary flag for very high amounts.
        5.  `amount_normalized = amount / 10000;`: Normalizes the amount variable.
        6.  `txn_count_normalized = txn_count_7d / 20;`: Normalizes the transaction count.
        7.  `IF missing(amount_zscore) then amount_zscore = 0;`: Handles missing values in `amount_zscore`.
        8.  `IF missing(days_since_last_txn) then days_since_last_txn = 999;`: Handles missing values in `days_since_last_txn`.
        9.  `amount_x_velocity = amount_normalized * txn_count_normalized;`: Creates an interaction feature.
        10. `amount_x_deviation = amount_normalized * ABS(amount_zscore);`: Creates an interaction feature.
        11. `%PUT`: Logs a note indicating the data preparation.
2.  **`%CALCULATE_ML_SCORE`**:
    *   **Purpose**: Calculates an ML-based fraud score using a simulated logistic regression model.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `logit_score = ...`: Calculates the logit score using a linear combination of features and coefficients.
        4.  `ml_fraud_probability = 1 / (1 + EXP(-logit_score));`: Converts the logit score to a probability using the sigmoid function.
        5.  `ml_fraud_score = ml_fraud_probability * 100;`: Converts the probability to a score (0-100).
        6.  `IF/ELSE IF/ELSE`: Assigns `ml_risk_band` based on `ml_fraud_score`.
        7.  `ml_alert = (ml_fraud_score >= 60);`: Sets an ML alert flag based on the fraud score.
        8.  `FORMAT ml_fraud_probability PERCENT8.2;`: Formats the ml fraud probability.
        9.  `%PUT`: Logs a note indicating the ml fraud scores calculation.
3.  **`%ML_PERFORMANCE_METRICS`**:
    *   **Purpose**: Generates performance metrics for the ML model.
    *   **Steps**:
        1.  `PROC MEANS`: Calculates descriptive statistics for `ml_fraud_score` and `ml_fraud_probability`.
        2.  `PROC FREQ`: Generates frequency tables for `ml_risk_band` and `ml_alert`.
4.  **`%COMPARE_MODELS`**:
    *   **Purpose**: Compares the ML model's performance with the rule-based model and calculates a combined score.
    *   **Steps**:
        1.  `DATA`: Creates a new dataset specified by the `outds` macro variable.
        2.  `SET`: Reads data from the input dataset specified by the `inds` macro variable.
        3.  `IF/ELSE IF/ELSE ELSE`: Categorizes the agreement between the ML model and the rule-based model.
        4.  `combined_score = (ml_fraud_score * 0.6) + (rule_score * 0.4);`: Calculates a combined score.
        5.  `IF/ELSE IF/ELSE`: Assigns a `combined_risk_level` based on the combined score.
        6.  `PROC FREQ`: Generates a frequency table for `model_agreement`.
        7.  `PROC CORR`: Calculates the correlation between `ml_fraud_score` and `rule_score`.
        8.  `%PUT`: Logs a note indicating the model comparison.
5.  **Macro Execution**:
    1.  `%PREPARE_ML_DATA`: Prepares the data for ML scoring using `WORK.transactions_with_rules` and stores the result in `WORK.ml_data_prepared`.
    2.  `%CALCULATE_ML_SCORE`: Calculates the ML fraud scores using `WORK.ml_data_prepared` and stores the result in `WORK.transactions_ml_scored`.
    3.  `%ML_PERFORMANCE_METRICS`: Generates performance metrics for the ML model using `WORK.transactions_ml_scored`.
    4.  `%COMPARE_MODELS`: Compares the ML and rule-based models using `WORK.transactions_ml_scored` and stores the result in `WORK.transactions_combined_score`.
6.  `PROC PRINT`: Displays the top 20 ML-based fraud alerts from `WORK.transactions_ml_scored`.

#### 2. Business Rules Implemented

*   **Feature Creation**:
    *   Binary flags for high and very high amounts.
    *   Normalization of amount and transaction count.
    *   Interaction features (`amount_x_velocity`, `amount_x_deviation`).
*   **Simulated Logistic Regression**:
    *   Calculates a logit score using a linear combination of features and coefficients.
    *   Converts the logit score to a probability using the sigmoid function.
    *   Converts the probability to a fraud score (0-100).
*   **ML Risk Band Assignment**:
    *   `CRITICAL`: `ml_fraud_score >= 80`
    *   `HIGH`: `ml_fraud_score >= 60`
    *   `MEDIUM`: `ml_fraud_score >= 40`
    *   `LOW`: `ml_fraud_score >= 20`
    *   `VERY_LOW`: Otherwise
*   **ML Alert Flag**:
    *   `ml_alert = (ml_fraud_score >= 60)`
*   **Model Agreement Categorization**:
    *   `BOTH_ALERT`: Both ML and rule-based models alert.
    *   `ML_ONLY`: Only ML model alerts.
    *   `RULE_ONLY`: Only rule-based model alerts.
    *   `BOTH_CLEAR`: Neither model alerts.
*   **Combined Score**:
    *   Weighted average of the ML and rule-based scores.
*   **Combined Risk Level**:
    *   Risk level assigned based on the combined score.

#### 3. IF/ELSE Conditional Logic Breakdown

*   **`%PREPARE_ML_DATA`**:
    *   No IF/ELSE is present in this macro.
*   **`%CALCULATE_ML_SCORE`**:
    *   `IF ml_fraud_score >= 80 then ml_risk_band = 'CRITICAL';`: Risk band assignment.
    *   `ELSE IF ml_fraud_score >= 60 then ml_risk_band = 'HIGH';`
    *   `ELSE IF ml_fraud_score >= 40 then ml_risk_band = 'MEDIUM';`
    *   `ELSE IF ml_fraud_score >= 20 then ml_risk_band = 'LOW';`
    *   `ELSE ml_risk_band = 'VERY_LOW';`
    *   `ml_alert = (ml_fraud_score >= 60);`: Sets alert flag.
*   **`%COMPARE_MODELS`**:
    *   `IF ml_alert = 1 AND is_suspicious = 1 then model_agreement = 'BOTH_ALERT';`: Model