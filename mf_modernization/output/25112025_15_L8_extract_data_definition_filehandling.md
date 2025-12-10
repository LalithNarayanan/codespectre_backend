## Analysis of LTCAL032

### File Access and Description

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string. This is likely used for debugging or identification purposes.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C03.2'`: Initializes the field with the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS:**
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
        *   **H-LOS:** `PIC 9(03)`:  Length of Stay (3 digits).
        *   **H-REG-DAYS:** `PIC 9(03)`: Regular Days (3 digits).
        *   **H-TOTAL-DAYS:** `PIC 9(05)`: Total Days (5 digits).
        *   **H-SSOT:** `PIC 9(02)`: Short Stay Outlier Threshold (2 digits).
        *   **H-BLEND-RTC:** `PIC 9(02)`: Blend Return Code (2 digits).
        *   **H-BLEND-FAC:** `PIC 9(01)V9(01)`: Blend Facility Portion (2 digits, 1 decimal place).
        *   **H-BLEND-PPS:** `PIC 9(01)V9(01)`: Blend PPS Portion (2 digits, 1 decimal place).
        *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)`: Short Stay Payment Amount (9 digits, 2 decimal places).
        *   **H-SS-COST:** `PIC 9(07)V9(02)`: Short Stay Cost (9 digits, 2 decimal places).
        *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)`: Labor Portion of Payment (9 digits, 6 decimal places).
        *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)`: Non-Labor Portion of Payment (9 digits, 6 decimal places).
        *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)`: Fixed Loss Amount (9 digits, 2 decimal places).
        *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: New Facility Specific Rate (7 digits, 2 decimal places).
*   **W-DRG-FILLS:**
    *   This is a group item.
        *   It contains multiple `PIC X(44)` fields, each initialized with a long string of characters.  These strings likely encode the data that will be used in the DRG table, which is then defined using the REDEFINES clause.
*   **W-DRG-TABLE:**
    *   `REDEFINES W-DRG-FILLS`: This structure redefines the `W-DRG-FILLS` area.
        *   **WWM-ENTRY:** `OCCURS 502 TIMES`: This is an array (table) that can hold 502 entries.
            *   `ASCENDING KEY IS WWM-DRG`:  Indicates that the table is sorted by the `WWM-DRG` field.
            *   `INDEXED BY WWM-INDX`:  Allows the use of the `WWM-INDX` index for table access.
                *   **WWM-DRG:** `PIC X(3)`: DRG Code (3 characters).
                *   **WWM-RELWT:** `PIC 9(1)V9(4)`: Relative Weight (1 integer digit, 4 decimal places).
                *   **WWM-ALOS:** `PIC 9(2)V9(1)`: Average Length of Stay (2 integer digits, 1 decimal place).

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**
    *   This group item represents the input data passed to the program.
        *   **B-NPI10:**
            *   **B-NPI8:** `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters.
            *   **B-NPI-FILLER:** `PIC X(02)`: NPI filler - next 2 characters.
        *   **B-PROVIDER-NO:** `PIC X(06)`: Provider Number (6 characters).
        *   **B-PATIENT-STATUS:** `PIC X(02)`: Patient Status (2 characters).
        *   **B-DRG-CODE:** `PIC X(03)`: DRG Code (3 characters).
        *   **B-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **B-COV-DAYS:** `PIC 9(03)`: Covered Days (3 digits).
        *   **B-LTR-DAYS:** `PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   **B-DISCHARGE-DATE:**
            *   **B-DISCHG-CC:** `PIC 9(02)`: Discharge Century Code (2 digits).
            *   **B-DISCHG-YY:** `PIC 9(02)`: Discharge Year (2 digits).
            *   **B-DISCHG-MM:** `PIC 9(02)`: Discharge Month (2 digits).
            *   **B-DISCHG-DD:** `PIC 9(02)`: Discharge Day (2 digits).
        *   **B-COV-CHARGES:** `PIC 9(07)V9(02)`: Covered Charges (9 digits, 2 decimal places).
        *   **B-SPEC-PAY-IND:** `PIC X(01)`: Special Payment Indicator (1 character).
        *   **FILLER:** `PIC X(13)`: Filler (13 characters).
*   **PPS-DATA-ALL:**
    *   This group item represents the output data passed back from the program, containing the calculated payment information.
        *   **PPS-RTC:** `PIC 9(02)`: Return Code (2 digits).
        *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)`: Charge Threshold (9 digits, 2 decimal places).
        *   **PPS-DATA:**
            *   **PPS-MSA:** `PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)`: Wage Index (2 integer digits, 4 decimal places).
            *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)`: Average Length of Stay (2 integer digits, 1 decimal place).
            *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)`: Relative Weight (1 integer digit, 4 decimal places).
            *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)`: Outlier Payment Amount (9 digits, 2 decimal places).
            *   **PPS-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
            *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)`: Federal Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)`: Final Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)`: Facility Costs (9 digits, 2 decimal places).
            *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)`: New Facility Specific Rate (9 digits, 2 decimal places).
            *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)`: Outlier Threshold (9 digits, 2 decimal places).
            *   **PPS-SUBM-DRG-CODE:** `PIC X(03)`: Submitted DRG Code (3 characters).
            *   **PPS-CALC-VERS-CD:** `PIC X(05)`: Calculation Version Code (5 characters).
            *   **PPS-REG-DAYS-USED:** `PIC 9(03)`: Regular Days Used (3 digits).
            *   **PPS-LTR-DAYS-USED:** `PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   **PPS-BLEND-YEAR:** `PIC 9(01)`: Blend Year (1 digit).
            *   **PPS-COLA:** `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment) (1 integer digit, 3 decimal places).
            *   **FILLER:** `PIC X(04)`: Filler (4 characters).
        *   **PPS-OTHER-DATA:**
            *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)`: National Labor Percentage (1 integer digit, 5 decimal places).
            *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)`: National Non-Labor Percentage (1 integer digit, 5 decimal places).
            *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)`: Standard Federal Rate (7 digits, 2 decimal places).
            *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)`: Budget Neutrality Rate (1 integer digit, 3 decimal places).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
        *   **PPS-PC-DATA:**
            *   **PPS-COT-IND:** `PIC X(01)`: Cost Outlier Indicator (1 character).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
*   **PRICER-OPT-VERS-SW:**
    *   This group item likely contains flags to indicate which version of the pricer options to use.
        *   **PRICER-OPTION-SW:** `PIC X(01)`: Pricer Option Switch (1 character).
            *   **ALL-TABLES-PASSED:** `VALUE 'A'`: Condition name, value is 'A'.
            *   **PROV-RECORD-PASSED:** `VALUE 'P'`: Condition name, value is 'P'.
        *   **PPS-VERSIONS:**
            *   **PPDRV-VERSION:** `PIC X(05)`:  Version of the PPDRV module (5 characters).
*   **PROV-NEW-HOLD:**
    *   This group item represents the provider record data passed to the program.
        *   **PROV-NEWREC-HOLD1:**
            *   **P-NEW-NPI10:**
                *   **P-NEW-NPI8:** `PIC X(08)`: New NPI (8 characters).
                *   **P-NEW-NPI-FILLER:** `PIC X(02)`: NPI Filler (2 characters).
            *   **P-NEW-PROVIDER-NO:**
                *   **P-NEW-STATE:** `PIC 9(02)`: New State (2 digits).
                *   **FILLER:** `PIC X(04)`: Filler (4 characters).
            *   **P-NEW-DATE-DATA:**
                *   **P-NEW-EFF-DATE:**
                    *   **P-NEW-EFF-DT-CC:** `PIC 9(02)`: Effective Date Century Code (2 digits).
                    *   **P-NEW-EFF-DT-YY:** `PIC 9(02)`: Effective Date Year (2 digits).
                    *   **P-NEW-EFF-DT-MM:** `PIC 9(02)`: Effective Date Month (2 digits).
                    *   **P-NEW-EFF-DT-DD:** `PIC 9(02)`: Effective Date Day (2 digits).
                *   **P-NEW-FY-BEGIN-DATE:**
                    *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)`: Fiscal Year Begin Date Century Code (2 digits).
                    *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)`: Fiscal Year Begin Date Year (2 digits).
                    *   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)`: Fiscal Year Begin Date Month (2 digits).
                    *   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)`: Fiscal Year Begin Date Day (2 digits).
                *   **P-NEW-REPORT-DATE:**
                    *   **P-NEW-REPORT-DT-CC:** `PIC 9(02)`: Report Date Century Code (2 digits).
                    *   **P-NEW-REPORT-DT-YY:** `PIC 9(02)`: Report Date Year (2 digits).
                    *   **P-NEW-REPORT-DT-MM:** `PIC 9(02)`: Report Date Month (2 digits).
                    *   **P-NEW-REPORT-DT-DD:** `PIC 9(02)`: Report Date Day (2 digits).
                *   **P-NEW-TERMINATION-DATE:**
                    *   **P-NEW-TERM-DT-CC:** `PIC 9(02)`: Termination Date Century Code (2 digits).
                    *   **P-NEW-TERM-DT-YY:** `PIC 9(02)`: Termination Date Year (2 digits).
                    *   **P-NEW-TERM-DT-MM:** `PIC 9(02)`: Termination Date Month (2 digits).
                    *   **P-NEW-TERM-DT-DD:** `PIC 9(02)`: Termination Date Day (2 digits).
            *   **P-NEW-WAIVER-CODE:** `PIC X(01)`: Waiver Code (1 character).
                *   **P-NEW-WAIVER-STATE:** `VALUE 'Y'`: Condition name, value is 'Y'.
            *   **P-NEW-INTER-NO:** `PIC 9(05)`: New Internal Number (5 digits).
            *   **P-NEW-PROVIDER-TYPE:** `PIC X(02)`: New Provider Type (2 characters).
            *   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)`: Current Census Division (1 digit).
            *   **P-NEW-CURRENT-DIV:** `REDEFINES P-NEW-CURRENT-CENSUS-DIV`: Redefines the above field (1 digit).
            *   **P-NEW-MSA-DATA:**
                *   **P-NEW-CHG-CODE-INDEX:** `PIC X`: New Charge Code Index (1 character).
                *   **P-NEW-GEO-LOC-MSAX:** `PIC X(04) JUST RIGHT`: New Geo Location MSA (4 characters, right-justified).
                *   **P-NEW-GEO-LOC-MSA9:** `REDEFINES P-NEW-GEO-LOC-MSAX`: Redefines the above field as numeric (4 digits).
                *   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04) JUST RIGHT`: New Wage Index Location MSA (4 characters, right-justified).
                *   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04) JUST RIGHT`: New Standard Amount Location MSA (4 characters, right-justified).
                *   **P-NEW-STAND-AMT-LOC-MSA9:** `REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Redefines the above field.
                    *   **P-NEW-RURAL-1ST:**
                        *   **P-NEW-STAND-RURAL:** `PIC XX`: Rural Standard (2 characters).
                            *   **P-NEW-STD-RURAL-CHECK:** `VALUE '  '`: Condition name, value is two spaces.
                    *   **P-NEW-RURAL-2ND:** `PIC XX`: Rural Standard (2 characters).
            *   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX`: New Sole Community Hospital Year (2 characters).
            *   **P-NEW-LUGAR:** `PIC X`: New Lugar (1 character).
            *   **P-NEW-TEMP-RELIEF-IND:** `PIC X`: New Temporary Relief Indicator (1 character).
            *   **P-NEW-FED-PPS-BLEND-IND:** `PIC X`: New Federal PPS Blend Indicator (1 character).
            *   **FILLER:** `PIC X(05)`: Filler (5 characters).
        *   **PROV-NEWREC-HOLD2:**
            *   **P-NEW-VARIABLES:**
                *   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: New Facility Specific Rate (7 digits, 2 decimal places).
                *   **P-NEW-COLA:** `PIC 9(01)V9(03)`: New COLA (Cost of Living Adjustment) (1 integer digit, 3 decimal places).
                *   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)`: New Intern Ratio (1 integer digit, 4 decimal places).
                *   **P-NEW-BED-SIZE:** `PIC 9(05)`: New Bed Size (5 digits).
                *   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)`: New Operating Cost to Charge Ratio (1 integer digit, 3 decimal places).
                *   **P-NEW-CMI:** `PIC 9(01)V9(04)`: New CMI (Case Mix Index) (1 integer digit, 4 decimal places).
                *   **P-NEW-SSI-RATIO:** `PIC V9(04)`: New SSI Ratio (4 decimal places).
                *   **P-NEW-MEDICAID-RATIO:** `PIC V9(04)`: New Medicaid Ratio (4 decimal places).
                *   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)`: New PPS Blend Year Indicator (1 digit).
                *   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)`: New Pruf Update Factor (1 integer digit, 5 decimal places).
                *   **P-NEW-DSH-PERCENT:** `PIC V9(04)`: New DSH (Disproportionate Share Hospital) Percentage (4 decimal places).
                *   **P-NEW-FYE-DATE:** `PIC X(08)`: New Fiscal Year End Date (8 characters).
            *   **FILLER:** `PIC X(23)`: Filler (23 characters).
        *   **PROV-NEWREC-HOLD3:**
            *   **P-NEW-PASS-AMT-DATA:**
                *   **P-NEW-PASS-AMT-CAPITAL:** `PIC 9(04)V99`: New Pass Through Amount - Capital (6 digits, 2 decimal places).
                *   **P-NEW-PASS-AMT-DIR-MED-ED:** `PIC 9(04)V99`: New Pass Through Amount - Direct Medical Education (6 digits, 2 decimal places).
                *   **P-NEW-PASS-AMT-ORGAN-ACQ:** `PIC 9(04)V99`: New Pass Through Amount - Organ Acquisition (6 digits, 2 decimal places).
                *   **P-NEW-PASS-AMT-PLUS-MISC:** `PIC 9(04)V99`: New Pass Through Amount - Plus Miscellaneous (6 digits, 2 decimal places).
            *   **P-NEW-CAPI-DATA:**
                *   **P-NEW-CAPI-PPS-PAY-CODE:** `PIC X`: New Capital PPS Payment Code (1 character).
                *   **P-NEW-CAPI-HOSP-SPEC-RATE:** `PIC 9(04)V99`: New Capital Hospital Specific Rate (6 digits, 2 decimal places).
                *   **P-NEW-CAPI-OLD-HARM-RATE:** `PIC 9(04)V99`: New Capital Old Harm Rate (6 digits, 2 decimal places).
                *   **P-NEW-CAPI-NEW-HARM-RATIO:** `PIC 9(01)V9999`: New Capital New Harm Ratio (1 integer digit, 4 decimal places).
                *   **P-NEW-CAPI-CSTCHG-RATIO:** `PIC 9V999`: New Capital Cost to Charge Ratio (4 decimal places).
                *   **P-NEW-CAPI-NEW-HOSP:** `PIC X`: New Capital New Hospital (1 character).
                *   **P-NEW-CAPI-IME:** `PIC 9V9999`: New Capital IME (Indirect Medical Education) (4 decimal places).
                *   **P-NEW-CAPI-EXCEPTIONS:** `PIC 9(04)V99`: New Capital Exceptions (6 digits, 2 decimal places).
            *   **FILLER:** `PIC X(22)`: Filler (22 characters).
*   **WAGE-NEW-INDEX-RECORD:**
    *   This group item contains wage index data passed to the program.
        *   **W-MSA:** `PIC X(4)`: MSA Code (4 characters).
        *   **W-EFF-DATE:** `PIC X(8)`: Effective Date (8 characters).
        *   **W-WAGE-INDEX1:** `PIC S9(02)V9(04)`: Wage Index 1 (Signed, 2 integer digits, 4 decimal places).
        *   **W-WAGE-INDEX2:** `PIC S9(02)V9(04)`: Wage Index 2 (Signed, 2 integer digits, 4 decimal places).
        *   **W-WAGE-INDEX3:** `PIC S9(02)V9(04)`: Wage Index 3 (Signed, 2 integer digits, 4 decimal places).

## Analysis of LTCAL042

### File Access and Description

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string. This is likely used for debugging or identification purposes.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C04.2'`: Initializes the field with the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS:**
    *   This is a group item containing several numeric fields used to store intermediate calculation results.
        *   **H-LOS:** `PIC 9(03)`:  Length of Stay (3 digits).
        *   **H-REG-DAYS:** `PIC 9(03)`: Regular Days (3 digits).
        *   **H-TOTAL-DAYS:** `PIC 9(05)`: Total Days (5 digits).
        *   **H-SSOT:** `PIC 9(02)`: Short Stay Outlier Threshold (2 digits).
        *   **H-BLEND-RTC:** `PIC 9(02)`: Blend Return Code (2 digits).
        *   **H-BLEND-FAC:** `PIC 9(01)V9(01)`: Blend Facility Portion (2 digits, 1 decimal place).
        *   **H-BLEND-PPS:** `PIC 9(01)V9(01)`: Blend PPS Portion (2 digits, 1 decimal place).
        *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)`: Short Stay Payment Amount (9 digits, 2 decimal places).
        *   **H-SS-COST:** `PIC 9(07)V9(02)`: Short Stay Cost (9 digits, 2 decimal places).
        *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)`: Labor Portion of Payment (9 digits, 6 decimal places).
        *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)`: Non-Labor Portion of Payment (9 digits, 6 decimal places).
        *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)`: Fixed Loss Amount (9 digits, 2 decimal places).
        *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)`: New Facility Specific Rate (7 digits, 2 decimal places).
        *   **H-LOS-RATIO:** `PIC 9(01)V9(05)`: Length of Stay Ratio (1 integer digit, 5 decimal places).
*   **W-DRG-FILLS:**
    *   This is a group item.
        *   It contains multiple `PIC X(44)` fields, each initialized with a long string of characters.  These strings likely encode the data that will be used in the DRG table, which is then defined using the REDEFINES clause.
*   **W-DRG-TABLE:**
    *   `REDEFINES W-DRG-FILLS`: This structure redefines the `W-DRG-FILLS` area.
        *   **WWM-ENTRY:** `OCCURS 502 TIMES`: This is an array (table) that can hold 502 entries.
            *   `ASCENDING KEY IS WWM-DRG`:  Indicates that the table is sorted by the `WWM-DRG` field.
            *   `INDEXED BY WWM-INDX`:  Allows the use of the `WWM-INDX` index for table access.
                *   **WWM-DRG:** `PIC X(3)`: DRG Code (3 characters).
                *   **WWM-RELWT:** `PIC 9(1)V9(4)`: Relative Weight (1 integer digit, 4 decimal places).
                *   **WWM-ALOS:** `PIC 9(2)V9(1)`: Average Length of Stay (2 integer digits, 1 decimal place).

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**
    *   This group item represents the input data passed to the program.
        *   **B-NPI10:**
            *   **B-NPI8:** `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters.
            *   **B-NPI-FILLER:** `PIC X(02)`: NPI filler - next 2 characters.
        *   **B-PROVIDER-NO:** `PIC X(06)`: Provider Number (6 characters).
        *   **B-PATIENT-STATUS:** `PIC X(02)`: Patient Status (2 characters).
        *   **B-DRG-CODE:** `PIC X(03)`: DRG Code (3 characters).
        *   **B-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
        *   **B-COV-DAYS:** `PIC 9(03)`: Covered Days (3 digits).
        *   **B-LTR-DAYS:** `PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   **B-DISCHARGE-DATE:**
            *   **B-DISCHG-CC:** `PIC 9(02)`: Discharge Century Code (2 digits).
            *   **B-DISCHG-YY:** `PIC 9(02)`: Discharge Year (2 digits).
            *   **B-DISCHG-MM:** `PIC 9(02)`: Discharge Month (2 digits).
            *   **B-DISCHG-DD:** `PIC 9(02)`: Discharge Day (2 digits).
        *   **B-COV-CHARGES:** `PIC 9(07)V9(02)`: Covered Charges (9 digits, 2 decimal places).
        *   **B-SPEC-PAY-IND:** `PIC X(01)`: Special Payment Indicator (1 character).
        *   **FILLER:** `PIC X(13)`: Filler (13 characters).
*   **PPS-DATA-ALL:**
    *   This group item represents the output data passed back from the program, containing the calculated payment information.
        *   **PPS-RTC:** `PIC 9(02)`: Return Code (2 digits).
        *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)`: Charge Threshold (9 digits, 2 decimal places).
        *   **PPS-DATA:**
            *   **PPS-MSA:** `PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)`: Wage Index (2 integer digits, 4 decimal places).
            *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)`: Average Length of Stay (2 integer digits, 1 decimal place).
            *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)`: Relative Weight (1 integer digit, 4 decimal places).
            *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)`: Outlier Payment Amount (9 digits, 2 decimal places).
            *   **PPS-LOS:** `PIC 9(03)`: Length of Stay (3 digits).
            *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)`: Federal Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)`: Final Payment Amount (9 digits, 2 decimal places).
            *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)`: Facility Costs (9 digits, 2 decimal places).
            *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)`: New Facility Specific Rate (9 digits, 2 decimal places).
            *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)`: Outlier Threshold (9 digits, 2 decimal places).
            *   **PPS-SUBM-DRG-CODE:** `PIC X(03)`: Submitted DRG Code (3 characters).
            *   **PPS-CALC-VERS-CD:** `PIC X(05)`: Calculation Version Code (5 characters).
            *   **PPS-REG-DAYS-USED:** `PIC 9(03)`: Regular Days Used (3 digits).
            *   **PPS-LTR-DAYS-USED:** `PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   **PPS-BLEND-YEAR:** `PIC 9(01)`: Blend Year (1 digit).
            *   **PPS-COLA:** `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment) (1 integer digit, 3 decimal places).
            *   **FILLER:** `PIC X(04)`: Filler (4 characters).
        *   **PPS-OTHER-DATA:**
            *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)`: National Labor Percentage (1 integer digit, 5 decimal places).
            *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)`: National Non-Labor Percentage (1 integer digit, 5 decimal places).
            *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)`: Standard Federal Rate (7 digits, 2 decimal places).
            *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)`: Budget Neutrality Rate (1 integer digit, 3 decimal places).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
        *   **PPS-PC-DATA:**
            *   **PPS-COT-IND:** `PIC X(01)`: Cost Outlier Indicator (1 character).
            *   **FILLER:** `PIC X(20)`: Filler (20 characters).
*   **PRICER-OPT-VERS-SW:**
    *   This group item likely contains flags to indicate which version of the pricer options to use.
        *   **PRICER-OPTION-SW:** `PIC X(01)`: Pricer Option Switch (1 character).
            *   **ALL-TABLES-PASSED:** `VALUE 'A'`: Condition name, value is 'A'.
            *   **PROV-RECORD-PASSED:** `VALUE 'P'`: Condition name, value is 'P'.
        *   **PPS-VERSIONS:**
            *   **PPDRV-VERSION:** `PIC X(05)`:  Version of the PPDRV module (5 characters).
*   **PROV-NEW-HOLD:**
    *   This group item represents the provider record data passed to the program.
        *   **PROV-NEWREC-HOLD1:**
            *