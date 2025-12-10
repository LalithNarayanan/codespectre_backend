
# System Requirement Specification (SRS) – School Fee Payment Using NGB Credit Cards

## 1. Introduction
New Gen Bank (NGB), in its pursuit to expand its cards business and explore opportunities in the school sector, proposes a strategic initiative to enable school fee payments via NGB Credit Cards. The pilot will begin with Europe School and support payments through multiple NGB digital channels.

## 2. Scope of Requirement

### Functional Modules
- School Registration
- Student Registration / Amendment / De-registration
- Fee Payment via Online Banking / Mobile Banking / IVR
- Conversion of Fee Payment to Easy Payment Plan (EPP)

## 3. Functional Requirements

### A. School Registration
- UI for Card Operations Team to register schools:
  - School Name
  - Location
  - Account Number
- Product team to send registration data via email (Excel format)
- Configure NGB GL account internally
- Allow registration of multiple fee types per school (e.g., School Fee, Bus Fee)

### B. Student Registration / Amendment / De-registration

#### Via Online/Mobile Banking
- Available to customers with active credit cards
- Register multiple students
- Input fields:
  - Student Name
  - Student ID (entered twice)
  - School (dropdown)
- OTP authentication mandatory
- SMS alerts for registration/amendment/de-registration

#### Via Contact Center (E-Form)
- Authenticate via IVR TIN
- Agent uses E-Form to:
  - Register
  - Amend
  - De-register student
- Manual input fields (based on IVR info)
- Restrict copy-paste on Student ID field
- SMS alerts post-processing

### C. Fee Payment

#### Common Functionalities
- Channels: Online Banking, Mobile Banking, IVR
- Only registered students eligible for payment
- Show all active cards for selection
- Option to convert to EPP
- Transaction logged with unique reference ID
- Confirmation SMS sent

#### Online/Mobile Banking
- Display fee types based on registered school
- Dropdowns for student and fee type
- Optional 20-character remark field
- View history for last 6 months
- EPP conversion triggers E-Form generation

#### IVR
- Authenticate using IVR TIN
- Voice/menu navigation for options
- Optional TTS for student name
- OTP and daily limits configurable
- E-Form created by agent
- Update ICRS with transaction records

### D. Fee Posting
Each transaction must:
- Debit the Credit Card
- Debit GL Account (Visa Conventional / Visa Islamic / MasterCard)
- Credit School Account
- Ensure description format constraints (max 40 characters)
- Postings made individually for each student/fee


## 5. Business Rules
- A school must have a minimum of 1,000 enrolled students to qualify for registration in the NGB fee payment program.
- School Must Be Operational for at Least 3 Years
- The school must generate a minimum annual fee collection of €500,000.
- Only customers with active credit cards can register students
- Student ID must be entered twice and must match
- Payments only allowed for registered students
- Payment fails if card balance is insufficient
- Mandatory SMS notifications for all key activities
- No loyalty points if payment converted to EPP
- Maintain transaction logs with unique reference ID
- Daily limits apply to IVR payments
- EPP request rejected if balance is insufficient at conversion time

## 6. Assumptions
- Schools must have an NGB account to register
- No loyalty points awarded for EPP transactions
- Rejection of EPP due to insufficient balance will be SMS-notified


## 8. Business Units Involved
- Cards Management
- Direct Banking
- Contact Centre

## 9. Systems Involved
- Online Banking
- Mobile Banking
- CRM
- IVR
- Cards System

## 10. Reporting
Auto-generated Excel reports to be emailed to each registered school including:
- School Name & Location
- Student ID & Name
- Amount
- Transaction Date
- Remarks (user-input)

## Appendix
- Sample SMS formats
- Sample Excel Report Format
- UI Wireframes / Prototypes (if available)

---

### Summary

#### ✅ Functional Requirements
- School registration, student management, multichannel fee payment, EPP conversion, fee posting.

#### ✅ Non-Functional Requirements
- Performance, security, scalability, audit compliance, interoperability.

#### ✅ Business Rules
- Active cardholder-only access, validation constraints, transaction traceability, reward conditions.
