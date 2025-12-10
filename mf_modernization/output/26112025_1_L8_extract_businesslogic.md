## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, formatted in Markdown for clarity.

### Program: LTCAL032

*   **Program ID:** LTCAL032
*   **Version:** C03.2
*   **Purpose:**  Calculates Long-Term Care (LTC) payments based on the DRG, length of stay, and other billing information.  This version is for the FY2003, effective January 1, 2003.

#### 1.  Paragraph Execution Order and Description

Here's a breakdown of the paragraphs executed, along with descriptions.  Note that the `PERFORM` statements control the flow.

1.  **0000-MAINLINE-CONTROL:**  The main control paragraph.
    *   Calls the other paragraphs in a specific sequence.
    *   `PERFORM 0100-INITIAL-ROUTINE`: Initializes variables.
    *   `PERFORM 1000-EDIT-THE-BILL-INFO`: Performs initial data validation on the input bill data.
    *   `IF PPS-RTC = 00`: Conditional execution:  If no errors were found in 1000-EDIT-THE-BILL-INFO, the following paragraphs are executed.
        *   `PERFORM 1700-EDIT-DRG-CODE`:  Looks up the DRG code in a table.
        *   `PERFORM 2000-ASSEMBLE-PPS-VARIABLES`:  Gathers and prepares the necessary variables for the payment calculation.
        *   `PERFORM 3000-CALC-PAYMENT`: Calculates the standard payment amount and determines if short stay logic is needed.
        *   `PERFORM 7000-CALC-OUTLIER`: Calculates outlier payments if applicable.
        *   `PERFORM 8000-BLEND`: Applies blend logic based on the provider's blend year.
    *   `PERFORM 9000-MOVE-RESULTS`: Moves the calculated results to the output area.
    *   `GOBACK`:  Returns control to the calling program.

2.  **0100-INITIAL-ROUTINE:**
    *   `MOVE ZEROS TO PPS-RTC`: Initializes the return code (PPS-RTC) to zero, indicating no errors initially.
    *   `INITIALIZE PPS-DATA`: Clears the PPS-DATA group.
    *   `INITIALIZE PPS-OTHER-DATA`: Clears the PPS-OTHER-DATA group.
    *   `INITIALIZE HOLD-PPS-COMPONENTS`: Clears the HOLD-PPS-COMPONENTS group.
    *   `MOVE .72885 TO PPS-NAT-LABOR-PCT`: Sets the National Labor Percentage.
    *   `MOVE .27115 TO PPS-NAT-NONLABOR-PCT`: Sets the National Non-Labor Percentage.
    *   `MOVE 34956.15 TO PPS-STD-FED-RATE`: Sets the Standard Federal Rate.
    *   `MOVE 24450 TO H-FIXED-LOSS-AMT`: Sets the Fixed Loss Amount.
    *   `MOVE 0.934 TO PPS-BDGT-NEUT-RATE`: Sets the Budget Neutrality Rate.

3.  **1000-EDIT-THE-BILL-INFO:**
    *   `IF (B-LOS NUMERIC) AND (B-LOS > 0)`: Checks if the Length of Stay (B-LOS) is numeric and greater than zero.
        *   If true, `MOVE B-LOS TO H-LOS`: Moves the LOS to a working storage field.
        *   `ELSE MOVE 56 TO PPS-RTC`: If the LOS is invalid, sets the return code to 56 (Invalid Length of Stay).
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF P-NEW-WAIVER-STATE`: Checks if the waiver state is active
            *   `MOVE 53 TO PPS-RTC`: If the waiver state is active, sets the return code to 53.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR (B-DISCHARGE-DATE < W-EFF-DATE))`: Checks if the discharge date is before the provider's effective date or wage index effective date.
            *   `MOVE 55 TO PPS-RTC`: If the discharge date is invalid, sets the return code to 55.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF P-NEW-TERMINATION-DATE > 00000000`: Checks if the provider has a termination date.
            *   `IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is on or after the termination date.
                *   `MOVE 51 TO PPS-RTC`: If the discharge date is invalid, sets the return code to 51.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-COV-CHARGES NOT NUMERIC`: Checks if the covered charges are numeric.
            *   `MOVE 58 TO PPS-RTC`: If the covered charges are invalid, sets the return code to 58.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if the lifetime reserve days are numeric and less than or equal to 60.
            *   `MOVE 61 TO PPS-RTC`: If the lifetime reserve days are invalid, sets the return code to 61.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF (B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if the covered days are numeric and greater than zero if the length of stay is greater than zero.
            *   `MOVE 62 TO PPS-RTC`: If the covered days are invalid, sets the return code to 62.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-LTR-DAYS > B-COV-DAYS`: Checks if the lifetime reserve days are greater than the covered days.
            *   `MOVE 62 TO PPS-RTC`: If the lifetime reserve days are invalid, sets the return code to 62.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS`: Calculates regular days.
        *   `COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS`: Calculates total days.
        *   `PERFORM 1200-DAYS-USED`: Calls subroutine to calculate days used.

4.  **1200-DAYS-USED:** This paragraph calculates the days used for regular and lifetime reserve days based on the length of stay, covered days, and lifetime reserve days.
    *   `IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)`: Checks if the lifetime reserve days are greater than zero and regular days are zero.
        *   `IF B-LTR-DAYS > H-LOS`: Checks if the lifetime reserve days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-LTR-DAYS-USED`: Moves the length of stay to the lifetime reserve days used.
        *   `ELSE MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED`: Moves the lifetime reserve days to the lifetime reserve days used.
    *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)`: Checks if the regular days are greater than zero and lifetime reserve days are zero.
        *   `IF H-REG-DAYS > H-LOS`: Checks if the regular days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-REG-DAYS-USED`: Moves the length of stay to the regular days used.
        *   `ELSE MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
    *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)`: Checks if both regular days and lifetime reserve days are greater than zero.
        *   `IF H-REG-DAYS > H-LOS`: Checks if the regular days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-REG-DAYS-USED`: Moves the length of stay to the regular days used.
            *   `MOVE 0 TO PPS-LTR-DAYS-USED`: Sets the lifetime reserve days used to zero.
        *   `ELSE IF H-TOTAL-DAYS > H-LOS`: Checks if the total days are greater than the length of stay.
            *   `MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
            *   `COMPUTE PPS-LTR-DAYS-USED = H-LOS - H-REG-DAYS`: Calculates the lifetime reserve days used.
        *   `ELSE IF H-TOTAL-DAYS <= H-LOS`: Checks if the total days are less than or equal to the length of stay.
            *   `MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
            *   `MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED`: Moves the lifetime reserve days to the lifetime reserve days used.

5.  **1700-EDIT-DRG-CODE:**
    *   `MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE`: Moves the DRG code from the input bill data to a working storage field.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `SEARCH ALL WWM-ENTRY`: Searches a table (WWM-ENTRY) for the DRG code.
            *   `AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, sets the return code to 54 (DRG on claim not found in table).
            *   `WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE`: If the DRG code is found.
                *   `PERFORM 1750-FIND-VALUE`: Calls a subroutine to retrieve the corresponding values.

6.  **1750-FIND-VALUE:**
    *   `MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT`: Moves the relative weight from the DRG table to the output area.
    *   `MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS`: Moves the average length of stay from the DRG table to the output area.

7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   `IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0`: Checks if the wage index is numeric and greater than zero.
        *   `MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX`: If the wage index is valid, moves it to the output area.
        *   `ELSE MOVE 52 TO PPS-RTC`: If the wage index is invalid, sets the return code to 52 (Invalid Wage Index).
    *   `IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC`: Checks if the operating cost-to-charge ratio is numeric.
        *   `MOVE 65 TO PPS-RTC`: If the operating cost-to-charge ratio is invalid, sets the return code to 65.
    *   `MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR`: Moves the blend year indicator to the output area.
    *   `IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6`: Checks if the blend year is between 1 and 5.
        *   If true, proceeds to calculate blend factors.
        *   `ELSE MOVE 72 TO PPS-RTC`: If the blend year is invalid, sets the return code to 72 (Invalid blend indicator).
    *   Sets blend factors and return codes based on the blend year. For example:
        *   `IF PPS-BLEND-YEAR = 1`:
            *   `MOVE .8 TO H-BLEND-FAC`: Sets the facility blend factor to 0.8.
            *   `MOVE .2 TO H-BLEND-PPS`: Sets the PPS blend factor to 0.2.
            *   `MOVE 4 TO H-BLEND-RTC`: Sets the return code for blend year 1.

8.  **3000-CALC-PAYMENT:**
    *   `MOVE P-NEW-COLA TO PPS-COLA`: Moves the COLA (Cost of Living Adjustment) to the output area.
    *   `COMPUTE PPS-FAC-COSTS ROUNDED = P-NEW-OPER-CSTCHG-RATIO * B-COV-CHARGES`: Calculates the facility costs.
    *   `COMPUTE H-LABOR-PORTION ROUNDED = (PPS-STD-FED-RATE * PPS-NAT-LABOR-PCT) * PPS-WAGE-INDEX`: Calculates the labor portion of the federal payment.
    *   `COMPUTE H-NONLABOR-PORTION ROUNDED = (PPS-STD-FED-RATE * PPS-NAT-NONLABOR-PCT) * PPS-COLA`: Calculates the non-labor portion of the federal payment.
    *   `COMPUTE PPS-FED-PAY-AMT ROUNDED = (H-LABOR-PORTION + H-NONLABOR-PORTION)`: Calculates the federal payment amount.
    *   `COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED = (PPS-FED-PAY-AMT * PPS-RELATIVE-WGT)`: Calculates the DRG adjusted payment amount.
    *   `COMPUTE H-SSOT = (PPS-AVG-LOS / 6) * 5`: Calculates the Short Stay Outlier Threshold.
    *   `IF H-LOS <= H-SSOT`: Checks if the length of stay is less than or equal to the short stay outlier threshold.
        *   `PERFORM 3400-SHORT-STAY`: If true, calls the short stay calculation subroutine.

9.  **3400-SHORT-STAY:**
    *   `COMPUTE H-SS-COST ROUNDED = (PPS-FAC-COSTS * 1.2)`: Calculates the short-stay cost (120% of facility costs).
    *   `COMPUTE H-SS-PAY-AMT ROUNDED = ((PPS-DRG-ADJ-PAY-AMT / PPS-AVG-LOS) * H-LOS) * 1.2`: Calculates the short-stay payment amount (120% of the per diem DRG payment, multiplied by the length of stay).
    *   Compares the short-stay cost, short-stay payment amount and DRG adjusted payment amount and selects the lowest to be the DRG adjusted payment amount and sets the PPS-RTC accordingly.

10. **7000-CALC-OUTLIER:**
    *   `COMPUTE PPS-OUTLIER-THRESHOLD ROUNDED = PPS-DRG-ADJ-PAY-AMT + H-FIXED-LOSS-AMT`: Calculates the outlier threshold.
    *   `IF PPS-FAC-COSTS > PPS-OUTLIER-THRESHOLD`: Checks if the facility costs exceed the outlier threshold.
        *   `COMPUTE PPS-OUTLIER-PAY-AMT ROUNDED = ((PPS-FAC-COSTS - PPS-OUTLIER-THRESHOLD) * .8) * PPS-BDGT-NEUT-RATE * H-BLEND-PPS`: Calculates the outlier payment amount.
    *   `IF B-SPEC-PAY-IND = '1'`: Checks if the bill has a special payment indicator.
        *   `MOVE 0 TO PPS-OUTLIER-PAY-AMT`: If true, sets the outlier payment amount to zero.
    *   Sets PPS-RTC based on whether an outlier payment was calculated and whether the payment was for a short stay.
    *   Adjusts PPS-LTR-DAYS-USED if the regular days used are greater than the short stay outlier threshold.
    *   Sets PPS-RTC to 67 if certain conditions are met, related to the covered days and the cost outlier indicator.

11. **8000-BLEND:**
    *   `COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED = (PPS-DRG-ADJ-PAY-AMT * PPS-BDGT-NEUT-RATE) * H-BLEND-PPS`: Applies the budget neutrality factor and the PPS blend factor to the DRG adjusted payment amount.
    *   `COMPUTE PPS-NEW-FAC-SPEC-RATE ROUNDED = (P-NEW-FAC-SPEC-RATE * PPS-BDGT-NEUT-RATE) * H-BLEND-FAC`: Applies the budget neutrality factor and the facility blend factor to the new facility specific rate.
    *   `COMPUTE PPS-FINAL-PAY-AMT = PPS-DRG-ADJ-PAY-AMT + PPS-OUTLIER-PAY-AMT + PPS-NEW-FAC-SPEC-RATE`: Calculates the final payment amount.
    *   `ADD H-BLEND-RTC TO PPS-RTC`: Adds the blend return code to the main return code.

12. **9000-MOVE-RESULTS:**
    *   `IF PPS-RTC < 50`: Checks if the return code indicates an error.
        *   If no error, moves H-LOS to PPS-LOS and sets the calculation version.
    *   `ELSE`: If there was an error, initializes the PPS data and sets the calculation version.

#### 2. Business Rules

*   **Payment Calculation:** The core logic involves calculating payments based on DRG, length of stay, and facility costs.
*   **Short Stay:** If the length of stay is less than or equal to 5/6 of the average length of stay, a short-stay payment calculation is performed.
*   **Outlier Payments:** Outlier payments are calculated if the facility costs exceed a threshold.
*   **Blending:**  The program applies blend factors based on the provider's blend year, which determines the proportion of the facility rate and the DRG payment.
*   **DRG Lookup:** The program looks up the DRG code in a table (defined in the COPY LTDRG031) to retrieve the relative weight and average length of stay.
*   **Data Validation:**  The program performs extensive data validation on the input bill data, including checks for numeric fields, valid dates, and valid values.
*   **Waiver State:**  If the provider is in a waiver state, the program does not calculate PPS.
*   **Termination Date:** The program checks if the provider has a termination date and if the discharge date is on or after the termination date.

#### 3. Data Validation and Error Handling Logic

*   **PPS-RTC:**  The `PPS-RTC` field is the primary mechanism for error handling.  It is initialized to zero, and various error conditions cause it to be set to a non-zero value.  The value indicates the specific error encountered.
*   **Input Data Validation (1000-EDIT-THE-BILL-INFO):**
    *   Checks if B-LOS (Length of Stay) is numeric and greater than zero (PPS-RTC = 56).
    *   Checks for waiver state (PPS-RTC = 53).
    *   Checks if the discharge date is before the effective date or wage index effective date (PPS-RTC = 55).
    *   Checks for termination dates (PPS-RTC = 51).
    *   Checks if B-COV-CHARGES (Covered Charges) is numeric (PPS-RTC = 58).
    *   Checks if B-LTR-DAYS (Lifetime Reserve Days) is numeric and less than or equal to 60 (PPS-RTC = 61).
    *   Checks for invalid B-COV-DAYS (Covered Days) (PPS-RTC = 62).
    *   Checks if B-LTR-DAYS is greater than B-COV-DAYS (PPS-RTC = 62).
*   **DRG Code Validation (1700-EDIT-DRG-CODE):**
    *   Checks if the DRG code exists in the table (PPS-RTC = 54).
*   **Variable Validation (2000-ASSEMBLE-PPS-VARIABLES):**
    *   Checks if the wage index is numeric and greater than zero (PPS-RTC = 52).
    *   Checks if the operating cost-to-charge ratio is numeric (PPS-RTC = 65).
    *   Checks for a valid blend year indicator (PPS-RTC = 72).
*   **Error Propagation:** The program uses `GO TO` statements to exit certain paragraphs if the `PPS-RTC` is set to a non-zero value, preventing further processing.

---

### Program: LTCAL042

*   **Program ID:** LTCAL042
*   **Version:** C04.2
*   **Purpose:**  Similar to LTCAL032, but likely with updates for a later fiscal year (FY2004), effective July 1, 2003.  It calculates Long-Term Care (LTC) payments.

#### 1. Paragraph Execution Order and Description

The execution order is almost identical to LTCAL032.

1.  **0000-MAINLINE-CONTROL:**  The main control paragraph.
    *   Calls the other paragraphs in a specific sequence.
    *   `PERFORM 0100-INITIAL-ROUTINE`: Initializes variables.
    *   `PERFORM 1000-EDIT-THE-BILL-INFO`: Performs initial data validation on the input bill data.
    *   `IF PPS-RTC = 00`: Conditional execution:  If no errors were found in 1000-EDIT-THE-BILL-INFO, the following paragraphs are executed.
        *   `PERFORM 1700-EDIT-DRG-CODE`:  Looks up the DRG code in a table.
        *   `PERFORM 2000-ASSEMBLE-PPS-VARIABLES`:  Gathers and prepares the necessary variables for the payment calculation.
        *   `PERFORM 3000-CALC-PAYMENT`: Calculates the standard payment amount and determines if short stay logic is needed.
        *   `PERFORM 7000-CALC-OUTLIER`: Calculates outlier payments if applicable.
        *   `PERFORM 8000-BLEND`: Applies blend logic based on the provider's blend year.
    *   `PERFORM 9000-MOVE-RESULTS`: Moves the calculated results to the output area.
    *   `GOBACK`:  Returns control to the calling program.

2.  **0100-INITIAL-ROUTINE:**
    *   `MOVE ZEROS TO PPS-RTC`: Initializes the return code (PPS-RTC) to zero, indicating no errors initially.
    *   `INITIALIZE PPS-DATA`: Clears the PPS-DATA group.
    *   `INITIALIZE PPS-OTHER-DATA`: Clears the PPS-OTHER-DATA group.
    *   `INITIALIZE HOLD-PPS-COMPONENTS`: Clears the HOLD-PPS-COMPONENTS group.
    *   `MOVE .72885 TO PPS-NAT-LABOR-PCT`: Sets the National Labor Percentage.
    *   `MOVE .27115 TO PPS-NAT-NONLABOR-PCT`: Sets the National Non-Labor Percentage.
    *   `MOVE 35726.18 TO PPS-STD-FED-RATE`: Sets the Standard Federal Rate.
    *   `MOVE 19590 TO H-FIXED-LOSS-AMT`: Sets the Fixed Loss Amount.
    *   `MOVE 0.940 TO PPS-BDGT-NEUT-RATE`: Sets the Budget Neutrality Rate.

3.  **1000-EDIT-THE-BILL-INFO:**
    *   `IF (B-LOS NUMERIC) AND (B-LOS > 0)`: Checks if the Length of Stay (B-LOS) is numeric and greater than zero.
        *   If true, `MOVE B-LOS TO H-LOS`: Moves the LOS to a working storage field.
        *   `ELSE MOVE 56 TO PPS-RTC`: If the LOS is invalid, sets the return code to 56 (Invalid Length of Stay).
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF P-NEW-COLA NOT NUMERIC`: Checks if the COLA (Cost of Living Adjustment) is numeric.
            *   `MOVE 50 TO PPS-RTC`: If the COLA is invalid, sets the return code to 50.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF P-NEW-WAIVER-STATE`: Checks if the waiver state is active
            *   `MOVE 53 TO PPS-RTC`: If the waiver state is active, sets the return code to 53.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR (B-DISCHARGE-DATE < W-EFF-DATE))`: Checks if the discharge date is before the provider's effective date or wage index effective date.
            *   `MOVE 55 TO PPS-RTC`: If the discharge date is invalid, sets the return code to 55.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF P-NEW-TERMINATION-DATE > 00000000`: Checks if the provider has a termination date.
            *   `IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE`: Checks if the discharge date is on or after the termination date.
                *   `MOVE 51 TO PPS-RTC`: If the discharge date is invalid, sets the return code to 51.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-COV-CHARGES NOT NUMERIC`: Checks if the covered charges are numeric.
            *   `MOVE 58 TO PPS-RTC`: If the covered charges are invalid, sets the return code to 58.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60`: Checks if the lifetime reserve days are numeric and less than or equal to 60.
            *   `MOVE 61 TO PPS-RTC`: If the lifetime reserve days are invalid, sets the return code to 61.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF (B-COV-DAYS NOT NUMERIC) OR (B-COV-DAYS = 0 AND H-LOS > 0)`: Checks if the covered days are numeric and greater than zero if the length of stay is greater than zero.
            *   `MOVE 62 TO PPS-RTC`: If the covered days are invalid, sets the return code to 62.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `IF B-LTR-DAYS > B-COV-DAYS`: Checks if the lifetime reserve days are greater than the covered days.
            *   `MOVE 62 TO PPS-RTC`: If the lifetime reserve days are invalid, sets the return code to 62.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS`: Calculates regular days.
        *   `COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS`: Calculates total days.
        *   `PERFORM 1200-DAYS-USED`: Calls subroutine to calculate days used.

4.  **1200-DAYS-USED:** This paragraph calculates the days used for regular and lifetime reserve days based on the length of stay, covered days, and lifetime reserve days.
    *   `IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)`: Checks if the lifetime reserve days are greater than zero and regular days are zero.
        *   `IF B-LTR-DAYS > H-LOS`: Checks if the lifetime reserve days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-LTR-DAYS-USED`: Moves the length of stay to the lifetime reserve days used.
        *   `ELSE MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED`: Moves the lifetime reserve days to the lifetime reserve days used.
    *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)`: Checks if the regular days are greater than zero and lifetime reserve days are zero.
        *   `IF H-REG-DAYS > H-LOS`: Checks if the regular days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-REG-DAYS-USED`: Moves the length of stay to the regular days used.
        *   `ELSE MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
    *   `ELSE IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)`: Checks if both regular days and lifetime reserve days are greater than zero.
        *   `IF H-REG-DAYS > H-LOS`: Checks if the regular days are greater than the length of stay.
            *   `MOVE H-LOS TO PPS-REG-DAYS-USED`: Moves the length of stay to the regular days used.
            *   `MOVE 0 TO PPS-LTR-DAYS-USED`: Sets the lifetime reserve days used to zero.
        *   `ELSE IF H-TOTAL-DAYS > H-LOS`: Checks if the total days are greater than the length of stay.
            *   `MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
            *   `COMPUTE PPS-LTR-DAYS-USED = H-LOS - H-REG-DAYS`: Calculates the lifetime reserve days used.
        *   `ELSE IF H-TOTAL-DAYS <= H-LOS`: Checks if the total days are less than or equal to the length of stay.
            *   `MOVE H-REG-DAYS TO PPS-REG-DAYS-USED`: Moves the regular days to the regular days used.
            *   `MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED`: Moves the lifetime reserve days to the lifetime reserve days used.

5.  **1700-EDIT-DRG-CODE:**
    *   `MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE`: Moves the DRG code from the input bill data to a working storage field.
    *   `IF PPS-RTC = 00`: Checks if any errors have been found so far.
        *   `SEARCH ALL WWM-ENTRY`: Searches a table (WWM-ENTRY) for the DRG code.
            *   `AT END MOVE 54 TO PPS-RTC`: If the DRG code is not found in the table, sets the return code to 54 (DRG on claim not found in table).
            *   `WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE`: If the DRG code is found.
                *   `PERFORM 1750-FIND-VALUE`: Calls a subroutine to retrieve the corresponding values.

6.  **1750-FIND-VALUE:**
    *   `MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT`: Moves the relative weight from the DRG table to the output area.
    *   `MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS`: Moves the average length of stay from the DRG table to the output area.

7.  **2000-ASSEMBLE-PPS-VARIABLES:**
    *   `IF P-NEW-FY-BEGIN-DATE >= 20031001 AND B-DISCHARGE-DATE >= P-NEW-FY-BEGIN-DATE`: This is a new condition to determine which wage index to use based on the provider's fiscal year begin date and the discharge date.
        *   `IF W-WAGE-INDEX2 NUMERIC AND W-WAGE-INDEX2 > 0`: Checks if the second wage index is numeric and greater than zero.
            *   `MOVE W-WAGE-INDEX2 TO PPS-WAGE-INDEX`: If the wage index is valid, moves it to the output area.
            *   `ELSE MOVE 52 TO PPS-RTC`: If the wage index is invalid, sets the return code to 52 (Invalid Wage Index).
        *   `ELSE`: If the condition is false
            *   `IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0`: Checks if the first wage index is numeric and greater than zero.
                *   `MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX`: If the wage index is valid, moves it to the output area.
                *   `ELSE MOVE 52 TO PPS-RTC`: If the wage index is invalid, sets the return code to 52 (Invalid Wage Index).
    *   `IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC`: Checks if the operating cost-to-charge ratio is numeric.
        *   `MOVE 65 TO PPS-RTC`: If the operating cost-to-charge ratio is invalid, sets the return code to 65.
    *   `MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR`: Moves the blend year indicator to the output area.
    *   `IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6`: Checks if the blend year is between 1 and 5.
        *   If true, proceeds to calculate blend factors.
        *   `ELSE MOVE 72 TO PPS-RTC`: If the blend year is invalid, sets the return code to 72 (Invalid blend indicator).
    *   Sets blend factors and return codes based on the blend year. For example:
        *   `IF PPS-BLEND-YEAR = 1`:
            *   `MOVE .8 TO H-BLEND-FAC`: Sets the facility blend factor to 0.8.
            *   `MOVE .2 TO H-BLEND-PPS`: Sets the PPS blend factor to 0.2.
            *   `MOVE 4 TO H-BLEND-RTC`: Sets the return code for blend year 1.

8.  **3000-CALC-PAYMENT:**
    *   `MOVE P-NEW-COLA TO PPS-COLA`: Moves the