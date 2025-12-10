### Overview of the Program

This PySpark program implements a fraud detection pipeline. It ingests transaction data, performs data validation and cleaning, engineers features, applies rule-based and machine learning (ML) scoring, combines the scores, and generates a final report. The pipeline is designed to identify potentially fraudulent transactions and provide insights for further investigation. The program mirrors a similar SAS-based fraud detection pipeline, with corresponding functions and macro mappings.

### Business Functions Addressed by the Program

*   **Data Ingestion:** Reads transaction data from a CSV file.
*   **Data Validation:** Checks for missing values and invalid amounts.
*   **Data Cleaning and Standardization:** Cleans and standardizes transaction data, including transaction type, merchant name, and country codes.
*   **Duplicate Removal:** Removes duplicate transaction records.
*   **Outlier Handling:** Handles outliers in transaction amounts using Winsorization.
*   **Feature Engineering:**
    *   Calculates velocity features (transaction counts and amounts within a rolling window).
    *   Calculates amount deviation features (average amount, standard deviation, Z-score, and percentage deviation).
    *   Creates time-based features (hour, day of week, day of month, month, time of day, weekend flag, unusual hour flag).
    *   Creates location-based features (transaction count per country, rare country flag, international flag).
*   **Rule-Based Fraud Detection:** Applies a set of predefined rules to identify suspicious transactions.
*   **ML-Based Fraud Scoring:** Calculates a fraud score using a simulated logistic regression model.
*   **Score Combination:** Combines rule-based and ML-based scores to generate a final fraud score.
*   **Reporting:** Generates a final report, including summary statistics and saving high-risk transactions.

### DataFrames/Tables Created and Consumed

*   **transactions\_df:**
    *   **Creation:** Created by importing and validating data from the CSV file specified by `INPUT_PATH` and `TRANSACTION_FILE`.
    *   **Consumption/Transformation:** Consumed and transformed throughout the pipeline by various functions like `validate_transactions`, `clean_transactions`, `remove_duplicates`, `handle_outliers`, `calculate_velocity_features`, `calculate_amount_deviation`, `create_time_features`, `create_location_features`, `apply_fraud_rules`, `prepare_ml_data`, `calculate_ml_score`, and `combine_scores`.
    *   **Data Flow:** Raw transaction data -> validated data -> cleaned data -> data with engineered features -> data with rule-based scores -> data with ML scores -> final scored data.
*   **customer\_stats\_df:**
    *   **Creation:** Created within `calculate_amount_deviation` by grouping `transactions_df` by "customer\_id" and calculating aggregate statistics (average amount, standard deviation, and transaction count).
    *   **Consumption:** Consumed by `calculate_amount_deviation` to join back to the `transactions_df`.
    *   **Data Flow:** Derived from aggregated `transactions_df`.
*   **country\_counts\_df:**
    *   **Creation:** Created within `create_location_features` by grouping `transactions_df` by "country\_code\_clean" and calculating the transaction count.
    *   **Consumption:** Consumed by `create_location_features` to join back to the `transactions_df`.
    *   **Data Flow:** Derived from aggregated `transactions_df`.
*   **rule\_alerts\_df:**
    *   **Creation:** Created within `generate_rule_alerts` by filtering `transactions_df` based on the rule score.
    *   **Consumption:** Consumed by `generate_rule_alerts` to calculate the risk level counts and alert rate.
    *   **Data Flow:** Filtered and ordered `transactions_df`.
*   **risk\_level\_counts:**
    *   **Creation:** Created within `generate_rule_alerts` by grouping `alerts_df` by "rule\_risk\_level" and counting.
    *   **Consumption:** Consumed by `generate_rule_alerts` to show the risk level counts.
    *   **Data Flow:** Aggregated `alerts_df`.
*   **rule\_summary\_df:**
    *   **Creation:** Created within `rule_summary_report` by aggregating rule flags from `transactions_df`.
    *   **Consumption:** Consumed by `rule_summary_report` to show the trigger counts.
    *   **Data Flow:** Aggregated `transactions_df`.
*   **High-Risk Transactions (CSV file):**
    *   **Creation:** Created within `generate_final_report` by filtering `transactions_df` based on the final risk level and writing to a CSV file.
    *   **Consumption:**  The file is saved as a report for external consumption.
    *   **Data Flow:** Filtered `transactions_df`.
*   **Processed Transactions (Parquet file):**
    *   **Creation:** Created in the `main` function by writing `transactions_df` to a Parquet file.
    *   **Consumption:** The file is saved as a processed data asset for future use.
    *   **Data Flow:** Final `transactions_df`.
