Here's an analysis of the provided COBOL programs, formatted in markdown:

## LTCAL032 Analysis

### Files Accessed and Description

*   **COPY LTDRG031:** This is a copybook included in the program. It likely contains data structures or code related to DRG (Diagnosis Related Group) information.

### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL032 - W O R K I N G S T O R A G E'`:  Initializes the field with a descriptive string.  This is likely a program identifier or a comment.
*   **`CAL-VERSION`**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C03.2'`:  Initializes the field with the version number of the calculation logic.
*   **`HOLD-PPS-COMPONENTS`**:
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
    *   **`H-LOS`**:
        *   `PIC 9(03)`: A 3-digit numeric field (integer), likely representing Length of Stay.
    *   **`H-REG-DAYS`**:
        *   `PIC 9(03)`: A 3-digit numeric field (integer), likely representing Regular Days.
    *   **`H-TOTAL-DAYS`**:
        *   `PIC 9(05)`: A 5-digit numeric field (integer), likely representing Total Days.
    *   **`H-SSOT`**:
        *   `PIC 9(02)`: A 2-digit numeric field (integer), likely related to Short Stay Outlier Threshold.
    *   **`H-BLEND-RTC`**:
        *   `PIC 9(02)`: A 2-digit numeric field (integer), likely representing the Blend Return Code.
    *   **`H-BLEND-FAC`**:
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field with an implied decimal point (one digit before and one digit after), likely representing the facility blend percentage.
    *   **`H-BLEND-PPS`**:
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field with an implied decimal point (one digit before and one digit after), likely representing the PPS blend percentage.
    *   **`H-SS-PAY-AMT`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Short Stay Payment Amount.
    *   **`H-SS-COST`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Short Stay Cost.
    *   **`H-LABOR-PORTION`**:
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field with an implied decimal point (7 digits before and 6 digits after), likely representing Labor Portion.
    *   **`H-NONLABOR-PORTION`**:
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field with an implied decimal point (7 digits before and 6 digits after), likely representing Non-Labor Portion.
    *   **`H-FIXED-LOSS-AMT`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Fixed Loss Amount.
    *   **`H-NEW-FAC-SPEC-RATE`**:
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after), likely representing the new facility specific rate.
*   **`PPS-NAT-LABOR-PCT`**:
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after), likely representing National Labor Percentage.
*   **`PPS-NAT-NONLABOR-PCT`**:
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after), likely representing National Non-Labor Percentage.
*   **`PPS-STD-FED-RATE`**:
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after), likely representing Standard Federal Rate.
*   **`PPS-BDGT-NEUT-RATE`**:
        *   `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after), likely representing Budget Neutrality Rate.
*   **`HOLD-PPS-COMPONENTS`**:
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
*   **`PRICER-OPT-VERS-SW`**:
    *   **`PRICER-OPTION-SW`**:
        *   `PIC X(01)`: A 1-character alphanumeric field.
        *   **`ALL-TABLES-PASSED`**:
            *   `VALUE 'A'`:  Condition name associated with 'A'.
        *   **`PROV-RECORD-PASSED`**:
            *   `VALUE 'P'`: Condition name associated with 'P'.
    *   **`PPS-VERSIONS`**:
        *   **`PPDRV-VERSION`**:
            *   `PIC X(05)`: A 5-character alphanumeric field, likely to store version information.

### Data Structures in LINKAGE SECTION

*   **`BILL-NEW-DATA`**:  This structure represents the input data passed to the program.
    *   **`B-NPI10`**:  NPI (National Provider Identifier)
        *   **`B-NPI8`**: `PIC X(08)`:  An 8-character field for the NPI.
        *   **`B-NPI-FILLER`**: `PIC X(02)`: A 2-character filler field, likely for formatting.
    *   **`B-PROVIDER-NO`**: `PIC X(06)`:  A 6-character field for the provider number.
    *   **`B-PATIENT-STATUS`**: `PIC X(02)`: A 2-character field for patient status.
    *   **`B-DRG-CODE`**: `PIC X(03)`:  A 3-character field for the DRG code.
    *   **`B-LOS`**: `PIC 9(03)`:  A 3-digit numeric field for Length of Stay.
    *   **`B-COV-DAYS`**: `PIC 9(03)`: A 3-digit numeric field for Covered Days.
    *   **`B-LTR-DAYS`**: `PIC 9(02)`: A 2-digit numeric field for Lifetime Reserve Days.
    *   **`B-DISCHARGE-DATE`**:
        *   **`B-DISCHG-CC`**: `PIC 9(02)`:  2-digit century code for discharge date.
        *   **`B-DISCHG-YY`**: `PIC 9(02)`:  2-digit year for discharge date.
        *   **`B-DISCHG-MM`**: `PIC 9(02)`:  2-digit month for discharge date.
        *   **`B-DISCHG-DD`**: `PIC 9(02)`:  2-digit day for discharge date.
    *   **`B-COV-CHARGES`**: `PIC 9(07)V9(02)`:  A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for covered charges.
    *   **`B-SPEC-PAY-IND`**: `PIC X(01)`: A 1-character field indicating special payment.
    *   **`FILLER`**: `PIC X(13)`: A 13-character filler field.
*   **`PPS-DATA-ALL`**: This structure is used to return calculated data back to the calling program.
    *   **`PPS-RTC`**: `PIC 9(02)`:  A 2-digit numeric field for the Return Code, indicating the outcome of the pricing calculation.
    *   **`PPS-CHRG-THRESHOLD`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the charge threshold.
    *   **`PPS-DATA`**:  Group item containing PPS related data.
        *   **`PPS-MSA`**: `PIC X(04)`: A 4-character field for the MSA (Metropolitan Statistical Area) code.
        *   **`PPS-WAGE-INDEX`**: `PIC 9(02)V9(04)`: A 6-digit numeric field with an implied decimal point (2 digits before and 4 digits after) for the wage index.
        *   **`PPS-AVG-LOS`**: `PIC 9(02)V9(01)`: A 3-digit numeric field with an implied decimal point (2 digits before and 1 digit after) for the average length of stay.
        *   **`PPS-RELATIVE-WGT`**: `PIC 9(01)V9(04)`: A 5-digit numeric field with an implied decimal point (1 digit before and 4 digits after) for the relative weight.
        *   **`PPS-OUTLIER-PAY-AMT`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the outlier payment amount.
        *   **`PPS-LOS`**: `PIC 9(03)`: A 3-digit numeric field for the length of stay.
        *   **`PPS-DRG-ADJ-PAY-AMT`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the DRG adjusted payment amount.
        *   **`PPS-FED-PAY-AMT`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the federal payment amount.
        *   **`PPS-FINAL-PAY-AMT`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the final payment amount.
        *   **`PPS-FAC-COSTS`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the facility costs.
        *   **`PPS-NEW-FAC-SPEC-RATE`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the new facility specific rate.
        *   **`PPS-OUTLIER-THRESHOLD`**: `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after) for the outlier threshold.
        *   **`PPS-SUBM-DRG-CODE`**: `PIC X(03)`: A 3-character field for the submitted DRG code.
        *   **`PPS-CALC-VERS-CD`**: `PIC X(05)`: A 5-character field for the calculation version code.
        *   **`PPS-REG-DAYS-USED`**: `PIC 9(03)`: A 3-digit numeric field for the regular days used.
        *   **`PPS-LTR-DAYS-USED`**: `PIC 9(03)`: A 3-digit numeric field for the lifetime reserve days used.
        *   **`PPS-BLEND-YEAR`**: `PIC 9(01)`: A 1-digit numeric field for the blend year.
        *   **`PPS-COLA`**: `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after) for the COLA (Cost of Living Adjustment).
        *   **`FILLER`**: `PIC X(04)`: A 4-character filler field.
    *   **`PPS-OTHER-DATA`**:  Group item containing other PPS related data.
        *   **`PPS-NAT-LABOR-PCT`**: `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after) for the national labor percentage.
        *   **`PPS-NAT-NONLABOR-PCT`**: `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after) for the national non-labor percentage.
        *   **`PPS-STD-FED-RATE`**: `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after) for the standard federal rate.
        *   **`PPS-BDGT-NEUT-RATE`**: `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after) for the budget neutrality rate.
        *   **`FILLER`**: `PIC X(20)`: A 20-character filler field.
    *   **`PPS-PC-DATA`**:  Group item containing PPS related data.
        *   **`PPS-COT-IND`**: `PIC X(01)`: A 1-character field for the cost outlier indicator.
        *   **`FILLER`**: `PIC X(20)`: A 20-character filler field.
*   **`PROV-NEW-HOLD`**: This structure contains provider-specific information.
    *   **`PROV-NEWREC-HOLD1`**:
        *   **`P-NEW-NPI10`**:
            *   **`P-NEW-NPI8`**: `PIC X(08)`:  An 8-character field for the NPI.
            *   **`P-NEW-NPI-FILLER`**: `PIC X(02)`: A 2-character filler field, likely for formatting.
        *   **`P-NEW-PROVIDER-NO`**:
            *   **`P-NEW-STATE`**: `PIC 9(02)`: A 2-digit numeric field for the provider's state.
            *   **`FILLER`**: `PIC X(04)`: A 4-character filler field.
        *   **`P-NEW-DATE-DATA`**:
            *   **`P-NEW-EFF-DATE`**:
                *   **`P-NEW-EFF-DT-CC`**: `PIC 9(02)`: 2-digit century code for effective date.
                *   **`P-NEW-EFF-DT-YY`**: `PIC 9(02)`: 2-digit year for effective date.
                *   **`P-NEW-EFF-DT-MM`**: `PIC 9(02)`: 2-digit month for effective date.
                *   **`P-NEW-EFF-DT-DD`**: `PIC 9(02)`: 2-digit day for effective date.
            *   **`P-NEW-FY-BEGIN-DATE`**:
                *   **`P-NEW-FY-BEG-DT-CC`**: `PIC 9(02)`: 2-digit century code for fiscal year begin date.
                *   **`P-NEW-FY-BEG-DT-YY`**: `PIC 9(02)`: 2-digit year for fiscal year begin date.
                *   **`P-NEW-FY-BEG-DT-MM`**: `PIC 9(02)`: 2-digit month for fiscal year begin date.
                *   **`P-NEW-FY-BEG-DT-DD`**: `PIC 9(02)`: 2-digit day for fiscal year begin date.
            *   **`P-NEW-REPORT-DATE`**:
                *   **`P-NEW-REPORT-DT-CC`**: `PIC 9(02)`: 2-digit century code for report date.
                *   **`P-NEW-REPORT-DT-YY`**: `PIC 9(02)`: 2-digit year for report date.
                *   **`P-NEW-REPORT-DT-MM`**: `PIC 9(02)`: 2-digit month for report date.
                *   **`P-NEW-REPORT-DT-DD`**: `PIC 9(02)`: 2-digit day for report date.
            *   **`P-NEW-TERMINATION-DATE`**:
                *   **`P-NEW-TERM-DT-CC`**: `PIC 9(02)`: 2-digit century code for termination date.
                *   **`P-NEW-TERM-DT-YY`**: `PIC 9(02)`: 2-digit year for termination date.
                *   **`P-NEW-TERM-DT-MM`**: `PIC 9(02)`: 2-digit month for termination date.
                *   **`P-NEW-TERM-DT-DD`**: `PIC 9(02)`: 2-digit day for termination date.
        *   **`P-NEW-WAIVER-CODE`**:
            *   **`P-NEW-WAIVER-STATE`**:  Condition name for waiver state.
        *   **`P-NEW-INTER-NO`**: `PIC 9(05)`: A 5-digit numeric field for an internal number.
        *   **`P-NEW-PROVIDER-TYPE`**: `PIC X(02)`: A 2-character field for the provider type.
        *   **`P-NEW-CURRENT-CENSUS-DIV`**: `PIC 9(01)`: A 1-digit numeric field for the current census division.
        *   **`P-NEW-CURRENT-DIV`**:  Redefines `P-NEW-CURRENT-CENSUS-DIV`.
        *   **`P-NEW-MSA-DATA`**:
            *   **`P-NEW-CHG-CODE-INDEX`**: `PIC X`: A 1-character field for the charge code index.
            *   **`P-NEW-GEO-LOC-MSAX`**: `PIC X(04)`: A 4-character field for the geographic location MSA (Metropolitan Statistical Area) - right justified.
            *   **`P-NEW-GEO-LOC-MSA9`**: Redefines `P-NEW-GEO-LOC-MSAX`.
            *   **`P-NEW-WAGE-INDEX-LOC-MSA`**: `PIC X(04)`: A 4-character field for the wage index location MSA - right justified.
            *   **`P-NEW-STAND-AMT-LOC-MSA`**: `PIC X(04)`: A 4-character field for the standard amount location MSA - right justified.
            *   **`P-NEW-STAND-AMT-LOC-MSA9`**: Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                *   **`P-NEW-RURAL-1ST`**:
                    *   **`P-NEW-STAND-RURAL`**: `PIC XX`: A 2-character field for the standard rural value.
                        *   **`P-NEW-STD-RURAL-CHECK`**:  Condition name for standard rural check.
                    *   **`P-NEW-RURAL-2ND`**: `PIC XX`: A 2-character field.
        *   **`P-NEW-SOL-COM-DEP-HOSP-YR`**: `PIC XX`: A 2-character field.
        *   **`P-NEW-LUGAR`**: `PIC X`: A 1-character field.
        *   **`P-NEW-TEMP-RELIEF-IND`**: `PIC X`: A 1-character field.
        *   **`P-NEW-FED-PPS-BLEND-IND`**: `PIC X`: A 1-character field for the federal PPS blend indicator.
        *   **`FILLER`**: `PIC X(05)`: A 5-character filler field.
    *   **`PROV-NEWREC-HOLD2`**:
        *   **`P-NEW-VARIABLES`**:
            *   **`P-NEW-FAC-SPEC-RATE`**: `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after) for the facility specific rate.
            *   **`P-NEW-COLA`**: `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after) for the COLA.
            *   **`P-NEW-INTERN-RATIO`**: `PIC 9(01)V9(04)`: A 5-digit numeric field with an implied decimal point (1 digit before and 4 digits after) for the intern ratio.
            *   **`P-NEW-BED-SIZE`**: `PIC 9(05)`: A 5-digit numeric field for the bed size.
            *   **`P-NEW-OPER-CSTCHG-RATIO`**: `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after) for the operating cost-to-charge ratio.
            *   **`P-NEW-CMI`**: `PIC 9(01)V9(04)`: A 5-digit numeric field with an implied decimal point (1 digit before and 4 digits after) for the CMI (Case Mix Index).
            *   **`P-NEW-SSI-RATIO`**: `V9(04)`: A 4-digit numeric field with an implied decimal point (4 digits after) for the SSI (Supplemental Security Income) ratio.
            *   **`P-NEW-MEDICAID-RATIO`**: `V9(04)`: A 4-digit numeric field with an implied decimal point (4 digits after) for the Medicaid ratio.
            *   **`P-NEW-PPS-BLEND-YR-IND`**: `PIC 9(01)`: A 1-digit numeric field for the PPS blend year indicator.
            *   **`P-NEW-PRUF-UPDTE-FACTOR`**: `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after).
            *   **`P-NEW-DSH-PERCENT`**: `V9(04)`: A 4-digit numeric field with an implied decimal point (4 digits after) for the DSH (Disproportionate Share Hospital) percentage.
            *   **`P-NEW-FYE-DATE`**: `PIC X(08)`: An 8-character field for the fiscal year end date.
        *   **`FILLER`**: `PIC X(23)`: A 23-character filler field.
    *   **`PROV-NEWREC-HOLD3`**:
        *   **`P-NEW-PASS-AMT-DATA`**:
            *   **`P-NEW-PASS-AMT-CAPITAL`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the capital pass-through amount.
            *   **`P-NEW-PASS-AMT-DIR-MED-ED`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the direct medical education pass-through amount.
            *   **`P-NEW-PASS-AMT-ORGAN-ACQ`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the organ acquisition pass-through amount.
            *   **`P-NEW-PASS-AMT-PLUS-MISC`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the plus miscellaneous pass-through amount.
        *   **`P-NEW-CAPI-DATA`**:
            *   **`P-NEW-CAPI-PPS-PAY-CODE`**: `PIC X`: A 1-character field for the capital PPS payment code.
            *   **`P-NEW-CAPI-HOSP-SPEC-RATE`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the hospital specific capital rate.
            *   **`P-NEW-CAPI-OLD-HARM-RATE`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the old harm capital rate.
            *   **`P-NEW-CAPI-NEW-HARM-RATIO`**: `PIC 9(01)V9999`: A 5-digit numeric field with an implied decimal point (1 digit before and 4 digits after) for the new harm capital ratio.
            *   **`P-NEW-CAPI-CSTCHG-RATIO`**: `PIC 9V999`: A 4-digit numeric field with an implied decimal point (3 digits after) for the capital cost-to-charge ratio.
            *   **`P-NEW-CAPI-NEW-HOSP`**: `PIC X`: A 1-character field for the new hospital capital indicator.
            *   **`P-NEW-CAPI-IME`**: `PIC 9V9999`: A 5-digit numeric field with an implied decimal point (4 digits after) for the IME (Indirect Medical Education) capital.
            *   **`P-NEW-CAPI-EXCEPTIONS`**: `PIC 9(04)V99`: A 6-digit numeric field with an implied decimal point (4 digits before and 2 digits after) for the capital exceptions.
        *   **`FILLER`**: `PIC X(22)`: A 22-character filler field.
*   **`WAGE-NEW-INDEX-RECORD`**: This structure contains wage index information.
    *   **`W-MSA`**: `PIC X(4)`: A 4-character field for the MSA code.
    *   **`W-EFF-DATE`**: `PIC X(8)`: An 8-character field for the effective date.
    *   **`W-WAGE-INDEX1`**: `PIC S9(02)V9(04)`: A 6-digit signed numeric field with an implied decimal point (2 digits before and 4 digits after) for wage index 1.
    *   **`W-WAGE-INDEX2`**: `PIC S9(02)V9(04)`: A 6-digit signed numeric field with an implied decimal point (2 digits before and 4 digits after) for wage index 2.
    *   **`W-WAGE-INDEX3`**: `PIC S9(02)V9(04)`: A 6-digit signed numeric field with an implied decimal point (2 digits before and 4 digits after) for wage index 3.

### Summary of Program Functionality

This program, `LTCAL032`, appears to be a COBOL subroutine designed to calculate payments for long-term care (LTC) claims, likely for a government healthcare program (e.g., Medicare or Medicaid). It receives claim data, provider information, and wage index data as input, performs various edits and calculations based on DRG codes, length of stay, and other factors, and returns the calculated payment information, including an outlier payment if applicable.  The program uses a copybook `LTDRG031` which contains DRG related data.  The return code `PPS-RTC` indicates how the bill was paid.

## LTCAL042 Analysis

### Files Accessed and Description

*   **COPY LTDRG031:** This is a copybook included in the program. It likely contains data structures or code related to DRG (Diagnosis Related Group) information.

### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL042 - W O R K I N G S T O R A G E'`:  Initializes the field with a descriptive string.  This is likely a program identifier or a comment.
*   **`CAL-VERSION`**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C04.2'`:  Initializes the field with the version number of the calculation logic.
*   **`HOLD-PPS-COMPONENTS`**:
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
    *   **`H-LOS`**:
        *   `PIC 9(03)`: A 3-digit numeric field (integer), likely representing Length of Stay.
    *   **`H-REG-DAYS`**:
        *   `PIC 9(03)`: A 3-digit numeric field (integer), likely representing Regular Days.
    *   **`H-TOTAL-DAYS`**:
        *   `PIC 9(05)`: A 5-digit numeric field (integer), likely representing Total Days.
    *   **`H-SSOT`**:
        *   `PIC 9(02)`: A 2-digit numeric field (integer), likely related to Short Stay Outlier Threshold.
    *   **`H-BLEND-RTC`**:
        *   `PIC 9(02)`: A 2-digit numeric field (integer), likely representing the Blend Return Code.
    *   **`H-BLEND-FAC`**:
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field with an implied decimal point (one digit before and one digit after), likely representing the facility blend percentage.
    *   **`H-BLEND-PPS`**:
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field with an implied decimal point (one digit before and one digit after), likely representing the PPS blend percentage.
    *   **`H-SS-PAY-AMT`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Short Stay Payment Amount.
    *   **`H-SS-COST`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Short Stay Cost.
    *   **`H-LABOR-PORTION`**:
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field with an implied decimal point (7 digits before and 6 digits after), likely representing Labor Portion.
    *   **`H-NONLABOR-PORTION`**:
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field with an implied decimal point (7 digits before and 6 digits after), likely representing Non-Labor Portion.
    *   **`H-FIXED-LOSS-AMT`**:
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field with an implied decimal point (7 digits before and 2 digits after), likely representing Fixed Loss Amount.
    *   **`H-NEW-FAC-SPEC-RATE`**:
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after), likely representing the new facility specific rate.
    *   **`H-LOS-RATIO`**:
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after), likely representing the ratio of LOS to average LOS.
*   **`PPS-NAT-LABOR-PCT`**:
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after), likely representing National Labor Percentage.
*   **`PPS-NAT-NONLABOR-PCT`**:
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field with an implied decimal point (1 digit before and 5 digits after), likely representing National Non-Labor Percentage.
*   **`PPS-STD-FED-RATE`**:
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field with an implied decimal point (5 digits before and 2 digits after), likely representing Standard Federal Rate.
*   **`PPS-BDGT-NEUT-RATE`**:
        *   `PIC 9(01)V9(03)`: A 4-digit numeric field with an implied decimal point (1 digit before and 3 digits after), likely representing Budget Neutrality Rate.
*   **`HOLD-PPS-COMPONENTS`**:
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
*   **`PRICER-OPT-VERS-SW`**:
    *   **`PRICER-OPTION-SW`**:
        *   `PIC X(01)`: A 1-character alphanumeric field.
        *   **`ALL-TABLES-PASSED`**:
            *   `