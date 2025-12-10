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