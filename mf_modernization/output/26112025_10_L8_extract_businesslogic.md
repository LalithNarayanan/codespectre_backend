## Analysis of COBOL Program LTCAL032

### Program Overview

*   **Program ID:** LTCAL032
*   **Purpose:** This COBOL program calculates Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) for the fiscal year 2003, effective January 1, 2003. It receives bill data as input, performs edits, looks up DRG information, calculates payments (including short stay and outlier adjustments), and returns the results.
*   **Key Features:**
    *   Data validation and error handling.
    *   DRG code lookup in a table (LTDRG031, included via COPY).
    *   Calculation of standard payments.
    *   Short-stay payment calculations.
    *   Outlier payment calculations.
    *   Blend year calculations for facilities in transition.
    *   Returns a return code (PPS-RTC) indicating the payment method.

### Paragraph Execution Order and Descriptions

1.  **0000-MAINLINE-CONTROL:**
    *   **Description:** This is the main control paragraph. It orchestrates the program's execution flow by calling other paragraphs in a defined sequence.
    *   **Execution Order:**
        *   `PERFORM 0100-INITIAL-ROUTINE`: Initializes working storage variables.
        *   `PERFORM 1000-EDIT-THE-BILL-INFO`: Performs data validation and edits on the input bill data.
        *   `IF PPS-RTC = 00`:  Checks if any edit errors occurred. If no errors, continues to next steps.
            *   `PERFORM 1700-EDIT-DRG-CODE`: Looks up the DRG code in the DRG table.
        *   `IF PPS-RTC = 00`: Checks if DRG lookup was successful.
            *   `PERFORM 2000-ASSEMBLE-PPS-VARIABLES`: Assembles the necessary PPS variables.
        *   `IF PPS-RTC = 00`: Checks if PPS variables were assembled successfully.
            *   `PERFORM 3000-CALC-PAYMENT`: Calculates the standard payment amount.
            *   `PERFORM 7000-CALC-OUTLIER`: Calculates outlier payments if applicable.
        *   `IF PPS-RTC < 50`: Checks if the return code is less than 50 (indicating a successful calculation).
            *   `PERFORM 8000-BLEND`: Applies blend year logic if applicable.
        *   `PERFORM 9000-MOVE-RESULTS`: Moves the calculated results to the output fields.
        *   `GOBACK`: Returns control to the calling program.

2.  **0100-INITIAL-ROUTINE:**
    *   **Description:** Initializes working storage variables and sets some constant values.
    *   **Actions:**
        *   `MOVE ZEROS TO PPS-RTC`: Initializes the return code to zero (indicating no errors).
        *   `INITIALIZE PPS-DATA`: Initializes the PPS-DATA group to its default values.
        *   `INITIALIZE PPS-OTHER-DATA`: Initializes the PPS-OTHER-DATA group.
        *   `INITIALIZE HOLD-PPS-COMPONENTS`: Initializes the HOLD-PPS-COMPONENTS group.
        *   `MOVE .72885 TO PPS-NAT-LABOR-PCT`: Sets the national labor percentage.
        *   `MOVE .27115 TO PPS-NAT-NONLABOR-PCT`: Sets the national non-labor percentage.
        *   `MOVE 34956.15 TO PPS-STD-FED-RATE`: Sets the standard federal rate.
        *   `MOVE 24450 TO H-FIXED-LOSS-AMT`: Sets the fixed loss amount.
        *   `MOVE 0.934 TO PPS-BDGT-NEUT-RATE`: Sets the budget neutrality rate.

3.  **1000-EDIT-THE-BILL-INFO:**
    *   **Description:** This paragraph validates the input bill data. If any validation fails, it sets the PPS-RTC to an error code.
    *   **Actions (Data Validation):**
        *   `IF (B-LOS NUMERIC) AND (B-LOS > 0)`: Checks if Length of Stay (LOS) is numeric and greater than zero. If not, sets `PPS-RTC` to 56 (Invalid Length of Stay).
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF P-NEW-WAIVER-STATE`: Checks if waiver state is active. If true, sets `PPS-RTC` to 53.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR (B-DISCHARGE-DATE < W-EFF-DATE))`: Checks if discharge date is before the provider's or wage index's effective date. If true, sets `PPS-RTC` to 55.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF P-NEW-TERMINATION-DATE > 00000000`: Checks if a termination date exists.
                *   `IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is on or after the termination date. If true, sets `PPS-RTC` to 51.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-COV-CHARGES NOT NUMERIC`: Checks if covered charges are numeric. If not, sets `PPS-RTC` to 58.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if Lifetime Reserve Days (LTR) is numeric and less than or equal to 60. If not, sets `PPS-RTC` to 61.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF (B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if covered days is numeric and if covered days is zero while LOS is greater than zero. If not, sets `PPS-RTC` to 62.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-LTR-DAYS > B-COV-DAYS`: Checks if LTR days exceed covered days. If true, sets `PPS-RTC` to 62.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS`: Calculates regular days.
            *   `COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS`: Calculates total days.
        *   `IF PPS-RTC = 00`: Calls 1200-DAYS-USED to determine how many regular and lifetime reserve days are used for calculations.

4.  **1200-DAYS-USED:**
    *   **Description:** Determines the number of regular and lifetime reserve days used for calculations based on the input data.
    *   **Logic:**
        *   `IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)`: If LTR days exist but regular days are zero.
            *   `IF B-LTR-DAYS > H-LOS`: If LTR days are greater than LOS, use LOS for LTR days used.
            *   `ELSE`: Otherwise, use LTR days for LTR days used.
        *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)`: If regular days exist but LTR days are zero.
            *   `IF H-REG-DAYS > H-LOS`: If regular days are greater than LOS, use LOS for regular days used.
            *   `ELSE`: Otherwise, use regular days for regular days used.
        *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)`: If both regular and LTR days exist.
            *   `IF H-REG-DAYS > H-LOS`: If regular days are greater than LOS, use LOS for regular days used and set LTR days used to zero.
            *   `ELSE IF H-TOTAL-DAYS > H-LOS`: If total days are greater than LOS, use regular days for regular days used and calculate LTR days used.
            *   `ELSE IF H-TOTAL-DAYS <= H-LOS`: If total days are less than or equal to LOS, use regular days for regular days used and LTR days for LTR days used.
        *   `ELSE`: (Neither regular nor LTR days exist).  No action.

5.  **1700-EDIT-DRG-CODE:**
    *   **Description:** This paragraph searches for the DRG code in the `WWM-ENTRY` table (defined by the `COPY LTDRG031` statement).
    *   **Actions:**
        *   `MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE`: Moves the DRG code from the input bill data to a working storage variable.
        *   `IF PPS-RTC = 00`: Checks if no errors have occurred.
            *   `SEARCH ALL WWM-ENTRY`: Performs a binary search on the `WWM-ENTRY` table.
                *   `AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, sets `PPS-RTC` to 54 (DRG not found).
                *   `WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE`: If the DRG code is found.
                    *   `PERFORM 1750-FIND-VALUE`: Calls 1750-FIND-VALUE to retrieve the DRG's associated values.

6.  **1750-FIND-VALUE:**
    *   **Description:**  This paragraph retrieves the relative weight and average length of stay for the found DRG.
    *   **Actions:**
        *   `MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT`: Moves the relative weight from the DRG table to the `PPS-RELATIVE-WGT` field.
        *   `MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS`: Moves the average length of stay from the DRG table to the `PPS-AVG-LOS` field.

7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   **Description:** This paragraph retrieves and assembles the necessary PPS variables, including the wage index and blend year indicator.
    *   **Actions:**
        *   `IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0`: Checks if `W-WAGE-INDEX1` is numeric and greater than zero.
            *   `MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX`: Moves the wage index to the `PPS-WAGE-INDEX` field.
            *   `ELSE`: If not numeric or zero, sets `PPS-RTC` to 52 (Invalid Wage Index) and goes to the exit.
        *   `IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC`: Checks if the operating cost-to-charge ratio is numeric. If not, sets `PPS-RTC` to 65.
        *   `MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR`: Moves the blend year indicator from the provider record to `PPS-BLEND-YEAR`.
        *   `IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6`: Validates that the blend year indicator is within the valid range (1-5). If valid, processing continues.  If invalid sets `PPS-RTC` to 72.
        *   Sets blend factors and return codes based on the `PPS-BLEND-YEAR`.

8.  **3000-CALC-PAYMENT:**
    *   **Description:**  Calculates the standard payment amount, and then calls the short stay routine.
    *   **Actions:**
        *   `MOVE P-NEW-COLA TO PPS-COLA`: Moves the cost of living allowance (COLA) to `PPS-COLA`.
        *   `COMPUTE PPS-FAC-COSTS ROUNDED = P-NEW-OPER-CSTCHG-RATIO * B-COV-CHARGES`: Calculates the facility costs.
        *   `COMPUTE H-LABOR-PORTION ROUNDED = (PPS-STD-FED-RATE * PPS-NAT-LABOR-PCT) * PPS-WAGE-INDEX`: Calculates the labor portion of the payment.
        *   `COMPUTE H-NONLABOR-PORTION ROUNDED = (PPS-STD-FED-RATE * PPS-NAT-NONLABOR-PCT) * PPS-COLA`: Calculates the non-labor portion of the payment.
        *   `COMPUTE PPS-FED-PAY-AMT ROUNDED = (H-LABOR-PORTION + H-NONLABOR-PORTION)`: Calculates the federal payment amount.
        *   `COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED = (PPS-FED-PAY-AMT * PPS-RELATIVE-WGT)`: Calculates the DRG adjusted payment amount.
        *   `COMPUTE H-SSOT = (PPS-AVG-LOS / 6) * 5`: Calculates short stay outlier threshold.
        *   `IF H-LOS <= H-SSOT`:  If the length of stay is less than or equal to 5/6 of the average length of stay, calls the short stay routine.
            *   `PERFORM 3400-SHORT-STAY`: Calls the short stay calculation routine.

9.  **3400-SHORT-STAY:**
    *   **Description:** Calculates the short-stay payment if the length of stay is less than or equal to 5/6 of the average length of stay.
    *   **Actions:**
        *   `COMPUTE H-SS-COST ROUNDED = (PPS-FAC-COSTS * 1.2)`: Calculates the short-stay cost (facility costs * 1.2).
        *   `COMPUTE H-SS-PAY-AMT ROUNDED = ((PPS-DRG-ADJ-PAY-AMT / PPS-AVG-LOS) * H-LOS) * 1.2`: Calculates the short-stay payment amount.
        *   `IF H-SS-COST < H-SS-PAY-AMT`: Compares the short-stay cost with the short-stay payment amount.
            *   `IF H-SS-COST < PPS-DRG-ADJ-PAY-AMT`: Compares the smaller of the previous two with the DRG adjusted payment amount.
                *   `MOVE H-SS-COST TO PPS-DRG-ADJ-PAY-AMT`:  If the short-stay cost is the lowest, sets the DRG adjusted payment amount to the short-stay cost.
                *   `MOVE 02 TO PPS-RTC`: Sets the return code to 02 (Short stay payment without outlier).
        *   `ELSE`:
            *   `IF H-SS-PAY-AMT < PPS-DRG-ADJ-PAY-AMT`: Compares the short-stay payment amount with DRG adjusted payment amount.
                *   `MOVE H-SS-PAY-AMT TO PPS-DRG-ADJ-PAY-AMT`:  If the short-stay payment amount is the lowest, sets the DRG adjusted payment amount to the short-stay payment amount.
                *   `MOVE 02 TO PPS-RTC`: Sets the return code to 02 (Short stay payment without outlier).

10. **7000-CALC-OUTLIER:**
    *   **Description:** Calculates outlier payments if applicable.
    *   **Actions:**
        *   `COMPUTE PPS-OUTLIER-THRESHOLD ROUNDED = PPS-DRG-ADJ-PAY-AMT + H-FIXED-LOSS-AMT`: Calculates the outlier threshold.
        *   `IF PPS-FAC-COSTS > PPS-OUTLIER-THRESHOLD`: Checks if facility costs exceed the outlier threshold.
            *   `COMPUTE PPS-OUTLIER-PAY-AMT ROUNDED = ((PPS-FAC-COSTS - PPS-OUTLIER-THRESHOLD) * .8) * PPS-BDGT-NEUT-RATE * H-BLEND-PPS`: Calculates the outlier payment amount.
        *   `IF B-SPEC-PAY-IND = '1'`:  If the special payment indicator is '1', the outlier payment is set to zero.
        *   `IF PPS-OUTLIER-PAY-AMT > 0 AND PPS-RTC = 02`: If an outlier payment exists and it's a short stay, set return code to 03.
        *   `IF PPS-OUTLIER-PAY-AMT > 0 AND PPS-RTC = 00`: If an outlier payment exists and it's not short stay, set return code to 01.
        *   `IF PPS-RTC = 00 OR 02`: If it's a normal or short stay payment.
            *   `IF PPS-REG-DAYS-USED > H-SSOT`: Checks if the regular days used are greater than the short stay outlier threshold.  If true, sets LTR days used to 0.
        *   `IF PPS-RTC = 01 OR 03`: If it's an outlier payment.
            *   `IF (B-COV-DAYS < H-LOS) OR PPS-COT-IND = 'Y'`: Checks if covered days are less than LOS or if the cost outlier indicator is 'Y'.
                *   `COMPUTE PPS-CHRG-THRESHOLD ROUNDED = PPS-OUTLIER-THRESHOLD / P-NEW-OPER-CSTCHG-RATIO`: Calculates charge threshold.
                *   `MOVE 67 TO PPS-RTC`: Sets the return code to 67.

11. **8000-BLEND:**
    *   **Description:** Applies blend year logic to the payment calculations.
    *   **Actions:**
        *   `COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED = (PPS-DRG-ADJ-PAY-AMT * PPS-BDGT-NEUT-RATE) * H-BLEND-PPS`: Applies budget neutrality and blend percentage to DRG adjusted payment.
        *   `COMPUTE PPS-NEW-FAC-SPEC-RATE ROUNDED = (P-NEW-FAC-SPEC-RATE * PPS-BDGT-NEUT-RATE) * H-BLEND-FAC`: Applies budget neutrality and blend percentage to facility specific rate.
        *   `COMPUTE PPS-FINAL-PAY-AMT = PPS-DRG-ADJ-PAY-AMT + PPS-OUTLIER-PAY-AMT + PPS-NEW-FAC-SPEC-RATE`: Calculates the final payment amount.
        *   `ADD H-BLEND-RTC TO PPS-RTC`: Adds the blend year return code to the existing return code.

12. **9000-MOVE-RESULTS:**
    *   **Description:** Moves calculated results to the output fields.
    *   **Actions:**
        *   `IF PPS-RTC < 50`:  If no errors occurred.
            *   `MOVE H-LOS TO PPS-LOS`: Moves LOS to the output.
            *   `MOVE 'V03.2' TO PPS-CALC-VERS-CD`: Moves the calculation version code.
        *   `ELSE`: If errors occurred.
            *   `INITIALIZE PPS-DATA`: Initializes the PPS-DATA group.
            *   `INITIALIZE PPS-OTHER-DATA`: Initializes the PPS-OTHER-DATA group.
            *   `MOVE 'V03.2' TO PPS-CALC-VERS-CD`: Moves the calculation version code.

### Business Rules

*   **Payment Calculation:** The program calculates payments based on the DRG, length of stay, and facility-specific data.
*   **DRG Lookup:**  The program retrieves DRG-specific information from the `LTDRG031` table.
*   **Short-Stay Payment:** If the length of stay is less than or equal to 5/6 of the average length of stay, a short-stay payment calculation is performed.
*   **Outlier Payment:**  Outlier payments are calculated if the facility costs exceed a calculated threshold.
*   **Blend Year Payment:** The program applies blend year logic based on the provider's blend year indicator, which affects the percentage of facility-specific and DRG payments.
*   **Data Validation:** Extensive data validation is performed to ensure the integrity of the input data.  If validation fails, the program sets an appropriate return code.
*   **Effective Date:** The program is designed to be effective for claims with a discharge date on or after January 1, 2003.

### Data Validation and Error Handling Logic

*   **Input Data Validation (1000-EDIT-THE-BILL-INFO):**
    *   **B-LOS:** Must be numeric and greater than zero (PPS-RTC = 56).
    *   **P-NEW-WAIVER-STATE:** If 'Y', set `PPS-RTC` to 53.
    *   **B-DISCHARGE-DATE vs. P-NEW-EFF-DATE & W-EFF-DATE:** Discharge date must be on or after the effective dates (PPS-RTC = 55).
    *   **P-NEW-TERMINATION-DATE:** If a termination date exists, discharge date must be before termination date (PPS-RTC = 51).
    *   **B-COV-CHARGES:** Must be numeric (PPS-RTC = 58).
    *   **B-LTR-DAYS:** Must be numeric and less than or equal to 60 (PPS-RTC = 61).
    *   **B-COV-DAYS:** Must be numeric, and must be greater than zero if LOS is greater than zero (PPS-RTC = 62).
    *   **B-LTR-DAYS vs. B-COV-DAYS:** LTR days must not exceed covered days (PPS-RTC = 62).
*   **DRG Code Validation (1700-EDIT-DRG-CODE):**
    *   The DRG code must be found in the DRG table (PPS-RTC = 54).
*   **PPS Variable Validation (2000-ASSEMBLE-PPS-VARIABLES):**
    *   **W-WAGE-INDEX1:** Must be numeric and greater than zero (PPS-RTC = 52).
    *   **P-NEW-OPER-CSTCHG-RATIO:** Must be numeric (PPS-RTC = 65).
    *   **PPS-BLEND-YEAR:** Must be between 1 and 5 (PPS-RTC = 72).
*   **Other Checks:**
    *   Provider specific COLA must be numeric (PPS-RTC = 50).

*   **Error Handling:** The program uses a `PPS-RTC` field to store error codes.  The value of `PPS-RTC` is checked throughout the program. If `PPS-RTC` is not zero (00) at any point, it indicates an error, and the program either stops processing or alters its calculations accordingly.

## Analysis of COBOL Program LTCAL042

### Program Overview

*   **Program ID:** LTCAL042
*   **Purpose:** This COBOL program calculates Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) for the fiscal year 2003, effective July 1, 2003. This is a modified version of LTCAL032. It receives bill data as input, performs edits, looks up DRG information, calculates payments (including short stay and outlier adjustments), and returns the results.
*   **Key Features:**
    *   Data validation and error handling.
    *   DRG code lookup in a table (LTDRG031, included via COPY).
    *   Calculation of standard payments.
    *   Short-stay payment calculations.  Includes a special provider calculation.
    *   Outlier payment calculations.
    *   Blend year calculations for facilities in transition.
    *   Returns a return code (PPS-RTC) indicating the payment method.
    *   Contains logic to handle a special provider (332006) for short-stay calculations.
    *   Uses LOS-RATIO in the blend calculation

### Paragraph Execution Order and Descriptions

1.  **0000-MAINLINE-CONTROL:**
    *   **Description:** This is the main control paragraph. It orchestrates the program's execution flow by calling other paragraphs in a defined sequence.
    *   **Execution Order:**
        *   `PERFORM 0100-INITIAL-ROUTINE`: Initializes working storage variables.
        *   `PERFORM 1000-EDIT-THE-BILL-INFO`: Performs data validation and edits on the input bill data.
        *   `IF PPS-RTC = 00`: Checks if any edit errors occurred. If no errors, continues to next steps.
            *   `PERFORM 1700-EDIT-DRG-CODE`: Looks up the DRG code in the DRG table.
        *   `IF PPS-RTC = 00`: Checks if DRG lookup was successful.
            *   `PERFORM 2000-ASSEMBLE-PPS-VARIABLES`: Assembles the necessary PPS variables.
        *   `IF PPS-RTC = 00`: Checks if PPS variables were assembled successfully.
            *   `PERFORM 3000-CALC-PAYMENT`: Calculates the standard payment amount.
            *   `PERFORM 7000-CALC-OUTLIER`: Calculates outlier payments if applicable.
        *   `IF PPS-RTC < 50`: Checks if the return code is less than 50 (indicating a successful calculation).
            *   `PERFORM 8000-BLEND`: Applies blend year logic if applicable.
        *   `PERFORM 9000-MOVE-RESULTS`: Moves the calculated results to the output fields.
        *   `GOBACK`: Returns control to the calling program.

2.  **0100-INITIAL-ROUTINE:**
    *   **Description:** Initializes working storage variables and sets some constant values.
    *   **Actions:**
        *   `MOVE ZEROS TO PPS-RTC`: Initializes the return code to zero (indicating no errors).
        *   `INITIALIZE PPS-DATA`: Initializes the PPS-DATA group to its default values.
        *   `INITIALIZE PPS-OTHER-DATA`: Initializes the PPS-OTHER-DATA group.
        *   `INITIALIZE HOLD-PPS-COMPONENTS`: Initializes the HOLD-PPS-COMPONENTS group.
        *   `MOVE .72885 TO PPS-NAT-LABOR-PCT`: Sets the national labor percentage.
        *   `MOVE .27115 TO PPS-NAT-NONLABOR-PCT`: Sets the national non-labor percentage.
        *   `MOVE 35726.18 TO PPS-STD-FED-RATE`: Sets the standard federal rate.
        *   `MOVE 19590 TO H-FIXED-LOSS-AMT`: Sets the fixed loss amount.
        *   `MOVE 0.940 TO PPS-BDGT-NEUT-RATE`: Sets the budget neutrality rate.

3.  **1000-EDIT-THE-BILL-INFO:**
    *   **Description:** This paragraph validates the input bill data. If any validation fails, it sets the PPS-RTC to an error code.
    *   **Actions (Data Validation):**
        *   `IF (B-LOS NUMERIC) AND (B-LOS > 0)`: Checks if Length of Stay (LOS) is numeric and greater than zero. If not, sets `PPS-RTC` to 56 (Invalid Length of Stay).
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF P-NEW-COLA NOT NUMERIC`: Checks if the cost of living allowance (COLA) is numeric. If not, sets `PPS-RTC` to 50.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF P-NEW-WAIVER-STATE`: Checks if waiver state is active. If true, sets `PPS-RTC` to 53.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR (B-DISCHARGE-DATE < W-EFF-DATE))`: Checks if discharge date is before the provider's or wage index's effective date. If true, sets `PPS-RTC` to 55.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF P-NEW-TERMINATION-DATE > 00000000`: Checks if a termination date exists.
                *   `IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is on or after the termination date. If true, sets `PPS-RTC` to 51.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-COV-CHARGES NOT NUMERIC`: Checks if covered charges are numeric. If not, sets `PPS-RTC` to 58.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if Lifetime Reserve Days (LTR) is numeric and less than or equal to 60. If not, sets `PPS-RTC` to 61.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF (B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if covered days is numeric and if covered days is zero while LOS is greater than zero. If not, sets `PPS-RTC` to 62.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `IF B-LTR-DAYS > B-COV-DAYS`: Checks if LTR days exceed covered days. If true, sets `PPS-RTC` to 62.
        *   `IF PPS-RTC = 00`: Checks if no errors up to this point.
            *   `COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS`: Calculates regular days.
            *   `COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS`: Calculates total days.
        *   `IF PPS-RTC = 00`: Calls 1200-DAYS-USED to determine how many regular and lifetime reserve days are used for calculations.

4.  **1200-DAYS-USED:**
    *   **Description:** Determines the number of regular and lifetime reserve days used for calculations based on the input data.
    *   **Logic:**
        *   `IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)`: If LTR days exist but regular days are zero.
            *   `IF B-LTR-DAYS > H-LOS`: If LTR days are greater than LOS, use LOS for LTR days used.
            *   `ELSE`: Otherwise, use LTR days for LTR days used.
        *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)`: If regular days exist but LTR days are zero.
            *   `IF H-REG-DAYS > H-LOS`: If regular days are greater than LOS, use LOS for regular days used.
            *   `ELSE`: Otherwise, use regular days for regular days used.
        *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)`: If both regular and LTR days exist.
            *   `IF H-REG-DAYS > H-LOS`: If regular days are greater than LOS, use LOS for regular days used and set LTR days used to zero.
            *   `ELSE IF H-TOTAL-DAYS > H-LOS`: If total days are greater than LOS, use regular days for regular days used and calculate LTR days used.
            *   `ELSE IF H-TOTAL-DAYS <= H-LOS`: If total days are less than or equal to LOS, use regular days for regular days used and LTR days for LTR days used.
        *   `ELSE`: (Neither regular nor LTR days exist).  No action.

5.  **1700-EDIT-DRG-CODE:**
    *   **Description:** This paragraph searches for the DRG code in the `WWM-ENTRY` table (defined by the `COPY LTDRG031` statement).
    *   **Actions:**
        *   `MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE`: Moves the DRG code from the input bill data to a working storage variable.
        *   `IF PPS-RTC = 00`: Checks if no errors have occurred.
            *   `SEARCH ALL WWM-ENTRY`: Performs a binary search on the `WWM-ENTRY` table.
                *   `AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, sets `PPS-RTC` to 54 (DRG not found).
                *   `WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE`: If the DRG code is found.
                    *   `PERFORM 1750-FIND-VALUE`: Calls 1750-FIND-VALUE to retrieve the DRG's associated values.

6.  **1750-FIND-VALUE:**
    *   **Description:**  This paragraph retrieves the relative weight and average length of stay for the found DRG.
    *   **Actions:**
        *   `MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT`: Moves the relative weight from the DRG table to the `PPS-RELATIVE-WGT` field.
        *   `MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS`: Moves the average length of stay from the DRG table to the `PPS-AVG-LOS` field.

7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   **Description:** This paragraph retrieves and assembles the necessary PPS variables, including the wage index and blend year indicator.
    *   **Actions:**
        *   `IF P-NEW-FY-BEGIN-DATE >= 20031001 AND B-DISCHARGE-DATE >= P-NEW-FY-BEGIN-DATE`: Checks if Provider's Fiscal Year (FY) begin date is on or after October 1, 2003 AND if the bill's discharge date is on or after the provider's FY begin date.
            *   `IF W-WAGE-INDEX2 NUMERIC AND W-WAGE-INDEX2 > 0`: If the above conditions are met,