## Analysis of LTCAL032

### Program Overview

*   **Program ID:** LTCAL032
*   **Purpose:** This COBOL program calculates the Long-Term Care (LTC) payment for a given bill, based on the provided input data and the applicable DRG (Diagnosis Related Group) information. It determines the payment amount, including potential outliers and short-stay adjustments, and returns the calculated results and a return code indicating the payment method.
*   **Version:** C03.2
*   **Effective Date:** January 1, 2003

### Paragraph Execution Order and Descriptions

1.  **0000-MAINLINE-CONTROL:**
    *   This is the main control paragraph. It orchestrates the execution flow of the program by calling other paragraphs in a specific sequence.
    *   Calls the following paragraphs:
        *   0100-INITIAL-ROUTINE
        *   1000-EDIT-THE-BILL-INFO
        *   1700-EDIT-DRG-CODE (conditionally)
        *   2000-ASSEMBLE-PPS-VARIABLES (conditionally)
        *   3000-CALC-PAYMENT (conditionally)
        *   7000-CALC-OUTLIER (conditionally)
        *   8000-BLEND (conditionally)
        *   9000-MOVE-RESULTS
        *   GOBACK
2.  **0100-INITIAL-ROUTINE:**
    *   Initializes working storage variables and sets default values.
    *   Moves zeros to `PPS-RTC` (Return Code).
    *   Initializes several working storage data structures: `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS`.
    *   Sets constants for national labor and non-labor portions, the standard federal rate, a fixed loss amount, and the budget neutrality rate.
3.  **1000-EDIT-THE-BILL-INFO:**
    *   Performs edits on the bill data passed to the program. If any edits fail, the `PPS-RTC` is set to an appropriate error code, and the program flow might be altered to avoid further processing.
    *   Edits performed:
        *   Checks if `B-LOS` (length of stay) is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
        *   Checks if the provider is in a waiver state (P-NEW-WAIVER-STATE). Sets `PPS-RTC` to 53 if true.
        *   Checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date or the wage index effective date. Sets `PPS-RTC` to 55 if true.
        *   Checks if the provider's termination date is valid and if the discharge date is after the termination date. Sets `PPS-RTC` to 51 if true.
        *   Checks if `B-COV-CHARGES` (covered charges) is numeric. Sets `PPS-RTC` to 58 if not.
        *   Checks if `B-LTR-DAYS` (lifetime reserve days) is numeric and if it is greater than 60. Sets `PPS-RTC` to 61 if not.
        *   Checks if `B-COV-DAYS` (covered days) is numeric and if either `B-COV-DAYS` is 0 and `H-LOS` (length of stay) is greater than 0. Sets `PPS-RTC` to 62 if not.
        *   Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. Sets `PPS-RTC` to 62 if true.
        *   Computes `H-REG-DAYS` (regular days) and `H-TOTAL-DAYS` (total days).
        *   Calls 1200-DAYS-USED.
4.  **1200-DAYS-USED:**
    *   Calculates the number of regular and lifetime reserve days used based on the length of stay and the number of covered days and lifetime reserve days.
    *   The logic here is designed to determine how many regular days and lifetime reserve days are used for the payment calculation, considering the total length of stay, covered days, and lifetime reserve days.
5.  **1700-EDIT-DRG-CODE:**
    *   Moves the DRG code from the input bill data (`B-DRG-CODE`) to `PPS-SUBM-DRG-CODE`.
    *   Searches the DRG table (`WWM-ENTRY`) for a matching DRG code.
    *   If a match is found, calls `1750-FIND-VALUE`.
    *   If no match is found, sets `PPS-RTC` to 54.
6.  **1750-FIND-VALUE:**
    *   Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the DRG table to the `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` fields, respectively.
7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   This paragraph retrieves and assembles the necessary PPS (Prospective Payment System) variables.
    *   Checks if `W-WAGE-INDEX1` (wage index) is numeric and greater than 0, moving its value to `PPS-WAGE-INDEX` if it is. Otherwise, sets `PPS-RTC` to 52.
    *   Checks if `P-NEW-OPER-CSTCHG-RATIO` (operating cost-to-charge ratio) is numeric. Sets `PPS-RTC` to 65 if not.
    *   Moves `P-NEW-FED-PPS-BLEND-IND` (federal PPS blend indicator) to `PPS-BLEND-YEAR`.
    *   Validates `PPS-BLEND-YEAR` to ensure it's within the valid range (1-5). Sets `PPS-RTC` to 72 if invalid.
    *   Calculates blend factors (`H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`) based on the `PPS-BLEND-YEAR`.
8.  **3000-CALC-PAYMENT:**
    *   Calculates the standard payment amount.
    *   Moves `P-NEW-COLA` (cost of living adjustment) to `PPS-COLA`.
    *   Calculates `PPS-FAC-COSTS` (facility costs) by multiplying `P-NEW-OPER-CSTCHG-RATIO` by `B-COV-CHARGES`.
    *   Calculates `H-LABOR-PORTION` (labor portion), `H-NONLABOR-PORTION` (non-labor portion), and `PPS-FED-PAY-AMT` (federal payment amount) using the national labor/non-labor percentages, wage index, standard federal rate, and COLA.
    *   Calculates `PPS-DRG-ADJ-PAY-AMT` (DRG adjusted payment amount) using the relative weight and the federal payment amount.
    *   Calculates `H-SSOT` (short stay outlier threshold).
    *   If the length of stay (`H-LOS`) is less than or equal to `H-SSOT`, calls `3400-SHORT-STAY`.
9.  **3400-SHORT-STAY:**
    *   Calculates short-stay costs and payment amounts.
    *   Calculates `H-SS-COST` (short stay cost) and `H-SS-PAY-AMT` (short stay payment amount).
    *   Determines the `PPS-RTC` based on the comparison of `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT`.
        *   If `H-SS-COST` is the lowest, it moves `H-SS-COST` to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02.
        *   If `H-SS-PAY-AMT` is the lowest, it moves `H-SS-PAY-AMT` to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02.
10. **7000-CALC-OUTLIER:**
    *   Calculates outlier payments if applicable.
    *   Calculates `PPS-OUTLIER-THRESHOLD`.
    *   If `PPS-FAC-COSTS` exceeds the threshold, calculates `PPS-OUTLIER-PAY-AMT`.
    *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to zero.
    *   Sets `PPS-RTC` to indicate outlier payment (01 or 03) based on the conditions.
    *   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED` and `H-SSOT`.
    *   If `PPS-RTC` is 01 or 03 and certain conditions are met, sets `PPS-RTC` to 67.
11. **8000-BLEND:**
    *   This paragraph calculates the "final" payment amount, considering blend factors.
    *   Calculates `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    *   Adds `H-BLEND-RTC` to `PPS-RTC`.
12. **9000-MOVE-RESULTS:**
    *   Moves the calculated results to the output fields.
    *   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V03.2'.
    *   If `PPS-RTC` is 50 or greater, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V03.2'.

### Business Rules

*   **Payment Calculation:** The program calculates the LTC payment based on the DRG code, length of stay, covered charges, and other provider-specific and claim-specific information.
*   **DRG Lookup:** The program looks up the DRG code in the `LTDRG031` copybook to retrieve the relative weight and average length of stay.
*   **Short Stay:** If the length of stay is less than or equal to 5/6 of the average length of stay, the program calculates a short-stay payment.
*   **Outlier Payments:** The program calculates outlier payments if the facility costs exceed a calculated threshold.
*   **Blend Payments:** The program applies blend factors based on the `PPS-BLEND-YEAR` to determine the final payment amount.
*   **Data Validation:** The program validates various input fields to ensure data integrity.
*   **Return Codes:** The program uses a return code (`PPS-RTC`) to indicate how the bill was paid or the reason why it could not be paid.
*   **Provider Specific Rate:** Facility specific rate will be calculated based on the facility specific rate.

### Data Validation and Error Handling Logic

*   **B-LOS Validation (Paragraph 1000):**
    *   `B-LOS NUMERIC`: Checks if the length of stay is a numeric value.
    *   `B-LOS > 0`: Checks if the length of stay is greater than zero.
    *   Error Handling: If either check fails, `PPS-RTC` is set to 56 (Invalid Length of Stay).
*   **Waiver State Check (Paragraph 1000):**
    *   `P-NEW-WAIVER-STATE`: Checks if the provider is in a waiver state (value 'Y').
    *   Error Handling: If true, `PPS-RTC` is set to 53 (Waiver State - Not calculated by PPS).
*   **Discharge Date Edits (Paragraph 1000):**
    *   `B-DISCHARGE-DATE < P-NEW-EFF-DATE OR B-DISCHARGE-DATE < W-EFF-DATE`: Checks if the discharge date is before the provider's effective date or the wage index effective date.
    *   Error Handling: If true, `PPS-RTC` is set to 55 (Discharge date before effective date).
*   **Termination Date Edits (Paragraph 1000):**
    *   `P-NEW-TERMINATION-DATE > 00000000`: Checks if the termination date is not zero.
    *   `B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is after the termination date.
    *   Error Handling: If true, `PPS-RTC` is set to 51 (Provider record terminated).
*   **Covered Charges Validation (Paragraph 1000):**
    *   `B-COV-CHARGES NOT NUMERIC`: Checks if covered charges are numeric.
    *   Error Handling: If not numeric, `PPS-RTC` is set to 58 (Total covered charges not numeric).
*   **Lifetime Reserve Days Validation (Paragraph 1000):**
    *   `B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if lifetime reserve days are numeric and less than or equal to 60.
    *   Error Handling: If not numeric or greater than 60, `PPS-RTC` is set to 61 (Lifetime reserve days invalid).
*   **Covered Days Validation (Paragraph 1000):**
    *   `(B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if covered days are numeric and if covered days are 0 when length of stay is greater than 0.
    *   Error Handling: If invalid, `PPS-RTC` is set to 62 (Invalid number of covered days).
*   **Covered Days vs Lifetime Reserve Days Validation (Paragraph 1000):**
    *   `B-LTR-DAYS > B-COV-DAYS`: Checks if lifetime reserve days are greater than covered days.
    *   Error Handling: If true, `PPS-RTC` is set to 62 (Invalid number of covered days).
*   **DRG Code Lookup (Paragraph 1700):**
    *   `SEARCH ALL WWM-ENTRY AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, `PPS-RTC` is set to 54 (DRG on claim not found in table).
*   **Wage Index Validation (Paragraph 2000):**
    *   `W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0`: Checks if the wage index is numeric and greater than 0.
    *   Error Handling: If not valid, `PPS-RTC` is set to 52 (Invalid wage index).
*   **Operating Cost-to-Charge Ratio Validation (Paragraph 2000):**
    *   `P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC`: Checks if the operating cost-to-charge ratio is numeric.
    *   Error Handling: If not numeric, `PPS-RTC` is set to 65 (Operating cost-to-charge ratio not numeric).
*   **Blend Year Validation (Paragraph 2000):**
    *   `PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6`: Checks if the blend year is within the valid range (1-5).
    *   Error Handling: If invalid, `PPS-RTC` is set to 72 (Invalid blend indicator).

## Analysis of LTCAL042

### Program Overview

*   **Program ID:** LTCAL042
*   **Purpose:** This COBOL program calculates the Long-Term Care (LTC) payment for a given bill, based on the provided input data and the applicable DRG (Diagnosis Related Group) information. It determines the payment amount, including potential outliers and short-stay adjustments, and returns the calculated results and a return code indicating the payment method.
*   **Version:** C04.2
*   **Effective Date:** July 1, 2003

### Paragraph Execution Order and Descriptions

1.  **0000-MAINLINE-CONTROL:**
    *   This is the main control paragraph. It orchestrates the execution flow of the program by calling other paragraphs in a specific sequence.
    *   Calls the following paragraphs:
        *   0100-INITIAL-ROUTINE
        *   1000-EDIT-THE-BILL-INFO
        *   1700-EDIT-DRG-CODE (conditionally)
        *   2000-ASSEMBLE-PPS-VARIABLES (conditionally)
        *   3000-CALC-PAYMENT (conditionally)
        *   7000-CALC-OUTLIER (conditionally)
        *   8000-BLEND (conditionally)
        *   9000-MOVE-RESULTS
        *   GOBACK
2.  **0100-INITIAL-ROUTINE:**
    *   Initializes working storage variables and sets default values.
    *   Moves zeros to `PPS-RTC` (Return Code).
    *   Initializes several working storage data structures: `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS`.
    *   Sets constants for national labor and non-labor portions, the standard federal rate, a fixed loss amount, and the budget neutrality rate.
3.  **1000-EDIT-THE-BILL-INFO:**
    *   Performs edits on the bill data passed to the program. If any edits fail, the `PPS-RTC` is set to an appropriate error code, and the program flow might be altered to avoid further processing.
    *   Edits performed:
        *   Checks if `B-LOS` (length of stay) is numeric and greater than 0. Sets `PPS-RTC` to 56 if not.
        *   Checks if `P-NEW-COLA` (Cost of Living Adjustment) is numeric. Sets `PPS-RTC` to 50 if not.
        *   Checks if the provider is in a waiver state (P-NEW-WAIVER-STATE). Sets `PPS-RTC` to 53 if true.
        *   Checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date or the wage index effective date. Sets `PPS-RTC` to 55 if true.
        *   Checks if the provider's termination date is valid and if the discharge date is after the termination date. Sets `PPS-RTC` to 51 if true.
        *   Checks if `B-COV-CHARGES` (covered charges) is numeric. Sets `PPS-RTC` to 58 if not.
        *   Checks if `B-LTR-DAYS` (lifetime reserve days) is numeric and if it is greater than 60. Sets `PPS-RTC` to 61 if not.
        *   Checks if `B-COV-DAYS` (covered days) is numeric and if either `B-COV-DAYS` is 0 and `H-LOS` (length of stay) is greater than 0. Sets `PPS-RTC` to 62 if not.
        *   Checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`. Sets `PPS-RTC` to 62 if true.
        *   Computes `H-REG-DAYS` (regular days) and `H-TOTAL-DAYS` (total days).
        *   Calls 1200-DAYS-USED.
4.  **1200-DAYS-USED:**
    *   Calculates the number of regular and lifetime reserve days used based on the length of stay and the number of covered days and lifetime reserve days.
    *   The logic here is designed to determine how many regular days and lifetime reserve days are used for the payment calculation, considering the total length of stay, covered days, and lifetime reserve days.
5.  **1700-EDIT-DRG-CODE:**
    *   Moves the DRG code from the input bill data (`B-DRG-CODE`) to `PPS-SUBM-DRG-CODE`.
    *   Searches the DRG table (`WWM-ENTRY`) for a matching DRG code.
    *   If a match is found, calls `1750-FIND-VALUE`.
    *   If no match is found, sets `PPS-RTC` to 54.
6.  **1750-FIND-VALUE:**
    *   Moves the relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the DRG table to the `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` fields, respectively.
7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   This paragraph retrieves and assembles the necessary PPS (Prospective Payment System) variables.
    *   Conditional logic to select wage index based on discharge date and provider fiscal year begin date.
        *   If `P-NEW-FY-BEGIN-DATE >= 20031001 AND B-DISCHARGE-DATE >= P-NEW-FY-BEGIN-DATE` then use `W-WAGE-INDEX2`, else use `W-WAGE-INDEX1`.
    *   Checks if the selected wage index is numeric and greater than 0, moving its value to `PPS-WAGE-INDEX` if it is. Otherwise, sets `PPS-RTC` to 52.
    *   Checks if `P-NEW-OPER-CSTCHG-RATIO` (operating cost-to-charge ratio) is numeric. Sets `PPS-RTC` to 65 if not.
    *   Moves `P-NEW-FED-PPS-BLEND-IND` (federal PPS blend indicator) to `PPS-BLEND-YEAR`.
    *   Validates `PPS-BLEND-YEAR` to ensure it's within the valid range (1-5). Sets `PPS-RTC` to 72 if invalid.
    *   Calculates blend factors (`H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`) based on the `PPS-BLEND-YEAR`.
8.  **3000-CALC-PAYMENT:**
    *   Calculates the standard payment amount.
    *   Moves `P-NEW-COLA` (cost of living adjustment) to `PPS-COLA`.
    *   Calculates `PPS-FAC-COSTS` (facility costs) by multiplying `P-NEW-OPER-CSTCHG-RATIO` by `B-COV-CHARGES`.
    *   Calculates `H-LABOR-PORTION` (labor portion), `H-NONLABOR-PORTION` (non-labor portion), and `PPS-FED-PAY-AMT` (federal payment amount) using the national labor/non-labor percentages, wage index, standard federal rate, and COLA.
    *   Calculates `PPS-DRG-ADJ-PAY-AMT` (DRG adjusted payment amount) using the relative weight and the federal payment amount.
    *   Calculates `H-SSOT` (short stay outlier threshold).
    *   If the length of stay (`H-LOS`) is less than or equal to `H-SSOT`, calls `3400-SHORT-STAY`.
9.  **3400-SHORT-STAY:**
    *   Calculates short-stay costs and payment amounts.
    *   If `P-NEW-PROVIDER-NO` is '332006', calls `4000-SPECIAL-PROVIDER`.
    *   Else, calculates short-stay cost and payment amounts.
    *   Determines the `PPS-RTC` based on the comparison of `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT`.
        *   If `H-SS-COST` is the lowest, it moves `H-SS-COST` to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02.
        *   If `H-SS-PAY-AMT` is the lowest, it moves `H-SS-PAY-AMT` to `PPS-DRG-ADJ-PAY-AMT` and sets `PPS-RTC` to 02.
10. **4000-SPECIAL-PROVIDER:**
    *   Special calculation for short stay for provider number '332006'.
    *   If discharge date is between 20030701 and 20040101, applies a factor of 1.95.
    *   If discharge date is between 20040101 and 20050101, applies a factor of 1.93.
11. **7000-CALC-OUTLIER:**
    *   Calculates outlier payments if applicable.
    *   Calculates `PPS-OUTLIER-THRESHOLD`.
    *   If `PPS-FAC-COSTS` exceeds the threshold, calculates `PPS-OUTLIER-PAY-AMT`.
    *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to zero.
    *   Sets `PPS-RTC` to indicate outlier payment (01 or 03) based on the conditions.
    *   Adjusts `PPS-LTR-DAYS-USED` based on `PPS-REG-DAYS-USED` and `H-SSOT`.
    *   If `PPS-RTC` is 01 or 03 and certain conditions are met, sets `PPS-RTC` to 67.
12. **8000-BLEND:**
    *   This paragraph calculates the "final" payment amount, considering blend factors.
    *   Calculates `H-LOS-RATIO`.
    *   If `H-LOS-RATIO` is greater than 1, sets it to 1.
    *   Calculates `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    *   Adds `H-BLEND-RTC` to `PPS-RTC`.
13. **9000-MOVE-RESULTS:**
    *   Moves the calculated results to the output fields.
    *   If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V04.2'.
    *   If `PPS-RTC` is 50 or greater, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V04.2'.

### Business Rules

*   **Payment Calculation:** The program calculates the LTC payment based on the DRG code, length of stay, covered charges, and other provider-specific and claim-specific information.
*   **DRG Lookup:** The program looks up the DRG code in the `LTDRG031` copybook to retrieve the relative weight and average length of stay.
*   **Short Stay:** If the length of stay is less than or equal to 5/6 of the average length of stay, the program calculates a short-stay payment.
*   **Outlier Payments:** The program calculates outlier payments if the facility costs exceed a calculated threshold.
*   **Blend Payments:** The program applies blend factors based on the `PPS-BLEND-YEAR` to determine the final payment amount.
*   **Data Validation:** The program validates various input fields to ensure data integrity.
*   **Return Codes:** The program uses a return code (`PPS-RTC`) to indicate how the bill was paid or the reason why it could not be paid.
*   **Provider Specific Rate:** Facility specific rate will be calculated based on the facility specific rate.
*   **Special Provider Logic:** Special short stay calculations are applied for the provider with number '332006'.
*   **Length of Stay Ratio:** A length of stay ratio is calculated and used in the facility specific rate calculation.

### Data Validation and Error Handling Logic

*   **B-LOS Validation (Paragraph 1000):**
    *   `B-LOS NUMERIC`: Checks if the length of stay is a numeric value.
    *   `B-LOS > 0`: Checks if the length of stay is greater than zero.
    *   Error Handling: If either check fails, `PPS-RTC` is set to 56 (Invalid Length of Stay).
*   **COLA Validation (Paragraph 1000):**
    *   `P-NEW-COLA NOT NUMERIC`: Checks if Cost of Living Adjustment is numeric.
    *   Error Handling: If not numeric, `PPS-RTC` is set to 50.
*   **Waiver State Check (Paragraph 1000):**
    *   `P-NEW-WAIVER-STATE`: Checks if the provider is in a waiver state (value 'Y').
    *   Error Handling: If true, `PPS-RTC` is set to 53 (Waiver State - Not calculated by PPS).
*   **Discharge Date Edits (Paragraph 1000):**
    *   `B-DISCHARGE-DATE < P-NEW-EFF-DATE OR B-DISCHARGE-DATE < W-EFF-DATE`: Checks if the discharge date is before the provider's effective date or the wage index effective date.
    *   Error Handling: If true, `PPS-RTC` is set to 55 (Discharge date before effective date).
*   **Termination Date Edits (Paragraph 1000):**
    *   `P-NEW-TERMINATION-DATE > 00000000`: Checks if the termination date is not zero.
    *   `B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is after the termination date.
    *   Error Handling: If true, `PPS-RTC` is set to 51 (Provider record terminated).
*   **Covered Charges Validation (Paragraph 1000):**
    *   `B-COV-CHARGES NOT NUMERIC`: Checks if covered charges are numeric.
    *   Error Handling: If not numeric, `PPS-RTC` is set to 58 (Total covered charges not numeric).
*   **Lifetime Reserve Days Validation (Paragraph 1000):**
    *   `B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if lifetime reserve days are numeric and less than or equal to 60.
    *   Error Handling: If not numeric or greater than 60, `PPS-RTC` is set to 61 (Lifetime reserve days invalid).
*   **Covered Days Validation (Paragraph 1000):**
    *   `(B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if covered days are numeric and if covered days are 0 when length of stay is greater than 0.
    *   Error Handling: If invalid, `PPS-RTC` is set to 62 (Invalid number of covered days).
*   **Covered Days vs Lifetime Reserve Days Validation (Paragraph 1000):**
    *   `B-LTR-DAYS > B-COV-DAYS`: Checks if lifetime reserve days are greater than covered days.
    *   Error Handling: If true, `PPS-RTC` is set to 62 (Invalid number of covered days).
*   **DRG Code Lookup (Paragraph 1700):**
    *   `SEARCH ALL WWM-ENTRY AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, `PPS-RTC` is set to 54 (DRG on claim not found in table).
*   **Wage Index Validation (Paragraph 2000):**
    *   `W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0`: Checks if the wage index is numeric and greater than 0.
    *   Error Handling: If not valid, `PPS-RTC` is set to 52 (Invalid wage index).
*   **Operating Cost-to-Charge Ratio Validation (Paragraph 2000):**
    *   `P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC`: Checks if the operating cost-to-charge ratio is numeric.
    *   Error Handling: If not numeric, `PPS-RTC` is set to 65 (Operating cost-to-charge ratio not numeric).
*   **Blend Year Validation (Paragraph 2000):**
    *   `PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6`: Checks if the blend year is within the valid range (1-5).
    *   Error Handling: If invalid, `PPS-RTC` is set to 72 (Invalid blend indicator).
