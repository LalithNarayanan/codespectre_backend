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