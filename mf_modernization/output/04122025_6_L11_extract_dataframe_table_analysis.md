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
