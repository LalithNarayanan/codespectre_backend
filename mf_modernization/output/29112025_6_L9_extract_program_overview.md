### Program: 01_transaction_data_import

#### Overview of the Program

This program focuses on importing raw transaction data from an external source (CSV file, presumably) into SAS datasets. It likely performs basic data type conversions and potentially initial validation checks as well.

#### Business Functions Addressed

*   Data Ingestion: Reads transaction data from a source file.
*   Data Quality: Performs initial validation to ensure data integrity.

#### Datasets Created and Consumed

*   **Consumes:**
    *   Daily transaction files (CSV): The input data source.
*   **Creates:**
    *   `transactions_raw`: A SAS dataset containing the raw transaction data.

#### Data Flow

1.  Read data from the daily transaction files (CSV).
2.  Create the `transactions_raw` SAS dataset.

---

### Program: 02_data_quality_cleaning

#### Overview of the Program

This program focuses on improving the quality of the raw transaction data. It performs data cleaning tasks to handle missing values, correct inconsistencies, and standardize data formats. Data validation rules will be applied to ensure the data adheres to predefined standards.

#### Business Functions Addressed

*   Data Quality: Cleans and validates the imported data.

#### Datasets Created and Consumed

*   **Consumes:**
    *   `transactions_raw`: The raw transaction data from the previous step.
    *   `customer_master`: Customer data containing KYC information.
*   **Creates:**
    *   `transactions_cleaned`: A SAS dataset containing the cleaned and validated transaction data.

#### Data Flow

1.  Reads the `transactions_raw` dataset.
2.  Reads the `customer_master` dataset.
3.  Performs data cleaning and validation on the transaction data.
4.  Creates the `transactions_cleaned` SAS dataset.

---

### Program: 03_feature_engineering

#### Overview of the Program

This program calculates new variables (features) from the cleaned transaction data. These engineered features are designed to improve the performance of fraud detection rules and machine learning models.

#### Business Functions Addressed

*   Feature Engineering: Creates new variables based on existing data.

#### Datasets Created and Consumed

*   **Consumes:**
    *   `transactions_cleaned`: The cleaned transaction data.
*   **Creates:**
    *   `transactions_engineered`: A SAS dataset containing the original data plus the engineered features.

#### Data Flow

1.  Reads the `transactions_cleaned` dataset.
2.  Calculates new features (e.g., velocity, amount deviation, etc.) based on the business rules.
3.  Creates the `transactions_engineered` SAS dataset.

---

### Program: 04_rule_based_detection

#### Overview of the Program

This program implements the rule-based fraud detection engine. It evaluates the engineered transaction data against predefined rules to identify potentially fraudulent transactions.  Each rule will assign a score and severity level based on the rule definitions.

#### Business Functions Addressed

*   Fraud Detection: Implements rule-based detection.
*   Risk Assessment: Assigns risk scores based on rule violations.

#### Datasets Created and Consumed

*   **Consumes:**
    *   `transactions_engineered`: The dataset containing engineered features.
*   **Creates:**
    *   `transactions_rule_scored`: A SAS dataset containing the transaction data and rule-based scores.

#### Data Flow

1.  Reads the `transactions_engineered` dataset.
2.  Applies the fraud detection rules.
3.  Calculates rule-based scores for each transaction.
4.  Creates the `transactions_rule_scored` dataset.

---

### Program: 05_ml_scoring_model

#### Overview of the Program

This program applies a pre-trained machine learning model (e.g., logistic regression) to the transaction data. The model predicts the probability of fraud for each transaction, and assigns a risk score.

#### Business Functions Addressed

*   Fraud Detection: Implements machine learning-based detection.
*   Risk Assessment: Assigns risk scores based on ML model predictions.

#### Datasets Created and Consumed

*   **Consumes:**
    *   `transactions_engineered`: The dataset containing engineered features.
*   **Creates:**
    *   `transactions_ml_scored`: A SAS dataset containing the transaction data and machine learning-based scores.

#### Data Flow

1.  Reads the `transactions_engineered` dataset.
2.  Applies the pre-trained machine learning model.
3.  Calculates ML-based scores for each transaction.
4.  Creates the `transactions_ml_scored` dataset.

---

### Program: 06_case_management_output

#### Overview of the Program

This program combines the results from the rule-based and machine learning detection engines. It calculates a combined risk score, prioritizes cases for investigation, and generates output for case management.

#### Business Functions Addressed

*   Case Prioritization: Prioritizes cases based on combined risk scores.
*   Reporting and Alerting: Generates output for case management and potential alerts.

#### Datasets Created and Consumed

*   **Consumes:**
    *   `transactions_rule_scored`: The dataset containing rule-based scores.
    *   `transactions_ml_scored`: The dataset containing machine learning-based scores.
*   **Creates:**
    *   `investigation_queue`: A SAS dataset containing prioritized cases for investigation.

#### Data Flow

1.  Reads the `transactions_rule_scored` and `transactions_ml_scored` datasets.
2.  Combines rule-based and ML scores to calculate a combined risk score.
3.  Prioritizes cases based on the combined risk score.
4.  Creates the `investigation_queue` dataset.
