# Fraud Detection Business Rules

## Rule-Based Detection Scenarios

### Rule 1: Structuring Detection
**Definition**: Multiple transactions just below CTR threshold ($10,000)
**Threshold**: 3+ transactions between $9,000-$10,000 within 24 hours
**Severity**: HIGH
**Score Weight**: 40 points

### Rule 2: Velocity Anomaly
**Definition**: Unusual transaction frequency
**Threshold**: 5+ transactions totaling >$50,000 within 24 hours
**Severity**: HIGH
**Score Weight**: 35 points

### Rule 3: Dormant Account Activity
**Definition**: Long-inactive account suddenly active with high value
**Threshold**: Account inactive >180 days, <5 historical transactions, new transaction >$10,000
**Severity**: MEDIUM
**Score Weight**: 30 points

### Rule 4: High-Risk Geography
**Definition**: First transaction to high-risk country
**Threshold**: International transaction to sanctioned/high-risk jurisdiction, no prior international history
**Severity**: HIGH
**Score Weight**: 45 points

### Rule 5: Amount Deviation
**Definition**: Transaction significantly exceeds customer baseline
**Threshold**: >3 standard deviations from historical average
**Severity**: MEDIUM
**Score Weight**: 25 points

### Rule 6: New Account Risk
**Definition**: High-value activity on newly opened account
**Threshold**: Account age <30 days, transaction >$20,000
**Severity**: MEDIUM
**Score Weight**: 30 points

### Rule 7: Geographic Dispersion
**Definition**: Transactions across multiple countries rapidly
**Threshold**: 3+ different countries within 24 hours
**Severity**: HIGH
**Score Weight**: 35 points

### Rule 8: Timing Anomaly
**Definition**: Large transaction during unusual hours
**Threshold**: Transaction >2x average amount during 10PM-6AM
**Severity**: LOW
**Score Weight**: 15 points

## Machine Learning Model

### Model Type
Logistic Regression for fraud probability prediction

### Input Features
- Amount Z-score
- Transaction count (24h)
- Account age
- International flag
- Country count (24h)
- Amount deviation ratio
- Unusual timing indicator
- Rapid succession flag
- Round amount indicator

### Risk Bands
- CRITICAL: ML probability ≥ 0.70 (score: 90)
- HIGH: ML probability ≥ 0.50 (score: 70)
- MEDIUM: ML probability ≥ 0.30 (score: 50)
- LOW: ML probability ≥ 0.15 (score: 30)
- MINIMAL: ML probability < 0.15 (score: 10)

## Combined Scoring
Final Risk Score = (Rule Score × 0.4) + (ML Score × 0.6)

## Investigation Priorities
- P1 (IMMEDIATE): Combined score ≥ 75, auto-block transaction
- P2 (URGENT): Combined score ≥ 60
- P3 (STANDARD): Combined score ≥ 45
- P4 (REVIEW): Combined score < 45
