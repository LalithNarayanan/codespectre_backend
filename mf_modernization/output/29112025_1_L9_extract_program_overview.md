## Program Name: 01_transaction_data_import

**Purpose**: This program imports transaction data from an external source into SAS datasets. It likely performs initial data loading and may include basic data type conversions.

**Business Functions**:
- Data Ingestion
- Data Preparation

**Key Datasets**:
- Input: external_transaction_file (source: Database, CSV file, or other external source)
- Output: raw_transaction_data (purpose: Stores the imported transaction data for further processing)

**Dependencies**: None
---

## Program Name: 02_data_quality_cleaning

**Purpose**: This program focuses on data quality by cleaning and validating the imported transaction data. It addresses missing values, inconsistencies, and other data quality issues.

**Business Functions**:
- Data Cleaning
- Data Validation

**Key Datasets**:
- Input: raw_transaction_data (source: from 01_transaction_data_import)
- Output: cleaned_transaction_data (purpose: Stores the cleaned and validated transaction data)

**Dependencies**: 01_transaction_data_import
---

## Program Name: 03_feature_engineering

**Purpose**: This program creates new variables (features) from the cleaned transaction data. These new features are designed to improve the performance of predictive models or rule-based detection systems.

**Business Functions**:
- Feature Creation
- Data Transformation

**Key Datasets**:
- Input: cleaned_transaction_data (source: from 02_data_quality_cleaning)
- Output: engineered_transaction_data (purpose: Stores the transaction data with added features)

**Dependencies**: 02_data_quality_cleaning
---

## Program Name: 04_rule_based_detection

**Purpose**: This program applies predefined business rules to the engineered transaction data to identify potentially fraudulent or suspicious transactions.

**Business Functions**:
- Fraud Detection
- Rule Application

**Key Datasets**:
- Input: engineered_transaction_data (source: from 03_feature_engineering)
- Output: rule_based_alerts (purpose: Stores the output of rule-based detection, including alerts and associated details)

**Dependencies**: 03_feature_engineering
---

## Program Name: 05_ml_scoring_model

**Purpose**: This program applies a pre-trained machine learning model to the engineered transaction data to predict the likelihood of fraud for each transaction.

**Business Functions**:
- Predictive Modeling
- Fraud Scoring

**Key Datasets**:
- Input: engineered_transaction_data (source: from 03_feature_engineering)
- Output: ml_model_scoring_results (purpose: Stores the output of the ML model, including fraud scores)

**Dependencies**: 03_feature_engineering, a pre-trained ML model (likely stored in a separate location or library)
---

## Program Name: 06_case_management_output

**Purpose**: This program consolidates the results from rule-based detection and the machine learning model, and generates output suitable for case management and further investigation.

**Business Functions**:
- Alert Aggregation
- Reporting

**Key Datasets**:
- Input: rule_based_alerts (source: from 04_rule_based_detection), ml_model_scoring_results (source: from 05_ml_scoring_model)
- Output: case_management_data (purpose: Stores aggregated alerts and scores for case management review and investigation)

**Dependencies**: 04_rule_based_detection, 05_ml_scoring_model
