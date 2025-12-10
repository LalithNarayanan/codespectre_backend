Here's an analysis of the provided COBOL programs, formatted in markdown:

### Program: LTCAL032

*   **File Accesses:**
    *   No explicit file accesses are defined in the `FILE-CONTROL` section.  The program likely relies on data passed via the `LINKAGE SECTION` and potentially uses the `COPY` statement to include data structures from other sources.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description:  A literal string used for internal program identification or debugging purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`
        *   Description:  A group of variables to hold intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of stay
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days
        *   `H-SSOT` PIC 9(02).
            *   Description: Short stay outlier threshold
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Blend return code
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend facility rate
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend PPS rate
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount for outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  This structure is passed *into* the program and contains the bill-related data.
        *   `B-NPI10`
            *   `B-NPI8` PIC X(08).
                *   Description:  National Provider Identifier (NPI) - first 8 characters.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  National Provider Identifier (NPI) - last 2 characters.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient status code.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of stay.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve days.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Discharge Century
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Discharge Year
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Discharge Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Discharge Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special payment indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused filler.
    *   `PPS-DATA-ALL`
        *   Description: Structure to pass and return PPS Calculation data
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code from the PPS calculation.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold
        *   `PPS-DATA`
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier payment amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal payment amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final payment amount (returned).
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG Code
               *   `PPS-CALC-VERS-CD`  PIC X(05).
                   *   Description:  Calculation Version Code
               *   `PPS-REG-DAYS-USED` PIC 9(03).
                   *   Description:  Regular Days Used
               *   `PPS-LTR-DAYS-USED` PIC 9(03).
                   *   Description:  Lifetime Reserve Days Used
               *   `PPS-BLEND-YEAR`  PIC 9(01).
                   *   Description:  Blend Year
               *   `PPS-COLA`  PIC 9(01)V9(03).
                   *   Description:  COLA
        *   `FILLER` PIC X(04).
            *   Description: Filler
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Switch to indicate whether all the tables are passed or just the provider record
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch
                *   88  ALL-TABLES-PASSED VALUE 'A'.
                    *   Description: All tables are passed
                *   88  PROV-RECORD-PASSED VALUE 'P'.
                    *   Description: Provider record is passed
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the pricing program
    *   `PROV-NEW-HOLD`
        *   Description:  This structure is passed *into* the program and contains the Provider data.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  New NPI
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  Filler for NPI
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description:  State
                *   `FILLER` PIC X(04).
                    *   Description:  Filler
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date Century
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date Year
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date Month
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: FY Begin Date Century
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: FY Begin Date Year
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: FY Begin Date Month
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: FY Begin Date Day
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date Century
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date Year
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date Month
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date Day
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination Date Century
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination Date Year
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination Date Month
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination Date Day
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   88 P-NEW-WAIVER-STATE VALUE 'Y'.
                    *   Description: Waiver State
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Intern Number
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Census Division
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Census Division
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geo Location MSA
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description: Geo Location MSA
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   88  P-NEW-STD-RURAL-CHECK VALUE '  '.
                                *   Description:  Rural Check
                        *   Description:  Rural
                    *   `P-NEW-RURAL-2ND` PIC XX.
                        *   Description:  Rural
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sol Com Dep Hosp Year
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator
            *   `FILLER` PIC X(05).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                    *   Description: Facility Specific Rate
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                    *   Description: COLA
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                    *   Description: Intern Ratio
                *   `P-NEW-BED-SIZE` PIC 9(05).
                    *   Description: Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                    *   Description: Operating Cost to Charge Ratio
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                    *   Description: CMI
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                    *   Description: SSI Ratio
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                    *   Description: Medicaid Ratio
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                    *   Description: PPS Blend Year Indicator
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                    *   Description: PRUF Update Factor
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                    *   Description: DSH Percentage
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: FYE Date
            *   `FILLER` PIC X(23).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD3`
            *   `P-NEW-PASS-AMT-DATA`
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description: Passed Amount Capital
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description: Passed Amount Dir Med Ed
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description: Passed Amount Organ Acq
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description: Passed Amount Plus Misc
            *   `P-NEW-CAPI-DATA`
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   Description: Capi PPS Pay Code
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   Description: Capi Hosp Spec Rate
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   Description: Capi Old Harm Rate
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   Description: Capi New Harm Ratio
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   Description: Capi Cost Charge Ratio
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   Description: Capi New Hosp
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   Description: Capi IME
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                    *   Description: Capi Exceptions
            *   `FILLER` PIC X(22).
                *   Description: Filler
    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This structure is passed *into* the program and contains the Wage Index data.
        *   `W-MSA` PIC X(4).
            *   Description: MSA code.
        *   `W-EFF-DATE` PIC X(8).
            *   Description: Effective date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
            *   Description: Wage Index 1.
            *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
                *   Description: Wage Index 2
                *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
                    *   Description: Wage Index 3

### Program: LTCAL042

*   **File Accesses:**
    *   No explicit file accesses are defined in the `FILE-CONTROL` section.  The program likely relies on data passed via the `LINKAGE SECTION` and potentially uses the `COPY` statement to include data structures from other sources.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal program identification or debugging purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`
        *   Description: A group of variables to hold intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of stay
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days
        *   `H-SSOT` PIC 9(02).
            *   Description: Short stay outlier threshold
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Blend return code
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend facility rate
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend PPS rate
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount for outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description: Length of Stay Ratio

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  This structure is passed *into* the program and contains the bill-related data.
        *   `B-NPI10`
            *   `B-NPI8` PIC X(08).
                *   Description:  National Provider Identifier (NPI) - first 8 characters.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  National Provider Identifier (NPI) - last 2 characters.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient status code.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of stay.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve days.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Discharge Century
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Discharge Year
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Discharge Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Discharge Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special payment indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused filler.
    *   `PPS-DATA-ALL`
        *   Description: Structure to pass and return PPS Calculation data
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code from the PPS calculation.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold
        *   `PPS-DATA`
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier payment amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal payment amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final payment amount (returned).
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG Code
               *   `PPS-CALC-VERS-CD`  PIC X(05).
                   *   Description:  Calculation Version Code
               *   `PPS-REG-DAYS-USED` PIC 9(03).
                   *   Description:  Regular Days Used
               *   `PPS-LTR-DAYS-USED` PIC 9(03).
                   *   Description:  Lifetime Reserve Days Used
               *   `PPS-BLEND-YEAR`  PIC 9(01).
                   *   Description:  Blend Year
               *   `PPS-COLA`  PIC 9(01)V9(03).
                   *   Description:  COLA
        *   `FILLER` PIC X(04).
            *   Description: Filler
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Switch to indicate whether all the tables are passed or just the provider record
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch
                *   88  ALL-TABLES-PASSED VALUE 'A'.
                    *   Description: All tables are passed
                *   88  PROV-RECORD-PASSED VALUE 'P'.
                    *   Description: Provider record is passed
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the pricing program
    *   `PROV-NEW-HOLD`
        *   Description:  This structure is passed *into* the program and contains the Provider data.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  New NPI
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  Filler for NPI
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description:  State
                *   `FILLER` PIC X(04).
                    *   Description:  Filler
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date Century
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date Year
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date Month
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: FY Begin Date Century
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: FY Begin Date Year
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: FY Begin Date Month
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: FY Begin Date Day
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date Century
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date Year
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date Month
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date Day
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination Date Century
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination Date Year
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination Date Month
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination Date Day
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   88 P-NEW-WAIVER-STATE VALUE 'Y'.
                    *   Description: Waiver State
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Intern Number
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Census Division
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Census Division
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geo Location