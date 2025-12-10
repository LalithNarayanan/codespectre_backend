### Program Analysis

#### Program: Fraud Detection Pipeline

##### DataFrames/Tables Created and Consumed

*   **transactions\_df**:
    *   **Description**: Stores the transaction data throughout the pipeline. It is transformed and updated in each step.
    *   **Created/Consumed**: Created by `import_transactions`. Consumed and transformed by all subsequent functions.
*   **validated\_df**:
    *   **Description**: Stores the validated transaction data after filtering out invalid records.
    *   **Created/Consumed**: Created by `validate_transactions`.
*   **customer\_stats\_df**:
    *   **Description**: Stores the average amount, standard deviation of amount, and count of transactions, grouped by customer.
    *   **Created/Consumed**: Created by `calculate_amount_deviation`. Consumed by `calculate_amount_deviation`.
*   **country\_counts\_df**:
    *   **Description**: Stores the count of transactions, grouped by country code.
    *   **Created/Consumed**: Created by `create_location_features`. Consumed by `create_location_features`.
*   **alerts\_df**:
    *   **Description**: Stores transactions that exceed the fraud alert threshold.
    *   **Created/Consumed**: Created by `generate_rule_alerts`.
*   **risk\_level\_counts**:
    *   **Description**: Stores counts of alerts, grouped by risk level.
    *   **Created/Consumed**: Created by `generate_rule_alerts`. Consumed by `generate_rule_alerts`.
*   **recommendation\_summary**:
    *   **Description**: Stores counts of transactions, grouped by final recommendation.
    *   **Created/Consumed**: Created by `generate_final_report`. Consumed by `generate_final_report`.
*   **rule\_summary\_df**:
    *   **Description**: Stores the summary report of rule triggers.
    *   **Created/Consumed**: Created by `rule_summary_report`. Consumed by `rule_summary_report`.

##### Input Sources

*   **spark.read.csv**:
    *   **Details**: Reads transaction data from a CSV file specified by `INPUT_PATH` and `TRANSACTION_FILE`.
    *   **Schema**: Uses the `TRANSACTION_SCHEMA` to define the data types of the columns.
    *   **Options**: Uses the option `header="true"` to indicate that the CSV file has a header row.

##### Output DataFrames/Tables

*   **Temporary Views**: None
*   **Permanent Catalog Tables**: None
*   **Output Files**:
    *   High-risk transactions are saved to a CSV file in the format `/output/reports/high_risk_transactions_YYYYMMDD_HHMMSS.csv`.
    *   Processed transactions are saved to a Parquet file in the format `/data/processed/processed_transactions_YYYYMMDD_HHMMSS`.

##### Key Column Usage and Transformations

*   **transaction\_id**: Used for duplicate removal and validation.
*   **customer\_id**: Used for joining data and calculating customer-specific features.
*   **amount**: Used for outlier handling, calculating amount deviation features, rule-based fraud detection, ML scoring and normalization.
*   **transaction\_date**: Used to create a SAS date format and transaction timestamp.
*   **transaction\_time**: Used to create a transaction timestamp.
*   **transaction\_type**: Cleaned and standardized.
*   **merchant\_name**: Cleaned and standardized.
*   **country\_code**: Cleaned, standardized, and used for location-based features.
*   **validation\_status**: Calculated based on missing values and invalid amounts.
*   **transaction\_type\_clean**: `UPPER` and `TRIM` transformations.
*   **merchant\_name\_clean**: `INITCAP` and `TRIM` transformations.
*   **country\_code\_clean**: `UPPER` and `SUBSTRING` transformations.
*   **transaction\_date\_sas**: Converted to `date` type using `to_date`.
*   **transaction\_datetime**: Created by combining date and time using `to_timestamp`.
*   **amount**: Replaced missing values with 0 using `coalesce`.
*   **Outlier Handling**: Winsorization or removal based on 1st and 99th percentiles.
*   **Velocity Features**: Calculates transaction counts, amount, and average amount over a 7-day window.
*   **Amount Deviation Features**: Calculates average amount, standard deviation, Z-score, and percentage deviation using `groupBy` and `agg`.
*   **Time Features**: Extracts hour, day of the week, day of the month, and month from the transaction date.
*   **Location Features**: Calculates country transaction counts and flags for rare countries and international transactions.
*   **Rule-Based Scores**: Calculates rule-based scores based on multiple conditions.
*   **ML Scoring**: Normalizes continuous variables, creates interaction features, and calculates an ML score.
*   **Final Score**: Combines rule-based and ML scores to calculate a final fraud score.

##### Schema Definitions and Column Data Types

*   **TRANSACTION\_SCHEMA**:
    *   `transaction_id`: `StringType`, nullable=True
    *   `customer_id`: `StringType`, nullable=True
    *   `amount`: `DoubleType`, nullable=True
    *   `transaction_date`: `StringType`, nullable=True
    *   `transaction_time`: `StringType`, nullable=True
    *   `transaction_type`: `StringType`, nullable=True
    *   `merchant_name`: `StringType`, nullable=True
    *   `country_code`: `StringType`, nullable=True
*   **Other DataFrames**: The schema evolves as new columns are added and existing ones are transformed. Data types are inferred or explicitly cast.

##### Table/View Registration

*   **createOrReplaceTempView**: Not used.
*   **saveAsTable**: Not used. The final output is saved to CSV and Parquet files.
