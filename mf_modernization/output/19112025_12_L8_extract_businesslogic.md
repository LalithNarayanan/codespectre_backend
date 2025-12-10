# Step: Program Analysis of LTCAL032

## Program: LTCAL032
### Overview
This COBOL program, `LTCAL032`, is a subroutine designed to calculate Long-Term Care (LTC) payments based on the Prospective Payment System (PPS). It receives billing data, performs edits, assembles pricing variables, calculates payments (including outliers and short stay adjustments), and returns the results. The program uses a copybook `LTDRG031` which contains DRG (Diagnosis Related Group) information.

### Paragraphs and Descriptions in Execution Order
The execution order is determined by the `PERFORM` statements in `0000-MAINLINE-CONTROL`.

- **0000-MAINLINE-CONTROL:**
  - Calls the following paragraphs in sequence:
    - `0100-INITIAL-ROUTINE`
    - `1000-EDIT-THE-BILL-INFO`
    - `1700-EDIT-DRG-CODE` (conditionally)
    - `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
    - `3000-CALC-PAYMENT` (conditionally)
    - `7000-CALC-OUTLIER` (conditionally)
    - `8000-BLEND` (conditionally)
    - `9000-MOVE-RESULTS`
    - `GOBACK`

- **0100-INITIAL-ROUTINE:**
  - Initializes working storage variables:
    - Sets `PPS-RTC` to zeros.
    - Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    - Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
  - `EXIT`.

- **1000-EDIT-THE-BILL-INFO:**
  - Performs data validation on the input bill data:
    - Checks if `B-LOS` is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
    - Checks if `P-NEW-WAIVER-STATE` is true. If so, sets `PPS-RTC` to 53.
    - Checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date or the wage index effective date. If so, sets `PPS-RTC` to 55.
    - Checks if the termination date (`P-NEW-TERMINATION-DATE`) is greater than zero and if the discharge date is after the termination date. If so, sets `PPS-RTC` to 51.
    - Checks if `B-COV-CHARGES` is numeric. If not, sets `PPS-RTC` to 58.
    - Checks if `B-LTR-DAYS` is not numeric or greater than 60. If so, sets `PPS-RTC` to 61.
    - Checks if `B-COV-DAYS` is not numeric or equal to zero and `H-LOS` is greater than 0. If so, sets `PPS-RTC` to 62.
    - Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. If so, sets `PPS-RTC` to 62.
    - Computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
    - Calls `1200-DAYS-USED`.
  - `EXIT`.

- **1200-DAYS-USED:**
  - Calculates the `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS` and `H-LOS`.
  - `EXIT`.

- **1700-EDIT-DRG-CODE:**
  - Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
  - Searches the `WWM-ENTRY` table (from `LTDRG031`) for the matching `PPS-SUBM-DRG-CODE`.
    - If not found, sets `PPS-RTC` to 54.
    - If found, calls `1750-FIND-VALUE`.
  - `EXIT`.

- **1750-FIND-VALUE:**
  - Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the found DRG table entry to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.
  - `EXIT`.

- **2000-ASSEMBLE-PPS-VARIABLES:**
  - Retrieves and validates wage index and provider specific variables based on the discharge date.
    - Checks if `W-WAGE-INDEX1` is numeric and greater than 0, if not, sets `PPS-RTC` to 52.
    - Checks if `P-NEW-OPER-CSTCHG-RATIO` is numeric. If not, sets `PPS-RTC` to 65.
    - Determines the blend year based on `P-NEW-FED-PPS-BLEND-IND`.
    - Sets `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC` based on the blend year.
  - `EXIT`.

- **3000-CALC-PAYMENT:**
  - Calculates the standard payment amount:
    - Moves `P-NEW-COLA` to `PPS-COLA`.
    - Computes `PPS-FAC-COSTS`.
    - Computes `H-LABOR-PORTION` and `H-NONLABOR-PORTION`.
    - Computes `PPS-FED-PAY-AMT`.
    - Computes `PPS-DRG-ADJ-PAY-AMT`.
    - Computes `H-SSOT`.
    - Calls `3400-SHORT-STAY` if `H-LOS` is less than or equal to `H-SSOT`.
  - `EXIT`.

- **3400-SHORT-STAY:**
  - Calculates short-stay costs and payment amounts.
    - Computes `H-SS-COST`.
    - Computes `H-SS-PAY-AMT`.
    - Determines the `PPS-RTC` based on which amount is less and if the amount is less than `PPS-DRG-ADJ-PAY-AMT`.
  - `EXIT`.

- **7000-CALC-OUTLIER:**
  - Calculates outlier payments:
    - Computes `PPS-OUTLIER-THRESHOLD`.
    - If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, computes `PPS-OUTLIER-PAY-AMT`.
    - If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    - Sets `PPS-RTC` to indicate outlier payment status.
    - Adjusts `PPS-LTR-DAYS-USED` if `PPS-RTC` is 00 or 02.
    - Sets `PPS-CHRG-THRESHOLD` and `PPS-RTC` to 67 if certain conditions are met.
  - `EXIT`.

- **8000-BLEND:**
  - Calculates the final payment amount based on blend year:
    - Computes `PPS-DRG-ADJ-PAY-AMT`.
    - Computes `PPS-NEW-FAC-SPEC-RATE`.
    - Computes `PPS-FINAL-PAY-AMT`.
    - Adds `H-BLEND-RTC` to `PPS-RTC`.
  - `EXIT`.

- **9000-MOVE-RESULTS:**
  - Moves the calculated results to the `PPS-DATA-ALL` structure for return to the calling program.
    - If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS`.
    - Moves `V03.2` to `PPS-CALC-VERS-CD`.
    - Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA` and moves `V03.2` to `PPS-CALC-VERS-CD`.
  - `EXIT`.

### Business Rules
- **Data Validation:**
  - Length of Stay (`B-LOS`) must be numeric and greater than 0.
  - Waiver state (`P-NEW-WAIVER-STATE`) is considered.
  - Discharge date must be after the provider's effective date and wage index effective date.
  - Discharge date must be before the termination date, if any.
  - Covered charges (`B-COV-CHARGES`) must be numeric.
  - Lifetime reserve days (`B-LTR-DAYS`) must be numeric and not exceed 60.
  - Covered days (`B-COV-DAYS`) must be numeric, and must be greater than zero if LOS is greater than 0.
  - LTR days cannot be greater than Cov days.
- **Payment Calculation:**
  - Uses DRG information from the `WWM-ENTRY` table (from `LTDRG031`).
  - Applies short-stay adjustments based on the length of stay and average length of stay.
  - Calculates outlier payments if facility costs exceed a threshold.
  - Applies blend factors based on the blend year indicator.

### Data Validation and Error Handling Logic
- **PPS-RTC:** The `PPS-RTC` field is the primary indicator of errors and payment method.
- **Data Validation Errors (PPS-RTC set to a value > 50):**
    - `PPS-RTC = 56`: Invalid Length of Stay (B-LOS not numeric or <=0).
    - `PPS-RTC = 53`: Waiver State.
    - `PPS-RTC = 55`: Discharge date is before provider or wage index effective date.
    - `PPS-RTC = 51`: Discharge date is after provider termination date.
    - `PPS-RTC = 58`: Total covered charges is not numeric.
    - `PPS-RTC = 61`: Lifetime reserve days not numeric or greater than 60.
    - `PPS-RTC = 62`: Invalid number of covered days or LTR-DAYS greater than covered days.
    - `PPS-RTC = 65`: Operating cost-to-charge ratio not numeric.
    - `PPS-RTC = 72`: Invalid blend indicator.
- **Payment Method Indicators (PPS-RTC set to a value < 50):**
    - `PPS-RTC = 00`: Normal DRG payment without outlier.
    - `PPS-RTC = 01`: Normal DRG payment with outlier.
    - `PPS-RTC = 02`: Short stay payment without outlier.
    - `PPS-RTC = 03`: Short stay payment with outlier.
    - `PPS-RTC = 04-19`: Blend year payments.
- **Other Validation:**
    - The program validates numeric fields before using them in calculations.
    - The program searches the DRG table to validate the DRG code.

# Step: Program Analysis of LTCAL042

## Program: LTCAL042
### Overview
This COBOL program, `LTCAL042`, is a subroutine designed to calculate Long-Term Care (LTC) payments based on the Prospective Payment System (PPS). It receives billing data, performs edits, assembles pricing variables, calculates payments (including outliers and short stay adjustments), and returns the results. The program uses a copybook `LTDRG031` which contains DRG (Diagnosis Related Group) information.  Compared to LTCAL032, this version includes a special calculation for a specific provider and adjusts the outlier and blend calculations, including a LOS ratio in the blend calculation.

### Paragraphs and Descriptions in Execution Order
The execution order is determined by the `PERFORM` statements in `0000-MAINLINE-CONTROL`.

- **0000-MAINLINE-CONTROL:**
  - Calls the following paragraphs in sequence:
    - `0100-INITIAL-ROUTINE`
    - `1000-EDIT-THE-BILL-INFO`
    - `1700-EDIT-DRG-CODE` (conditionally)
    - `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
    - `3000-CALC-PAYMENT` (conditionally)
    - `7000-CALC-OUTLIER` (conditionally)
    - `8000-BLEND` (conditionally)
    - `9000-MOVE-RESULTS`
    - `GOBACK`

- **0100-INITIAL-ROUTINE:**
  - Initializes working storage variables:
    - Sets `PPS-RTC` to zeros.
    - Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    - Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
  - `EXIT`.

- **1000-EDIT-THE-BILL-INFO:**
  - Performs data validation on the input bill data:
    - Checks if `B-LOS` is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
    - Checks if `P-NEW-COLA` is numeric. If not, sets `PPS-RTC` to 50.
    - Checks if `P-NEW-WAIVER-STATE` is true. If so, sets `PPS-RTC` to 53.
    - Checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date or the wage index effective date. If so, sets `PPS-RTC` to 55.
    - Checks if the termination date (`P-NEW-TERMINATION-DATE`) is greater than zero and if the discharge date is after the termination date. If so, sets `PPS-RTC` to 51.
    - Checks if `B-COV-CHARGES` is numeric. If not, sets `PPS-RTC` to 58.
    - Checks if `B-LTR-DAYS` is not numeric or greater than 60. If so, sets `PPS-RTC` to 61.
    - Checks if `B-COV-DAYS` is not numeric or equal to zero and `H-LOS` is greater than 0. If so, sets `PPS-RTC` to 62.
    - Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. If so, sets `PPS-RTC` to 62.
    - Computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
    - Calls `1200-DAYS-USED`.
  - `EXIT`.

- **1200-DAYS-USED:**
  - Calculates the `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS` and `H-LOS`.
  - `EXIT`.

- **1700-EDIT-DRG-CODE:**
  - Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
  - Searches the `WWM-ENTRY` table (from `LTDRG031`) for the matching `PPS-SUBM-DRG-CODE`.
    - If not found, sets `PPS-RTC` to 54.
    - If found, calls `1750-FIND-VALUE`.
  - `EXIT`.

- **1750-FIND-VALUE:**
  - Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the found DRG table entry to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.
  - `EXIT`.

- **2000-ASSEMBLE-PPS-VARIABLES:**
  - Retrieves and validates wage index and provider specific variables based on the discharge date.
    - Checks if `P-NEW-FY-BEGIN-DATE >= 20031001` AND `B-DISCHARGE-DATE >= P-NEW-FY-BEGIN-DATE`. Uses `W-WAGE-INDEX2` if true, sets `PPS-RTC` to 52 if not numeric. Otherwise uses `W-WAGE-INDEX1`, sets `PPS-RTC` to 52 if not numeric.
    - Checks if `P-NEW-OPER-CSTCHG-RATIO` is numeric. If not, sets `PPS-RTC` to 65.
    - Determines the blend year based on `P-NEW-FED-PPS-BLEND-IND`.
    - Sets `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC` based on the blend year.
  - `EXIT`.

- **3000-CALC-PAYMENT:**
  - Calculates the standard payment amount:
    - Moves `P-NEW-COLA` to `PPS-COLA`.
    - Computes `PPS-FAC-COSTS`.
    - Computes `H-LABOR-PORTION` and `H-NONLABOR-PORTION`.
    - Computes `PPS-FED-PAY-AMT`.
    - Computes `PPS-DRG-ADJ-PAY-AMT`.
    - Computes `H-SSOT`.
    - Calls `3400-SHORT-STAY` if `H-LOS` is less than or equal to `H-SSOT`.
  - `EXIT`.

- **3400-SHORT-STAY:**
  - Calculates short-stay costs and payment amounts.
    - If provider number `P-NEW-PROVIDER-NO` is '332006', calls `4000-SPECIAL-PROVIDER`.
    - Otherwise Computes `H-SS-COST`.
    - Computes `H-SS-PAY-AMT`.
    - Determines the `PPS-RTC` based on which amount is less and if the amount is less than `PPS-DRG-ADJ-PAY-AMT`.
  - `EXIT`.

- **4000-SPECIAL-PROVIDER:**
  - Special Calculation for Provider '332006'
    - Calculates `H-SS-COST` and `H-SS-PAY-AMT` based on discharge date. Uses different factors based on date ranges (before Jan 1, 2004, and between Jan 1, 2004 and Jan 1, 2005)
  - `EXIT`.

- **7000-CALC-OUTLIER:**
  - Calculates outlier payments:
    - Computes `PPS-OUTLIER-THRESHOLD`.
    - If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, computes `PPS-OUTLIER-PAY-AMT`.
    - If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    - Sets `PPS-RTC` to indicate outlier payment status.
    - Adjusts `PPS-LTR-DAYS-USED` if `PPS-RTC` is 00 or 02.
    - Sets `PPS-CHRG-THRESHOLD` and `PPS-RTC` to 67 if certain conditions are met.
  - `EXIT`.

- **8000-BLEND:**
  - Calculates the final payment amount based on blend year:
    - Computes `H-LOS-RATIO`.
    - Limits `H-LOS-RATIO` to a maximum of 1.
    - Computes `PPS-DRG-ADJ-PAY-AMT`.
    - Computes `PPS-NEW-FAC-SPEC-RATE`. Uses `H-LOS-RATIO` in this calculation.
    - Computes `PPS-FINAL-PAY-AMT`.
    - Adds `H-BLEND-RTC` to `PPS-RTC`.
  - `EXIT`.

- **9000-MOVE-RESULTS:**
  - Moves the calculated results to the `PPS-DATA-ALL` structure for return to the calling program.
    - If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS`.
    - Moves `V04.2` to `PPS-CALC-VERS-CD`.
    - Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA` and moves `V04.2` to `PPS-CALC-VERS-CD`.
  - `EXIT`.

### Business Rules
- **Data Validation:**
  - Length of Stay (`B-LOS`) must be numeric and greater than 0.
  - COLA (`P-NEW-COLA`) must be numeric
  - Waiver state (`P-NEW-WAIVER-STATE`) is considered.
  - Discharge date must be after the provider's effective date and wage index effective date.
  - Discharge date must be before the termination date, if any.
  - Covered charges (`B-COV-CHARGES`) must be numeric.
  - Lifetime reserve days (`B-LTR-DAYS`) must be numeric and not exceed 60.
  - Covered days (`B-COV-DAYS`) must be numeric, and must be greater than zero if LOS is greater than 0.
  - LTR days cannot be greater than Cov days.
- **Payment Calculation:**
  - Uses DRG information from the `WWM-ENTRY` table (from `LTDRG031`).
  - Applies short-stay adjustments based on the length of stay and average length of stay.
  - Calculates outlier payments if facility costs exceed a threshold.
  - Applies blend factors based on the blend year indicator.
    - Includes a specific calculation for provider '332006'.
    - Uses a `H-LOS-RATIO` in the blend calculation.

### Data Validation and Error Handling Logic
- **PPS-RTC:** The `PPS-RTC` field is the primary indicator of errors and payment method.
- **Data Validation Errors (PPS-RTC set to a value > 50):**
    - `PPS-RTC = 56`: Invalid Length of Stay (B-LOS not numeric or <=0).
    - `PPS-RTC = 50`:  COLA is not numeric.
    - `PPS-RTC = 53`: Waiver State.
    - `PPS-RTC = 55`: Discharge date is before provider or wage index effective date.
    - `PPS-RTC = 51`: Discharge date is after provider termination date.
    - `PPS-RTC = 58`: Total covered charges is not numeric.
    - `PPS-RTC = 61`: Lifetime reserve days not numeric or greater than 60.
    - `PPS-RTC = 62`: Invalid number of covered days or LTR-DAYS greater than covered days.
    - `PPS-RTC = 65`: Operating cost-to-charge ratio not numeric.
    - `PPS-RTC = 72`: Invalid blend indicator.
- **Payment Method Indicators (PPS-RTC set to a value < 50):**
    - `PPS-RTC = 00`: Normal DRG payment without outlier.
    - `PPS-RTC = 01`: Normal DRG payment with outlier.
    - `PPS-RTC = 02`: Short stay payment without outlier.
    - `PPS-RTC = 03`: Short stay payment with outlier.
    - `PPS-RTC = 04-19`: Blend year payments.
- **Other Validation:**
    - The program validates numeric fields before using them in calculations.
    - The program searches the DRG table to validate the DRG code.

# Step: Program Analysis of LTDRG031

## Program: LTDRG031
### Overview
This is a COBOL copybook, not a program. It contains a table (`W-DRG-TABLE`) of DRG (Diagnosis Related Group) codes and associated data, used for calculating payments in the LTCAL programs.  The table is defined using the `OCCURS` clause, allowing for efficient searching using the `SEARCH ALL` verb in COBOL.

### Data Structures
- **W-DRG-FILLS:** A group of `PIC X(44)` fields, used to store the DRG table data.
- **W-DRG-TABLE:**  A redefinition of `W-DRG-FILLS`, providing the structure for accessing the DRG data:
    - **WWM-ENTRY:** An `OCCURS 502 TIMES` structure representing each DRG entry.
        - **WWM-DRG:**  The 3-character DRG code (key).
        - **WWM-RELWT:** The relative weight for the DRG.
        - **WWM-ALOS:** The average length of stay for the DRG.

### Business Rules
- The copybook stores the DRG codes and their corresponding relative weights and average lengths of stay.
- This information is used by the calling programs (LTCAL032, LTCAL042) to calculate payments based on the DRG code.

### Data Validation and Error Handling Logic
- The data itself is assumed to be validated when it is populated.
- The calling programs are responsible for validating the DRG code against the table. If a match is not found, the calling program sets an error code (PPS-RTC = 54 in LTCAL032 and LTCAL042).

# Summary
- **LTCAL032:** Calculates LTC payments.  Performs data validation, DRG lookup, short-stay calculations, outlier calculations, and blend year calculations.  It uses `LTDRG031` for DRG information.  Error handling is primarily through the `PPS-RTC` field.
- **LTCAL042:** A modified version of LTCAL032. It includes a special calculation for a specific provider and incorporates a LOS ratio in the blend calculation. It uses `LTDRG031` for DRG information. Error handling is primarily through the `PPS-RTC` field.
- **LTDRG031:** A copybook that contains the DRG table used by LTCAL032 and LTCAL042.  It stores DRG codes, relative weights, and average lengths of stay.
