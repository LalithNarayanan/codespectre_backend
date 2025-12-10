## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and their descriptions.

### Program: LTCAL032

#### Files Accessed:

*   **COPY LTDRG031:**  This indicates the inclusion of a copybook named "LTDRG031".  This copybook likely contains data structures related to DRG (Diagnosis Related Group) information, such as DRG codes, relative weights, and average lengths of stay.  The exact nature of the data depends on the content of the copybook itself.

#### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF:**
    *   `PIC X(46)` - Alphanumeric field, 46 characters long.
    *   `VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'` -  Contains a literal string identifying the program and the storage section.
*   **CAL-VERSION:**
    *   `PIC X(05)` - Alphanumeric field, 5 characters long.
    *   `VALUE 'C03.2'` - Contains the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS:** (Defined via COPY LTDRG031) - This structure holds various components used in the Prospective Payment System (PPS) calculations.  The specific fields are defined within the `LTDRG031` copybook, and are described below:
    *   **H-LOS:** `PIC 9(03)` - Numeric field, 3 digits, representing Length of Stay.
    *   **H-REG-DAYS:** `PIC 9(03)` - Numeric field, 3 digits, representing Regular Days.
    *   **H-TOTAL-DAYS:** `PIC 9(05)` - Numeric field, 5 digits, representing Total Days.
    *   **H-SSOT:** `PIC 9(02)` - Numeric field, 2 digits, Short Stay Outlier Threshold.
    *   **H-BLEND-RTC:** `PIC 9(02)` - Numeric field, 2 digits, Blend Return Code.
    *   **H-BLEND-FAC:** `PIC 9(01)V9(01)` - Numeric field, 2 digits (1 integer, 1 decimal), Facility Blend Percentage.
    *   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - Numeric field, 2 digits (1 integer, 1 decimal), PPS Blend Percentage.
    *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Short Stay Payment Amount.
    *   **H-SS-COST:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Short Stay Cost.
    *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)` - Numeric field, 13 digits (7 integer, 6 decimal), Labor Portion.
    *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Numeric field, 13 digits (7 integer, 6 decimal), Non-Labor Portion.
    *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - Numeric field, 7 digits (5 integer, 2 decimal), New Facility Specific Rate.

#### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA:** This structure is passed *into* the program, likely from a calling program, and contains the billing information.
    *   **B-NPI10:**
        *   **B-NPI8:** `PIC X(08)` - Alphanumeric field, 8 characters, National Provider Identifier (NPI) - first part.
        *   **B-NPI-FILLER:** `PIC X(02)` - Alphanumeric field, 2 characters, NPI - Filler.
    *   **B-PROVIDER-NO:** `PIC X(06)` - Alphanumeric field, 6 characters, Provider Number.
    *   **B-PATIENT-STATUS:** `PIC X(02)` - Alphanumeric field, 2 characters, Patient Status.
    *   **B-DRG-CODE:** `PIC X(03)` - Alphanumeric field, 3 characters, DRG Code.
    *   **B-LOS:** `PIC 9(03)` - Numeric field, 3 digits, Length of Stay.
    *   **B-COV-DAYS:** `PIC 9(03)` - Numeric field, 3 digits, Covered Days.
    *   **B-LTR-DAYS:** `PIC 9(02)` - Numeric field, 2 digits, Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Century/Control Code.
        *   **B-DISCHG-YY:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Year.
        *   **B-DISCHG-MM:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Month.
        *   **B-DISCHG-DD:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Day.
    *   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Covered Charges.
    *   **B-SPEC-PAY-IND:** `PIC X(01)` - Alphanumeric field, 1 character, Special Payment Indicator.
    *   **FILLER:** `PIC X(13)` - Alphanumeric field, 13 characters, Unused/Filler.
*   **PPS-DATA-ALL:** This structure is passed *back* from the program to the calling program, and contains the calculated PPS data.
    *   **PPS-RTC:** `PIC 9(02)` - Numeric field, 2 digits, PPS Return Code.
    *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Charge Threshold.
    *   **PPS-DATA:**
        *   **PPS-MSA:** `PIC X(04)` - Alphanumeric field, 4 characters, MSA (Metropolitan Statistical Area) Code.
        *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Numeric field, 6 digits (2 integer, 4 decimal), PPS Wage Index.
        *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Numeric field, 3 digits (2 integer, 1 decimal), PPS Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Numeric field, 5 digits (1 integer, 4 decimal), PPS Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Outlier Payment Amount.
        *   **PPS-LOS:** `PIC 9(03)` - Numeric field, 3 digits, Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Final Payment Amount.
        *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Alphanumeric field, 3 characters, Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** `PIC X(05)` - Alphanumeric field, 5 characters, Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Numeric field, 3 digits, Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Numeric field, 3 digits, Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** `PIC 9(01)` - Numeric field, 1 digit, Blend Year.
        *   **PPS-COLA:** `PIC 9(01)V9(03)` - Numeric field, 4 digits (1 integer, 3 decimal), COLA (Cost of Living Adjustment).
        *   **FILLER:** `PIC X(04)` - Alphanumeric field, 4 characters, Unused/Filler.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)` - Numeric field, 6 digits (1 integer, 5 decimal), National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)` - Numeric field, 6 digits (1 integer, 5 decimal), National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)` - Numeric field, 7 digits (5 integer, 2 decimal), Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)` - Numeric field, 4 digits (1 integer, 3 decimal), Budget Neutrality Rate.
        *   **FILLER:** `PIC X(20)` - Alphanumeric field, 20 characters, Unused/Filler.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** `PIC X(01)` - Alphanumeric field, 1 character, Cost Outlier Indicator.
        *   **FILLER:** `PIC X(20)` - Alphanumeric field, 20 characters, Unused/Filler.
*   **PRICER-OPT-VERS-SW:**  This structure is passed *into* the program, likely indicating the options selected for the pricing.
    *   **PRICER-OPTION-SW:** `PIC X(01)` - Alphanumeric field, 1 character, Pricer Option Switch.
        *   **ALL-TABLES-PASSED:** `VALUE 'A'` - Condition:  Indicates all tables are passed.
        *   **PROV-RECORD-PASSED:** `VALUE 'P'` - Condition:  Indicates provider record is passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** `PIC X(05)` - Alphanumeric field, 5 characters, Version of the PPDRV program.
*   **PROV-NEW-HOLD:**  This structure is passed *into* the program, and contains provider-specific information.
    *   **PROV-NEWREC-HOLD1:**  Contains provider record data.
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** `PIC X(08)` - Alphanumeric field, 8 characters, NPI - first part.
            *   **P-NEW-NPI-FILLER:** `PIC X(02)` - Alphanumeric field, 2 characters, NPI - Filler.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** `PIC 9(02)` - Numeric field, 2 digits, Provider State.
            *   **FILLER:** `PIC X(04)` - Alphanumeric field, 4 characters, Unused/Filler.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:** `PIC 9(02)` - Numeric field, 2 digits, Effective Date - Century/Control Code.
                *   **P-NEW-EFF-DT-YY:** `PIC 9(02)` - Numeric field, 2 digits, Effective Date - Year.
                *   **P-NEW-EFF-DT-MM:** `PIC 9(02)` - Numeric field, 2 digits, Effective Date - Month.
                *   **P-NEW-EFF-DT-DD:** `PIC 9(02)` - Numeric field, 2 digits, Effective Date - Day.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)` - Numeric field, 2 digits, Fiscal Year Begin Date - Century/Control Code.
                *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)` - Numeric field, 2 digits, Fiscal Year Begin Date - Year.
                *   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)` - Numeric field, 2 digits, Fiscal Year Begin Date - Month.
                *   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)` - Numeric field, 2 digits, Fiscal Year Begin Date - Day.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:** `PIC 9(02)` - Numeric field, 2 digits, Report Date - Century/Control Code.
                *   **P-NEW-REPORT-DT-YY:** `PIC 9(02)` - Numeric field, 2 digits, Report Date - Year.
                *   **P-NEW-REPORT-DT-MM:** `PIC 9(02)` - Numeric field, 2 digits, Report Date - Month.
                *   **P-NEW-REPORT-DT-DD:** `PIC 9(02)` - Numeric field, 2 digits, Report Date - Day.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:** `PIC 9(02)` - Numeric field, 2 digits, Termination Date - Century/Control Code.
                *   **P-NEW-TERM-DT-YY:** `PIC 9(02)` - Numeric field, 2 digits, Termination Date - Year.
                *   **P-NEW-TERM-DT-MM:** `PIC 9(02)` - Numeric field, 2 digits, Termination Date - Month.
                *   **P-NEW-TERM-DT-DD:** `PIC 9(02)` - Numeric field, 2 digits, Termination Date - Day.
        *   **P-NEW-WAIVER-CODE:** `PIC X(01)` - Alphanumeric field, 1 character, Waiver Code.
            *   **P-NEW-WAIVER-STATE:** `VALUE 'Y'` - Condition: Indicates if a waiver state is applicable.
        *   **P-NEW-INTER-NO:** `PIC 9(05)` - Numeric field, 5 digits, Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** `PIC X(02)` - Alphanumeric field, 2 characters, Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Numeric field, 1 digit, Current Census Division.
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Numeric field, 1 digit, Current Division (Redefines the above).
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** `PIC X` - Alphanumeric field, 1 character, Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** `PIC X(04) JUST RIGHT` - Alphanumeric field, 4 characters, Geo Location MSA (Metropolitan Statistical Area) - Right Justified.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** `PIC 9(04)` - Numeric field, 4 digits, Geo Location MSA (Redefines the above).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04) JUST RIGHT` - Alphanumeric field, 4 characters, Wage Index Location MSA - Right Justified.
            *   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04) JUST RIGHT` - Alphanumeric field, 4 characters, Standard Amount Location MSA - Right Justified.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** `PIC XX` - Alphanumeric field, 2 characters, Standard Rural Indicator.
                        *   **P-NEW-STD-RURAL-CHECK:** `VALUE '  '` - Condition: Check for Standard Rural.
                *   **P-NEW-RURAL-2ND:** `PIC XX` - Alphanumeric field, 2 characters, Rural Indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX` - Alphanumeric field, 2 characters, Sole Community/Dependent Hospital Year.
        *   **P-NEW-LUGAR:** `PIC X` - Alphanumeric field, 1 character, Lugar.
        *   **P-NEW-TEMP-RELIEF-IND:** `PIC X` - Alphanumeric field, 1 character, Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** `PIC X` - Alphanumeric field, 1 character, Federal PPS Blend Indicator.
        *   **FILLER:** `PIC X(05)` - Alphanumeric field, 5 characters, Unused/Filler.
    *   **PROV-NEWREC-HOLD2:**  More provider record data.
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - Numeric field, 7 digits (5 integer, 2 decimal), Facility Specific Rate.
            *   **P-NEW-COLA:** `PIC 9(01)V9(03)` - Numeric field, 4 digits (1 integer, 3 decimal), COLA (Cost of Living Adjustment).
            *   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)` - Numeric field, 5 digits (1 integer, 4 decimal), Intern Ratio.
            *   **P-NEW-BED-SIZE:** `PIC 9(05)` - Numeric field, 5 digits, Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)` - Numeric field, 4 digits (1 integer, 3 decimal), Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** `PIC 9(01)V9(04)` - Numeric field, 5 digits (1 integer, 4 decimal), CMI (Case Mix Index).
            *   **P-NEW-SSI-RATIO:** `PIC V9(04)` - Numeric field, 4 digits (0 integer, 4 decimal), SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO:** `PIC V9(04)` - Numeric field, 4 digits (0 integer, 4 decimal), Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)` - Numeric field, 1 digit, PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)` - Numeric field, 6 digits (1 integer, 5 decimal), Pruf Update Factor.
            *   **P-NEW-DSH-PERCENT:** `PIC V9(04)` - Numeric field, 4 digits (0 integer, 4 decimal), DSH (Disproportionate Share Hospital) Percentage.
            *   **P-NEW-FYE-DATE:** `PIC X(08)` - Alphanumeric field, 8 characters, Fiscal Year End Date.
        *   **FILLER:** `PIC X(23)` - Alphanumeric field, 23 characters, Unused/Filler.
    *   **PROV-NEWREC-HOLD3:**  More provider record data.
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Passed Amount - Capital.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Passed Amount - Direct Medical Education.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Passed Amount - Organ Acquisition.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Passed Amount - Plus Miscellaneous.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** `PIC X` - Alphanumeric field, 1 character, Capital PPS Payment Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Capital Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Capital Old Harm Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** `PIC 9(01)V9999` - Numeric field, 5 digits (1 integer, 4 decimal), Capital New Harm Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** `PIC 9V999` - Numeric field, 4 digits (0 integer, 3 decimal), Capital Cost to Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** `PIC X` - Alphanumeric field, 1 character, Capital New Hospital Indicator.
            *   **P-NEW-CAPI-IME:** `PIC 9V9999` - Numeric field, 5 digits (0 integer, 4 decimal), Capital IME (Indirect Medical Education).
            *   **P-NEW-CAPI-EXCEPTIONS:** `PIC 9(04)V99` - Numeric field, 6 digits (4 integer, 2 decimal), Capital Exceptions.
        *   **FILLER:** `PIC X(22)` - Alphanumeric field, 22 characters, Unused/Filler.
*   **WAGE-NEW-INDEX-RECORD:**  This structure is passed *into* the program and contains wage index information.
    *   **W-MSA:** `PIC X(4)` - Alphanumeric field, 4 characters, MSA (Metropolitan Statistical Area) Code.
    *   **W-EFF-DATE:** `PIC X(8)` - Alphanumeric field, 8 characters, Effective Date.
    *   **W-WAGE-INDEX1:** `PIC S9(02)V9(04)` - Signed numeric field, 6 digits (2 integer, 4 decimal), Wage Index 1.
    *   **W-WAGE-INDEX2:** `PIC S9(02)V9(04)` - Signed numeric field, 6 digits (2 integer, 4 decimal), Wage Index 2.
    *   **W-WAGE-INDEX3:** `PIC S9(02)V9(04)` - Signed numeric field, 6 digits (2 integer, 4 decimal), Wage Index 3.

### Program: LTCAL042

#### Files Accessed:

*   **COPY LTDRG031:** This indicates the inclusion of a copybook named "LTDRG031".  This copybook likely contains data structures related to DRG (Diagnosis Related Group) information.

#### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF:**
    *   `PIC X(46)` - Alphanumeric field, 46 characters long.
    *   `VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'` -  Contains a literal string identifying the program and the storage section.
*   **CAL-VERSION:**
    *   `PIC X(05)` - Alphanumeric field, 5 characters long.
    *   `VALUE 'C04.2'` - Contains the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS:** (Defined via COPY LTDRG031) - Same as in LTCAL032. This structure holds various components used in the Prospective Payment System (PPS) calculations.  The specific fields are defined within the `LTDRG031` copybook, and are described below:
    *   **H-LOS:** `PIC 9(03)` - Numeric field, 3 digits, representing Length of Stay.
    *   **H-REG-DAYS:** `PIC 9(03)` - Numeric field, 3 digits, representing Regular Days.
    *   **H-TOTAL-DAYS:** `PIC 9(05)` - Numeric field, 5 digits, representing Total Days.
    *   **H-SSOT:** `PIC 9(02)` - Numeric field, 2 digits, Short Stay Outlier Threshold.
    *   **H-BLEND-RTC:** `PIC 9(02)` - Numeric field, 2 digits, Blend Return Code.
    *   **H-BLEND-FAC:** `PIC 9(01)V9(01)` - Numeric field, 2 digits (1 integer, 1 decimal), Facility Blend Percentage.
    *   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - Numeric field, 2 digits (1 integer, 1 decimal), PPS Blend Percentage.
    *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Short Stay Payment Amount.
    *   **H-SS-COST:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Short Stay Cost.
    *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)` - Numeric field, 13 digits (7 integer, 6 decimal), Labor Portion.
    *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Numeric field, 13 digits (7 integer, 6 decimal), Non-Labor Portion.
    *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - Numeric field, 7 digits (5 integer, 2 decimal), New Facility Specific Rate.
    *   **H-LOS-RATIO:** `PIC 9(01)V9(05)` - Numeric field, 6 digits (1 integer, 5 decimal), Length of Stay Ratio.

#### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA:**  This structure is passed *into* the program, likely from a calling program, and contains the billing information.  Same structure as in LTCAL032.
    *   **B-NPI10:**
        *   **B-NPI8:** `PIC X(08)` - Alphanumeric field, 8 characters, National Provider Identifier (NPI) - first part.
        *   **B-NPI-FILLER:** `PIC X(02)` - Alphanumeric field, 2 characters, NPI - Filler.
    *   **B-PROVIDER-NO:** `PIC X(06)` - Alphanumeric field, 6 characters, Provider Number.
    *   **B-PATIENT-STATUS:** `PIC X(02)` - Alphanumeric field, 2 characters, Patient Status.
    *   **B-DRG-CODE:** `PIC X(03)` - Alphanumeric field, 3 characters, DRG Code.
    *   **B-LOS:** `PIC 9(03)` - Numeric field, 3 digits, Length of Stay.
    *   **B-COV-DAYS:** `PIC 9(03)` - Numeric field, 3 digits, Covered Days.
    *   **B-LTR-DAYS:** `PIC 9(02)` - Numeric field, 2 digits, Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Century/Control Code.
        *   **B-DISCHG-YY:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Year.
        *   **B-DISCHG-MM:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Month.
        *   **B-DISCHG-DD:** `PIC 9(02)` - Numeric field, 2 digits, Discharge Date - Day.
    *   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), Covered Charges.
    *   **B-SPEC-PAY-IND:** `PIC X(01)` - Alphanumeric field, 1 character, Special Payment Indicator.
    *   **FILLER:** `PIC X(13)` - Alphanumeric field, 13 characters, Unused/Filler.
*   **PPS-DATA-ALL:** This structure is passed *back* from the program to the calling program, and contains the calculated PPS data. Same structure as in LTCAL032.
    *   **PPS-RTC:** `PIC 9(02)` - Numeric field, 2 digits, PPS Return Code.
    *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Charge Threshold.
    *   **PPS-DATA:**
        *   **PPS-MSA:** `PIC X(04)` - Alphanumeric field, 4 characters, MSA (Metropolitan Statistical Area) Code.
        *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Numeric field, 6 digits (2 integer, 4 decimal), PPS Wage Index.
        *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Numeric field, 3 digits (2 integer, 1 decimal), PPS Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Numeric field, 5 digits (1 integer, 4 decimal), PPS Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Outlier Payment Amount.
        *   **PPS-LOS:** `PIC 9(03)` - Numeric field, 3 digits, Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Final Payment Amount.
        *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Numeric field, 9 digits (7 integer, 2 decimal), PPS Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Alphanumeric field, 3 characters, Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** `PIC X(05)` - Alphanumeric field, 5 characters, Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Numeric field, 3 digits, Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Numeric field, 3 digits, Lifetime Reserve Days Used