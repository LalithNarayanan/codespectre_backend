# Step 1: Program Overview

## Program: LTCAL032
### Overview
This COBOL program, `LTCAL032`, is a subroutine designed to calculate Long Term Care (LTC) payments based on the Prospective Payment System (PPS) for DRGs. It receives billing data, performs edits, assembles pricing components, calculates payments, and determines outlier payments. It returns a return code (PPS-RTC) indicating how the bill was paid.  This version is effective January 1, 2003, and uses the `LTDRG031` copybook for DRG-related data.

### Paragraphs in Execution Order and Descriptions
-   **0000-MAINLINE-CONTROL:**
    -   Calls the following paragraphs in sequence:
        -   `0100-INITIAL-ROUTINE`
        -   `1000-EDIT-THE-BILL-INFO`
        -   `1700-EDIT-DRG-CODE` (conditionally)
        -   `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
        -   `3000-CALC-PAYMENT` (conditionally)
        -   `7000-CALC-OUTLIER` (conditionally)
        -   `8000-BLEND` (conditionally)
        -   `9000-MOVE-RESULTS`
        -   `GOBACK`

-   **0100-INITIAL-ROUTINE:**
    -   Initializes working storage variables.
    -   Sets default values for national labor/non-labor percentages, standard federal rate, fixed loss amount, and budget neutrality rate.

-   **1000-EDIT-THE-BILL-INFO:**
    -   Performs edits on the input bill data.
        -   Checks if `B-LOS` is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
        -   Checks if `P-NEW-WAIVER-STATE` is true. Sets `PPS-RTC` to 53 if true.
        -   Checks if the discharge date is before the effective date or wage index effective date. Sets `PPS-RTC` to 55 if true.
        -   Checks if termination date is valid, and if the discharge date is greater than or equal to the termination date. Sets `PPS-RTC` to 51 if true.
        -   Checks if `B-COV-CHARGES` is numeric. Sets `PPS-RTC` to 58 if not.
        -   Checks if `B-LTR-DAYS` is numeric or greater than 60. Sets `PPS-RTC` to 61 if true.
        -   Checks if `B-COV-DAYS` is not numeric or if it's 0 and `H-LOS` > 0. Sets `PPS-RTC` to 62 if true.
        -   Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. Sets `PPS-RTC` to 62 if true.
        -   Computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
        -   Calls `1200-DAYS-USED`.

-   **1200-DAYS-USED:**
    -   Calculates the number of days used for regular and lifetime reserve days based on the values of `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.

-   **1700-EDIT-DRG-CODE:**
    -   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    -   Searches the `WWM-ENTRY` table (from `LTDRG031`) for a matching `WWM-DRG`.
    -   If not found, sets `PPS-RTC` to 54.
    -   If found, calls `1750-FIND-VALUE`.

-   **1750-FIND-VALUE:**
    -   Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the `WWM-ENTRY` table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.

-   **2000-ASSEMBLE-PPS-VARIABLES:**
    -   Retrieves and validates the wage index (`W-WAGE-INDEX1`). Sets `PPS-RTC` to 52 if invalid and exits.
    -   Validates `P-NEW-OPER-CSTCHG-RATIO`. Sets `PPS-RTC` to 65 if invalid.
    -   Determines the blend year (`PPS-BLEND-YEAR`) from `P-NEW-FED-PPS-BLEND-IND`.
    -   Validates `PPS-BLEND-YEAR`. Sets `PPS-RTC` to 72 if invalid and exits.
    -   Sets blend factors and return code based on the `PPS-BLEND-YEAR`.

-   **3000-CALC-PAYMENT:**
    -   Moves `P-NEW-COLA` to `PPS-COLA`.
    -   Computes `PPS-FAC-COSTS`.
    -   Computes `H-LABOR-PORTION`, `H-NONLABOR-PORTION`, `PPS-FED-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `H-SSOT`.
    -   Calls `3400-SHORT-STAY` if `H-LOS` is less than or equal to `H-SSOT`.

-   **3400-SHORT-STAY:**
    -   Calculates short stay cost (`H-SS-COST`) and short stay payment amount (`H-SS-PAY-AMT`).
    -   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` and moves the minimum value to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02 if a short stay payment is applicable.

-   **7000-CALC-OUTLIER:**
    -   Computes the outlier threshold (`PPS-OUTLIER-THRESHOLD`).
    -   Computes the outlier payment amount (`PPS-OUTLIER-PAY-AMT`) if `PPS-FAC-COSTS` exceeds the threshold.
    -   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    -   Sets `PPS-RTC` to 03 or 01 based on outlier payment eligibility.
    -   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED`, `H-SSOT` and `PPS-RTC`.
    -   If `PPS-RTC` is 01 or 03, and certain conditions are met, computes `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.

-   **8000-BLEND:**
    -   Computes `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    -   Adds `H-BLEND-RTC` to `PPS-RTC`.

-   **9000-MOVE-RESULTS:**
    -   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V03.2'.
    -   Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V03.2'.

### Business Rules
-   Payment calculation based on DRG, length of stay, and other factors.
-   Outlier payments are calculated if the facility costs exceed a threshold.
-   Short-stay payments are calculated if the length of stay is less than or equal to 5/6 of the average length of stay.
-   Blended payment methodologies are applied based on the provider's blend year.
-   Various edits and validations are performed on the input data.

### Data Validation and Error Handling Logic
-   **Data Type and Range Checks:**
    -   `B-LOS` must be numeric and greater than 0 (sets `PPS-RTC` to 56).
    -   `B-COV-CHARGES` must be numeric (sets `PPS-RTC` to 58).
    -   `B-LTR-DAYS` must be numeric and less than or equal to 60 (sets `PPS-RTC` to 61).
    -   `B-COV-DAYS` must be numeric, and if `B-COV-DAYS` is 0, then `H-LOS` must also be 0 (sets `PPS-RTC` to 62).
    -   `PPS-BLEND-YEAR` must be between 1 and 5 (sets `PPS-RTC` to 72).
    -   `W-WAGE-INDEX1` must be numeric and greater than 0 (sets `PPS-RTC` to 52).
    -   `P-NEW-OPER-CSTCHG-RATIO` must be numeric (sets `PPS-RTC` to 65).
    -   `P-NEW-COLA` must be numeric (sets `PPS-RTC` to 50).
-   **Date Validations:**
    -   Discharge date must be after the provider's effective date and the wage index effective date (sets `PPS-RTC` to 55).
    -   Discharge date must be before the provider's termination date (sets `PPS-RTC` to 51).
-   **Table Lookups:**
    -   DRG code must be found in the DRG table (sets `PPS-RTC` to 54).
-   **Logic Checks:**
    -   If `P-NEW-WAIVER-STATE` is true, sets `PPS-RTC` to 53.
    -   If `B-LTR-DAYS` is greater than `B-COV-DAYS`, sets `PPS-RTC` to 62.
-   **Error Codes (PPS-RTC):**
    -   50: `PROVIDER SPECIFIC RATE OR COLA NOT NUMERIC`
    -   51: `PROVIDER RECORD TERMINATED`
    -   52: `INVALID WAGE INDEX`
    -   53: `WAIVER STATE - NOT CALCULATED BY PPS`
    -   54: `DRG ON CLAIM NOT FOUND IN TABLE`
    -   55: `DISCHARGE DATE < PROVIDER EFF START DATE OR DISCHARGE DATE < MSA EFF START DATE FOR PPS`
    -   56: `INVALID LENGTH OF STAY`
    -   58: `TOTAL COVERED CHARGES NOT NUMERIC`
    -   61: `LIFETIME RESERVE DAYS NOT NUMERIC OR BILL-LTR-DAYS > 60`
    -   62: `INVALID NUMBER OF COVERED DAYS OR BILL-LTR-DAYS > COVERED DAYS`
    -   65: `OPERATING COST-TO-CHARGE RATIO NOT NUMERIC`
    -   67: `COST OUTLIER WITH LOS > COVERED DAYS OR COST OUTLIER THRESHOLD CALCULATION`
    -   72: `INVALID BLEND INDICATOR (NOT 1 THRU 5)`

## Program: LTCAL042
### Overview
This COBOL program, `LTCAL042`, is another subroutine designed to calculate Long Term Care (LTC) payments based on the Prospective Payment System (PPS) for DRGs. It is very similar to `LTCAL032` but has some differences.  It receives billing data, performs edits, assembles pricing components, calculates payments, and determines outlier payments. It returns a return code (PPS-RTC) indicating how the bill was paid.  This version is effective July 1, 2003, and uses the `LTDRG031` copybook for DRG-related data.

### Paragraphs in Execution Order and Descriptions
-   **0000-MAINLINE-CONTROL:**
    -   Calls the following paragraphs in sequence:
        -   `0100-INITIAL-ROUTINE`
        -   `1000-EDIT-THE-BILL-INFO`
        -   `1700-EDIT-DRG-CODE` (conditionally)
        -   `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
        -   `3000-CALC-PAYMENT` (conditionally)
        -   `7000-CALC-OUTLIER` (conditionally)
        -   `8000-BLEND` (conditionally)
        -   `9000-MOVE-RESULTS`
        -   `GOBACK`

-   **0100-INITIAL-ROUTINE:**
    -   Initializes working storage variables.
    -   Sets default values for national labor/non-labor percentages, standard federal rate, fixed loss amount, and budget neutrality rate.

-   **1000-EDIT-THE-BILL-INFO:**
    -   Performs edits on the input bill data.
        -   Checks if `B-LOS` is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
        -   Checks if `P-NEW-COLA` is numeric. Sets `PPS-RTC` to 50 if not.
        -   Checks if `P-NEW-WAIVER-STATE` is true. Sets `PPS-RTC` to 53 if true.
        -   Checks if the discharge date is before the effective date or wage index effective date. Sets `PPS-RTC` to 55 if true.
        -   Checks if termination date is valid, and if the discharge date is greater than or equal to the termination date. Sets `PPS-RTC` to 51 if true.
        -   Checks if `B-COV-CHARGES` is numeric. Sets `PPS-RTC` to 58 if not.
        -   Checks if `B-LTR-DAYS` is numeric or greater than 60. Sets `PPS-RTC` to 61 if true.
        -   Checks if `B-COV-DAYS` is not numeric or if it's 0 and `H-LOS` > 0. Sets `PPS-RTC` to 62 if true.
        -   Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. Sets `PPS-RTC` to 62 if true.
        -   Computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
        -   Calls `1200-DAYS-USED`.

-   **1200-DAYS-USED:**
    -   Calculates the number of days used for regular and lifetime reserve days based on the values of `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.

-   **1700-EDIT-DRG-CODE:**
    -   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    -   Searches the `WWM-ENTRY` table (from `LTDRG031`) for a matching `WWM-DRG`.
    -   If not found, sets `PPS-RTC` to 54.
    -   If found, calls `1750-FIND-VALUE`.

-   **1750-FIND-VALUE:**
    -   Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the `WWM-ENTRY` table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.

-   **2000-ASSEMBLE-PPS-VARIABLES:**
    -   The logic has been updated to check for the fiscal year begin date and discharge date to determine the correct wage index to use.
        -   If `P-NEW-FY-BEGIN-DATE` is greater than or equal to 20031001 AND `B-DISCHARGE-DATE` is greater than or equal to `P-NEW-FY-BEGIN-DATE`, then it uses `W-WAGE-INDEX2`.
        -   Otherwise, it uses `W-WAGE-INDEX1`.
    -   Retrieves and validates the wage index (`W-WAGE-INDEX1` or `W-WAGE-INDEX2`). Sets `PPS-RTC` to 52 if invalid and exits.
    -   Validates `P-NEW-OPER-CSTCHG-RATIO`. Sets `PPS-RTC` to 65 if invalid.
    -   Determines the blend year (`PPS-BLEND-YEAR`) from `P-NEW-FED-PPS-BLEND-IND`.
    -   Validates `PPS-BLEND-YEAR`. Sets `PPS-RTC` to 72 if invalid and exits.
    -   Sets blend factors and return code based on the `PPS-BLEND-YEAR`.

-   **3000-CALC-PAYMENT:**
    -   Moves `P-NEW-COLA` to `PPS-COLA`.
    -   Computes `PPS-FAC-COSTS`.
    -   Computes `H-LABOR-PORTION`, `H-NONLABOR-PORTION`, `PPS-FED-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `H-SSOT`.
    -   Calls `3400-SHORT-STAY` if `H-LOS` is less than or equal to `H-SSOT`.

-   **3400-SHORT-STAY:**
    -   If `P-NEW-PROVIDER-NO` is equal to '332006', calls `4000-SPECIAL-PROVIDER`.
    -   Otherwise, calculates short stay cost (`H-SS-COST`) and short stay payment amount (`H-SS-PAY-AMT`).
    -   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` and moves the minimum value to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02 if a short stay payment is applicable.

-   **4000-SPECIAL-PROVIDER:**
    -   Applies special calculation for provider '332006' based on discharge date.
        -   If `B-DISCHARGE-DATE` is between 20030701 and 20040101, applies a factor of 1.95.
        -   If `B-DISCHARGE-DATE` is between 20040101 and 20050101, applies a factor of 1.93.

-   **7000-CALC-OUTLIER:**
    -   Computes the outlier threshold (`PPS-OUTLIER-THRESHOLD`).
    -   Computes the outlier payment amount (`PPS-OUTLIER-PAY-AMT`) if `PPS-FAC-COSTS` exceeds the threshold.
    -   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    -   Sets `PPS-RTC` to 03 or 01 based on outlier payment eligibility.
    -   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED`, `H-SSOT` and `PPS-RTC`.
    -   If `PPS-RTC` is 01 or 03, and certain conditions are met, computes `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.

-   **8000-BLEND:**
    -   Computes `H-LOS-RATIO`.
    -   Computes `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    -   Adds `H-BLEND-RTC` to `PPS-RTC`.

-   **9000-MOVE-RESULTS:**
    -   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V04.2'.
    -   Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V04.2'.

### Business Rules
-   Payment calculation based on DRG, length of stay, and other factors.
-   Outlier payments are calculated if the facility costs exceed a threshold.
-   Short-stay payments are calculated if the length of stay is less than or equal to 5/6 of the average length of stay.
-   Blended payment methodologies are applied based on the provider's blend year.
-   Special payment rules apply for provider '332006' based on discharge date.
-   Various edits and validations are performed on the input data.

### Data Validation and Error Handling Logic
-   **Data Type and Range Checks:**
    -   `B-LOS` must be numeric and greater than 0 (sets `PPS-RTC` to 56).
    -   `B-COV-CHARGES` must be numeric (sets `PPS-RTC` to 58).
    -   `B-LTR-DAYS` must be numeric and less than or equal to 60 (sets `PPS-RTC` to 61).
    -   `B-COV-DAYS` must be numeric, and if `B-COV-DAYS` is 0, then `H-LOS` must also be 0 (sets `PPS-RTC` to 62).
    -   `PPS-BLEND-YEAR` must be between 1 and 5 (sets `PPS-RTC` to 72).
    -   `W-WAGE-INDEX1` and `W-WAGE-INDEX2` must be numeric and greater than 0 (sets `PPS-RTC` to 52).
    -   `P-NEW-OPER-CSTCHG-RATIO` must be numeric (sets `PPS-RTC` to 65).
    -   `P-NEW-COLA` must be numeric (sets `PPS-RTC` to 50).
-   **Date Validations:**
    -   Discharge date must be after the provider's effective date and the wage index effective date (sets `PPS-RTC` to 55).
    -   Discharge date must be before the provider's termination date (sets `PPS-RTC` to 51).
-   **Table Lookups:**
    -   DRG code must be found in the DRG table (sets `PPS-RTC` to 54).
-   **Logic Checks:**
    -   If `P-NEW-WAIVER-STATE` is true, sets `PPS-RTC` to 53.
    -   If `B-LTR-DAYS` is greater than `B-COV-DAYS`, sets `PPS-RTC` to 62.
-   **Error Codes (PPS-RTC):**
    -   50: `PROVIDER SPECIFIC RATE OR COLA NOT NUMERIC`
    -   51: `PROVIDER RECORD TERMINATED`
    -   52: `INVALID WAGE INDEX`
    -   53: `WAIVER STATE - NOT CALCULATED BY PPS`
    -   54: `DRG ON CLAIM NOT FOUND IN TABLE`
    -   55: `DISCHARGE DATE < PROVIDER EFF START DATE OR DISCHARGE DATE < MSA EFF START DATE FOR PPS`
    -   56: `INVALID LENGTH OF STAY`
    -   58: `TOTAL COVERED CHARGES NOT NUMERIC`
    -   61: `LIFETIME RESERVE DAYS NOT NUMERIC OR BILL-LTR-DAYS > 60`
    -   62: `INVALID NUMBER OF COVERED DAYS OR BILL-LTR-DAYS > COVERED DAYS`
    -   65: `OPERATING COST-TO-CHARGE RATIO NOT NUMERIC`
    -   67: `COST OUTLIER WITH LOS > COVERED DAYS OR COST OUTLIER THRESHOLD CALCULATION`
    -   72: `INVALID BLEND INDICATOR (NOT 1 THRU 5)`

## Program: LTDRG031
### Overview
This is a `COPY` member, which means it's not a standalone program but a collection of data definitions. It contains a table (`W-DRG-TABLE`) that holds DRG codes, relative weights, and average lengths of stay.  This data is used by `LTCAL032` and `LTCAL042`.

### Data Definition
-   **W-DRG-FILLS:** A group of PIC X(44) fields containing the DRG data, used to initialize the `W-DRG-TABLE`.
-   **W-DRG-TABLE:**  A table defined using `W-DRG-FILLS` and `REDEFINES`.
    -   **WWM-ENTRY:**  An OCCURS clause defining an array of entries.
        -   **WWM-DRG:**  PIC X(3), the DRG code (key).
        -   **WWM-RELWT:** PIC 9(1)V9(4), the relative weight.
        -   **WWM-ALOS:** PIC 9(2)V9(1), the average length of stay.

# Summary
-   `LTCAL032` and `LTCAL042` are COBOL subroutines for calculating LTC payments.  `LTCAL042` is a later version with some modifications.  Both programs perform edits, assemble variables, calculate payments (including short-stay and outlier calculations), and set a return code.
-   `LTDRG031` is a data definition (COPY) member providing the DRG table used by the calculation programs.
