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
