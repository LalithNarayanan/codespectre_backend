### Program Analysis: Fraud Detection Pipeline

This PySpark program implements a fraud detection pipeline. It reads transaction data, performs data cleaning, feature engineering, rule-based fraud detection, ML-based scoring, and generates a final report.

#### External Data Sources, File I/O, and Database Operations

*   **External Data Sources:**
    *   CSV file containing transaction data.
*   **File I/O:**
    *   Reading transaction data from a CSV file.
    *   Writing high-risk transactions to a CSV file.
    *   Writing all processed transactions to a Parquet file.
*   **Database Operations:**
    *   None

#### `spark.read` Operations

*   `spark.read.option("header", "true").schema(schema).csv(filepath)`: Reads transaction data from a CSV file.

#### `DataFrame.write` Operations

*   `.write.mode("overwrite").option("header", "true").csv(output_file_path)`: Writes high-risk transactions to a CSV file.
*   `.write.mode("overwrite").parquet(processed_output_path)`: Writes all processed transactions to a Parquet file.

#### JDBC/Database Connection Details

*   None

#### File System Operations

*   Reading from a local or cloud storage path specified by `INPUT_PATH` (e.g., `/data/raw`).
*   Writing to a local or cloud storage path specified by `OUTPUT_PATH` (e.g., `/data/processed`).
*   Writing reports to a local or cloud storage path specified by `REPORT_PATH` (e.g., `/output/reports`).

#### Data Format Specifications

*   **Input CSV:**
    *   Header: `true`
    *   Schema: Defined by `TRANSACTION_SCHEMA` (specifies data types for each column).
    *   Delimiter: Assumed to be comma (`,`) as it's a CSV.
    *   `inferSchema`: Not used; schema is explicitly defined.
*   **Output CSV:**
    *   Header: `true`
    *   Delimiter: Comma (`,`)
*   **Output Parquet:**
    *   Schema: Inherited from the DataFrame being written.
    *   Format: Parquet.

---

### Code Blocks for Read/Write Operations

**1. Reading Transaction Data (import\_transactions function)**

```python
        df = spark.read \
            .option("header", "true") \
            .schema(schema) \
            .csv(filepath)
```

**2. Writing High-Risk Transactions (generate\_final\_report function)**

```python
        high_risk_transactions.select(
            "transaction_id", "customer_id", "amount", "transaction_datetime",
            "merchant_name_clean", "country_code_clean",
            "rule_score", "rule_risk_level", "rule_triggered",
            "ml_score", "ml_risk_level",
            "final_fraud_score", "final_risk_level", "final_recommendation"
        ).write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(output_file_path)
```

**3. Writing Processed Transactions (main function)**

```python
        transactions_df.write \
            .mode("overwrite") \
            .parquet(processed_output_path)
```
