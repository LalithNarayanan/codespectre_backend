## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, `LTCAL032`, `LTCAL042`, and `LTDRG031`, formatted as requested.

### Program: LTCAL032

#### Paragraph Execution Order and Description

The program's execution flow is as follows:

1.  **0000-MAINLINE-CONTROL:**  This is the main control paragraph.  It orchestrates the overall processing.
    *   Calls `0100-INITIAL-ROUTINE` to initialize variables.
    *   Calls `1000-EDIT-THE-BILL-INFO` to perform initial data edits.
    *   If `PPS-RTC` is still 00 (meaning no errors), calls `1700-EDIT-DRG-CODE` to validate DRG code.
    *   If `PPS-RTC` is still 00, calls `2000-ASSEMBLE-PPS-VARIABLES` to assemble PPS variables.
    *   If `PPS-RTC` is still 00, calls `3000-CALC-PAYMENT` to calculate the payment.
    *   Calls `7000-CALC-OUTLIER` to calculate outliers.
    *   If `PPS-RTC` is less than 50 (indicating no major error), calls `8000-BLEND` to apply blending logic.
    *   Calls `9000-MOVE-RESULTS` to move the results to the output area.
    *   Calls `GOBACK` to terminate the program.

2.  **0100-INITIAL-ROUTINE:**
    *   Initializes `PPS-RTC` to zero (00).
    *   Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    *   Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
    *   Calls `EXIT` to terminate the paragraph

3.  **1000-EDIT-THE-BILL-INFO:** This paragraph performs various edits on the input bill data.
    *   Checks if `B-LOS` (Length of Stay) is numeric and greater than 0; if not, sets `PPS-RTC` to 56.
    *   If `PPS-RTC` is 00, checks if `P-NEW-WAIVER-STATE` is true (waiver state). If true, sets `PPS-RTC` to 53.
    *   If `PPS-RTC` is 00, checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date (`P-NEW-EFF-DATE`) or the wage index effective date (`W-EFF-DATE`). If so, sets `PPS-RTC` to 55.
    *   If `PPS-RTC` is 00, checks if a termination date (`P-NEW-TERMINATION-DATE`) is present and if the discharge date is on or after the termination date. If so, sets `PPS-RTC` to 51.
    *   If `PPS-RTC` is 00, checks if `B-COV-CHARGES` (Covered Charges) is numeric; if not, sets `PPS-RTC` to 58.
    *   If `PPS-RTC` is 00, checks if `B-LTR-DAYS` (Lifetime Reserve Days) is not numeric or if it's greater than 60; if so, sets `PPS-RTC` to 61.
    *   If `PPS-RTC` is 00, checks if `B-COV-DAYS` (Covered Days) is not numeric or if it is zero and `H-LOS` (Length of Stay) is greater than 0; if so, sets `PPS-RTC` to 62.
    *   If `PPS-RTC` is 00, checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`; if so, sets `PPS-RTC` to 62.
    *   If `PPS-RTC` is 00, computes `H-REG-DAYS` (Regular Days) and `H-TOTAL-DAYS`.
    *   If `PPS-RTC` is 00, calls `1200-DAYS-USED` to calculate days used for LTR and Regular Days.
    *   Calls `EXIT` to terminate the paragraph

4.  **1200-DAYS-USED:** This paragraph calculates the number of regular and lifetime reserve days used.
    *   The Logic is:
        *   If LTR days are greater than 0 and regular days are 0, it determines the days used based on the length of stay.
        *   If regular days are greater than 0 and LTR days are 0, it determines the days used based on the length of stay.
        *   If both regular and LTR days are greater than 0, it determines the days used based on the length of stay.
    *   Calls `EXIT` to terminate the paragraph

5.  **1700-EDIT-DRG-CODE:** This paragraph edits the DRG code.
    *   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    *   If `PPS-RTC` is 00, searches the `WWM-ENTRY` table (defined in `LTDRG031`) for a matching DRG code. If not found, sets `PPS-RTC` to 54.
    *   If a match is found, calls `1750-FIND-VALUE`.
    *   Calls `EXIT` to terminate the paragraph

6.  **1750-FIND-VALUE:** This paragraph finds the value in the DRG code table.
    *   Moves `WWM-RELWT` (relative weight) and `WWM-ALOS` (average length of stay) from the `WWM-ENTRY` table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS`, respectively.
    *   Calls `EXIT` to terminate the paragraph

7.  **2000-ASSEMBLE-PPS-VARIABLES:** This paragraph assembles the PPS variables.
    *   If `W-WAGE-INDEX1` (wage index) is numeric and greater than 0, moves it to `PPS-WAGE-INDEX`; otherwise, sets `PPS-RTC` to 52.
    *   If `P-NEW-OPER-CSTCHG-RATIO` (Operating Cost to Charge Ratio) is not numeric, sets `PPS-RTC` to 65.
    *   Moves `P-NEW-FED-PPS-BLEND-IND` to `PPS-BLEND-YEAR`.
    *   Checks if `PPS-BLEND-YEAR` is between 1 and 5. If not, sets `PPS-RTC` to 72.
    *   Initializes blend-related variables: `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`.
    *   Sets blend factors based on `PPS-BLEND-YEAR`.
        *   Year 1: 80% facility, 20% DRG
        *   Year 2: 60% facility, 40% DRG
        *   Year 3: 40% facility, 60% DRG
        *   Year 4: 20% facility, 80% DRG
    *   Calls `EXIT` to terminate the paragraph

8.  **3000-CALC-PAYMENT:**  This paragraph calculates the standard payment amount and determines if it is a short-stay.
    *   Moves `P-NEW-COLA` (Cost of Living Adjustment) to `PPS-COLA`.
    *   Computes `PPS-FAC-COSTS` (Facility Costs).
    *   Computes `H-LABOR-PORTION` (Labor Portion),  `H-NONLABOR-PORTION` (Non-Labor Portion), and `PPS-FED-PAY-AMT` (Federal Payment Amount).
    *   Computes `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount).
    *   Computes `H-SSOT` (Short Stay Outlier Threshold).
    *   If `H-LOS` (Length of Stay) is less than or equal to `H-SSOT`, it calls `3400-SHORT-STAY`.
    *   Calls `EXIT` to terminate the paragraph

9.  **3400-SHORT-STAY:** This paragraph calculates the short-stay payment.
    *   Computes `H-SS-COST` (Short Stay Cost) and `H-SS-PAY-AMT` (Short Stay Payment Amount).
    *   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` to determine the final payment amount and sets `PPS-RTC` to 02 if a short stay applies.
    *   Calls `EXIT` to terminate the paragraph

10. **7000-CALC-OUTLIER:** This paragraph calculates the outlier payment.
    *   Computes `PPS-OUTLIER-THRESHOLD`.
    *   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, it computes `PPS-OUTLIER-PAY-AMT`.
    *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    *   Sets `PPS-RTC` to 03 if there is an outlier payment and the current `PPS-RTC` is 02.
    *   Sets `PPS-RTC` to 01 if there is an outlier payment and the current `PPS-RTC` is 00.
    *   If `PPS-RTC` is 00 or 02, and `PPS-REG-DAYS-USED` is greater than `H-SSOT`, it sets `PPS-LTR-DAYS-USED` to 0.
    *   If `PPS-RTC` is 01 or 03 and certain conditions are met, it sets `PPS-RTC` to 67.
    *   Calls `EXIT` to terminate the paragraph

11. **8000-BLEND:** This paragraph calculates the final payment amount after blending.
    *   Computes `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    *   Adds `H-BLEND-RTC` to `PPS-RTC`.
    *   Calls `EXIT` to terminate the paragraph

12. **9000-MOVE-RESULTS:** This paragraph moves the results.
    *   If `PPS-RTC` is less than 50, it moves `H-LOS` to `PPS-LOS` and `V03.2` to `PPS-CALC-VERS-CD`.
    *   Otherwise, it initializes `PPS-DATA`, `PPS-OTHER-DATA` and move `V03.2` to `PPS-CALC-VERS-CD`.
    *   Calls `EXIT` to terminate the paragraph

#### Business Rules

*   **DRG Payment Calculation:** The core function of the program is to calculate the payment amount for a healthcare claim based on the DRG (Diagnosis Related Group) assigned to the patient's stay.
*   **Length of Stay (LOS) Edits:** Edits are performed on the Length of Stay to ensure it is numeric and greater than zero.
*   **Waiver State:** If the provider is in a waiver state, the claim is not calculated by PPS.
*   **Discharge Date Validation:** The discharge date must be after the provider's effective date and the wage index effective date.
*   **Termination Date Validation:** If a provider has a termination date, the discharge date must be before the termination date.
*   **Covered Charges Validation:** The covered charges must be numeric.
*   **Lifetime Reserve Days Validation:** The lifetime reserve days must be numeric and less than or equal to 60.
*   **Covered Days Validation:** Covered Days must be numeric, and there are checks to ensure the LTR days are not greater than the covered days.
*   **DRG Code Validation:** The DRG code must exist in the DRG table.
*   **Wage Index:** The program uses the wage index to calculate the labor portion of the payment.
*   **Blending:** The program applies blending rules based on the provider's blend year.
*   **Outlier Calculation:** If the facility costs exceed a threshold, an outlier payment is calculated.
*   **Short Stay Payment:** If the length of stay is less than a certain threshold, a short stay payment is calculated.

#### Data Validation and Error Handling Logic

*   **Input Data Validation:**
    *   **Numeric Checks:** The program extensively validates numeric fields (e.g., `B-LOS`, `B-COV-CHARGES`, `B-LTR-DAYS`, `B-COV-DAYS`, `W-WAGE-INDEX1`, `P-NEW-OPER-CSTCHG-RATIO`, `P-NEW-COLA`).
    *   **Range Checks:** Checks are performed to ensure values are within acceptable ranges (e.g., `B-LTR-DAYS` <= 60).
    *   **Date Comparisons:** The program compares dates (discharge date vs. effective dates, termination dates) to ensure data consistency.
*   **DRG Code Validation:** The program verifies that the DRG code exists in a lookup table (`WWM-ENTRY`).
*   **Error Handling:**
    *   **PPS-RTC:** The `PPS-RTC` field is the primary mechanism for error reporting.  Different values of `PPS-RTC` indicate different error conditions.
    *   **GO TO:** The `GO TO` statements are used to exit the processing early if an error is detected. This prevents further calculations if the input data is invalid.

### Program: LTCAL042

#### Paragraph Execution Order and Description

The program's execution flow is as follows:

1.  **0000-MAINLINE-CONTROL:**  This is the main control paragraph.  It orchestrates the overall processing.
    *   Calls `0100-INITIAL-ROUTINE` to initialize variables.
    *   Calls `1000-EDIT-THE-BILL-INFO` to perform initial data edits.
    *   If `PPS-RTC` is still 00 (meaning no errors), calls `1700-EDIT-DRG-CODE` to validate DRG code.
    *   If `PPS-RTC` is still 00, calls `2000-ASSEMBLE-PPS-VARIABLES` to assemble PPS variables.
    *   If `PPS-RTC` is still 00, calls `3000-CALC-PAYMENT` to calculate the payment.
    *   Calls `7000-CALC-OUTLIER` to calculate outliers.
    *   If `PPS-RTC` is less than 50 (indicating no major error), calls `8000-BLEND` to apply blending logic.
    *   Calls `9000-MOVE-RESULTS` to move the results to the output area.
    *   Calls `GOBACK` to terminate the program.

2.  **0100-INITIAL-ROUTINE:**
    *   Initializes `PPS-RTC` to zero (00).
    *   Initializes `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS` to their initial values.
    *   Moves constant values to `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
    *   Calls `EXIT` to terminate the paragraph

3.  **1000-EDIT-THE-BILL-INFO:** This paragraph performs various edits on the input bill data.
    *   Checks if `B-LOS` (Length of Stay) is numeric and greater than 0; if not, sets `PPS-RTC` to 56.
    *   If `PPS-RTC` is 00, checks if `P-NEW-COLA` is numeric, if not, sets `PPS-RTC` to 50.
    *   If `PPS-RTC` is 00, checks if `P-NEW-WAIVER-STATE` is true (waiver state). If true, sets `PPS-RTC` to 53.
    *   If `PPS-RTC` is 00, checks if the discharge date (`B-DISCHARGE-DATE`) is before the provider's effective date (`P-NEW-EFF-DATE`) or the wage index effective date (`W-EFF-DATE`). If so, sets `PPS-RTC` to 55.
    *   If `PPS-RTC` is 00, checks if a termination date (`P-NEW-TERMINATION-DATE`) is present and if the discharge date is on or after the termination date. If so, sets `PPS-RTC` to 51.
    *   If `PPS-RTC` is 00, checks if `B-COV-CHARGES` (Covered Charges) is numeric; if not, sets `PPS-RTC` to 58.
    *   If `PPS-RTC` is 00, checks if `B-LTR-DAYS` (Lifetime Reserve Days) is not numeric or if it's greater than 60; if so, sets `PPS-RTC` to 61.
    *   If `PPS-RTC` is 00, checks if `B-COV-DAYS` (Covered Days) is not numeric or if it is zero and `H-LOS` (Length of Stay) is greater than 0; if so, sets `PPS-RTC` to 62.
    *   If `PPS-RTC` is 00, checks if `B-LTR-DAYS` is greater than `B-COV-DAYS`; if so, sets `PPS-RTC` to 62.
    *   If `PPS-RTC` is 00, computes `H-REG-DAYS` (Regular Days) and `H-TOTAL-DAYS`.
    *   If `PPS-RTC` is 00, calls `1200-DAYS-USED` to calculate days used for LTR and Regular Days.
    *   Calls `EXIT` to terminate the paragraph

4.  **1200-DAYS-USED:** This paragraph calculates the number of regular and lifetime reserve days used.
    *   The Logic is:
        *   If LTR days are greater than 0 and regular days are 0, it determines the days used based on the length of stay.
        *   If regular days are greater than 0 and LTR days are 0, it determines the days used based on the length of stay.
        *   If both regular and LTR days are greater than 0, it determines the days used based on the length of stay.
    *   Calls `EXIT` to terminate the paragraph

5.  **1700-EDIT-DRG-CODE:** This paragraph edits the DRG code.
    *   Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
    *   If `PPS-RTC` is 00, searches the `WWM-ENTRY` table (defined in `LTDRG031`) for a matching DRG code. If not found, sets `PPS-RTC` to 54.
    *   If a match is found, calls `1750-FIND-VALUE`.
    *   Calls `EXIT` to terminate the paragraph

6.  **1750-FIND-VALUE:** This paragraph finds the value in the DRG code table.
    *   Moves `WWM-RELWT` (relative weight) and `WWM-ALOS` (average length of stay) from the `WWM-ENTRY` table to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS`, respectively.
    *   Calls `EXIT` to terminate the paragraph

7.  **2000-ASSEMBLE-PPS-VARIABLES:** This paragraph assembles the PPS variables.
    *   If the FY Begin Date is greater than or equal to 20031001 and the discharge date is greater than or equal to the FY Begin Date, the wage index 2 is used, if not, wage index 1 is used. If wage index is not numeric or 0, sets `PPS-RTC` to 52.
    *   If `P-NEW-OPER-CSTCHG-RATIO` (Operating Cost to Charge Ratio) is not numeric, sets `PPS-RTC` to 65.
    *   Moves `P-NEW-FED-PPS-BLEND-IND` to `PPS-BLEND-YEAR`.
    *   Checks if `PPS-BLEND-YEAR` is between 1 and 5. If not, sets `PPS-RTC` to 72.
    *   Initializes blend-related variables: `H-BLEND-FAC`, `H-BLEND-PPS`, and `H-BLEND-RTC`.
    *   Sets blend factors based on `PPS-BLEND-YEAR`.
        *   Year 1: 80% facility, 20% DRG
        *   Year 2: 60% facility, 40% DRG
        *   Year 3: 40% facility, 60% DRG
        *   Year 4: 20% facility, 80% DRG
    *   Calls `EXIT` to terminate the paragraph

8.  **3000-CALC-PAYMENT:**  This paragraph calculates the standard payment amount and determines if it is a short-stay.
    *   Moves `P-NEW-COLA` (Cost of Living Adjustment) to `PPS-COLA`.
    *   Computes `PPS-FAC-COSTS` (Facility Costs).
    *   Computes `H-LABOR-PORTION` (Labor Portion),  `H-NONLABOR-PORTION` (Non-Labor Portion), and `PPS-FED-PAY-AMT` (Federal Payment Amount).
    *   Computes `PPS-DRG-ADJ-PAY-AMT` (DRG Adjusted Payment Amount).
    *   Computes `H-SSOT` (Short Stay Outlier Threshold).
    *   If `H-LOS` (Length of Stay) is less than or equal to `H-SSOT`, it calls `3400-SHORT-STAY`.
    *   Calls `EXIT` to terminate the paragraph

9.  **3400-SHORT-STAY:** This paragraph calculates the short-stay payment.
    *   If the provider number is 332006, calls the `4000-SPECIAL-PROVIDER` paragraph.
    *   Computes `H-SS-COST` (Short Stay Cost) and `H-SS-PAY-AMT` (Short Stay Payment Amount).
    *   Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` to determine the final payment amount and sets `PPS-RTC` to 02 if a short stay applies.
    *   Calls `EXIT` to terminate the paragraph

10. **4000-SPECIAL-PROVIDER:** This paragraph calculates the short-stay payment for the provider number 332006.
    *   If the discharge date is between 20030701 and 20040101, it computes the short stay cost and payment amount with a multiplier of 1.95.
    *   If the discharge date is between 20040101 and 20050101, it computes the short stay cost and payment amount with a multiplier of 1.93.
    *   Calls `EXIT` to terminate the paragraph

11. **7000-CALC-OUTLIER:** This paragraph calculates the outlier payment.
    *   Computes `PPS-OUTLIER-THRESHOLD`.
    *   If `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`, it computes `PPS-OUTLIER-PAY-AMT`.
    *   If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
    *   Sets `PPS-RTC` to 03 if there is an outlier payment and the current `PPS-RTC` is 02.
    *   Sets `PPS-RTC` to 01 if there is an outlier payment and the current `PPS-RTC` is 00.
    *   If `PPS-RTC` is 00 or 02, and `PPS-REG-DAYS-USED` is greater than `H-SSOT`, it sets `PPS-LTR-DAYS-USED` to 0.
    *   If `PPS-RTC` is 01 or 03 and certain conditions are met, it sets `PPS-RTC` to 67.
    *   Calls `EXIT` to terminate the paragraph

12. **8000-BLEND:** This paragraph calculates the final payment amount after blending.
    *   Computes `H-LOS-RATIO` (LOS Ratio).
    *   Limits `H-LOS-RATIO` to a maximum of 1.
    *   Computes `PPS-DRG-ADJ-PAY-AMT`, `PPS-NEW-FAC-SPEC-RATE`, and `PPS-FINAL-PAY-AMT`.
    *   Adds `H-BLEND-RTC` to `PPS-RTC`.
    *   Calls `EXIT` to terminate the paragraph

13. **9000-MOVE-RESULTS:** This paragraph moves the results.
    *   If `PPS-RTC` is less than 50, it moves `H-LOS` to `PPS-LOS` and `V04.2` to `PPS-CALC-VERS-CD`.
    *   Otherwise, it initializes `PPS-DATA`, `PPS-OTHER-DATA` and move `V04.2` to `PPS-CALC-VERS-CD`.
    *   Calls `EXIT` to terminate the paragraph

#### Business Rules

*   **DRG Payment Calculation:** The core function of the program is to calculate the payment amount for a healthcare claim based on the DRG (Diagnosis Related Group) assigned to the patient's stay.
*   **Length of Stay (LOS) Edits:** Edits are performed on the Length of Stay to ensure it is numeric and greater than zero.
*   **Waiver State:** If the provider is in a waiver state, the claim is not calculated by PPS.
*   **Discharge Date Validation:** The discharge date must be after the provider's effective date and the wage index effective date.
*   **Termination Date Validation:** If a provider has a termination date, the discharge date must be before the termination date.
*   **Covered Charges Validation:** The covered charges must be numeric.
*   **Lifetime Reserve Days Validation:** The lifetime reserve days must be numeric and less than or equal to 60.
*   **Covered Days Validation:** Covered Days must be numeric, and there are checks to ensure the LTR days are not greater than the covered days.
*   **DRG Code Validation:** The DRG code must exist in the DRG table.
*   **Wage Index:** The program uses the wage index to calculate the labor portion of the payment.
*   **Blending:** The program applies blending rules based on the provider's blend year.
*   **Outlier Calculation:** If the facility costs exceed a threshold, an outlier payment is calculated.
*   **Short Stay Payment:** If the length of stay is less than a certain threshold, a short stay payment is calculated.
*   **Special Provider Payment:** Applies a different short stay calculation for provider number 332006.

#### Data Validation and Error Handling Logic

*   **Input Data Validation:**
    *   **Numeric Checks:** The program extensively validates numeric fields (e.g., `B-LOS`, `B-COV-CHARGES`, `B-LTR-DAYS`, `B-COV-DAYS`, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `P-NEW-OPER-CSTCHG-RATIO`, `P-NEW-COLA`).
    *   **Range Checks:** Checks are performed to ensure values are within acceptable ranges (e.g., `B-LTR-DAYS` <= 60).
    *   **Date Comparisons:** The program compares dates (discharge date vs. effective dates, termination dates) to ensure data consistency.
*   **DRG Code Validation:** The program verifies that the DRG code exists in a lookup table (`WWM-ENTRY`).
*   **Error Handling:**
    *   **PPS-RTC:** The `PPS-RTC` field is the primary mechanism for error reporting.  Different values of `PPS-RTC` indicate different error conditions.
    *   **GO TO:** The `GO TO` statements are used to exit the processing early if an error is detected. This prevents further calculations if the input data is invalid.

### Program: LTDRG031

#### Paragraph Execution Order and Description

This program is a COPY member; it does not have a `PROCEDURE DIVISION` and therefore has no executable paragraphs.  It defines the DRG table structure.

#### Business Rules

*   **DRG Table Structure:**  Defines the structure of the DRG table, which contains DRG codes, relative weights, and average lengths of stay.
*   **Data Storage:**  The `WWM-ENTRY` occurs 502 times, indicating storage for 502 DRG records.
*   **Keying:** The `ASCENDING KEY IS WWM-DRG` clause indicates that the table is sorted by the DRG code.

#### Data Validation and Error Handling Logic

*   **Data Integrity:** The data within this table is crucial for the calculations performed in the calling programs (`LTCAL032` and `LTCAL042`).  The accuracy and consistency of the DRG codes, relative weights, and average lengths of stay are critical for correct payment calculations.
*   **Search and Retrieval:** The calling programs use `SEARCH ALL` to find the correct DRG record within this table, based on the `WWM-DRG` field. If the DRG code is not found, an error is triggered.
