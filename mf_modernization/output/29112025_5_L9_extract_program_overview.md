### Program: 01_transaction_data_import

*   **Overview of the Program**
    This program imports transaction data from the daily transaction files (CSV). This is the initial step in the data pipeline, bringing raw data into the system for subsequent processing.

*   **Business Functions Addressed**
    *   Data Ingestion

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   Daily transaction files (CSV) - *Data Source*
    *   **Creates:**
        *   `transactions_raw` - This dataset is likely the raw transaction data imported from the CSV files. This dataset serves as the input for the next step in the pipeline.

### Program: 02_data_quality_cleaning

*   **Overview of the Program**
    This program focuses on data quality validation and cleaning of the imported transaction data. It addresses issues like missing values, incorrect data types, and invalid data based on the defined validation rules.

*   **Business Functions Addressed**
    *   Data Quality Validation
    *   Data Cleaning

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   `transactions_raw` - *Output from 01_transaction_data_import*
    *   **Creates:**
        *   `transactions_cleaned` - This dataset contains the cleaned and validated transaction data, ready for feature engineering.

### Program: 03_feature_engineering

*   **Overview of the Program**
    This program performs feature engineering on the cleaned transaction data. It calculates new variables (features) that will be used for fraud detection, such as transaction velocity, and deviations from customer baselines.

*   **Business Functions Addressed**
    *   Feature Engineering

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   `transactions_cleaned` - *Output from 02_data_quality_cleaning*
    *   **Creates:**
        *   `transactions_enriched` - This dataset contains the original transaction data plus the newly engineered features, which will be used by the detection engines.

### Program: 04_rule_based_detection

*   **Overview of the Program**
    This program implements the rule-based fraud detection engine. It evaluates the `transactions_enriched` dataset against the predefined business rules (e.g., structuring detection, velocity anomaly). It assigns a rule score and identifies potentially fraudulent transactions.

*   **Business Functions Addressed**
    *   Fraud Detection (Rule-Based)

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   `transactions_enriched` - *Output from 03_feature_engineering*
    *   **Creates:**
        *   `transactions_rule_scored` - This dataset contains the transaction data, enriched with the rule-based scores and flags indicating which rules were triggered. This dataset will be used in the final risk scoring.

### Program: 05_ml_scoring_model

*   **Overview of the Program**
    This program applies the machine learning model to the `transactions_enriched` dataset. It uses the engineered features to predict the probability of fraud for each transaction and assigns an ML score based on the model's output.

*   **Business Functions Addressed**
    *   Fraud Detection (Machine Learning)

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   `transactions_enriched` - *Output from 03_feature_engineering*
    *   **Creates:**
        *   `transactions_ml_scored` - This dataset contains the transaction data, enriched with the machine learning model's probability score and associated risk bands. This dataset will be used in the final risk scoring.

### Program: 06_case_management_output

*   **Overview of the Program**
    This program combines the results from both the rule-based and machine learning engines, calculates the final risk score, prioritizes cases for investigation, and generates output for case management.

*   **Business Functions Addressed**
    *   Risk Scoring
    *   Case Prioritization
    *   Output Generation for Investigation Queue

*   **Datasets Created and Consumed, and Data Flow**
    *   **Consumes:**
        *   `transactions_rule_scored` - *Output from 04_rule_based_detection*
        *   `transactions_ml_scored` - *Output from 05_ml_scoring_model*
    *   **Creates:**
        *   `investigation_queue` - This dataset contains the prioritized list of transactions that require further investigation, based on the combined risk scores. This dataset is the primary output of the system, used by investigators.
