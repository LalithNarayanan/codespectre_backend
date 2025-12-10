## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement to include `LTDRG031`. This implies that `LTDRG031` likely contains data that the program needs to access, though not necessarily through standard file I/O.
*   **Data Structures in `WORKING-STORAGE SECTION`:**

    *   `01 W-STORAGE-REF          PIC X(46)`:  A 46-character field used to store a program identification string.
    *   `01 CAL-VERSION            PIC X(05)`:  A 5-character field storing the calculation version ('C03.2').
    *   `01 HOLD-PPS-COMPONENTS`: This structure holds various components used in PPS calculations:
        *   `05 H-LOS                  PIC 9(03)`: Length of Stay (3 digits).
        *   `05 H-REG-DAYS             PIC 9(03)`: Regular Days (3 digits).
        *   `05 H-TOTAL-DAYS           PIC 9(05)`: Total Days (5 digits).
        *   `05 H-SSOT                 PIC 9(02)`:  Short Stay Outlier Threshold (2 digits).
        *   `05 H-BLEND-RTC            PIC 9(02)`:  Blend Rate Code (2 digits).
        *   `05 H-BLEND-FAC            PIC 9(01)V9(01)`: Blend Facility Rate (2 digits, 1 decimal).
        *   `05 H-BLEND-PPS            PIC 9(01)V9(01)`: Blend PPS Rate (2 digits, 1 decimal).
        *   `05 H-SS-PAY-AMT           PIC 9(07)V9(02)`: Short Stay Payment Amount (9 digits, 2 decimals).
        *   `05 H-SS-COST              PIC 9(07)V9(02)`: Short Stay Cost (9 digits, 2 decimals).
        *   `05 H-LABOR-PORTION        PIC 9(07)V9(06)`: Labor Portion (9 digits, 6 decimals).
        *   `05 H-NONLABOR-PORTION     PIC 9(07)V9(06)`: Non-Labor Portion (9 digits, 6 decimals).
        *   `05 H-FIXED-LOSS-AMT       PIC 9(07)V9(02)`: Fixed Loss Amount (9 digits, 2 decimals).
        *   `05 H-NEW-FAC-SPEC-RATE    PIC 9(05)V9(02)`: New Facility Specific Rate (5 digits, 2 decimals).
    *   `01  W-DRG-FILLS`: This appears to be a large set of values which is then redefined to create a table.
    *   `01  W-DRG-TABLE REDEFINES W-DRG-FILLS`: This structure defines a table of DRG (Diagnosis Related Group) data.
        *   `03  WWM-ENTRY OCCURS 502 TIMES`:  Defines a table with 502 entries.
            *   `05  WWM-DRG             PIC X(3)`:  DRG Code (3 characters).  Used as the key.
            *   `05  WWM-RELWT           PIC 9(1)V9(4)`: Relative Weight (1 digit, 4 decimals).
            *   `05  WWM-ALOS            PIC 9(2)V9(1)`: Average Length of Stay (2 digits, 1 decimal).

*   **Data Structures in `LINKAGE SECTION`:**

    *   `01 BILL-NEW-DATA`: This structure represents the input bill data passed to the program.
        *   `10 B-NPI10`: NPI (National Provider Identifier)
            *   `15 B-NPI8             PIC X(08)`:  NPI (8 characters).
            *   `15 B-NPI-FILLER       PIC X(02)`:  Filler for NPI (2 characters).
        *   `10 B-PROVIDER-NO          PIC X(06)`: Provider Number (6 characters).
        *   `10 B-PATIENT-STATUS       PIC X(02)`: Patient Status (2 characters).
        *   `10 B-DRG-CODE             PIC X(03)`: DRG Code (3 characters).
        *   `10 B-LOS                  PIC 9(03)`: Length of Stay (3 digits).
        *   `10 B-COV-DAYS             PIC 9(03)`: Covered Days (3 digits).
        *   `10 B-LTR-DAYS             PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   `10 B-DISCHARGE-DATE`:  Discharge Date.
            *   `15 B-DISCHG-CC              PIC 9(02)`: Century/Control Code (2 digits).
            *   `15 B-DISCHG-YY              PIC 9(02)`: Year (2 digits).
            *   `15 B-DISCHG-MM              PIC 9(02)`: Month (2 digits).
            *   `15 B-DISCHG-DD              PIC 9(02)`: Day (2 digits).
        *   `10 B-COV-CHARGES                PIC 9(07)V9(02)`: Covered Charges (7 digits, 2 decimals).
        *   `10 B-SPEC-PAY-IND               PIC X(01)`: Special Payment Indicator (1 character).
        *   `10 FILLER                       PIC X(13)`:  Filler (13 characters).
    *   `01 PPS-DATA-ALL`: This structure is used to return calculated PPS (Prospective Payment System) data to the calling program.
        *   `05 PPS-RTC                       PIC 9(02)`: Return Code (2 digits).  Indicates the result of the calculation.
        *   `05 PPS-CHRG-THRESHOLD            PIC 9(07)V9(02)`: Charge Threshold (7 digits, 2 decimals).
        *   `05 PPS-DATA`: PPS data
            *   `10 PPS-MSA                   PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   `10 PPS-WAGE-INDEX            PIC 9(02)V9(04)`: Wage Index (2 digits, 4 decimals).
            *   `10 PPS-AVG-LOS               PIC 9(02)V9(01)`: Average Length of Stay (2 digits, 1 decimal).
            *   `10 PPS-RELATIVE-WGT          PIC 9(01)V9(04)`: Relative Weight (1 digit, 4 decimals).
            *   `10 PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02)`: Outlier Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-LOS                   PIC 9(03)`: Length of Stay (3 digits).
            *   `10 PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FED-PAY-AMT           PIC 9(07)V9(02)`: Federal Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FINAL-PAY-AMT         PIC 9(07)V9(02)`: Final Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FAC-COSTS             PIC 9(07)V9(02)`: Facility Costs (7 digits, 2 decimals).
            *   `10 PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02)`: New Facility Specific Rate (7 digits, 2 decimals).
            *   `10 PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02)`: Outlier Threshold (7 digits, 2 decimals).
            *   `10 PPS-SUBM-DRG-CODE         PIC X(03)`: Submitted DRG Code (3 characters).
            *   `10 PPS-CALC-VERS-CD          PIC X(05)`: Calculation Version Code (5 characters).
            *   `10 PPS-REG-DAYS-USED         PIC 9(03)`: Regular Days Used (3 digits).
            *   `10 PPS-LTR-DAYS-USED         PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   `10 PPS-BLEND-YEAR            PIC 9(01)`: Blend Year (1 digit).
            *   `10 PPS-COLA                  PIC 9(01)V9(03)`: Cost of Living Adjustment (1 digit, 3 decimals).
            *   `10 FILLER                    PIC X(04)`: Filler (4 characters).
        *   `05 PPS-OTHER-DATA`: Other PPS data.
            *   `10 PPS-NAT-LABOR-PCT         PIC 9(01)V9(05)`: National Labor Percentage (1 digit, 5 decimals).
            *   `10 PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05)`: National Non-Labor Percentage (1 digit, 5 decimals).
            *   `10 PPS-STD-FED-RATE          PIC 9(05)V9(02)`: Standard Federal Rate (5 digits, 2 decimals).
            *   `10 PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03)`: Budget Neutrality Rate (1 digit, 3 decimals).
            *   `10 FILLER                    PIC X(20)`: Filler (20 characters).
        *   `05 PPS-PC-DATA`: PPS Payment Component Data
            *   `10 PPS-COT-IND               PIC X(01)`: Cost Outlier Indicator (1 character).
            *   `10 FILLER                    PIC X(20)`: Filler (20 characters).
    *   `01 PRICER-OPT-VERS-SW`:  Pricer Option/Version Switch.  Used to indicate if all tables or just the provider record was passed.
        *   `05 PRICER-OPTION-SW          PIC X(01)`:  Option Switch ('A' for all tables, 'P' for provider record).
            *   `88 ALL-TABLES-PASSED          VALUE 'A'`: Condition for all tables passed.
            *   `88 PROV-RECORD-PASSED         VALUE 'P'`: Condition for provider record passed.
        *   `05 PPS-VERSIONS`: PPS Versions.
            *   `10 PPDRV-VERSION         PIC X(05)`: Version of the PPDRV program (5 characters).
    *   `01 PROV-NEW-HOLD`:  Provider Record Hold.  This structure holds provider specific data.
        *   `02 PROV-NEWREC-HOLD1`: Part 1 of the Provider Record
            *   `05 P-NEW-NPI10`:  NPI (National Provider Identifier)
                *   `10 P-NEW-NPI8             PIC X(08)`:  NPI (8 characters).
                *   `10 P-NEW-NPI-FILLER       PIC X(02)`:  Filler for NPI (2 characters).
            *   `05 P-NEW-PROVIDER-NO`: Provider Number.
                *   `10 P-NEW-STATE            PIC 9(02)`: State Code (2 digits).
                *   `10 FILLER                 PIC X(04)`: Filler (4 characters).
            *   `05 P-NEW-DATE-DATA`: Date Data.
                *   `10 P-NEW-EFF-DATE`: Effective Date.
                    *   `15 P-NEW-EFF-DT-CC    PIC 9(02)`: Century/Control Code (2 digits).
                    *   `15 P-NEW-EFF-DT-YY    PIC 9(02)`: Year (2 digits).
                    *   `15 P-NEW-EFF-DT-MM    PIC 9(02)`: Month (2 digits).
                    *   `15 P-NEW-EFF-DT-DD    PIC 9(02)`: Day (2 digits).
                *   `10 P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02)`: Century/Control Code (2 digits).
                    *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02)`: Year (2 digits).
                    *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02)`: Month (2 digits).
                    *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02)`: Day (2 digits).
                *   `10 P-NEW-REPORT-DATE`: Report Date.
                    *   `15 P-NEW-REPORT-DT-CC PIC 9(02)`: Century/Control Code (2 digits).
                    *   `15 P-NEW-REPORT-DT-YY PIC 9(02)`: Year (2 digits).
                    *   `15 P-NEW-REPORT-DT-MM PIC 9(02)`: Month (2 digits).
                    *   `15 P-NEW-REPORT-DT-DD PIC 9(02)`: Day (2 digits).
                *   `10 P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `15 P-NEW-TERM-DT-CC   PIC 9(02)`: Century/Control Code (2 digits).
                    *   `15 P-NEW-TERM-DT-YY   PIC 9(02)`: Year (2 digits).
                    *   `15 P-NEW-TERM-DT-MM   PIC 9(02)`: Month (2 digits).
                    *   `15 P-NEW-TERM-DT-DD   PIC 9(02)`: Day (2 digits).
            *   `05 P-NEW-WAIVER-CODE          PIC X(01)`: Waiver Code (1 character).
                *   `88 P-NEW-WAIVER-STATE       VALUE 'Y'`: Condition for Waiver State.
            *   `05 P-NEW-INTER-NO             PIC 9(05)`: Intern Number (5 digits).
            *   `05 P-NEW-PROVIDER-TYPE        PIC X(02)`: Provider Type (2 characters).
            *   `05 P-NEW-CURRENT-CENSUS-DIV   PIC 9(01)`: Current Census Division (1 digit).
            *   `05 P-NEW-CURRENT-DIV   REDEFINES P-NEW-CURRENT-CENSUS-DIV   PIC 9(01)`: Redefines the current census division as a single digit.
            *   `05 P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data.
                *   `10 P-NEW-CHG-CODE-INDEX       PIC X`: Charge Code Index (1 character).
                *   `10 P-NEW-GEO-LOC-MSAX         PIC X(04) JUST RIGHT`: Geographic Location MSA (4 characters).
                *   `10 P-NEW-GEO-LOC-MSA9   REDEFINES P-NEW-GEO-LOC-MSAX  PIC 9(04)`: Redefines the geographic location as numeric (4 digits).
                *   `10 P-NEW-WAGE-INDEX-LOC-MSA   PIC X(04) JUST RIGHT`: Wage Index Location MSA (4 characters).
                *   `10 P-NEW-STAND-AMT-LOC-MSA    PIC X(04) JUST RIGHT`: Standard Amount Location MSA (4 characters).
                *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Redefines the standard amount location as numeric.
                    *   `15 P-NEW-RURAL-1ST`: Rural 1st part.
                        *   `20 P-NEW-STAND-RURAL  PIC XX`: Standard Rural (2 characters).
                            *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '`: Condition for standard rural check.
                    *   `15 P-NEW-RURAL-2ND        PIC XX`: Rural 2nd part (2 characters).
            *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX`:  Sole Community/Dependent Hospital Year (2 characters).
            *   `05 P-NEW-LUGAR                    PIC X`: LUGAR (1 character).
            *   `05 P-NEW-TEMP-RELIEF-IND          PIC X`: Temporary Relief Indicator (1 character).
            *   `05 P-NEW-FED-PPS-BLEND-IND        PIC X`: Federal PPS Blend Indicator (1 character).
            *   `05 FILLER                         PIC X(05)`: Filler (5 characters).
        *   `02 PROV-NEWREC-HOLD2`: Part 2 of the Provider Record.
            *   `05 P-NEW-VARIABLES`: Variables.
                *   `10 P-NEW-FAC-SPEC-RATE     PIC  9(05)V9(02)`: Facility Specific Rate (5 digits, 2 decimals).
                *   `10 P-NEW-COLA              PIC  9(01)V9(03)`: Cost of Living Adjustment (1 digit, 3 decimals).
                *   `10 P-NEW-INTERN-RATIO      PIC  9(01)V9(04)`: Intern Ratio (1 digit, 4 decimals).
                *   `10 P-NEW-BED-SIZE          PIC  9(05)`: Bed Size (5 digits).
                *   `10 P-NEW-OPER-CSTCHG-RATIO PIC  9(01)V9(03)`: Operating Cost to Charge Ratio (1 digit, 3 decimals).
                *   `10 P-NEW-CMI               PIC  9(01)V9(04)`: CMI (Case Mix Index) (1 digit, 4 decimals).
                *   `10 P-NEW-SSI-RATIO         PIC  V9(04)`: SSI Ratio (4 decimals).
                *   `10 P-NEW-MEDICAID-RATIO    PIC  V9(04)`: Medicaid Ratio (4 decimals).
                *   `10 P-NEW-PPS-BLEND-YR-IND  PIC  9(01)`: PPS Blend Year Indicator (1 digit).
                *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC  9(01)V9(05)`: Pruf Update Factor (1 digit, 5 decimals).
                *   `10 P-NEW-DSH-PERCENT       PIC  V9(04)`: DSH Percentage (4 decimals).
                *   `10 P-NEW-FYE-DATE          PIC  X(08)`: Fiscal Year End Date (8 characters).
            *   `05 FILLER                      PIC  X(23)`: Filler (23 characters).
        *   `02 PROV-NEWREC-HOLD3`: Part 3 of the Provider Record.
            *   `05 P-NEW-PASS-AMT-DATA`: Pass Amount Data.
                *   `10 P-NEW-PASS-AMT-CAPITAL    PIC 9(04)V99`: Pass Through Amount - Capital (4 digits, 2 decimals).
                *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99`: Pass Through Amount - Direct Medical Education (4 digits, 2 decimals).
                *   `10 P-NEW-PASS-AMT-ORGAN-ACQ  PIC 9(04)V99`: Pass Through Amount - Organ Acquisition (4 digits, 2 decimals).
                *   `10 P-NEW-PASS-AMT-PLUS-MISC  PIC 9(04)V99`: Pass Through Amount - Plus Miscellaneous (4 digits, 2 decimals).
            *   `05 P-NEW-CAPI-DATA`: Capital Data.
                *   `15 P-NEW-CAPI-PPS-PAY-CODE   PIC X`: Capital PPS Payment Code (1 character).
                *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99`: Capital Hospital Specific Rate (4 digits, 2 decimals).
                *   `15 P-NEW-CAPI-OLD-HARM-RATE  PIC 9(04)V99`: Capital Old Harm Rate (4 digits, 2 decimals).
                *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999`: Capital New Harm Ratio (1 digit, 4 decimals).
                *   `15 P-NEW-CAPI-CSTCHG-RATIO   PIC 9V999`: Capital Cost to Charge Ratio (1 digit, 3 decimals).
                *   `15 P-NEW-CAPI-NEW-HOSP       PIC X`: Capital New Hospital (1 character).
                *   `15 P-NEW-CAPI-IME            PIC 9V9999`: Capital IME (Indirect Medical Education) (4 decimals).
                *   `15 P-NEW-CAPI-EXCEPTIONS     PIC 9(04)V99`: Capital Exceptions (4 digits, 2 decimals).
            *   `05 FILLER                        PIC X(22)`: Filler (22 characters).
    *   `01 WAGE-NEW-INDEX-RECORD`:  Wage Index Record.
        *   `05 W-MSA                         PIC X(4)`: MSA (Metropolitan Statistical Area) Code (4 characters).
        *   `05 W-EFF-DATE                    PIC X(8)`: Effective Date (8 characters).
        *   `05 W-WAGE-INDEX1                 PIC S9(02)V9(04)`: Wage Index 1 (Signed 2 digits, 4 decimals).
        *   `05 W-WAGE-INDEX2                 PIC S9(02)V9(04)`: Wage Index 2 (Signed 2 digits, 4 decimals).
        *   `05 W-WAGE-INDEX3                 PIC S9(02)V9(04)`: Wage Index 3 (Signed 2 digits, 4 decimals).

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement to include `LTDRG031`. This implies that `LTDRG031` likely contains data that the program needs to access, though not necessarily through standard file I/O.
*   **Data Structures in `WORKING-STORAGE SECTION`:**

    *   `01 W-STORAGE-REF          PIC X(46)`:  A 46-character field used to store a program identification string.
    *   `01 CAL-VERSION            PIC X(05)`:  A 5-character field storing the calculation version ('C04.2').
    *   `01 HOLD-PPS-COMPONENTS`: This structure holds various components used in PPS calculations:
        *   `05 H-LOS                  PIC 9(03)`: Length of Stay (3 digits).
        *   `05 H-REG-DAYS             PIC 9(03)`: Regular Days (3 digits).
        *   `05 H-TOTAL-DAYS           PIC 9(05)`: Total Days (5 digits).
        *   `05 H-SSOT                 PIC 9(02)`:  Short Stay Outlier Threshold (2 digits).
        *   `05 H-BLEND-RTC            PIC 9(02)`:  Blend Rate Code (2 digits).
        *   `05 H-BLEND-FAC            PIC 9(01)V9(01)`: Blend Facility Rate (2 digits, 1 decimal).
        *   `05 H-BLEND-PPS            PIC 9(01)V9(01)`: Blend PPS Rate (2 digits, 1 decimal).
        *   `05 H-SS-PAY-AMT           PIC 9(07)V9(02)`: Short Stay Payment Amount (9 digits, 2 decimals).
        *   `05 H-SS-COST              PIC 9(07)V9(02)`: Short Stay Cost (9 digits, 2 decimals).
        *   `05 H-LABOR-PORTION        PIC 9(07)V9(06)`: Labor Portion (9 digits, 6 decimals).
        *   `05 H-NONLABOR-PORTION     PIC 9(07)V9(06)`: Non-Labor Portion (9 digits, 6 decimals).
        *   `05 H-FIXED-LOSS-AMT       PIC 9(07)V9(02)`: Fixed Loss Amount (9 digits, 2 decimals).
        *   `05 H-NEW-FAC-SPEC-RATE    PIC 9(05)V9(02)`: New Facility Specific Rate (5 digits, 2 decimals).
        *   `05 H-LOS-RATIO            PIC 9(01)V9(05)`: Length of Stay Ratio (1 digit, 5 decimals).
    *   `01  W-DRG-FILLS`: This appears to be a large set of values which is then redefined to create a table.
    *   `01  W-DRG-TABLE REDEFINES W-DRG-FILLS`: This structure defines a table of DRG (Diagnosis Related Group) data.
        *   `03  WWM-ENTRY OCCURS 502 TIMES`:  Defines a table with 502 entries.
            *   `05  WWM-DRG             PIC X(3)`:  DRG Code (3 characters).  Used as the key.
            *   `05  WWM-RELWT           PIC 9(1)V9(4)`: Relative Weight (1 digit, 4 decimals).
            *   `05  WWM-ALOS            PIC 9(2)V9(1)`: Average Length of Stay (2 digits, 1 decimal).

*   **Data Structures in `LINKAGE SECTION`:**

    *   `01 BILL-NEW-DATA`: This structure represents the input bill data passed to the program.
        *   `10 B-NPI10`: NPI (National Provider Identifier)
            *   `15 B-NPI8             PIC X(08)`:  NPI (8 characters).
            *   `15 B-NPI-FILLER       PIC X(02)`:  Filler for NPI (2 characters).
        *   `10 B-PROVIDER-NO          PIC X(06)`: Provider Number (6 characters).
        *   `10 B-PATIENT-STATUS       PIC X(02)`: Patient Status (2 characters).
        *   `10 B-DRG-CODE             PIC X(03)`: DRG Code (3 characters).
        *   `10 B-LOS                  PIC 9(03)`: Length of Stay (3 digits).
        *   `10 B-COV-DAYS             PIC 9(03)`: Covered Days (3 digits).
        *   `10 B-LTR-DAYS             PIC 9(02)`: Lifetime Reserve Days (2 digits).
        *   `10 B-DISCHARGE-DATE`:  Discharge Date.
            *   `15 B-DISCHG-CC              PIC 9(02)`: Century/Control Code (2 digits).
            *   `15 B-DISCHG-YY              PIC 9(02)`: Year (2 digits).
            *   `15 B-DISCHG-MM              PIC 9(02)`: Month (2 digits).
            *   `15 B-DISCHG-DD              PIC 9(02)`: Day (2 digits).
        *   `10 B-COV-CHARGES                PIC 9(07)V9(02)`: Covered Charges (7 digits, 2 decimals).
        *   `10 B-SPEC-PAY-IND               PIC X(01)`: Special Payment Indicator (1 character).
        *   `10 FILLER                       PIC X(13)`:  Filler (13 characters).
    *   `01 PPS-DATA-ALL`: This structure is used to return calculated PPS (Prospective Payment System) data to the calling program.
        *   `05 PPS-RTC                       PIC 9(02)`: Return Code (2 digits).  Indicates the result of the calculation.
        *   `05 PPS-CHRG-THRESHOLD            PIC 9(07)V9(02)`: Charge Threshold (7 digits, 2 decimals).
        *   `05 PPS-DATA`: PPS data
            *   `10 PPS-MSA                   PIC X(04)`: MSA (Metropolitan Statistical Area) Code (4 characters).
            *   `10 PPS-WAGE-INDEX            PIC 9(02)V9(04)`: Wage Index (2 digits, 4 decimals).
            *   `10 PPS-AVG-LOS               PIC 9(02)V9(01)`: Average Length of Stay (2 digits, 1 decimal).
            *   `10 PPS-RELATIVE-WGT          PIC 9(01)V9(04)`: Relative Weight (1 digit, 4 decimals).
            *   `10 PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02)`: Outlier Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-LOS                   PIC 9(03)`: Length of Stay (3 digits).
            *   `10 PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02)`: DRG Adjusted Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FED-PAY-AMT           PIC 9(07)V9(02)`: Federal Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FINAL-PAY-AMT         PIC 9(07)V9(02)`: Final Payment Amount (7 digits, 2 decimals).
            *   `10 PPS-FAC-COSTS             PIC 9(07)V9(02)`: Facility Costs (7 digits, 2 decimals).
            *   `10 PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02)`: New Facility Specific Rate (7 digits, 2 decimals).
            *   `10 PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02)`: Outlier Threshold (7 digits, 2 decimals).
            *   `10 PPS-SUBM-DRG-CODE         PIC X(03)`: Submitted DRG Code (3 characters).
            *   `10 PPS-CALC-VERS-CD          PIC X(05)`: Calculation Version Code (5 characters).
            *   `10 PPS-REG-DAYS-USED         PIC 9(03)`: Regular Days Used (3 digits).
            *   `10 PPS-LTR-DAYS-USED         PIC 9(03)`: Lifetime Reserve Days Used (3 digits).
            *   `10 PPS-BLEND-YEAR            PIC 9(01)`: Blend Year (1 digit).
            *   `10 PPS-COLA                  PIC 9(01)V9(03)`: Cost of Living Adjustment (1 digit, 3 decimals).
            *   `10 FILLER                    PIC X(04)`: Filler (4 characters).
        *   `05 PPS-OTHER-DATA`: Other PPS data.
            *   `10 PPS-NAT-LABOR-PCT         PIC 9(01)V9(05)`: National Labor Percentage (1 digit, 5 decimals).
            *   `10 PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05)`: National Non-Labor Percentage (1 digit, 5 decimals).
            *   `10 PPS-STD-FED-RATE          PIC 9(05)V9(02)`: Standard Federal Rate (5 digits, 2 decimals).
            *   `10 PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03)`: Budget Neutrality Rate (1 digit, 3 decimals).
            *   `10 FILLER                    PIC X(20)`: Filler (20 characters).
        *   `05 PPS-PC-DATA`: PPS Payment Component Data
            *   `10 PPS-COT-IND               PIC X(01)`: Cost Outlier Indicator (1 character).
            *   `10 FILLER                    PIC X(20)`: Filler (20 characters).
    *   `01 PRICER-OPT-VERS-SW`:  Pricer Option/Version Switch.  Used to indicate if all tables or just the provider record was passed.
        *   `05 PRICER-OPTION-SW          PIC X(01)`:  Option Switch ('A' for all tables, 'P' for provider record).
            *   `88 ALL-TABLES-PASSED          VALUE 'A'`: Condition for all tables passed.
            *   `88 PROV-RECORD-PASSED         VALUE 'P'`: Condition for provider record passed.
        *   `05 PPS-VERSIONS`: PPS Versions.
            *   `10 PPDRV-VERSION         PIC X(05)`: Version of the PPDRV program (5 characters).
    *   `01 PROV-NEW-HOLD`:  Provider Record Hold.  This structure holds provider specific data.
        *   `02 PROV-NEWREC-HOLD1`: Part 1 of the Provider Record
            *   `05 P-NEW-NPI10`:  NPI (National Provider Identifier)
                *   `10 P-NEW-NPI8             PIC X(0