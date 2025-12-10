# SAS Program Analysis

This document provides a detailed analysis of the provided SAS programs, focusing on external database connections, file I/O operations, PROC SQL queries, and LIBNAME/IMPORT/EXPORT/FILENAME statements.

## 01_transaction_data_import.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **File Imports**: This program imports transaction data from a CSV file.
*   **Internal I/O**: Reads data from a CSV file and writes to SAS datasets in the `WORK` library.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC PRINT` generates output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program uses `PROC SQL` to count records for validation purposes.

```sas
PROC SQL NOPRINT;
    SELECT COUNT(*) INTO :valid_count FROM &outds;
    SELECT COUNT(*) INTO :total_count FROM &inds;
QUIT;
```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

This program uses `PROC IMPORT` to bring data from a CSV file into a SAS dataset.

```sas
PROC IMPORT 
    DATAFILE="&filepath"
    OUT=&outds
    DBMS=CSV
    REPLACE;
    GETNAMES=YES;
RUN;
```

*   **`DATAFILE`**: The input file is specified by `&filepath`, which resolves to `/data/raw/transactions.csv`.
*   **`OUT`**: The output SAS dataset is `&outds`, which resolves to `WORK.raw_transactions`.
*   **`DBMS`**: The database management system specified is `CSV`, indicating a comma-separated values file.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program. The `DATAFILE` option in `PROC IMPORT` directly references the file path.

### Database Engine Usage

The `DBMS=CSV` option in `PROC IMPORT` indicates that a CSV file is being processed, not an external database engine like ODBC or OLEDB.

## 02_data_quality_cleaning.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **Internal I/O**: Reads from and writes to SAS datasets within the `WORK` library.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC MEANS` generates statistical output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program uses `PROC SQL` to count records before and after duplicate removal.

```sas
PROC SQL NOPRINT;
    SELECT COUNT(*) INTO :before_count FROM &inds;
    SELECT COUNT(*) INTO :after_count FROM &outds;
QUIT;
```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

No `PROC IMPORT` or `PROC EXPORT` statements are used in this program. All data manipulation occurs on existing SAS datasets.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program.

### Database Engine Usage

No external database engines (like ODBC, OLEDB, etc.) are used in this program. All operations are performed on SAS datasets.

## 03_feature_engineering.sas

### External Database Connections, File Imports/Exports, and I/O Operations

*   **Internal I/O**: Reads from and writes to SAS datasets within the `WORK` library. Intermediate datasets (`customer_stats`, `country_counts`) are also created.
*   **Logging**: Uses `%PUT` statements for logging program execution and results.
*   **Output**: `PROC PRINT` generates output to the SAS listing or log.

### PROC SQL Queries and Database Operations

This program extensively uses `PROC SQL` for calculating and merging features.

1.  **Calculate Amount Deviation and Merge Statistics:**
    ```sas
    PROC SQL;
        CREATE TABLE &outds AS
        SELECT 
            a.*,
            b.customer_avg_amount,
            b.customer_std_amount,
            b.customer_txn_count,
            /* Calculate z-score */
            CASE 
                WHEN b.customer_std_amount > 0 THEN
                    (a.amount - b.customer_avg_amount) / b.customer_std_amount
                ELSE 0
            END AS amount_zscore,
            /* Calculate percentage deviation */
            CASE
                WHEN b.customer_avg_amount > 0 THEN
                    ((a.amount - b.customer_avg_amount) / b.customer_avg_amount) * 100
                ELSE 0
            END AS amount_pct_deviation
        FROM &inds a
        LEFT JOIN customer_stats b
        ON a.customer_id = b.customer_id;
    QUIT;
    ```

2.  **Calculate Country Transaction Counts:**
    ```sas
    PROC SQL;
        CREATE TABLE country_counts AS
        SELECT 
            country_code_clean,
            COUNT(*) AS country_txn_count
        FROM &inds
        GROUP BY country_code_clean;
    QUIT;
    ```

3.  **Merge Country Features:**
    ```sas
    PROC SQL;
        CREATE TABLE &outds AS
        SELECT 
            a.*,
            b.country_txn_count,
            /* Flag for rare countries */
            CASE 
                WHEN b.country_txn_count < 10 THEN 1
                ELSE 0
            END AS is_rare_country,
            /* Check if international transaction */
            CASE
                WHEN a.country_code_clean NE 'US' THEN 1
                ELSE 0
            END AS is_international
        FROM &inds a
        LEFT JOIN country_counts b
        ON a.country_code_clean = b.country_code_clean;
    QUIT;
    ```

### LIBNAME Assignments for Database Connections

No `LIBNAME` statements are used for external database connections in this program. The `WORK` library is used for temporary SAS datasets.

### PROC IMPORT/EXPORT Statements with File Details

No `PROC IMPORT` or `PROC EXPORT` statements are used in this program. All data manipulation occurs on existing SAS datasets.

### FILENAME Statements and File Operations

No `FILENAME` statements are used in this program.

### Database Engine Usage

No external database engines (like ODBC, OLEDB, etc.) are used in this program. All operations are performed on SAS datasets.