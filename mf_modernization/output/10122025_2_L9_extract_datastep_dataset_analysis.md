This document provides a detailed analysis of the provided SAS programs, focusing on data flow, transformations, and key programming constructs.

---

# 01_transaction_data_import.sas

## Program Description
This program is responsible for importing raw transaction data from a CSV file and performing an initial validation step to ensure data quality before further processing.

## Datasets Created and Consumed

### Consumed Datasets
*   **External File**: `/data/raw/transactions.csv`
    *   **Description**: The source CSV file containing raw transaction records. It is expected to have columns such as `transaction_id`, `customer_id`, `amount`, `transaction_date`, `transaction_type`, `merchant_name`, `country_code`, `transaction_time`.

### Created Datasets
*   **WORK.raw_transactions** (Temporary)
    *   **Description**: A SAS dataset created directly from the import of the `/data/raw/transactions.csv` file. It holds the raw, unvalidated transaction data.
*   **WORK.transactions_validated** (Temporary)
    *   **Description**: A SAS dataset derived from `WORK.raw_transactions` after applying validation rules. This dataset contains only records identified as 'VALID' based on the specified criteria.

## Input Sources

*   **`PROC IMPORT` DATAFILE**:
    *   **Source**: `&input_path/&transaction_file` which resolves to `/data/raw/transactions.csv`.
    *   **Details**: This statement reads data from the specified CSV file directly into the `WORK.raw_transactions` SAS dataset. `GETNAMES=YES` indicates that the first row of the CSV contains variable names.
*   **`SET` Statement**:
    *   **Source**: `&output_lib..raw_transactions` which resolves to `WORK.raw_transactions`.
    *   **Details**: Used within the `VALIDATE_DATA` macro to read records from the `WORK.raw_transactions` dataset for validation processing.
*   **`PROC SQL` SELECT**:
    *   **Source**: `&outds` (resolves to `WORK.transactions_validated`) and `&inds` (resolves to `WORK.raw_transactions`).
    *   **Details**: Used to count records in the validated dataset and the raw dataset for logging purposes, storing counts in macro variables `valid_count` and `total_count`.

## Output Datasets

*   **WORK.raw_transactions**: Temporary
*   **WORK.transactions_validated**: Temporary

## Key Variable Usage and Transformations

*   **`validation_status` (new variable)**:
    *   **Description**: A new character variable created in the `VALIDATE_DATA` macro to flag the validation outcome for each record.
    *   **Transformations**: Assigned values like 'MISSING_ID', 'MISSING_CUSTOMER', 'MISSING_AMOUNT', 'MISSING_DATE', 'INVALID_AMOUNT', or 'VALID' based on conditional checks.
*   **`transaction_id`, `customer_id`, `amount`, `transaction_date`**:
    *   **Usage**: These variables are checked for missing values (`missing()`) to determine `validation_status`.
*   **`amount`**:
    *   **Usage**: Checked if the value is less than or equal to zero (`amount <= 0`) to determine `validation_status`.
*   **Filtering**:
    *   Only records where `validation_status = 'VALID'` are kept in the `WORK.transactions_validated` dataset.

## RETAIN Statements and Variable Initialization

*   No `RETAIN` statements are used in this program.
*   The `validation_status` variable is initialized with a `length` statement before its values are assigned based on conditions.

## LIBNAME and FILENAME Assignments

*   No explicit `LIBNAME` or `FILENAME` statements are used.
*   The `PROC IMPORT` statement directly uses a file path constructed from macro variables for the `DATAFILE` option.

---

# 02_data_quality_cleaning.sas

## Program Description
This program focuses on cleaning and standardizing the validated transaction data. It performs tasks such as standardizing text fields, handling missing numerical values, converting dates, removing duplicate records, and handling outliers in transaction amounts.

## Datasets Created and Consumed

### Consumed Datasets
*   **WORK.transactions_validated** (Temporary)
    *   **Description**: The output from the previous program, containing transactions that passed initial validation.

### Created Datasets
*   **WORK.transactions_cleaned** (Temporary)
    *   **Description**: Derived from `WORK.transactions_validated` after applying various cleaning and standardization transformations to text fields, handling missing amounts, and converting date/time fields to SAS formats.
*   **WORK.transactions_deduped** (Temporary)
    *   **Description**: Derived from `WORK.transactions_cleaned` with duplicate records removed based on the `transaction_id`.
*   **WORK.transactions_final** (Temporary)
    *   **Description**: Derived from `WORK.transactions_deduped` after handling outliers in the `amount` variable, specifically by winsorizing (capping) values at the 1st and 99th percentiles.
*   **WORK.percentiles** (Temporary)
    *   **Description**: An intermediate dataset created by `PROC MEANS` to store the 1st and 99th percentile values of the `amount` variable, used for outlier handling.

## Input Sources

*   **`SET` Statement**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_validated`, `WORK.transactions_cleaned`, `WORK.transactions_deduped` in successive macro calls).
    *   **Details**: Used in `CLEAN_TRANSACTIONS` and `HANDLE_OUTLIERS` macros to read records for processing.
*   **`PROC SORT` DATA**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_cleaned`).
    *   **Details**: Used in `REMOVE_DUPLICATES` macro to sort the dataset by `transaction_id` before removing duplicates.
*   **`PROC MEANS` DATA**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_deduped`).
    *   **Details**: Used in `HANDLE_OUTLIERS` macro to calculate percentiles for the `amount` variable.
*   **`SET` Statement (for `percentiles`)**:
    *   **Source**: `percentiles`.
    *   **Details**: Used in a `DATA _NULL_` step to read the calculated percentile values and store them in macro variables.
*   **`PROC SQL` SELECT**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_cleaned`) and `&outds` (resolves to `WORK.transactions_deduped`).
    *   **Details**: Used in `REMOVE_DUPLICATES` macro to count records before and after deduplication for logging.

## Output Datasets

*   **WORK.transactions_cleaned**: Temporary
*   **WORK.transactions_deduped**: Temporary
*   **WORK.transactions_final**: Temporary
*   **WORK.percentiles**: Temporary

## Key Variable Usage and Transformations

*   **`transaction_type_clean` (new variable)**:
    *   **Description**: Standardized version of `transaction_type`.
    *   **Transformations**: `UPCASE(STRIP(transaction_type))` converts to uppercase and removes leading/trailing spaces.
*   **`merchant_name_clean` (new variable)**:
    *   **Description**: Cleaned version of `merchant_name`.
    *   **Transformations**: `PROPCASE(STRIP(merchant_name))` converts to proper case and removes leading/trailing spaces.
*   **`country_code_clean` (new variable)**:
    *   **Description**: Standardized country code.
    *   **Transformations**: `UPCASE(SUBSTR(country_code, 1, 2))` converts to uppercase and takes the first two characters.
*   **`amount`**:
    *   **Transformations**: `if missing(amount) then amount = 0;` replaces missing values with 0. In `HANDLE_OUTLIERS`, values are winsorized (capped) using `p1_value` and `p99_value`.
*   **`transaction_date_sas` (new variable)**:
    *   **Description**: Transaction date converted to a SAS date format.
    *   **Transformations**: `INPUT(transaction_date, YYMMDD10.)` converts a character date string to a numeric SAS date value. Formatted as `DATE9.`.
*   **`transaction_datetime` (new variable)**:
    *   **Description**: Combined transaction date and time into a SAS datetime format.
    *   **Transformations**: `DHMS(transaction_date_sas, HOUR(transaction_time), MINUTE(transaction_time), SECOND(transaction_time))` creates a datetime value. Formatted as `DATETIME20.`.
*   **`transaction_id`**:
    *   **Usage**: Used as the `BY` variable in `PROC SORT` with `NODUPKEY` to identify and remove duplicate records.

## RETAIN Statements and Variable Initialization

*   No `RETAIN` statements are used in this program.
*   New character variables (`transaction_type_clean`, `merchant_name_clean`, `country_code_clean`) are initialized with `length` statements.
*   `transaction_date_sas` and `transaction_datetime` are implicitly initialized as numeric when created.

## LIBNAME and FILENAME Assignments

*   No explicit `LIBNAME` or `FILENAME` statements are used.

---

# 03_feature_engineering.sas

## Program Description
This program focuses on creating new features from the cleaned transaction data, which are often used in fraud detection models. Features include velocity-based metrics, amount deviation metrics, time-based components, and location-based indicators.

## Datasets Created and Consumed

### Consumed Datasets
*   **WORK.transactions_final** (Temporary)
    *   **Description**: The output from the previous program, containing cleaned, deduplicated, and outlier-handled transaction data.

### Created Datasets
*   **WORK.txn_with_velocity** (Temporary)
    *   **Description**: Derived from `WORK.transactions_final` with added velocity features, such as transaction count and amount within a specified rolling window (e.g., 7 days) and days since the last transaction.
*   **WORK.customer_stats** (Temporary)
    *   **Description**: An intermediate dataset created by `PROC MEANS` to store customer-level statistics (average amount, standard deviation, transaction count) for use in calculating amount deviation features.
*   **WORK.txn_with_deviation** (Temporary)
    *   **Description**: Derived from `WORK.txn_with_velocity` with added amount deviation features, such as transaction amount z-score and percentage deviation from a customer's average.
*   **WORK.txn_with_time_features** (Temporary)
    *   **Description**: Derived from `WORK.txn_with_deviation` with added time-based features, including hour, day of week, day of month, month, time-of-day categories, and weekend/unusual hour flags.
*   **WORK.country_counts** (Temporary)
    *   **Description**: An intermediate dataset created by `PROC SQL` to store the total transaction count for each country, used for location-based features.
*   **WORK.transactions_engineered** (Temporary)
    *   **Description**: The final dataset containing all engineered features, derived from `WORK.txn_with_time_features` with added location-based features like country transaction count, rare country flag, and international transaction flag.

## Input Sources

*   **`SET` Statement**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_final`, `WORK.txn_with_velocity`, `WORK.txn_with_deviation` in successive macro calls).
    *   **Details**: Used in `CALCULATE_VELOCITY`, `CREATE_TIME_FEATURES` macros to read records for processing.
*   **`PROC SORT` DATA**:
    *   **Source**: `&inds` (resolves to `WORK.transactions_final`).
    *   **Details**: Used in `CALCULATE_VELOCITY` macro to sort the dataset by `customer_id`, `transaction_date_sas`, and `transaction_time` to enable correct sequential calculations for velocity features.
*   **`PROC MEANS` DATA**:
    *   **Source**: `&inds` (resolves to `WORK.txn_with_velocity`).
    *   **Details**: Used in `CALCULATE_AMOUNT_DEVIATION` macro to calculate customer-level aggregate statistics (`MEAN`, `STD`, `N` of `amount`).
*   **`PROC SQL` CREATE TABLE AS SELECT**:
    *   **Source**: `&inds` (resolves to `WORK.txn_with_velocity`, `WORK.txn_with_time_features`) and intermediate datasets (`customer_stats`, `country_counts`).
    *   **Details**: Used in `CALCULATE_AMOUNT_DEVIATION` and `CREATE_LOCATION_FEATURES` macros to perform joins and create new features using SQL.
*   **`LEFT JOIN`**:
    *   **Source**: `customer_stats` and `country_counts`.
    *   **Details**: Used in `CALCULATE_AMOUNT_DEVIATION` and `CREATE_LOCATION_FEATURES` macros to merge calculated aggregate statistics back to the transaction-level data based on `customer_id` or `country_code_clean`.

## Output Datasets

*   **WORK.txn_with_velocity**: Temporary
*   **WORK.customer_stats**: Temporary
*   **WORK.txn_with_deviation**: Temporary
*   **WORK.txn_with_time_features**: Temporary
*   **WORK.country_counts**: Temporary
*   **WORK.transactions_engineered**: Temporary

## Key Variable Usage and Transformations

*   **`days_since_last_txn` (new variable)**:
    *   **Description**: Number of days since the customer's previous transaction.
    *   **Transformations**: `transaction_date_sas - last_txn_date`.
*   **`txn_count_&window_days.d`, `txn_amount_&window_days.d` (new variables)**:
    *   **Description**: Rolling count and sum of transactions within the specified `window_days` (e.g., 7 days) for each customer.
    *   **Transformations**: Incremented conditionally based on `days_since_last_txn` and reset on new `customer_id` or if the transaction falls outside the window.
*   **`avg_txn_amount_&window_days.d` (new variable)**:
    *   **Description**: Average transaction amount within the rolling window.
    *   **Transformations**: `txn_amount_&window_days.d / txn_count_&window_days.d`.
*   **`customer_avg_amount`, `customer_std_amount`, `customer_txn_count` (new variables)**:
    *   **Description**: Customer-level aggregate statistics of transaction `amount`.
    *   **Transformations**: Calculated using `PROC MEANS` grouped by `customer_id`.
*   **`amount_zscore` (new variable)**:
    *   **Description**: Z-score of the current transaction amount relative to the customer's average and standard deviation.
    *   **Transformations**: `(a.amount - b.customer_avg_amount) / b.customer_std_amount`. Handles division by zero.
*   **`amount_pct_deviation` (new variable)**:
    *   **Description**: Percentage deviation of the current transaction amount from the customer's average.
    *   **Transformations**: `((a.amount - b.customer_avg_amount) / b.customer_avg_amount) * 100`. Handles division by zero.
*   **`txn_hour`, `txn_day_of_week`, `txn_day_of_month`, `txn_month` (new variables)**:
    *   **Description**: Extracted time components from `transaction_time` and `transaction_date_sas`.
    *   **Transformations**: `HOUR()`, `WEEKDAY()`, `DAY()`, `MONTH()` functions.
*   **`time_of_day` (new variable)**:
    *   **Description**: Categorical time-of-day (e.g., 'NIGHT', 'MORNING', 'AFTERNOON', 'EVENING').
    *   **Transformations**: Conditional assignment based on `txn_hour`.
*   **`is_weekend` (new variable)**:
    *   **Description**: Binary flag indicating if the transaction occurred on a weekend.
    *   **Transformations**: `(txn_day_of_week IN (1, 7))`.
*   **`is_unusual_hour` (new variable)**:
    *   **Description**: Binary flag indicating if the transaction occurred during unusual hours (e.g., 0-5 AM).
    *   **Transformations**: `(txn_hour >= 0 AND txn_hour < 6)`.
*   **`country_txn_count` (new variable)**:
    *   **Description**: Total transaction count for each `country_code_clean`.
    *   **Transformations**: `COUNT(*)` grouped by `country_code_clean` in `PROC SQL`.
*   **`is_rare_country` (new variable)**:
    *   **Description**: Binary flag indicating if the country has a low transaction count (e.g., less than 10).
    *   **Transformations**: `CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END`.
*   **`is_international` (new variable)**:
    *   **Description**: Binary flag indicating if the transaction is international (not 'US').
    *   **Transformations**: `CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END`.

## RETAIN Statements and Variable Initialization

*   **`RETAIN` Statement**:
    *   **Variables**: `txn_count_&window_days.d 0`, `txn_amount_&window_days.d 0`, `last_txn_date .`
    *   **Details**: These variables are retained across rows within each `customer_id` group in the `CALCULATE_VELOCITY` macro to enable rolling sum/count calculations.
*   **Variable Initialization**:
    *   `txn_count_&window_days.d`, `txn_amount_&window_days.d`, `last_txn_date`:
        *   Initialized to `0` or `.` (missing) at the start of each new `customer_id` group (`if FIRST.customer_id then do;`).
        *   `last_txn_date` is updated with `transaction_date_sas` for the current record to be used in the next iteration.
*   New character variables (`time_of_day`) are initialized with `length` statements.

## LIBNAME and FILENAME Assignments

*   No explicit `LIBNAME` or `FILENAME` statements are used.