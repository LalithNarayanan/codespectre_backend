### Program: SASPOC

*   **Overview of the Program:**
    *   This program serves as a driver program, orchestrating the execution of other macros to read, update, and manage customer data. It initializes, reads data, updates a customer data set, and allocates/deallocates libraries.

*   **Business Functions Addressed:**
    *   Data Loading
    *   Data Integration (merging and updating customer data)
    *   Data Management

*   **Datasets Created and Consumed (Data Flow):**

    1.  **Input:**
        *   `MYLIB.&SYSPARM1..META(&FREQ.INI)`:  This is an input configuration file (INI) read via an include statement. It's likely used to set up metadata or parameters for the program. The specific data within this file isn't defined here.
    2.  **Intermediate:**
        *   `POCOUT`: The dataset created within the `%DREAD` macro. This dataset is created from the input CSV file.
    3.  **Output:**
        *   `OUTPUTP.customer_data`: This dataset is consumed by the `%DUPDATE` macro. It represents the "previous" version of the customer data.  The source of this dataset isn't defined in this program, it is assumed to exist.
        *   `OUTPUT.customer_data`: This dataset is also consumed by the `%DUPDATE` macro. It represents the "new" version of the customer data. The source of this dataset is the `POCOUT` dataset created by the `%DREAD` macro.
        *   `FINAL.customer_data`:  This dataset is the output of the `%DUPDATE` macro, representing the updated customer data.

### Program: DUPDATE

*   **Overview of the Program:**
    *   This macro updates a customer data set, tracking changes and maintaining a history of customer information. It merges a previous and new dataset, identifies changes, and creates new records or closes old ones based on the comparison.

*   **Business Functions Addressed:**
    *   Data Integration
    *   Data Versioning/Auditing (tracking changes over time)

*   **Datasets Created and Consumed (Data Flow):**

    1.  **Input:**
        *   `OUTPUTP.customer_data`:  Represents the previous version of the customer data. (Passed as `prev_ds`).
        *   `OUTPUT.customer_data`: Represents the new version of the customer data. (Passed as `new_ds`).
    2.  **Output:**
        *   `FINAL.customer_data`:  The updated customer data set, created by merging and comparing the input datasets. (Passed as `out_ds`).

### Program: DREAD

*   **Overview of the Program:**
    *   This macro reads data from a pipe-delimited CSV file, assigning attributes and creating a SAS dataset. It also creates an index on the Customer\_ID variable, and conditionally creates an output dataset.

*   **Business Functions Addressed:**
    *   Data Loading
    *   Data Formatting
    *   Data Indexing

*   **Datasets Created and Consumed (Data Flow):**

    1.  **Input:**
        *   `filepath`:  A pipe-delimited CSV file, specified as a macro parameter.
    2.  **Intermediate:**
        *   `customer_data`: A SAS dataset created within the macro, derived from the input CSV file.
    *   `OUTRDP.customer_data`: A SAS dataset created from `customer_data`.
        *   `work.customer_data`: A SAS dataset created from `customer_data`.
    3.  **Output:**
        *   `output.customer_data`: A SAS dataset created from `work.customer_data` if `output.customer_data` does not exist.
