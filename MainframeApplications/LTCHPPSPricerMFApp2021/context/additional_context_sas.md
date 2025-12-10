# Additional Context: Banking Fraud Detection & AML System

## Business Domain
This system implements real-time fraud detection and Anti-Money Laundering (AML) 
transaction monitoring for a retail banking environment.

## Regulatory Requirements
- Bank Secrecy Act (BSA) compliance
- AML transaction monitoring requirements
- Currency Transaction Report (CTR) thresholds: $10,000
- Suspicious Activity Report (SAR) filing obligations

## Business Objectives
1. Detect fraudulent transactions in real-time
2. Identify potential money laundering patterns (structuring, layering)
3. Reduce false positive alert rate
4. Prioritize high-risk cases for investigation
5. Maintain regulatory compliance audit trail

## Key Terminology
- **Structuring**: Breaking large transactions into smaller amounts to avoid reporting
- **Velocity**: Rate of transactions over time window
- **Outlier**: Transaction significantly deviating from customer baseline
- **AML**: Anti-Money Laundering
- **KYC**: Know Your Customer
- **Risk Score**: Combined probability score from rules and ML model

## System Architecture
Sequential data pipeline processing daily transaction batches:
1. Data ingestion from multiple sources
2. Data quality validation and cleaning
3. Feature engineering (velocity, baseline, deviations)
4. Dual detection engines (rule-based + machine learning)
5. Case prioritization and investigation queue generation

## Data Sources
- Daily transaction files (CSV)
- Customer master data
- Historical fraud cases (for ML training)
