## Analysis of SAS Programs

Here's an analysis of each SAS program, detailing external database connections, file I/O, PROC SQL queries, LIBNAME assignments, PROC IMPORT/EXPORT statements, FILENAME statements, and database engine usage.

### 01_transaction_data_import.sas

*   **External Database Connections:** None
*   **File Imports/Exports:**
    *   Imports a CSV file.
*   **I/O Operations:**
    *   Reads a CSV file.
    *   Writes a SAS dataset.
    *   Prints a sample of the dataset.
*   **PROC SQL Queries and Database Operations:**
    *   `PROC SQL` is used to count records after validation.

    ```sas
    PROC SQL NOPRINT;
        SELECT COUNT(*) INTO :valid_count FROM &outds;
        SELECT COUNT(*) INTO :total_count FROM &inds;
    QUIT;
    ```

*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:**
    *   `PROC IMPORT` is used to import the CSV file.

    ```sas
    PROC IMPORT 
        DATAFILE="&filepath"
        OUT=&outds
        DBMS=CSV
        REPLACE;
        GETNAMES=YES;
    RUN;
    ```

*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable

### 02_data_quality_cleaning.sas

*   **External Database Connections:** None
*   **File Imports/Exports:** None
*   **I/O Operations:**
    *   Reads and writes SAS datasets.
    *   Prints summary statistics.
*   **PROC SQL Queries and Database Operations:**
    *   `PROC SQL` is used to count records before and after duplicate removal.

    ```sas
    PROC SQL NOPRINT;
        SELECT COUNT(*) INTO :before_count FROM &inds;
        SELECT COUNT(*) INTO :after_count FROM &outds;
    QUIT;
    ```

*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:** None
*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable

### 03_feature_engineering.sas

*   **External Database Connections:** None
*   **File Imports/Exports:** None
*   **I/O Operations:**
    *   Reads and writes SAS datasets.
    *   Prints summary statistics.
*   **PROC SQL Queries and Database Operations:**
    *   `PROC SQL` is used to calculate customer statistics for amount deviation.

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
    *   `PROC SQL` is used to create country counts.

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
    *   `PROC SQL` is used to merge back and create features.

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

*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:** None
*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable

### 04_rule_based_detection.sas

*   **External Database Connections:** None
*   **File Imports/Exports:** None
*   **I/O Operations:**
    *   Reads and writes SAS datasets.
    *   Prints frequency tables.
    *   Prints summary reports.
*   **PROC SQL Queries and Database Operations:**
    *   `PROC SQL` is used to create rule trigger summary.

    ```sas
    PROC SQL;
        CREATE TABLE rule_summary AS
        SELECT 
            'HIGH_VELOCITY' AS rule_name,
            SUM(CASE WHEN INDEX(rule_triggered, 'HIGH_VELOCITY') > 0 THEN 1 ELSE 0 END) AS trigger_count
        FROM &inds
        UNION ALL
        SELECT 
            'AMOUNT_DEVIATION' AS rule_name,
            SUM(CASE WHEN INDEX(rule_triggered, 'AMOUNT_DEVIATION') > 0 THEN 1 ELSE 0 END)
        FROM &inds
        UNION ALL
        SELECT 
            'HIGH_AMOUNT' AS rule_name,
            SUM(CASE WHEN INDEX(rule_triggered, 'HIGH_AMOUNT') > 0 THEN 1 ELSE 0 END)
        FROM &inds
        UNION ALL
        SELECT 
            'UNUSUAL_HOUR' AS rule_name,
            SUM(CASE WHEN INDEX(rule_triggered, 'UNUSUAL_HOUR') > 0 THEN 1 ELSE 0 END)
        FROM &inds
        UNION ALL
        SELECT 
            'INTERNATIONAL' AS rule_name,
            SUM(CASE WHEN INDEX(rule_triggered, 'INTERNATIONAL') > 0 THEN 1 ELSE 0 END)
        FROM &inds;
    QUIT;
    ```
    *   `PROC SQL` is used to count alerts.

    ```sas
    PROC SQL NOPRINT;
        SELECT COUNT(*) INTO :alert_count FROM &outds;
        SELECT COUNT(*) INTO :total_count FROM &inds;
    QUIT;
    ```

*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:** None
*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable

### 05_ml_scoring_model.sas

*   **External Database Connections:** None
*   **File Imports/Exports:** None
*   **I/O Operations:**
    *   Reads and writes SAS datasets.
    *   Prints summary statistics.
    *   Prints frequency tables.
    *   Prints correlation tables.
*   **PROC SQL Queries and Database Operations:** None
*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:** None
*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable

### 06_case_management_output.sas

*   **External Database Connections:** None
*   **File Imports/Exports:**
    *   Exports a CSV file.
*   **I/O Operations:**
    *   Reads and writes SAS datasets.
    *   Prints summary reports.
    *   Prints frequency tables.
*   **PROC SQL Queries and Database Operations:**
    *   `PROC SQL` is used to calculate queue statistics.

    ```sas
    PROC SQL NOPRINT;
        SELECT COUNT(*) INTO :queue_count FROM &outds;
        SELECT COUNT(DISTINCT customer_id) INTO :unique_customers FROM &outds;
    QUIT;
    ```
    *   `PROC SQL` is used to generate daily summary statistics.

    ```sas
    PROC SQL;
        CREATE TABLE daily_summary AS
        SELECT 
            COUNT(*) AS total_transactions,
            SUM(ml_alert) AS ml_alerts,
            SUM(is_suspicious) AS rule_alerts,
            SUM(CASE WHEN ml_alert=1 OR is_suspicious=1 THEN 1 ELSE 0 END) AS total_alerts,
            SUM(amount) AS total_amount FORMAT=DOLLAR20.2,
            SUM(CASE WHEN ml_alert=1 OR is_suspicious=1 THEN amount ELSE 0 END) 
                AS flagged_amount FORMAT=DOLLAR20.2,
            CALCULATED total_alerts / CALCULATED total_transactions * 100 
                AS alert_rate FORMAT=5.2
        FROM &inds;
    QUIT;
    ```
    *   `PROC SQL` is used to generate top customer statistics.

    ```sas
    PROC SQL OUTOBS=20;
        CREATE TABLE top_customers AS
        SELECT 
            customer_id,
            COUNT(*) AS alert_count,
            SUM(amount) AS total_flagged_amount FORMAT=DOLLAR15.2,
            AVG(combined_score) AS avg_score FORMAT=5.1,
            MAX(case_priority) AS highest_priority
        FROM &inds
        WHERE ml_alert = 1 OR is_suspicious = 1
        GROUP BY customer_id
        ORDER BY alert_count DESC, total_flagged_amount DESC;
    QUIT;
    ```
    *   `PROC SQL` is used to generate hourly trend.

    ```sas
    PROC SQL;
        CREATE TABLE hourly_trend AS
        SELECT 
            txn_hour,
            COUNT(*) AS transaction_count,
            SUM(CASE WHEN ml_alert=1 OR is_suspicious=1 THEN 1 ELSE 0 END) AS alert_count,
            CALCULATED alert_count / CALCULATED transaction_count * 100 
                AS alert_rate FORMAT=5.2
        FROM &inds
        GROUP BY txn_hour
        ORDER BY txn_hour;
    QUIT;
    ```
    *   `PROC SQL` is used to count SAR cases.

    ```sas
    PROC SQL NOPRINT;
        SELECT COUNT(*) INTO :sar_count FROM &outds;
    QUIT;
    ```

*   **LIBNAME Assignments:** None
*   **PROC IMPORT/EXPORT Statements:**
    *   `PROC EXPORT` is used to export the investigation queue to a CSV file.

    ```sas
    PROC EXPORT 
        DATA=export_data
        OUTFILE="&filepath/investigation_queue_&SYSDATE9..csv"
        DBMS=CSV
        REPLACE;
    RUN;
    ```

*   **FILENAME Statements:** None
*   **Database Engine Usage:** Not Applicable
