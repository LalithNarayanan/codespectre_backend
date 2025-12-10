# Step 1: Program Analysis for LTCAL032

## LTCAL032
### Overview
This COBOL program, LTCAL032, is designed to calculate payments for Long-Term Care (LTC) claims based on the Prospective Payment System (PPS). It receives claim data, performs edits, calculates payment amounts, and returns the results. It uses a copybook `LTDRG031` for DRG-related data.

### Paragraph Execution Order and Description
-   `0000-MAINLINE-CONTROL`: The main control paragraph.
    -   Calls `0100-INITIAL-ROUTINE` to initialize variables.
    -   Calls `1000-EDIT-THE-BILL-INFO` to edit the bill information.
    -   If `PPS-RTC` is 00 (no errors), calls `1700-EDIT-DRG-CODE` to validate the DRG code.
    -   If `PPS-RTC` is 00, calls `2000-ASSEMBLE-PPS-VARIABLES` to assemble PPS variables.
    -   If `PPS-RTC` is 00, calls `3000-CALC-PAYMENT` to calculate the payment. Then calls `7000-CALC-OUTLIER` to calculate the outlier.
    -   If `PPS-RTC` is less than 50, calls `8000-BLEND` to apply blending rules.
    -   Calls `9000-MOVE-RESULTS` to move the results.
    -   `GOBACK`.

-   `0100-INITIAL-ROUTINE`: Initializes working storage variables.
    -   Sets `PPS-RTC` to zeros.
    -   Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS`.
    -   Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
    -   `EXIT`.

-   `1000-EDIT-THE-BILL-INFO`: Edits the bill data.
    -   If `B-LOS` is numeric and greater than 0, moves `B-LOS` to `H-LOS`. Otherwise, sets `PPS-RTC` to 56.
    -   If `PPS-RTC` is 00, and `P-NEW-WAIVER-STATE` is true, sets `PPS-RTC` to 53.
    -   If `PPS-RTC` is 00, and the discharge date is before the provider's or wage index's effective date, sets `PPS-RTC` to 55.
    -   If `PPS-RTC` is 00, and the provider's termination date is greater than 0, and the discharge date is greater or equal to the termination date, sets `PPS-RTC` to 51.
    -   If `PPS-RTC` is 00, and `B-COV-CHARGES` is not numeric, sets `PPS-RTC` to 58.
    -   If `PPS-RTC` is 00, and `B-LTR-DAYS` is not numeric or greater than 60, sets `PPS-RTC` to 61.
    -   If `PPS-RTC` is 00, and `B-COV-DAYS` is not numeric or 0 and `H-LOS` is greater than 0, sets `PPS-RTC` to 62.
    -   If `PPS-RTC` is 00, and `B-LTR-DAYS` is greater than `B-COV-DAYS`, sets `PPS-RTC` to 62.
    -   If `PPS-RTC` is 00, computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
    -   If `PPS-RTC` is 00, calls `1200-DAYS-USED`.
    -   `EXIT`.

-   `1200-DAYS-USED`: Calculates and moves the regular and lifetime reserve days used.
    -   If `B-LTR-DAYS` is greater than 0 and `H-REG-DAYS` is 0, adjusts `PPS-LTR-DAYS-USED` based on `H-LOS`
    -   If `H-REG-DAYS` is greater than 0 and `B-LTR-DAYS` is 0, adjusts `PPS-REG-DAYS-USED` based on `H-LOS`.
    -   If both `H-REG-DAYS` and `B-LTR-DAYS` are greater than 0, adjusts `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `H-LOS` and `H-TOTAL-DAYS`.
    -   `EXIT`.

-   `1700-EDIT-DRG-CODE`: Edits the DRG code.
    -   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    -   If `PPS-RTC` is 00, searches the `WWM-ENTRY` table for a matching DRG code.
        -   If not found, sets `PPS-RTC` to 54.
        -   If found, calls `1750-FIND-VALUE`.
    -   `EXIT`.

-   `1750-FIND-VALUE`: Retrieves DRG-related values from the table.
    -   Moves `WWM-RELWT` to `PPS-RELATIVE-WGT`.
    -   Moves `WWM-ALOS` to `PPS-AVG-LOS`.
    -   `EXIT`.

-   `2000-ASSEMBLE-PPS-VARIABLES`: Assembles PPS variables.
    -   If `W-WAGE-INDEX1` is numeric and greater than 0, moves it to `PPS-WAGE-INDEX`. Otherwise, sets `PPS-RTC` to 52 and goes to `2000-EXIT`.
    -   If `P-NEW-OPER-CSTCHG-RATIO` is not numeric, sets `PPS-RTC` to 65.
    -   Moves `P-NEW-FED-PPS-BLEND-IND` to `PPS-BLEND-YEAR`.
    -   If `PPS-BLEND-YEAR` is not between 1 and 5, sets `PPS-RTC` to 72 and goes to `2000-EXIT`.
    -   Initializes `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`.
    -   Sets blend factors based on `PPS-BLEND-YEAR`.
    -   `EXIT`.

-   `3000-CALC-PAYMENT`: Calculates the standard payment amount.
    -   Moves `P-NEW-COLA` to `PPS-COLA`.
    -   Computes `PPS-FAC-COSTS`.
    -   Computes `H-LABOR-PORTION`.
    -   Computes `H-NONLABOR-PORTION`.
    -   Computes `PPS-FED-PAY-AMT`.
    -   Computes `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `H-SSOT`.
    -   If `H-LOS` is less than or equal to `H-SSOT`, calls `3400-SHORT-STAY`.
    -   `EXIT`.

-   `3400-SHORT-STAY`: Calculates short-stay payments.
    -   Computes `H-SS-COST`.
    -   Computes `H-SS-PAY-AMT`.
    -   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` and moves the lowest value to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02 if a short stay payment is applicable.
    -   `EXIT`.

-   `7000-CALC-OUTLIER`: Calculates outlier payments.
    -   Computes `PPS-OUTLIER-THRESHOLD`.
    -   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, computes `PPS-OUTLIER-PAY-AMT`.
    -   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    -   If `PPS-OUTLIER-PAY-AMT` is greater than 0 and `PPS-RTC` is 02, sets `PPS-RTC` to 03.
    -   If `PPS-OUTLIER-PAY-AMT` is greater than 0 and `PPS-RTC` is 00, sets `PPS-RTC` to 01.
    -   If `PPS-RTC` is 00 or 02, and `PPS-REG-DAYS-USED` is greater than `H-SSOT`, sets `PPS-LTR-DAYS-USED` to 0.
    -   If `PPS-RTC` is 01 or 03, and `B-COV-DAYS` is less than `H-LOS` or `PPS-COT-IND` is 'Y', computes `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.
    -   `EXIT`.

-   `8000-BLEND`: Applies blend rules.
    -   Computes `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `PPS-NEW-FAC-SPEC-RATE`.
    -   Computes `PPS-FINAL-PAY-AMT`.
    -   Adds `H-BLEND-RTC` to `PPS-RTC`.
    -   `EXIT`.

-   `9000-MOVE-RESULTS`: Moves the final results to the output fields.
    -   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and 'V03.2' to `PPS-CALC-VERS-CD`.
    -   Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA`, and moves 'V03.2' to `PPS-CALC-VERS-CD`.
    -   `EXIT`.

### Business Rules
-   The program calculates payments based on the DRG, length of stay, and other claim-specific data.
-   It handles outlier payments and short-stay payments.
-   It applies blending rules based on the provider's blend year.
-   The program uses values from `LTDRG031` copybook for DRG-related information.
-   The program uses Federal Standard Rate, National Labor and Non-Labor percentages.
-   The program uses the Cost to Charge Ratio and the COLA (Cost of Living Adjustment)

### Data Validation and Error Handling Logic
-   **1000-EDIT-THE-BILL-INFO:**
    -   Validates `B-LOS`: Must be numeric and greater than 0.  Sets `PPS-RTC` to 56 if invalid.
    -   Checks `P-NEW-WAIVER-STATE`: If true, sets `PPS-RTC` to 53.
    -   Validates discharge date against effective dates: Sets `PPS-RTC` to 55 if invalid.
    -   Validates discharge date against termination date: Sets `PPS-RTC` to 51 if invalid.
    -   Validates `B-COV-CHARGES`: Must be numeric. Sets `PPS-RTC` to 58 if invalid.
    -   Validates `B-LTR-DAYS`: Must be numeric and <= 60. Sets `PPS-RTC` to 61 if invalid.
    -   Validates `B-COV-DAYS`: Must be numeric, or if zero, `H-LOS` should also be zero. Sets `PPS-RTC` to 62 if invalid.
    -   Validates `B-LTR-DAYS` against `B-COV-DAYS`: Sets `PPS-RTC` to 62 if `B-LTR-DAYS` > `B-COV-DAYS`.
-   **1700-EDIT-DRG-CODE:**
    -   Searches for the DRG code in the `WWM-ENTRY` table. Sets `PPS-RTC` to 54 if not found.
-   **2000-ASSEMBLE-PPS-VARIABLES:**
    -   Validates `W-WAGE-INDEX1`: Must be numeric and > 0. Sets `PPS-RTC` to 52 if invalid.
    -   Validates `P-NEW-OPER-CSTCHG-RATIO`: Must be numeric. Sets `PPS-RTC` to 65 if invalid.
    -   Validates `PPS-BLEND-YEAR`: Must be between 1 and 5. Sets `PPS-RTC` to 72 if invalid.

# Step 2: Program Analysis for LTCAL042

## LTCAL042
### Overview
This COBOL program, LTCAL042, is designed to calculate payments for Long-Term Care (LTC) claims based on the Prospective Payment System (PPS). It receives claim data, performs edits, calculates payment amounts, and returns the results. It uses a copybook `LTDRG031` for DRG-related data. This version seems to be an updated version of LTCAL032.

### Paragraph Execution Order and Description
-   `0000-MAINLINE-CONTROL`: The main control paragraph.
    -   Calls `0100-INITIAL-ROUTINE` to initialize variables.
    -   Calls `1000-EDIT-THE-BILL-INFO` to edit the bill information.
    -   If `PPS-RTC` is 00 (no errors), calls `1700-EDIT-DRG-CODE` to validate the DRG code.
    -   If `PPS-RTC` is 00, calls `2000-ASSEMBLE-PPS-VARIABLES` to assemble PPS variables.
    -   If `PPS-RTC` is 00, calls `3000-CALC-PAYMENT` to calculate the payment. Then calls `7000-CALC-OUTLIER` to calculate the outlier.
    -   If `PPS-RTC` is less than 50, calls `8000-BLEND` to apply blending rules.
    -   Calls `9000-MOVE-RESULTS` to move the results.
    -   `GOBACK`.

-   `0100-INITIAL-ROUTINE`: Initializes working storage variables.
    -   Sets `PPS-RTC` to zeros.
    -   Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS`.
    -   Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
    -   `EXIT`.

-   `1000-EDIT-THE-BILL-INFO`: Edits the bill data.
    -   If `B-LOS` is numeric and greater than 0, moves `B-LOS` to `H-LOS`. Otherwise, sets `PPS-RTC` to 56.
    -   If `PPS-RTC` is 00 and `P-NEW-COLA` is not numeric, sets `PPS-RTC` to 50.
    -   If `PPS-RTC` is 00, and `P-NEW-WAIVER-STATE` is true, sets `PPS-RTC` to 53.
    -   If `PPS-RTC` is 00, and the discharge date is before the provider's or wage index's effective date, sets `PPS-RTC` to 55.
    -   If `PPS-RTC` is 00, and the provider's termination date is greater than 0, and the discharge date is greater or equal to the termination date, sets `PPS-RTC` to 51.
    -   If `PPS-RTC` is 00, and `B-COV-CHARGES` is not numeric, sets `PPS-RTC` to 58.
    -   If `PPS-RTC` is 00, and `B-LTR-DAYS` is not numeric or greater than 60, sets `PPS-RTC` to 61.
    -   If `PPS-RTC` is 00, and `B-COV-DAYS` is not numeric or 0 and `H-LOS` is greater than 0, sets `PPS-RTC` to 62.
    -   If `PPS-RTC` is 00, and `B-LTR-DAYS` is greater than `B-COV-DAYS`, sets `PPS-RTC` to 62.
    -   If `PPS-RTC` is 00, computes `H-REG-DAYS` and `H-TOTAL-DAYS`.
    -   If `PPS-RTC` is 00, calls `1200-DAYS-USED`.
    -   `EXIT`.

-   `1200-DAYS-USED`: Calculates and moves the regular and lifetime reserve days used.
    -   If `B-LTR-DAYS` is greater than 0 and `H-REG-DAYS` is 0, adjusts `PPS-LTR-DAYS-USED` based on `H-LOS`
    -   If `H-REG-DAYS` is greater than 0 and `B-LTR-DAYS` is 0, adjusts `PPS-REG-DAYS-USED` based on `H-LOS`.
    -   If both `H-REG-DAYS` and `B-LTR-DAYS` are greater than 0, adjusts `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `H-LOS` and `H-TOTAL-DAYS`.
    -   `EXIT`.

-   `1700-EDIT-DRG-CODE`: Edits the DRG code.
    -   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    -   If `PPS-RTC` is 00, searches the `WWM-ENTRY` table for a matching DRG code.
        -   If not found, sets `PPS-RTC` to 54.
        -   If found, calls `1750-FIND-VALUE`.
    -   `EXIT`.

-   `1750-FIND-VALUE`: Retrieves DRG-related values from the table.
    -   Moves `WWM-RELWT` to `PPS-RELATIVE-WGT`.
    -   Moves `WWM-ALOS` to `PPS-AVG-LOS`.
    -   `EXIT`.

-   `2000-ASSEMBLE-PPS-VARIABLES`: Assembles PPS variables.
    -   Checks the provider's fiscal year beginning date.  If the discharge date is on or after 10/01/2003 and the provider's FY begins on or after 10/01/2003, it selects `W-WAGE-INDEX2`, otherwise, it selects `W-WAGE-INDEX1`.  If either wage index is not numeric or <= 0, sets `PPS-RTC` to 52 and exits.
    -   If `P-NEW-OPER-CSTCHG-RATIO` is not numeric, sets `PPS-RTC` to 65.
    -   Moves `P-NEW-FED-PPS-BLEND-IND` to `PPS-BLEND-YEAR`.
    -   If `PPS-BLEND-YEAR` is not between 1 and 5, sets `PPS-RTC` to 72 and goes to `2000-EXIT`.
    -   Initializes `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`.
    -   Sets blend factors based on `PPS-BLEND-YEAR`.
    -   `EXIT`.

-   `3000-CALC-PAYMENT`: Calculates the standard payment amount.
    -   Moves `P-NEW-COLA` to `PPS-COLA`.
    -   Computes `PPS-FAC-COSTS`.
    -   Computes `H-LABOR-PORTION`.
    -   Computes `H-NONLABOR-PORTION`.
    -   Computes `PPS-FED-PAY-AMT`.
    -   Computes `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `H-SSOT`.
    -   If `H-LOS` is less than or equal to `H-SSOT`, calls `3400-SHORT-STAY`.
    -   `EXIT`.

-   `3400-SHORT-STAY`: Calculates short-stay payments.
    -   If `P-NEW-PROVIDER-NO` is '332006', calls `4000-SPECIAL-PROVIDER`.
    -   Otherwise, computes `H-SS-COST` and `H-SS-PAY-AMT`.
    -   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` and moves the lowest value to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02 if a short stay payment is applicable.
    -   `EXIT`.

-   `4000-SPECIAL-PROVIDER`: Calculates short stay payments for special provider with ID '332006'
    -   If discharge date is between 07/01/2003 and 01/01/2004, computes `H-SS-COST` and `H-SS-PAY-AMT` using a factor of 1.95.
    -   Else if discharge date is between 01/01/2004 and 01/01/2005, computes `H-SS-COST` and `H-SS-PAY-AMT` using a factor of 1.93.
    -   `EXIT`.

-   `7000-CALC-OUTLIER`: Calculates outlier payments.
    -   Computes `PPS-OUTLIER-THRESHOLD`.
    -   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, computes `PPS-OUTLIER-PAY-AMT`.
    -   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    -   If `PPS-OUTLIER-PAY-AMT` is greater than 0 and `PPS-RTC` is 02, sets `PPS-RTC` to 03.
    -   If `PPS-OUTLIER-PAY-AMT` is greater than 0 and `PPS-RTC` is 00, sets `PPS-RTC` to 01.
    -   If `PPS-RTC` is 00 or 02, and `PPS-REG-DAYS-USED` is greater than `H-SSOT`, sets `PPS-LTR-DAYS-USED` to 0.
    -   If `PPS-RTC` is 01 or 03, and `B-COV-DAYS` is less than `H-LOS` or `PPS-COT-IND` is 'Y', computes `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.
    -   `EXIT`.

-   `8000-BLEND`: Applies blend rules.
    -   Computes `H-LOS-RATIO`.
    -   If `H-LOS-RATIO` is greater than 1, sets it to 1.
    -   Computes `PPS-DRG-ADJ-PAY-AMT`.
    -   Computes `PPS-NEW-FAC-SPEC-RATE`.
    -   Computes `PPS-FINAL-PAY-AMT`.
    -   Adds `H-BLEND-RTC` to `PPS-RTC`.
    -   `EXIT`.

-   `9000-MOVE-RESULTS`: Moves the final results to the output fields.
    -   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and 'V04.2' to `PPS-CALC-VERS-CD`.
    -   Otherwise, initializes `PPS-DATA` and `PPS-OTHER-DATA`, and moves 'V04.2' to `PPS-CALC-VERS-CD`.
    -   `EXIT`.

### Business Rules
-   The program calculates payments based on the DRG, length of stay, and other claim-specific data.
-   It handles outlier payments and short-stay payments.
-   It applies blending rules based on the provider's blend year.
-   The program uses values from `LTDRG031` copybook for DRG-related information.
-   The program uses Federal Standard Rate, National Labor and Non-Labor percentages.
-   The program uses the Cost to Charge Ratio and the COLA (Cost of Living Adjustment)
-   Special rules apply to provider '332006' for short stay calculation.
-   The program calculates the LOS ratio

### Data Validation and Error Handling Logic
-   **1000-EDIT-THE-BILL-INFO:**
    -   Validates `B-LOS`: Must be numeric and greater than 0. Sets `PPS-RTC` to 56 if invalid.
    -   Validates `P-NEW-COLA`: Must be numeric. Sets `PPS-RTC` to 50 if invalid.
    -   Checks `P-NEW-WAIVER-STATE`: If true, sets `PPS-RTC` to 53.
    -   Validates discharge date against effective dates: Sets `PPS-RTC` to 55 if invalid.
    -   Validates discharge date against termination date: Sets `PPS-RTC` to 51 if invalid.
    -   Validates `B-COV-CHARGES`: Must be numeric. Sets `PPS-RTC` to 58 if invalid.
    -   Validates `B-LTR-DAYS`: Must be numeric and <= 60. Sets `PPS-RTC` to 61 if invalid.
    -   Validates `B-COV-DAYS`: Must be numeric, or if zero, `H-LOS` should also be zero. Sets `PPS-RTC` to 62 if invalid.
    -   Validates `B-LTR-DAYS` against `B-COV-DAYS`: Sets `PPS-RTC` to 62 if `B-LTR-DAYS` > `B-COV-DAYS`.
-   **1700-EDIT-DRG-CODE:**
    -   Searches for the DRG code in the `WWM-ENTRY` table. Sets `PPS-RTC` to 54 if not found.
-   **2000-ASSEMBLE-PPS-VARIABLES:**
    -   Validates `W-WAGE-INDEX1` or `W-WAGE-INDEX2`: Must be numeric and > 0. Sets `PPS-RTC` to 52 if invalid.
    -   Validates `P-NEW-OPER-CSTCHG-RATIO`: Must be numeric. Sets `PPS-RTC` to 65 if invalid.
    -   Validates `PPS-BLEND-YEAR`: Must be between 1 and 5. Sets `PPS-RTC` to 72 if invalid.

## LTDRG031
### Overview
This copybook contains the DRG table data used by the LTCAL programs. It defines a table `WWM-ENTRY` that stores DRG codes, relative weights, and average lengths of stay.

### Data Structures
-   `W-DRG-FILLS`: Contains a series of PIC X(44) values.
-   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` to provide a structured format.
    -   `WWM-ENTRY`: An OCCURS 502 TIMES table.
        -   `WWM-DRG`: PIC X(3) - DRG Code.
        -   `WWM-RELWT`: PIC 9(1)V9(4) - Relative Weight.
        -   `WWM-ALOS`: PIC 9(2)V9(1) - Average Length of Stay.

### Business Rules
-   The copybook provides DRG-specific data (DRG code, relative weight, and average length of stay) for payment calculations.
-   The data is used to calculate the DRG Adjusted Payment Amount.

### Data Validation and Error Handling Logic
-   The data within the copybook is assumed to be valid as it represents the DRG table. The program using this copybook (LTCAL032 and LTCAL042) validates the DRG code against this table. If a DRG code is not found, the `PPS-RTC` is set to 54.
