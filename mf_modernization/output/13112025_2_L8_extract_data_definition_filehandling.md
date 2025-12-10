Here's the analysis of the provided COBOL programs, detailing the files accessed, data structures in WORKING-STORAGE, and data structures in LINKAGE SECTION for each program.

## LTCAL032

**Files Accessed:**

*   **None** -  This program does not directly access any files.
*   **COPY LTDRG031.** - This program includes a copybook named `LTDRG031`.

**Data Structures in WORKING-STORAGE SECTION:**

```cobol
001800 01  W-STORAGE-REF                  PIC X(46)  VALUE
001900     'LTCAL032      - W O R K I N G   S T O R A G E'.
002000 01  CAL-VERSION                    PIC X(05)  VALUE 'C03.2'.
024500 01  HOLD-PPS-COMPONENTS.
024900     05  H-LOS                        PIC 9(03).
024900     05  H-REG-DAYS                   PIC 9(03).
024900     05  H-TOTAL-DAYS                 PIC 9(05).
024900     05  H-SSOT                       PIC 9(02).
024900     05  H-BLEND-RTC                  PIC 9(02).
024900     05  H-BLEND-FAC                  PIC 9(01)V9(01).
024900     05  H-BLEND-PPS                  PIC 9(01)V9(01).
026200     05  H-SS-PAY-AMT                 PIC 9(07)V9(02).
026200     05  H-SS-COST                    PIC 9(07)V9(02).
026300     05  H-LABOR-PORTION              PIC 9(07)V9(06).
026300     05  H-NONLABOR-PORTION           PIC 9(07)V9(06).
026200     05  H-FIXED-LOSS-AMT             PIC 9(07)V9(02).
050600     05  H-NEW-FAC-SPEC-RATE          PIC 9(05)V9(02).
040800 01  PRICER-OPT-VERS-SW.
040900     05  PRICER-OPTION-SW          PIC X(01).
041000         88  ALL-TABLES-PASSED          VALUE 'A'.
041100         88  PROV-RECORD-PASSED         VALUE 'P'.
041200     05  PPS-VERSIONS.
041300         10  PPDRV-VERSION         PIC X(05).
```

*   `W-STORAGE-REF`:  A 46-character field containing a descriptive string identifying the program and the storage area.
*   `CAL-VERSION`: A 5-character field storing the version of the calculation logic. Value is 'C03.2'.
*   `HOLD-PPS-COMPONENTS`: A group of fields used to store intermediate calculation results and components related to the PPS (Prospective Payment System) calculation.
    *   `H-LOS`: Length of Stay (3 digits).
    *   `H-REG-DAYS`: Regular Days (3 digits).
    *   `H-TOTAL-DAYS`: Total Days (5 digits).
    *   `H-SSOT`: Short Stay Threshold (2 digits).
    *   `H-BLEND-RTC`: Blend Year Return Code (2 digits).
    *   `H-BLEND-FAC`: Blend Facility Rate (1 digit, 1 decimal place).
    *   `H-BLEND-PPS`: Blend PPS Rate (1 digit, 1 decimal place).
    *   `H-SS-PAY-AMT`: Short Stay Payment Amount (7 digits, 2 decimal places).
    *   `H-SS-COST`: Short Stay Cost (7 digits, 2 decimal places).
    *   `H-LABOR-PORTION`: Labor Portion (7 digits, 6 decimal places).
    *   `H-NONLABOR-PORTION`: Non-Labor Portion (7 digits, 6 decimal places).
    *   `H-FIXED-LOSS-AMT`: Fixed Loss Amount (7 digits, 2 decimal places).
    *   `H-NEW-FAC-SPEC-RATE`: New Facility Specific Rate (5 digits, 2 decimal places).
*   `PRICER-OPT-VERS-SW`: A group used to determine the versions of the LTDRV031 programs that will be passed back.
    *   `PRICER-OPTION-SW`: A single-character field.
        *   `ALL-TABLES-PASSED`: Condition that is true when `PRICER-OPTION-SW` is 'A'.
        *   `PROV-RECORD-PASSED`: Condition that is true when `PRICER-OPTION-SW` is 'P'.
    *   `PPS-VERSIONS`: Group containing the version of the calculation.
        *   `PPDRV-VERSION`:  Version of the PPDRV program (5 characters).

**Data Structures in LINKAGE SECTION:**

```cobol
028600 01  BILL-NEW-DATA.
028700     10  B-NPI10.
028800         15  B-NPI8             PIC X(08).
028900         15  B-NPI-FILLER       PIC X(02).
029000     10  B-PROVIDER-NO          PIC X(06).
029000     10  B-PATIENT-STATUS       PIC X(02).
029000     10  B-DRG-CODE             PIC X(03).
029200     10  B-LOS                  PIC 9(03).
029300     10  B-COV-DAYS             PIC 9(03).
029700     10  B-LTR-DAYS             PIC 9(02).
029900     10  B-DISCHARGE-DATE.
030000         15  B-DISCHG-CC              PIC 9(02).
030100         15  B-DISCHG-YY              PIC 9(02).
030000         15  B-DISCHG-MM              PIC 9(02).
030100         15  B-DISCHG-DD              PIC 9(02).
030200     10  B-COV-CHARGES                PIC 9(07)V9(02).
030200     10  B-SPEC-PAY-IND               PIC X(01).
030300     10  FILLER                       PIC X(13).
036300 01  PPS-DATA-ALL.
036500     05  PPS-RTC                       PIC 9(02).
036500     05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02).
036400     05  PPS-DATA.
036600         10  PPS-MSA                   PIC X(04).
036600         10  PPS-WAGE-INDEX            PIC 9(02)V9(04).
036800         10  PPS-AVG-LOS               PIC 9(02)V9(01).
036900         10  PPS-RELATIVE-WGT          PIC 9(01)V9(04).
037300         10  PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02).
037500         10  PPS-LOS                   PIC 9(03).
038000         10  PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02).
038000         10  PPS-FED-PAY-AMT           PIC 9(07)V9(02).
038000         10  PPS-FINAL-PAY-AMT         PIC 9(07)V9(02).
038000         10  PPS-FAC-COSTS             PIC 9(07)V9(02).
038000         10  PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02).
038300         10  PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02).
038500         10  PPS-SUBM-DRG-CODE         PIC X(03).
               10  PPS-CALC-VERS-CD          PIC X(05).
               10  PPS-REG-DAYS-USED         PIC 9(03).
               10  PPS-LTR-DAYS-USED         PIC 9(03).
               10  PPS-BLEND-YEAR            PIC 9(01).
               10  PPS-COLA                  PIC 9(01)V9(03).
038800         10  FILLER                    PIC X(04).
038900     05  PPS-OTHER-DATA.
039200         10  PPS-NAT-LABOR-PCT         PIC 9(01)V9(05).
039200         10  PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05).
039400         10  PPS-STD-FED-RATE          PIC 9(05)V9(02).
039400         10  PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03).
039800         10  FILLER                    PIC X(20).
039900     05  PPS-PC-DATA.
040000         10  PPS-COT-IND               PIC X(01).
040100         10  FILLER                    PIC X(20).
042000 01  PROV-NEW-HOLD.
042100     02  PROV-NEWREC-HOLD1.
042200         05  P-NEW-NPI10.
042300             10  P-NEW-NPI8             PIC X(08).
042400             10  P-NEW-NPI-FILLER       PIC X(02).
042500         05  P-NEW-PROVIDER-NO.
042600             10  P-NEW-STATE            PIC 9(02).
042700             10  FILLER                 PIC X(04).
042800         05  P-NEW-DATE-DATA.
042900             10  P-NEW-EFF-DATE.
043000                 15  P-NEW-EFF-DT-CC    PIC 9(02).
043100                 15  P-NEW-EFF-DT-YY    PIC 9(02).
043200                 15  P-NEW-EFF-DT-MM    PIC 9(02).
043300                 15  P-NEW-EFF-DT-DD    PIC 9(02).
043400             10  P-NEW-FY-BEGIN-DATE.
043500                 15  P-NEW-FY-BEG-DT-CC PIC 9(02).
043600                 15  P-NEW-FY-BEG-DT-YY PIC 9(02).
043700                 15  P-NEW-FY-BEG-DT-MM PIC 9(02).
043800                 15  P-NEW-FY-BEG-DT-DD PIC 9(02).
043900             10  P-NEW-REPORT-DATE.
044000                 15  P-NEW-REPORT-DT-CC PIC 9(02).
044100                 15  P-NEW-REPORT-DT-YY PIC 9(02).
044200                 15  P-NEW-REPORT-DT-MM PIC 9(02).
044300                 15  P-NEW-REPORT-DT-DD PIC 9(02).
044400             10  P-NEW-TERMINATION-DATE.
044500                 15  P-NEW-TERM-DT-CC   PIC 9(02).
044600                 15  P-NEW-TERM-DT-YY   PIC 9(02).
044700                 15  P-NEW-TERM-DT-MM   PIC 9(02).
044800                 15  P-NEW-TERM-DT-DD   PIC 9(02).
044900         05  P-NEW-WAIVER-CODE          PIC X(01).
045000             88  P-NEW-WAIVER-STATE       VALUE 'Y'.
045100         05  P-NEW-INTER-NO             PIC 9(05).
045200         05  P-NEW-PROVIDER-TYPE        PIC X(02).
047000         05  P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).
048000         05  P-NEW-CURRENT-DIV   REDEFINES
048100                    P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).
048300         05  P-NEW-MSA-DATA.
048400             10  P-NEW-CHG-CODE-INDEX       PIC X.
048500             10  P-NEW-GEO-LOC-MSAX         PIC X(04) JUST RIGHT.
048600             10  P-NEW-GEO-LOC-MSA9   REDEFINES
048700                             P-NEW-GEO-LOC-MSAX  PIC 9(04).
048800             10  P-NEW-WAGE-INDEX-LOC-MSA   PIC X(04) JUST RIGHT.
048900             10  P-NEW-STAND-AMT-LOC-MSA    PIC X(04) JUST RIGHT.
049000             10  P-NEW-STAND-AMT-LOC-MSA9
049100                 REDEFINES P-NEW-STAND-AMT-LOC-MSA.
049200                 15  P-NEW-RURAL-1ST.
049300                     20  P-NEW-STAND-RURAL  PIC XX.
049400                         88  P-NEW-STD-RURAL-CHECK VALUE '  '.
049500                 15  P-NEW-RURAL-2ND        PIC XX.
049600         05  P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.
050000         05  P-NEW-LUGAR                    PIC X.
050100         05  P-NEW-TEMP-RELIEF-IND          PIC X.
050200         05  P-NEW-FED-PPS-BLEND-IND        PIC X.
050300         05  FILLER                         PIC X(05).
050400     02  PROV-NEWREC-HOLD2.
050500         05  P-NEW-VARIABLES.
050600             10  P-NEW-FAC-SPEC-RATE     PIC  9(05)V9(02).
050700             10  P-NEW-COLA              PIC  9(01)V9(03).
050800             10  P-NEW-INTERN-RATIO      PIC  9(01)V9(04).
050900             10  P-NEW-BED-SIZE          PIC  9(05).
051000             10  P-NEW-OPER-CSTCHG-RATIO PIC  9(01)V9(03).
051100             10  P-NEW-CMI               PIC  9(01)V9(04).
051200             10  P-NEW-SSI-RATIO         PIC  V9(04).
051300             10  P-NEW-MEDICAID-RATIO    PIC  V9(04).
051400             10  P-NEW-PPS-BLEND-YR-IND  PIC  9(01).
051500             10  P-NEW-PRUF-UPDTE-FACTOR PIC  9(01)V9(05).
051600             10  P-NEW-DSH-PERCENT       PIC  V9(04).
051700             10  P-NEW-FYE-DATE          PIC  X(08).
051800         05  FILLER                      PIC  X(23).
051900     02  PROV-NEWREC-HOLD3.
052000         05  P-NEW-PASS-AMT-DATA.
052100             10  P-NEW-PASS-AMT-CAPITAL    PIC 9(04)V99.
052200             10  P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.
052300             10  P-NEW-PASS-AMT-ORGAN-ACQ  PIC 9(04)V99.
052400             10  P-NEW-PASS-AMT-PLUS-MISC  PIC 9(04)V99.
052500         05  P-NEW-CAPI-DATA.
052600             15  P-NEW-CAPI-PPS-PAY-CODE   PIC X.
052700             15  P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.
052800             15  P-NEW-CAPI-OLD-HARM-RATE  PIC 9(04)V99.
052900             15  P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.
053000             15  P-NEW-CAPI-CSTCHG-RATIO   PIC 9V999.
053100             15  P-NEW-CAPI-NEW-HOSP       PIC X.
053200             15  P-NEW-CAPI-IME            PIC 9V9999.
053300             15  P-NEW-CAPI-EXCEPTIONS     PIC 9(04)V99.
053400         05  FILLER                        PIC X(22).
053900 01  WAGE-NEW-INDEX-RECORD.
054000     05  W-MSA                         PIC X(4).
054100     05  W-EFF-DATE                    PIC X(8).
054200     05  W-WAGE-INDEX1                 PIC S9(02)V9(04).
054200     05  W-WAGE-INDEX2                 PIC S9(02)V9(04).
           05  W-WAGE-INDEX3                 PIC S9(02)V9(04).
```

*   `BILL-NEW-DATA`:  This structure is passed *into* the program from the calling program, and contains the bill data.
    *   `B-NPI10`: NPI (National Provider Identifier) - contains the NPI8 and a filler.
    *   `B-PROVIDER-NO`: Provider Number (6 characters).
    *   `B-PATIENT-STATUS`: Patient Status (2 characters).
    *   `B-DRG-CODE`: DRG (Diagnosis Related Group) Code (3 characters).
    *   `B-LOS`: Length of Stay (3 digits).
    *   `B-COV-DAYS`: Covered Days (3 digits).
    *   `B-LTR-DAYS`: Lifetime Reserve Days (2 digits).
    *   `B-DISCHARGE-DATE`: Discharge Date (CCYYMMDD).
    *   `B-COV-CHARGES`: Covered Charges (7 digits, 2 decimal places).
    *   `B-SPEC-PAY-IND`: Special Payment Indicator (1 character).
*   `PPS-DATA-ALL`: This is the structure that is passed *out* of the program and returns the PPS calculation results.
    *   `PPS-RTC`: Return Code (2 digits).
    *   `PPS-CHRG-THRESHOLD`: Charge Threshold (7 digits, 2 decimal places).
    *   `PPS-DATA`: PPS Calculation data.
        *   `PPS-MSA`: MSA (Metropolitan Statistical Area) (4 characters).
        *   `PPS-WAGE-INDEX`: Wage Index (2 digits, 4 decimal places).
        *   `PPS-AVG-LOS`: Average Length of Stay (2 digits, 1 decimal place).
        *   `PPS-RELATIVE-WGT`: Relative Weight (1 digit, 4 decimal places).
        *   `PPS-OUTLIER-PAY-AMT`: Outlier Payment Amount (7 digits, 2 decimal places).
        *   `PPS-LOS`: Length of Stay (3 digits).
        *   `PPS-DRG-ADJ-PAY-AMT`: DRG Adjusted Payment Amount (7 digits, 2 decimal places).
        *   `PPS-FED-PAY-AMT`: Federal Payment Amount (7 digits, 2 decimal places).
        *   `PPS-FINAL-PAY-AMT`: Final Payment Amount (7 digits, 2 decimal places).
        *   `PPS-FAC-COSTS`: Facility Costs (7 digits, 2 decimal places).
        *   `PPS-NEW-FAC-SPEC-RATE`: New Facility Specific Rate (7 digits, 2 decimal places).
        *   `PPS-OUTLIER-THRESHOLD`: Outlier Threshold (7 digits, 2 decimal places).
        *   `PPS-SUBM-DRG-CODE`: Submitted DRG Code (3 characters).
        *   `PPS-CALC-VERS-CD`: Calculation Version Code (5 characters).
        *   `PPS-REG-DAYS-USED`: Regular Days Used (3 digits).
        *   `PPS-LTR-DAYS-USED`: Lifetime Reserve Days Used (3 digits).
        *   `PPS-BLEND-YEAR`: Blend Year (1 digit).
        *   `PPS-COLA`: COLA (Cost of Living Adjustment) (1 digit, 3 decimal places).
    *   `PPS-OTHER-DATA`: Other PPS data.
        *   `PPS-NAT-LABOR-PCT`: National Labor Percentage (1 digit, 5 decimal places).
        *   `PPS-NAT-NONLABOR-PCT`: National Non-Labor Percentage (1 digit, 5 decimal places).
        *   `PPS-STD-FED-RATE`: Standard Federal Rate (5 digits, 2 decimal places).
        *   `PPS-BDGT-NEUT-RATE`: Budget Neutrality Rate (1 digit, 3 decimal places).
    *   `PPS-PC-DATA`: PPS PC Data.
        *   `PPS-COT-IND`: Cost Outlier Indicator (1 character).
*   `PROV-NEW-HOLD`: This structure is passed into the program, and contains the provider record.
    *   `PROV-NEWREC-HOLD1`: Provider Record Hold 1.
        *   `P-NEW-NPI10`:  NPI (National Provider Identifier) - contains the NPI8 and a filler.
        *   `P-NEW-PROVIDER-NO`: Provider Number.
        *   `P-NEW-DATE-DATA`: Date Data.
            *   `P-NEW-EFF-DATE`: Effective Date (CCYYMMDD).
            *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date (CCYYMMDD).
            *   `P-NEW-REPORT-DATE`: Report Date (CCYYMMDD).
            *   `P-NEW-TERMINATION-DATE`: Termination Date (CCYYMMDD).
        *   `P-NEW-WAIVER-CODE`: Waiver Code.
            *   `P-NEW-WAIVER-STATE`: Condition that is true when `P-NEW-WAIVER-CODE` is 'Y'.
        *   `P-NEW-INTER-NO`: Intern Number.
        *   `P-NEW-PROVIDER-TYPE`: Provider Type (2 characters).
        *   `P-NEW-CURRENT-CENSUS-DIV`: Current Census Division (1 digit).
        *   `P-NEW-CURRENT-DIV`: Redefines `P-NEW-CURRENT-CENSUS-DIV`.
        *   `P-NEW-MSA-DATA`: MSA Data.
            *   `P-NEW-CHG-CODE-INDEX`: Charge Code Index (1 character).
            *   `P-NEW-GEO-LOC-MSAX`: Geographic Location MSA (4 characters).
            *   `P-NEW-GEO-LOC-MSA9`: Redefines `P-NEW-GEO-LOC-MSAX`.
            *   `P-NEW-WAGE-INDEX-LOC-MSA`: Wage Index Location MSA (4 characters).
            *   `P-NEW-STAND-AMT-LOC-MSA`: Standard Amount Location MSA (4 characters).
            *   `P-NEW-STAND-AMT-LOC-MSA9`: Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                *   `P-NEW-RURAL-1ST`: Rural 1st.
                    *   `P-NEW-STAND-RURAL`: Standard Rural (2 characters).
                        *   `P-NEW-STD-RURAL-CHECK`: Condition that is true when `P-NEW-STAND-RURAL` is '  '.
                    *   `P-NEW-RURAL-2ND`: Rural 2nd (2 characters).
        *   `P-NEW-SOL-COM-DEP-HOSP-YR`: Sole Community Dependent Hospital Year (2 characters).
        *   `P-NEW-LUGAR`: Lugar (1 character).
        *   `P-NEW-TEMP-RELIEF-IND`: Temporary Relief Indicator (1 character).
        *   `P-NEW-FED-PPS-BLEND-IND`: Federal PPS Blend Indicator (1 character).
    *   `PROV-NEWREC-HOLD2`: Provider Record Hold 2.
        *   `P-NEW-VARIABLES`: Variables.
            *   `P-NEW-FAC-SPEC-RATE`: Facility Specific Rate (5 digits, 2 decimal places).
            *   `P-NEW-COLA`: COLA (Cost of Living Adjustment) (1 digit, 3 decimal places).
            *   `P-NEW-INTERN-RATIO`: Intern Ratio (1 digit, 4 decimal places).
            *   `P-NEW-BED-SIZE`: Bed Size (5 digits).
            *   `P-NEW-OPER-CSTCHG-RATIO`: Operating Cost-to-Charge Ratio (1 digit, 3 decimal places).
            *   `P-NEW-CMI`: CMI (Case Mix Index) (1 digit, 4 decimal places).
            *   `P-NEW-SSI-RATIO`: SSI Ratio (4 decimal places).
            *   `P-NEW-MEDICAID-RATIO`: Medicaid Ratio (4 decimal places).
            *   `P-NEW-PPS-BLEND-YR-IND`: PPS Blend Year Indicator (1 digit).
            *   `P-NEW-PRUF-UPDTE-FACTOR`: PRUF Update Factor (1 digit, 5 decimal places).
            *   `P-NEW-DSH-PERCENT`: DSH Percentage (4 decimal places).
            *   `P-NEW-FYE-DATE`: Fiscal Year End Date (8 characters).
    *   `PROV-NEWREC-HOLD3`: Provider Record Hold 3.
        *   `P-NEW-PASS-AMT-DATA`: Pass-Through Amount Data.
            *   `P-NEW-PASS-AMT-CAPITAL`: Pass-Through Amount Capital (4 digits, 2 decimal places).
            *   `P-NEW-PASS-AMT-DIR-MED-ED`: Pass-Through Amount Direct Medical Education (4 digits, 2 decimal places).
            *   `P-NEW-PASS-AMT-ORGAN-ACQ`: Pass-Through Amount Organ Acquisition (4 digits, 2 decimal places).
            *   `P-NEW-PASS-AMT-PLUS-MISC`: Pass-Through Amount Plus Misc (4 digits, 2 decimal places).
        *   `P-NEW-CAPI-DATA`: Capital Data.
            *   `P-NEW-CAPI-PPS-PAY-CODE`: Capital PPS Payment Code (1 character).
            *   `P-NEW-CAPI-HOSP-SPEC-RATE`: Capital Hospital Specific Rate (4 digits, 2 decimal places).
            *   `P-NEW-CAPI-OLD-HARM-RATE`: Capital Old HARM Rate (4 digits, 2 decimal places).
            *   `P-NEW-CAPI-NEW-HARM-RATIO`: Capital New HARM Ratio (1 digit, 4 decimal places).
            *   `P-NEW-CAPI-CSTCHG-RATIO`: Capital Cost-to-Charge Ratio (3 decimal places).
            *   `P-NEW-CAPI-NEW-HOSP`: Capital New Hospital (1 character).
            *   `P-NEW-CAPI-IME`: Capital IME (Indirect Medical Education) (4 decimal places).
            *   `P-NEW-CAPI-EXCEPTIONS`: Capital Exceptions (4 digits, 2 decimal places).
*   `WAGE-NEW-INDEX-RECORD`: This is passed into the program, and contains the wage index data.
    *   `W-MSA`: MSA (Metropolitan Statistical Area) (4 characters).
    *   `W-EFF-DATE`: Effective Date (8 characters).
    *   `W-WAGE-INDEX1`: Wage Index 1 (signed 2 digits, 4 decimal places).
    *   `W-WAGE-INDEX2`: Wage Index 2 (signed 2 digits, 4 decimal places).
    *   `W-WAGE-INDEX3`: Wage Index 3 (signed 2 digits, 4 decimal places).

## LTCAL042

**Files Accessed:**

*   **None** - This program does not directly access any files.
*   **COPY LTDRG031.** - This program includes a copybook named `LTDRG031`.

**Data Structures in WORKING-STORAGE SECTION:**

```cobol
001800 01  W-STORAGE-REF                  PIC X(46)  VALUE
001900     'LTCAL042      - W O R K I N G   S T O R A G E'.
002000 01  CAL-VERSION                    PIC X(05)  VALUE 'C04.2'.
024500 01  HOLD-PPS-COMPONENTS.
024900     05  H-LOS                        PIC 9(03).
024900     05  H-REG-DAYS                   PIC 9(03).
024900     05  H-TOTAL-DAYS                 PIC 9(05).
024900     05  H-SSOT                       PIC 9(02).
024900     05  H-BLEND-RTC                  PIC 9(02).
024900     05  H-BLEND-FAC                  PIC 9(01)V9(01).
024900     05  H-BLEND-PPS                  PIC 9(01)V9(01).
026200     05  H-SS-PAY-AMT                 PIC 9(07)V9(02).
026200     05  H-SS-COST                    PIC 9(07)V9(02).
026300     05  H-LABOR-PORTION              PIC 9(07)V9(06).
026300     05  H-NONLABOR-PORTION           PIC 9(07)V9(06).
026200     05  H-FIXED-LOSS-AMT             PIC 9(07)V9(02).
050600     05  H-NEW-FAC-SPEC-RATE          PIC 9(05)V9(02).
050600     05  H-LOS-RATIO                  PIC 9(01)V9(05).
040800 01  PRICER-OPT-VERS-SW.
040900     05  PRICER-OPTION-SW          PIC X(01).
041000         88  ALL-TABLES-PASSED          VALUE 'A'.
041100         88  PROV-RECORD-PASSED         VALUE 'P'.
041200     05  PPS-VERSIONS.
041300         10  PPDRV-VERSION         PIC X(05).
```

*   `W-STORAGE-REF`: A 46-character field containing a descriptive string identifying the program and the storage area.
*   `CAL-VERSION