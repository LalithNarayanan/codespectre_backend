## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, `LTCAL032`, `LTCAL042`, and `LTDRG031`, formatted using Markdown.

### Program: LTCAL032

#### Program Overview

`LTCAL032` is a COBOL program designed to calculate Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) and other patient and provider-specific data. It's a subroutine called by another program to determine the appropriate payment amount.  It uses a copybook `LTDRG031` which contains the DRG table.

#### Paragraph Execution Order and Description

Here's a breakdown of the paragraphs executed in `LTCAL032`, along with descriptions:

1.  **`0000-MAINLINE-CONTROL`**:
    *   This is the main control paragraph. It orchestrates the flow of the program by calling other paragraphs.
    *   Calls the following paragraphs sequentially:
        *   `0100-INITIAL-ROUTINE`
        *   `1000-EDIT-THE-BILL-INFO`
        *   `1700-EDIT-DRG-CODE` (conditionally)
        *   `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
        *   `3000-CALC-PAYMENT` (conditionally)
        *   `7000-CALC-OUTLIER` (conditionally)
        *   `8000-BLEND` (conditionally)
        *   `9000-MOVE-RESULTS`
        *   `GOBACK` - Returns control to the calling program.

2.  **`0100-INITIAL-ROUTINE`**:
    *   Initializes working storage variables, specifically:
        *   `PPS-RTC` to zeros (Return Code).
        *   `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    *   Sets constants for:
        *   `PPS-NAT-LABOR-PCT` (National Labor Percentage).
        *   `PPS-NAT-NONLABOR-PCT` (National Non-Labor Percentage).
        *   `PPS-STD-FED-RATE` (Standard Federal Rate).
        *   `H-FIXED-LOSS-AMT` (Fixed Loss Amount).
        *   `PPS-BDGT-NEUT-RATE` (Budget Neutrality Rate).

3.  **`1000-EDIT-THE-BILL-INFO`**:
    *   Performs data validation on the input `BILL-NEW-DATA` record.  If any edits fail, it sets the `PPS-RTC` (return code) to an error code.
    *   **Edits performed:**
        *   Validates `B-LOS` (Length of Stay) - must be numeric and greater than 0. Sets `PPS-RTC` to 56 if invalid.
        *   Checks `P-NEW-WAIVER-STATE` (Waiver State) - If 'Y', sets `PPS-RTC` to 53.
        *   Compares `B-DISCHARGE-DATE` (Discharge Date) with `P-NEW-EFF-DATE` (Provider Effective Date) and `W-EFF-DATE` (Wage Index Effective Date). Sets `PPS-RTC` to 55 if the discharge date is earlier.
        *   Checks `P-NEW-TERMINATION-DATE` (Termination Date) against `B-DISCHARGE-DATE`. Sets `PPS-RTC` to 51 if the discharge date is on or after the termination date.
        *   Validates `B-COV-CHARGES` (Covered Charges) - must be numeric. Sets `PPS-RTC` to 58 if not numeric.
        *   Validates `B-LTR-DAYS` (Lifetime Reserve Days) - must be numeric and <= 60. Sets `PPS-RTC` to 61 if invalid.
        *   Validates `B-COV-DAYS` (Covered Days) - must be numeric. Also checks if `B-COV-DAYS` is 0 and `H-LOS` > 0. Sets `PPS-RTC` to 62 if invalid.
        *   Validates `B-LTR-DAYS` (Lifetime Reserve Days) against `B-COV-DAYS`. Sets `PPS-RTC` to 62 if LTR days exceed covered days.
        *   Calculates `H-REG-DAYS` (Regular Days) and `H-TOTAL-DAYS` (Total Days).
        *   Calls `1200-DAYS-USED`

4.  **`1200-DAYS-USED`**:
    *   Calculates `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`. This logic determines how many regular and lifetime reserve days are used for payment calculation, considering the length of stay.

5.  **`1700-EDIT-DRG-CODE`**:
    *   Moves the `B-DRG-CODE` (DRG Code from the input) to `PPS-SUBM-DRG-CODE`.
    *   **Searches the DRG table (defined in `LTDRG031`)** for a matching DRG code.
        *   If the DRG code is not found, sets `PPS-RTC` to 54.
        *   If found, calls `1750-FIND-VALUE`.

6.  **`1750-FIND-VALUE`**:
    *   Moves the `WWM-RELWT` (Relative Weight) and `WWM-ALOS` (Average Length of Stay) from the DRG table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.

7.  **`2000-ASSEMBLE-PPS-VARIABLES`**:
    *   Retrieves and validates provider and wage index information.
    *   **Logic:**
        *   Checks if the `W-WAGE-INDEX1` is numeric and greater than 0, if true moves the value to `PPS-WAGE-INDEX`, else sets `PPS-RTC` to 52.
        *   Checks if `P-NEW-OPER-CSTCHG-RATIO` is numeric; if not, sets `PPS-RTC` to 65.
        *   Sets `PPS-BLEND-YEAR` from `P-NEW-FED-PPS-BLEND-IND`.
        *   Validates `PPS-BLEND-YEAR` to be between 1 and 5 (inclusive). If not, sets `PPS-RTC` to 72.
        *   Calculates blend factors (`H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`) based on the `PPS-BLEND-YEAR`.

8.  **`3000-CALC-PAYMENT`**:
    *   Calculates the standard payment amount.
    *   **Calculations performed:**
        *   Moves `P-NEW-COLA` to `PPS-COLA`.
        *   Calculates `PPS-FAC-COSTS` (Facility Costs).
        *   Calculates `H-LABOR-PORTION` (Labor Portion).
        *   Calculates `H-NONLABOR-PORTION` (Non-Labor Portion).
        *   Calculates `PPS-FED-PAY-AMT` (Federal Payment Amount).
        *   Calculates `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount).
        *   Calculates `H-SSOT` (Short Stay Outlier Threshold).
        *   Calls `3400-SHORT-STAY` if `H-LOS` (Length of Stay) is less than or equal to `H-SSOT`

9.  **`3400-SHORT-STAY`**:
    *   Calculates short-stay payment amounts.
    *   **Calculations performed:**
        *   Calculates `H-SS-COST` (Short Stay Cost).
        *   Calculates `H-SS-PAY-AMT` (Short Stay Payment Amount).
        *   Compares `H-SS-COST`, `H-SS-PAY-AMT` and `PPS-DRG-ADJ-PAY-AMT` and moves the lowest value to `PPS-DRG-ADJ-PAY-AMT`.
        *   Sets `PPS-RTC` to 02 to indicate a short stay payment.

10. **`7000-CALC-OUTLIER`**:
    *   Calculates outlier payments.
    *   **Calculations performed:**
        *   Calculates `PPS-OUTLIER-THRESHOLD`.
        *   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, calculates `PPS-OUTLIER-PAY-AMT`.
        *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
        *   Sets the `PPS-RTC` based on the values of `PPS-OUTLIER-PAY-AMT` and the current value of `PPS-RTC`, to indicate an outlier payment.
        *   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED`, `H-SSOT`, and the current value of `PPS-RTC`.
        *   If `PPS-RTC` is 01 or 03 and certain conditions are met, sets `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.

11. **`8000-BLEND`**:
    *   Calculates the final payment amount, considering blend factors.
    *   **Calculations performed:**
        *   Adjusts `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount) by applying the budget neutrality rate and blend percentage.
        *   Calculates `PPS-NEW-FAC-SPEC-RATE` (New Facility Specific Rate) by applying the budget neutrality rate and facility blend percentage.
        *   Calculates `PPS-FINAL-PAY-AMT` (Final Payment Amount).
        *   Adds `H-BLEND-RTC` to `PPS-RTC`.

12. **`9000-MOVE-RESULTS`**:
    *   Moves the calculated results to the output variables.
    *   If `PPS-RTC` is less than 50, moves the `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V03.2'.
    *   If `PPS-RTC` is 50 or greater, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V03.2'.
    *   This paragraph prepares the results to be returned to the calling program.

#### Business Rules

*   **DRG Payment Calculation:** The program calculates payments based on the DRG, length of stay, and other factors.
*   **Short Stay:** If the length of stay is less than or equal to 5/6 of the average length of stay, a short-stay payment is calculated.
*   **Outlier Payments:** Outlier payments are calculated if the facility costs exceed a calculated threshold.
*   **Blending:** The program supports blended payment methodologies based on the provider's blend year.
*   **Data Validation:**  The program validates various input data elements and sets an error code if validation fails.
*   **Waiver State:**  If the provider is in a waiver state, the program sets an error code.
*   **Termination Date:**  The program considers provider termination dates when calculating payments.

#### Data Validation and Error Handling

*   **`PPS-RTC` (Return Code):**  This field is central to error handling. The program sets `PPS-RTC` to different values to indicate the reason for payment adjustments or denials.
*   **Input Data Validation (in `1000-EDIT-THE-BILL-INFO`):**
    *   Numeric checks for `B-LOS`, `B-COV-CHARGES`, `B-LTR-DAYS`, and `B-COV-DAYS`.
    *   Range checks for `B-LTR-DAYS` (<= 60).
    *   Date comparisons (discharge date vs. effective dates and termination date).
*   **DRG Code Validation (in `1700-EDIT-DRG-CODE`):**  Checks if the DRG code exists in the DRG table.
*   **Provider Data Validation (in `2000-ASSEMBLE-PPS-VARIABLES`):**
    *   Numeric check for `W-WAGE-INDEX1` and `P-NEW-OPER-CSTCHG-RATIO`.
    *   Validation of `PPS-BLEND-YEAR`.
*   **Error Codes:**
    *   50: Provider specific rate not numeric
    *   51: Provider record terminated
    *   52: Invalid wage index
    *   53: Waiver state
    *   54: DRG not found
    *   55: Discharge date before effective date
    *   56: Invalid length of stay
    *   58: Covered charges not numeric
    *   61: LTR days invalid
    *   62: Invalid covered days
    *   65: Operating cost to charge ratio not numeric
    *   67: Cost outlier with invalid LOS
    *   72: Invalid blend indicator

### Program: LTCAL042

#### Program Overview

`LTCAL042` is very similar to `LTCAL032`.  It is also a COBOL program designed to calculate Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) and other patient and provider-specific data. It's a subroutine called by another program to determine the appropriate payment amount.  It uses a copybook `LTDRG031` which contains the DRG table.
The key difference between `LTCAL032` and `LTCAL042` is that `LTCAL042` uses different values for some constants and has additional logic for a special provider.

#### Paragraph Execution Order and Description

The paragraph execution order is almost identical to `LTCAL032`.

1.  **`0000-MAINLINE-CONTROL`**:
    *   This is the main control paragraph. It orchestrates the flow of the program by calling other paragraphs.
    *   Calls the following paragraphs sequentially:
        *   `0100-INITIAL-ROUTINE`
        *   `1000-EDIT-THE-BILL-INFO`
        *   `1700-EDIT-DRG-CODE` (conditionally)
        *   `2000-ASSEMBLE-PPS-VARIABLES` (conditionally)
        *   `3000-CALC-PAYMENT` (conditionally)
        *   `7000-CALC-OUTLIER` (conditionally)
        *   `8000-BLEND` (conditionally)
        *   `9000-MOVE-RESULTS`
        *   `GOBACK` - Returns control to the calling program.

2.  **`0100-INITIAL-ROUTINE`**:
    *   Initializes working storage variables, specifically:
        *   `PPS-RTC` to zeros (Return Code).
        *   `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    *   Sets constants for:
        *   `PPS-NAT-LABOR-PCT` (National Labor Percentage).
        *   `PPS-NAT-NONLABOR-PCT` (National Non-Labor Percentage).
        *   `PPS-STD-FED-RATE` (Standard Federal Rate).
        *   `H-FIXED-LOSS-AMT` (Fixed Loss Amount).
        *   `PPS-BDGT-NEUT-RATE` (Budget Neutrality Rate).

3.  **`1000-EDIT-THE-BILL-INFO`**:
    *   Performs data validation on the input `BILL-NEW-DATA` record.  If any edits fail, it sets the `PPS-RTC` (return code) to an error code.
    *   **Edits performed:**
        *   Validates `B-LOS` (Length of Stay) - must be numeric and greater than 0. Sets `PPS-RTC` to 56 if invalid.
        *   Checks `P-NEW-COLA` (Cost of Living Adjustment) is numeric. Sets `PPS-RTC` to 50 if invalid.
        *   Checks `P-NEW-WAIVER-STATE` (Waiver State) - If 'Y', sets `PPS-RTC` to 53.
        *   Compares `B-DISCHARGE-DATE` (Discharge Date) with `P-NEW-EFF-DATE` (Provider Effective Date) and `W-EFF-DATE` (Wage Index Effective Date). Sets `PPS-RTC` to 55 if the discharge date is earlier.
        *   Checks `P-NEW-TERMINATION-DATE` (Termination Date) against `B-DISCHARGE-DATE`. Sets `PPS-RTC` to 51 if the discharge date is on or after the termination date.
        *   Validates `B-COV-CHARGES` (Covered Charges) - must be numeric. Sets `PPS-RTC` to 58 if not numeric.
        *   Validates `B-LTR-DAYS` (Lifetime Reserve Days) - must be numeric and <= 60. Sets `PPS-RTC` to 61 if invalid.
        *   Validates `B-COV-DAYS` (Covered Days) - must be numeric. Also checks if `B-COV-DAYS` is 0 and `H-LOS` > 0. Sets `PPS-RTC` to 62 if invalid.
        *   Validates `B-LTR-DAYS` (Lifetime Reserve Days) against `B-COV-DAYS`. Sets `PPS-RTC` to 62 if LTR days exceed covered days.
        *   Calculates `H-REG-DAYS` (Regular Days) and `H-TOTAL-DAYS` (Total Days).
        *   Calls `1200-DAYS-USED`

4.  **`1200-DAYS-USED`**:
    *   Calculates `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`. This logic determines how many regular and lifetime reserve days are used for payment calculation, considering the length of stay.

5.  **`1700-EDIT-DRG-CODE`**:
    *   Moves the `B-DRG-CODE` (DRG Code from the input) to `PPS-SUBM-DRG-CODE`.
    *   **Searches the DRG table (defined in `LTDRG031`)** for a matching DRG code.
        *   If the DRG code is not found, sets `PPS-RTC` to 54.
        *   If found, calls `1750-FIND-VALUE`.

6.  **`1750-FIND-VALUE`**:
    *   Moves the `WWM-RELWT` (Relative Weight) and `WWM-ALOS` (Average Length of Stay) from the DRG table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.

7.  **`2000-ASSEMBLE-PPS-VARIABLES`**:
    *   Retrieves and validates provider and wage index information.
    *   **Logic:**
        *   If `P-NEW-FY-BEGIN-DATE` (Provider Fiscal Year Begin Date) is >= 20031001 AND `B-DISCHARGE-DATE` (Bill Discharge Date) is >= `P-NEW-FY-BEGIN-DATE`, then uses `W-WAGE-INDEX2`, otherwise uses `W-WAGE-INDEX1`. If WAGE-INDEX is not numeric sets `PPS-RTC` to 52.
        *   Checks if `P-NEW-OPER-CSTCHG-RATIO` is numeric; if not, sets `PPS-RTC` to 65.
        *   Sets `PPS-BLEND-YEAR` from `P-NEW-FED-PPS-BLEND-IND`.
        *   Validates `PPS-BLEND-YEAR` to be between 1 and 5 (inclusive). If not, sets `PPS-RTC` to 72.
        *   Calculates blend factors (`H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`) based on the `PPS-BLEND-YEAR`.

8.  **`3000-CALC-PAYMENT`**:
    *   Calculates the standard payment amount.
    *   **Calculations performed:**
        *   Moves `P-NEW-COLA` to `PPS-COLA`.
        *   Calculates `PPS-FAC-COSTS` (Facility Costs).
        *   Calculates `H-LABOR-PORTION` (Labor Portion).
        *   Calculates `H-NONLABOR-PORTION` (Non-Labor Portion).
        *   Calculates `PPS-FED-PAY-AMT` (Federal Payment Amount).
        *   Calculates `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount).
        *   Calculates `H-SSOT` (Short Stay Outlier Threshold).
        *   Calls `3400-SHORT-STAY` if `H-LOS` (Length of Stay) is less than or equal to `H-SSOT`

9.  **`3400-SHORT-STAY`**:
    *   Calculates short-stay payment amounts.
    *   **Logic:**
        *   If `P-NEW-PROVIDER-NO` is equal to '332006', calls `4000-SPECIAL-PROVIDER`.
        *   Else, calculates `H-SS-COST` and `H-SS-PAY-AMT`, and compares the values against `PPS-DRG-ADJ-PAY-AMT` and moves the lowest value to `PPS-DRG-ADJ-PAY-AMT`.
        *   Sets `PPS-RTC` to 02 to indicate a short stay payment.

10. **`4000-SPECIAL-PROVIDER`**:
    *   Special Logic for provider '332006'.
    *   **Logic:**
        *   If `B-DISCHARGE-DATE` is between 20030701 and 20040101, calculates `H-SS-COST` and `H-SS-PAY-AMT` using a factor of 1.95.
        *   Else If `B-DISCHARGE-DATE` is between 20040101 and 20050101, calculates `H-SS-COST` and `H-SS-PAY-AMT` using a factor of 1.93.

11. **`7000-CALC-OUTLIER`**:
    *   Calculates outlier payments.
    *   **Calculations performed:**
        *   Calculates `PPS-OUTLIER-THRESHOLD`.
        *   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, calculates `PPS-OUTLIER-PAY-AMT`.
        *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
        *   Sets the `PPS-RTC` based on the values of `PPS-OUTLIER-PAY-AMT` and the current value of `PPS-RTC`, to indicate an outlier payment.
        *   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED`, `H-SSOT`, and the current value of `PPS-RTC`.
        *   If `PPS-RTC` is 01 or 03 and certain conditions are met, sets `PPS-CHRG-THRESHOLD` and sets `PPS-RTC` to 67.

12. **`8000-BLEND`**:
    *   Calculates the final payment amount, considering blend factors.
    *   **Calculations performed:**
        *   Calculates `H-LOS-RATIO`.
        *   Adjusts `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount) by applying the budget neutrality rate and blend percentage.
        *   Calculates `PPS-NEW-FAC-SPEC-RATE` (New Facility Specific Rate) by applying the budget neutrality rate, facility blend percentage and `H-LOS-RATIO`.
        *   Calculates `PPS-FINAL-PAY-AMT` (Final Payment Amount).
        *   Adds `H-BLEND-RTC` to `PPS-RTC`.

13. **`9000-MOVE-RESULTS`**:
    *   Moves the calculated results to the output variables.
    *   If `PPS-RTC` is less than 50, moves the `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V04.2'.
    *   If `PPS-RTC` is 50 or greater, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V04.2'.
    *   This paragraph prepares the results to be returned to the calling program.

#### Business Rules

*   **DRG Payment Calculation:** The program calculates payments based on the DRG, length of stay, and other factors.
*   **Short Stay:** If the length of stay is less than or equal to 5/6 of the average length of stay, a short-stay payment is calculated.
*   **Outlier Payments:** Outlier payments are calculated if the facility costs exceed a calculated threshold.
*   **Blending:** The program supports blended payment methodologies based on the provider's blend year.
*   **Data Validation:**  The program validates various input data elements and sets an error code if validation fails.
*   **Waiver State:**  If the provider is in a waiver state, the program sets an error code.
*   **Termination Date:**  The program considers provider termination dates when calculating payments.
*   **Provider Specific Logic:** Special logic exists for provider '332006' that changes short stay calculations based on the discharge date.
*   **Wage Index:** The program uses different wage indexes based on the discharge date and provider fiscal year.

#### Data Validation and Error Handling

*   **`PPS-RTC` (Return Code):**  This field is central to error handling. The program sets `PPS-RTC` to different values to indicate the reason for payment adjustments or denials.
*   **Input Data Validation (in `1000-EDIT-THE-BILL-INFO`):**
    *   Numeric checks for `B-LOS`, `P-NEW-COLA`, `B-COV-CHARGES`, `B-LTR-DAYS`, and `B-COV-DAYS`.
    *   Range checks for `B-LTR-DAYS` (<= 60).
    *   Date comparisons (discharge date vs. effective dates and termination date).
*   **DRG Code Validation (in `1700-EDIT-DRG-CODE`):**  Checks if the DRG code exists in the DRG table.
*   **Provider Data Validation (in `2000-ASSEMBLE-PPS-VARIABLES`):**
    *   Numeric check for `W-WAGE-INDEX1` and `P-NEW-OPER-CSTCHG-RATIO`.
    *   Validation of `PPS-BLEND-YEAR`.
*   **Error Codes:**
    *   50: Provider specific rate or COLA not numeric
    *   51: Provider record terminated
    *   52: Invalid wage index
    *   53: Waiver state
    *   54: DRG not found
    *   55: Discharge date before effective date
    *   56: Invalid length of stay
    *   58: Covered charges not numeric
    *   61: LTR days invalid
    *   62: Invalid covered days
    *   65: Operating cost to charge ratio not numeric
    *   67: Cost outlier with invalid LOS
    *   72: Invalid blend indicator

### Program: LTDRG031

#### Program Overview

`LTDRG031` is a COBOL copybook (included in `LTCAL032` and `LTCAL042`) that defines the DRG table.  This table contains DRG codes and associated payment information (Relative Weight and Average Length of Stay). This data is used by the LTCAL programs to determine the payment for a specific DRG.

#### Data Structure

The copybook defines a structure called `W-DRG-TABLE`, which contains:

*   `WWM-ENTRY` (Occurs 502 times):  An array of entries, each representing a DRG.
    *   `WWM-DRG`:  The 3-character DRG code. This is the key field used for searching.
    *   `WWM-RELWT`:  The relative weight for the DRG (used in payment calculation).
    *   `WWM-ALOS`:  The average length of stay for the DRG.

#### Business Rules

*   **DRG Table Lookup:**  The program uses the DRG code from the input data to look up the corresponding relative weight and average length of stay in this table.
*   **Data Source:** This copybook acts as a data source for DRG-specific payment information.

#### Data Validation and Error Handling

*   **Data Integrity:** The data within the table is critical to the accuracy of the payment calculations.  There is no error handling within the copybook itself. Errors would be caught in the calling programs if a DRG code is not found.
*   **Table Size:** The table has a fixed size (502 entries).
*   **Key Field:** `WWM-DRG` is the key field, and it's used to search the table.  The table is assumed to be sorted in ascending order by `WWM-DRG`.
