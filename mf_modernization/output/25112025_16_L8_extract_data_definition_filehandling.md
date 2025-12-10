## Analysis of LTCAL032

### File Access and Description

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field.  It appears to be a program identifier or a reference to the working storage.
    *   `VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C03.2'`: Stores the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS:**
    *   A group of fields used to store intermediate calculation results.
        *   **H-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **H-REG-DAYS:** `PIC 9(03)`: Regular Days (3 digits).
        *   **H-TOTAL-DAYS:** `PIC 9(05)`: Total Days (5 digits).
        *   **H-SSOT:** `PIC 9(02)`: Short Stay Outlier Threshold (2 digits).
        *   **H-BLEND-RTC:** `PIC 9(02)`: Blend Return Code (2 digits).
        *   **H-BLEND-FAC:** `PIC 9(01)V9(01)`: Blend Facility Rate (1 integer, 1 decimal).
        *   **H-BLEND-PPS:** `PIC 9(01)V9(01)`: Blend PPS Rate (1 integer, 1 decimal).
        *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)`: Short Stay Payment Amount (7 integers, 2 decimals).
        *   **H-SS-COST:** `PIC 9(07)V9(02)`: Short Stay Cost (7 integers, 2 decimals).
        *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)`: Labor Portion (7 integers, 6 decimals).
        *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)`: Non-Labor Portion (7 integers, 6 decimals).
        *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)`: Fixed Loss Amount (7 integers, 2 decimals).
        *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: New Facility Specific Rate (5 integers, 2 decimals).
*   **W-DRG-FILLS/W-DRG-TABLE:** (Defined via COPY LTDRG031)
    *   **W-DRG-FILLS:** A series of 44-character fields containing DRG data.
    *   **W-DRG-TABLE REDEFINES W-DRG-FILLS:**  Redefines the above structure to allow for indexed access.
        *   **WWM-ENTRY OCCURS 502 TIMES:**  Defines an array of 502 entries.
            *   **WWM-DRG:** `PIC X(3)`: The DRG code (3 characters).
            *   **WWM-RELWT:** `PIC 9(1)V9(4)`: Relative Weight (1 integer, 4 decimals).
            *   **WWM-ALOS:** `PIC 9(2)V9(1)`: Average Length of Stay (2 integers, 1 decimal).

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**
    *   This is the input data structure passed to the program.
        *   **B-NPI10:**
            *   **B-NPI8:** `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters.
            *   **B-NPI-FILLER:** `PIC X(02)`:  Filler for NPI (2 characters).
        *   **B-PROVIDER-NO:** `PIC X(06)`: Provider Number (6 characters).
        *   **B-PATIENT-STATUS:** `PIC X(02)`: Patient Status (2 characters).
        *   **B-DRG-CODE:** `PIC X(03)`: DRG Code (3 characters).
        *   **B-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **B-COV-DAYS:** `PIC 9(03)`: Covered Days (3 digits).
        *   **B-LTR-DAYS:** `PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   **B-DISCHARGE-DATE:**
            *   **B-DISCHG-CC:** `PIC 9(02)`: Discharge Date - Century/Score (2 digits).
            *   **B-DISCHG-YY:** `PIC 9(02)`: Discharge Date - Year (2 digits).
            *   **B-DISCHG-MM:** `PIC 9(02)`: Discharge Date - Month (2 digits).
            *   **B-DISCHG-DD:** `PIC 9(02)`: Discharge Date - Day (2 digits).
        *   **B-COV-CHARGES:** `PIC 9(07)V9(02)`: Covered Charges (7 integers, 2 decimals).
        *   **B-SPEC-PAY-IND:** `PIC X(01)`: Special Payment Indicator (1 character).
        *   **FILLER:** `PIC X(13)`: Filler (13 characters).
*   **PPS-DATA-ALL:**
    *   This is the output data structure passed back from the program.
        *   **PPS-RTC:** `PIC 9(02)`: Return Code (2 digits).
        *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)`: Charges Threshold (7 integers, 2 decimals).
        *   **PPS-DATA:**
            *   **PPS-MSA:** `PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)`: Wage Index (2 integers, 4 decimals).
            *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)`: Average Length of Stay (2 integers, 1 decimal).
            *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)`: Relative Weight (1 integer, 4 decimals).
            *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)`: Outlier Payment Amount (7 integers, 2 decimals).
            *   **PPS-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
            *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (7 integers, 2 decimals).
            *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)`: Federal Payment Amount (7 integers, 2 decimals).
            *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)`: Final Payment Amount (7 integers, 2 decimals).
            *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)`: Facility Costs (7 integers, 2 decimals).
            *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)`: New Facility Specific Rate (7 integers, 2 decimals).
            *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)`: Outlier Threshold (7 integers, 2 decimals).
            *   **PPS-SUBM-DRG-CODE:** `PIC X(03)`: Submitted DRG Code (3 characters).
            *   **PPS-CALC-VERS-CD:** `PIC X(05)`: Calculation Version Code (5 characters).
            *   **PPS-REG-DAYS-USED:** `PIC 9(03)`: Regular Days Used (3 digits).
            *   **PPS-LTR-DAYS-USED:** `PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   **PPS-BLEND-YEAR:** `PIC 9(01)`: Blend Year (1 digit).
            *   **PPS-COLA:** `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment) (1 integer, 3 decimals).
            *   **FILLER:** `PIC X(04)`: Filler (4 characters).
        *   **PPS-OTHER-DATA:**
            *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)`: National Labor Percentage (1 integer, 5 decimals).
            *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)`: National Non-Labor Percentage (1 integer, 5 decimals).
            *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)`: Standard Federal Rate (5 integers, 2 decimals).
            *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)`: Budget Neutrality Rate (1 integer, 3 decimals).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
        *   **PPS-PC-DATA:**
            *   **PPS-COT-IND:** `PIC X(01)`: Cost Outlier Indicator (1 character).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
*   **PRICER-OPT-VERS-SW:**
    *   Used to indicate whether all tables are passed or just the provider record.
        *   **PRICER-OPTION-SW:** `PIC X(01)`:  Switch for pricer options (1 character).
            *   **ALL-TABLES-PASSED:** `VALUE 'A'`:  Condition indicating all tables passed.
            *   **PROV-RECORD-PASSED:** `VALUE 'P'`: Condition indicating only provider record passed.
        *   **PPS-VERSIONS:**
            *   **PPDRV-VERSION:** `PIC X(05)`:  Version of the PPDRV program (5 characters).
*   **PROV-NEW-HOLD:**
    *   This is the Provider record passed to the program.
        *   **PROV-NEWREC-HOLD1:**
            *   **P-NEW-NPI10:**
                *   **P-NEW-NPI8:** `PIC X(08)`: New NPI (8 characters).
                *   **P-NEW-NPI-FILLER:** `PIC X(02)`: Filler for NPI (2 characters).
            *   **P-NEW-PROVIDER-NO:**
                *   **P-NEW-STATE:** `PIC 9(02)`: State Code (2 digits).
                *   **FILLER:** `PIC X(04)`: Filler (4 characters).
            *   **P-NEW-DATE-DATA:**
                *   **P-NEW-EFF-DATE:**
                    *   **P-NEW-EFF-DT-CC:** `PIC 9(02)`: Effective Date - Century/Score (2 digits).
                    *   **P-NEW-EFF-DT-YY:** `PIC 9(02)`: Effective Date - Year (2 digits).
                    *   **P-NEW-EFF-DT-MM:** `PIC 9(02)`: Effective Date - Month (2 digits).
                    *   **P-NEW-EFF-DT-DD:** `PIC 9(02)`: Effective Date - Day (2 digits).
                *   **P-NEW-FY-BEGIN-DATE:**
                    *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)`: Fiscal Year Begin Date - Century/Score (2 digits).
                    *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)`: Fiscal Year Begin Date - Year (2 digits).
                    *   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)`: Fiscal Year Begin Date - Month (2 digits).
                    *   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)`: Fiscal Year Begin Date - Day (2 digits).
                *   **P-NEW-REPORT-DATE:**
                    *   **P-NEW-REPORT-DT-CC:** `PIC 9(02)`: Report Date - Century/Score (2 digits).
                    *   **P-NEW-REPORT-DT-YY:** `PIC 9(02)`: Report Date - Year (2 digits).
                    *   **P-NEW-REPORT-DT-MM:** `PIC 9(02)`: Report Date - Month (2 digits).
                    *   **P-NEW-REPORT-DT-DD:** `PIC 9(02)`: Report Date - Day (2 digits).
                *   **P-NEW-TERMINATION-DATE:**
                    *   **P-NEW-TERM-DT-CC:** `PIC 9(02)`: Termination Date - Century/Score (2 digits).
                    *   **P-NEW-TERM-DT-YY:** `PIC 9(02)`: Termination Date - Year (2 digits).
                    *   **P-NEW-TERM-DT-MM:** `PIC 9(02)`: Termination Date - Month (2 digits).
                    *   **P-NEW-TERM-DT-DD:** `PIC 9(02)`: Termination Date - Day (2 digits).
            *   **P-NEW-WAIVER-CODE:** `PIC X(01)`: Waiver Code (1 character).
                *   **P-NEW-WAIVER-STATE:** `VALUE 'Y'`: Condition indicating waiver state.
            *   **P-NEW-INTER-NO:** `PIC 9(05)`: Intern Number (5 digits).
            *   **P-NEW-PROVIDER-TYPE:** `PIC X(02)`: Provider Type (2 characters).
            *   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)`: Current Census Division (1 digit).
            *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:**  Redefinition of the census division field.
            *   **P-NEW-MSA-DATA:**
                *   **P-NEW-CHG-CODE-INDEX:** `PIC X`: Charge Code Index (1 character).
                *   **P-NEW-GEO-LOC-MSAX:** `PIC X(04)`: Geographic Location MSA (4 characters).
                *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** Redefinition of the MSA location field (4 digits).
                *   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04)`: Wage Index Location MSA (4 characters).
                *   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04)`: Standard Amount Location MSA (4 characters).
                *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:** Redefinition of the standard amount MSA field.
                    *   **P-NEW-RURAL-1ST:**
                        *   **P-NEW-STAND-RURAL:** `PIC XX`: Standard Rural (2 characters).
                            *   **P-NEW-STD-RURAL-CHECK VALUE '  '**: Condition when standard rural is blank.
                        *   **P-NEW-RURAL-2ND:** `PIC XX`: Rural (2 characters).
            *   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX`:  Sole Community, Dependent Hospital Year (2 characters).
            *   **P-NEW-LUGAR:** `PIC X`: Lugar (1 character).
            *   **P-NEW-TEMP-RELIEF-IND:** `PIC X`: Temporary Relief Indicator (1 character).
            *   **P-NEW-FED-PPS-BLEND-IND:** `PIC X`: Federal PPS Blend Indicator (1 character).
            *   **FILLER:** `PIC X(05)`: Filler (5 characters).
        *   **PROV-NEWREC-HOLD2:**
            *   **P-NEW-VARIABLES:**
                *   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: Facility Specific Rate (5 integers, 2 decimals).
                *   **P-NEW-COLA:** `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment) (1 integer, 3 decimals).
                *   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)`: Intern Ratio (1 integer, 4 decimals).
                *   **P-NEW-BED-SIZE:** `PIC 9(05)`: Bed Size (5 digits).
                *   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio (1 integer, 3 decimals).
                *   **P-NEW-CMI:** `PIC 9(01)V9(04)`: CMI (Case Mix Index) (1 integer, 4 decimals).
                *   **P-NEW-SSI-RATIO:** `PIC V9(04)`: SSI Ratio (4 decimals).
                *   **P-NEW-MEDICAID-RATIO:** `PIC V9(04)`: Medicaid Ratio (4 decimals).
                *   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)`: PPS Blend Year Indicator (1 digit).
                *   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)`: Pruf Update Factor (1 integer, 5 decimals).
                *   **P-NEW-DSH-PERCENT:** `PIC V9(04)`: DSH (Disproportionate Share Hospital) Percent (4 decimals).
                *   **P-NEW-FYE-DATE:** `PIC X(08)`: Fiscal Year End Date (8 characters).
            *   **FILLER:** `PIC X(23)`: Filler (23 characters).
        *   **PROV-NEWREC-HOLD3:**
            *   **P-NEW-PASS-AMT-DATA:**
                *   **P-NEW-PASS-AMT-CAPITAL:** `PIC 9(04)V99`: Passed Amount - Capital (4 integers, 2 decimals).
                *   **P-NEW-PASS-AMT-DIR-MED-ED:** `PIC 9(04)V99`: Passed Amount - Direct Medical Education (4 integers, 2 decimals).
                *   **P-NEW-PASS-AMT-ORGAN-ACQ:** `PIC 9(04)V99`: Passed Amount - Organ Acquisition (4 integers, 2 decimals).
                *   **P-NEW-PASS-AMT-PLUS-MISC:** `PIC 9(04)V99`: Passed Amount - Plus Miscellaneous (4 integers, 2 decimals).
            *   **P-NEW-CAPI-DATA:**
                *   **P-NEW-CAPI-PPS-PAY-CODE:** `PIC X`: Capital PPS Payment Code (1 character).
                *   **P-NEW-CAPI-HOSP-SPEC-RATE:** `PIC 9(04)V99`: Capital Hospital Specific Rate (4 integers, 2 decimals).
                *   **P-NEW-CAPI-OLD-HARM-RATE:** `PIC 9(04)V99`: Capital Old Harm Rate (4 integers, 2 decimals).
                *   **P-NEW-CAPI-NEW-HARM-RATIO:** `PIC 9(01)V9999`: Capital New Harm Ratio (1 integer, 4 decimals).
                *   **P-NEW-CAPI-CSTCHG-RATIO:** `PIC 9V999`: Capital Cost to Charge Ratio (3 decimals).
                *   **P-NEW-CAPI-NEW-HOSP:** `PIC X`: Capital New Hospital (1 character).
                *   **P-NEW-CAPI-IME:** `PIC 9V9999`: Capital IME (Indirect Medical Education) (4 decimals).
                *   **P-NEW-CAPI-EXCEPTIONS:** `PIC 9(04)V99`: Capital Exceptions (4 integers, 2 decimals).
            *   **FILLER:** `PIC X(22)`: Filler (22 characters).
*   **WAGE-NEW-INDEX-RECORD:**
    *   This is the Wage Index record passed to the program.
        *   **W-MSA:** `PIC X(4)`: MSA Code (4 characters).
        *   **W-EFF-DATE:** `PIC X(8)`: Effective Date (8 characters).
        *   **W-WAGE-INDEX1:** `PIC S9(02)V9(04)`: Wage Index 1 (signed, 2 integers, 4 decimals).
        *   **W-WAGE-INDEX2:** `PIC S9(02)V9(04)`: Wage Index 2 (signed, 2 integers, 4 decimals).
        *   **W-WAGE-INDEX3:** `PIC S9(02)V9(04)`: Wage Index 3 (signed, 2 integers, 4 decimals).

## Analysis of LTCAL042

### File Access and Description

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field.  It appears to be a program identifier or a reference to the working storage.
    *   `VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C04.2'`: Stores the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS:**
    *   A group of fields used to store intermediate calculation results.
        *   **H-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **H-REG-DAYS:** `PIC 9(03)`: Regular Days (3 digits).
        *   **H-TOTAL-DAYS:** `PIC 9(05)`: Total Days (5 digits).
        *   **H-SSOT:** `PIC 9(02)`: Short Stay Outlier Threshold (2 digits).
        *   **H-BLEND-RTC:** `PIC 9(02)`: Blend Return Code (2 digits).
        *   **H-BLEND-FAC:** `PIC 9(01)V9(01)`: Blend Facility Rate (1 integer, 1 decimal).
        *   **H-BLEND-PPS:** `PIC 9(01)V9(01)`: Blend PPS Rate (1 integer, 1 decimal).
        *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)`: Short Stay Payment Amount (7 integers, 2 decimals).
        *   **H-SS-COST:** `PIC 9(07)V9(02)`: Short Stay Cost (7 integers, 2 decimals).
        *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)`: Labor Portion (7 integers, 6 decimals).
        *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)`: Non-Labor Portion (7 integers, 6 decimals).
        *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)`: Fixed Loss Amount (7 integers, 2 decimals).
        *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: New Facility Specific Rate (5 integers, 2 decimals).
        *   **H-LOS-RATIO:** `PIC 9(01)V9(05)`: Length of Stay Ratio (1 integer, 5 decimals).
*   **W-DRG-FILLS/W-DRG-TABLE:** (Defined via COPY LTDRG031)
    *   **W-DRG-FILLS:** A series of 44-character fields containing DRG data.
    *   **W-DRG-TABLE REDEFINES W-DRG-FILLS:**  Redefines the above structure to allow for indexed access.
        *   **WWM-ENTRY OCCURS 502 TIMES:**  Defines an array of 502 entries.
            *   **WWM-DRG:** `PIC X(3)`: The DRG code (3 characters).
            *   **WWM-RELWT:** `PIC 9(1)V9(4)`: Relative Weight (1 integer, 4 decimals).
            *   **WWM-ALOS:** `PIC 9(2)V9(1)`: Average Length of Stay (2 integers, 1 decimal).

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**
    *   This is the input data structure passed to the program.
        *   **B-NPI10:**
            *   **B-NPI8:** `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters.
            *   **B-NPI-FILLER:** `PIC X(02)`:  Filler for NPI (2 characters).
        *   **B-PROVIDER-NO:** `PIC X(06)`: Provider Number (6 characters).
        *   **B-PATIENT-STATUS:** `PIC X(02)`: Patient Status (2 characters).
        *   **B-DRG-CODE:** `PIC X(03)`: DRG Code (3 characters).
        *   **B-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **B-COV-DAYS:** `PIC 9(03)`: Covered Days (3 digits).
        *   **B-LTR-DAYS:** `PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   **B-DISCHARGE-DATE:**
            *   **B-DISCHG-CC:** `PIC 9(02)`: Discharge Date - Century/Score (2 digits).
            *   **B-DISCHG-YY:** `PIC 9(02)`: Discharge Date - Year (2 digits).
            *   **B-DISCHG-MM:** `PIC 9(02)`: Discharge Date - Month (2 digits).
            *   **B-DISCHG-DD:** `PIC 9(02)`: Discharge Date - Day (2 digits).
        *   **B-COV-CHARGES:** `PIC 9(07)V9(02)`: Covered Charges (7 integers, 2 decimals).
        *   **B-SPEC-PAY-IND:** `PIC X(01)`: Special Payment Indicator (1 character).
        *   **FILLER:** `PIC X(13)`: Filler (13 characters).
*   **PPS-DATA-ALL:**
    *   This is the output data structure passed back from the program.
        *   **PPS-RTC:** `PIC 9(02)`: Return Code (2 digits).
        *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)`: Charges Threshold (7 integers, 2 decimals).
        *   **PPS-DATA:**
            *   **PPS-MSA:** `PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)`: Wage Index (2 integers, 4 decimals).
            *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)`: Average Length of Stay (2 integers, 1 decimal).
            *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)`: Relative Weight (1 integer, 4 decimals).
            *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)`: Outlier Payment Amount (7 integers, 2 decimals).
            *   **PPS-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
            *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (7 integers, 2 decimals).
            *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)`: Federal Payment Amount (7 integers, 2 decimals).
            *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)`: Final Payment Amount (7 integers, 2 decimals).
            *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)`: Facility Costs (7 integers, 2 decimals).
            *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)`: New Facility Specific Rate (7 integers, 2 decimals).
            *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)`: Outlier Threshold (7 integers, 2 decimals).
            *   **PPS-SUBM-DRG-CODE:** `PIC X(03)`: Submitted DRG Code (3 characters).
            *   **PPS-CALC-VERS-CD:** `PIC X(05)`: Calculation Version Code (5 characters).
            *   **PPS-REG-DAYS-USED:** `PIC 9(03)`: Regular Days Used (3 digits).
            *   **PPS-LTR-DAYS-USED:** `PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   **PPS-BLEND-YEAR:** `PIC 9(01)`: Blend Year (1 digit).
            *   **PPS-COLA:** `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment) (1 integer, 3 decimals).
            *   **FILLER:** `PIC X(04)`: Filler (4 characters).
        *   **PPS-OTHER-DATA:**
            *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)`: National Labor Percentage (1 integer, 5 decimals).
            *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)`: National Non-Labor Percentage (1 integer, 5 decimals).
            *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)`: Standard Federal Rate (5 integers, 2 decimals).
            *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)`: Budget Neutrality Rate (1 integer, 3 decimals).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
        *   **PPS-PC-DATA:**
            *   **PPS-COT-IND:** `PIC X(01)`: Cost Outlier Indicator (1 character).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
*   **PRICER-OPT-VERS-SW:**
    *   Used to indicate whether all tables are passed or just the provider record.
        *   **PRICER-OPTION-SW:** `PIC X(01)`:  Switch for pricer options (1 character).
            *   **ALL-TABLES-PASSED:** `VALUE 'A'`:  Condition indicating all tables passed.
            *   **PROV-RECORD-PASSED:** `VALUE 'P'`: Condition indicating only provider record passed.
        *   **PPS-VERSIONS:**
            *   **PPDRV-VERSION:** `PIC X(05)`:  Version of the PPDRV program (5 characters).
*   **PROV-NEW-HOLD:**
    *   This is the Provider record passed to the program.
        *   **PROV-NEWREC-HOLD1:**
            *   **P-NEW-NPI10:**
                *   **P-NEW-NPI8:** `PIC X(08)`: New NPI (8 characters).
                *   **P-NEW-NPI-FILLER:** `PIC X(02)`: Filler for NPI (2 characters).
            *   **P-NEW-PROVIDER-NO:**
                *   **P-NEW-STATE:** `PIC 9(02)`: State Code (2 digits).
                *   **FILLER:** `PIC X(04)`: Filler (4 characters).
            *   **P-NEW-DATE-DATA:**
                *   **P-NEW-EFF-DATE:**
                    *   **P-NEW-EFF-DT-CC:** `PIC 9(02)`: Effective Date - Century/Score (2 digits).
                    *   **P-NEW-EFF-DT-YY:** `PIC 9(02)`: Effective Date - Year (2 digits).
                    *   **P-NEW-EFF-DT-MM:** `PIC 9(02)`: Effective Date - Month (2 digits).
                    *   **P-NEW-EFF-DT-DD:** `PIC 9(02)`: Effective Date - Day (2 digits).
                *   **P-NEW-FY-BEGIN-DATE:**
                    *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)`: Fiscal Year Begin Date - Century/Score (2 digits).
                    *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)`: Fiscal Year Begin