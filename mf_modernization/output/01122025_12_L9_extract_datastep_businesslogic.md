## 01_transaction_data_import.sas

*   **List of DATA macros and steps:**

    1.  **Macro:** `IMPORT_TRANSACTIONS`
        *   **Purpose:** Imports transaction data from a CSV file.
        *   **Steps:**
            *   `PROC IMPORT`: Imports the CSV file specified by the `filepath` macro variable into a SAS dataset specified by the `outds` macro variable.
            *   `%PUT`: Logs a note indicating the successful import.
            *   `%IF`: Checks the `SYSERR` automatic macro variable to determine if the import was successful. If `SYSERR` is greater than 0, indicating an error, it logs an error message and aborts the program.
    2.  **Macro:** `VALIDATE_DATA`
        *   **Purpose:** Validates the imported transaction data by checking for missing values and amount validity, and filters out invalid records.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `LENGTH`: Defines the length of the `validation_status` variable.
                *   `IF/ELSE IF/ELSE`: Conditional logic to check for missing values in `transaction_id`, `customer_id`, `amount`, and `transaction_date`, and if amount is less than or equal to 0, setting the `validation_status` accordingly. If no issues are found, it sets `validation_status` to 'VALID'.
                *   `IF`: Filters the data, keeping only records where `validation_status` is 'VALID'.
            *   `PROC SQL`: Calculates the number of valid and total records.
                *   `SELECT COUNT(*) INTO`: Queries to count valid and total records and stores the results in macro variables `valid_count` and `total_count` respectively.
            *   `%PUT`: Logs the number of validated records out of the total records.
    3.  **Macro Execution:**
        *   `%IMPORT_TRANSACTIONS`: Executes the `IMPORT_TRANSACTIONS` macro to import the CSV file (`transactions.csv`) from the specified input path (`/data/raw`) and stores the imported data in `WORK.raw_transactions`.
        *   `%VALIDATE_DATA`: Executes the `VALIDATE_DATA` macro to validate the data in `WORK.raw_transactions` and stores the validated data in `WORK.transactions_validated`.
    4.  `PROC PRINT`: Displays the first 10 observations of the validated transactions dataset (`WORK.transactions_validated`).

*   **Business Rules implemented in DATA steps:**

    *   Missing Value Checks: Checks for missing values in `transaction_id`, `customer_id`, `amount`, and `transaction_date`. If any are missing, a `validation_status` is set.
    *   Amount Validation: Checks if the `amount` is less than or equal to 0. If true, a `validation_status` is set.
    *   Data Filtering: Only records with a `validation_status` of 'VALID' are kept, effectively removing records that failed the validation rules.

*   **IF/ELSE conditional logic breakdown:**

    *   `IMPORT_TRANSACTIONS` Macro:
        *   `%IF &SYSERR > 0 %THEN %DO;`: Checks if the system error variable (`SYSERR`) is greater than 0, indicating an error during the import process. If an error occurred, the code within the `%DO` block is executed, logging an error and aborting the program.
    *   `VALIDATE_DATA` Macro:
        *   `IF missing(transaction_id) THEN validation_status = 'MISSING_ID';`: Checks if `transaction_id` is missing.
        *   `ELSE IF missing(customer_id) THEN validation_status = 'MISSING_CUSTOMER';`: Checks if `customer_id` is missing if `transaction_id` is not missing.
        *   `ELSE IF missing(amount) THEN validation_status = 'MISSING_AMOUNT';`: Checks if `amount` is missing if `customer_id` is not missing.
        *   `ELSE IF missing(transaction_date) THEN validation_status = 'MISSING_DATE';`: Checks if `transaction_date` is missing if `amount` is not missing.
        *   `ELSE IF amount <= 0 THEN validation_status = 'INVALID_AMOUNT';`: Checks if amount is less than or equal to zero if `transaction_date` is not missing.
        *   `ELSE validation_status = 'VALID';`: If none of the above conditions are met, the record is considered valid.

*   **DO loop processing logic:**

    *   There are no DO loops in this program.

*   **Key calculations and transformations:**

    *   Data Import: Imports data from a CSV file.
    *   Validation Status: Assigns validation status based on data quality checks.
    *   Record Filtering: Keeps only the valid records based on the validation status.
    *   Counts: Calculates the number of valid and total records using PROC SQL.

*   **Data validation logic:**

    *   Missing Value Checks: Validation for missing values in key transaction fields.
    *   Amount Validation: Validation for the amount field to ensure it is greater than zero.
    *   Data Filtering: Filters the data to keep only the valid records.

## 02_data_quality_cleaning.sas

*   **List of DATA macros and steps:**

    1.  **Macro:** `CLEAN_TRANSACTIONS`
        *   **Purpose:** Cleans and standardizes transaction data.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `LENGTH`: Defines the length of the new variables.
                *   `transaction_type_clean = UPCASE(STRIP(transaction_type));`: Converts `transaction_type` to uppercase and removes leading/trailing spaces.
                *   `merchant_name_clean = PROPCASE(STRIP(merchant_name));`: Converts `merchant_name` to proper case (first letter uppercase, rest lowercase) and removes leading/trailing spaces.
                *   `country_code_clean = UPCASE(SUBSTR(country_code, 1, 2));`: Extracts the first two characters of `country_code`, converts them to uppercase, and removes leading/trailing spaces.
                *   `IF missing(amount) THEN amount = 0;`: Replaces missing `amount` values with 0.
                *   `IF NOT missing(transaction_date) THEN DO;`: Converts `transaction_date` to a SAS date format if the date is not missing.
                    *   `transaction_date_sas = INPUT(transaction_date, YYMMDD10.);`: Converts the character date to a SAS date value.
                    *   `FORMAT transaction_date_sas DATE9.;`: Formats the SAS date value.
                    *   `END;`
                *   `transaction_datetime = DHMS(transaction_date_sas, HOUR(transaction_time), MINUTE(transaction_time), SECOND(transaction_time));`: Combines the SAS date and time components into a single datetime value.
                *   `FORMAT transaction_datetime DATETIME20.;`: Formats the datetime value.
            *   `%PUT`: Logs a note indicating the successful cleaning.
    2.  **Macro:** `REMOVE_DUPLICATES`
        *   **Purpose:** Removes duplicate records based on a specified key variable.
        *   **Steps:**
            *   `PROC SORT`: Sorts the input dataset `inds` by the key variable (`key`) and removes duplicate records using the `NODUPKEY` option, storing the result in the `outds` dataset.
            *   `PROC SQL`: Calculates the number of records before and after duplicate removal.
                *   `SELECT COUNT(*) INTO`: Queries to count the records before and after sorting and removing duplicates, storing the results in the macro variables `before_count` and `after_count`.
            *   `%LET dup_count = %EVAL(&before_count - &after_count);`: Calculates the number of duplicates removed.
            *   `%PUT`: Logs a note indicating the number of duplicate records removed.
    3.  **Macro:** `HANDLE_OUTLIERS`
        *   **Purpose:** Handles outliers in a specified variable using either Winsorizing or removing the outliers.
        *   **Steps:**
            *   `PROC MEANS`: Calculates the 1st and 99th percentiles of the specified variable (`var`) in the input dataset `inds`.
                *   `OUTPUT OUT=percentiles`: Saves the percentile results in a dataset named `percentiles`.
            *   `DATA _NULL_`: Uses a data step to read the `percentiles` dataset and create macro variables for the 1st and 99th percentile values.
                *   `CALL SYMPUTX`: Creates macro variables `p1_value` and `p99_value` and assigns the percentile values to them.
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `%IF &method = WINSORIZE %THEN %DO;`: Conditional logic based on the `method` macro variable.
                    *   `IF &var < &p1_value then &var = &p1_value;`: If the variable is less than the 1st percentile, it's set to the 1st percentile value.
                    *   `ELSE IF &var > &p99_value then &var = &p99_value;`: If the variable is greater than the 99th percentile, it's set to the 99th percentile value.
                    *   `END;`
                *   `%ELSE IF &method = REMOVE %THEN %DO;`: Conditional logic based on the `method` macro variable.
                    *   `IF &var >= &p1_value AND &var <= &p99_value;`: Keeps the records where the variable is within the 1st and 99th percentile range.
                    *   `END;`
            *   `%PUT`: Logs a note indicating the outlier handling method and variable used.
    4.  **Macro Execution:**
        *   `%CLEAN_TRANSACTIONS`: Executes the `CLEAN_TRANSACTIONS` macro to clean the validated transactions dataset (`WORK.transactions_validated`) and stores the cleaned data in `WORK.transactions_cleaned`.
        *   `%REMOVE_DUPLICATES`: Executes the `REMOVE_DUPLICATES` macro to remove duplicates from the cleaned transactions dataset (`WORK.transactions_cleaned`) based on the `transaction_id` key, storing the deduped data in `WORK.transactions_deduped`.
        *   `%HANDLE_OUTLIERS`: Executes the `HANDLE_OUTLIERS` macro to handle outliers in the `amount` variable of the deduped transactions dataset (`WORK.transactions_deduped`) using the Winsorize method, storing the final data in `WORK.transactions_final`.
    5.  `PROC MEANS`: Calculates and displays descriptive statistics (N, MEAN, STD, MIN, MAX) for the `amount` variable in the final dataset (`WORK.transactions_final`).

*   **Business Rules implemented in DATA steps:**

    *   Amount Replacement: Missing values in the `amount` field are replaced with 0.
    *   Data Standardization: Standardization of `transaction_type`, `merchant_name`, and `country_code`.
    *   Date Conversion: Conversion of `transaction_date` to SAS date format.
    *   Outlier Handling: Winsorizing or removing outliers from the `amount` variable.

*   **IF/ELSE conditional logic breakdown:**

    *   `CLEAN_TRANSACTIONS` Macro:
        *   `IF missing(amount) THEN amount = 0;`: Replaces missing `amount` values with 0.
        *   `IF NOT missing(transaction_date) THEN DO;`: Converts `transaction_date` to a SAS date format if the date is not missing.
    *   `HANDLE_OUTLIERS` Macro:
        *   `%IF &method = WINSORIZE %THEN %DO;`: Based on the `method` macro variable.
            *   `IF &var < &p1_value then &var = &p1_value;`: If the variable is less than the 1st percentile, it's set to the 1st percentile value.
            *   `ELSE IF &var > &p99_value then &var = &p99_value;`: If the variable is greater than the 99th percentile, it's set to the 99th percentile value.
            *   `END;`
        *   `%ELSE IF &method = REMOVE %THEN %DO;`: Based on the `method` macro variable.
            *   `IF &var >= &p1_value AND &var <= &p99_value;`: Keeps the records where the variable is within the 1st and 99th percentile range.
            *   `END;`

*   **DO loop processing logic:**

    *   There are no DO loops in this program.

*   **Key calculations and transformations:**

    *   Data Standardization: Cleaning and standardizing of transaction data.
    *   Missing Value Imputation: Replacing missing amounts with 0.
    *   Date Conversion: Converting character dates to SAS date values.
    *   Datetime Creation: Combining date and time components into a datetime value.
    *   Duplicate Removal: Removing duplicate records based on a specified key.
    *   Outlier Handling: Winsorizing or removing outliers.
    *   Descriptive Statistics: Calculating descriptive statistics for the amount.

*   **Data validation logic:**

    *   Missing Value Imputation: Handles missing values by replacing them with 0.
    *   Data Standardization: Standardizing key transaction data.
    *   Outlier Handling:  Addresses extreme values in the amount variable.

## 03_feature_engineering.sas

*   **List of DATA macros and steps:**

    1.  **Macro:** `CALCULATE_VELOCITY`
        *   **Purpose:** Calculates velocity features (transaction counts and amounts within a rolling window) for each customer.
        *   **Steps:**
            *   `PROC SORT`: Sorts the input dataset `inds` by `customer_id`, `transaction_date_sas`, and `transaction_time`.
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `BY customer_id`: Specifies that the calculations are performed within each customer's data.
                *   `RETAIN`: Retains the values of the following variables across observations within each customer: `txn_count_&window_days.d`, `txn_amount_&window_days.d`, and `last_txn_date`.
                *   `IF FIRST.customer_id THEN DO;`: Resets the counters and `last_txn_date` at the beginning of each new customer's data.
                *   `IF NOT missing(last_txn_date) THEN`: Calculates `days_since_last_txn` if `last_txn_date` is not missing.
                *   `IF NOT missing(last_txn_date) THEN DO;`: Updates transaction counters and amounts within the rolling window.
                    *   `IF days_since_last_txn <= &window_days then do;`:  If the transaction falls within the rolling window, the count and amount are incremented.
                    *   `ELSE do;`: If the transaction is outside the rolling window, the counters are reset.
                    *   `end;`
                *   `ELSE do;`:  Initializes the counters if `last_txn_date` is missing.
                *   `last_txn_date = transaction_date_sas;`: Updates the `last_txn_date`.
                *   `avg_txn_amount_&window_days.d = txn_amount_&window_days.d / txn_count_&window_days.d;`: Calculates the average transaction amount within the rolling window.
                *   `DROP last_txn_date;`: Drops the `last_txn_date` variable.
            *   `%PUT`: Logs a note indicating the successful calculation of velocity features.
    2.  **Macro:** `CALCULATE_AMOUNT_DEVIATION`
        *   **Purpose:** Calculates amount deviation features (average amount, standard deviation, Z-score, and percentage deviation) for each customer.
        *   **Steps:**
            *   `PROC MEANS`: Calculates the mean, standard deviation, and count of the `amount` variable for each `customer_id`.
                *   `OUTPUT OUT=customer_stats`: Saves the results in a dataset named `customer_stats`.
            *   `PROC SQL`: Merges the customer statistics back into the main dataset and calculates the Z-score and percentage deviation.
                *   `CREATE TABLE &outds AS`: Creates a new dataset specified by the `outds` macro variable, which is the result of the `SELECT` statement.
                *   `SELECT a.*, b.customer_avg_amount, b.customer_std_amount, b.customer_txn_count`: Selects all columns from the input dataset (`a`) and merges in the customer statistics (`b`).
                *   `CASE WHEN b.customer_std_amount > 0 THEN (a.amount - b.customer_avg_amount) / b.customer_std_amount ELSE 0 END AS amount_zscore`: Calculates the Z-score. If the standard deviation is 0, the Z-score is set to 0.
                *   `CASE WHEN b.customer_avg_amount > 0 THEN ((a.amount - b.customer_avg_amount) / b.customer_avg_amount) * 100 ELSE 0 END AS amount_pct_deviation`: Calculates the percentage deviation. If the average amount is 0, the percentage deviation is set to 0.
                *   `FROM &inds a LEFT JOIN customer_stats b ON a.customer_id = b.customer_id`: Joins the input dataset (`a`) with the customer statistics dataset (`b`) using `customer_id`.
            *   `%PUT`: Logs a note indicating the successful calculation of amount deviation features.
    3.  **Macro:** `CREATE_TIME_FEATURES`
        *   **Purpose:** Creates time-based features from the transaction date and time.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `txn_hour = HOUR(transaction_time);`: Extracts the hour from the transaction time.
                *   `txn_day_of_week = WEEKDAY(transaction_date_sas);`: Extracts the day of the week from the transaction date.
                *   `txn_day_of_month = DAY(transaction_date_sas);`: Extracts the day of the month from the transaction date.
                *   `txn_month = MONTH(transaction_date_sas);`: Extracts the month from the transaction date.
                *   `length time_of_day $20;`: Defines the length of the `time_of_day` variable.
                *   `IF/ELSE IF/ELSE IF/ELSE`: Assigns the `time_of_day` category based on the transaction hour.
                *   `is_weekend = (txn_day_of_week IN (1, 7));`: Creates a weekend flag.
                *   `is_unusual_hour = (txn_hour >= 0 AND txn_hour < 6);`: Creates an unusual hour flag.
            *   `%PUT`: Logs a note indicating the successful creation of time-based features.
    4.  **Macro:** `CREATE_LOCATION_FEATURES`
        *   **Purpose:** Creates location-based features.
        *   **Steps:**
            *   `PROC SQL`: Calculates the transaction counts by country code.
                *   `CREATE TABLE country_counts AS`: Creates a new dataset named `country_counts` as a result of the `SELECT` statement.
                *   `SELECT country_code_clean, COUNT(*) AS country_txn_count`: Counts the number of transactions for each `country_code_clean`.
                *   `FROM &inds GROUP BY country_code_clean`: Groups the data by `country_code_clean`.
            *   `PROC SQL`: Merges the country counts back into the main dataset and creates features.
                *   `CREATE TABLE &outds AS`: Creates a new dataset specified by the `outds` macro variable, which is the result of the `SELECT` statement.
                *   `SELECT a.*, b.country_txn_count`: Selects all columns from the input dataset (`a`) and merges in the country counts (`b`).
                *   `CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END AS is_rare_country`: Creates a flag indicating if a country is rare (transaction count less than 10).
                *   `CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END AS is_international`: Creates a flag indicating if a transaction is international.
                *   `FROM &inds a LEFT JOIN country_counts b ON a.country_code_clean = b.country_code_clean`: Joins the input dataset (`a`) with the country counts dataset (`b`) using `country_code_clean`.
            *   `%PUT`: Logs a note indicating the successful creation of location-based features.
    5.  **Macro Execution:**
        *   `%CALCULATE_VELOCITY`: Executes the `CALCULATE_VELOCITY` macro to calculate velocity features on the final cleaned data (`WORK.transactions_final`), storing the results in `WORK.txn_with_velocity`.
        *   `%CALCULATE_AMOUNT_DEVIATION`: Executes the `CALCULATE_AMOUNT_DEVIATION` macro to calculate amount deviation features on the dataset with velocity features (`WORK.txn_with_velocity`), storing the results in `WORK.txn_with_deviation`.
        *   `%CREATE_TIME_FEATURES`: Executes the `CREATE_TIME_FEATURES` macro to create time-based features on the dataset with deviation features (`WORK.txn_with_deviation`), storing the results in `WORK.txn_with_time_features`.
        *   `%CREATE_LOCATION_FEATURES`: Executes the `CREATE_LOCATION_FEATURES` macro to create location-based features on the dataset with time features (`WORK.txn_with_time_features`), storing the results in `WORK.transactions_engineered`.
    6.  `PROC PRINT`: Displays a sample of the engineered features from `WORK.transactions_engineered`.

*   **Business Rules implemented in DATA steps:**

    *   Velocity Calculation: Calculates transaction counts and amounts within a rolling window for each customer.
    *   Amount Deviation Calculation: Calculates customer-specific statistics (mean, standard deviation) and then determines Z-scores and percentage deviations for each transaction.
    *   Time-Based Feature Creation: Categorizes transaction times into time-of-day buckets, and creates weekend and unusual hour flags.
    *   Location-Based Feature Creation:  Creates a flag for rare countries (low transaction volume) and an international transaction flag.

*   **IF/ELSE conditional logic breakdown:**

    *   `CREATE_TIME_FEATURES` Macro:
        *   `IF txn_hour >= 0 AND txn_hour < 6 then time_of_day = 'NIGHT';`: Assigns `time_of_day` based on the transaction hour.
        *   `ELSE IF txn_hour >= 6 AND txn_hour < 12 then time_of_day = 'MORNING';`: Assigns `time_of_day` based on the transaction hour.
        *   `ELSE IF txn_hour >= 12 AND txn_hour < 18 then time_of_day = 'AFTERNOON';`: Assigns `time_of_day` based on the transaction hour.
        *   `ELSE time_of_day = 'EVENING';`: Assigns `time_of_day` based on the transaction hour.

*   **DO loop processing logic:**

    *   There are no DO loops in this program.

*   **Key calculations and transformations:**

    *   Velocity Feature Calculation: Rolling window calculations for transaction counts and amounts.
    *   Amount Deviation Calculation: Z-score and percentage deviation calculations.
    *   Time-Based Feature Engineering: Extraction and categorization of time components.
    *   Location-Based Feature Engineering: Creation of rare country and international transaction flags.
    *   Aggregation: Calculation of customer-level statistics.
    *   Merging: Joining datasets to incorporate calculated features.

*   **Data validation logic:**

    *   There is no explicit data validation logic in this program.

## 04_rule_based_detection.sas

*   **List of DATA macros and steps:**

    1.  **Macro:** `APPLY_FRAUD_RULES`
        *   **Purpose:** Applies rule-based fraud detection logic and calculates a rule score.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `length rule_triggered $200;`: Defines the length of the `rule_triggered` variable.
                *   `rule_triggered = '';`: Initializes the `rule_triggered` variable.
                *   `rule_score = 0;`: Initializes the `rule_score` variable.
                *   `IF/DO`: Implements fraud detection rules.  Each rule checks a specific condition and, if met, appends the rule's name to `rule_triggered` and adds points to the `rule_score`.
                *   `length rule_risk_level $10;`: Defines the length of the `rule_risk_level` variable.
                *   `IF/ELSE IF/ELSE IF/ELSE`: Assigns a risk level based on the `rule_score`.
                *   `is_suspicious = (rule_score >= 50);`: Creates a flag indicating whether the transaction is suspicious based on the rule score.
            *   `%PUT`: Logs a note indicating the successful application of fraud detection rules.
    2.  **Macro:** `GENERATE_RULE_ALERTS`
        *   **Purpose:** Generates alerts based on the rule score and provides a summary.
        *   **Steps:**
            *   `DATA`: Filters the input dataset `inds` to include only transactions with a `rule_score` greater than or equal to the `threshold` (default is 50). The result is stored in the `outds` dataset.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `WHERE rule_score >= &threshold;`: Filters the data based on the threshold.
            *   `PROC SORT`: Sorts the alert dataset (`outds`) in descending order of `rule_score` and `transaction_date_sas`.
            *   `PROC FREQ`: Generates a frequency table of the `rule_risk_level`.
            *   `PROC SQL`: Calculates the number of alerts and the total number of transactions.
                *   `SELECT COUNT(*) INTO`: Queries to count the number of alerts and the total number of transactions, storing the results in the macro variables `alert_count` and `total_count` respectively.
            *   `%LET alert_rate = %SYSEVALF((&alert_count / &total_count) * 100);`: Calculates the alert rate.
            *   `%PUT`: Logs a note indicating the number of alerts and the alert rate.
    3.  **Macro:** `RULE_SUMMARY_REPORT`
        *   **Purpose:** Creates a summary report of rule triggers.
        *   **Steps:**
            *   `PROC SQL`: Creates a summary table (`rule_summary`) that counts the number of times each rule was triggered.
                *   `SELECT 'HIGH_VELOCITY' AS rule_name, SUM(CASE WHEN INDEX(rule_triggered, 'HIGH_VELOCITY') > 0 THEN 1 ELSE 0 END) AS trigger_count`: Counts the number of times the 'HIGH_VELOCITY' rule was triggered.
                *   `UNION ALL`: Combines the results for all rules.
            *   `PROC PRINT`: Displays the rule summary table.
    4.  **Macro Execution:**
        *   `%APPLY_FRAUD_RULES`: Executes the `APPLY_FRAUD_RULES` macro to apply the fraud detection rules to the engineered transaction data (`WORK.transactions_engineered`) and stores the results in `WORK.transactions_with_rules`.
        *   `%GENERATE_RULE_ALERTS`: Executes the `GENERATE_RULE_ALERTS` macro to generate alerts based on a threshold of 50 from the dataset with rule results (`WORK.transactions_with_rules`), storing the alerts in `WORK.rule_based_alerts`.
        *   `%RULE_SUMMARY_REPORT`: Executes the `RULE_SUMMARY_REPORT` macro to create a summary report of rule triggers based on the transactions with rules dataset (`WORK.transactions_with_rules`).
    5.  `PROC PRINT`: Displays the top 20 fraud alerts, including the relevant variables, from the `WORK.rule_based_alerts` dataset.

*   **Business Rules implemented in DATA steps:**

    *   High Velocity:  More than 10 transactions in 7 days.
    *   Amount Deviation: Transaction amount deviates more than 3 standard deviations from the customer's average.
    *   High Amount:  Transaction amount is greater than \$5000.
    *   Unusual Hour: Transaction occurs during unusual hours (0-6 AM).
    *   International Transaction: Transaction is international (country code not 'US').
    *   Rare Country: Transaction is from a rare country.
    *   Rapid Succession: Multiple transactions in short time (less than 1 hour).
    *   Round Amount: Transaction amount is a round number (multiple of 100) and greater than or equal to \$1000.
    *   Risk Scoring: A score is assigned to each transaction based on which rules are triggered.
    *   Risk Level Assignment: A risk level (CRITICAL, HIGH, MEDIUM, LOW) is assigned based on the rule score.
    *   Alert Generation:  Transactions with a rule score above a threshold are flagged as alerts.

*   **IF/ELSE conditional logic breakdown:**

    *   `APPLY_FRAUD_RULES` Macro:
        *   `IF txn_count_7d > 10 then do;`: Rule 1: High Velocity.
        *   `IF ABS(amount_zscore) > 3 then do;`: Rule 2: Amount Deviation.
        *   `IF amount > 5000 then do;`: Rule 3: High Amount.
        *   `IF is_unusual_hour = 1 then do;`: Rule 4: Unusual Hour.
        *   `IF is_international = 1 then do;`: Rule 5: International Transaction.
        *   `IF is_rare_country = 1 then do;`: Rule 6: Rare Country.
        *   `IF days_since_last_txn < 0.042 then do;`: Rule 7: Rapid Succession.
        *   `IF MOD(amount, 100) = 0 AND amount >= 1000 then do;`: Rule 8: Round Amount.
        *   `IF rule_score >= 75 then rule_risk_level = 'CRITICAL';`: Assigns risk levels based on the rule score.
        *   `ELSE IF rule_score >= 50 then rule_risk_level = 'HIGH';`: Assigns risk levels based on the rule score.
        *   `ELSE IF rule_score >= 25 then rule_risk_level = 'MEDIUM';`: Assigns risk levels based on the rule score.
        *   `ELSE rule_risk_level = 'LOW';`: Assigns risk levels based on the rule score.
    *   `GENERATE_RULE_ALERTS` Macro:
        *   `WHERE rule_score >= &threshold;`: Filters transactions based on a rule score threshold.

*   **DO loop processing logic:**

    *   There are no DO loops in this program.

*   **Key calculations and transformations:**

    *   Rule Application:  Applying pre-defined fraud detection rules.
    *   Rule Scoring: Assigning scores based on triggered rules.
    *   Risk Level Assignment: Categorizing transactions based on their rule scores.
    *   Alert Generation: Identifying transactions that exceed a risk score threshold.
    *   Alert Rate Calculation: Computing the percentage of transactions that triggered alerts.
    *   Summary Report Generation: Summarizing triggered rules.

*   **Data validation logic:**

    *   This program does not contain data validation logic.

## 05_ml_scoring_model.sas

*   **List of DATA macros and steps:**

    1.  **Macro:** `PREPARE_ML_DATA`
        *   **Purpose:** Prepares the data for ML scoring by creating binary flags, normalizing continuous variables, and creating interaction features.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `is_high_amount = (amount > 1000);`: Creates a binary flag for high amounts.
                *   `is_very_high_amount = (amount > 5000);`: Creates a binary flag for very high amounts.
                *   `amount_normalized = amount / 10000;`: Normalizes the amount variable.
                *   `txn_count_normalized = txn_count_7d / 20;`: Normalizes the transaction count variable.
                *   `IF missing(amount_zscore) then amount_zscore = 0;`: Handles missing values in amount_zscore by imputing 0.
                *   `IF missing(days_since_last_txn) then days_since_last_txn = 999;`: Handles missing values in days\_since\_last\_txn by imputing 999.
                *   `amount_x_velocity = amount_normalized * txn_count_normalized;`: Creates an interaction feature.
                *   `amount_x_deviation = amount_normalized * ABS(amount_zscore);`: Creates an interaction feature.
            *   `%PUT`: Logs a note indicating the successful preparation of data for ML scoring.
    2.  **Macro:** `CALCULATE_ML_SCORE`
        *   **Purpose:** Calculates an ML-based fraud score using a simulated logistic regression model.
        *   **Steps:**
            *   `DATA`: Creates a new dataset specified by the `outds` macro variable, based on the input dataset `inds`.
                *   `SET`: Reads data from the input dataset `inds`.
                *   `logit_score = ...`: Calculates the logit score using a linear combination of the input features and coefficients.
                *   `ml_fraud_probability = 1 / (1 + EXP(-logit_score));`: Converts the logit score to a probability using the sigmoid function.
                *   `ml_fraud_score = ml_fraud_probability * 100;`: Converts the probability to a score (0-100).
                *   `length ml_risk_band $10;`: Defines the length of the `ml_risk_band` variable.
                *   `IF/ELSE IF/ELSE IF/ELSE`: Assigns an ML risk band based on the `ml_fraud_score`.
                *   `ml_alert = (ml_fraud