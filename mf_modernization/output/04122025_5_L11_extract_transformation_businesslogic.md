```markdown
### Analysis of the PySpark Program: Fraud Detection Pipeline

This PySpark program implements a fraud detection pipeline. The pipeline ingests transaction data, performs data quality checks, cleans and transforms the data, engineers features, applies rule-based and ML-based fraud detection, combines the scores, and generates a final report.

#### **01_transaction_data_import.sas**

1.  **Transformations:**
    *   `import_transactions(spark: SparkSession, filepath: str, schema: T.StructType) -> T.DataFrame`:
        *   `spark.read.option("header", "true").schema(schema).csv(filepath)`: Reads the CSV file from the specified filepath, using the provided schema and considering the first row as the header.
    *   `validate_transactions(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("validation_status", ...)`: Adds a new column "validation\_status" based on the following conditional logic.
            *   `F.when(F.col("transaction_id").isNull(), F.lit("MISSING_ID"))`: If "transaction\_id" is null, set "validation\_status" to "MISSING\_ID".
            *   `F.when(F.col("customer_id").isNull(), F.lit("MISSING_CUSTOMER"))`: If "customer\_id" is null, set "validation\_status" to "MISSING\_CUSTOMER".
            *   `F.when(F.col("amount").isNull(), F.lit("MISSING_AMOUNT"))`: If "amount" is null, set "validation\_status" to "MISSING\_AMOUNT".
            *   `F.when(F.col("transaction_date").isNull(), F.lit("MISSING_DATE"))`: If "transaction\_date" is null, set "validation\_status" to "MISSING\_DATE".
            *   `F.when(F.col("amount") <= 0, F.lit("INVALID_AMOUNT"))`: If "amount" is less than or equal to 0, set "validation\_status" to "INVALID\_AMOUNT".
            *   `otherwise(F.lit("VALID"))`: Otherwise, set "validation\_status" to "VALID".
        *   `filter(F.col("validation_status") == "VALID")`: Filters the DataFrame, keeping only the rows where "validation\_status" is "VALID".

2.  **Business Rules:**
    *   Transactions with missing transaction IDs, customer IDs, amounts, or transaction dates are considered invalid.
    *   Transactions with amounts less than or equal to 0 are considered invalid.

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used to create the "validation\_status" column, based on different conditions related to missing values and the amount.
    *   `.filter()` is used to keep only valid transactions based on the "validation\_status".

4.  **Aggregations and groupBy operations:**
    *   None

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   None

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used to create "validation\_status"

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   `isNull()` is used to check for missing values in transaction\_id, customer\_id, amount and transaction\_date.
    *   `filter()` is used to remove invalid transactions based on the validation status.

#### **02_data_quality_cleaning.sas**

1.  **Transformations:**
    *   `clean_transactions(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("transaction_type_clean", F.upper(F.trim(F.col("transaction_type"))))`: Creates a new column "transaction\_type\_clean" by converting "transaction\_type" to uppercase and removing leading/trailing spaces.
        *   `withColumn("merchant_name_clean", F.initcap(F.trim(F.col("merchant_name"))))`: Creates a new column "merchant\_name\_clean" by capitalizing the first letter of each word in "merchant\_name" and removing leading/trailing spaces.
        *   `withColumn("country_code_clean", F.upper(F.substring(F.col("country_code"), 1, 2)))`: Creates a new column "country\_code\_clean" by extracting the first two characters of "country\_code" and converting them to uppercase.
        *   `withColumn("amount", F.coalesce(F.col("amount"), F.lit(0)))`: Replaces null values in the "amount" column with 0.
        *   `withColumn("transaction_date_sas", F.to_date(F.col("transaction_date"), "yyyy-MM-dd"))`: Converts the "transaction\_date" string to a date format.
        *   `withColumn("transaction_datetime", F.to_timestamp(F.concat_ws(" ", F.col("transaction_date"), F.col("transaction_time")), "yyyy-MM-dd HH:mm:ss"))`: Creates a "transaction\_datetime" column by combining the "transaction\_date" and "transaction\_time" columns and converting them to a timestamp format.
    *   `remove_duplicates(df: T.DataFrame, key_cols: list) -> T.DataFrame`:
        *   `.dropDuplicates(key_cols)`: Removes duplicate rows based on the specified key columns.
    *   `handle_outliers(df: T.DataFrame, var_col: str, method: str = "WINSORIZE") -> T.DataFrame`:
        *   `approxQuantile(var_col, [0.01, 0.99], 0.01)`: Calculates the 1st and 99th percentiles of the specified variable.
        *   `withColumn(var_col, ...)`: Applies Winsorization, replacing values less than the 1st percentile with the 1st percentile and values greater than the 99th percentile with the 99th percentile, if the method is "WINSORIZE".
            *   `F.when(F.col(var_col) < p1_value, p1_value)`: If the value in the specified column is less than the 1st percentile, it is replaced by the 1st percentile.
            *   `F.when(F.col(var_col) > p99_value, p99_value)`: If the value in the specified column is greater than the 99th percentile, it is replaced by the 99th percentile.
            *   `otherwise(F.col(var_col))`: Otherwise, keeps the original value.
        *   `filter((F.col(var_col) >= p1_value) & (F.col(var_col) <= p99_value))`: Removes rows where the value of the specified column is outside the range defined by the 1st and 99th percentiles, if the method is "REMOVE".

2.  **Business Rules:**
    *   Standardize transaction type and merchant name.
    *   Standardize country codes.
    *   Handle missing amounts by replacing them with 0.
    *   Convert date and time strings to appropriate data types.
    *   Remove duplicate transactions based on specified key columns.
    *   Handle outliers in the amount by either winsorizing or removing them.

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used in the `handle_outliers` function for Winsorization.
    *   `.filter()` is used in the `handle_outliers` function for removing outliers.

4.  **Aggregations and groupBy operations:**
    *   `approxQuantile()` is used to calculate percentiles, used as part of outlier detection.

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   None

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used extensively for cleaning and standardizing data, converting data types, and handling outliers.
    *   `F.upper()`, `F.trim()`, `F.initcap()`, `F.substring()`, `F.coalesce()`, `F.to_date()`, `F.to_timestamp()` are used for cleaning and standardizing the data.

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   `F.coalesce()` is used to handle missing values by replacing them with a default value (0).

#### **03_feature_engineering.sas**

1.  **Transformations:**
    *   `calculate_velocity_features(df: T.DataFrame, window_days: int = 7) -> T.DataFrame`:
        *   `Window.partitionBy("customer_id").orderBy("transaction_datetime")`: Defines a window specification to order transactions by transaction datetime within each customer.
        *   `withColumn("prev_transaction_date_sas", F.lag("transaction_date_sas", 1).over(window_spec_customer))`: Calculates the previous transaction date for each customer using the `lag` window function.
        *   `withColumn("days_since_last_txn", ...)`: Calculates the number of days since the last transaction.
            *   `F.when(F.col("prev_transaction_date_sas").isNotNull(), F.datediff(F.col("transaction_date_sas"), F.col("prev_transaction_date_sas"))).otherwise(None)`: Uses `datediff` to calculate the difference between the current and previous transaction dates, handling the first transaction (where there is no previous transaction) by setting the value to `None`.
        *   `Window.partitionBy("customer_id").orderBy("transaction_datetime").rangeBetween(-F.expr(f"INTERVAL {window_days} DAYS"), 0)`: Defines a rolling window for calculating velocity features.
        *   `withColumn(f"txn_count_{window_days}d", F.count("transaction_id").over(window_spec_rolling))`: Calculates the count of transactions within the rolling window.
        *   `withColumn(f"txn_amount_{window_days}d", F.sum("amount").over(window_spec_rolling))`: Calculates the sum of transaction amounts within the rolling window.
        *   `withColumn(f"avg_txn_amount_{window_days}d", F.avg("amount").over(window_spec_rolling))`: Calculates the average transaction amount within the rolling window.
        *   `withColumn(f"txn_count_{window_days}d", F.coalesce(F.col(f"txn_count_{window_days}d"), F.lit(0)))`: Handles null values that can be produced by window functions for the first records by replacing them with 0.
        *   `withColumn(f"txn_amount_{window_days}d", F.coalesce(F.col(f"txn_amount_{window_days}d"), F.lit(0.0)))`: Handles null values that can be produced by window functions for the first records by replacing them with 0.0.
        *   `withColumn(f"avg_txn_amount_{window_days}d", F.coalesce(F.col(f"avg_txn_amount_{window_days}d"), F.lit(0.0)))`: Handles null values that can be produced by window functions for the first records by replacing them with 0.0.
    *   `calculate_amount_deviation(df: T.DataFrame) -> T.DataFrame`:
        *   `groupBy("customer_id").agg(F.avg("amount").alias("customer_avg_amount"), F.stddev("amount").alias("customer_std_amount"), F.count("transaction_id").alias("customer_txn_count"))`: Calculates the average amount, standard deviation of amount, and the number of transactions for each customer using `groupBy` and `agg`.
        *   `.join(F.broadcast(customer_stats_df), on="customer_id", how="left")`: Joins the calculated customer statistics with the original DataFrame using a left join.  The `broadcast` hint is used to optimize the join if the customer statistics are small.
        *   `withColumn("amount_zscore", ...)`: Calculates the Z-score for the transaction amount.
            *   `F.when(F.col("customer_std_amount") > 0, (F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_std_amount")).otherwise(0.0)`: Calculates the Z-score only if the standard deviation is greater than 0, otherwise sets the Z-score to 0.
        *   `withColumn("amount_pct_deviation", ...)`: Calculates the percentage deviation of the transaction amount from the customer's average amount.
            *   `F.when(F.col("customer_avg_amount") > 0, ((F.col("amount") - F.col("customer_avg_amount")) / F.col("customer_avg_amount")) * 100).otherwise(0.0)`: Calculates the percentage deviation only if the average amount is greater than 0, otherwise sets the percentage deviation to 0.
        *   `withColumn("customer_avg_amount", F.coalesce(F.col("customer_avg_amount"), F.lit(0.0)))`: Handles null values that can be produced by the join for new customers by replacing them with 0.0.
        *   `withColumn("customer_std_amount", F.coalesce(F.col("customer_std_amount"), F.lit(0.0)))`: Handles null values that can be produced by the join for new customers by replacing them with 0.0.
        *   `withColumn("customer_txn_count", F.coalesce(F.col("customer_txn_count"), F.lit(0)))`: Handles null values that can be produced by the join for new customers by replacing them with 0.
    *   `create_time_features(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("txn_hour", F.hour(F.col("transaction_datetime")))`: Extracts the hour from the transaction datetime.
        *   `withColumn("txn_day_of_week", F.dayofweek(F.col("transaction_date_sas")))`: Extracts the day of the week from the transaction date.
        *   `withColumn("txn_day_of_month", F.dayofmonth(F.col("transaction_date_sas")))`: Extracts the day of the month from the transaction date.
        *   `withColumn("txn_month", F.month(F.col("transaction_date_sas")))`: Extracts the month from the transaction date.
        *   `withColumn("time_of_day", ...)`: Creates a "time\_of\_day" category based on the transaction hour.
            *   `F.when((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6), F.lit("NIGHT"))`: If the hour is between 0 and 5, set time\_of\_day to "NIGHT".
            *   `F.when((F.col("txn_hour") >= 6) & (F.col("txn_hour") < 12), F.lit("MORNING"))`: If the hour is between 6 and 11, set time\_of\_day to "MORNING".
            *   `F.when((F.col("txn_hour") >= 12) & (F.col("txn_hour") < 18), F.lit("AFTERNOON"))`: If the hour is between 12 and 17, set time\_of\_day to "AFTERNOON".
            *   `otherwise(F.lit("EVENING"))`: Otherwise, set time\_of\_day to "EVENING".
        *   `withColumn("is_weekend", F.col("txn_day_of_week").isin([1, 7]).cast(T.IntegerType()))`: Creates an "is\_weekend" flag based on the day of the week (1 for Sunday, 7 for Saturday).
        *   `withColumn("is_unusual_hour", ((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6)).cast(T.IntegerType()))`: Creates an "is\_unusual\_hour" flag based on the transaction hour (0-5 considered unusual).
    *   `create_location_features(df: T.DataFrame) -> T.DataFrame`:
        *   `groupBy("country_code_clean").agg(F.count("transaction_id").alias("country_txn_count"))`: Calculates the number of transactions for each country using `groupBy` and `agg`.
        *   `.join(F.broadcast(country_counts_df), on="country_code_clean", how="left")`: Joins the country counts with the original DataFrame using a left join.  The `broadcast` hint is used to optimize the join if the country counts are small.
        *   `withColumn("is_rare_country", F.when(F.col("country_txn_count") < 10, 1).otherwise(0))`: Creates an "is\_rare\_country" flag based on the number of transactions per country.
        *   `withColumn("is_international", (F.col("country_code_clean") != "US").cast(T.IntegerType()))`: Creates an "is\_international" flag based on whether the country code is not "US".
        *   `withColumn("country_txn_count", F.coalesce(F.col("country_txn_count"), F.lit(0)))`: Handles null values that can be produced by the join by replacing them with 0.

2.  **Business Rules:**
    *   Calculate velocity features (transaction counts and amounts within a rolling window).
    *   Calculate days since the last transaction.
    *   Calculate amount deviation features (average amount, standard deviation, Z-score, and percentage deviation).
    *   Create time-based features (hour, day of week, day of month, month, time of day, weekend flag, unusual hour flag).
    *   Create location-based features (transaction count per country, rare country flag, international flag).

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used to categorize the "time\_of\_day" and create the "is\_rare\_country" and "is\_international" flags.

4.  **Aggregations and groupBy operations:**
    *   `groupBy().agg()` is used to calculate customer statistics in `calculate_amount_deviation`.
    *   `groupBy().agg()` is used to calculate country transaction counts in `create_location_features`.
    *   `F.count()`, `F.sum()`, and `F.avg()` are used with `over()` for rolling window calculations in `calculate_velocity_features`.

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   `Window.partitionBy("customer_id").orderBy("transaction_datetime")` is used to define the window for calculating `days_since_last_txn` and in `calculate_amount_deviation`.
    *   `F.lag()` is used to calculate `prev_transaction_date_sas` and calculate `days_since_last_txn`.
    *   `Window.partitionBy("customer_id").orderBy("transaction_datetime").rangeBetween(-F.expr(f"INTERVAL {window_days} DAYS"), 0)` is used to define the rolling window for calculating velocity features.
    *   `F.count()`, `F.sum()`, and `F.avg()` are used with `over()` and the rolling window to calculate velocity features.

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used extensively to create new features.
    *   `F.datediff()` is used to calculate the days since the last transaction.
    *   `F.hour()`, `F.dayofweek()`, `F.dayofmonth()`, `F.month()` are used to extract time-based features.
    *   Arithmetic operations are used to calculate Z-scores and percentage deviations.

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   `F.coalesce()` is used to handle potential null values resulting from joins and window functions.

#### **04_rule_based_detection.sas**

1.  **Transformations:**
    *   `apply_fraud_rules(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("rule_high_velocity", (F.col("txn_count_7d") > 10).cast(T.IntegerType()))`: Creates a rule flag for high velocity based on transactions in the last 7 days.
        *   `withColumn("rule_amount_deviation", (F.abs(F.col("amount_zscore")) > 3).cast(T.IntegerType()))`: Creates a rule flag for large amount deviation based on the Z-score.
        *   `withColumn("rule_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`: Creates a rule flag for high transaction amount.
        *   `withColumn("rule_unusual_hour", (F.col("is_unusual_hour") == 1).cast(T.IntegerType()))`: Creates a rule flag for unusual transaction hour.
        *   `withColumn("rule_international", (F.col("is_international") == 1).cast(T.IntegerType()))`: Creates a rule flag for international transactions.
        *   `withColumn("rule_rare_country", (F.col("is_rare_country") == 1).cast(T.IntegerType()))`: Creates a rule flag for transactions in rare countries.
        *   `withColumn("rule_rapid_succession", (F.col("days_since_last_txn").isNotNull() & (F.col("days_since_last_txn") < 0.042)).cast(T.IntegerType()))`: Creates a rule flag for rapid succession of transactions (within one hour).
        *   `withColumn("rule_round_amount", ((F.col("amount") % 100 == 0) & (F.col("amount") >= 1000)).cast(T.IntegerType()))`: Creates a rule flag for round amounts.
        *   `withColumn("rule_score", ...)`: Calculates the rule score by summing points for each triggered rule.
        *   `withColumn("rule_triggered_array", F.array_remove(F.array(*rule_names), F.lit(None)))`: Creates an array of triggered rule names and removes any `None` values.
        *   `withColumn("rule_triggered", F.concat_ws(", ", F.col("rule_triggered_array")))`: Concatenates the triggered rule names into a single string.
        *   `drop("rule_triggered_array")`: Drops the intermediate array column.
        *   `withColumn("rule_risk_level", ...)`: Assigns a risk level based on the rule score.
            *   `F.when(F.col("rule_score") >= 75, F.lit("CRITICAL"))`: If the rule score is greater than or equal to 75, set the risk level to "CRITICAL".
            *   `F.when(F.col("rule_score") >= 50, F.lit("HIGH"))`: If the rule score is greater than or equal to 50, set the risk level to "HIGH".
            *   `F.when(F.col("rule_score") >= 25, F.lit("MEDIUM"))`: If the rule score is greater than or equal to 25, set the risk level to "MEDIUM".
            *   `otherwise(F.lit("LOW"))`: Otherwise, set the risk level to "LOW".
        *   `withColumn("is_suspicious", (F.col("rule_score") >= 50).cast(T.IntegerType()))`: Creates a flag to indicate if a transaction is suspicious.
    *   `generate_rule_alerts(df: T.DataFrame, threshold: int = 50) -> T.DataFrame`:
        *   `filter(F.col("rule_score") >= threshold)`: Filters the DataFrame to include only transactions with a rule score greater than or equal to the threshold.
        *   `orderBy(F.col("rule_score").desc(), F.col("transaction_date_sas").desc())`: Orders the alerts by rule score in descending order and then by transaction date in descending order.
        *   `groupBy("rule_risk_level").count().orderBy("rule_risk_level")`: Counts the number of alerts for each risk level.
    *   `rule_summary_report(df: T.DataFrame) -> T.DataFrame`:
        *   `groupBy().agg(...)`: Aggregates the rule flags to count the number of times each rule was triggered.
        *   `collect()[0].asDict()`: Collects the results as a dictionary.
        *   `df.sparkSession.createDataFrame(summary_data, schema=summary_schema).orderBy(F.col("trigger_count").desc())`: Converts the dictionary into a DataFrame.

2.  **Business Rules:**
    *   Apply a set of fraud detection rules.
    *   Calculate a rule score based on the triggered rules.
    *   Assign a risk level based on the rule score.
    *   Generate alerts based on the rule score.
    *   Create a rule summary report.

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used to assign the risk level based on the rule score.

4.  **Aggregations and groupBy operations:**
    *   `groupBy().agg()` is used to calculate the rule summary report.
    *   `groupBy().count()` is used to count the number of alerts per risk level.

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   None

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used extensively to create rule flags, calculate the rule score, assign risk levels, and generate the rule triggered string.
    *   Arithmetic operations are used to calculate the rule score.

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   `.filter()` is used to filter out transactions based on the rule score threshold in `generate_rule_alerts`.

#### **05_ml_scoring_model.sas**

1.  **Transformations:**
    *   `prepare_ml_data(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("is_high_amount", (F.col("amount") > 1000).cast(T.IntegerType()))`: Creates a binary flag for high amounts.
        *   `withColumn("is_very_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`: Creates a binary flag for very high amounts.
        *   `withColumn("amount_normalized", F.col("amount") / 10000)`: Normalizes the amount.
        *   `withColumn("txn_count_normalized", F.col("txn_count_7d") / 20)`: Normalizes the transaction count.
        *   `withColumn("amount_zscore", F.coalesce(F.col("amount_zscore"), F.lit(0.0)))`: Handles missing values in amount\_zscore.
        *   `withColumn("days_since_last_txn", F.coalesce(F.col("days_since_last_txn"), F.lit(999.0)))`: Handles missing values in days\_since\_last\_txn.
        *   `withColumn("amount_x_velocity", F.col("amount_normalized") * F.col("txn_count_normalized"))`: Creates an interaction feature between amount and velocity.
        *   `withColumn("amount_x_deviation", F.col("amount_normalized") * F.abs(F.col("amount_zscore")))`: Creates an interaction feature between amount and deviation.
    *   `calculate_ml_score(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("logit_score", ...)`: Calculates the logit score using a linear combination of features.
        *   `withColumn("ml_score_probability", F.lit(1) / (F.lit(1) + F.exp(-F.col("logit_score"))))`: Converts the logit score to a probability using the sigmoid function.
        *   `withColumn("ml_score", (F.col("ml_score_probability") * 100).cast(T.IntegerType()))`: Scales the probability to a score between 0 and 100.
        *   `withColumn("ml_risk_level", ...)`: Assigns a risk level based on the ML score.
            *   `F.when(F.col("ml_score") >= 80, F.lit("CRITICAL"))`: If the ML score is greater than or equal to 80, set the risk level to "CRITICAL".
            *   `F.when(F.col("ml_score") >= 60, F.lit("HIGH"))`: If the ML score is greater than or equal to 60, set the risk level to "HIGH".
            *   `F.when(F.col("ml_score") >= 40, F.lit("MEDIUM"))`: If the ML score is greater than or equal to 40, set the risk level to "MEDIUM".
            *   `otherwise(F.lit("LOW"))`: Otherwise, set the risk level to "LOW".

2.  **Business Rules:**
    *   Create binary flags for amount.
    *   Normalize continuous variables.
    *   Handle missing values.
    *   Create interaction features.
    *   Calculate an ML-based fraud score using a simulated logistic regression model.
    *   Assign an ML-based risk level.

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used to assign the ML risk level.

4.  **Aggregations and groupBy operations:**
    *   None

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   None

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used extensively to create features, calculate the logit score, convert to a probability, scale the score, and assign risk levels.
    *   Arithmetic operations are used for normalization, interaction feature calculation, and the logit score calculation.
    *   `F.exp()` is used to calculate the exponential function for the sigmoid.

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   `F.coalesce()` is used to handle missing values.

#### **06_combine_scores_reporting.sas**

1.  **Transformations:**
    *   `combine_scores(df: T.DataFrame) -> T.DataFrame`:
        *   `withColumn("final_fraud_score", (F.col("rule_score") * 0.4) + (F.col("ml_score") * 0.6))`: Calculates the final fraud score as a weighted average of the rule score and the ML score.
        *   `withColumn("final_risk_level", ...)`: Assigns a final risk level based on the final fraud score.
            *   `F.when(F.col("final_fraud_score") >= 70, F.lit("CRITICAL"))`: If the final fraud score is greater than or equal to 70, set the final risk level to "CRITICAL".
            *   `F.when(F.col("final_fraud_score") >= 50, F.lit("HIGH"))`: If the final fraud score is greater than or equal to 50, set the final risk level to "HIGH".
            *   `F.when(F.col("final_fraud_score") >= 30, F.lit("MEDIUM"))`: If the final fraud score is greater than or equal to 30, set the final risk level to "MEDIUM".
            *   `otherwise(F.lit("LOW"))`: Otherwise, set the final risk level to "LOW".
        *   `withColumn("final_recommendation", ...)`: Assigns a final recommendation based on the final fraud score.
            *   `F.when(F.col("final_fraud_score") >= 50, F.lit("INVESTIGATE"))`: If the final fraud score is greater than or equal to 50, set the recommendation to "INVESTIGATE".
            *   `F.when(F.col("final_fraud_score") >= 30, F.lit("MONITOR"))`: If the final fraud score is greater than or equal to 30, set the recommendation to "MONITOR".
            *   `otherwise(F.lit("APPROVE"))`: Otherwise, set the recommendation to "APPROVE".
    *   `generate_final_report(df: T.DataFrame, output_path: str) -> None`:
        *   `filter(F.col("final_risk_level").isin(["CRITICAL", "HIGH"]))`: Filters the DataFrame to include only high-risk transactions.
        *   `groupBy("final_risk_level").count().orderBy("final_risk_level")`: Counts the number of transactions for each final risk level.
        *   `groupBy("final_recommendation").count().orderBy("final_recommendation")`: Counts the number of transactions for each final recommendation.
        *   `select(...)`: Selects relevant columns for the final report.
        *   `.write.mode("overwrite").option("header", "true").csv(output_file_path)`: Writes the high-risk transactions to a CSV file.

2.  **Business Rules:**
    *   Combine the rule-based and ML-based scores.
    *   Assign a final risk level based on the combined score.
    *   Generate a final recommendation.
    *   Generate a final fraud detection report.

3.  **Conditional Logic:**
    *   `F.when().otherwise()` is used to assign the final risk level and final recommendation.

4.  **Aggregations and groupBy operations:**
    *   `groupBy().count()` is used to generate the final risk level and recommendation distributions.

5.  **Window functions (over, partitionBy, orderBy, row_number, rank, lag, lead):**
    *   None

6.  **Key calculations and column transformations (withColumn, expr):**
    *   `withColumn` is used to calculate the final fraud score, assign the final risk level, and generate the final recommendation.
    *   Arithmetic operations are used for calculating the final fraud score.

7.  **Data validation and quality checks (filter, isNull, isNotNull):**
    *   None
