### List of PySpark programs analyzed

*   Fraud Detection Pipeline

### Sequence of Transformations and Actions

1.  **Initialization:**
    *   `create_spark_session()`: Initializes a SparkSession with configurations for legacy time parsing, shuffle partitions, driver, and executor memory.
2.  **Data Import (01_transaction\_data\_import.sas):**
    *   `import_transactions()`: Reads transaction data from a CSV file (specified by `INPUT_PATH` and `TRANSACTION_FILE`) using the defined `TRANSACTION_SCHEMA`.
    *   `validate_transactions()`:
        *   Counts the total number of records.
        *   Adds a `validation_status` column based on checks for missing values and invalid amounts.
        *   Filters the DataFrame, keeping only records where `validation_status` is "VALID".
        *   Counts the number of valid records.
3.  **Data Quality Cleaning (02\_data\_quality\_cleaning.sas):**
    *   `clean_transactions()`:
        *   Creates `transaction_type_clean` by uppercasing and trimming `transaction_type`.
        *   Creates `merchant_name_clean` by capitalizing and trimming `merchant_name`.
        *   Creates `country_code_clean` by uppercasing and extracting the first two characters of `country_code`.
        *   Replaces missing values in `amount` with 0.
        *   Converts `transaction_date` to `transaction_date_sas` using `to_date`.
        *   Creates `transaction_datetime` by combining date and time columns using `to_timestamp`.
    *   `remove_duplicates()`: Removes duplicate records based on the specified key columns ("transaction\_id", "customer\_id", "transaction\_datetime").
    *   `handle_outliers()`: Handles outliers in the `amount` column using the Winsorize method:
        *   Calculates 1st and 99th percentiles of `amount`.
        *   Winsorizes `amount` to the calculated percentiles.
4.  **Feature Engineering (03\_feature\_engineering.sas):**
    *   `calculate_velocity_features()`:
        *   Calculates `days_since_last_txn` using `lag` and `datediff`.
        *   Calculates rolling window features: `txn_count_7d`, `txn_amount_7d`, and `avg_txn_amount_7d`.
    *   `calculate_amount_deviation()`:
        *   Calculates customer-level statistics: average amount, standard deviation, and transaction count.
        *   Joins the customer statistics back to the main DataFrame.
        *   Calculates `amount_zscore` (Z-score).
        *   Calculates `amount_pct_deviation` (percentage deviation).
    *   `create_time_features()`:
        *   Extracts time-based features: `txn_hour`, `txn_day_of_week`, `txn_day_of_month`, and `txn_month`.
        *   Creates `time_of_day` categories based on `txn_hour`.
        *   Creates `is_weekend` and `is_unusual_hour` flags.
    *   `create_location_features()`:
        *   Calculates country-level transaction counts.
        *   Joins the country counts back to the main DataFrame.
        *   Creates `is_rare_country` and `is_international` flags.
5.  **Caching:** Caches the `transactions_df` DataFrame to optimize performance for subsequent operations.  A `count()` action is used to trigger the caching.
6.  **Rule-Based Detection (04\_rule\_based\_detection.sas):**
    *   `apply_fraud_rules()`:
        *   Calculates individual rule flags (e.g., `rule_high_velocity`, `rule_amount_deviation`).
        *   Calculates `rule_score` based on the triggered rules.
        *   Concatenates triggered rule names into `rule_triggered`.
        *   Calculates `rule_risk_level` (CRITICAL, HIGH, MEDIUM, LOW) based on `rule_score`.
        *   Creates `is_suspicious` flag based on `rule_score`.
    *   `generate_rule_alerts()`:
        *   Counts total transactions.
        *   Filters for transactions where `rule_score` is greater than or equal to 50.
        *   Orders the alerts by descending `rule_score` and `transaction_date_sas`.
        *   Counts alerts by risk level and displays the counts.
        *   Calculates and logs the alert rate.
    *   `rule_summary_report()`:
        *   Aggregates the individual rule flags to generate a summary of rule triggers.
        *   Displays the rule trigger summary.
7.  **ML Scoring (05\_ml\_scoring\_model.sas):**
    *   `prepare_ml_data()`:
        *   Creates binary flags (`is_high_amount`, `is_very_high_amount`).
        *   Normalizes continuous variables (`amount_normalized`, `txn_count_normalized`).
        *   Handles missing values in `amount_zscore` and `days_since_last_txn`.
        *   Creates interaction features (`amount_x_velocity`, `amount_x_deviation`).
    *   `calculate_ml_score()`:
        *   Calculates the `logit_score` using a simulated logistic regression formula.
        *   Calculates `ml_score_probability` using a sigmoid function.
        *   Scales the probability to a score (`ml_score`).
        *   Assigns `ml_risk_level` (CRITICAL, HIGH, MEDIUM, LOW) based on the score.
8.  **Combine Scores and Reporting (06\_combine\_scores\_reporting.sas):**
    *   `combine_scores()`:
        *   Calculates the `final_fraud_score` as a weighted average of `rule_score` and `ml_score`.
        *   Determines the `final_risk_level` based on `final_fraud_score`.
        *   Assigns a `final_recommendation` (INVESTIGATE, MONITOR, APPROVE) based on `final_fraud_score`.
    *   `generate_final_report()`:
        *   Counts total transactions.
        *   Filters for high-risk transactions.
        *   Calculates and logs high-risk counts and rates.
        *   Creates and displays a summary of the final risk level distribution.
        *   Creates and displays a summary of the final recommendation distribution.
        *   Saves high-risk transactions to a CSV file (specified by `OUTPUT_PATH`).
9.  **Final Output:**
    *   Saves all processed transactions to a Parquet file (specified by `OUTPUT_PATH`).
10. **SparkSession Stop:**
    *   `spark.stop()`: Stops the SparkSession.

### DataFrame Dependencies

*   `transactions_df` is the primary DataFrame that is transformed throughout the pipeline.
*   Each function typically takes the `transactions_df` or a modified version of it as input and returns a modified DataFrame.
*   `customer_stats_df` is created within `calculate_amount_deviation()` and is joined back to `transactions_df`.
*   `country_counts_df` is created within `create_location_features()` and is joined back to `transactions_df`.
*   `alerts_df` is created in `generate_rule_alerts()` by filtering `transactions_df`.
*   `risk_level_counts` is created in `generate_rule_alerts()` by grouping `alerts_df`.
*   `rule_summary_df` is created in `rule_summary_report()` by aggregating `transactions_df`.
*   `high_risk_transactions` is created in `generate_final_report()` by filtering `transactions_df`.

### Function/Pipeline Execution Order

The functions are executed in the order they are called within the `main()` function, which represents the overall pipeline execution:

1.  `create_spark_session()`
2.  `import_transactions()`
3.  `validate_transactions()`
4.  `clean_transactions()`
5.  `remove_duplicates()`
6.  `handle_outliers()`
7.  `calculate_velocity_features()`
8.  `calculate_amount_deviation()`
9.  `create_time_features()`
10. `create_location_features()`
11. `apply_fraud_rules()`
12. `generate_rule_alerts()`
13. `rule_summary_report()`
14. `prepare_ml_data()`
15. `calculate_ml_score()`
16. `combine_scores()`
17. `generate_final_report()`
18. `spark.stop()`

### Action Trigger Points

*   `count()`: Used multiple times to trigger the execution of transformations and to trigger caching.
*   `show()`: Used to display the results of aggregations and reports.
*   `write.csv()`: Used to save high-risk transactions to a CSV file.
*   `write.parquet()`: Used to save all processed transactions to a Parquet file.
*   `collect()`: Used to retrieve a single row for rule summary report.

### List of Use Cases Addressed

*   **Data Import and Validation:** Importing transaction data from a CSV file, validating the data, and filtering out invalid records.
*   **Data Cleaning and Standardization:** Cleaning and standardizing transaction data, including transaction type, merchant name, and country codes.
*   **Duplicate Removal:** Removing duplicate transactions.
*   **Outlier Handling:** Handling outliers in the transaction amount.
*   **Feature Engineering:** Creating various features, including:
    *   Velocity features (transaction counts, amount sums, average amount in a rolling window).
    *   Amount deviation features (average amount, standard deviation, Z-score, percentage deviation).
    *   Time-based features (hour, day of week, day of month, month, time of day categories, weekend flag, unusual hour flag).
    *   Location-based features (country transaction counts, rare country flag, international flag).
*   **Rule-Based Fraud Detection:** Applying a set of fraud detection rules and calculating a rule score.
*   **Alert Generation:** Generating alerts based on the rule score.
*   **Machine Learning Scoring:** Preparing data for ML scoring, calculating an ML-based fraud score, and assigning an ML-based risk level.
*   **Score Combination:** Combining rule-based and ML-based scores to derive a final fraud assessment.
*   **Reporting:** Generating a final fraud detection report, including summary statistics and saving high-risk transactions to a CSV file.
