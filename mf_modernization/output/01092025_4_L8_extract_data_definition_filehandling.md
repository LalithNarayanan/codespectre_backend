Here's an analysis of the provided COBOL programs:

## LTCAL032

**Files Accessed:**

*   **COPY LTDRG031:** This is a copybook (included via the `COPY` statement).  It's likely a data structure containing DRG (Diagnosis Related Group) information, used for calculations.  The exact nature of the data within `LTDRG031` can be determined by examining its content.

**Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:**
    *   PIC X(46) - A 46-character alphanumeric field containing the program's name and a description ("LTCAL032 - W O R K I N G S T O R A G E").  Used for identification or debugging.
*   **CAL-VERSION:**
    *   PIC X(05) - A 5-character alphanumeric field storing the calculation version ("C03.2").  Used for version control.
*   **HOLD-PPS-COMPONENTS:**
    *   A group of data items used to store intermediate calculation results.
        *   **H-LOS:** PIC 9(03) - Length of Stay (LOS), 3 digits.
        *   **H-REG-DAYS:** PIC 9(03) - Regular Days, 3 digits.
        *   **H-TOTAL-DAYS:** PIC 9(05) - Total Days, 5 digits.
        *   **H-SSOT:** PIC 9(02) -  Likely Short Stay Outlier Threshold, 2 digits.
        *   **H-BLEND-RTC:** PIC 9(02) - Blend Return Code, 2 digits.
        *   **H-BLEND-FAC:** PIC 9(01)V9(01) - Blend Facility Percentage, 2 digits with an implied decimal (e.g., 0.8).
        *   **H-BLEND-PPS:** PIC 9(01)V9(01) - Blend PPS Percentage, 2 digits with an implied decimal.
        *   **H-SS-PAY-AMT:** PIC 9(07)V9(02) - Short Stay Payment Amount, 9 digits with 2 decimal places.
        *   **H-SS-COST:** PIC 9(07)V9(02) - Short Stay Cost, 9 digits with 2 decimal places.
        *   **H-LABOR-PORTION:** PIC 9(07)V9(06) - Labor Portion, 7 digits with 6 decimal places.
        *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06) - Non-Labor Portion, 7 digits with 6 decimal places.
        *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02) - Fixed Loss Amount, 7 digits with 2 decimal places.
        *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - New Facility Specific Rate, 5 digits with 2 decimal places.
*   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05) - National Labor Percentage, 1 digit with 5 decimal places.
*   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05) - National Non-Labor Percentage, 1 digit with 5 decimal places.
*   **PPS-STD-FED-RATE:** PIC 9(05)V9(02) - Standard Federal Rate, 5 digits with 2 decimal places.
*   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02) - Fixed Loss Amount, 7 digits with 2 decimal places.
*   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03) - Budget Neutrality Rate, 1 digit with 3 decimal places.

**Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:**  This is the main input data structure, passed from the calling program.  It contains billing information.
    *   **B-NPI10:**  National Provider Identifier (NPI)
        *   **B-NPI8:** PIC X(08) - 8-character NPI (first part).
        *   **B-NPI-FILLER:** PIC X(02) - 2-character filler (second part).
    *   **B-PROVIDER-NO:** PIC X(06) - Provider Number, 6 characters.
    *   **B-PATIENT-STATUS:** PIC X(02) - Patient Status, 2 characters.
    *   **B-DRG-CODE:** PIC X(03) - DRG Code, 3 characters.
    *   **B-LOS:** PIC 9(03) - Length of Stay, 3 digits.
    *   **B-COV-DAYS:** PIC 9(03) - Covered Days, 3 digits.
    *   **B-LTR-DAYS:** PIC 9(02) - Lifetime Reserve Days, 2 digits.
    *   **B-DISCHARGE-DATE:** Discharge Date
        *   **B-DISCHG-CC:** PIC 9(02) - Century Code, 2 digits.
        *   **B-DISCHG-YY:** PIC 9(02) - Year, 2 digits.
        *   **B-DISCHG-MM:** PIC 9(02) - Month, 2 digits.
        *   **B-DISCHG-DD:** PIC 9(02) - Day, 2 digits.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02) - Covered Charges, 7 digits with 2 decimal places.
    *   **B-SPEC-PAY-IND:** PIC X(01) - Special Payment Indicator, 1 character.
    *   **FILLER:** PIC X(13) - Unused filler, 13 characters.
*   **PPS-DATA-ALL:** This is the main output data structure, passed back to the calling program.  It contains the calculated PPS (Prospective Payment System) data.
    *   **PPS-RTC:** PIC 9(02) - Return Code, 2 digits (indicates payment type/reason for non-payment).
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02) - Charge Threshold, 7 digits with 2 decimal places.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04) - Metropolitan Statistical Area (MSA) code, 4 characters.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04) - Wage Index, 2 digits with 4 decimal places.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01) - Average Length of Stay, 2 digits with 1 decimal place.
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04) - Relative Weight, 1 digit with 4 decimal places.
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02) - Outlier Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-LOS:** PIC 9(03) - Length of Stay, 3 digits.
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02) - DRG Adjusted Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02) - Federal Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02) - Final Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02) - Facility Costs, 7 digits with 2 decimal places.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02) - New Facility Specific Rate, 7 digits with 2 decimal places.
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02) - Outlier Threshold, 7 digits with 2 decimal places.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03) - Submitted DRG Code, 3 characters.
        *   **PPS-CALC-VERS-CD:** PIC X(05) - Calculation Version Code, 5 characters.
        *   **PPS-REG-DAYS-USED:** PIC 9(03) - Regular Days Used, 3 digits.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03) - Lifetime Reserve Days Used, 3 digits.
        *   **PPS-BLEND-YEAR:** PIC 9(01) - Blend Year, 1 digit.
        *   **PPS-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment, 1 digit with 3 decimal places.
        *   **FILLER:** PIC X(04) - Filler, 4 characters.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05) - National Labor Percentage, 1 digit with 5 decimal places.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05) - National Non-Labor Percentage, 1 digit with 5 decimal places.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02) - Standard Federal Rate, 5 digits with 2 decimal places.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03) - Budget Neutrality Rate, 1 digit with 3 decimal places.
        *   **FILLER:** PIC X(20) - Filler, 20 characters.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01) - Cost Outlier Indicator, 1 character.
        *   **FILLER:** PIC X(20) - Filler, 20 characters.
*   **PRICER-OPT-VERS-SW:**  Version information for the calling program.
    *   **PRICER-OPTION-SW:** PIC X(01) - Option Switch, 1 character.
        *   **ALL-TABLES-PASSED:** VALUE 'A' - Indicates all tables were passed.
        *   **PROV-RECORD-PASSED:** VALUE 'P' - Indicates the provider record was passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05) - Version of the PPDRV program, 5 characters.
*   **PROV-NEW-HOLD:**  Provider record data.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08) - NPI (first part), 8 characters.
            *   **P-NEW-NPI-FILLER:** PIC X(02) - NPI (second part), 2 characters.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02) - State, 2 digits.
            *   **FILLER:** PIC X(04) - Filler, 4 characters.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:** Effective Date
                *   **P-NEW-EFF-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-REPORT-DATE:** Report Date
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-TERMINATION-DATE:** Termination Date
                *   **P-NEW-TERM-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-TERM-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-TERM-DT-DD:** PIC 9(02) - Day, 2 digits.
        *   **P-NEW-WAIVER-CODE:** PIC X(01) - Waiver Code, 1 character.
            *   **P-NEW-WAIVER-STATE:** VALUE 'Y' - Indicates the waiver state is 'Y'.
        *   **P-NEW-INTER-NO:** PIC 9(05) - Internal Number, 5 digits.
        *   **P-NEW-PROVIDER-TYPE:** PIC X(02) - Provider Type, 2 characters.
        *   **P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01) - Current Census Division, 1 digit.
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** Redefines the same storage location.
        *   **P-NEW-MSA-DATA:** MSA Data
            *   **P-NEW-CHG-CODE-INDEX:** PIC X - Charge Code Index, 1 character.
            *   **P-NEW-GEO-LOC-MSAX:** PIC X(04) - Geographic Location MSA Code, 4 characters.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** Redefines the same storage location.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** PIC X(04) - Wage Index Location MSA Code, 4 characters.
            *   **P-NEW-STAND-AMT-LOC-MSA:** PIC X(04) - Standard Amount Location MSA Code, 4 characters.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:** Redefines the same storage location.
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** PIC XX - Standard Rural, 2 characters.
                        *   **P-NEW-STD-RURAL-CHECK:** VALUE '  ' - Check for standard rural.
                    *   **P-NEW-RURAL-2ND:** PIC XX - Rural, 2 characters.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** PIC XX - Sole Community Hospital Year, 2 characters.
        *   **P-NEW-LUGAR:** PIC X - Lugar, 1 character.
        *   **P-NEW-TEMP-RELIEF-IND:** PIC X - Temporary Relief Indicator, 1 character.
        *   **P-NEW-FED-PPS-BLEND-IND:** PIC X - Federal PPS Blend Indicator, 1 character.
        *   **FILLER:** PIC X(05) - Filler, 5 characters.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - Facility Specific Rate, 5 digits with 2 decimal places.
            *   **P-NEW-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment, 1 digit with 3 decimal places.
            *   **P-NEW-INTERN-RATIO:** PIC 9(01)V9(04) - Intern Ratio, 1 digit with 4 decimal places.
            *   **P-NEW-BED-SIZE:** PIC 9(05) - Bed Size, 5 digits.
            *   **P-NEW-OPER-CSTCHG-RATIO:** PIC 9(01)V9(03) - Operating Cost to Charge Ratio, 1 digit with 3 decimal places.
            *   **P-NEW-CMI:** PIC 9(01)V9(04) - Case Mix Index, 1 digit with 4 decimal places.
            *   **P-NEW-SSI-RATIO:** PIC V9(04) - SSI Ratio, 4 decimal places.
            *   **P-NEW-MEDICAID-RATIO:** PIC V9(04) - Medicaid Ratio, 4 decimal places.
            *   **P-NEW-PPS-BLEND-YR-IND:** PIC 9(01) - PPS Blend Year Indicator, 1 digit.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** PIC 9(01)V9(05) - Pruf Update Factor, 1 digit with 5 decimal places.
            *   **P-NEW-DSH-PERCENT:** PIC V9(04) - DSH Percentage, 4 decimal places.
            *   **P-NEW-FYE-DATE:** PIC X(08) - Fiscal Year End Date, 8 characters.
        *   **FILLER:** PIC X(23) - Filler, 23 characters.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** PIC 9(04)V99 - Passed Amount Capital, 4 digits with 2 decimal places.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** PIC 9(04)V99 - Passed Amount Direct Medical Education, 4 digits with 2 decimal places.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** PIC 9(04)V99 - Passed Amount Organ Acquisition, 4 digits with 2 decimal places.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** PIC 9(04)V99 - Passed Amount Plus Miscellaneous, 4 digits with 2 decimal places.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** PIC X - Capital PPS Pay Code, 1 character.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** PIC 9(04)V99 - Capital Hospital Specific Rate, 4 digits with 2 decimal places.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** PIC 9(04)V99 - Capital Old Harm Rate, 4 digits with 2 decimal places.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** PIC 9(01)V9999 - Capital New Harm Ratio, 1 digit with 4 decimal places.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** PIC 9V999 - Capital Cost to Charge Ratio, 3 decimal places.
            *   **P-NEW-CAPI-NEW-HOSP:** PIC X - Capital New Hospital, 1 character.
            *   **P-NEW-CAPI-IME:** PIC 9V9999 - Capital IME, 4 decimal places.
            *   **P-NEW-CAPI-EXCEPTIONS:** PIC 9(04)V99 - Capital Exceptions, 4 digits with 2 decimal places.
        *   **FILLER:** PIC X(22) - Filler, 22 characters.
*   **WAGE-NEW-INDEX-RECORD:** Wage Index data.
    *   **W-MSA:** PIC X(4) - MSA Code, 4 characters.
    *   **W-EFF-DATE:** PIC X(8) - Effective Date, 8 characters.
    *   **W-WAGE-INDEX1:** PIC S9(02)V9(04) - Wage Index 1, 2 digits with 4 decimal places (signed).
    *   **W-WAGE-INDEX2:** PIC S9(02)V9(04) - Wage Index 2, 2 digits with 4 decimal places (signed).
    *   **W-WAGE-INDEX3:** PIC S9(02)V9(04) - Wage Index 3, 2 digits with 4 decimal places (signed).

## LTCAL042

**Files Accessed:**

*   **COPY LTDRG031:**  Identical to LTCAL032, this is a copybook containing DRG information.

**Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:**
    *   PIC X(46) - A 46-character alphanumeric field containing the program's name and a description ("LTCAL042 - W O R K I N G S T O R A G E").  Used for identification or debugging.
*   **CAL-VERSION:**
    *   PIC X(05) - A 5-character alphanumeric field storing the calculation version ("C04.2").  Used for version control.
*   **HOLD-PPS-COMPONENTS:**
    *   A group of data items used to store intermediate calculation results.
        *   **H-LOS:** PIC 9(03) - Length of Stay (LOS), 3 digits.
        *   **H-REG-DAYS:** PIC 9(03) - Regular Days, 3 digits.
        *   **H-TOTAL-DAYS:** PIC 9(05) - Total Days, 5 digits.
        *   **H-SSOT:** PIC 9(02) -  Likely Short Stay Outlier Threshold, 2 digits.
        *   **H-BLEND-RTC:** PIC 9(02) - Blend Return Code, 2 digits.
        *   **H-BLEND-FAC:** PIC 9(01)V9(01) - Blend Facility Percentage, 2 digits with an implied decimal (e.g., 0.8).
        *   **H-BLEND-PPS:** PIC 9(01)V9(01) - Blend PPS Percentage, 2 digits with an implied decimal.
        *   **H-SS-PAY-AMT:** PIC 9(07)V9(02) - Short Stay Payment Amount, 9 digits with 2 decimal places.
        *   **H-SS-COST:** PIC 9(07)V9(02) - Short Stay Cost, 9 digits with 2 decimal places.
        *   **H-LABOR-PORTION:** PIC 9(07)V9(06) - Labor Portion, 7 digits with 6 decimal places.
        *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06) - Non-Labor Portion, 7 digits with 6 decimal places.
        *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02) - Fixed Loss Amount, 7 digits with 2 decimal places.
        *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - New Facility Specific Rate, 5 digits with 2 decimal places.
        *   **H-LOS-RATIO:** PIC 9(01)V9(05) - Length of Stay Ratio, 1 digit with 5 decimal places.

**Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:**  This is the main input data structure, passed from the calling program.  It contains billing information.
    *   **B-NPI10:**  National Provider Identifier (NPI)
        *   **B-NPI8:** PIC X(08) - 8-character NPI (first part).
        *   **B-NPI-FILLER:** PIC X(02) - 2-character filler (second part).
    *   **B-PROVIDER-NO:** PIC X(06) - Provider Number, 6 characters.
    *   **B-PATIENT-STATUS:** PIC X(02) - Patient Status, 2 characters.
    *   **B-DRG-CODE:** PIC X(03) - DRG Code, 3 characters.
    *   **B-LOS:** PIC 9(03) - Length of Stay, 3 digits.
    *   **B-COV-DAYS:** PIC 9(03) - Covered Days, 3 digits.
    *   **B-LTR-DAYS:** PIC 9(02) - Lifetime Reserve Days, 2 digits.
    *   **B-DISCHARGE-DATE:** Discharge Date
        *   **B-DISCHG-CC:** PIC 9(02) - Century Code, 2 digits.
        *   **B-DISCHG-YY:** PIC 9(02) - Year, 2 digits.
        *   **B-DISCHG-MM:** PIC 9(02) - Month, 2 digits.
        *   **B-DISCHG-DD:** PIC 9(02) - Day, 2 digits.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02) - Covered Charges, 7 digits with 2 decimal places.
    *   **B-SPEC-PAY-IND:** PIC X(01) - Special Payment Indicator, 1 character.
    *   **FILLER:** PIC X(13) - Unused filler, 13 characters.
*   **PPS-DATA-ALL:** This is the main output data structure, passed back to the calling program.  It contains the calculated PPS (Prospective Payment System) data.
    *   **PPS-RTC:** PIC 9(02) - Return Code, 2 digits (indicates payment type/reason for non-payment).
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02) - Charge Threshold, 7 digits with 2 decimal places.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04) - Metropolitan Statistical Area (MSA) code, 4 characters.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04) - Wage Index, 2 digits with 4 decimal places.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01) - Average Length of Stay, 2 digits with 1 decimal place.
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04) - Relative Weight, 1 digit with 4 decimal places.
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02) - Outlier Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-LOS:** PIC 9(03) - Length of Stay, 3 digits.
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02) - DRG Adjusted Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02) - Federal Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02) - Final Payment Amount, 7 digits with 2 decimal places.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02) - Facility Costs, 7 digits with 2 decimal places.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02) - New Facility Specific Rate, 7 digits with 2 decimal places.
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02) - Outlier Threshold, 7 digits with 2 decimal places.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03) - Submitted DRG Code, 3 characters.
        *   **PPS-CALC-VERS-CD:** PIC X(05) - Calculation Version Code, 5 characters.
        *   **PPS-REG-DAYS-USED:** PIC 9(03) - Regular Days Used, 3 digits.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03) - Lifetime Reserve Days Used, 3 digits.
        *   **PPS-BLEND-YEAR:** PIC 9(01) - Blend Year, 1 digit.
        *   **PPS-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment, 1 digit with 3 decimal places.
        *   **FILLER:** PIC X(04) - Filler, 4 characters.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05) - National Labor Percentage, 1 digit with 5 decimal places.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05) - National Non-Labor Percentage, 1 digit with 5 decimal places.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02) - Standard Federal Rate, 5 digits with 2 decimal places.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03) - Budget Neutrality Rate, 1 digit with 3 decimal places.
        *   **FILLER:** PIC X(20) - Filler, 20 characters.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01) - Cost Outlier Indicator, 1 character.
        *   **FILLER:** PIC X(20) - Filler, 20 characters.
*   **PRICER-OPT-VERS-SW:**  Version information for the calling program.
    *   **PRICER-OPTION-SW:** PIC X(01) - Option Switch, 1 character.
        *   **ALL-TABLES-PASSED:** VALUE 'A' - Indicates all tables were passed.
        *   **PROV-RECORD-PASSED:** VALUE 'P' - Indicates the provider record was passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05) - Version of the PPDRV program, 5 characters.
*   **PROV-NEW-HOLD:**  Provider record data.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08) - NPI (first part), 8 characters.
            *   **P-NEW-NPI-FILLER:** PIC X(02) - NPI (second part), 2 characters.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02) - State, 2 digits.
            *   **FILLER:** PIC X(04) - Filler, 4 characters.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:** Effective Date
                *   **P-NEW-EFF-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-REPORT-DATE:** Report Date
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02) - Month, 2 digits.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02) - Day, 2 digits.
            *   **P-NEW-TERMINATION-DATE:** Termination Date
                *   **P-NEW-TERM-DT-CC:** PIC 9(02) - Century Code, 2 digits.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02) - Year, 2 digits.
                *   **P-NEW-TERM-DT-MM:** PIC 9(