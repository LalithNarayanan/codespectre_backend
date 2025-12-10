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
