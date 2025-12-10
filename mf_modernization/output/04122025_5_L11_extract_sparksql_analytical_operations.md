### PySpark Program Analysis

This PySpark program implements a fraud detection pipeline, mirroring the functionality of SAS programs. It imports, validates, cleans, and transforms transaction data, applies rule-based and machine learning (ML) scoring, and generates a final report.

#### Spark SQL queries and descriptions

1.  **`spark.read.option("header", "true").schema(schema).csv(filepath)`**
    *   **Description:** Reads a CSV file from the specified `filepath` into a Spark DataFrame. It uses the provided `schema` to define the data types of the columns and includes the header row.
    *   **Business Application:** Imports raw transaction data for the fraud detection process.

2.  **`df.withColumn("validation_status", F.when(...).when(...).when(...).otherwise(...))`**
    *   **Description:** Creates a new column "validation\_status" based on conditional checks for missing or invalid data. Uses `F.when()` and `F.otherwise()` to assign status values.
    *   **Business Application:** Validates transaction data, flagging records with missing or invalid values.

3.  **`df.filter(F.col("validation_status") == "VALID")`**
    *   **Description:** Filters the DataFrame to keep only records where the "validation\_status" is "VALID".
    *   **Business Application:** Removes invalid transaction records from the dataset.

4.  **`df.withColumn("transaction_type_clean", F.upper(F.trim(F.col("transaction_type"))))`**
    *   **Description:** Creates a new column "transaction\_type\_clean" by converting the "transaction\_type" column to uppercase and trimming leading/trailing spaces.
    *   **Business Application:** Standardizes transaction types for consistency.

5.  **`df.withColumn("merchant_name_clean", F.initcap(F.trim(F.col("merchant_name"))))`**
    *   **Description:** Creates a new column "merchant\_name\_clean" by capitalizing the first letter of each word in the "merchant\_name" column and trimming spaces.
    *   **Business Application:** Standardizes merchant names for consistency.

6.  **`df.withColumn("country_code_clean", F.upper(F.substring(F.col("country_code"), 1, 2)))`**
    *   **Description:** Creates a new column "country\_code\_clean" by converting the first two characters of the "country\_code" column to uppercase.
    *   **Business Application:** Standardizes country codes for consistency.

7.  **`df.withColumn("amount", F.coalesce(F.col("amount"), F.lit(0)))`**
    *   **Description:** Replaces null values in the "amount" column with 0.
    *   **Business Application:** Handles missing amount values.

8.  **`df.withColumn("transaction_date_sas", F.to_date(F.col("transaction_date"), "yyyy-MM-dd"))`**
    *   **Description:** Converts the "transaction\_date" column (string) to a date format using the specified date format.
    *   **Business Application:** Converts date strings to date objects for date-based calculations.

9.  **`df.withColumn("transaction_datetime", F.to_timestamp(F.concat_ws(" ", F.col("transaction_date"), F.col("transaction_time")), "yyyy-MM-dd HH:mm:ss"))`**
    *   **Description:** Creates a "transaction\_datetime" column by combining the "transaction\_date" and "transaction\_time" columns into a timestamp format.
    *   **Business Application:** Creates a datetime object for time-based calculations.

10. **`df.dropDuplicates(key_cols)`**
    *   **Description:** Removes duplicate rows from the DataFrame based on the columns specified in `key_cols`.
    *   **Business Application:** Removes duplicate transaction records.

11. **`df.approxQuantile(var_col, [0.01, 0.99], 0.01)`**
    *   **Description:** Calculates the 1st and 99th percentiles of the specified variable (`var_col`).
    *   **Business Application:** Identifies and handles outliers in the data.

12. **`df.withColumn(var_col, F.when(...).when(...).otherwise(...))`**
    *   **Description:** Applies Winsorization to the specified variable (`var_col`). Values below the 1st percentile are set to the 1st percentile, and values above the 99th percentile are set to the 99th percentile.
    *   **Business Application:** Handles outliers by capping extreme values.

13. **`df.filter((F.col(var_col) >= p1_value) & (F.col(var_col) <= p99_value))`**
    *   **Description:** Removes outliers from the specified variable (`var_col`) by filtering out values outside the range defined by the 1st and 99th percentiles.
    *   **Business Application:** Handles outliers by removing extreme values.

14. **`df.withColumn("prev_transaction_date_sas", F.lag("transaction_date_sas", 1).over(window_spec_customer))`**
    *   **Description:** Creates a new column "prev\_transaction\_date\_sas" containing the previous transaction date for each customer, using a window specification to partition by customer and order by transaction timestamp.
    *   **Business Application:** Calculates the date of the previous transaction for each customer.

15. **`df.withColumn("days_since_last_txn", F.when(...).otherwise(None))`**
    *   **Description:** Calculates the number of days since the last transaction for each customer using `F.datediff()`.
    *   **Business Application:** Calculates the time elapsed since the last transaction for each customer.

16. **`df.withColumn(f"txn_count_{window_days}d", F.count("transaction_id").over(window_spec_rolling))`**
    *   **Description:** Calculates the count of transactions within a rolling window of `window_days` for each customer.
    *   **Business Application:** Calculates transaction velocity (number of transactions).

17. **`df.withColumn(f"txn_amount_{window_days}d", F.sum("amount").over(window_spec_rolling))`**
    *   **Description:** Calculates the sum of transaction amounts within a rolling window of `window_days` for each customer.
    *   **Business Application:** Calculates the total transaction amount within the rolling window.

18. **`df.withColumn(f"avg_txn_amount_{window_days}d", F.avg("amount").over(window_spec_rolling))`**
    *   **Description:** Calculates the average transaction amount within a rolling window of `window_days` for each customer.
    *   **Business Application:** Calculates the average transaction amount within the rolling window.

19. **`df.groupBy("customer_id").agg(F.avg("amount").alias("customer_avg_amount"), F.stddev("amount").alias("customer_std_amount"), F.count("transaction_id").alias("customer_txn_count"))`**
    *   **Description:** Calculates the average amount, standard deviation of amount, and transaction count for each customer.
    *   **Business Application:** Calculates customer-level statistics for deviation analysis.

20. **`df.join(F.broadcast(customer_stats_df), on="customer_id", how="left")`**
    *   **Description:** Joins the customer statistics DataFrame (`customer_stats_df`) with the main DataFrame on "customer\_id" using a left join. Uses `F.broadcast()` to optimize the join if `customer_stats_df` is small.
    *   **Business Application:** Combines customer-level statistics with transaction data.

21. **`df.withColumn("amount_zscore", F.when(...).otherwise(0.0))`**
    *   **Description:** Calculates the Z-score for the transaction amount, using the customer's average and standard deviation of transaction amounts.
    *   **Business Application:** Calculates a Z-score to identify transactions that deviate from the customer's norm.

22. **`df.withColumn("amount_pct_deviation", F.when(...).otherwise(0.0))`**
    *   **Description:** Calculates the percentage deviation of the transaction amount from the customer's average transaction amount.
    *   **Business Application:** Calculates the percentage deviation of the transaction amount.

23. **`df.withColumn("txn_hour", F.hour(F.col("transaction_datetime")))`**
    *   **Description:** Extracts the hour from the "transaction\_datetime" column.
    *   **Business Application:** Extracts the hour of the day from the transaction timestamp.

24. **`df.withColumn("txn_day_of_week", F.dayofweek(F.col("transaction_date_sas")))`**
    *   **Description:** Extracts the day of the week from the "transaction\_date\_sas" column.
    *   **Business Application:** Extracts the day of the week from the transaction date.

25. **`df.withColumn("txn_day_of_month", F.dayofmonth(F.col("transaction_date_sas")))`**
    *   **Description:** Extracts the day of the month from the "transaction\_date\_sas" column.
    *   **Business Application:** Extracts the day of the month from the transaction date.

26. **`df.withColumn("txn_month", F.month(F.col("transaction_date_sas")))`**
    *   **Description:** Extracts the month from the "transaction\_date\_sas" column.
    *   **Business Application:** Extracts the month from the transaction date.

27. **`df.withColumn("time_of_day", F.when(...).when(...).when(...).otherwise(...))`**
    *   **Description:** Categorizes the transaction time into time-of-day buckets (NIGHT, MORNING, AFTERNOON, EVENING).
    *   **Business Application:** Categorizes transactions based on the time of day.

28.  **`df.withColumn("is_weekend", F.col("txn_day_of_week").isin([1, 7]).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "is\_weekend" indicating whether the transaction occurred on a weekend.
    *   **Business Application:** Flags transactions that occurred on weekends.

29.  **`df.withColumn("is_unusual_hour", ((F.col("txn_hour") >= 0) & (F.col("txn_hour") < 6)).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "is\_unusual\_hour" indicating whether the transaction occurred during unusual hours (0-6 AM).
    *   **Business Application:** Flags transactions that occurred during unusual hours.

30. **`df.groupBy("country_code_clean").agg(F.count("transaction_id").alias("country_txn_count"))`**
    *   **Description:** Counts the number of transactions for each country code.
    *   **Business Application:** Calculates transaction counts by country.

31. **`df.join(F.broadcast(country_counts_df), on="country_code_clean", how="left")`**
    *   **Description:** Joins the country counts DataFrame with the main DataFrame on "country\_code\_clean" using a left join. Uses `F.broadcast()` for efficiency.
    *   **Business Application:** Combines country-level transaction counts with transaction data.

32.  **`df.withColumn("is_rare_country", F.when(...).otherwise(0))`**
    *   **Description:** Creates a binary flag "is\_rare\_country" indicating whether a transaction occurred in a country with fewer than 10 transactions.
    *   **Business Application:** Flags transactions that occurred in rare countries.

33.  **`df.withColumn("is_international", (F.col("country_code_clean") != "US").cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "is\_international" indicating whether a transaction occurred in a country other than "US".
    *   **Business Application:** Flags international transactions.

34.  **`df.withColumn("rule_high_velocity", (F.col("txn_count_7d") > 10).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_high\_velocity" based on the transaction count within a 7-day window.
    *   **Business Application:** Flags transactions exceeding a high-velocity threshold.

35.  **`df.withColumn("rule_amount_deviation", (F.abs(F.col("amount_zscore")) > 3).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_amount\_deviation" based on the absolute value of the amount Z-score.
    *   **Business Application:** Flags transactions with a significant amount deviation.

36.  **`df.withColumn("rule_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_high\_amount" indicating whether the transaction amount exceeds $5000.
    *   **Business Application:** Flags high-amount transactions.

37.  **`df.withColumn("rule_unusual_hour", (F.col("is_unusual_hour") == 1).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_unusual\_hour" based on the "is\_unusual\_hour" flag.
    *   **Business Application:** Flags transactions occurring during unusual hours.

38.  **`df.withColumn("rule_international", (F.col("is_international") == 1).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_international" based on the "is\_international" flag.
    *   **Business Application:** Flags international transactions.

39.  **`df.withColumn("rule_rare_country", (F.col("is_rare_country") == 1).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_rare\_country" based on the "is\_rare\_country" flag.
    *   **Business Application:** Flags transactions occurring in rare countries.

40.  **`df.withColumn("rule_rapid_succession", (F.col("days_since_last_txn").isNotNull() & (F.col("days_since_last_txn") < 0.042)).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_rapid\_succession" based on the time since the last transaction.
    *   **Business Application:** Flags transactions in rapid succession (within 1 hour).

41.  **`df.withColumn("rule_round_amount", ((F.col("amount") % 100 == 0) & (F.col("amount") >= 1000)).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "rule\_round\_amount" for transactions with amounts that are multiples of 100 and greater than or equal to 1000.
    *   **Business Application:** Flags transactions with round amounts.

42.  **`df.withColumn("rule_score", (F.col("rule_high_velocity") * 25) + ...)`**
    *   **Description:** Calculates a rule-based score based on the weighted sum of triggered rule flags.
    *   **Business Application:** Calculates an overall score based on the triggered rules.

43.  **`df.withColumn("rule_triggered_array", F.array_remove(F.array(*rule_names), F.lit(None)))`**
    *   **Description:** Creates an array of triggered rule names.
    *   **Business Application:** Identifies which rules triggered for a specific transaction.

44.  **`df.withColumn("rule_triggered", F.concat_ws(", ", F.col("rule_triggered_array"))`**
    *   **Description:** Concatenates the triggered rule names into a comma-separated string.
    *   **Business Application:** Creates a string representation of triggered rules.

45.  **`df.withColumn("rule_risk_level", F.when(...).when(...).when(...).otherwise(...))`**
    *   **Description:** Assigns a risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the rule score.
    *   **Business Application:** Categorizes transactions into risk levels based on the rule score.

46.  **`df.withColumn("is_suspicious", (F.col("rule_score") >= 50).cast(T.IntegerType()))`**
    *   **Description:** Creates a flag "is\_suspicious" indicating whether a transaction is suspicious based on the rule score.
    *   **Business Application:** Flags transactions that are suspicious based on the rule score.

47.  **`df.filter(F.col("rule_score") >= threshold)`**
    *   **Description:** Filters the DataFrame to include only transactions with a rule score greater than or equal to the specified threshold.
    *   **Business Application:** Filters for transactions that meet the threshold for generating alerts.

48.  **`alerts_df.orderBy(F.col("rule_score").desc(), F.col("transaction_date_sas").desc())`**
    *   **Description:** Orders the alerts DataFrame by rule score in descending order, then by transaction date in descending order.
    *   **Business Application:** Sorts alerts by score and date for prioritization.

49.  **`alerts_df.groupBy("rule_risk_level").count().orderBy("rule_risk_level")`**
    *   **Description:** Counts the number of alerts for each risk level.
    *   **Business Application:** Provides a summary of alerts by risk level.

50.  **`df.groupBy().agg(F.sum(F.col("rule_high_velocity")).alias("HIGH_VELOCITY"), ...)`**
    *   **Description:** Aggregates the sum of each rule flag across all transactions.
    *   **Business Application:** Provides a summary of the number of times each rule was triggered.

51.  **`df.sparkSession.createDataFrame(summary_data, schema=summary_schema).orderBy(F.col("trigger_count").desc())`**
    *   **Description:** Creates a DataFrame from the rule summary dictionary.
    *   **Business Application:** Formats the rule summary data into a DataFrame for display.

52.  **`df.withColumn("is_high_amount", (F.col("amount") > 1000).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "is\_high\_amount" for amounts greater than 1000.
    *   **Business Application:** Creates a binary flag for high-amount transactions.

53.  **`df.withColumn("is_very_high_amount", (F.col("amount") > 5000).cast(T.IntegerType()))`**
    *   **Description:** Creates a binary flag "is\_very\_high\_amount" for amounts greater than 5000.
    *   **Business Application:** Creates a binary flag for very high-amount transactions.

54.  **`df.withColumn("amount_normalized", F.col("amount") / 10000)`**
    *   **Description:** Normalizes the "amount" column by dividing by 10000.
    *   **Business Application:** Normalizes the transaction amount for ML model input.

55.  **`df.withColumn("txn_count_normalized", F.col("txn_count_7d") / 20)`**
    *   **Description:** Normalizes the "txn\_count\_7d" column by dividing by 20.
    *   **Business Application:** Normalizes the transaction count for ML model input.

56.  **`df.withColumn("logit_score", F.lit(-2.5) + ...)`**
    *   **Description:** Calculates the logit score using a linear combination of the normalized features and coefficients.
    *   **Business Application:** Calculates the logit score using the formula.

57.  **`df.withColumn("ml_score_probability", F.lit(1) / (F.lit(1) + F.exp(-F.col("logit_score"))))`**
    *   **Description:** Converts the logit score to a probability using the sigmoid function.
    *   **Business Application:** Converts the logit score to a probability.

58.  **`df.withColumn("ml_score", (F.col("ml_score_probability") * 100).cast(T.IntegerType()))`**
    *   **Description:** Scales the probability to a score between 0 and 100.
    *   **Business Application:** Scales the probability to a score.

59.  **`df.withColumn("ml_risk_level", F.when(...).when(...).when(...).otherwise(...))`**
    *   **Description:** Assigns a risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the ML score.
    *   **Business Application:** Categorizes transactions into risk levels based on the ML score.

60.  **`df.withColumn("final_fraud_score", (F.col("rule_score") * 0.4) + (F.col("ml_score") * 0.6))`**
    *   **Description:** Calculates the final fraud score as a weighted average of the rule-based and ML scores.
    *   **Business Application:** Combines the rule and ML scores to produce a final score.

61.  **`df.withColumn("final_risk_level", F.when(...).when(...).otherwise(...))`**
    *   **Description:** Assigns a final risk level (CRITICAL, HIGH, MEDIUM, LOW) based on the final fraud score.
    *   **Business Application:** Assigns a final risk level based on the combined score.

62.  **`df.withColumn("final_recommendation", F.when(...).when(...).otherwise(...))`**
    *   **Description:** Generates a final recommendation (INVESTIGATE, MONITOR, APPROVE) based on the final fraud score.
    *   **Business Application:** Recommends an action based on the final risk level.

63.  **`.write.mode("overwrite").option("header", "true").csv(output_file_path)`**
    *   **Description:** Writes the DataFrame to a CSV file.
    *   **Business Application:** Saves high-risk transaction data to a CSV file for further investigation and reporting.

64.  **`.write.mode("overwrite").parquet(processed_output_path)`**
    *   **Description:** Writes the processed DataFrame to a Parquet file.
    *   **Business Application:** Saves all processed transaction data to a Parquet file for future use.

#### Analytical operations

*   **`groupBy()`**: Used extensively for aggregation and calculating statistics at the customer, country, and overall levels.
*   **`agg()`**: Used to perform aggregate calculations like `count()`, `sum()`, `avg()`, and `stddev()`.
*   **`join()`**: Used to combine data from different DataFrames (e.g., joining customer statistics with transaction data).
*   **`orderBy()`**: Used to sort data, particularly for alerts and reports.
*   **`rangeBetween()`**: Used within the window specification for rolling window calculations.
*   **`count()`**: Used to count the number of transactions.
*   **`sum()`**: Used to sum transaction amounts.
*   **`avg()`**: Used to calculate average transaction amounts.
*   **`stddev()`**: Used to calculate the standard deviation of transaction amounts.

#### Statistical functions used

*   `mean`: Used indirectly through `avg()`
*   `stddev`: Used to calculate the standard deviation of transaction amounts.
*   `count`: Used to count transactions, customer transaction counts, and rule triggers.
*   `sum`: Used to sum transaction amounts and rule triggers.
*   `approxQuantile`: Used to calculate percentiles for outlier detection.
*   `abs`: Used to calculate absolute values (for amount deviation).

#### Machine learning or predictive logic

*   **Simulated Logistic Regression:** The program includes a simplified logistic regression model to calculate an ML-based fraud score. It uses a linear combination of features and a sigmoid function to generate a probability and then a fraud score.

#### Report generation and formatting logic

*   **`generate_rule_alerts()`:** Generates alerts based on the rule score and displays a summary of alerts by risk level.
*   **`rule_summary_report()`:** Creates a summary report of rule triggers.
*   **`generate_final_report()`:** Generates a final fraud detection report, including summary statistics and saving high-risk transactions to a CSV file.

#### Business application of each SQL query or analytical operation

The business applications of the SQL queries and analytical operations are as described above. The core objective is to detect fraudulent transactions using a combination of rule-based and ML techniques. This includes:

*   **Data Import and Validation:** Ensuring data quality and completeness.
*   **Data Cleaning and Standardization:** Preparing the data for analysis.
*   **Feature Engineering:** Creating relevant features to improve fraud detection.
*   **Rule-Based Detection:** Identifying suspicious transactions based on pre-defined rules.
*   **ML Scoring:** Assessing the risk of fraud using a simulated logistic regression model.
*   **Score Combination and Reporting:** Generating a final fraud score, risk level, and recommendations, and producing reports to summarize findings.
