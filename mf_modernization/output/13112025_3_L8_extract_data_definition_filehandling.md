## Analysis of LTCAL032

This COBOL program, `LTCAL032`, is a subroutine designed to calculate Long-Term Care (LTC) payments based on the DRG (Diagnosis Related Group) system. It receives patient and provider data, performs calculations, and returns payment information. It appears to be for the fiscal year 2003, effective January 1, 2003.

### Files Accessed:

*   This program does not directly access any external files. It uses a `COPY` statement to include the data structure `LTDRG031`, which likely contains the DRG lookup table.

### Data Structures in WORKING-STORAGE SECTION:

```cobol
01  W-STORAGE-REF                  PIC X(46)  VALUE
    'LTCAL032      - W O R K I N G   S T O R A G E'.
```

*   **W-STORAGE-REF:** (PIC X(46)) A descriptive string identifying the program and the working storage area.

```cobol
01  CAL-VERSION                    PIC X(05)  VALUE 'C03.2'.
```

*   **CAL-VERSION:** (PIC X(05))  Indicates the version of the calculation logic.

```cobol
01  HOLD-PPS-COMPONENTS.
    05  H-LOS                        PIC 9(03).
    05  H-REG-DAYS                   PIC 9(03).
    05  H-TOTAL-DAYS                 PIC 9(05).
    05  H-SSOT                       PIC 9(02).
    05  H-BLEND-RTC                  PIC 9(02).
    05  H-BLEND-FAC                  PIC 9(01)V9(01).
    05  H-BLEND-PPS                  PIC 9(01)V9(01).
    05  H-SS-PAY-AMT                 PIC 9(07)V9(02).
    05  H-SS-COST                    PIC 9(07)V9(02).
    05  H-LABOR-PORTION              PIC 9(07)V9(06).
    05  H-NONLABOR-PORTION           PIC 9(07)V9(06).
    05  H-FIXED-LOSS-AMT             PIC 9(07)V9(02).
    05  H-NEW-FAC-SPEC-RATE          PIC 9(05)V9(02).
```

*   **HOLD-PPS-COMPONENTS:** This group of variables holds intermediate calculation results and components for the PPS (Prospective Payment System) calculations.
    *   **H-LOS:** (PIC 9(03)) Length of Stay.
    *   **H-REG-DAYS:** (PIC 9(03)) Regular days.
    *   **H-TOTAL-DAYS:** (PIC 9(05)) Total days.
    *   **H-SSOT:** (PIC 9(02)) Short Stay Outlier Threshold.
    *   **H-BLEND-RTC:** (PIC 9(02)) Blend Rate code.
    *   **H-BLEND-FAC:** (PIC 9(01)V9(01)) Blend Facility factor.
    *   **H-BLEND-PPS:** (PIC 9(01)V9(01)) Blend PPS factor.
    *   **H-SS-PAY-AMT:** (PIC 9(07)V9(02)) Short Stay Payment Amount.
    *   **H-SS-COST:** (PIC 9(07)V9(02)) Short Stay Cost.
    *   **H-LABOR-PORTION:** (PIC 9(07)V9(06)) Labor portion of the payment.
    *   **H-NONLABOR-PORTION:** (PIC 9(07)V9(06)) Non-labor portion of the payment.
    *   **H-FIXED-LOSS-AMT:** (PIC 9(07)V9(02)) Fixed loss amount for outlier calculation.
    *   **H-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) New Facility Specific Rate.

```cobol
01  PPS-DATA-ALL.
    05  PPS-RTC                       PIC 9(02).
    05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02).
    05  PPS-DATA.
        10  PPS-MSA                   PIC X(04).
        10  PPS-WAGE-INDEX            PIC 9(02)V9(04).
        10  PPS-AVG-LOS               PIC 9(02)V9(01).
        10  PPS-RELATIVE-WGT          PIC 9(01)V9(04).
        10  PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02).
        10  PPS-LOS                   PIC 9(03).
        10  PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02).
        10  PPS-FED-PAY-AMT           PIC 9(07)V9(02).
        10  PPS-FINAL-PAY-AMT         PIC 9(07)V9(02).
        10  PPS-FAC-COSTS             PIC 9(07)V9(02).
        10  PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02).
        10  PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02).
        10  PPS-SUBM-DRG-CODE         PIC X(03).
        10  PPS-CALC-VERS-CD          PIC X(05).
        10  PPS-REG-DAYS-USED         PIC 9(03).
        10  PPS-LTR-DAYS-USED         PIC 9(03).
        10  PPS-BLEND-YEAR            PIC 9(01).
        10  PPS-COLA                  PIC 9(01)V9(03).
        10  FILLER                    PIC X(04).
    05  PPS-OTHER-DATA.
        10  PPS-NAT-LABOR-PCT         PIC 9(01)V9(05).
        10  PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05).
        10  PPS-STD-FED-RATE          PIC 9(05)V9(02).
        10  PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03).
        10  FILLER                    PIC X(20).
    05  PPS-PC-DATA.
        10  PPS-COT-IND               PIC X(01).
        10  FILLER                    PIC X(20).
```

*   **PPS-DATA-ALL:** This group contains all the data fields related to the PPS calculation and returned to the calling program.
    *   **PPS-RTC:** (PIC 9(02)) Return Code. Indicates the result of the calculation and any errors.
    *   **PPS-CHRG-THRESHOLD:** (PIC 9(07)V9(02)) Charge threshold for outlier calculation.
    *   **PPS-DATA:**  Contains the main PPS calculation data.
        *   **PPS-MSA:** (PIC X(04))  MSA (Metropolitan Statistical Area) code.
        *   **PPS-WAGE-INDEX:** (PIC 9(02)V9(04)) Wage index for the MSA.
        *   **PPS-AVG-LOS:** (PIC 9(02)V9(01)) Average Length of Stay for the DRG.
        *   **PPS-RELATIVE-WGT:** (PIC 9(01)V9(04)) Relative weight for the DRG.
        *   **PPS-OUTLIER-PAY-AMT:** (PIC 9(07)V9(02)) Outlier payment amount.
        *   **PPS-LOS:** (PIC 9(03)) Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** (PIC 9(07)V9(02)) DRG adjusted payment amount.
        *   **PPS-FED-PAY-AMT:** (PIC 9(07)V9(02)) Federal payment amount.
        *   **PPS-FINAL-PAY-AMT:** (PIC 9(07)V9(02)) Final calculated payment amount.
        *   **PPS-FAC-COSTS:** (PIC 9(07)V9(02)) Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** (PIC 9(07)V9(02)) New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** (PIC 9(07)V9(02)) Outlier threshold.
        *   **PPS-SUBM-DRG-CODE:** (PIC X(03)) Submitted DRG code.
        *   **PPS-CALC-VERS-CD:** (PIC X(05)) Calculation version code.
        *   **PPS-REG-DAYS-USED:** (PIC 9(03)) Regular days used for payment.
        *   **PPS-LTR-DAYS-USED:** (PIC 9(03)) Lifetime Reserve Days used for payment.
        *   **PPS-BLEND-YEAR:** (PIC 9(01)) Blend year indicator.
        *   **PPS-COLA:** (PIC 9(01)V9(03)) Cost of Living Adjustment.
    *   **PPS-OTHER-DATA:** Contains other data used in PPS calculations.
        *   **PPS-NAT-LABOR-PCT:** (PIC 9(01)V9(05)) National labor percentage.
        *   **PPS-NAT-NONLABOR-PCT:** (PIC 9(01)V9(05)) National non-labor percentage.
        *   **PPS-STD-FED-RATE:** (PIC 9(05)V9(02)) Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** (PIC 9(01)V9(03)) Budget Neutrality Rate.
    *   **PPS-PC-DATA:** Contains data for processing of Capital Outlier.
        *   **PPS-COT-IND:** (PIC X(01)) Capital Outlier Indicator.

```cobol
01  PRICER-OPT-VERS-SW.
    05  PRICER-OPTION-SW          PIC X(01).
        88  ALL-TABLES-PASSED          VALUE 'A'.
        88  PROV-RECORD-PASSED         VALUE 'P'.
    05  PPS-VERSIONS.
        10  PPDRV-VERSION         PIC X(05).
```

*   **PRICER-OPT-VERS-SW:**  Switch for passing various versions of the program.
    *   **PRICER-OPTION-SW:** (PIC X(01)) Switch to indicate if all tables or just the provider record are passed.
        *   **ALL-TABLES-PASSED:** (VALUE 'A')  Indicates that all tables are passed.
        *   **PROV-RECORD-PASSED:** (VALUE 'P') Indicates that only the provider record is passed.
    *   **PPS-VERSIONS:** Contains the version of the calling program.
        *   **PPDRV-VERSION:** (PIC X(05)) Version of the calling program.

```cobol
01  PROV-NEW-HOLD.
    02  PROV-NEWREC-HOLD1.
        05  P-NEW-NPI10.
            10  P-NEW-NPI8             PIC X(08).
            10  P-NEW-NPI-FILLER       PIC X(02).
        05  P-NEW-PROVIDER-NO.
            10  P-NEW-STATE            PIC 9(02).
            10  FILLER                 PIC X(04).
        05  P-NEW-DATE-DATA.
            10  P-NEW-EFF-DATE.
                15  P-NEW-EFF-DT-CC    PIC 9(02).
                15  P-NEW-EFF-DT-YY    PIC 9(02).
                15  P-NEW-EFF-DT-MM    PIC 9(02).
                15  P-NEW-EFF-DT-DD    PIC 9(02).
            10  P-NEW-FY-BEGIN-DATE.
                15  P-NEW-FY-BEG-DT-CC PIC 9(02).
                15  P-NEW-FY-BEG-DT-YY PIC 9(02).
                15  P-NEW-FY-BEG-DT-MM PIC 9(02).
                15  P-NEW-FY-BEG-DT-DD PIC 9(02).
            10  P-NEW-REPORT-DATE.
                15  P-NEW-REPORT-DT-CC PIC 9(02).
                15  P-NEW-REPORT-DT-YY PIC 9(02).
                15  P-NEW-REPORT-DT-MM PIC 9(02).
                15  P-NEW-REPORT-DT-DD PIC 9(02).
            10  P-NEW-TERMINATION-DATE.
                15  P-NEW-TERM-DT-CC   PIC 9(02).
                15  P-NEW-TERM-DT-YY   PIC 9(02).
                15  P-NEW-TERM-DT-MM   PIC 9(02).
                15  P-NEW-TERM-DT-DD   PIC 9(02).
        05  P-NEW-WAIVER-CODE          PIC X(01).
            88  P-NEW-WAIVER-STATE       VALUE 'Y'.
        05  P-NEW-INTER-NO             PIC 9(05).
        05  P-NEW-PROVIDER-TYPE        PIC X(02).
        05  P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).
        05  P-NEW-CURRENT-DIV   REDEFINES
                    P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).
        05  P-NEW-MSA-DATA.
            10  P-NEW-CHG-CODE-INDEX       PIC X.
            10  P-NEW-GEO-LOC-MSAX         PIC X(04) JUST RIGHT.
            10  P-NEW-GEO-LOC-MSA9   REDEFINES
                            P-NEW-GEO-LOC-MSAX  PIC 9(04).
            10  P-NEW-WAGE-INDEX-LOC-MSA   PIC X(04) JUST RIGHT.
            10  P-NEW-STAND-AMT-LOC-MSA    PIC X(04) JUST RIGHT.
            10  P-NEW-STAND-AMT-LOC-MSA9
                REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                15  P-NEW-RURAL-1ST.
                    20  P-NEW-STAND-RURAL  PIC XX.
                        88  P-NEW-STD-RURAL-CHECK VALUE '  '.
                    15  P-NEW-RURAL-2ND        PIC XX.
        05  P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.
        05  P-NEW-LUGAR                    PIC X.
        05  P-NEW-TEMP-RELIEF-IND          PIC X.
        05  P-NEW-FED-PPS-BLEND-IND        PIC X.
        05  FILLER                         PIC X(05).
    02  PROV-NEWREC-HOLD2.
        05  P-NEW-VARIABLES.
            10  P-NEW-FAC-SPEC-RATE     PIC  9(05)V9(02).
            10  P-NEW-COLA              PIC  9(01)V9(03).
            10  P-NEW-INTERN-RATIO      PIC  9(01)V9(04).
            10  P-NEW-BED-SIZE          PIC  9(05).
            10  P-NEW-OPER-CSTCHG-RATIO PIC  9(01)V9(03).
            10  P-NEW-CMI               PIC  9(01)V9(04).
            10  P-NEW-SSI-RATIO         PIC  V9(04).
            10  P-NEW-MEDICAID-RATIO    PIC  V9(04).
            10  P-NEW-PPS-BLEND-YR-IND  PIC  9(01).
            10  P-NEW-PRUF-UPDTE-FACTOR PIC  9(01)V9(05).
            10  P-NEW-DSH-PERCENT       PIC  V9(04).
            10  P-NEW-FYE-DATE          PIC  X(08).
        05  FILLER                      PIC  X(23).
    02  PROV-NEWREC-HOLD3.
        05  P-NEW-PASS-AMT-DATA.
            10  P-NEW-PASS-AMT-CAPITAL    PIC 9(04)V99.
            10  P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.
            10  P-NEW-PASS-AMT-ORGAN-ACQ  PIC 9(04)V99.
            10  P-NEW-PASS-AMT-PLUS-MISC  PIC 9(04)V99.
        05  P-NEW-CAPI-DATA.
            15  P-NEW-CAPI-PPS-PAY-CODE   PIC X.
            15  P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.
            15  P-NEW-CAPI-OLD-HARM-RATE  PIC 9(04)V99.
            15  P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.
            15  P-NEW-CAPI-CSTCHG-RATIO   PIC 9V999.
            15  P-NEW-CAPI-NEW-HOSP       PIC X.
            15  P-NEW-CAPI-IME            PIC 9V9999.
            15  P-NEW-CAPI-EXCEPTIONS     PIC 9(04)V99.
        05  FILLER                        PIC X(22).
```

*   **PROV-NEW-HOLD:**  This complex group holds the provider-specific information.
    *   **PROV-NEWREC-HOLD1:**  Contains provider identification, dates, and other flags.
        *   **P-NEW-NPI10:** (Group) National Provider Identifier (NPI).
            *   **P-NEW-NPI8:** (PIC X(08))  NPI (first 8 digits).
            *   **P-NEW-NPI-FILLER:** (PIC X(02)) NPI Filler.
        *   **P-NEW-PROVIDER-NO:**  Provider Number
        *   **P-NEW-STATE:** (PIC 9(02))  State code.
        *   **P-NEW-DATE-DATA:** Contains various date fields.
            *   **P-NEW-EFF-DATE:** (Group) Effective date.
                *   **P-NEW-EFF-DT-CC:** (PIC 9(02)) Century/Code
                *   **P-NEW-EFF-DT-YY:** (PIC 9(02)) Year
                *   **P-NEW-EFF-DT-MM:** (PIC 9(02)) Month
                *   **P-NEW-EFF-DT-DD:** (PIC 9(02)) Day
            *   **P-NEW-FY-BEGIN-DATE:** (Group) Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-CC:** (PIC 9(02)) Century/Code
                *   **P-NEW-FY-BEG-DT-YY:** (PIC 9(02)) Year
                *   **P-NEW-FY-BEG-DT-MM:** (PIC 9(02)) Month
                *   **P-NEW-FY-BEG-DT-DD:** (PIC 9(02)) Day
            *   **P-NEW-REPORT-DATE:** (Group) Report Date.
                *   **P-NEW-REPORT-DT-CC:** (PIC 9(02)) Century/Code
                *   **P-NEW-REPORT-DT-YY:** (PIC 9(02)) Year
                *   **P-NEW-REPORT-DT-MM:** (PIC 9(02)) Month
                *   **P-NEW-REPORT-DT-DD:** (PIC 9(02)) Day
            *   **P-NEW-TERMINATION-DATE:** (Group) Termination Date.
                *   **P-NEW-TERM-DT-CC:** (PIC 9(02)) Century/Code
                *   **P-NEW-TERM-DT-YY:** (PIC 9(02)) Year
                *   **P-NEW-TERM-DT-MM:** (PIC 9(02)) Month
                *   **P-NEW-TERM-DT-DD:** (PIC 9(02)) Day
        *   **P-NEW-WAIVER-CODE:** (PIC X(01))  Waiver code.
            *   **P-NEW-WAIVER-STATE:** (VALUE 'Y')  Waiver state indicator.
        *   **P-NEW-INTER-NO:** (PIC 9(05))  Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** (PIC X(02))  Provider type code.
        *   **P-NEW-CURRENT-CENSUS-DIV:** (PIC 9(01)) Current Census Division.
        *   **P-NEW-CURRENT-DIV:** (PIC 9(01)) Redefines P-NEW-CURRENT-CENSUS-DIV.
        *   **P-NEW-MSA-DATA:** Contains MSA specific data.
            *   **P-NEW-CHG-CODE-INDEX:** (PIC X) Charge code index.
            *   **P-NEW-GEO-LOC-MSAX:** (PIC X(04)) Geo location MSA (just right).
            *   **P-NEW-GEO-LOC-MSA9:** (PIC 9(04)) Redefines P-NEW-GEO-LOC-MSAX.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** (PIC X(04)) Wage index location MSA (just right).
            *   **P-NEW-STAND-AMT-LOC-MSA:** (PIC X(04)) Standard amount location MSA (just right).
            *   **P-NEW-STAND-AMT-LOC-MSA9:** (Group) Redefines P-NEW-STAND-AMT-LOC-MSA
                *   **P-NEW-RURAL-1ST:** (Group)
                    *   **P-NEW-STAND-RURAL:** (PIC XX) Rural indicator.
                        *   **P-NEW-STD-RURAL-CHECK:** (VALUE '  ') Rural indicator check
                    *   **P-NEW-RURAL-2ND:** (PIC XX) Rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** (PIC XX) Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** (PIC X) Location.
        *   **P-NEW-TEMP-RELIEF-IND:** (PIC X) Temporary relief indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** (PIC X) Federal PPS blend indicator.
    *   **PROV-NEWREC-HOLD2:** Contains the provider's specific variables.
        *   **P-NEW-VARIABLES:** (Group)
            *   **P-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) Facility specific rate.
            *   **P-NEW-COLA:** (PIC 9(01)V9(03)) Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** (PIC 9(01)V9(04)) Intern ratio.
            *   **P-NEW-BED-SIZE:** (PIC 9(05)) Bed size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** (PIC 9(01)V9(03)) Operating cost to charge ratio.
            *   **P-NEW-CMI:** (PIC 9(01)V9(04)) Case Mix Index.
            *   **P-NEW-SSI-RATIO:** (PIC V9(04)) Supplemental Security Income ratio.
            *   **P-NEW-MEDICAID-RATIO:** (PIC V9(04)) Medicaid ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** (PIC 9(01)) PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** (PIC 9(01)V9(05))  Provider Update Factor.
            *   **P-NEW-DSH-PERCENT:** (PIC V9(04)) Disproportionate Share Hospital percentage.
            *   **P-NEW-FYE-DATE:** (PIC X(08)) Fiscal Year End Date.
    *   **PROV-NEWREC-HOLD3:**  Contains the pass amount data.
        *   **P-NEW-PASS-AMT-DATA:** (Group)
            *   **P-NEW-PASS-AMT-CAPITAL:** (PIC 9(04)V99) Capital pass-through amount.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** (PIC 9(04)V99) Direct Medical Education pass-through amount.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** (PIC 9(04)V99) Organ Acquisition pass-through amount.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** (PIC 9(04)V99) Plus miscellaneous pass-through amount.
        *   **P-NEW-CAPI-DATA:** (Group) Capital data.
            *   **P-NEW-CAPI-PPS-PAY-CODE:** (PIC X) Capital PPS payment code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** (PIC 9(04)V99) Hospital specific capital rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** (PIC 9(04)V99) Old HARM rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** (PIC 9(01)V9999) New HARM ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** (PIC 9V999) Capital cost to charge ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** (PIC X) New hospital indicator.
            *   **P-NEW-CAPI-IME:** (PIC 9V9999) Capital IME (Indirect Medical Education).
            *   **P-NEW-CAPI-EXCEPTIONS:** (PIC 9(04)V99) Capital exceptions.

```cobol
01  WAGE-NEW-INDEX-RECORD.
    05  W-MSA                         PIC X(4).
    05  W-EFF-DATE                    PIC X(8).
    05  W-WAGE-INDEX1                 PIC S9(02)V9(04).
    05  W-WAGE-INDEX2                 PIC S9(02)V9(04).
    05  W-WAGE-INDEX3                 PIC S9(02)V9(04).
```

*   **WAGE-NEW-INDEX-RECORD:**  This structure holds the wage index data.
    *   **W-MSA:** (PIC X(4)) MSA code.
    *   **W-EFF-DATE:** (PIC X(8)) Effective date of the wage index.
    *   **W-WAGE-INDEX1:** (PIC S9(02)V9(04)) Wage Index 1.
    *   **W-WAGE-INDEX2:** (PIC S9(02)V9(04)) Wage Index 2.
    *   **W-WAGE-INDEX3:** (PIC S9(02)V9(04)) Wage Index 3.

### Data Structures in LINKAGE SECTION:

```cobol
01  BILL-NEW-DATA.
    10  B-NPI10.
        15  B-NPI8             PIC X(08).
        15  B-NPI-FILLER       PIC X(02).
    10  B-PROVIDER-NO          PIC X(06).
    10  B-PATIENT-STATUS       PIC X(02).
    10  B-DRG-CODE             PIC X(03).
    10  B-LOS                  PIC 9(03).
    10  B-COV-DAYS             PIC 9(03).
    10  B-LTR-DAYS             PIC 9(02).
    10  B-DISCHARGE-DATE.
        15  B-DISCHG-CC              PIC 9(02).
        15  B-DISCHG-YY              PIC 9(02).
        15  B-DISCHG-MM              PIC 9(02).
        15  B-DISCHG-DD              PIC 9(02).
    10  B-COV-CHARGES                PIC 9(07)V9(02).
    10  B-SPEC-PAY-IND               PIC X(01).
    10  FILLER                       PIC X(13).
```

*   **BILL-NEW-DATA:**  This data structure represents the bill information passed *to* the subroutine from the calling program.
    *   **B-NPI10:**  (Group) NPI (National Provider Identifier).
        *   **B-NPI8:** (PIC X(08)) NPI (first 8 digits).
        *   **B-NPI-FILLER:** (PIC X(02)) NPI Filler.
    *   **B-PROVIDER-NO:** (PIC X(06)) Provider number.
    *   **B-PATIENT-STATUS:** (PIC X(02)) Patient status code.
    *   **B-DRG-CODE:** (PIC X(03)) DRG code.
    *   **B-LOS:** (PIC 9(03)) Length of stay.
    *   **B-COV-DAYS:** (PIC 9(03)) Covered days.
    *   **B-LTR-DAYS:** (PIC 9(02)) Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:** (Group) Discharge date.
        *   **B-DISCHG-CC:** (PIC 9(02)) Century/Code
        *   **B-DISCHG-YY:** (PIC 9(02)) Year
        *   **B-DISCHG-MM:** (PIC 9(02)) Month
        *   **B-DISCHG-DD:** (PIC 9(02)) Day
    *   **B-COV-CHARGES:** (PIC 9(07)V9(02)) Covered charges.
    *   **B-SPEC-PAY-IND:** (PIC X(01)) Special payment indicator.
    *   **FILLER:** (PIC X(13)) Unused space.

```cobol
01  PPS-DATA-ALL.
    05  PPS-RTC                       PIC 9(02).
    05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02).
    05  PPS-DATA.
        10  PPS-MSA                   PIC X(04).
        10  PPS-WAGE-INDEX            PIC 9(02)V9(04).
        10  PPS-AVG-LOS               PIC 9(02)V9(01).
        10  PPS-RELATIVE-WGT          PIC 9(01)V9(04).
        10  PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02).
        10  PPS-LOS                   PIC 9(03).
        10  PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02).
        10  PPS-FED-PAY-AMT           PIC 9(07)V9(02).
        10  PPS-FINAL-PAY-AMT         PIC 9(07)V9(02).
        10  PPS-FAC-COSTS             PIC 9(07)V9(02).
        10  PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02).
        10  PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02).
        10  PPS-SUBM-DRG-CODE         PIC X(03).
        10  PPS-CALC-VERS-CD          PIC X(05).
        10  PPS-REG-DAYS-USED         PIC 9(03).
        10  PPS-LTR-DAYS-USED         PIC 9(03).
        10  PPS-BLEND-YEAR            PIC 9(01).
        10  PPS-COLA                  PIC 9(01)V9(03).
        10  FILLER                    PIC X(04).
    05  PPS-OTHER-DATA.
        10  PPS-NAT-LABOR-PCT         PIC 9(01)V9(05).
        10  PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(0