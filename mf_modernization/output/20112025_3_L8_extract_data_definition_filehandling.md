## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement to include `LTDRG031`. This indicates that `LTDRG031` likely contains data that the program needs to access.
*   **Data Structures (WORKING-STORAGE SECTION):**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A character field used for internal program identification or debugging purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` (Defined through the `COPY` statement and further defined in the program)
        *   Description:  A group of variables to hold various components used in the PPS (Prospective Payment System) calculations.
        *   Subfields:
            *   `H-LOS` PIC 9(03).: Length of Stay
            *   `H-REG-DAYS` PIC 9(03).: Regular Days
            *   `H-TOTAL-DAYS` PIC 9(05).: Total Days
            *   `H-SSOT` PIC 9(02).:
            *   `H-BLEND-RTC` PIC 9(02).:
            *   `H-BLEND-FAC` PIC 9(01)V9(01).:
            *   `H-BLEND-PPS` PIC 9(01)V9(01).:
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02).: Short Stay Pay Amount
            *   `H-SS-COST` PIC 9(07)V9(02).: Short Stay Cost
            *   `H-LABOR-PORTION` PIC 9(07)V9(06).: Labor portion of payment
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).: Non-labor portion of payment
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
    *   Variables defined within the `COPY` member (`LTDRG031`)
        *   Description: This section likely defines the DRG (Diagnosis Related Group) table.  The specific fields are not visible in this program but are defined in `LTDRG031`.
*   **Data Structures (LINKAGE SECTION):**

    *   `BILL-NEW-DATA`
        *   Description:  This data structure represents the input bill data passed to the program.
        *   Subfields:
            *   `B-NPI10`:
                *   `B-NPI8` PIC X(08).: NPI (National Provider Identifier) - first 8 characters
                *   `B-NPI-FILLER` PIC X(02).: NPI - last 2 characters
            *   `B-PROVIDER-NO` PIC X(06).: Provider Number
            *   `B-PATIENT-STATUS` PIC X(02).: Patient Status
            *   `B-DRG-CODE` PIC X(03).: DRG Code
            *   `B-LOS` PIC 9(03).: Length of Stay
            *   `B-COV-DAYS` PIC 9(03).: Covered Days
            *   `B-LTR-DAYS` PIC 9(02).: Lifetime Reserve Days
            *   `B-DISCHARGE-DATE`:
                *   `B-DISCHG-CC` PIC 9(02).: Discharge Date - Century
                *   `B-DISCHG-YY` PIC 9(02).: Discharge Date - Year
                *   `B-DISCHG-MM` PIC 9(02).: Discharge Date - Month
                *   `B-DISCHG-DD` PIC 9(02).: Discharge Date - Day
            *   `B-COV-CHARGES` PIC 9(07)V9(02).: Covered Charges
            *   `B-SPEC-PAY-IND` PIC X(01).: Special Payment Indicator
            *   `FILLER` PIC X(13).: Filler
    *   `PPS-DATA-ALL`
        *   Description:  This data structure holds the calculated PPS data returned from the program.
        *   Subfields:
            *   `PPS-RTC` PIC 9(02).: Return Code
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).: Charge Threshold
            *   `PPS-DATA`:
                *   `PPS-MSA` PIC X(04).: MSA (Metropolitan Statistical Area)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).: Wage Index
                *   `PPS-AVG-LOS` PIC 9(02)V9(01).: Average Length of Stay
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).: Relative Weight
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).: Outlier Payment Amount
                *   `PPS-LOS` PIC 9(03).: Length of Stay
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).: DRG Adjusted Payment Amount
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).: Federal Payment Amount
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).: Final Payment Amount
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02).: Facility Costs
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).: Outlier Threshold
                *   `PPS-SUBM-DRG-CODE` PIC X(03).: Submitted DRG Code
                *   `PPS-CALC-VERS-CD` PIC X(05).: Calculation Version Code
                *   `PPS-REG-DAYS-USED` PIC 9(03).: Regular Days Used
                *   `PPS-LTR-DAYS-USED` PIC 9(03).: Lifetime Reserve Days Used
                *   `PPS-BLEND-YEAR` PIC 9(01).: Blend Year
                *   `PPS-COLA` PIC 9(01)V9(03).: COLA (Cost of Living Adjustment)
                *   `FILLER` PIC X(04).: Filler
            *   `PPS-OTHER-DATA`:
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).: National Labor Percentage
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).: National Non-Labor Percentage
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).: Standard Federal Rate
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).: Budget Neutrality Rate
                *   `FILLER` PIC X(20).: Filler
            *   `PPS-PC-DATA`:
                *   `PPS-COT-IND` PIC X(01).: Cost Outlier Indicator
                *   `FILLER` PIC X(20).: Filler
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Used to pass pricer option and version information
        *   Subfields:
            *   `PRICER-OPTION-SW` PIC X(01).: Pricer Option Switch.
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   `PROV-RECORD-PASSED` VALUE 'P'.
            *   `PPS-VERSIONS`:
                *   `PPDRV-VERSION` PIC X(05).: Version of the DRG program
    *   `PROV-NEW-HOLD`
        *   Description:  This data structure represents the provider record passed to the program.
        *   Subfields:
            *   `PROV-NEWREC-HOLD1`:
                *   `P-NEW-NPI10`:
                    *   `P-NEW-NPI8` PIC X(08).: NPI - first 8 characters
                    *   `P-NEW-NPI-FILLER` PIC X(02).: NPI - last 2 characters
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02).: Provider State
                    *   `FILLER` PIC X(04).: Filler
                *   `P-NEW-DATE-DATA`:
                    *   `P-NEW-EFF-DATE`:
                        *   `P-NEW-EFF-DT-CC` PIC 9(02).: Effective Date - Century
                        *   `P-NEW-EFF-DT-YY` PIC 9(02).: Effective Date - Year
                        *   `P-NEW-EFF-DT-MM` PIC 9(02).: Effective Date - Month
                        *   `P-NEW-EFF-DT-DD` PIC 9(02).: Effective Date - Day
                    *   `P-NEW-FY-BEGIN-DATE`:
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).: Fiscal Year Begin Date - Century
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).: Fiscal Year Begin Date - Year
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).: Fiscal Year Begin Date - Month
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).: Fiscal Year Begin Date - Day
                    *   `P-NEW-REPORT-DATE`:
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02).: Report Date - Century
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02).: Report Date - Year
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02).: Report Date - Month
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02).: Report Date - Day
                    *   `P-NEW-TERMINATION-DATE`:
                        *   `P-NEW-TERM-DT-CC` PIC 9(02).: Termination Date - Century
                        *   `P-NEW-TERM-DT-YY` PIC 9(02).: Termination Date - Year
                        *   `P-NEW-TERM-DT-MM` PIC 9(02).: Termination Date - Month
                        *   `P-NEW-TERM-DT-DD` PIC 9(02).: Termination Date - Day
                *   `P-NEW-WAIVER-CODE` PIC X(01).: Waiver Code
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                *   `P-NEW-INTER-NO` PIC 9(05).: Internal Number
                *   `P-NEW-PROVIDER-TYPE` PIC X(02).: Provider Type
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).: Current Census Division
                *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   `P-NEW-MSA-DATA`:
                    *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                        *   `P-NEW-RURAL-1ST`:
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                            *   `P-NEW-RURAL-2ND` PIC XX.
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   `P-NEW-LUGAR` PIC X.
                *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   `FILLER` PIC X(05).: Filler
            *   `PROV-NEWREC-HOLD2`:
                *   `P-NEW-VARIABLES`:
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).: Facility Specific Rate
                    *   `P-NEW-COLA` PIC 9(01)V9(03).: COLA
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).: Intern Ratio
                    *   `P-NEW-BED-SIZE` PIC 9(05).: Bed Size
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).: Operating Cost to Charge Ratio
                    *   `P-NEW-CMI` PIC 9(01)V9(04).: CMI
                    *   `P-NEW-SSI-RATIO` PIC V9(04).: SSI Ratio
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04).: Medicaid Ratio
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).: PPS Blend Year Indicator
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).: Pruf Update Factor
                    *   `P-NEW-DSH-PERCENT` PIC V9(04).: DSH Percentage
                    *   `P-NEW-FYE-DATE` PIC X(08).: Fiscal Year End Date
                *   `FILLER` PIC X(23).: Filler
            *   `PROV-NEWREC-HOLD3`:
                *   `P-NEW-PASS-AMT-DATA`:
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                *   `P-NEW-CAPI-DATA`:
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                *   `FILLER` PIC X(22).: Filler
    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This data structure represents the wage index record passed to the program.
        *   Subfields:
            *   `W-MSA` PIC X(4).: MSA
            *   `W-EFF-DATE` PIC X(8).: Effective Date
            *   `W-WAGE-INDEX1` PIC S9(02)V9(04).: Wage Index 1
            *   `W-WAGE-INDEX2` PIC S9(02)V9(04).: Wage Index 2
            *   `W-WAGE-INDEX3` PIC S9(02)V9(04).: Wage Index 3

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement to include `LTDRG031`. This indicates that `LTDRG031` likely contains data that the program needs to access.
*   **Data Structures (WORKING-STORAGE SECTION):**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A character field used for internal program identification or debugging purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` (Defined through the `COPY` statement and further defined in the program)
        *   Description:  A group of variables to hold various components used in the PPS (Prospective Payment System) calculations.
        *   Subfields:
            *   `H-LOS` PIC 9(03).: Length of Stay
            *   `H-REG-DAYS` PIC 9(03).: Regular Days
            *   `H-TOTAL-DAYS` PIC 9(05).: Total Days
            *   `H-SSOT` PIC 9(02).:
            *   `H-BLEND-RTC` PIC 9(02).:
            *   `H-BLEND-FAC` PIC 9(01)V9(01).:
            *   `H-BLEND-PPS` PIC 9(01)V9(01).:
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02).: Short Stay Pay Amount
            *   `H-SS-COST` PIC 9(07)V9(02).: Short Stay Cost
            *   `H-LABOR-PORTION` PIC 9(07)V9(06).: Labor portion of payment
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).: Non-labor portion of payment
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   `H-LOS-RATIO` PIC 9(01)V9(05).
    *   Variables defined within the `COPY` member (`LTDRG031`)
        *   Description: This section likely defines the DRG (Diagnosis Related Group) table.  The specific fields are not visible in this program but are defined in `LTDRG031`.
*   **Data Structures (LINKAGE SECTION):**

    *   `BILL-NEW-DATA`
        *   Description:  This data structure represents the input bill data passed to the program.
        *   Subfields:
            *   `B-NPI10`:
                *   `B-NPI8` PIC X(08).: NPI (National Provider Identifier) - first 8 characters
                *   `B-NPI-FILLER` PIC X(02).: NPI - last 2 characters
            *   `B-PROVIDER-NO` PIC X(06).: Provider Number
            *   `B-PATIENT-STATUS` PIC X(02).: Patient Status
            *   `B-DRG-CODE` PIC X(03).: DRG Code
            *   `B-LOS` PIC 9(03).: Length of Stay
            *   `B-COV-DAYS` PIC 9(03).: Covered Days
            *   `B-LTR-DAYS` PIC 9(02).: Lifetime Reserve Days
            *   `B-DISCHARGE-DATE`:
                *   `B-DISCHG-CC` PIC 9(02).: Discharge Date - Century
                *   `B-DISCHG-YY` PIC 9(02).: Discharge Date - Year
                *   `B-DISCHG-MM` PIC 9(02).: Discharge Date - Month
                *   `B-DISCHG-DD` PIC 9(02).: Discharge Date - Day
            *   `B-COV-CHARGES` PIC 9(07)V9(02).: Covered Charges
            *   `B-SPEC-PAY-IND` PIC X(01).: Special Payment Indicator
            *   `FILLER` PIC X(13).: Filler
    *   `PPS-DATA-ALL`
        *   Description:  This data structure holds the calculated PPS data returned from the program.
        *   Subfields:
            *   `PPS-RTC` PIC 9(02).: Return Code
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).: Charge Threshold
            *   `PPS-DATA`:
                *   `PPS-MSA` PIC X(04).: MSA (Metropolitan Statistical Area)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).: Wage Index
                *   `PPS-AVG-LOS` PIC 9(02)V9(01).: Average Length of Stay
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).: Relative Weight
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).: Outlier Payment Amount
                *   `PPS-LOS` PIC 9(03).: Length of Stay
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).: DRG Adjusted Payment Amount
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).: Federal Payment Amount
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).: Final Payment Amount
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02).: Facility Costs
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).: Outlier Threshold
                *   `PPS-SUBM-DRG-CODE` PIC X(03).: Submitted DRG Code
                *   `PPS-CALC-VERS-CD` PIC X(05).: Calculation Version Code
                *   `PPS-REG-DAYS-USED` PIC 9(03).: Regular Days Used
                *   `PPS-LTR-DAYS-USED` PIC 9(03).: Lifetime Reserve Days Used
                *   `PPS-BLEND-YEAR` PIC 9(01).: Blend Year
                *   `PPS-COLA` PIC 9(01)V9(03).: COLA (Cost of Living Adjustment)
                *   `FILLER` PIC X(04).: Filler
            *   `PPS-OTHER-DATA`:
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).: National Labor Percentage
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).: National Non-Labor Percentage
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).: Standard Federal Rate
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).: Budget Neutrality Rate
                *   `FILLER` PIC X(20).: Filler
            *   `PPS-PC-DATA`:
                *   `PPS-COT-IND` PIC X(01).: Cost Outlier Indicator
                *   `FILLER` PIC X(20).: Filler
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Used to pass pricer option and version information
        *   Subfields:
            *   `PRICER-OPTION-SW` PIC X(01).: Pricer Option Switch.
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   `PROV-RECORD-PASSED` VALUE 'P'.
            *   `PPS-VERSIONS`:
                *   `PPDRV-VERSION` PIC X(05).: Version of the DRG program
    *   `PROV-NEW-HOLD`
        *   Description:  This data structure represents the provider record passed to the program.
        *   Subfields:
            *   `PROV-NEWREC-HOLD1`:
                *   `P-NEW-NPI10`:
                    *   `P-NEW-NPI8` PIC X(08).: NPI - first 8 characters
                    *   `P-NEW-NPI-FILLER` PIC X(02).: NPI - last 2 characters
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02).: Provider State
                    *   `FILLER` PIC X(04).: Filler
                *   `P-NEW-DATE-DATA`:
                    *   `P-NEW-EFF-DATE`:
                        *   `P-NEW-EFF-DT-CC` PIC 9(02).: Effective Date - Century
                        *   `P-NEW-EFF-DT-YY` PIC 9(02).: Effective Date - Year
                        *   `P-NEW-EFF-DT-MM` PIC 9(02).: Effective Date - Month
                        *   `P-NEW-EFF-DT-DD` PIC 9(02).: Effective Date - Day
                    *   `P-NEW-FY-BEGIN-DATE`:
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).: Fiscal Year Begin Date - Century
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).: Fiscal Year Begin Date - Year
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).: Fiscal Year Begin Date - Month
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).: Fiscal Year Begin Date - Day
                    *   `P-NEW-REPORT-DATE`:
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02).: Report Date - Century
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02).: Report Date - Year
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02).: Report Date - Month
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02).: Report Date - Day
                    *   `P-NEW-TERMINATION-DATE`:
                        *   `P-NEW-TERM-DT-CC` PIC 9(02).: Termination Date - Century
                        *   `P-NEW-TERM-DT-YY` PIC 9(02).: Termination Date - Year
                        *   `P-NEW-TERM-DT-MM` PIC 9(02).: Termination Date - Month
                        *   `P-NEW-TERM-DT-DD` PIC 9(02).: Termination Date - Day
                *   `P-NEW-WAIVER-CODE` PIC X(01).: Waiver Code
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                *   `P-NEW-INTER-NO` PIC 9(05).: Internal Number
                *   `P-NEW-PROVIDER-TYPE` PIC X(02).: Provider Type
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).: Current Census Division
                *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   `P-NEW-MSA-DATA`:
                    *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                        *   `P-NEW-RURAL-1ST`:
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                            *   `P-NEW-RURAL-2ND` PIC XX.
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   `P-NEW-LUGAR` PIC X.
                *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   `FILLER` PIC X(05).: Filler
            *   `PROV-NEWREC-HOLD2`:
                *   `P-NEW-VARIABLES`:
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).: Facility Specific Rate
                    *   `P-NEW-COLA` PIC 9(01)V9(03).: COLA
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).: Intern Ratio
                    *   `P-NEW-BED-SIZE` PIC 9(05).: Bed Size
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).: Operating Cost to Charge Ratio
                    *   `P-NEW-CMI` PIC 9(01)V9(04).: CMI
                    *   `P-NEW-SSI-RATIO` PIC V9(04).: SSI Ratio
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04).: Medicaid Ratio
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).: PPS Blend Year Indicator
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).: Pruf Update Factor
                    *   `P-NEW-DSH-PERCENT` PIC V9(04).: DSH Percentage
                    *   `P-NEW-FYE-DATE` PIC X(08).: Fiscal Year End Date
                *   `FILLER` PIC X(23).: Filler
            *   `PROV-NEWREC-HOLD3`:
                *   `P-NEW-PASS-AMT-DATA`:
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                *   `P-NEW-CAPI-DATA`:
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                *   `FILLER` PIC X(22).: Filler
    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This data structure represents the wage index record passed to the program.
        *   Subfields: