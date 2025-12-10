## Program Name: 01_transaction_data_import

**Purpose**: This program imports transaction data from an external source into SAS, likely creating a SAS dataset for subsequent analysis.

**Business Functions**:
- Data Ingestion
- Data Preparation

**Key Datasets**:
- Input: transaction_data.csv (source: external system, e.g., a database or file server)
- Output: transactions (purpose: stores the imported transaction data in a SAS dataset)

**Dependencies**: None. This is likely the starting point of the data pipeline.

---

## Program Name: 02_data_quality_cleaning

**Purpose**: This program cleans and validates the imported transaction data, addressing data quality issues such as missing values, inconsistencies, and outliers.

**Business Functions**:
- Data Cleansing
- Data Validation

**Key Datasets**:
- Input: transactions (source: Program 01_transaction_data_import)
- Output: cleaned_transactions (purpose: stores the cleaned and validated transaction data)

**Dependencies**: 01_transaction_data_import (as it uses the output of that program as input)

---

## Program Name: 03_feature_engineering

**Purpose**: This program creates new variables (features) from the existing data to enhance the analytical capabilities of the dataset, potentially improving the performance of fraud detection models.

**Business Functions**:
- Feature Creation
- Data Enrichment

**Key Datasets**:
- Input: cleaned_transactions (source: Program 02_data_quality_cleaning)
- Output: engineered_transactions (purpose: stores the transaction data with added features)

**Dependencies**: 02_data_quality_cleaning (as it uses the output of that program as input)

---

## Program Name: 04_rule_based_detection

**Purpose**: This program applies predefined business rules to identify potentially fraudulent transactions based on specific criteria.

**Business Functions**:
- Rule-Based Fraud Detection
- Alert Generation

**Key Datasets**:
- Input: engineered_transactions (source: Program 03_feature_engineering)
- Output: rule_based_alerts (purpose: stores the transactions flagged as potentially fraudulent by the rules)

**Dependencies**: 03_feature_engineering (as it uses the output of that program as input)

---

## Program Name: 05_ml_scoring_model

**Purpose**: This program applies a pre-trained machine learning model to score transactions for fraud risk and identify potentially fraudulent transactions.

**Business Functions**:
- Machine Learning-Based Fraud Detection
- Risk Scoring

**Key Datasets**:
- Input: engineered_transactions (source: Program 03_feature_engineering), trained_model (source: from a separate model training process, stored in a SAS format)
- Output: ml_scored_transactions (purpose: stores the transactions with fraud risk scores assigned by the model)

**Dependencies**: 03_feature_engineering (as it uses the output of that program as input), a separately trained machine learning model.

---

## Program Name: 06_case_management_output

**Purpose**: This program consolidates the results from the rule-based and machine learning detection programs and prepares output for case management, enabling further investigation of potentially fraudulent transactions.

**Business Functions**:
- Alert Aggregation
- Case Prioritization
- Reporting

**Key Datasets**:
- Input: rule_based_alerts (source: Program 04_rule_based_detection), ml_scored_transactions (source: Program 05_ml_scoring_model)
- Output: case_management_data (purpose: stores the consolidated data for case management and reporting)

**Dependencies**: 04_rule_based_detection and 05_ml_scoring_model (as it uses the outputs of those programs as inputs).
