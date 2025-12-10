### Program 01: 01_transaction_data_import.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   File I/O: Reads a CSV file containing transaction data.
*   **spark.read operations:**
    *   `spark.read.option("header", "true").schema(schema).csv(filepath)`: Reads a CSV file with a header row and applies a predefined schema.
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   Reads from a file path specified by `INPUT_PATH` and `TRANSACTION_FILE` (e.g., `/data/raw/transactions.csv`).
*   **Data format specifications:**
    *   CSV format.
    *   `header="true"`: Specifies that the first row of the CSV file contains header information.
    *   `schema`: Uses a predefined `TRANSACTION_SCHEMA` (StructType) to enforce data types and structure during the read operation.

### Program 02: 02_data_quality_cleaning.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 03: 03_feature_engineering.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 04: 04_rule_based_detection.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 05: 05_ml_scoring_model.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   None
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   None
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   None
*   **Data format specifications:**
    *   None

### Program 06: 06_combine_scores_reporting.sas

*   **External Data Sources, File I/O, and Database Operations:**
    *   File I/O: Writes high-risk transactions to a CSV file.
*   **spark.read operations:**
    *   None
*   **DataFrame.write operations:**
    *   `high_risk_transactions.select(...).write.mode("overwrite").option("header", "true").csv(output_file_path)`: Writes a CSV file containing high-risk transaction data.
*   **JDBC/database connection details:**
    *   None
*   **File system operations:**
    *   Writes to a file path specified by `REPORT_PATH` (e.g., `/output/reports/high_risk_transactions_YYYYMMDD_HHMMSS.csv`).
*   **Data format specifications:**
    *   CSV format.
    *   `header="true"`: Writes a header row to the CSV file.

