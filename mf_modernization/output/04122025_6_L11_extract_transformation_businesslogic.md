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