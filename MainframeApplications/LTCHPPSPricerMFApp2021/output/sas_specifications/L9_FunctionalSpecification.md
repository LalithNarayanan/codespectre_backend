
# Program Overview
This document provides an analysis of the provided SAS programs, detailing their purpose, business functions, and data flow.

---

## Program: `01_transaction_data_import.sas`

### Overview of the Program

This program serves as the initial step in the data pipeline, responsible for importing raw transaction data from an external CSV file into a SAS dataset. Following the import, it performs essential preliminary data validation checks. These checks identify and filter out transactions with critical missing information (such as transaction ID, customer ID, amount, or date) or invalid amounts (e.g., non-positive amounts), ensuring that only fundamentally sound records proceed to subsequent processing stages.

### List of all the Business Functions Addressed by the Program

*   **Data Ingestion**: Facilitates the automated loading of raw transaction data from an external flat file (CSV) into the SAS environment, making it accessible for further analysis.
*   **Initial Data Quality Control**: Implements foundational data integrity checks at the point of entry. This includes validating the presence of key identifiers and ensuring numerical fields like `amount` meet basic business rules (e.g., being positive).
*   **Data Preparation for Analysis**: Creates a baseline dataset that has undergone initial scrutiny, establishing a reliable starting point for subsequent data cleaning, transformation, and feature engineering.

### List of all the Datasets it Creates and Consumes, along with the Data Flow

*   **Consumes:**
    *   `transactions.csv`: An external CSV file containing raw, unvalidated transaction records. This is the primary input source.

*   **Creates:**
    *   `WORK.raw_transactions`: A temporary SAS dataset that stores the direct import of data from `transactions.csv`.
    *   `WORK.transactions_validated`: A temporary SAS dataset containing records from `WORK.raw_transactions` that have successfully passed the initial validation checks. Invalid records are excluded from this dataset.

*   **Data Flow:**
    1.  The `transactions.csv` file is imported into the `WORK.raw_transactions` SAS dataset.
    2.  The `WORK.raw_transactions` dataset is then processed to apply initial validation rules.
    3.  Records that satisfy the validation criteria are written to the `WORK.transactions_validated` SAS dataset, which is the final output of this program.

---

## Program: `02_data_quality_cleaning.sas`

### Overview of the Program

This program is dedicated to enhancing the quality, consistency, and usability of the transaction data through a series of cleaning and standardization operations. It addresses issues such as inconsistent text formatting, missing numerical values, improper date/time data types, duplicate records, and extreme outliers in transaction amounts. The goal is to produce a refined dataset that is robust and reliable for advanced analytical tasks, particularly for fraud detection modeling.

### List of all the Business Functions Addressed by the Program

*   **Data Standardization**: Ensures uniformity across various data fields, such as converting text fields (e.g., transaction type, merchant name, country code) to a consistent case and format.
*   **Missing Value Imputation**: Manages missing values in critical numerical fields (specifically `amount`) by replacing them with a predefined default, preventing errors in subsequent calculations.
*   **Date/Time Data Type Conversion**: Transforms raw date and time strings into appropriate SAS date and datetime formats, enabling accurate chronological analysis and feature engineering.
*   **Duplicate Record Management**: Identifies and removes redundant transaction entries based on a unique identifier (`transaction_id`), preserving the integrity and uniqueness of the dataset.
*   **Outlier Treatment**: Mitigates the impact of extreme values in quantitative variables (e.g., `amount`) through methods like winsorization, which caps values at specified percentiles, thereby improving the stability and performance of analytical models.
*   **Data Preparation for Advanced Analytics**: Produces a comprehensive, clean, and well-structured dataset that is ready for complex feature engineering and predictive modeling.

### List of all the Datasets it Creates and Consumes, along with the Data Flow

*   **Consumes:**
    *   `WORK.transactions_validated`: The input dataset from the `01_transaction_data_import` program, containing transaction records that have passed initial validation.

*   **Creates:**
    *   `WORK.transactions_cleaned`: A temporary SAS dataset resulting from standardizing text fields, handling missing amounts, and converting date/time variables from `WORK.transactions_validated`.
    *   `WORK.transactions_deduped`: A temporary SAS dataset derived from `WORK.transactions_cleaned` after identifying and removing duplicate transaction records based on `transaction_id`.
    *   `WORK.transactions_final`: A temporary SAS dataset derived from `WORK.transactions_deduped` where outliers in the `amount` variable have been treated (winsorized in this specific implementation).

*   **Data Flow:**
    1.  The `WORK.transactions_validated` dataset undergoes cleaning and standardization, resulting in the `WORK.transactions_cleaned` dataset.
    2.  The `WORK.transactions_cleaned` dataset is then processed to remove duplicate records, producing `WORK.transactions_deduped`.
    3.  Finally, outlier treatment is applied to the `amount` variable in `WORK.transactions_deduped`, creating the `WORK.transactions_final` dataset, which is the final output of this program.

---

## Program: `03_feature_engineering.sas`

### Overview of the Program

This program is dedicated to the creation of new, derived features from the cleaned transaction data. These engineered features are designed to uncover latent patterns and characteristics within the data that are highly predictive of fraudulent activities. The features generated include measures of transaction velocity, deviations from typical customer spending behavior, various time-based attributes (e.g., hour of day, day of week), and location-based insights. The output is a rich dataset suitable for training and evaluating machine learning models for fraud detection.

### List of all the Business Functions Addressed by the Program

*   **Fraud Pattern Identification**: Generates sophisticated features that are critical for detecting complex fraud patterns, such as unusual transaction frequency (velocity features) or transactions that deviate significantly from a customer's normal spending habits (amount deviation features).
*   **Customer Behavior Profiling**: Develops aggregated statistical features (e.g., average amount, standard deviation of amount per customer) to establish a baseline of normal customer behavior against which individual transactions can be compared.
*   **Temporal Analysis**: Extracts and categorizes time-related attributes (e.g., transaction hour, day of the week, weekend status) to identify transactions occurring at atypical or high-risk times.
*   **Geographic Risk Assessment**: Creates features based on transaction location, such as identifying transactions from rare countries or international transactions, which may carry a higher inherent risk.
*   **Data Enrichment for Predictive Modeling**: Transforms raw and cleaned transactional attributes into a comprehensive set of predictive variables, significantly enhancing the input data for machine learning algorithms used in fraud detection.

### List of all the Datasets it Creates and Consumes, along with the Data Flow

*   **Consumes:**
    *   `WORK.transactions_final`: The input dataset from the `02_data_quality_cleaning` program, containing cleaned, standardized, de-duplicated, and outlier-treated transaction records.

*   **Creates:**
    *   `WORK.txn_with_velocity`: A temporary SAS dataset derived from `WORK.transactions_final`, enriched with features related to transaction frequency and amount within a specified time window (e.g., 7-day velocity) and days since the last transaction for each customer.
    *   `WORK.txn_with_deviation`: A temporary SAS dataset derived from `WORK.txn_with_velocity`, further enhanced with features quantifying how the current transaction amount deviates from the customer's historical average and standard deviation (e.g., amount z-score, percentage deviation).
    *   `WORK.txn_with_time_features`: A temporary SAS dataset derived from `WORK.txn_with_deviation`, incorporating various time-based features such as transaction hour, day of the week, day of the month, month, time-of-day categories, a weekend flag, and an unusual hour flag.
    *   `WORK.transactions_engineered`: A temporary SAS dataset derived from `WORK.txn_with_time_features`, which includes location-based features such as country-specific transaction counts, a flag for transactions from rare countries, and a flag indicating international transactions.

*   **Data Flow:**
    1.  The `WORK.transactions_final` dataset is used to calculate velocity features, resulting in the `WORK.txn_with_velocity` dataset.
    2.  The `WORK.txn_with_velocity` dataset is then processed to calculate amount deviation features, creating `WORK.txn_with_deviation`.
    3.  Subsequently, time-based features are generated from `WORK.txn_with_deviation`, producing `WORK.txn_with_time_features`.
    4.  Finally, location-based features are added to `WORK.txn_with_time_features`, resulting in the `WORK.transactions_engineered` dataset, which is the final output of this program and contains all derived features for subsequent modeling.
# DATA Step and Dataset Analysis
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
# DATA Step Business Logic
# SAS Program Analysis

This document provides a detailed analysis of the provided SAS programs, outlining their purpose, execution flow, business rules, conditional logic, transformations, and data validation.

## Program: `01_transaction_data_import.sas`

### Program Purpose

The primary purpose of `01_transaction_data_import.sas` is to import raw transaction data from a CSV file into a SAS dataset and perform initial validation to ensure the quality and integrity of critical transaction fields.

### Execution Flow

The program executes the following macros and steps in sequential order:

1.  **Macro Call: `%IMPORT_TRANSACTIONS`**
    *   **Purpose:** This macro is called to import the `transactions.csv` file from the `/data/raw` path into a SAS dataset named `WORK.raw_transactions`. It includes error handling to abort the program if the import fails.

2.  **Macro Call: `%VALIDATE_DATA`**
    *   **Purpose:** This macro is called to validate the `WORK.raw_transactions` dataset. It checks for missing critical fields and invalid transaction amounts, creating a new dataset named `WORK.transactions_validated` that contains only valid records.

3.  **SAS Step: `PROC PRINT`**
    *   **Purpose:** This step is executed to display the first 10 observations of the `WORK.transactions_validated` dataset, providing a quick visual inspection of the successfully imported and validated data.

### Detailed Macro and Step Analysis

#### Macro: `IMPORT_TRANSACTIONS`

*   **Purpose:** Imports data from a CSV file into a SAS dataset.
*   **Business Rules Implemented:** None within a DATA step. The macro ensures that the import process itself is successful.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `%if &SYSERR > 0 %then %do; ... %end;`: This conditional logic checks the value of the `SYSERR` automatic macro variable after the `PROC IMPORT` step.
        *   If `SYSERR` is greater than 0, it indicates that an error occurred during the `PROC IMPORT` process. An error message is logged, and the SAS session is aborted to prevent further processing with potentially corrupt or incomplete data.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:** None.
*   **Data Validation Logic:** Checks the `SYSERR` macro variable to ensure the `PROC IMPORT` step completed without system errors.

#### Macro: `VALIDATE_DATA`

*   **Purpose:** Performs initial data quality checks on the imported transaction data.
*   **Business Rules Implemented in DATA steps:**
    *   Every transaction must have a unique identifier (`transaction_id`).
    *   Every transaction must be associated with a customer (`customer_id`).
    *   Every transaction must have a specified monetary value (`amount`).
    *   Every transaction must have a recorded date (`transaction_date`).
    *   Transaction amounts must be positive (`amount > 0`).
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `if missing(transaction_id) then validation_status = 'MISSING_ID';`: If `transaction_id` is missing, the `validation_status` is set to 'MISSING_ID'.
    *   `else if missing(customer_id) then validation_status = 'MISSING_CUSTOMER';`: If `transaction_id` is present but `customer_id` is missing, `validation_status` is set to 'MISSING_CUSTOMER'.
    *   `else if missing(amount) then validation_status = 'MISSING_AMOUNT';`: If `transaction_id` and `customer_id` are present but `amount` is missing, `validation_status` is set to 'MISSING_AMOUNT'.
    *   `else if missing(transaction_date) then validation_status = 'MISSING_DATE';`: If `transaction_id`, `customer_id`, and `amount` are present but `transaction_date` is missing, `validation_status` is set to 'MISSING_DATE'.
    *   `else if amount <= 0 then validation_status = 'INVALID_AMOUNT';`: If all previous conditions are false (i.e., all critical fields are present) but `amount` is less than or equal to zero, `validation_status` is set to 'INVALID_AMOUNT'.
    *   `else validation_status = 'VALID';`: If none of the above conditions are met, the record is considered valid, and `validation_status` is set to 'VALID'.
    *   `if validation_status = 'VALID';`: This is a subsetting IF statement. Only records where `validation_status` is 'VALID' are written to the output dataset `&outds`.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:**
    *   A new character variable `validation_status` is created to categorize the validity of each record based on defined business rules.
*   **Data Validation Logic:**
    *   Checks for missing values in `transaction_id`, `customer_id`, `amount`, and `transaction_date`.
    *   Checks for non-positive values in `amount`.
    *   Filters out invalid records, ensuring that only records meeting all validation criteria are passed to the next stage.

#### SAS Step: `PROC PRINT`

*   **Purpose:** Displays a subset of the validated transactions.
*   **Business Rules Implemented:** None.
*   **IF/ELSE Conditional Logic Breakdown:** Not present.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:** None.
*   **Data Validation Logic:** None.

---

## Program: `02_data_quality_cleaning.sas`

### Program Purpose

The purpose of `02_data_quality_cleaning.sas` is to enhance the quality and standardization of the transaction data. This includes cleaning and transforming character variables, handling missing numeric values, converting date/time formats, removing duplicate records, and managing outliers in transaction amounts.

### Execution Flow

The program executes the following macros and steps in sequential order:

1.  **Macro Call: `%CLEAN_TRANSACTIONS`**
    *   **Purpose:** This macro is called to standardize various character fields (`transaction_type`, `merchant_name`, `country_code`), impute missing `amount` values, and convert/create proper SAS date and datetime variables from existing date and time fields. The input is `WORK.transactions_validated`, and the output is `WORK.transactions_cleaned`.

2.  **Macro Call: `%REMOVE_DUPLICATES`**
    *   **Purpose:** This macro is called to remove duplicate transaction records based on `transaction_id`. It takes `WORK.transactions_cleaned` as input and produces `WORK.transactions_deduped`.

3.  **Macro Call: `%HANDLE_OUTLIERS`**
    *   **Purpose:** This macro is called to address outliers in the `amount` variable. It uses a winsorization method (capping values at the 1st and 99th percentiles) on `WORK.transactions_deduped`, storing the result in `WORK.transactions_final`.

4.  **SAS Step: `PROC MEANS`**
    *   **Purpose:** This step is executed to calculate and display descriptive statistics (N, Mean, Std Dev, Min, Max) for the `amount` variable in the final cleaned dataset (`WORK.transactions_final`), allowing for verification of the outlier handling.

### Detailed Macro and Step Analysis

#### Macro: `CLEAN_TRANSACTIONS`

*   **Purpose:** Standardizes and cleans various fields, and prepares date/time variables.
*   **Business Rules Implemented in DATA steps:**
    *   Transaction types should be standardized to uppercase and stripped of leading/trailing spaces.
    *   Merchant names should be formatted in proper case and stripped of leading/trailing spaces.
    *   Country codes should be standardized to the first two characters, converted to uppercase, and stripped of leading/trailing spaces.
    *   Missing transaction amounts should be imputed with a value of 0.
    *   Transaction dates should be converted to a standard SAS date format.
    *   A combined transaction date and time (datetime) should be created.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `if missing(amount) then amount = 0;`: If the `amount` variable is missing, its value is set to 0. This is an imputation rule.
    *   `if NOT missing(transaction_date) then do; ... end;`: This condition checks if `transaction_date` is not missing.
        *   If true, the code block within `do; ... end;` is executed to convert `transaction_date` to a SAS date value and apply a format.
*   **DO Loop Processing Logic:**
    *   `if NOT missing(transaction_date) then do; ... end;`: This is a simple DO group, not a loop, that executes a sequence of statements if the preceding `IF` condition is met.
*   **Key Calculations and Transformations:**
    *   `transaction_type_clean = UPCASE(STRIP(transaction_type));`: Converts `transaction_type` to uppercase and removes extra spaces.
    *   `merchant_name_clean = PROPCASE(STRIP(merchant_name));`: Converts `merchant_name` to proper case and removes extra spaces.
    *   `country_code_clean = UPCASE(SUBSTR(country_code, 1, 2));`: Extracts the first two characters of `country_code`, converts to uppercase, and removes extra spaces.
    *   `transaction_date_sas = INPUT(transaction_date, YYMMDD10.);`: Converts a character date string to a numeric SAS date value.
    *   `transaction_datetime = DHMS(transaction_date_sas, HOUR(transaction_time), MINUTE(transaction_time), SECOND(transaction_time));`: Combines the SAS date, hour, minute, and second components into a SAS datetime value.
*   **Data Validation Logic:** None explicitly, but the imputation of missing amounts and standardization of character fields are data quality improvement steps.

#### Macro: `REMOVE_DUPLICATES`

*   **Purpose:** Identifies and removes duplicate records based on a specified key.
*   **Business Rules Implemented in DATA steps:**
    *   Records are considered duplicates if they have the same value for the specified `key` variable (e.g., `transaction_id`). Only one instance of such a record should be retained.
*   **IF/ELSE Conditional Logic Breakdown:** Not present.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:**
    *   `PROC SORT` with the `NODUPKEY` option: This procedure sorts the data by the specified key and, during the output process, ensures that only the first occurrence of a record with a unique key value is written to the output dataset, effectively removing duplicates.
*   **Data Validation Logic:** Enforces uniqueness of records based on the primary key, preventing redundant data entries.

#### Macro: `HANDLE_OUTLIERS`

*   **Purpose:** Manages extreme values (outliers) in a numeric variable using either winsorization or removal.
*   **Business Rules Implemented in DATA steps:**
    *   Outlier transaction amounts (values below the 1st percentile or above the 99th percentile) should be handled.
    *   The method for handling outliers can be either 'WINSORIZE' (cap values at percentiles) or 'REMOVE' (exclude records).
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `%if &method = WINSORIZE %then %do; ... %end;`: This macro-level conditional logic checks if the `method` parameter is 'WINSORIZE'.
        *   `if &var < &p1_value then &var = &p1_value;`: If the value of the target variable (`&var`) is less than the 1st percentile, it is capped to the 1st percentile value.
        *   `else if &var > &p99_value then &var = &p99_value;`: If the value of the target variable is greater than the 99th percentile, it is capped to the 99th percentile value.
    *   `%else %if &method = REMOVE %then %do; ... %end;`: This macro-level conditional logic executes if the `method` parameter is 'REMOVE'.
        *   `if &var >= &p1_value AND &var <= &p99_value;`: This is a subsetting IF statement. Only records where the target variable's value falls between the 1st and 99th percentiles (inclusive) are kept in the output dataset.
*   **DO Loop Processing Logic:**
    *   `%if &method = WINSORIZE %then %do; ... %end;`: This is a macro DO group that executes the winsorization logic when the condition is true.
    *   `%else %if &method = REMOVE %then %do; ... %end;`: This is a macro DO group that executes the removal logic when the condition is true.
*   **Key Calculations and Transformations:**
    *   `PROC MEANS` calculates the 1st and 99th percentiles of the specified variable.
    *   Winsorization: Values are adjusted (`&var = &p1_value` or `&var = &p99_value`) based on percentile thresholds.
    *   Removal: Records are filtered based on percentile thresholds.
*   **Data Validation Logic:** Identifies and modifies or removes records with extreme values in a specified numeric variable, improving the statistical robustness of the dataset.

#### SAS Step: `PROC MEANS`

*   **Purpose:** Provides a statistical summary of the `amount` variable.
*   **Business Rules Implemented:** None.
*   **IF/ELSE Conditional Logic Breakdown:** Not present.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:** Calculates N, Mean, Standard Deviation, Minimum, and Maximum for the `amount` variable.
*   **Data Validation Logic:** None.

---

## Program: `03_feature_engineering.sas`

### Program Purpose

The purpose of `03_feature_engineering.sas` is to create a rich set of new features from the cleaned transaction data. These features are designed to capture various aspects of transactions, such as temporal patterns, behavioral deviations, and geographical context, which are valuable for analytical tasks like fraud detection.

### Execution Flow

The program executes the following macros and steps in sequential order:

1.  **Macro Call: `%CALCULATE_VELOCITY`**
    *   **Purpose:** This macro calculates velocity features (e.g., transaction count, total amount, average amount within a 7-day rolling window, and days since last transaction) for each customer. It takes `WORK.transactions_final` as input and outputs `WORK.txn_with_velocity`.

2.  **Macro Call: `%CALCULATE_AMOUNT_DEVIATION`**
    *   **Purpose:** This macro calculates features that measure how individual transaction amounts deviate from a customer's historical average, including Z-score and percentage deviation. It uses `WORK.txn_with_velocity` and outputs `WORK.txn_with_deviation`.

3.  **Macro Call: `%CREATE_TIME_FEATURES`**
    *   **Purpose:** This macro extracts and categorizes various time-based features from the transaction date and time, such as hour of day, day of week, time-of-day categories, and flags for weekends or unusual hours. It processes `WORK.txn_with_deviation` and generates `WORK.txn_with_time_features`.

4.  **Macro Call: `%CREATE_LOCATION_FEATURES`**
    *   **Purpose:** This macro creates location-based features, including the total transaction count per country and flags for rare or international transactions. It uses `WORK.txn_with_time_features` and outputs the final engineered dataset `WORK.transactions_engineered`.

5.  **SAS Step: `PROC PRINT`**
    *   **Purpose:** This step is executed to display a sample of 10 observations from the `WORK.transactions_engineered` dataset, showcasing some of the newly created features.

### Detailed Macro and Step Analysis

#### Macro: `CALCULATE_VELOCITY`

*   **Purpose:** Computes rolling window statistics and time difference between transactions for each customer.
*   **Business Rules Implemented in DATA steps:**
    *   Transaction velocity (count and amount) should be calculated within a specified sliding window (e.g., 7 days) for each customer.
    *   The number of days since a customer's last transaction should be tracked.
    *   When a new customer's transactions are processed, velocity counters should reset.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `if FIRST.customer_id then do; ... end;`: If the current record is the first for a given `customer_id`, the velocity counters (`txn_count_&window_days.d`, `txn_amount_&window_days.d`) and `last_txn_date` are reset to their initial values.
    *   `if NOT missing(last_txn_date) then days_since_last_txn = transaction_date_sas - last_txn_date; else days_since_last_txn = .;`: Calculates `days_since_last_txn` if a `last_txn_date` exists; otherwise, it's set to missing.
    *   `if NOT missing(last_txn_date) then do; ... end; else do; ... end;`: This block handles the update logic for the rolling window.
        *   `if days_since_last_txn <= &window_days then do; ... end;`: If the current transaction falls within the defined `window_days` from the `last_txn_date`, the count and amount for the window are incremented.
        *   `else do; ... end;`: If the current transaction is outside the window, the window counters are reset to include only the current transaction's values.
    *   `if txn_count_&window_days.d > 0 then avg_txn_amount_&window_days.d = ...; else avg_txn_amount_&window_days.d = 0;`: Calculates the average transaction amount for the window, preventing division by zero if `txn_count` is 0.
*   **DO Loop Processing Logic:**
    *   `if FIRST.customer_id then do; ... end;`: A DO group for initializing variables at the start of each customer group.
    *   `if NOT missing(last_txn_date) then do; ... end;`: A DO group for updating velocity features based on the `days_since_last_txn`.
        *   Nested `if days_since_last_txn <= &window_days then do; ... end;` and `else do; ... end;`: These are further DO groups for conditional updates within the rolling window logic.
    *   `else do; ... end;`: An `ELSE` DO group for initializing velocity features if `last_txn_date` is missing.
*   **Key Calculations and Transformations:**
    *   `days_since_last_txn = transaction_date_sas - last_txn_date;`: Calculates the difference in days between consecutive transactions for a customer.
    *   `txn_count_&window_days.d + 1;` (sum statement): Increments a counter for transactions within the window.
    *   `txn_amount_&window_days.d + amount;` (sum statement): Accumulates the total amount of transactions within the window.
    *   `avg_txn_amount_&window_days.d = txn_amount_&window_days.d / txn_count_&window_days.d;`: Calculates the average transaction amount within the window.
    *   `RETAIN` statement: Ensures variables persist values across observations within a `BY` group.
*   **Data Validation Logic:** None.

#### Macro: `CALCULATE_AMOUNT_DEVIATION`

*   **Purpose:** Calculates how individual transaction amounts deviate from a customer's typical spending behavior.
*   **Business Rules Implemented in DATA steps:**
    *   Transaction amounts should be compared against a customer's historical average and standard deviation to identify unusual behavior.
    *   Calculations involving division by zero (e.g., when standard deviation or average is zero) should be handled gracefully, typically by setting the result to zero.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `CASE WHEN b.customer_std_amount > 0 THEN ... ELSE 0 END AS amount_zscore`: This SQL `CASE` statement acts as an IF/ELSE.
        *   If `customer_std_amount` is greater than 0, the Z-score is calculated.
        *   Otherwise (to prevent division by zero), `amount_zscore` is set to 0.
    *   `CASE WHEN b.customer_avg_amount > 0 THEN ... ELSE 0 END AS amount_pct_deviation`: This SQL `CASE` statement acts as an IF/ELSE.
        *   If `customer_avg_amount` is greater than 0, the percentage deviation is calculated.
        *   Otherwise (to prevent division by zero), `amount_pct_deviation` is set to 0.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:**
    *   `PROC MEANS` calculates `customer_avg_amount`, `customer_std_amount`, and `customer_txn_count` for each customer.
    *   `amount_zscore = (a.amount - b.customer_avg_amount) / b.customer_std_amount;`: Standardizes the current transaction amount relative to the customer's mean and standard deviation.
    *   `amount_pct_deviation = ((a.amount - b.customer_avg_amount) / b.customer_avg_amount) * 100;`: Calculates the percentage difference between the current transaction amount and the customer's average.
*   **Data Validation Logic:** None.

#### Macro: `CREATE_TIME_FEATURES`

*   **Purpose:** Extracts and categorizes temporal aspects of transactions.
*   **Business Rules Implemented in DATA steps:**
    *   Time of day should be categorized into 'NIGHT' (0-5 AM), 'MORNING' (6-11 AM), 'AFTERNOON' (12-5 PM), and 'EVENING' (6 PM-11 PM).
    *   Weekends are defined as Sunday (1) or Saturday (7).
    *   Transactions occurring between 00:00 and 05:59 are considered to be during an 'unusual hour'.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `if txn_hour >= 0 AND txn_hour < 6 then time_of_day = 'NIGHT';`: If the hour is between 0 and 5, `time_of_day` is 'NIGHT'.
    *   `else if txn_hour >= 6 AND txn_hour < 12 then time_of_day = 'MORNING';`: If the hour is between 6 and 11, `time_of_day` is 'MORNING'.
    *   `else if txn_hour >= 12 AND txn_hour < 18 then time_of_day = 'AFTERNOON';`: If the hour is between 12 and 17, `time_of_day` is 'AFTERNOON'.
    *   `else time_of_day = 'EVENING';`: Otherwise (hour 18-23), `time_of_day` is 'EVENING'.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:**
    *   `txn_hour = HOUR(transaction_time);`: Extracts the hour component.
    *   `txn_day_of_week = WEEKDAY(transaction_date_sas);`: Extracts the day of the week (1=Sunday, 7=Saturday).
    *   `txn_day_of_month = DAY(transaction_date_sas);`: Extracts the day of the month.
    *   `txn_month = MONTH(transaction_date_sas);`: Extracts the month.
    *   `time_of_day` (categorization): Assigns a categorical label based on `txn_hour`.
    *   `is_weekend = (txn_day_of_week IN (1, 7));`: Creates a binary (0/1) flag for weekend transactions.
    *   `is_unusual_hour = (txn_hour >= 0 AND txn_hour < 6);`: Creates a binary (0/1) flag for transactions during unusual hours.
*   **Data Validation Logic:** None.

#### Macro: `CREATE_LOCATION_FEATURES`

*   **Purpose:** Generates features based on transaction country.
*   **Business Rules Implemented in DATA steps:**
    *   A country is considered 'rare' if it has fewer than 10 transactions recorded.
    *   Transactions not originating from 'US' are considered 'international'.
*   **IF/ELSE Conditional Logic Breakdown:**
    *   `CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END AS is_rare_country`: This SQL `CASE` statement acts as an IF/ELSE.
        *   If `country_txn_count` for a country is less than 10, `is_rare_country` is set to 1.
        *   Otherwise, it's set to 0.
    *   `CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END AS is_international`: This SQL `CASE` statement acts as an IF/ELSE.
        *   If `country_code_clean` is not 'US', `is_international` is set to 1.
        *   Otherwise, it's set to 0.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:**
    *   `country_txn_count` (from `PROC SQL` aggregation): Counts the number of transactions per country.
    *   `is_rare_country`: A binary flag indicating if a country has a low transaction volume.
    *   `is_international`: A binary flag indicating if a transaction occurred outside the 'US'.
*   **Data Validation Logic:** None.

#### SAS Step: `PROC PRINT`

*   **Purpose:** Displays a sample of the final engineered features.
*   **Business Rules Implemented:** None.
*   **IF/ELSE Conditional Logic Breakdown:** Not present.
*   **DO Loop Processing Logic:** Not present.
*   **Key Calculations and Transformations:** None.
*   **Data Validation Logic:** None.
# PROC Step and Statistical Processing
## Program: 01_transaction_data_import.sas

### List of all PROC steps with descriptions

*   **`PROC IMPORT`**: This procedure is used to import data from an external file, specifically a CSV file in this program, into a SAS dataset. It automatically reads the file and attempts to determine the data types and lengths of the variables.
*   **`PROC SQL`**: This procedure is used to execute SQL queries within SAS. In this program, it is used in `NOPRINT` mode to count the number of records in the input and output datasets, storing these counts into macro variables.
*   **`PROC PRINT`**: This procedure generates a listing of the contents of a SAS dataset. Here, it is used to display the first 10 observations of the validated transactions dataset.

### Statistical analysis methods used

This program primarily focuses on data import and initial data validation. No explicit statistical analysis methods are applied beyond basic counts.

### Predictive modeling logic

There is no predictive modeling logic within this program. Its purpose is data ingestion and initial quality checks, which are preparatory steps for any subsequent analysis or modeling.

### Macro variable definitions and usage

*   **`input_path`**: Defined as `/data/raw`. Used to specify the directory where the input CSV file is located.
*   **`output_lib`**: Defined as `WORK`. Used to specify the SAS library where the output datasets will be stored.
*   **`transaction_file`**: Defined as `transactions.csv`. Used to specify the name of the input CSV file.
*   **`filepath`**: A macro parameter in `IMPORT_TRANSACTIONS`. Used to pass the full path to the input CSV file.
*   **`outds`**: A macro parameter in `IMPORT_TRANSACTIONS` and `VALIDATE_DATA`. Used to pass the name of the output SAS dataset.
*   **`inds`**: A macro parameter in `VALIDATE_DATA`. Used to pass the name of the input SAS dataset.
*   **`SYSERR`**: An automatic SAS macro variable that stores the return code of the last executed step. Used to check for errors after `PROC IMPORT`.
*   **`valid_count`**: A macro variable created by `PROC SQL` to store the count of valid records. Used in a `%PUT` statement for logging.
*   **`total_count`**: A macro variable created by `PROC SQL` to store the total count of records. Used in a `%PUT` statement for logging.

### Report generation and formatting logic

*   **`%PUT` statements**: These statements are used extensively for logging messages to the SAS log, indicating the progress of the program, the results of macro executions (e.g., successful import, validation counts), and potential errors.
*   **`PROC PRINT`**: Generates a basic tabular report of the first 10 observations from the `transactions_validated` dataset.
*   **`TITLE` statement**: Adds a descriptive title "First 10 Validated Transactions" to the `PROC PRINT` output.

### Business application of each PROC

*   **`PROC IMPORT`**: In a business context, `PROC IMPORT` is crucial for ingesting raw transaction data from various sources (e.g., point-of-sale systems, online payment gateways, bank statements) that are often provided in flat file formats like CSV. This is the foundational step for any data analysis, reporting, or fraud detection initiative.
*   **`PROC SQL`**: Used here for data quality monitoring. By counting records before and after validation, businesses can quickly assess the volume of data successfully processed and identify potential issues with data completeness or the effectiveness of validation rules. This helps ensure that downstream analyses are based on sufficiently clean data.
*   **`PROC PRINT`**: Serves as a quick data sanity check. Business users or analysts can use this to visually inspect a sample of the imported and validated data, confirming that data types are correct, values appear reasonable, and the initial validation rules have been applied as expected, before committing to further, more resource-intensive processing.

---

## Program: 02_data_quality_cleaning.sas

### List of all PROC steps with descriptions

*   **`PROC SORT`**: This procedure sorts a SAS dataset by one or more variables. In the `REMOVE_DUPLICATES` macro, it sorts the data by a specified key and uses the `NODUPKEY` option to remove observations that have duplicate values for all variables in the `BY` statement.
*   **`PROC SQL`**: This procedure is used to execute SQL queries within SAS. In the `REMOVE_DUPLICATES` macro, it is used in `NOPRINT` mode to count records before and after duplicate removal to report the number of duplicates found.
*   **`PROC MEANS`**: This procedure calculates descriptive statistics for numeric variables. In the `HANDLE_OUTLIERS` macro, it is used in `NOPRINT` mode to calculate percentiles (specifically the 1st and 99th percentiles) of a specified variable. At the end of the program, it is used to display summary statistics (N, MEAN, STD, MIN, MAX) for the `amount` variable after all cleaning steps.

### Statistical analysis methods used

*   **Percentile Calculation**: `PROC MEANS` is used to calculate the 1st and 99th percentiles of the `amount` variable. Percentiles are a statistical measure indicating the value below which a given percentage of observations fall.
*   **Winsorization**: This is a method of outlier treatment. When `method=WINSORIZE` is specified, extreme values (below the 1st percentile or above the 99th percentile) of the `amount` variable are replaced with the values at the respective percentiles. This technique reduces the influence of outliers without completely removing them, which can be beneficial for statistical analyses and modeling.

### Predictive modeling logic

There is no predictive modeling logic in this program. It is entirely focused on data quality and cleaning, which are essential preprocessing steps for building robust predictive models. By standardizing, cleaning, and handling outliers, the program prepares the data to be more suitable and reliable for subsequent feature engineering and model training.

### Macro variable definitions and usage

*   **`input_lib`**: Defined as `WORK`. Used to specify the SAS library where input datasets are located.
*   **`output_lib`**: Defined as `WORK`. Used to specify the SAS library where output datasets will be stored.
*   **`inds`**: A macro parameter in `CLEAN_TRANSACTIONS`, `REMOVE_DUPLICATES`, and `HANDLE_OUTLIERS`. Used to pass the name of the input SAS dataset.
*   **`outds`**: A macro parameter in `CLEAN_TRANSACTIONS`, `REMOVE_DUPLICATES`, and `HANDLE_OUTLIERS`. Used to pass the name of the output SAS dataset.
*   **`key`**: A macro parameter in `REMOVE_DUPLICATES`. Used to specify the variable(s) by which to sort and identify duplicate records.
*   **`var`**: A macro parameter in `HANDLE_OUTLIERS`. Used to specify the numeric variable for which outliers are to be handled.
*   **`method`**: A macro parameter in `HANDLE_OUTLIERS`. Used to specify the outlier handling method (e.g., `WINSORIZE`, `REMOVE`).
*   **`before_count`**: A macro variable created by `PROC SQL` to store the count of records before duplicate removal. Used in a `%PUT` statement.
*   **`after_count`**: A macro variable created by `PROC SQL` to store the count of records after duplicate removal. Used in a `%PUT` statement.
*   **`dup_count`**: A macro variable calculated using `%EVAL` to store the number of duplicate records removed. Used in a `%PUT` statement.
*   **`p1_value`**: A macro variable created by `CALL SYMPUTX` to store the value of the 1st percentile. Used in the DATA step for winsorization.
*   **`p99_value`**: A macro variable created by `CALL SYMPUTX` to store the value of the 99th percentile. Used in the DATA step for winsorization.

### Report generation and formatting logic

*   **`%PUT` statements**: Used throughout the macros to log messages to the SAS log, indicating the completion of cleaning steps, the number of duplicates removed, and the outlier handling method applied.
*   **`FORMAT` statements**: Within the `CLEAN_TRANSACTIONS` macro, `FORMAT transaction_date_sas DATE9.` and `FORMAT transaction_datetime DATETIME20.` are used to display date and datetime variables in a human-readable format.
*   **`PROC MEANS` (final)**: Generates a summary report displaying the number of observations (N), mean, standard deviation (STD), minimum (MIN), and maximum (MAX) values for the `amount` variable.
*   **`TITLE` statement**: Adds a descriptive title "Transaction Amount Statistics After Cleaning" to the final `PROC MEANS` output.

### Business application of each PROC

*   **`PROC SORT`**: Crucial for ensuring data integrity by removing duplicate transactions (e.g., accidental re-entries, system glitches) which could lead to inflated revenue figures or inaccurate customer behavior analysis. It also prepares data for `BY` group processing in subsequent steps, which is essential for many business analyses.
*   **`PROC SQL`**: Provides quick data auditing to quantify the impact of cleaning steps. For businesses, knowing how many duplicates were removed helps validate the data quality process and understand the extent of data redundancy.
*   **`PROC MEANS` (for percentiles and outlier handling)**: Essential for robust financial analysis and fraud detection. Identifying extreme transaction amounts (outliers) helps in understanding the distribution of spending and in mitigating the impact of these extremes. Winsorization, for instance, ensures that unusually large or small transactions don't disproportionately skew financial reports or predictive models, leading to more stable and reliable business insights.
*   **`PROC MEANS` (final statistics)**: Provides a statistical overview of the cleaned transaction amounts. Businesses use this to confirm that the cleaning process has resulted in a reasonable and expected distribution of transaction values, which is vital for accurate financial reporting, risk assessment, and performance monitoring.

---

## Program: 03_feature_engineering.sas

### List of all PROC steps with descriptions

*   **`PROC SORT`**: This procedure sorts a SAS dataset by one or more variables. In the `CALCULATE_VELOCITY` macro, it sorts the data by `customer_id`, `transaction_date_sas`, and `transaction_time` to enable correct calculation of rolling window and sequential features.
*   **`PROC MEANS`**: This procedure calculates descriptive statistics for numeric variables. In the `CALCULATE_AMOUNT_DEVIATION` macro, it is used in `NOPRINT` mode to calculate customer-specific mean, standard deviation, and count of transaction amounts.
*   **`PROC SQL`**: This procedure executes SQL queries within SAS.
    *   In `CALCULATE_AMOUNT_DEVIATION`, it merges customer-level statistics back to the transaction data and calculates deviation features like `amount_zscore` and `amount_pct_deviation`.
    *   In `CREATE_LOCATION_FEATURES`, the first `PROC SQL` calculates the count of transactions per country. The second `PROC SQL` merges these country counts back to the transaction data and creates location-based flags (`is_rare_country`, `is_international`).
*   **`PROC PRINT`**: This procedure generates a listing of the contents of a SAS dataset. Here, it is used to display a sample of the engineered features from the final dataset.

### Statistical analysis methods used

*   **Descriptive Statistics**: `PROC MEANS` is used to calculate customer-level mean, standard deviation, and count of transaction amounts. These statistics form the basis for creating deviation features.
*   **Z-score Calculation**: The `amount_zscore` feature is calculated as `(amount - customer_avg_amount) / customer_std_amount`. A z-score is a statistical measure that describes a value's relationship to the mean of a group of values, measured in terms of standard deviations from the mean. This helps in identifying how unusual a specific transaction amount is for a given customer.
*   **Percentage Deviation**: The `amount_pct_deviation` feature calculates the percentage difference between a transaction amount and the customer's average amount. This is a simple statistical measure of relative deviation.

### Predictive modeling logic

This program is entirely dedicated to **feature engineering**, which is a critical preparatory stage for predictive modeling, particularly in fraud detection. The logic implemented here aims to create new variables (features) that capture patterns and anomalies indicative of fraudulent activity, thereby enhancing the predictive power of a subsequent fraud detection model.

*   **Velocity Features**: Features like `txn_count_7d`, `txn_amount_7d`, `avg_txn_amount_7d`, and `days_since_last_txn` are engineered to capture the frequency and volume of transactions over a recent rolling window (e.g., 7 days). Rapid increases in these metrics often signal suspicious activity, such as account takeover or "card testing."
*   **Amount Deviation Features**: `amount_zscore` and `amount_pct_deviation` quantify how much a current transaction deviates from a customer's typical spending behavior. Large positive or negative deviations can be strong indicators of unusual, potentially fraudulent, transactions.
*   **Time-based Features**: `txn_hour`, `txn_day_of_week`, `time_of_day`, `is_weekend`, and `is_unusual_hour` capture temporal aspects of transactions. Fraudulent activities often occur during unusual hours (e.g., late night) or days (e.g., weekends) when monitoring might be less stringent, or when the legitimate cardholder is less likely to be transacting.
*   **Location Features**: `is_rare_country` and `is_international` capture geographical risk. Transactions originating from unusual or high-risk countries, or international transactions in general, can have higher fraud probabilities.

These engineered features are designed to be direct inputs into a machine learning model (e.g., logistic regression, decision trees, neural networks) to predict the likelihood of fraud.

### Macro variable definitions and usage

*   **`input_lib`**: Defined as `WORK`. Used to specify the SAS library where input datasets are located.
*   **`output_lib`**: Defined as `WORK`. Used to specify the SAS library where output datasets will be stored.
*   **`inds`**: A macro parameter in all feature engineering macros. Used to pass the name of the input SAS dataset.
*   **`outds`**: A macro parameter in all feature engineering macros. Used to pass the name of the output SAS dataset.
*   **`window_days`**: A macro parameter in `CALCULATE_VELOCITY`. Used to specify the number of days for the rolling window calculation (e.g., 7 days). It is also embedded into variable names (e.g., `txn_count_&window_days.d`).

### Report generation and formatting logic

*   **`%PUT` statements**: Used extensively throughout the macros to log messages to the SAS log, indicating the completion of each feature engineering step (e.g., "Calculated velocity features," "Created time-based features").
*   **`PROC PRINT`**: Generates a sample tabular report of the first 10 observations, displaying a selected subset of the newly engineered features.
*   **`TITLE` statement**: Adds a descriptive title "Sample of Engineered Features" to the `PROC PRINT` output.

### Business application of each PROC

*   **`PROC SORT`**: Enables the calculation of sequential and rolling window features by ensuring data is ordered correctly by customer and transaction time. In fraud detection, this is vital for creating velocity features that track changes in spending patterns over time, helping to identify sudden, suspicious bursts of activity.
*   **`PROC MEANS`**: Calculates customer-specific aggregate statistics (mean, standard deviation). Businesses use these statistics to establish individual customer spending profiles. This forms the baseline for anomaly detection, allowing the identification of transactions that deviate significantly from a customer's normal behavior, which is a strong indicator of potential fraud.
*   **`PROC SQL`**: Efficiently merges aggregated statistics back to individual records and creates new features based on these statistics and other data attributes.
    *   For amount deviation, it's used to quantify how "unusual" a transaction amount is for a specific customer, providing crucial input for fraud scoring models.
    *   For location features, it's used to assess geographical risk associated with transactions. Identifying transactions from rare or high-risk countries helps businesses prioritize investigations and apply appropriate security measures.
*   **`PROC PRINT`**: Provides a quick visual inspection of the newly created features. For data scientists and business analysts, this is important for verifying that the features are calculated correctly, have reasonable values, and are suitable for input into a fraud detection model. It helps ensure the quality and interpretability of the features before model training.
# Database Connectivity and File I/O
# SAS Program Analysis

This document provides a detailed analysis of the provided SAS programs, focusing on external database connections, file I/O operations, PROC SQL queries, and LIBNAME/IMPORT/EXPORT/FILENAME statements.

## 01_transaction_data_import.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **File Imports**: This program imports transaction data from a CSV file.
*   **Internal I/O**: Reads data from a CSV file and writes to SAS datasets in the `WORK` library.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC PRINT` generates output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program uses `PROC SQL` to count records for validation purposes.

```sas
PROC SQL NOPRINT;
    SELECT COUNT(*) INTO :valid_count FROM &outds;
    SELECT COUNT(*) INTO :total_count FROM &inds;
QUIT;
```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

This program uses `PROC IMPORT` to bring data from a CSV file into a SAS dataset.

```sas
PROC IMPORT 
    DATAFILE="&filepath"
    OUT=&outds
    DBMS=CSV
    REPLACE;
    GETNAMES=YES;
RUN;
```

*   **`DATAFILE`**: The input file is specified by `&filepath`, which resolves to `/data/raw/transactions.csv`.
*   **`OUT`**: The output SAS dataset is `&outds`, which resolves to `WORK.raw_transactions`.
*   **`DBMS`**: The database management system specified is `CSV`, indicating a comma-separated values file.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program. The `DATAFILE` option in `PROC IMPORT` directly references the file path.

### Database Engine Usage

The `DBMS=CSV` option in `PROC IMPORT` indicates that a CSV file is being processed, not an external database engine like ODBC or OLEDB.

## 02_data_quality_cleaning.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **Internal I/O**: Reads from and writes to SAS datasets within the `WORK` library.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC MEANS` generates statistical output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program uses `PROC SQL` to count records before and after duplicate removal.

```sas
PROC SQL NOPRINT;
    SELECT COUNT(*) INTO :before_count FROM &inds;
    SELECT COUNT(*) INTO :after_count FROM &outds;
QUIT;
```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

No `PROC IMPORT` or `PROC EXPORT` statements are used in this program. All data manipulation occurs on existing SAS datasets.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program.

### Database Engine Usage

No external database engines (like ODBC, OLEDB, etc.) are used in this program. All operations are performed on SAS datasets.

## 03_feature_engineering.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **Internal I/O**: Reads from and writes to SAS datasets within the `WORK` library. Intermediate datasets (`customer_stats`, `country_counts`) are also created.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC PRINT` generates output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program extensively uses `PROC SQL` for calculating and merging features.

1.  **Calculate Amount Deviation and Merge Statistics:**
    ```sas
    PROC SQL;
        CREATE TABLE &outds AS
        SELECT 
            a.*,
            b.customer_avg_amount,
            b.customer_std_amount,
            b.customer_txn_count,
            /* Calculate z-score */
            CASE 
                WHEN b.customer_std_amount > 0 THEN
                    (a.amount - b.customer_avg_amount) / b.customer_std_amount
                ELSE 0
            END AS amount_zscore,
            /* Calculate percentage deviation */
            CASE
                WHEN b.customer_avg_amount > 0 THEN
                    ((a.amount - b.customer_avg_amount) / b.customer_avg_amount) * 100
                ELSE 0
            END AS amount_pct_deviation
        FROM &inds a
        LEFT JOIN customer_stats b
        ON a.customer_id = b.customer_id;
    QUIT;
    ```

2.  **Calculate Country Transaction Counts:**
    ```sas
    PROC SQL;
        CREATE TABLE country_counts AS
        SELECT 
            country_code_clean,
            COUNT(*) AS country_txn_count
        FROM &inds
        GROUP BY country_code_clean;
    QUIT;
    ```

3.  **Merge Country Features:**
    ```sas
    PROC SQL;
        CREATE TABLE &outds AS
        SELECT 
            a.*,
            b.country_txn_count,
            /* Flag for rare countries */
            CASE 
                WHEN b.country_txn_count < 10 THEN 1
                ELSE 0
            END AS is_rare_country,
            /* Check if international transaction */
            CASE
                WHEN a.country_code_clean NE 'US' THEN 1
                ELSE 0
            END AS is_international
        FROM &inds a
        LEFT JOIN country_counts b
        ON a.country_code_clean = b.country_code_clean;
    QUIT;
    ```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

No `PROC IMPORT` or `PROC EXPORT` statements are used in this program. All data manipulation occurs on existing SAS datasets.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program.

### Database Engine Usage

No external database engines (like ODBC, OLEDB, etc.) are used in this program. All operations are performed on SAS datasets.
# Step Execution Flow and Dependencies
This document analyzes the provided SAS programs, detailing their execution sequence, data dependencies, macro calls, and overall use cases.

### List of SAS Programs Analyzed

*   `01_transaction_data_import.sas`
*   `02_data_quality_cleaning.sas`
*   `03_feature_engineering.sas`

### Sequence of DATA and PROC Steps Execution

The SAS programs are designed to execute sequentially, with each program building upon the output of the previous one. The execution flow is summarized below:

#### 1. `01_transaction_data_import.sas`

This program is responsible for importing raw transaction data and performing initial validation.

*   **Macro Variable Definitions:**
    *   `input_path` is set to `/data/raw`.
    *   `output_lib` is set to `WORK`.
    *   `transaction_file` is set to `transactions.csv`.
*   **Macro Definition: `IMPORT_TRANSACTIONS`**
    *   Defines a macro to import a CSV file into a SAS dataset.
*   **Macro Definition: `VALIDATE_DATA`**
    *   Defines a macro to validate an input dataset, creating validation flags and filtering for valid records.
*   **Macro Execution: `%IMPORT_TRANSACTIONS`**
    *   **PROC IMPORT:** Reads the CSV file specified by `&input_path/&transaction_file` (`/data/raw/transactions.csv`).
        *   **Description:** Imports raw transaction data into `WORK.raw_transactions`.
    *   **Macro Logic:** Logs the import status and checks the `SYSERR` macro variable for errors, aborting if the import failed.
*   **Macro Execution: `%VALIDATE_DATA`**
    *   **DATA Step:** Reads `WORK.raw_transactions`.
        *   **Description:** Creates a `validation_status` variable, checking for missing `transaction_id`, `customer_id`, `amount`, `transaction_date`, and invalid `amount` (less than or equal to 0). It then filters the dataset, keeping only records where `validation_status` is 'VALID', and outputs them to `WORK.transactions_validated`.
    *   **PROC SQL:** Reads `WORK.raw_transactions` and `WORK.transactions_validated`.
        *   **Description:** Counts the total records from the raw dataset and the valid records from the validated dataset, storing these counts in macro variables for logging.
*   **PROC PRINT:** Reads `WORK.transactions_validated`.
    *   **Description:** Displays the first 10 observations of the `WORK.transactions_validated` dataset to show the initial results.

#### 2. `02_data_quality_cleaning.sas`

This program focuses on cleaning, standardizing, and refining the validated transaction data.

*   **Macro Variable Definitions:**
    *   `input_lib` is set to `WORK`.
    *   `output_lib` is set to `WORK`.
*   **Macro Definition: `CLEAN_TRANSACTIONS`**
    *   Defines a macro to standardize and clean various fields in a transaction dataset.
*   **Macro Definition: `REMOVE_DUPLICATES`**
    *   Defines a macro to sort a dataset and remove duplicate records based on a specified key.
*   **Macro Definition: `HANDLE_OUTLIERS`**
    *   Defines a macro to detect and handle outliers in a numeric variable, supporting winsorization or removal methods.
*   **Macro Execution: `%CLEAN_TRANSACTIONS`**
    *   **DATA Step:** Reads `WORK.transactions_validated` (output from `01_transaction_data_import.sas`).
        *   **Description:** Standardizes `transaction_type`, `merchant_name`, and `country_code` by cleaning spaces and converting case. It replaces missing `amount` values with 0, converts `transaction_date` to a SAS date format, and creates a `transaction_datetime` variable. The result is stored in `WORK.transactions_cleaned`.
*   **Macro Execution: `%REMOVE_DUPLICATES`**
    *   **PROC SORT:** Reads `WORK.transactions_cleaned`.
        *   **Description:** Sorts the `WORK.transactions_cleaned` dataset by `transaction_id` and removes records with duplicate `transaction_id` values. The unique records are output to `WORK.transactions_deduped`.
    *   **PROC SQL:** Reads `WORK.transactions_cleaned` and `WORK.transactions_deduped`.
        *   **Description:** Counts records before and after duplicate removal for logging the number of removed duplicates.
*   **Macro Execution: `%HANDLE_OUTLIERS`**
    *   **PROC MEANS:** Reads `WORK.transactions_deduped`.
        *   **Description:** Calculates the 1st and 99th percentiles (P1 and P99) for the `amount` variable and outputs these to a temporary dataset named `WORK.percentiles`.
    *   **DATA _NULL_ Step:** Reads `WORK.percentiles`.
        *   **Description:** Reads the calculated percentile values from `WORK.percentiles` and stores them in macro variables `p1_value` and `p99_value`.
    *   **DATA Step:** Reads `WORK.transactions_deduped`.
        *   **Description:** Applies winsorization to the `amount` variable, capping values below `p1_value` at `p1_value` and values above `p99_value` at `p99_value`. The processed data is stored in `WORK.transactions_final`.
*   **PROC MEANS:** Reads `WORK.transactions_final`.
    *   **Description:** Calculates and displays descriptive statistics (N, Mean, Std Dev, Min, Max) for the `amount` variable in the `WORK.transactions_final` dataset, providing an overview after outlier handling.

#### 3. `03_feature_engineering.sas`

This program focuses on generating various features from the cleaned transaction data for potential use in analytical models.

*   **Macro Variable Definitions:**
    *   `input_lib` is set to `WORK`.
    *   `output_lib` is set to `WORK`.
*   **Macro Definition: `CALCULATE_VELOCITY`**
    *   Defines a macro to calculate rolling window velocity features (e.g., transaction count and amount within a time window) and days since the last transaction.
*   **Macro Definition: `CALCULATE_AMOUNT_DEVIATION`**
    *   Defines a macro to calculate amount deviation features (e.g., Z-score, percentage deviation) relative to a customer's average transaction behavior.
*   **Macro Definition: `CREATE_TIME_FEATURES`**
    *   Defines a macro to extract and create time-based features from transaction dates and times.
*   **Macro Definition: `CREATE_LOCATION_FEATURES`**
    *   Defines a macro to create location-based features, such as transaction counts by country and flags for rare or international transactions.
*   **Macro Execution: `%CALCULATE_VELOCITY`**
    *   **PROC SORT:** Reads `WORK.transactions_final` (output from `02_data_quality_cleaning.sas`).
        *   **Description:** Sorts the dataset by `customer_id`, `transaction_date_sas`, and `transaction_time` to prepare for cumulative calculations within the `DATA` step. The sorted data is implicitly used by the subsequent `DATA` step.
    *   **DATA Step:** Reads the sorted `WORK.transactions_final`.
        *   **Description:** Calculates `days_since_last_txn`, `txn_count_7d` (rolling 7-day transaction count), `txn_amount_7d` (rolling 7-day transaction amount), and `avg_txn_amount_7d` per customer. The resulting dataset is `WORK.txn_with_velocity`.
*   **Macro Execution: `%CALCULATE_AMOUNT_DEVIATION`**
    *   **PROC MEANS:** Reads `WORK.txn_with_velocity`.
        *   **Description:** Calculates the mean, standard deviation, and count of `amount` for each `customer_id`, outputting these statistics to `WORK.customer_stats`.
    *   **PROC SQL:** Reads `WORK.txn_with_velocity` and `WORK.customer_stats`.
        *   **Description:** Joins the transaction data with the customer statistics and calculates `amount_zscore` and `amount_pct_deviation` for each transaction relative to the customer's historical average. The output is `WORK.txn_with_deviation`.
*   **Macro Execution: `%CREATE_TIME_FEATURES`**
    *   **DATA Step:** Reads `WORK.txn_with_deviation`.
        *   **Description:** Extracts `txn_hour`, `txn_day_of_week`, `txn_day_of_month`, `txn_month` from the transaction date/time. It also creates categorical `time_of_day` (NIGHT, MORNING, AFTERNOON, EVENING) and binary flags `is_weekend` and `is_unusual_hour`. The output is `WORK.txn_with_time_features`.
*   **Macro Execution: `%CREATE_LOCATION_FEATURES`**
    *   **PROC SQL:** Reads `WORK.txn_with_time_features`.
        *   **Description:** Calculates the total `country_txn_count` for each `country_code_clean` and stores it in `WORK.country_counts`.
    *   **PROC SQL:** Reads `WORK.txn_with_time_features` and `WORK.country_counts`.
        *   **Description:** Joins the transaction data with country counts and creates `is_rare_country` (flagging countries with less than 10 transactions) and `is_international` (flagging transactions not from 'US'). The final engineered dataset is `WORK.transactions_engineered`.
*   **PROC PRINT:** Reads `WORK.transactions_engineered`.
    *   **Description:** Displays a sample of 10 observations with selected engineered features to demonstrate the results.

### Dataset Dependencies

The programs exhibit a clear chain of dependencies, where the output of one step or program serves as the input for the next. All intermediate and final datasets are stored in the `WORK` library.

*   **`01_transaction_data_import.sas`:**
    *   `%IMPORT_TRANSACTIONS` creates `WORK.raw_transactions` from an external CSV file.
    *   `%VALIDATE_DATA` depends on `WORK.raw_transactions` and creates `WORK.transactions_validated`.
    *   The final `PROC PRINT` depends on `WORK.transactions_validated`.
*   **`02_data_quality_cleaning.sas`:**
    *   `%CLEAN_TRANSACTIONS` depends on `WORK.transactions_validated` (from `01_transaction_data_import.sas`) and creates `WORK.transactions_cleaned`.
    *   `%REMOVE_DUPLICATES` depends on `WORK.transactions_cleaned` and creates `WORK.transactions_deduped`.
    *   `%HANDLE_OUTLIERS` depends on `WORK.transactions_deduped` and creates `WORK.transactions_final`. It also temporarily creates `WORK.percentiles`.
    *   The final `PROC MEANS` depends on `WORK.transactions_final`.
*   **`03_feature_engineering.sas`:**
    *   `%CALCULATE_VELOCITY` depends on `WORK.transactions_final` (from `02_data_quality_cleaning.sas`) and creates `WORK.txn_with_velocity`.
    *   `%CALCULATE_AMOUNT_DEVIATION` depends on `WORK.txn_with_velocity` and creates `WORK.txn_with_deviation`. It also temporarily creates `WORK.customer_stats`.
    *   `%CREATE_TIME_FEATURES` depends on `WORK.txn_with_deviation` and creates `WORK.txn_with_time_features`.
    *   `%CREATE_LOCATION_FEATURES` depends on `WORK.txn_with_time_features` and creates `WORK.transactions_engineered`. It also temporarily creates `WORK.country_counts`.
    *   The final `PROC PRINT` depends on `WORK.transactions_engineered`.

### Macro Execution Order

The macros are defined at the beginning of each program and then called in a specific sequence to orchestrate the data processing pipeline.

#### `01_transaction_data_import.sas`

1.  `%IMPORT_TRANSACTIONS`
2.  `%VALIDATE_DATA`

#### `02_data_quality_cleaning.sas`

1.  `%CLEAN_TRANSACTIONS`
2.  `%REMOVE_DUPLICATES`
3.  `%HANDLE_OUTLIERS`

#### `03_feature_engineering.sas`

1.  `%CALCULATE_VELOCITY`
2.  `%CALCULATE_AMOUNT_DEVIATION`
3.  `%CREATE_TIME_FEATURES`
4.  `%CREATE_LOCATION_FEATURES`

### RUN/QUIT Statement Trigger Points

*   **`RUN;`** statements terminate DATA steps and most PROC steps, causing them to execute.
*   **`QUIT;`** statements terminate interactive PROCs like `PROC SQL` or `PROC IML`. If not explicitly used, SAS often implicitly quits an interactive PROC when another DATA or PROC step begins.

#### `01_transaction_data_import.sas`

*   `PROC IMPORT` is terminated by `RUN;`.
*   The `DATA` step in `%VALIDATE_DATA` is terminated by `RUN;`.
*   `PROC SQL` in `%VALIDATE_DATA` is terminated by `QUIT;`.
*   `PROC PRINT` is terminated by `RUN;`.

#### `02_data_quality_cleaning.sas`

*   The `DATA` step in `%CLEAN_TRANSACTIONS` is terminated by `RUN;`.
*   `PROC SORT` in `%REMOVE_DUPLICATES` is terminated by `RUN;`.
*   `PROC SQL` in `%REMOVE_DUPLICATES` is terminated by `QUIT;`.
*   `PROC MEANS` in `%HANDLE_OUTLIERS` is terminated by `RUN;`.
*   `DATA _NULL_` in `%HANDLE_OUTLIERS` is terminated by `RUN;`.
*   The `DATA` step in `%HANDLE_OUTLIERS` is terminated by `RUN;`.
*   `PROC MEANS` (final) is terminated by `RUN;`.

#### `03_feature_engineering.sas`

*   `PROC SORT` in `%CALCULATE_VELOCITY` is terminated by `RUN;`.
*   The `DATA` step in `%CALCULATE_VELOCITY` is terminated by `RUN;`.
*   `PROC MEANS` in `%CALCULATE_AMOUNT_DEVIATION` is terminated by `RUN;`.
*   `PROC SQL` in `%CALCULATE_AMOUNT_DEVIATION` is terminated by `QUIT;`.
*   The `DATA` step in `%CREATE_TIME_FEATURES` is terminated by `RUN;`.
*   The first `PROC SQL` in `%CREATE_LOCATION_FEATURES` is terminated by `QUIT;`.
*   The second `PROC SQL` in `%CREATE_LOCATION_FEATURES` is terminated by `QUIT;`.
*   `PROC PRINT` (final) is terminated by `RUN;`.

### List of Use Cases Addressed by All Programs Together

These SAS programs collectively address a comprehensive data preparation and feature engineering pipeline, commonly found in analytical projects, especially in domains like fraud detection or customer behavior analysis.

1.  **Data Ingestion and Initial Validation:** Importing raw data from external sources and performing fundamental checks for data integrity and completeness.
2.  **Data Quality and Cleaning:** Standardizing data formats, handling missing values, and correcting inconsistencies across various fields.
3.  **Duplicate Management:** Identifying and removing redundant records to ensure data uniqueness and accuracy.
4.  **Outlier Detection and Treatment:** Identifying and mitigating the impact of extreme values in critical numerical variables, improving the robustness of subsequent analyses.
5.  **Feature Engineering for Machine Learning:** Creating new, informative variables from existing data that capture complex patterns and relationships, enhancing the predictive power of analytical models. This includes:
    *   **Velocity Features:** Aggregating transactional activity over time windows (e.g., transaction count, total amount in the last 7 days) to capture changes in behavior.
    *   **Deviation Features:** Calculating how individual transactions deviate from a customer's typical behavior (e.g., Z-score, percentage deviation from average amount).
    *   **Time-Based Features:** Extracting temporal characteristics like hour of day, day of week, month, and creating flags for unusual transaction times (e.g., night transactions, weekends).
    *   **Location-Based Features:** Deriving insights from geographical data, such as transaction counts by country and flags for rare or international transactions.
6.  **Data Transformation for Analytics:** Preparing data in a structured and enriched format suitable for statistical modeling, reporting, and business intelligence applications.
# Error Handling and Logging
This analysis provides a detailed breakdown of error handling and logging mechanisms employed in each of the provided SAS programs.

### Program 01: `01_transaction_data_import.sas`

#### Error Checking Mechanisms
*   **SYSERR**: The program checks the `SYSERR` automatic macro variable immediately after the `PROC IMPORT` step. This is used to detect if the import procedure encountered any system-level errors or warnings that elevated `SYSERR` above zero.

#### PUT Statements for Logging
*   `%PUT NOTE: Imported &filepath to &outds;`: Logs a success message indicating which file was imported to which dataset.
*   `%PUT ERROR: Import failed with SYSERR=&SYSERR;`: Logs a critical error message, including the `SYSERR` value, if the `PROC IMPORT` step fails.
*   `%PUT NOTE: Validated &valid_count of &total_count records;`: Logs a summary of the data validation process, showing the count of valid records out of the total.

#### ABORT and STOP Conditions
*   **ABORT**: The `%ABORT` statement is used conditionally. If `SYSERR` is greater than 0 after `PROC IMPORT`, the macro execution is aborted, halting further processing of the SAS session. This prevents subsequent steps from running on potentially incomplete or corrupt data.

#### Error Handling in DATA Steps
*   **Data Validation Flags**: Within the `VALIDATE_DATA` macro, a `validation_status` variable is created. This variable explicitly flags records based on various data quality checks:
    *   `MISSING_ID`: `transaction_id` is missing.
    *   `MISSING_CUSTOMER`: `customer_id` is missing.
    *   `MISSING_AMOUNT`: `amount` is missing.
    *   `MISSING_DATE`: `transaction_date` is missing.
    *   `INVALID_AMOUNT`: `amount` is less than or equal to 0.
    *   `VALID`: All checks pass.
*   **Implicit Filtering**: The `if validation_status = 'VALID';` statement acts as an implicit error handling mechanism. Records that do not meet the 'VALID' criteria are filtered out and not written to the output dataset, effectively removing problematic entries from the clean data stream.

#### Exception Handling in PROC SQL
*   No explicit `SQLRC` or `SQLXRC` checks are performed after the `PROC SQL` steps used for counting records. The `NOPRINT` option is used to suppress output, but error codes are not explicitly handled.

#### Error Output Datasets or Files
*   No dedicated error output datasets or files are created. Records failing validation are simply excluded from the output dataset (`&outds` in `VALIDATE_DATA`).

### Program 02: `02_data_quality_cleaning.sas`

#### Error Checking Mechanisms
*   No explicit error checking mechanisms like `_ERROR_`, `FILERC`, `SQLRC`, or `SYSERR` are used within this program. The code assumes successful execution of all `DATA` and `PROC` steps.

#### PUT Statements for Logging
*   `%PUT NOTE: Cleaned &inds to &outds;`: Logs a message upon successful completion of the data cleaning macro.
*   `%PUT NOTE: Removed &dup_count duplicate records;`: Logs the number of duplicate records identified and removed by the `REMOVE_DUPLICATES` macro.
*   `%PUT NOTE: Handled outliers in &var using &method method;`: Logs the action taken for outlier handling, specifying the variable and method used.

#### ABORT and STOP Conditions
*   No `ABORT` or `STOP` statements are present in this program.

#### Error Handling in DATA Steps
*   **Missing Value Imputation**: In the `CLEAN_TRANSACTIONS` macro, `if missing(amount) then amount = 0;` handles missing `amount` values by replacing them with 0. This prevents potential issues in downstream calculations or analyses that do not tolerate missing numerical values.
*   **Date Conversion Safety**: `if NOT missing(transaction_date) then do; ... end;` ensures that the `INPUT` function for `transaction_date_sas` is only attempted if `transaction_date` is not missing, preventing potential data conversion errors for null values.
*   **Outlier Treatment**: The `HANDLE_OUTLIERS` macro includes logic to either:
    *   **Winsorize**: Cap values at the 1st and 99th percentiles (`if &var < &p1_value then &var = &p1_value; else if &var > &p99_value then &var = &p99_value;`). This mitigates the impact of extreme values without removing them.
    *   **Remove**: Filter out records where the variable's value falls outside the 1st and 99th percentiles (`if &var >= &p1_value AND &var <= &p99_value;`). This removes extreme outliers from the dataset.

#### Exception Handling in PROC SQL
*   No explicit `SQLRC` or `SQLXRC` checks are performed after the `PROC SQL` steps.

#### Error Output Datasets or Files
*   No dedicated error output datasets or files are created. Problematic data (e.g., duplicates, outliers) are either removed or transformed within the main data flow.

### Program 03: `03_feature_engineering.sas`

#### Error Checking Mechanisms
*   No explicit error checking mechanisms like `_ERROR_`, `FILERC`, `SQLRC`, or `SYSERR` are used within this program. The code assumes successful execution of all `DATA` and `PROC` steps.

#### PUT Statements for Logging
*   `%PUT NOTE: Calculated velocity features for &window_days day window;`: Logs the creation of velocity features.
*   `%PUT NOTE: Calculated amount deviation features;`: Logs the creation of amount deviation features.
*   `%PUT NOTE: Created time-based features;`: Logs the creation of time-based features.
*   `%PUT NOTE: Created location-based features;`: Logs the creation of location-based features.

#### ABORT and STOP Conditions
*   No `ABORT` or `STOP` statements are present in this program.

#### Error Handling in DATA Steps
*   **Customer-Specific Calculations**: In the `CALCULATE_VELOCITY` macro, `if FIRST.customer_id then do; ... end;` ensures that cumulative variables (`txn_count`, `txn_amount`, `last_txn_date`) are reset for each new customer. This is crucial for accurate rolling window calculations and prevents data from one customer from incorrectly influencing another.
*   **Handling Initial Missing Values**: `if NOT missing(last_txn_date) then ... else days_since_last_txn = .;` gracefully handles the calculation of `days_since_last_txn` for the very first transaction of a customer, where `last_txn_date` would be missing.
*   **Division by Zero Prevention**: `if txn_count_&window_days.d > 0 then ... else avg_txn_amount_&window_days.d = 0;` prevents a division-by-zero error when calculating `avg_txn_amount` if `txn_count` is zero. It assigns a default value of 0 in such cases.
*   **Comprehensive Categorization**: In `CREATE_TIME_FEATURES`, the `if txn_hour >= 0 AND txn_hour < 6 then ... else time_of_day = 'EVENING';` block ensures that all possible `txn_hour` values (0-23) are assigned a `time_of_day` category, preventing unassigned categories or errors for edge cases.

#### Exception Handling in PROC SQL
*   **Division by Zero Prevention**: Within the `CALCULATE_AMOUNT_DEVIATION` macro's `PROC SQL` step, `CASE` statements are used to prevent division by zero:
    *   `CASE WHEN b.customer_std_amount > 0 THEN ... ELSE 0 END AS amount_zscore`: If the standard deviation (`customer_std_amount`) is zero (meaning all amounts for that customer are identical), the `amount_zscore` is set to 0.
    *   `CASE WHEN b.customer_avg_amount > 0 THEN ... ELSE 0 END AS amount_pct_deviation`: If the average amount (`customer_avg_amount`) is zero, the `amount_pct_deviation` is set to 0.
*   No explicit `SQLRC` or `SQLXRC` checks are performed for other `PROC SQL` operations.

#### Error Output Datasets or Files
*   No dedicated error output datasets or files are created. All feature engineering steps transform or augment the data within the main dataset flow.