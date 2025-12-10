## Analysis of SAS Programs

### Program: 01_transaction_data_import.sas

*   **Overview of the Program:**
    This SAS program imports transaction data from a CSV file, performs initial data validation, and filters out invalid records. It uses macros to encapsulate the import and validation processes, promoting reusability and modularity.

*   **Business Functions Addressed:**
    *   Data Ingestion: Imports raw transaction data.
    *   Data Validation: Checks for missing values and invalid amounts.
    *   Data Quality: Filters out invalid records based on validation rules.

*   **Datasets Created and Consumed (Data Flow):**

    1.  **Input:** `/data/raw/transactions.csv` (CSV file containing raw transaction data)
    2.  **Created:** `WORK.raw_transactions` (SAS dataset containing the imported data from the CSV file).
    3.  **Consumed:** `WORK.raw_transactions`
    4.  **Created:** `WORK.transactions_validated` (SAS dataset containing validated transaction data, filtered for valid records).
    5.  **Consumed:** `WORK.transactions_validated` (Used for displaying the first 10 records).
    6.  **Output:** Prints the first 10 records of the validated data.

---

### Program: 02_data_quality_cleaning.sas

*   **Overview of the Program:**
    This SAS program cleans and standardizes transaction data, removes duplicates, and handles outliers. It uses macros for cleaning, duplicate removal, and outlier handling. The program transforms the data by standardizing formats, correcting inconsistencies, and addressing potential data quality issues.

*   **Business Functions Addressed:**
    *   Data Standardization: Standardizes transaction types, merchant names, and country codes.
    *   Data Transformation: Converts transaction dates and times to a standard format.
    *   Data Cleaning: Handles missing amounts and replaces them with 0.
    *   Data Deduplication: Removes duplicate records based on a specified key.
    *   Outlier Handling: Winsorizes or removes outliers in the transaction amount.
    *   Data Quality: Improves the overall quality of the transaction data by addressing inconsistencies and errors.

*   **Datasets Created and Consumed (Data Flow):**

    1.  **Input:** `WORK.transactions_validated` (SAS dataset containing validated transaction data from the previous program).
    2.  **Consumed:** `WORK.transactions_validated`
    3.  **Created:** `WORK.transactions_cleaned` (SAS dataset containing the cleaned transaction data, with standardized formats and missing values handled).
    4.  **Consumed:** `WORK.transactions_cleaned`
    5.  **Created:** `WORK.transactions_deduped` (SAS dataset with duplicate records removed).
    6.  **Consumed:** `WORK.transactions_deduped`
    7.  **Created:** `WORK.transactions_final` (SAS dataset with outliers handled - either winsorized or removed).
    8.  **Consumed:** `WORK.transactions_final` (Used for calculating and displaying descriptive statistics).
    9.  **Created:** `WORK.percentiles` (Temporary dataset created inside the `HANDLE_OUTLIERS` macro to store percentiles)
    10. **Output:** Prints descriptive statistics (N, Mean, STD, Min, Max) of the transaction amount after cleaning and outlier handling.
