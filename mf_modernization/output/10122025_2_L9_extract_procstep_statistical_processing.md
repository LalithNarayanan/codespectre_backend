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