
# Program Overview
### Overview of the Program

This PySpark program implements a fraud detection pipeline. It ingests transaction data, performs data validation, cleaning, and feature engineering. It then applies rule-based and machine learning (ML)-based fraud detection techniques. Finally, it combines the results, generates a final report, and saves high-risk transactions. The pipeline is designed to mirror a SAS-based fraud detection system, with each function corresponding to a SAS macro.

### Business Functions Addressed

*   **Data Ingestion and Validation:** Reads transaction data from a CSV file, defines a schema, and validates data integrity (missing values, invalid amounts).
*   **Data Cleaning and Standardization:** Cleans and standardizes transaction data, including transaction type, merchant name, and country code. It also handles missing amounts and converts date/time formats.
*   **Duplicate Removal:** Removes duplicate transaction records based on specified key columns.
*   **Outlier Handling:** Addresses outliers in the transaction amount using Winsorization or removal.
*   **Feature Engineering:** Creates various features, including:
    *   Velocity features (transaction counts and amounts within a rolling window).
    *   Amount deviation features (average amount, standard deviation, Z-score).
    *   Time-based features (hour, day of week, day of month, month, time of day, weekend flag).
    *   Location-based features (transaction counts by country, rare country flag, international transaction flag).
*   **Rule-Based Fraud Detection:** Applies a set of predefined rules to identify suspicious transactions based on the engineered features.  Calculates a rule score and risk level.
*   **ML-Based Fraud Scoring:** Prepares data for ML scoring (normalization, interaction features), and simulates a logistic regression model to generate an ML-based fraud score and risk level.
*   **Score Combination and Final Assessment:** Combines rule-based and ML scores to derive a final fraud score, risk level, and recommendation.
*   **Reporting and Alerting:** Generates a final report summarizing the fraud detection results, including alert counts, risk level distributions, and saves high-risk transactions for further investigation.

### DataFrames/Tables Created and Consumed

*   **`transactions_df`:**
    *   **Created by:** `import_transactions` (reads from CSV)
    *   **Consumed by:** `validate_transactions`, `clean_transactions`, `remove_duplicates`, `handle_outliers`, `calculate_velocity_features`, `calculate_amount_deviation`, `create_time_features`, `create_location_features`, `apply_fraud_rules`, `prepare_ml_data`, `calculate_ml_score`, `combine_scores`, `generate_final_report`
    *   **Data Flow:**  The primary DataFrame, it undergoes a series of transformations throughout the pipeline. Data is read from the input CSV, validated, cleaned, and enriched with features and fraud scores.  It is cached after feature engineering to optimize performance.
*   **`validated_df`:**
    *   **Created by:** `validate_transactions`
    *   **Consumed by:** `clean_transactions`
    *   **Data Flow:** Derived from `transactions_df` after validation, containing only valid transactions.
*   **`customer_stats_df`:**
    *   **Created by:** `calculate_amount_deviation`
    *   **Consumed by:** `calculate_amount_deviation` (via join with `transactions_df`)
    *   **Data Flow:** Aggregates customer-level statistics (average amount, standard deviation, transaction count) used in amount deviation calculations.
*   **`country_counts_df`:**
    *   **Created by:** `create_location_features`
    *   **Consumed by:** `create_location_features` (via join with `transactions_df`)
    *   **Data Flow:** Aggregates transaction counts by country, used to create location-based features.
*   **`rule_alerts_df`:**
    *   **Created by:** `generate_rule_alerts`
    *   **Consumed by:** `rule_summary_report`
    *   **Data Flow:** Filters `transactions_df` to include only transactions that triggered alerts based on rule scores.
*   **`rule_summary_df`:**
    *   **Created by:** `rule_summary_report`
    *   **Consumed by:** (No direct consumption within the pipeline, but used for reporting)
    *   **Data Flow:** Summarizes the counts of each fraud rule triggered.
*   **Output:**
    *   High-risk transactions are written to a CSV file in the `REPORT_PATH`.
    *   Processed transactions are saved to a Parquet file in the `OUTPUT_PATH`.

# DataFrame and Table Analysis
### Program Analysis

This PySpark program implements a fraud detection pipeline. It reads transaction data, performs data cleaning, feature engineering, rule-based detection, ML scoring, and generates a final report.

#### DataFrames/Tables

*   **transactions\_df:** This DataFrame is the central data structure, representing the transaction data at various stages of processing. It is created and transformed throughout the pipeline.
*   **customer\_stats\_df:**  A temporary DataFrame created within `calculate_amount_deviation` to store aggregated customer statistics (average amount, standard deviation, and transaction count).
*   **country\_counts\_df:** A temporary DataFrame created within `create_location_features` to store the count of transactions per country.
*   **alerts\_df:** A temporary DataFrame containing transactions that trigger fraud alerts based on rule scores.
*   **risk\_level\_counts:** A temporary DataFrame containing the count of alerts by risk level, used in reporting.
*   **recommendation\_summary:** A temporary DataFrame containing the count of alerts by recommendation, used in reporting.
*   **rule\_summary\_df:** A temporary DataFrame containing the summary of rule triggers.

#### Input Sources

*   **spark.read.csv:**
    *   `INPUT_PATH/TRANSACTION_FILE` (e.g., `/data/raw/transactions.csv`): Reads transaction data from a CSV file.  The `TRANSACTION_SCHEMA` is applied to ensure the correct data types and avoid schema inference issues.

#### Output DataFrames/Tables

*   **Temporary Views:** None of the DataFrames are explicitly registered as temporary views using `createOrReplaceTempView`.
*   **Permanent Catalog Tables:** None of the DataFrames are explicitly saved as permanent catalog tables using `saveAsTable`.
*   **CSV output:** The `high_risk_transactions` DataFrame is written as a CSV file to the location specified by `REPORT_PATH`.
*   **Parquet Output:** The final `transactions_df` is written as a Parquet file to the location specified by `OUTPUT_PATH`.

#### Key Column Usage and Transformations

*   **transaction\_id, customer\_id, amount, transaction\_date, transaction\_time, transaction\_type, merchant\_name, country\_code:** These are the key input columns from the CSV.
*   **Data Validation:**
    *   `validation_status`:  Added using `withColumn` and conditional logic (`F.when().otherwise()`) to flag invalid records based on null values and amount.
    *   `.filter()`:  Used to remove invalid records based on the `validation_status`.
*   **Data Cleaning:**
    *   `transaction_type_clean`: Created using `F.upper()` and `F.trim()`.
    *   `merchant_name_clean`: Created using `F.initcap()` and `F.trim()`.
    *   `country_code_clean`: Created using `F.upper()` and `F.substring()`.
    *   `amount`: Cleaned using `F.coalesce()` to replace null amounts with 0.
    *   `transaction_date_sas`: Converted using `F.to_date()`.
    *   `transaction_datetime`: Created using `F.to_timestamp()` by concatenating date and time strings.
    *   `.dropDuplicates()`: Used to remove duplicate records based on specified key columns.
    *   `handle_outliers`:  Applies Winsorization or removal of outliers using `approxQuantile` and `F.when().otherwise()` or `.filter()`.
*   **Feature Engineering:**
    *   `days_since_last_txn`: Calculated using `F.lag()` and `F.datediff()`.
    *   `txn_count_7d`, `txn_amount_7d`, `avg_txn_amount_7d`: Calculated using window functions (`Window.partitionBy().orderBy().rangeBetween()`) for rolling window calculations.
    *   `customer_avg_amount`, `customer_std_amount`, `customer_txn_count`: Calculated by `groupBy().agg()`
    *   `amount_zscore`, `amount_pct_deviation`: Calculated using conditional logic (`F.when().otherwise()`) and the customer statistics.
    *   `txn_hour`, `txn_day_of_week`, `txn_day_of_month`, `txn_month`: Extracted using `F.hour()`, `F.dayofweek()`, `F.dayofmonth()`, and `F.month()`.
    *   `time_of_day`: Created using conditional logic (`F.when().otherwise()`).
    *   `is_weekend`:  Created using `F.isin()` and `cast(T.IntegerType())`.
    *   `is_unusual_hour`:  Created using a boolean expression and `cast(T.IntegerType())`.
    *   `country_txn_count`:  Calculated by `groupBy().agg()`.
    *   `is_rare_country`, `is_international`: Created using conditional logic (`F.when().otherwise()`) and boolean expressions with `cast(T.IntegerType())`.
*   **Rule-Based Detection:**
    *   Individual rule flags (e.g., `rule_high_velocity`, `rule_amount_deviation`) are created using boolean expressions and `cast(T.IntegerType())`.
    *   `rule_score`: Calculated by summing the rule flags.
    *   `rule_triggered`: Concatenated triggered rule names using `F.array_remove()`, `F.array()` and `F.concat_ws()`.
    *   `rule_risk_level`: Assigned based on `rule_score` using conditional logic (`F.when().otherwise()`).
    *   `is_suspicious`: Flagged using a boolean expression and `cast(T.IntegerType())`.
*   **ML Scoring:**
    *   `is_high_amount`, `is_very_high_amount`: Created using boolean expressions and `cast(T.IntegerType())`.
    *   `amount_normalized`, `txn_count_normalized`: Normalized using division.
    *   `amount_zscore`, `days_since_last_txn`: Filled null values with `F.coalesce()`.
    *   `amount_x_velocity`, `amount_x_deviation`: Interaction features calculated.
    *   `logit_score`: Calculated using arithmetic operations and coefficients.
    *   `ml_score_probability`: Calculated using the sigmoid function (`F.exp()`).
    *   `ml_score`: Scaled from `ml_score_probability`.
    *   `ml_risk_level`: Assigned based on `ml_score` using conditional logic (`F.when().otherwise()`).
*   **Score Combination and Reporting:**
    *   `final_fraud_score`: Calculated using a weighted average.
    *   `final_risk_level`: Assigned based on `final_fraud_score` using conditional logic (`F.when().otherwise()`).
    *   `final_recommendation`: Assigned based on `final_fraud_score` using conditional logic (`F.when().otherwise()`).

#### Schema Definitions and Column Data Types

*   The `TRANSACTION_SCHEMA` defines the schema for the input CSV file, explicitly specifying the data types for each column:
    *   `transaction_id`: `StringType`
    *   `customer_id`: `StringType`
    *   `amount`: `DoubleType`
    *   `transaction_date`: `StringType`
    *   `transaction_time`: `StringType`
    *   `transaction_type`: `StringType`
    *   `merchant_name`: `StringType`
    *   `country_code`: `StringType`
*   Throughout the pipeline, the program uses `withColumn` to add new columns and transform existing ones, often changing data types or creating new columns based on calculations. For example, boolean expressions are cast to `IntegerType` for rule flags.

#### Table/View Registration

*   No tables or views are registered using `createOrReplaceTempView` or saved using `saveAsTable`. The program operates on DataFrames.

# Transformation and Business Logic
### Program 01: 01_transaction_data_import.sas

#### List of transformations in the order of execution and description:

1.  **`spark.read.option("header", "true").schema(schema).csv(filepath)`**:
    *   **Description:** Reads a CSV file from the specified `filepath`. The `option("header", "true")` specifies that the first row of the CSV contains the column headers. The `schema(schema)` applies the predefined `TRANSACTION_SCHEMA` to the DataFrame during the read operation, ensuring data types are correctly interpreted and preventing schema inference issues.

2.  **`withColumn("validation_status", ...)`**:
    *   **Description:** Adds a new column named `"validation_status"` to the DataFrame, which indicates the validation status of each transaction.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to assign validation statuses based on the following conditions:
        *   `MISSING_ID`: If `transaction_id` is null.
        *   `MISSING_CUSTOMER`: If `customer_id` is null.
        *   `MISSING_AMOUNT`: If `amount` is null.
        *   `MISSING_DATE`: If `transaction_date` is null.
        *   `INVALID_AMOUNT`: If `amount` is less than or equal to 0.
        *   `VALID`: Otherwise (if none of the above conditions are met).

3.  **`filter(F.col("validation_status") == "VALID")`**:
    *   **Description:** Filters the DataFrame to keep only the rows where the `"validation_status"` column is equal to "VALID".  This effectively removes invalid transactions based on the validation checks.

#### Business Rules implemented in transformations:

*   **Data Validation:** Checks for missing values in `transaction_id`, `customer_id`, `amount`, and `transaction_date`. It also checks for invalid amounts (<= 0). Invalid records are filtered out.

#### Conditional logic (when, otherwise, filter, where):

*   `F.when().otherwise()` is used to create the `"validation_status"` column based on multiple conditions (missing or invalid data).
*   `.filter()` is used to remove invalid transactions, retaining only those with a `"validation_status"` of "VALID".

#### Aggregations and groupBy operations:

*   None

#### Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):

*   None

#### Key calculations and column transformations (withColumn, expr):

*   `withColumn` is used to add the `"validation_status"` column.

#### Data validation and quality checks (filter, isNull, isNotNull):

*   `isNull()` is used within the `F.when()` conditions to check for missing values in several columns.
*   `.filter()` is used to remove invalid transactions based on the validation checks.

---

### Program 02: 02_data_quality_cleaning.sas

#### List of transformations in the order of execution and description:

1.  **`withColumn("transaction_type_clean", F.upper(F.trim(F.col("transaction_type"))))`**:
    *   **Description:** Creates a new column `"transaction_type_clean"` by cleaning the `"transaction_type"` column. It converts the values to uppercase using `F.upper()` and removes leading/trailing spaces using `F.trim()`.

2.  **`withColumn("merchant_name_clean", F.initcap(F.trim(F.col("merchant_name"))))`**:
    *   **Description:** Creates a new column `"merchant_name_clean"` by cleaning the `"merchant_name"` column. It capitalizes the first letter of each word using `F.initcap()` and removes leading/trailing spaces using `F.trim()`.

3.  **`withColumn("country_code_clean", F.upper(F.substring(F.col("country_code"), 1, 2)))`**:
    *   **Description:** Creates a new column `"country_code_clean"` by cleaning the `"country_code"` column. It converts the values to uppercase using `F.upper()` and extracts the first two characters using `F.substring()`.

4.  **`withColumn("amount", F.coalesce(F.col("amount"), F.lit(0)))`**:
    *   **Description:** Handles missing values in the `"amount"` column. If an amount is null, it replaces it with 0 using `F.coalesce()`.

5.  **`withColumn("transaction_date_sas", F.to_date(F.col("transaction_date"), "yyyy-MM-dd"))`**:
    *   **Description:** Converts the `"transaction_date"` column (which is read as a string) to a date format using `F.to_date()`. The format string "yyyy-MM-dd" specifies the expected date format.

6.  **`withColumn("transaction_datetime", F.to_timestamp(F.concat_ws(" ", F.col("transaction_date"), F.col("transaction_time")), "yyyy-MM-dd HH:mm:ss"))`**:
    *   **Description:** Creates a new column `"transaction_datetime"` by combining the `"transaction_date"` and `"transaction_time"` columns into a timestamp format using `F.to_timestamp()`. `F.concat_ws(" ", ...)` concatenates the date and time strings with a space in between. The format string "yyyy-MM-dd HH:mm:ss" specifies the expected timestamp format.

7.  **`dropDuplicates(key_cols)`**:
    *   **Description:** Removes duplicate rows based on the columns specified in `key_cols`.  In this case, the key columns are: `"transaction_id"`, `"customer_id"`, and `"transaction_datetime"`.

8.  **`approxQuantile(var_col, [0.01, 0.99], 0.01)`**:
    *   **Description:** Calculates approximate quantiles (percentiles) for the specified `var_col` (e.g., "amount"). It calculates the 1st and 99th percentiles, used for outlier detection.  The `0.01` parameter specifies the relative error.

9.  **`withColumn(var_col, F.when(...).when(...).otherwise(...))`**:
    *   **Description:** Applies Winsorization to the `var_col`. Values less than the 1st percentile are set to the 1st percentile, and values greater than the 99th percentile are set to the 99th percentile.
    *   **Conditional Logic:** `F.when()` and `F.otherwise()` are used to apply the Winsorization logic.

10. **`filter((F.col(var_col) >= p1_value) & (F.col(var_col) <= p99_value))`**:
    *   **Description:** Filters the DataFrame to remove outliers from `var_col` by keeping only the rows where the value of `var_col` is within the range defined by the 1st and 99th percentiles.
    *   **Conditional Logic:** Uses `&` (bitwise AND) to filter the data.

#### Business Rules implemented in transformations:

*   **Data Standardization:** Standardizes `transaction_type`, `merchant_name`, and `country_code` by cleaning and formatting the data.
*   **Missing Value Handling:** Replaces missing amounts with 0.
*   **Data Type Conversion:** Converts `transaction_date` to a date format and combines date and time into a timestamp.
*   **Duplicate Removal:** Removes duplicate transactions based on key columns.
*   **Outlier Handling:**  Winsorizes or removes outliers from the `amount` column based on the 1st and 99th percentiles.

#### Conditional logic (when, otherwise, filter, where):

*   `F.when().otherwise()` is used for Winsorization.
*   `.filter()` is used to remove outliers.

#### Aggregations and groupBy operations:

*   `approxQuantile()` is used to calculate percentiles.

#### Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):

*   None

#### Key calculations and column transformations (withColumn, expr):

*   `withColumn` is used extensively for cleaning, standardizing, converting data types, and handling missing values.
*   `F.upper()`, `F.trim()`, `F.initcap()`, `F.substring()`, `F.coalesce()`, `F.to_date()`, `F.to_timestamp()`, and `F.concat_ws()` are used within `withColumn` to perform various transformations.

#### Data validation and quality checks (filter, isNull, isNotNull):

*   None

---

### Program 03: 03_feature_engineering.sas

#### List of transformations in the order of execution and description:

1.  **`Window.partitionBy("customer_id").orderBy("transaction_datetime")`**:
    *   **Description:** Defines a window specification named `window_spec_customer` to partition the data by `"customer_id"` and order it by `"transaction_datetime"`. This is used for calculating features related to each customer's transaction history.

2.  **`withColumn("prev_transaction_date_sas", F.lag("transaction_date_sas", 1).over(window_spec_customer))`**:
    *   **Description:** Calculates the previous transaction date for each customer using the `F.lag()` window function. The data is partitioned by `"customer_id"` and ordered by `"transaction_datetime"` to ensure that the lag is calculated within each customer's transaction history.

3.  **`withColumn("days_since_last_txn", F.when(F.col("prev_transaction_date_sas").isNotNull(), F.datediff(F.col("transaction_date_sas"), F.col("prev_transaction_date_sas"))).otherwise(None))`**:
    *   **Description:** Calculates the number of days since the last transaction for each customer. It uses `F.datediff()` to find the difference between the current transaction date and the previous transaction date (obtained using `F.lag()`). If there is no previous transaction (i.e., `prev_transaction_date_sas` is null), `days_since_last_txn` is set to `None`.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to handle cases where there is no previous transaction.

4.  **`.drop("prev_transaction_date_sas")`**:
    *   **Description:** Removes the intermediate column `prev_transaction_date_sas` from the DataFrame.

5.  **`Window.partitionBy("customer_id").orderBy("transaction_datetime").rangeBetween(-F.expr(f"INTERVAL {window_days} DAYS"), 0)`**:
    *   **Description:** Defines a rolling window specification named `window_spec_rolling`. This window is used to calculate features over a rolling time window (specified by `window_days`). The window is partitioned by `"customer_id"`, ordered by `"transaction_datetime"`, and includes rows from `window_days` days before the current transaction up to the current transaction.

6.  **`withColumn(f"txn_count_{window_days}d", F.count("transaction_id").over(window_spec_rolling))`**:
    *   **Description:** Calculates the number of transactions (`txn_count_7d`) within the rolling window for each customer using the `F.count()` aggregation function.

7.  **`withColumn(f"txn_amount_{window_days}d", F.sum("amount").over(window_spec_rolling))`**:
    *   **Description:** Calculates the sum of transaction amounts (`txn_amount_7d`) within the rolling window for each customer using the `F.sum()` aggregation function.

8.  **`withColumn(f"avg_txn_amount_{window_days}d", F.avg("amount").over(window_spec_rolling))`**:
    *   **Description:** Calculates the average transaction amount (`avg_txn_amount_7d`) within the rolling window for each customer using the `F.avg()` aggregation function.

9.  **`withColumn(f"txn_count_{window_days}d", F.coalesce(F.col(f"txn_count_{window_days}d"), F.lit(0)))`**:
    *   **Description:** Handles potential null values in the `txn_count_7d` column (which can occur for the first few transactions of a customer).  It replaces nulls with 0 using `F.coalesce()`.

10. **`withColumn(f"txn_amount_{window_days}d", F.coalesce(F.col(f"txn_amount_{window_days}d"), F.lit(0.0)))`**:
    *   **Description:** Handles potential null values in the `txn_amount_7d` column and replaces nulls with 0.0.

11. **`withColumn(f"avg_txn_amount_{window_days}d", F.coalesce(F.col(f"avg_txn_amount_{window_days}d"), F.lit(0.0)))`**:
    *   **Description:** Handles potential null values in the `avg_txn_amount_7d` column and replaces nulls with 0.0.

12. **`groupBy("customer_id").agg(F.avg("amount").alias("customer_avg_amount"), F.stddev("amount").alias("customer_std_amount"), F.count("transaction_id").alias("customer_txn_count"))`**:
    *   **Description:** Calculates customer-level statistics: the average transaction amount (`customer_avg_amount`), the standard deviation of transaction amounts (`customer_std_amount`), and the number of transactions (`customer_txn_count`).

13. **`.join(F.broadcast(customer_stats_df), on="customer_id", how="left")`**:
    *   **Description:** Joins the customer statistics DataFrame (`customer_stats_df`) with the main DataFrame on `"customer_id"`. A broadcast join is used for efficiency, assuming `customer_stats_df` is relatively small. The join type is "left," meaning all rows from the left DataFrame (the main DataFrame) are retained.

14. **`withColumn("amount_zscore", F.when(F.col("customer_std_amount") > 0, (F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_std_amount")).otherwise(0.0))`**:
    *   **Description:** Calculates the Z-score for each transaction amount, representing how many standard deviations the amount is from the customer's average amount. The Z-score is calculated only if the customer's standard deviation is greater than 0; otherwise, it is set to 0.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to handle the case where the standard deviation is zero.

15. **`withColumn("amount_pct_deviation", F.when(F.col("customer_avg_amount") > 0, ((F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_avg_amount")) * 100).otherwise(0.0))`**:
    *   **Description:** Calculates the percentage deviation of the transaction amount from the customer's average amount. The percentage deviation is calculated only if the customer's average amount is greater than 0; otherwise, it is set to 0.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to handle the case where the average amount is zero.

16. **`withColumn("customer_avg_amount", F.coalesce(F.col("customer_avg_amount"), F.lit(0.0)))`**:
    *   **Description:** Handles potential null values in the `customer_avg_amount` column (which can occur if a customer has only one transaction) and replaces them with 0.0.

17. **`withColumn("customer_std_amount", F.coalesce(F.col("customer_std_amount"), F.lit(0.0)))`**:
    *   **Description:** Handles potential null values in the `customer_std_amount` column and replaces them with 0.0.

18. **`withColumn("customer_txn_count", F.coalesce(F.col("customer_txn_count"), F.lit(0)))`**:
    *   **Description:** Handles potential null values in the `customer_txn_count` column and replaces them with 0.

19. **`groupBy("country_code_clean").agg(F.count("transaction_id").alias("country_txn_count"))`**:
    *   **Description:** Calculates the number of transactions for each country code.

20. **`.join(F.broadcast(country_counts_df), on="country_code_clean", how="left")`**:
    *   **Description:** Joins the country counts DataFrame (`country_counts_df`) with the main DataFrame on `"country_code_clean"`.  A broadcast join is used, assuming `country_counts_df` is relatively small. The join type is "left".

21. **`withColumn("is_rare_country", F.when(F.col("country_txn_count") < 10, 1).otherwise(0))`**:
    *   **Description:** Creates a flag `is_rare_country` indicating whether a country has fewer than 10 transactions.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to set the flag.

22. **`withColumn("is_international", (F.col("country_code_clean") != "US").cast(T.IntegerType()))`**:
    *   **Description:** Creates a flag `is_international` indicating whether the country code is not "US".

23. **`withColumn("country_txn_count", F.coalesce(F.col("country_txn_count"), F.lit(0)))`**:
    *   **Description:** Handles potential null values in the `country_txn_count` column and replaces them with 0.

24. **`withColumn("txn_hour", F.hour(F.col("transaction_datetime")))`**:
    *   **Description:** Extracts the hour of the day from the `"transaction_datetime"` column.

25. **`withColumn("txn_day_of_week", F.dayofweek(F.col("transaction_date_sas")))`**:
    *   **Description:** Extracts the day of the week from the `"transaction_date_sas"` column.

26. **`withColumn("txn_day_of_month", F.dayofmonth(F.col("transaction_date_sas")))`**:
    *   **Description:** Extracts the day of the month from the `"transaction_date_sas"` column.

27. **`withColumn("txn_month", F.month(F.col("transaction_date_sas")))`**:
    *   **Description:** Extracts the month from the `"transaction_date_sas"` column.

28. **`withColumn("time_of_day", F.when(...).when(...).when(...).otherwise(...))`**:
    *   **Description:** Creates a new column named `"time_of_day"` based on the value of `"txn_hour"`, categorizing transactions into "NIGHT", "MORNING", "AFTERNOON", or "EVENING".
    *   **Conditional Logic:** Uses nested `F.when().otherwise()` conditions to categorize the time of day.

29. **`withColumn("is_weekend", F.col("txn_day_of_week").isin([1, 7]).cast(T.IntegerType()))`**:
    *   **Description:** Creates a flag `is_weekend` indicating whether the transaction occurred on a weekend (Sunday or Saturday).
    *   **Conditional Logic:** Uses `F.isin()` to check if `txn_day_of_week` is in the list \[1, 7].

30. **`withColumn("is_unusual_hour", ((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6)).cast(T.IntegerType()))`**:
    *   **Description:** Creates a flag `is_unusual_hour` indicating whether the transaction occurred during unusual hours (between midnight and 6 AM).
    *   **Conditional Logic:** Uses a boolean expression cast to an integer.

#### Business Rules implemented in transformations:

*   **Velocity Feature Calculation:** Calculates transaction counts, total amounts, and average amounts within a rolling 7-day window.
*   **Amount Deviation Feature Calculation:** Calculates Z-scores and percentage deviations to identify transactions with amounts that are unusual for a given customer.
*   **Time-Based Feature Creation:** Extracts and creates features like hour of day, day of week, day of month, month, time of day categories, and weekend/unusual hour flags.
*   **Location-Based Feature Creation:** Creates features related to the transaction's country, including a flag for rare countries and international transactions.

#### Conditional logic (when, otherwise, filter, where):

*   `F.when().otherwise()` is used to calculate `days_since_last_txn`, `amount_zscore`, `amount_pct_deviation`, `time_of_day`,  `is_rare_country`.
*   Boolean expressions are used to create the `is_weekend` and `is_unusual_hour` flags.

#### Aggregations and groupBy operations:

*   `groupBy().agg()` is used to calculate customer-level statistics.
*   `F.count()`, `F.sum()`, and `F.avg()` are used within window functions and aggregations.

#### Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):

*   `F.lag()` is used to calculate `prev_transaction_date_sas`.
*   Window functions with `F.count()`, `F.sum()`, and `F.avg()` are used to calculate rolling window features (velocity).

#### Key calculations and column transformations (withColumn, expr):

*   `withColumn` is used extensively to create new features and perform calculations.
*   `F.datediff()`, `F.hour()`, `F.dayofweek()`, `F.dayofmonth()`, `F.month()`, `F.isin()`, and arithmetic operations are used within `withColumn`.

#### Data validation and quality checks (filter, isNull, isNotNull):

*   `F.coalesce()` is used to handle potential null values in several columns.

---

### Program 04: 04_rule_based_detection.sas

#### List of transformations in the order of execution and description:

1.  **`withColumn("rule_high_velocity", (F.col("txn_count_7d") > 10).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_high_velocity` based on whether the `txn_count_7d` (number of transactions in the last 7 days) is greater than 10.

2.  **`withColumn("rule_amount_deviation", (F.abs(F.col("amount_zscore")) > 3).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_amount_deviation` based on whether the absolute value of `amount_zscore` (amount deviation) is greater than 3.

3.  **`withColumn("rule_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_high_amount` based on whether the transaction `amount` is greater than 5000.

4.  **`withColumn("rule_unusual_hour", (F.col("is_unusual_hour") == 1).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_unusual_hour` based on whether the `is_unusual_hour` flag is equal to 1.

5.  **`withColumn("rule_international", (F.col("is_international") == 1).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_international` based on whether the `is_international` flag is equal to 1.

6.  **`withColumn("rule_rare_country", (F.col("is_rare_country") == 1).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_rare_country` based on whether the `is_rare_country` flag is equal to 1.

7.  **`withColumn("rule_rapid_succession", (F.col("days_since_last_txn").isNotNull() & (F.col("days_since_last_txn") < 0.042)).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_rapid_succession` based on whether the time since the last transaction is less than 0.042 days (approximately 1 hour). Also checks if `days_since_last_txn` is not null.
    *   **Conditional Logic:** Uses `&` (bitwise AND).

8.  **`withColumn("rule_round_amount", ((F.col("amount") % 100 == 0) & (F.col("amount") >= 1000)).cast(T.IntegerType()))`**:
    *   **Description:** Creates a rule flag `rule_round_amount` based on whether the amount is a multiple of 100 and is greater than or equal to 1000.
    *   **Conditional Logic:** Uses `&` (bitwise AND).

9.  **`withColumn("rule_score", (F.col("rule_high_velocity") * 25) + (F.col("rule_amount_deviation") * 30) + ...)`**:
    *   **Description:** Calculates the `rule_score` by summing the points for triggered rules. Each rule flag is multiplied by a weight.

10. **`withColumn("rule_triggered_array", F.array_remove(F.array(*rule_names), F.lit(None)))`**:
    *   **Description:**  Creates an array of triggered rule names.  It uses `F.array()` to create an array of rule names and `F.array_remove()` to remove any `None` values.
    *   **Conditional Logic:** Uses nested `F.when().otherwise()` conditions to populate the array based on the rule flags.

11. **`withColumn("rule_triggered", F.concat_ws(", ", F.col("rule_triggered_array")))`**:
    *   **Description:** Concatenates the triggered rule names in the `rule_triggered_array` into a single string, separated by commas and spaces.

12. **`.drop("rule_triggered_array")`**:
    *   **Description:** Drops the intermediate column `rule_triggered_array`.

13. **`withColumn("rule_risk_level", F.when(...).when(...).when(...).otherwise(...))`**:
    *   **Description:** Determines the `rule_risk_level` based on the `rule_score`.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to assign risk levels (CRITICAL, HIGH, MEDIUM, LOW) based on score thresholds.

14. **`withColumn("is_suspicious", (F.col("rule_score") >= 50).cast(T.IntegerType()))`**:
    *   **Description:** Creates a flag `is_suspicious` indicating whether a transaction is suspicious based on whether the `rule_score` is greater than or equal to 50.

15. **`.filter(F.col("rule_score") >= threshold)`**:
    *   **Description:** Filters the DataFrame to include only transactions with a rule score greater or equal to the threshold.

16. **`.orderBy(F.col("rule_score").desc(), F.col("transaction_date_sas").desc())`**:
    *   **Description:** Orders the DataFrame by `rule_score` in descending order and by `transaction_date_sas` in descending order.

17. **`.groupBy("rule_risk_level").count().orderBy("rule_risk_level")`**:
    *   **Description:** Groups the DataFrame by `rule_risk_level` and counts the number of transactions in each risk level. The results are ordered by `rule_risk_level`.

18. **`.groupBy().agg(...)`**:
    *   **Description:** Calculates the total count for each rule.

19. **`df.sparkSession.createDataFrame(summary_data, schema=summary_schema).orderBy(F.col("trigger_count").desc())`**:
    *   **Description:** Creates a DataFrame from the summary data, orders by trigger count.

#### Business Rules implemented in transformations:

*   **Rule-Based Fraud Detection:** Implements a series of rules based on various features to identify potentially fraudulent transactions.  Each rule is assigned a score.
*   **Risk Level Assignment:** Assigns a risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the total rule score.
*   **Alert Generation:** Generates alerts for transactions exceeding a specified risk threshold.

#### Conditional logic (when, otherwise, filter, where):

*   `F.when().otherwise()` is used to create the rule flags, calculate the `rule_risk_level`, and generate the `rule_triggered_array`.
*   `.filter()` is used to select suspicious transactions and is used in the rule summary.

#### Aggregations and groupBy operations:

*   `groupBy().count()` is used to count the number of transactions by risk level and is used in the rule summary.
*   `groupBy().agg()` is used to aggregate data for the rule summary.

#### Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):

*   None

#### Key calculations and column transformations (withColumn, expr):

*   `withColumn` is used extensively to create rule flags, calculate the `rule_score`, `rule_risk_level`, and the `rule_triggered` string.
*   Arithmetic operations, `F.abs()`, `F.lit()`, `F.array()`, `F.array_remove()`, and `F.concat_ws()` are used within `withColumn`.

#### Data validation and quality checks (filter, isNull, isNotNull):

*   None

---

### Program 05: 05_ml_scoring_model.sas

#### List of transformations in the order of execution and description:

1.  **`withColumn("is_high_amount", (F.col("amount") > 1000).cast(T.IntegerType()))`**:
    *   **Description:** Creates a binary flag `is_high_amount` indicating whether the transaction amount is greater than 1000.

2.  **`withColumn("is_very_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`**:
    *   **Description:** Creates a binary flag `is_very_high_amount` indicating whether the transaction amount is greater than 5000.

3.  **`withColumn("amount_normalized", F.col("amount") / 10000)`**:
    *   **Description:** Normalizes the `amount` column by dividing it by 10000.

4.  **`withColumn("txn_count_normalized", F.col("txn_count_7d") / 20)`**:
    *   **Description:** Normalizes the `txn_count_7d` column by dividing it by 20.

5.  **`withColumn("amount_zscore", F.coalesce(F.col("amount_zscore"), F.lit(0.0)))`**:
    *   **Description:** Handles potential null values in the `amount_zscore` column and replaces them with 0.0.

6.  **`withColumn("days_since_last_txn", F.coalesce(F.col("days_since_last_txn"), F.lit(999.0)))`**:
    *   **Description:** Handles potential null values in the `days_since_last_txn` column and replaces them with 999.0.

7.  **`withColumn("amount_x_velocity", F.col("amount_normalized") * F.col("txn_count_normalized"))`**:
    *   **Description:** Creates an interaction feature `amount_x_velocity` by multiplying the normalized amount and normalized transaction count.

8.  **`withColumn("amount_x_deviation", F.col("amount_normalized") * F.abs(F.col("amount_zscore")))`**:
    *   **Description:** Creates an interaction feature `amount_x_deviation` by multiplying the normalized amount and the absolute value of the amount Z-score.

9.  **`withColumn("logit_score", ...)`**:
    *   **Description:** Calculates the logit score using a simulated logistic regression model. This involves a weighted sum of the features and an intercept.

10. **`withColumn("ml_score_probability", F.lit(1) / (F.lit(1) + F.exp(-F.col("logit_score"))))`**:
    *   **Description:** Converts the `logit_score` to a probability using the sigmoid function.

11. **`withColumn("ml_score", (F.col("ml_score_probability") * 100).cast(T.IntegerType()))`**:
    *   **Description:** Scales the probability to a score between 0 and 100.

12. **`withColumn("ml_risk_level", F.when(...).when(...).when(...).otherwise(...))`**:
    *   **Description:** Assigns an ML-based risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the `ml_score`.
    *   **Conditional Logic:** Uses `F.when().otherwise()` to assign risk levels based on score thresholds.

#### Business Rules implemented in transformations:

*   **Feature Engineering:** Creates binary flags, normalizes continuous variables, and creates interaction features for use in the ML model.
*   **ML Score Calculation:** Calculates an ML-based fraud score using a simulated logistic regression model.
*   **Risk Level Assignment:** Assigns an ML-based risk level based on the calculated ML score.

#### Conditional logic (when, otherwise, filter, where):

*   `F.when().otherwise()` is used to assign the `ml_risk_level`.

#### Aggregations and groupBy operations:

*   None

#### Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):

*   None

#### Key calculations and column transformations (withColumn, expr):

*   `withColumn` is used extensively to create new features, normalize variables, calculate the logit score, calculate the probability, and assign the `ml_risk_level`.
*   Arithmetic operations, `F.abs()`, `F.lit()`, and `F.exp()` are used within `withColumn`.

#### Data validation and quality checks (filter, isNull, isNotNull):

*   `F.coalesce()` is used to handle missing values.

---

### Program 06: 06_combine_scores_reporting.sas

#### List of transformations in the order of execution and description:

1.  **`withColumn("final_fraud_score", (F.col("rule_score") * 0.4) + (F.col("ml_score") * 0.6))`**:
    *   **Description:** Calculates the `final_fraud_score` as a
# Spark SQL and Analytical Operations
### PySpark Program Analysis

This PySpark program implements a fraud detection pipeline, mirroring the functionality of SAS programs. It imports, validates, cleans, and transforms transaction data, applies rule-based and machine learning (ML) scoring, and generates reports.

**Overall Structure:**

*   **Initialization:** Sets up a SparkSession with configurations for performance.
*   **Data Import and Validation:** Reads transaction data from a CSV, defines a schema, and validates data quality.
*   **Data Cleaning and Standardization:** Cleans and standardizes various transaction attributes like transaction type, merchant name, and country code.
*   **Feature Engineering:** Calculates new features such as velocity, amount deviation, time-based, and location-based features.
*   **Rule-Based Detection:** Applies a set of predefined rules to identify potentially fraudulent transactions.
*   **ML Scoring:** Simulates a logistic regression model to assign fraud scores.
*   **Score Combination and Reporting:** Combines rule-based and ML scores, generates a final fraud assessment, and produces reports.

**Detailed Analysis of Each Program/Function:**

1.  **`01_transaction_data_import.sas`**

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** None
    *   **Statistical Functions:** None
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** None
    *   **Business Application:** Imports transaction data from a CSV file, which is the initial step for any analysis.

    ```python
    def import_transactions(spark: SparkSession, filepath: str, schema: T.StructType) -> T.DataFrame:
        """
        Imports transaction data from a CSV file.
        Maps to SAS macro IMPORT_TRANSACTIONS.
        """
        logger.info(f"Attempting to import data from {filepath}...")
        try:
            df = spark.read \
                .option("header", "true") \
                .schema(schema) \
                .csv(filepath)
            logger.info(f"Successfully imported {filepath}.")
            return df
        except Exception as e:
            logger.error(f"ERROR: Failed to import {filepath}. Error: {e}")
            sys.exit(1) # Abort program as in SAS %ABORT

    def validate_transactions(df: T.DataFrame) -> T.DataFrame:
        """
        Validates the imported transaction data by checking for missing values and invalid amounts.
        Filters out invalid records.
        Maps to SAS macro VALIDATE_DATA.
        """
        logger.info("Starting data validation...")

        total_count = df.count()
        logger.info(f"Total records before validation: {total_count}")

        # SAS: Create validation flags based on missing values and amount <= 0
        # PySpark: Use F.when().otherwise() for conditional logic
        validated_df = df.withColumn(
            "validation_status",
            F.when(F.col("transaction_id").isNull(), F.lit("MISSING_ID"))
            .when(F.col("customer_id").isNull(), F.lit("MISSING_CUSTOMER"))
            .when(F.col("amount").isNull(), F.lit("MISSING_AMOUNT"))
            .when(F.col("transaction_date").isNull(), F.lit("MISSING_DATE"))
            .when(F.col("amount") <= 0, F.lit("INVALID_AMOUNT"))
            .otherwise(F.lit("VALID"))
        )

        # SAS: Keep only valid records
        # PySpark: Use .filter()
        validated_df = validated_df.filter(F.col("validation_status") == "VALID")

        valid_count = validated_df.count()
        logger.info(f"Validated {valid_count} of {total_count} records.")

        return validated_df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn` (conditional logic using `F.when().otherwise()`) and `filter`
    *   **Statistical Functions:** None
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** Logs the number of valid and invalid records.
    *   **Business Application:** Validates the imported data to ensure data quality by checking for missing values and invalid amounts.

2.  **`02_data_quality_cleaning.sas`**

    ```python
    def clean_transactions(df: T.DataFrame) -> T.DataFrame:
        """
        Cleans and standardizes transaction data.
        Maps to SAS macro CLEAN_TRANSACTIONS.
        """
        logger.info("Starting transaction data cleaning and standardization...")

        # SAS: Standardize transaction type (UPCASE, STRIP)
        # PySpark: F.upper(), F.trim()
        df = df.withColumn("transaction_type_clean", F.upper(F.trim(F.col("transaction_type"))))

        # SAS: Clean merchant name (PROPCASE, STRIP)
        # PySpark: F.initcap(), F.trim()
        df = df.withColumn("merchant_name_clean", F.initcap(F.trim(F.col("merchant_name"))))

        # SAS: Standardize country code (UPCASE, SUBSTR(country_code, 1, 2))
        # PySpark: F.upper(), F.substring()
        df = df.withColumn("country_code_clean", F.upper(F.substring(F.col("country_code"), 1, 2)))

        # SAS: Handle missing amounts - replace with 0
        # PySpark: F.coalesce()
        df = df.withColumn("amount", F.coalesce(F.col("amount"), F.lit(0)))

        # SAS: Convert transaction date to SAS date format (INPUT(transaction_date, YYMMDD10.))
        # PySpark: F.to_date()
        df = df.withColumn("transaction_date_sas", F.to_date(F.col("transaction_date"), "yyyy-MM-dd"))

        # SAS: Create transaction timestamp (DHMS(transaction_date_sas, HOUR(transaction_time), ...))
        # PySpark: F.to_timestamp() by concatenating date and time strings
        df = df.withColumn(
            "transaction_datetime",
            F.to_timestamp(F.concat_ws(" ", F.col("transaction_date"), F.col("transaction_time")), "yyyy-MM-dd HH:mm:ss")
        )

        logger.info("Transaction data cleaned and standardized.")
        return df

    def remove_duplicates(df: T.DataFrame, key_cols: list) -> T.DataFrame:
        """
        Removes duplicate records based on specified key columns.
        Maps to SAS macro REMOVE_DUPLICATES.
        """
        logger.info(f"Starting duplicate removal based on key: {key_cols}...")

        before_count = df.count()
        # SAS: PROC SORT DATA=&inds OUT=&outds NODUPKEY BY &key;
        # PySpark: .dropDuplicates()
        deduped_df = df.dropDuplicates(key_cols)
        after_count = deduped_df.count()

        dup_count = before_count - after_count
        logger.info(f"Removed {dup_count} duplicate records.")

        return deduped_df

    def handle_outliers(df: T.DataFrame, var_col: str, method: str = "WINSORIZE") -> T.DataFrame:
        """
        Handles outliers in a specified variable using Winsorization or removal.
        Maps to SAS macro HANDLE_OUTLIERS.
        """
        logger.info(f"Handling outliers in '{var_col}' using '{method}' method...")

        # SAS: PROC MEANS ... OUTPUT OUT=percentiles P1=p1 P99=p99;
        # PySpark: .approxQuantile()
        # Note: approxQuantile returns a list of values for the specified probabilities
        percentiles = df.approxQuantile(var_col, [0.01, 0.99], 0.01)
        p1_value = percentiles[0]
        p99_value = percentiles[1]

        logger.info(f"1st percentile for '{var_col}': {p1_value}")
        logger.info(f"99th percentile for '{var_col}': {p99_value}")

        if method.upper() == "WINSORIZE":
            # SAS: if &var < &p1_value then &var = &p1_value; else if &var > &p99_value then &var = &p1_value;
            # PySpark: F.when().otherwise()
            df = df.withColumn(
                var_col,
                F.when(F.col(var_col) < p1_value, p1_value)
                .when(F.col(var_col) > p99_value, p99_value)
                .otherwise(F.col(var_col))
            )
        elif method.upper() == "REMOVE":
            # SAS: if &var >= &p1_value AND &var <= &p99_value;
            # PySpark: .filter()
            df = df.filter((F.col(var_col) >= p1_value) & (F.col(var_col) <= p99_value))
        else:
            logger.warning(f"Unknown outlier handling method: {method}. No action taken.")

        logger.info(f"Outliers in '{var_col}' handled using '{method}' method.")
        return df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `dropDuplicates`, and `filter`
    *   **Statistical Functions:** `approxQuantile`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** Logs information about the number of duplicate records removed and outlier handling.
    *   **Business Application:** Cleans and standardizes the data by cleaning transaction types, merchant names, country codes, handling missing amounts, and converting date and time formats. Removes duplicate transactions and handles outliers in the amount variable.

3.  **`03_feature_engineering.sas`**

    ```python
    def calculate_velocity_features(df: T.DataFrame, window_days: int = 7) -> T.DataFrame:
        """
        Calculates velocity features (transaction counts and amounts within a rolling window)
        and days since last transaction for each customer.
        Maps to SAS macro CALCULATE_VELOCITY.
        """
        logger.info(f"Calculating velocity features for a {window_days}-day window...")

        # SAS: PROC SORT DATA=&inds; BY customer_id transaction_date_sas transaction_time;
        # PySpark: Define window specification for customer-level ordering
        window_spec_customer = Window.partitionBy("customer_id").orderBy("transaction_datetime")

        # SAS: days_since_last_txn = transaction_date_sas - last_txn_date;
        # PySpark: F.lag() to get previous date, F.datediff()
        df = df.withColumn(
            "prev_transaction_date_sas",
            F.lag("transaction_date_sas", 1).over(window_spec_customer)
        ).withColumn(
            "days_since_last_txn",
            F.when(
                F.col("prev_transaction_date_sas").isNotNull(),
                F.datediff(F.col("transaction_date_sas"), F.col("prev_transaction_date_sas"))
            ).otherwise(None) # SAS uses '.' for missing, PySpark uses None
        ).drop("prev_transaction_date_sas")

        # SAS: Rolling window calculations (txn_count_&window_days.d, txn_amount_&window_days.d, avg_txn_amount_&window_days.d)
        # The SAS RETAIN logic with conditional reset is complex to map directly to standard Spark window functions.
        # We'll use a fixed-interval rolling window, which is a common and performant interpretation of "velocity" in Spark.
        # This window includes transactions from 'window_days' ago up to the current transaction.
        window_spec_rolling = Window.partitionBy("customer_id").orderBy("transaction_datetime").rangeBetween(
            -F.expr(f"INTERVAL {window_days} DAYS"), 0
        )

        df = df.withColumn(f"txn_count_{window_days}d", F.count("transaction_id").over(window_spec_rolling)) \
               .withColumn(f"txn_amount_{window_days}d", F.sum("amount").over(window_spec_rolling)) \
               .withColumn(f"avg_txn_amount_{window_days}d", F.avg("amount").over(window_spec_rolling))

        # Handle potential nulls from window functions for first records
        df = df.withColumn(f"txn_count_{window_days}d", F.coalesce(F.col(f"txn_count_{window_days}d"), F.lit(0)))
        df = df.withColumn(f"txn_amount_{window_days}d", F.coalesce(F.col(f"txn_amount_{window_days}d"), F.lit(0.0)))
        df = df.withColumn(f"avg_txn_amount_{window_days}d", F.coalesce(F.col(f"avg_txn_amount_{window_days}d"), F.lit(0.0)))

        logger.info("Velocity features calculated.")
        return df

    def calculate_amount_deviation(df: T.DataFrame) -> T.DataFrame:
        """
        Calculates amount deviation features (average amount, standard deviation, Z-score,
        and percentage deviation) for each customer.
        Maps to SAS macro CALCULATE_AMOUNT_DEVIATION.
        """
        logger.info("Calculating amount deviation features...")

        # SAS: PROC MEANS ... BY customer_id ... OUTPUT OUT=customer_stats ...
        # PySpark: .groupBy().agg()
        customer_stats_df = df.groupBy("customer_id").agg(
            F.avg("amount").alias("customer_avg_amount"),
            F.stddev("amount").alias("customer_std_amount"),
            F.count("transaction_id").alias("customer_txn_count")
        )

        # SAS: PROC SQL ... LEFT JOIN customer_stats ...
        # PySpark: .join() with broadcast hint for efficiency if customer_stats_df is small
        df = df.join(F.broadcast(customer_stats_df), on="customer_id", how="left")

        # SAS: CASE WHEN b.customer_std_amount > 0 THEN ... ELSE 0 END AS amount_zscore
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "amount_zscore",
            F.when(F.col("customer_std_amount") > 0,
                   (F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_std_amount"))
            .otherwise(0.0)
        )

        # SAS: CASE WHEN b.customer_avg_amount > 0 THEN ... ELSE 0 END AS amount_pct_deviation
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "amount_pct_deviation",
            F.when(F.col("customer_avg_amount") > 0,
                   ((F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_avg_amount")) * 100)
            .otherwise(0.0)
        )

        # Fill potential nulls from join for new customers or if no stats
        df = df.withColumn("customer_avg_amount", F.coalesce(F.col("customer_avg_amount"), F.lit(0.0)))
        df = df.withColumn("customer_std_amount", F.coalesce(F.col("customer_std_amount"), F.lit(0.0)))
        df = df.withColumn("customer_txn_count", F.coalesce(F.col("customer_txn_count"), F.lit(0)))

        logger.info("Amount deviation features calculated.")
        return df

    def create_time_features(df: T.DataFrame) -> T.DataFrame:
        """
        Creates time-based features from the transaction date and time.
        Maps to SAS macro CREATE_TIME_FEATURES.
        """
        logger.info("Creating time-based features...")

        # SAS: HOUR(transaction_time), WEEKDAY(transaction_date_sas), DAY(transaction_date_sas), MONTH(transaction_date_sas)
        # PySpark: F.hour(), F.dayofweek(), F.dayofmonth(), F.month()
        df = df.withColumn("txn_hour", F.hour(F.col("transaction_datetime"))) \
               .withColumn("txn_day_of_week", F.dayofweek(F.col("transaction_date_sas"))) \
               .withColumn("txn_day_of_month", F.dayofmonth(F.col("transaction_date_sas"))) \
               .withColumn("txn_month", F.month(F.col("transaction_date_sas")))

        # SAS: Create time-of-day categories (IF/ELSE IF)
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "time_of_day",
            F.when((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6), F.lit("NIGHT"))
            .when((F.col("txn_hour") >= 6) & (F.col("txn_hour") < 12), F.lit("MORNING"))
            .when((F.col("txn_hour") >= 12) & (F.col("txn_hour") < 18), F.lit("AFTERNOON"))
            .otherwise(F.lit("EVENING"))
        )

        # SAS: Create weekend flag (txn_day_of_week IN (1, 7))
        # PySpark: F.isin()
        df = df.withColumn("is_weekend", F.col("txn_day_of_week").isin([1, 7]).cast(T.IntegerType()))

        # SAS: Create unusual hour flag (txn_hour >= 0 AND txn_hour < 6)
        # PySpark: Boolean expression cast to IntegerType
        df = df.withColumn("is_unusual_hour", ((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6)).cast(T.IntegerType()))

        logger.info("Time-based features created.")
        return df

    def create_location_features(df: T.DataFrame) -> T.DataFrame:
        """
        Creates location-based features.
        Maps to SAS macro CREATE_LOCATION_FEATURES.
        """
        logger.info("Creating location-based features...")

        # SAS: PROC SQL ... GROUP BY country_code_clean ...
        # PySpark: .groupBy().agg()
        country_counts_df = df.groupBy("country_code_clean").agg(
            F.count("transaction_id").alias("country_txn_count")
        )

        # SAS: PROC SQL ... LEFT JOIN country_counts ...
        # PySpark: .join() with broadcast hint
        df = df.join(F.broadcast(country_counts_df), on="country_code_clean", how="left")

        # SAS: CASE WHEN b.country_txn_count < 10 THEN 1 ELSE 0 END AS is_rare_country
        # PySpark: F.when().otherwise()
        df = df.withColumn(
            "is_rare_country",
            F.when(F.col("country_txn_count") < 10, 1).otherwise(0)
        )

        # SAS: CASE WHEN a.country_code_clean NE 'US' THEN 1 ELSE 0 END AS is_international
        # PySpark: Boolean expression cast to IntegerType
        df = df.withColumn(
            "is_international",
            (F.col("country_code_clean") != "US").cast(T.IntegerType())
        )

        # Fill potential nulls from join
        df = df.withColumn("country_txn_count", F.coalesce(F.col("country_txn_count"), F.lit(0)))

        logger.info("Location-based features created.")
        return df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `groupBy().agg()`, `join`, `Window.partitionBy().orderBy().rangeBetween()`
    *   **Statistical Functions:** `avg`, `stddev`, `count`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:** None
    *   **Business Application:** Calculates features used for fraud detection. These include:
        *   **Velocity Features:** Calculates rolling transaction counts, amounts, and average transaction amounts over a 7-day window.
        *   **Amount Deviation Features:** Calculates average amount, standard deviation, Z-score, and percentage deviation for each customer.
        *   **Time-Based Features:** Extracts hour, day of the week, day of the month, and month from the transaction datetime. Creates flags for time of day, weekend, and unusual hours.
        *   **Location-Based Features:** Calculates transaction counts by country and creates flags for rare countries and international transactions.

4.  **`04_rule_based_detection.sas`**

    ```python
    def apply_fraud_rules(df: T.DataFrame) -> T.DataFrame:
        """
        Applies rule-based fraud detection logic and calculates a rule score.
        Maps to SAS macro APPLY_FRAUD_RULES.
        """
        logger.info("Applying fraud detection rules...")

        # Initialize rule flags and scores
        # In PySpark, we build up the score and triggered rules iteratively or in one go.
        # Let's create individual rule flags first, then sum scores and concatenate names.

        # Rule 1: High velocity (>10 transactions in 7 days)
        df = df.withColumn("rule_high_velocity", (F.col("txn_count_7d") > 10).cast(T.IntegerType()))
        # Rule 2: Large amount deviation (>3 standard deviations)
        df = df.withColumn("rule_amount_deviation", (F.abs(F.col("amount_zscore")) > 3).cast(T.IntegerType()))
        # Rule 3: High amount (>$5000)
        df = df.withColumn("rule_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))
        # Rule 4: Unusual hour transaction
        df = df.withColumn("rule_unusual_hour", (F.col("is_unusual_hour") == 1).cast(T.IntegerType()))
        # Rule 5: International transaction
        df = df.withColumn("rule_international", (F.col("is_international") == 1).cast(T.IntegerType()))
        # Rule 6: Rare country
        df = df.withColumn("rule_rare_country", (F.col("is_rare_country") == 1).cast(T.IntegerType()))
        # Rule 7: Multiple transactions in short time (less than 1 hour = 0.042 days)
        # Handle potential nulls in days_since_last_txn by treating them as not rapid succession
        df = df.withColumn("rule_rapid_succession",
                           (F.col("days_since_last_txn").isNotNull() & (F.col("days_since_last_txn") < 0.042)).cast(T.IntegerType()))
        # Rule 8: Round amount (multiple of 100 and >= 1000)
        df = df.withColumn("rule_round_amount",
                           ((F.col("amount") % 100 == 0) & (F.col("amount") >= 1000)).cast(T.IntegerType()))

        # Calculate rule_score by summing points for triggered rules
        df = df.withColumn("rule_score",
            (F.col("rule_high_velocity") * 25) +
            (F.col("rule_amount_deviation") * 30) +
            (F.col("rule_high_amount") * 20) +
            (F.col("rule_unusual_hour") * 15) +
            (F.col("rule_international") * 10) +
            (F.col("rule_rare_country") * 15) +
            (F.col("rule_rapid_succession") * 25) +
            (F.col("rule_round_amount") * 10)
        )

        # Concatenate triggered rule names
        rule_names = [
            F.when(F.col("rule_high_velocity") == 1, F.lit("HIGH_VELOCITY")),
            F.when(F.col("rule_amount_deviation") == 1, F.lit("AMOUNT_DEVIATION")),
            F.when(F.col("rule_high_amount") == 1, F.lit("HIGH_AMOUNT")),
            F.when(F.col("rule_unusual_hour") == 1, F.lit("UNUSUAL_HOUR")),
            F.when(F.col("rule_international") == 1, F.lit("INTERNATIONAL")),
            F.when(F.col("rule_rare_country") == 1, F.lit("RARE_COUNTRY")),
            F.when(F.col("rule_rapid_succession") == 1, F.lit("RAPID_SUCCESSION")),
            F.when(F.col("rule_round_amount") == 1, F.lit("ROUND_AMOUNT"))
        ]
        # Filter out None values from the array before concatenating
        df = df.withColumn("rule_triggered_array", F.array_remove(F.array(*rule_names), F.lit(None)))
        df = df.withColumn("rule_triggered", F.concat_ws(", ", F.col("rule_triggered_array")))
        df = df.drop("rule_triggered_array") # Clean up intermediate column

        # Calculate final rule-based risk level
        df = df.withColumn(
            "rule_risk_level",
            F.when(F.col("rule_score") >= 75, F.lit("CRITICAL"))
            .when(F.col("rule_score") >= 50, F.lit("HIGH"))
            .when(F.col("rule_score") >= 25, F.lit("MEDIUM"))
            .otherwise(F.lit("LOW"))
        )

        # Flag for investigation
        df = df.withColumn("is_suspicious", (F.col("rule_score") >= 50).cast(T.IntegerType()))

        logger.info("Fraud detection rules applied.")
        return df

    def generate_rule_alerts(df: T.DataFrame, threshold: int = 50) -> T.DataFrame:
        """
        Generates alerts based on the rule score and provides a summary.
        Maps to SAS macro GENERATE_RULE_ALERTS.
        """
        logger.info(f"Generating rule-based alerts with threshold >= {threshold}...")

        total_transactions = df.count()

        # SAS: Filter suspicious transactions (WHERE rule_score >= &threshold;)
        # PySpark: .filter()
        alerts_df = df.filter(F.col("rule_score") >= threshold)

        # SAS: Sort by risk score (PROC SORT BY DESCENDING rule_score transaction_date_sas;)
        # PySpark: .orderBy()
        alerts_df = alerts_df.orderBy(F.col("rule_score").desc(), F.col("transaction_date_sas").desc())

        # SAS: Count alerts by risk level (PROC FREQ TABLES rule_risk_level / NOCUM;)
        # PySpark: .groupBy().count()
        risk_level_counts = alerts_df.groupBy("rule_risk_level").count().orderBy("rule_risk_level")
        logger.info("Rule-Based Alerts by Risk Level:")
        risk_level_counts.show(truncate=False)

        alert_count = alerts_df.count()
        alert_rate = (alert_count / total_transactions * 100) if total_transactions > 0 else 0.0
        logger.info(f"Generated {alert_count} alerts ({alert_rate:.2f}% of transactions).")

        return alerts_df

    def rule_summary_report(df: T.DataFrame) -> T.DataFrame:
        """
        Creates a summary report of rule triggers.
        Maps to SAS macro RULE_SUMMARY_REPORT.
        """
        logger.info("Generating rule summary report...")

        # SAS: PROC SQL ... UNION ALL for each rule
        # PySpark: Aggregate individual rule flags and then union
        rule_summary_df = df.groupBy().agg(
            F.sum(F.col("rule_high_velocity")).alias("HIGH_VELOCITY"),
            F.sum(F.col("rule_amount_deviation")).alias("AMOUNT_DEVIATION"),
            F.sum(F.col("rule_high_amount")).alias("HIGH_AMOUNT"),
            F.sum(F.col("rule_unusual_hour")).alias("UNUSUAL_HOUR"),
            F.sum(F.col("rule_international")).alias("INTERNATIONAL"),
            F.sum(F.col("rule_rare_country")).alias("RARE_COUNTRY"),
            F.sum(F.col("rule_rapid_succession")).alias("RAPID_SUCCESSION"),
            F.sum(F.col("rule_round_amount")).alias("ROUND_AMOUNT")
        ).collect()[0].asDict() # Get the single row as a dictionary

        # Convert dictionary to a DataFrame for display
        summary_data = []
        for rule_name, trigger_count in rule_summary_df.items():
            summary_data.append((rule_name, trigger_count))

        summary_schema = T.StructType([
            T.StructField("rule_name", T.StringType(), True),
            T.StructField("trigger_count", T.LongType(), True)
        ])
        rule_summary_df = df.sparkSession.createDataFrame(summary_data, schema=summary_schema) \
            .orderBy(F.col("trigger_count").desc())

        logger.info("Fraud Rule Trigger Summary:")
        rule_summary_df.show(truncate=False)

        return rule_summary_df
    ```

    *   **Spark SQL Queries:** None
    *   **Analytical Operations:** `withColumn`, `filter`, `groupBy().count()`, `orderBy` and `F.array_remove`
    *   **Statistical Functions:** `sum`
    *   **Machine Learning/Predictive Logic:** None
    *   **Report Generation and Formatting Logic:**
        *   Generates a summary report of rule triggers.
        *   Logs the rule-based alerts by risk level and alert rate.
        *   Displays the rule summary report.
    *   **Business Application:** Implements rule-based fraud detection. Rules are applied based on the calculated features to generate a rule score. Based on the rule score, a risk level is assigned, and suspicious transactions are flagged.

5.  **`05_ml_scoring_model.sas`**

    ```python
    def prepare_ml_data(df: T.DataFrame) -> T.DataFrame:
        """
        Prepares the data for ML scoring by creating binary flags, normalizing continuous variables,
        and creating interaction features.
        Maps to SAS macro PREPARE_ML_DATA.
        """
        logger.info("Preparing data for ML scoring...")

        # SAS: Create binary flags for categorical variables
        df = df.withColumn("is_high_amount", (F.col("amount") > 1000).cast(T.IntegerType())) \
               .withColumn("is_very_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))

        # SAS: Normalize continuous variables (simple min-max scaling)
        # PySpark: Direct division
        df = df.withColumn("amount_normalized", F.col("amount") / 10000) # Assuming max ~$10k
        df = df.withColumn("txn_count_normalized", F.col("txn_count_7d") / 20) # Assuming max ~20

        # SAS: Handle missing values
        # PySpark: F.coalesce()
        df = df.withColumn("amount_zscore", F.coalesce(F.col("amount_zscore"), F.lit(0.0)))
        df = df.withColumn("days_since_last_txn", F.coalesce(F.col("days_since_last_txn"), F.lit(999.0)))

        # SAS: Create interaction features
        df = df.withColumn("amount_x_velocity", F.col("amount_normalized") * F.col("txn_count_normalized")) \
               .withColumn("amount_x_deviation", F.col("amount_normalized") * F.abs(F.col("amount_zscore")))

        logger.info("Data prepared for ML scoring.")
        return df

    def calculate_ml_score(df: T.DataFrame) -> T.DataFrame:
        """
        Calculates an ML-based fraud score using a simulated logistic regression model.
        Maps to SAS macro CALCULATE_ML_SCORE.
        """
        logger.info("Calculating ML fraud scores (simulated logistic regression)...")

        # Simulated logistic regression coefficients
        # SAS: logit_score = ...
        # PySpark: Direct arithmetic calculation
        df = df.withColumn(
            "logit_score",
            F.lit(-2.5) +                                   # Intercept
            F.lit(0.8) * F.col("amount_normalized") +       # Amount effect
            F.lit(0.6) * F.col("txn_count_normalized") +    # Velocity effect
            F.lit(0.4) * F.abs(F.col("amount_zscore")) +    # Deviation effect
            F.lit(0.5) * F.col("is_unusual_hour") +         # Time effect
            F.lit(0.3) * F.col("is_international") +        # Location effect
            F.lit(0.7) * F.col("amount_x_velocity") +       # Interaction 1
            F.lit(0.5) * F.col("amount_x_deviation") +
# Data Connectivity and I/O Operations
### Program 01: 01_transaction_data_import.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   File I/O: Reads a CSV file containing transaction data.
*   **spark.read operations:**
    *   `spark.read.option("header", "true").schema(schema).csv(filepath)`: Reads a CSV file with a header row and applies a predefined schema.
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   Reads from a file path specified by `INPUT_PATH` and `TRANSACTION_FILE` (e.g., `/data/raw/transactions.csv`).
*   **Data format specifications:**
    *   CSV format.
    *   `header="true"`: Specifies that the first row of the CSV file contains header information.
    *   `schema`: Uses a predefined `TRANSACTION_SCHEMA` (StructType) to enforce data types and structure during the read operation.

### Program 02: 02_data_quality_cleaning.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 03: 03_feature_engineering.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 04: 04_rule_based_detection.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 05: 05_ml_scoring_model.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 06: 06_combine_scores_reporting.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   File I/O: Writes high-risk transactions to a CSV file.
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   `high_risk_transactions.select(...).write.mode("overwrite").option("header", "true").csv(output_file_path)`: Writes a CSV file containing high-risk transaction data.
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   Writes to a file path specified by `REPORT_PATH` (e.g., `/output/reports/high_risk_transactions_YYYYMMDD_HHMMSS.csv`).
*   **Data format specifications:**
    *   CSV format.
    *   `header="true"`: Writes a header row to the CSV file.


# Execution Flow and Dependencies
### List of PySpark programs analyzed

*   Fraud detection pipeline

### Sequence in which transformations and actions are executed, along with the description

1.  **Initialization**:
    *   `create_spark_session()`: Initializes a SparkSession with configurations for the application.
2.  **Data Import and Validation (01_transaction\_data\_import.sas)**:
    *   `import_transactions()`: Reads transaction data from a CSV file ( `/data/raw/transactions.csv` ) based on the defined schema.
    *   `validate_transactions()`: Validates the imported data by checking for missing values and invalid amounts. Filters out invalid records based on `validation_status`.
        *   Action: `count()` is triggered twice to get the initial and validated record counts.
3.  **Data Cleaning and Preprocessing (02\_data\_quality\_cleaning.sas)**:
    *   `clean_transactions()`: Cleans and standardizes the transaction data. This includes:
        *   Standardizing `transaction_type`, `merchant_name`, and `country_code`.
        *   Handling missing amounts and converting date and time columns to appropriate formats.
    *   `remove_duplicates()`: Removes duplicate records based on specified key columns.
    *   `handle_outliers()`: Handles outliers in the `amount` column using Winsorization.
        *   Action: `approxQuantile()` is triggered to calculate percentiles.
        *   Action: `count()` is triggered to get the record count after outlier handling (implicitly as part of the filter operation).
4.  **Feature Engineering (03\_feature\_engineering.sas)**:
    *   `calculate_velocity_features()`: Calculates velocity features (transaction counts and amounts within a rolling window) and days since the last transaction for each customer.
    *   `calculate_amount_deviation()`: Calculates amount deviation features (average amount, standard deviation, Z-score, and percentage deviation) for each customer.
    *   `create_time_features()`: Creates time-based features from the transaction date and time.
    *   `create_location_features()`: Creates location-based features.
        *   Action: `count()` is triggered within the feature engineering functions (indirectly, as part of the `groupBy().agg()` operations).
5.  **Caching**:
    *   `transactions_df.cache()`: Caches the DataFrame in memory for faster access.
    *   `transactions_df.count()`: Triggers the caching operation.
6.  **Rule-Based Fraud Detection (04\_rule\_based\_detection.sas)**:
    *   `apply_fraud_rules()`: Applies rule-based fraud detection logic and calculates a rule score.
    *   `generate_rule_alerts()`: Generates alerts based on the rule score.
        *   Action: `count()` is triggered to count the total transactions and the number of alerts.
        *   Action: `show()` is triggered to display the risk level counts.
    *   `rule_summary_report()`: Creates a summary report of rule triggers.
        *   Action: `show()` is triggered to display the rule trigger summary.
7.  **ML-Based Fraud Scoring (05\_ml\_scoring\_model.sas)**:
    *   `prepare_ml_data()`: Prepares the data for ML scoring by creating binary flags, normalizing continuous variables, and creating interaction features.
    *   `calculate_ml_score()`: Calculates an ML-based fraud score using a simulated logistic regression model.
8.  **Combining Scores and Reporting (06\_combine\_scores\_reporting.sas)**:
    *   `combine_scores()`: Combines rule-based and ML-based scores to derive a final fraud assessment.
    *   `generate_final_report()`: Generates a final fraud detection report, including summary statistics and saving high-risk transactions.
        *   Action: `count()` is triggered to get the total and high-risk transaction counts.
        *   Action: `show()` is triggered to display the risk level and recommendation summaries.
        *   Action: `write.csv()` is triggered to save high-risk transactions to a CSV file.
9.  **Saving Processed Data (Optional)**:
    *   `transactions_df.write.parquet()`: Saves the fully processed DataFrame to a Parquet file.

### DataFrame dependencies (which operations depend on outputs from prior transformations)

*   `validate_transactions()` depends on the output of `import_transactions()`.
*   `clean_transactions()`, `remove_duplicates()`, and `handle_outliers()` depend on the output of `validate_transactions()`.
*   The feature engineering functions (`calculate_velocity_features()`, `calculate_amount_deviation()`, `create_time_features()`, and `create_location_features()`) depend on the output of `handle_outliers()`.
*   `apply_fraud_rules()` depends on the output of the feature engineering functions.
*   `generate_rule_alerts()` and `rule_summary_report()` depend on the output of `apply_fraud_rules()`.
*   `prepare_ml_data()` and `calculate_ml_score()` depend on the output of the feature engineering functions.
*   `combine_scores()` depends on the outputs of `apply_fraud_rules()` and `calculate_ml_score()`.
*   `generate_final_report()` depends on the output of `combine_scores()`.
*   Saving the fully processed data depends on the output of `combine_scores()`.

### Function/pipeline execution order (if applicable)

The functions are executed in the order they are called within the `main()` function, following the sequence described above.

### Action trigger points (collect, show, write, count, take)

*   `count()`: Used extensively to get counts of records at various stages (validation, outlier handling, alert generation, and final reporting) and to trigger caching.
*   `show()`: Used to display the risk level counts and rule trigger summaries.
*   `write.csv()`: Used to save high-risk transactions to a CSV file.
*   `write.parquet()`: Used to save the fully processed data to a Parquet file.
*   `approxQuantile()`: Used to calculate percentiles for outlier handling.

### List of use cases addressed by all the programs together

*   **Fraud Detection:** The primary use case is to detect fraudulent transactions using a combination of rule-based and ML-based approaches.
*   **Data Import and Validation:** Importing transaction data from a CSV file and validating its integrity by checking for missing values and invalid amounts.
*   **Data Cleaning and Standardization:** Cleaning and standardizing transaction data, including handling missing values, standardizing transaction types, merchant names, and country codes, and converting data types.
*   **Duplicate Removal:** Removing duplicate records from the transaction data.
*   **Outlier Handling:** Handling outliers in transaction amounts using Winsorization.
*   **Feature Engineering:** Creating various features from transaction data, including:
    *   Velocity features (transaction counts and amounts within a rolling window).
    *   Amount deviation features (average amount, standard deviation, Z-score, and percentage deviation).
    *   Time-based features (hour of day, day of week, day of month, month, time of day categories, weekend flag, and unusual hour flag).
    *   Location-based features (country transaction counts, rare country flag, and international transaction flag).
*   **Rule-Based Fraud Detection:** Applying rule-based fraud detection logic based on the engineered features.
*   **ML-Based Fraud Scoring:** Calculating an ML-based fraud score using a simulated logistic regression model.
*   **Score Combination:** Combining rule-based and ML-based scores to derive a final fraud assessment.
*   **Reporting and Alerting:** Generating a final fraud detection report, including summary statistics, alert generation, and saving high-risk transactions.
*   **Data Storage:** Saving processed data to a Parquet file.

# Error Handling and Logging
### Analysis of the PySpark Program

This PySpark program implements a fraud detection pipeline. It includes data import, cleaning, feature engineering, rule-based detection, ML scoring (simulated), score combination, and reporting. The program incorporates several error handling and logging mechanisms.

#### Error Checking Mechanisms

*   **`try...except` blocks:** The `import_transactions` function uses a `try...except` block to catch potential exceptions during CSV file reading. This is crucial for handling file I/O errors, schema mismatches, and other import-related issues. The `generate_final_report` function also has a try-except block to handle potential errors during saving of high-risk transactions.
*   **`sys.exit(1)`:**  In the `import_transactions` function, upon encountering an error, the program calls `sys.exit(1)`. This is a way to terminate the entire PySpark application if the data import fails, mimicking the behavior of SAS's `%ABORT`.
*   **Data Validation:** The `validate_transactions` function checks for missing values (`NULL`) in key columns (transaction\_id, customer\_id, amount, transaction\_date) and filters out invalid records. The `amount` is also checked to be greater than zero.
*   **`if __name__ == "__main__":`:** This standard Python construct ensures that the `main()` function is executed only when the script is run directly, not when it's imported as a module.

#### Logging Statements

*   **`logging.basicConfig`:** Configures basic logging with a specified level (INFO) and format.
*   **`logger.info()`:** Used extensively to log informational messages about the pipeline's progress, such as initialization, function starts and completions, data counts, and file paths.
*   **`logger.error()`:** Used to log error messages, including the specific error message and, in some cases, the exception details (using `exc_info=True`) to provide a detailed stack trace. This is crucial for debugging.
*   **Comments:** The code includes comments to explain the purpose of each function, the mapping to corresponding SAS macros, and the logic implemented.

#### DataFrame Validation

*   **`validate_transactions` Function:** Performs explicit validation by checking for missing values using `F.col("column_name").isNull()` and invalid amounts (`amount <= 0`). Invalid records are filtered out.
*   **Schema Enforcement:** The `import_transactions` function uses a predefined `TRANSACTION_SCHEMA` to read the CSV data. This enforces the expected data types and helps prevent schema inference issues.
*   **Count Validation:** The program logs the total record count before and after data validation and duplicate removal. This helps in monitoring data loss due to cleaning or filtering.

#### Exception Handling in Transformations and Actions

*   **`try...except` blocks:** The `import_transactions` and `generate_final_report` functions use `try...except` blocks to handle potential exceptions during CSV reading and writing, respectively.
*   **Error Propagation:** The `sys.exit(1)` in `import_transactions` ensures that the entire job fails if the initial data import fails, preventing downstream processing with potentially corrupted or incomplete data.
*   **Catch-all Exception in `main()`:** The `main()` function has a top-level `try...except` block with `exc_info=True`. This is a crucial catch-all to handle any unhandled exceptions during the pipeline's execution and print the stack trace for debugging.

#### Error Output Handling

*   **Error Logging:**  All errors are logged using `logger.error()`, including the exception message.
*   **Failure and Exit:** The `sys.exit(1)` in `import_transactions` causes the program to exit on import failure.
*   **Saving High-Risk Transactions:** The `generate_final_report` function saves high-risk transactions to a separate CSV file. This provides a mechanism to isolate and examine potentially fraudulent records.

#### Spark Job Failure Conditions and Retry Logic

*   **`sys.exit(1)`:** The use of `sys.exit(1)` is a rudimentary form of failure handling, causing the entire Spark application to terminate on critical errors like import failures.  This is a basic form of failure handling.
*   **No Explicit Retry Logic:** The provided code does not include explicit retry mechanisms (e.g., retrying failed operations). In a production environment, you would typically implement retry logic using frameworks like Apache Airflow or custom retry mechanisms to handle transient failures.
*   **SparkSession Management:** The `finally` block in the `main()` function ensures that the `SparkSession` is stopped, even if an exception occurs. This releases resources and prevents resource leaks.

