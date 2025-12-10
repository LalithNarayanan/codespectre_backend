## Analysis of LTCAL032

### Files Accessed

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL032 - W O R K I N G S T O R A G E'`:  Initialized with a descriptive string, likely for debugging or identification.

*   **`CAL-VERSION`**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C03.2'`: Initialized with a version identifier, indicating the version of the calculation logic.

*   **`HOLD-PPS-COMPONENTS`**:
    *   This group of data elements stores intermediate calculation results and components used in the PPS (Prospective Payment System) calculation.
    *   `05 H-LOS PIC 9(03)`: Length of Stay (LOS),  3-digit numeric.
    *   `05 H-REG-DAYS PIC 9(03)`: Regular Days, 3-digit numeric.
    *   `05 H-TOTAL-DAYS PIC 9(05)`: Total Days, 5-digit numeric.
    *   `05 H-SSOT PIC 9(02)`: Short Stay Outlier Threshold, 2-digit numeric.
    *   `05 H-BLEND-RTC PIC 9(02)`: Blend Return Code, 2-digit numeric.
    *   `05 H-BLEND-FAC PIC 9(01)V9(01)`: Blend Facility Portion, 2-digit numeric (1 integer, 1 decimal).
    *   `05 H-BLEND-PPS PIC 9(01)V9(01)`: Blend PPS Portion, 2-digit numeric (1 integer, 1 decimal).
    *   `05 H-SS-PAY-AMT PIC 9(07)V9(02)`: Short Stay Payment Amount, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-SS-COST PIC 9(07)V9(02)`: Short Stay Cost, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-LABOR-PORTION PIC 9(07)V9(06)`: Labor Portion, 13-digit numeric (7 integer, 6 decimal).
    *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06)`: Non-Labor Portion, 13-digit numeric (7 integer, 6 decimal).
    *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02)`: Fixed Loss Amount, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: New Facility Specific Rate, 7-digit numeric (5 integer, 2 decimal).

### Data Structures in LINKAGE SECTION

*   **`BILL-NEW-DATA`**:
    *   This structure receives billing information from the calling program.
    *   `10 B-NPI10`:  NPI (National Provider Identifier)
        *   `15 B-NPI8 PIC X(08)`:  NPI, 8-character alphanumeric.
        *   `15 B-NPI-FILLER PIC X(02)`: Filler, 2-character alphanumeric.
    *   `10 B-PROVIDER-NO PIC X(06)`: Provider Number, 6-character alphanumeric.
    *   `10 B-PATIENT-STATUS PIC X(02)`: Patient Status, 2-character alphanumeric.
    *   `10 B-DRG-CODE PIC X(03)`: DRG Code, 3-character alphanumeric.
    *   `10 B-LOS PIC 9(03)`: Length of Stay, 3-digit numeric.
    *   `10 B-COV-DAYS PIC 9(03)`: Covered Days, 3-digit numeric.
    *   `10 B-LTR-DAYS PIC 9(02)`: Lifetime Reserve Days, 2-digit numeric.
    *   `10 B-DISCHARGE-DATE`: Discharge Date
        *   `15 B-DISCHG-CC PIC 9(02)`: Century/Control Code, 2-digit numeric.
        *   `15 B-DISCHG-YY PIC 9(02)`: Year, 2-digit numeric.
        *   `15 B-DISCHG-MM PIC 9(02)`: Month, 2-digit numeric.
        *   `15 B-DISCHG-DD PIC 9(02)`: Day, 2-digit numeric.
    *   `10 B-COV-CHARGES PIC 9(07)V9(02)`: Covered Charges, 9-digit numeric (7 integer, 2 decimal).
    *   `10 B-SPEC-PAY-IND PIC X(01)`: Special Payment Indicator, 1-character alphanumeric.
    *   `10 FILLER PIC X(13)`: Filler, 13-character alphanumeric.

*   **`PPS-DATA-ALL`**:
    *   This structure is used to return the calculated PPS data to the calling program.
    *   `05 PPS-RTC PIC 9(02)`: PPS Return Code, 2-digit numeric.
    *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02)`: Charge Threshold, 9-digit numeric (7 integer, 2 decimal).
    *   `05 PPS-DATA`: PPS Data
        *   `10 PPS-MSA PIC X(04)`: MSA (Metropolitan Statistical Area), 4-character alphanumeric.
        *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04)`: Wage Index, 6-digit numeric (2 integer, 4 decimal).
        *   `10 PPS-AVG-LOS PIC 9(02)V9(01)`: Average Length of Stay, 3-digit numeric (2 integer, 1 decimal).
        *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04)`: Relative Weight, 5-digit numeric (1 integer, 4 decimal).
        *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02)`: Outlier Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-LOS PIC 9(03)`: Length of Stay, 3-digit numeric.
        *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02)`: DRG Adjusted Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02)`: Federal Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02)`: Final Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FAC-COSTS PIC 9(07)V9(02)`: Facility Costs, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02)`: New Facility Specific Rate, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02)`: Outlier Threshold, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-SUBM-DRG-CODE PIC X(03)`: Submitted DRG Code, 3-character alphanumeric.
        *   `10 PPS-CALC-VERS-CD PIC X(05)`: Calculation Version Code, 5-character alphanumeric.
        *   `10 PPS-REG-DAYS-USED PIC 9(03)`: Regular Days Used, 3-digit numeric.
        *   `10 PPS-LTR-DAYS-USED PIC 9(03)`: Lifetime Reserve Days Used, 3-digit numeric.
        *   `10 PPS-BLEND-YEAR PIC 9(01)`: Blend Year, 1-digit numeric.
        *   `10 PPS-COLA PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment), 4-digit numeric (1 integer, 3 decimal).
        *   `10 FILLER PIC X(04)`: Filler, 4-character alphanumeric.
    *   `05 PPS-OTHER-DATA`: Other PPS Data
        *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05)`: National Labor Percentage, 6-digit numeric (1 integer, 5 decimal).
        *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05)`: National Non-Labor Percentage, 6-digit numeric (1 integer, 5 decimal).
        *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02)`: Standard Federal Rate, 7-digit numeric (5 integer, 2 decimal).
        *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03)`: Budget Neutrality Rate, 4-digit numeric (1 integer, 3 decimal).
        *   `10 FILLER PIC X(20)`: Filler, 20-character alphanumeric.
    *   `05 PPS-PC-DATA`: PPS PC Data
        *   `10 PPS-COT-IND PIC X(01)`: COT (Cost Outlier Threshold) Indicator, 1-character alphanumeric.
        *   `10 FILLER PIC X(20)`: Filler, 20-character alphanumeric.

*   **`PRICER-OPT-VERS-SW`**:
    *   This structure seems to indicate which versions of the tables are passed.
    *   `05 PRICER-OPTION-SW PIC X(01)`: Pricer Option Switch, 1-character alphanumeric.
        *   `88 ALL-TABLES-PASSED VALUE 'A'`:  Condition to check if all tables were passed.
        *   `88 PROV-RECORD-PASSED VALUE 'P'`: Condition to check if provider record was passed.
    *   `05 PPS-VERSIONS`: PPS Versions
        *   `10 PPDRV-VERSION PIC X(05)`: PPDRV Version, 5-character alphanumeric.

*   **`PROV-NEW-HOLD`**:
    *   This structure is used to pass provider-specific information to the calling program.
    *   `02 PROV-NEWREC-HOLD1`: Provider Record Hold 1
        *   `05 P-NEW-NPI10`: NPI (National Provider Identifier)
            *   `10 P-NEW-NPI8 PIC X(08)`: NPI, 8-character alphanumeric.
            *   `10 P-NEW-NPI-FILLER PIC X(02)`: Filler, 2-character alphanumeric.
        *   `05 P-NEW-PROVIDER-NO`: Provider Number
            *   `10 P-NEW-STATE PIC 9(02)`: State, 2-digit numeric.
            *   `10 FILLER PIC X(04)`: Filler, 4-character alphanumeric.
        *   `05 P-NEW-DATE-DATA`: Date Data
            *   `10 P-NEW-EFF-DATE`: Effective Date
                *   `15 P-NEW-EFF-DT-CC PIC 9(02)`: Effective Date Century/Control Code, 2-digit numeric.
                *   `15 P-NEW-EFF-DT-YY PIC 9(02)`: Effective Date Year, 2-digit numeric.
                *   `15 P-NEW-EFF-DT-MM PIC 9(02)`: Effective Date Month, 2-digit numeric.
                *   `15 P-NEW-EFF-DT-DD PIC 9(02)`: Effective Date Day, 2-digit numeric.
            *   `10 P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02)`: FY Begin Date Century/Control Code, 2-digit numeric.
                *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02)`: FY Begin Date Year, 2-digit numeric.
                *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02)`: FY Begin Date Month, 2-digit numeric.
                *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02)`: FY Begin Date Day, 2-digit numeric.
            *   `10 P-NEW-REPORT-DATE`: Report Date
                *   `15 P-NEW-REPORT-DT-CC PIC 9(02)`: Report Date Century/Control Code, 2-digit numeric.
                *   `15 P-NEW-REPORT-DT-YY PIC 9(02)`: Report Date Year, 2-digit numeric.
                *   `15 P-NEW-REPORT-DT-MM PIC 9(02)`: Report Date Month, 2-digit numeric.
                *   `15 P-NEW-REPORT-DT-DD PIC 9(02)`: Report Date Day, 2-digit numeric.
            *   `10 P-NEW-TERMINATION-DATE`: Termination Date
                *   `15 P-NEW-TERM-DT-CC PIC 9(02)`: Termination Date Century/Control Code, 2-digit numeric.
                *   `15 P-NEW-TERM-DT-YY PIC 9(02)`: Termination Date Year, 2-digit numeric.
                *   `15 P-NEW-TERM-DT-MM PIC 9(02)`: Termination Date Month, 2-digit numeric.
                *   `15 P-NEW-TERM-DT-DD PIC 9(02)`: Termination Date Day, 2-digit numeric.
        *   `05 P-NEW-WAIVER-CODE PIC X(01)`: Waiver Code, 1-character alphanumeric.
            *   `88 P-NEW-WAIVER-STATE VALUE 'Y'`: Condition if waiver state is 'Y'.
        *   `05 P-NEW-INTER-NO PIC 9(05)`: Intern Number, 5-digit numeric.
        *   `05 P-NEW-PROVIDER-TYPE PIC X(02)`: Provider Type, 2-character alphanumeric.
        *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Current Census Division, 1-digit numeric.
        *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Current Division, redefined as 1-digit numeric.
        *   `05 P-NEW-MSA-DATA`: MSA Data
            *   `10 P-NEW-CHG-CODE-INDEX PIC X`: Charge Code Index, 1-character alphanumeric.
            *   `10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT`: Geo Location MSA, 4-character alphanumeric, right-justified.
            *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04)`: Geo Location MSA, redefined as 4-digit numeric.
            *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT`: Wage Index Location MSA, 4-character alphanumeric, right-justified.
            *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT`: Standard Amount Location MSA, 4-character alphanumeric, right-justified.
            *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Standard Amount Location MSA, redefined.
                *   `15 P-NEW-RURAL-1ST`: Rural 1st
                    *   `20 P-NEW-STAND-RURAL PIC XX`: Standard Rural, 2-character alphanumeric.
                        *   `88 P-NEW-STD-RURAL-CHECK VALUE ' '`: Condition if standard rural check is spaces.
                *   `15 P-NEW-RURAL-2ND PIC XX`: Rural 2nd, 2-character alphanumeric.
        *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX`: Sole Community, Dependent Hospital Year, 2-character alphanumeric.
        *   `05 P-NEW-LUGAR PIC X`: Lugar, 1-character alphanumeric.
        *   `05 P-NEW-TEMP-RELIEF-IND PIC X`: Temporary Relief Indicator, 1-character alphanumeric.
        *   `05 P-NEW-FED-PPS-BLEND-IND PIC X`: Federal PPS Blend Indicator, 1-character alphanumeric.
        *   `05 FILLER PIC X(05)`: Filler, 5-character alphanumeric.
    *   `02 PROV-NEWREC-HOLD2`: Provider Record Hold 2
        *   `05 P-NEW-VARIABLES`: Variables
            *   `10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: Facility Specific Rate, 7-digit numeric (5 integer, 2 decimal).
            *   `10 P-NEW-COLA PIC 9(01)V9(03)`: COLA, 4-digit numeric (1 integer, 3 decimal).
            *   `10 P-NEW-INTERN-RATIO PIC 9(01)V9(04)`: Intern Ratio, 5-digit numeric (1 integer, 4 decimal).
            *   `10 P-NEW-BED-SIZE PIC 9(05)`: Bed Size, 5-digit numeric.
            *   `10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03)`: Operating Cost to Charge Ratio, 4-digit numeric (1 integer, 3 decimal).
            *   `10 P-NEW-CMI PIC 9(01)V9(04)`: CMI (Case Mix Index), 5-digit numeric (1 integer, 4 decimal).
            *   `10 P-NEW-SSI-RATIO PIC V9(04)`: SSI Ratio, 4-digit numeric (4 decimal).
            *   `10 P-NEW-MEDICAID-RATIO PIC V9(04)`: Medicaid Ratio, 4-digit numeric (4 decimal).
            *   `10 P-NEW-PPS-BLEND-YR-IND PIC 9(01)`: PPS Blend Year Indicator, 1-digit numeric.
            *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05)`: Pruf Update Factor, 6-digit numeric (1 integer, 5 decimal).
            *   `10 P-NEW-DSH-PERCENT PIC V9(04)`: DSH (Disproportionate Share Hospital) Percent, 4-digit numeric (4 decimal).
            *   `10 P-NEW-FYE-DATE PIC X(08)`: Fiscal Year End Date, 8-character alphanumeric.
        *   `05 FILLER PIC X(23)`: Filler, 23-character alphanumeric.
    *   `02 PROV-NEWREC-HOLD3`: Provider Record Hold 3
        *   `05 P-NEW-PASS-AMT-DATA`: Passed Amount Data
            *   `10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99`: Passed Amount Capital, 6-digit numeric (4 integer, 2 decimal).
            *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99`: Passed Amount Direct Medical Education, 6-digit numeric (4 integer, 2 decimal).
            *   `10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99`: Passed Amount Organ Acquisition, 6-digit numeric (4 integer, 2 decimal).
            *   `10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99`: Passed Amount Plus Misc, 6-digit numeric (4 integer, 2 decimal).
        *   `05 P-NEW-CAPI-DATA`: Capital Data
            *   `15 P-NEW-CAPI-PPS-PAY-CODE PIC X`: Capital PPS Pay Code, 1-character alphanumeric.
            *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99`: Capital Hospital Specific Rate, 6-digit numeric (4 integer, 2 decimal).
            *   `15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99`: Capital Old HARM Rate, 6-digit numeric (4 integer, 2 decimal).
            *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999`: Capital New HARM Ratio, 5-digit numeric (1 integer, 4 decimal).
            *   `15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999`: Capital Cost to Charge Ratio, 4-digit numeric (3 decimal).
            *   `15 P-NEW-CAPI-NEW-HOSP PIC X`: Capital New Hospital, 1-character alphanumeric.
            *   `15 P-NEW-CAPI-IME PIC 9V9999`: Capital IME (Indirect Medical Education), 5-digit numeric (4 decimal).
            *   `15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99`: Capital Exceptions, 6-digit numeric (4 integer, 2 decimal).
        *   `05 FILLER PIC X(22)`: Filler, 22-character alphanumeric.

*   **`WAGE-NEW-INDEX-RECORD`**:
    *   This structure is used to pass wage index data to the calling program.
    *   `05 W-MSA PIC X(4)`: MSA, 4-character alphanumeric.
    *   `05 W-EFF-DATE PIC X(8)`: Effective Date, 8-character alphanumeric.
    *   `05 W-WAGE-INDEX1 PIC S9(02)V9(04)`: Wage Index 1, 6-digit signed numeric (2 integer, 4 decimal).
    *   `05 W-WAGE-INDEX2 PIC S9(02)V9(04)`: Wage Index 2, 6-digit signed numeric (2 integer, 4 decimal).
    *   `05 W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage Index 3, 6-digit signed numeric (2 integer, 4 decimal).

### PROCEDURE DIVISION

*   The `PROCEDURE DIVISION` uses the `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PRICER-OPT-VERS-SW`, `PROV-NEW-HOLD`, and `WAGE-NEW-INDEX-RECORD` data structures defined in the `LINKAGE SECTION`. This indicates that the program is designed to be called as a subroutine.
*   The program calculates a PPS payment based on the input data.
*   The main processing steps include:
    *   `0100-INITIAL-ROUTINE`: Initializes variables and sets constants.
    *   `1000-EDIT-THE-BILL-INFO`: Edits the bill data.
    *   `1700-EDIT-DRG-CODE`: Edits the DRG code.
    *   `2000-ASSEMBLE-PPS-VARIABLES`: Assembles PPS variables based on provider and wage index data.
    *   `3000-CALC-PAYMENT`: Calculates the payment.
    *   `7000-CALC-OUTLIER`: Calculates outlier payments.
    *   `8000-BLEND`: Calculates blended payments.
    *   `9000-MOVE-RESULTS`: Moves the results to the output data structures.

## Analysis of LTCAL042

### Files Accessed

*   **LTDRG031:** This file is included via a `COPY` statement. It likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay, used for calculating payments.

### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL042 - W O R K I N G S T O R A G E'`:  Initialized with a descriptive string, likely for debugging or identification.

*   **`CAL-VERSION`**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C04.2'`: Initialized with a version identifier, indicating the version of the calculation logic.

*   **`HOLD-PPS-COMPONENTS`**:
    *   This group of data elements stores intermediate calculation results and components used in the PPS (Prospective Payment System) calculation.
    *   `05 H-LOS PIC 9(03)`: Length of Stay (LOS),  3-digit numeric.
    *   `05 H-REG-DAYS PIC 9(03)`: Regular Days, 3-digit numeric.
    *   `05 H-TOTAL-DAYS PIC 9(05)`: Total Days, 5-digit numeric.
    *   `05 H-SSOT PIC 9(02)`: Short Stay Outlier Threshold, 2-digit numeric.
    *   `05 H-BLEND-RTC PIC 9(02)`: Blend Return Code, 2-digit numeric.
    *   `05 H-BLEND-FAC PIC 9(01)V9(01)`: Blend Facility Portion, 2-digit numeric (1 integer, 1 decimal).
    *   `05 H-BLEND-PPS PIC 9(01)V9(01)`: Blend PPS Portion, 2-digit numeric (1 integer, 1 decimal).
    *   `05 H-SS-PAY-AMT PIC 9(07)V9(02)`: Short Stay Payment Amount, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-SS-COST PIC 9(07)V9(02)`: Short Stay Cost, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-LABOR-PORTION PIC 9(07)V9(06)`: Labor Portion, 13-digit numeric (7 integer, 6 decimal).
    *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06)`: Non-Labor Portion, 13-digit numeric (7 integer, 6 decimal).
    *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02)`: Fixed Loss Amount, 9-digit numeric (7 integer, 2 decimal).
    *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: New Facility Specific Rate, 7-digit numeric (5 integer, 2 decimal).
    *   `05 H-LOS-RATIO PIC 9(01)V9(05)`: LOS Ratio, 6-digit numeric (1 integer, 5 decimal).

### Data Structures in LINKAGE SECTION

*   **`BILL-NEW-DATA`**:
    *   This structure receives billing information from the calling program.
    *   `10 B-NPI10`:  NPI (National Provider Identifier)
        *   `15 B-NPI8 PIC X(08)`:  NPI, 8-character alphanumeric.
        *   `15 B-NPI-FILLER PIC X(02)`: Filler, 2-character alphanumeric.
    *   `10 B-PROVIDER-NO PIC X(06)`: Provider Number, 6-character alphanumeric.
    *   `10 B-PATIENT-STATUS PIC X(02)`: Patient Status, 2-character alphanumeric.
    *   `10 B-DRG-CODE PIC X(03)`: DRG Code, 3-character alphanumeric.
    *   `10 B-LOS PIC 9(03)`: Length of Stay, 3-digit numeric.
    *   `10 B-COV-DAYS PIC 9(03)`: Covered Days, 3-digit numeric.
    *   `10 B-LTR-DAYS PIC 9(02)`: Lifetime Reserve Days, 2-digit numeric.
    *   `10 B-DISCHARGE-DATE`: Discharge Date
        *   `15 B-DISCHG-CC PIC 9(02)`: Century/Control Code, 2-digit numeric.
        *   `15 B-DISCHG-YY PIC 9(02)`: Year, 2-digit numeric.
        *   `15 B-DISCHG-MM PIC 9(02)`: Month, 2-digit numeric.
        *   `15 B-DISCHG-DD PIC 9(02)`: Day, 2-digit numeric.
    *   `10 B-COV-CHARGES PIC 9(07)V9(02)`: Covered Charges, 9-digit numeric (7 integer, 2 decimal).
    *   `10 B-SPEC-PAY-IND PIC X(01)`: Special Payment Indicator, 1-character alphanumeric.
    *   `10 FILLER PIC X(13)`: Filler, 13-character alphanumeric.

*   **`PPS-DATA-ALL`**:
    *   This structure is used to return the calculated PPS data to the calling program.
    *   `05 PPS-RTC PIC 9(02)`: PPS Return Code, 2-digit numeric.
    *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02)`: Charge Threshold, 9-digit numeric (7 integer, 2 decimal).
    *   `05 PPS-DATA`: PPS Data
        *   `10 PPS-MSA PIC X(04)`: MSA (Metropolitan Statistical Area), 4-character alphanumeric.
        *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04)`: Wage Index, 6-digit numeric (2 integer, 4 decimal).
        *   `10 PPS-AVG-LOS PIC 9(02)V9(01)`: Average Length of Stay, 3-digit numeric (2 integer, 1 decimal).
        *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04)`: Relative Weight, 5-digit numeric (1 integer, 4 decimal).
        *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02)`: Outlier Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-LOS PIC 9(03)`: Length of Stay, 3-digit numeric.
        *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02)`: DRG Adjusted Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02)`: Federal Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02)`: Final Payment Amount, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-FAC-COSTS PIC 9(07)V9(02)`: Facility Costs, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02)`: New Facility Specific Rate, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02)`: Outlier Threshold, 9-digit numeric (7 integer, 2 decimal).
        *   `10 PPS-SUBM-DRG-CODE PIC X(03)`: Submitted DRG Code, 3-character alphanumeric.
        *   `10 PPS-CALC-VERS-CD PIC X(05)`: Calculation Version Code, 5-character alphanumeric.
        *   `10 PPS-REG-DAYS-USED PIC 9(03)`: Regular Days Used, 3-digit numeric.
        *   `10 PPS-LTR-DAYS-USED PIC 9(03)`: Lifetime Reserve Days Used, 3-digit numeric.
        *   `10 PPS-BLEND-YEAR PIC 9(01)`: Blend Year, 1-digit numeric.
        *   `10 PPS-COLA PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment), 4-digit numeric (1 integer, 3 decimal).
        *   `10 FILLER PIC X(04)`: Filler, 4-character alphanumeric.
    *   `05 PPS-OTHER-DATA`: Other PPS Data
        *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05)`: National Labor Percentage, 6-digit numeric (1 integer, 5 decimal).
        *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05)`: National Non-Labor Percentage, 6-digit numeric (