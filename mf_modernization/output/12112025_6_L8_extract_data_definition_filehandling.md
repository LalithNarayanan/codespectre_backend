Here's the analysis of each COBOL program you provided:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, it's highly likely that this program interacts with external data through:
        *   **COPY LTDRG031:** This implies that the program includes a COBOL copybook named `LTDRG031`. This copybook likely contains data structures (tables, records) needed for DRG calculations.  This is a form of data access, as the program is incorporating external data definitions.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'.
        *   Description:  A literal string used for internal program identification/debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Stores the version of the calculation logic (likely related to the effective date).
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS) - Input from BILL-NEW-DATA.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular Days (Covered Days - LTR Days)
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total Days (Regular Days + LTR Days)
        *   `H-SSOT` PIC 9(02).
            *   Description:  Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return Code adjustment for blended payments.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description:  Factor for facility portion of blended payments.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description:  Factor for PPS (DRG) portion of blended payments.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description:  Short Stay Payment Amount (calculated).
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description:  Short Stay Cost (calculated).
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description:  Labor portion of the payment (calculated).
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description:  Non-labor portion of the payment (calculated).
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description:  Fixed loss amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description:  New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the input data structure passed to the program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08).
                *   Description:  National Provider Identifier (NPI) - first 8 digits.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description:  Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description:  Patient Status code.
        *   `B-DRG-CODE` PIC X(03).
            *   Description:  Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description:  Length of Stay (LOS).
        *   `B-COV-DAYS` PIC 9(03).
            *   Description:  Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description:  Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description:  Discharge Date - Century/Control Code.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description:  Discharge Date - Year.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description:  Discharge Date - Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description:  Discharge Date - Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description:  Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description:  Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description:  Unused area.
    *   `PPS-DATA-ALL`:  This is the data structure passed back to the calling program.  It contains the calculated results.
        *   `PPS-RTC` PIC 9(02).
            *   Description:  Return Code (indicates payment type or error).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description:  Charge Threshold for outlier calculations.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description:  Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description:  Average Length of Stay (from DRG table).
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description:  Relative Weight (from DRG table).
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Outlier Payment Amount (calculated).
            *   `PPS-LOS` PIC 9(03).
                *   Description:  Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  DRG Adjusted Payment Amount (calculated).
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Federal Payment Amount (calculated).
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Final Payment Amount (calculated).
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description:  Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description:  New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description:  Outlier Threshold (calculated).
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description:  Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description:  Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description:  Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description:  Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description:  Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description:  Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description:  Unused area.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description:  National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description:  National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description:  Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description:  Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description:  Unused area.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01).
                *   Description:  Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description:  Unused area.
    *   `PRICER-OPT-VERS-SW`:
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description:  Switch indicating which data is passed back.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description:  Indicates all tables were passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description:  Indicates Provider record was passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
                *   Description:  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure holds provider-specific information.
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  NPI - First 8 digits
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  NPI Filler
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century/Control Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century/Control Code.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Day.
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date - Century/Control Code.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date - Year.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date - Month.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date - Day.
                *   `P-NEW-TERMINATION-DATE`:
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination Date - Century/Control Code.
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination Date - Year.
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination Date - Month.
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination Date - Day.
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   Description: Waiver Code
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                    *   Description: Waiver State
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Intern Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Current Division.
            *   `P-NEW-MSA-DATA`:
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description:  Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description:  Geographic Location MSA (alphanumeric).
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description:  Geographic Location MSA (numeric).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description:  Wage Index Location MSA (alphanumeric).
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description:  Standard Amount Location MSA (alphanumeric).
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   Description:  Standard Amount Location MSA (numeric).
                        *   `P-NEW-RURAL-1ST`:
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   Description: Standard Rural.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                    *   Description: Standard Rural Check
                            *   `P-NEW-RURAL-2ND` PIC XX.
                                *   Description: Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                    *   Description: Facility Specific Rate
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                    *   Description: Cost of Living Adjustment (COLA).
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                    *   Description: Intern Ratio
                *   `P-NEW-BED-SIZE` PIC 9(05).
                    *   Description: Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                    *   Description: Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                    *   Description: Case Mix Index (CMI).
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                    *   Description: Supplemental Security Income (SSI) Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                    *   Description: Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                    *   Description: PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                    *   Description: PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                    *   Description: Disproportionate Share Hospital (DSH) Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: Fiscal Year End Date.
            *   `FILLER` PIC X(23).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description:  Pass Through Amount - Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description:  Pass Through Amount - Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description:  Pass Through Amount - Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description:  Pass Through Amount - Plus Miscellaneous.
            *   `P-NEW-CAPI-DATA`:
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   Description:  Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   Description:  Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   Description:  Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   Description:  Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   Description:  Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   Description:  Capital New Hospital.
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   Description:  Capital Indirect Medical Education (IME).
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                    *   Description:  Capital Exceptions.
            *   `FILLER` PIC X(22).
                *   Description: Filler
    *   `WAGE-NEW-INDEX-RECORD`:  This structure holds wage index information.
        *   `W-MSA` PIC X(4).
            *   Description:  MSA (Metropolitan Statistical Area) code.
        *   `W-EFF-DATE` PIC X(8).
            *   Description:  Effective Date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
            *   Description:  Wage Index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
            *   Description:  Wage Index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
            *   Description:  Wage Index 3.

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, it's highly likely that this program interacts with external data through:
        *   **COPY LTDRG031:** This implies that the program includes a COBOL copybook named `LTDRG031`. This copybook likely contains data structures (tables, records) needed for DRG calculations.  This is a form of data access, as the program is incorporating external data definitions.

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'.
        *   Description:  A literal string used for internal program identification/debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description:  Stores the version of the calculation logic (likely related to the effective date).
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS) - Input from BILL-NEW-DATA.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular Days (Covered Days - LTR Days)
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total Days (Regular Days + LTR Days)
        *   `H-SSOT` PIC 9(02).
            *   Description:  Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return Code adjustment for blended payments.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description:  Factor for facility portion of blended payments.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description:  Factor for PPS (DRG) portion of blended payments.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description:  Short Stay Payment Amount (calculated).
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description:  Short Stay Cost (calculated).
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description:  Labor portion of the payment (calculated).
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description:  Non-labor portion of the payment (calculated).
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description:  Fixed loss amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description:  New Facility Specific Rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description: Ratio of LOS to Average LOS.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the input data structure passed to the program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08).
                *   Description:  National Provider Identifier (NPI) - first 8 digits.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description:  Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description:  Patient Status code.
        *   `B-DRG-CODE` PIC X(03).
            *   Description:  Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description:  Length of Stay (LOS).
        *   `B-COV-DAYS` PIC 9(03).
            *   Description:  Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description:  Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description:  Discharge Date - Century/Control Code.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description:  Discharge Date - Year.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description:  Discharge Date - Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description:  Discharge Date - Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description:  Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description:  Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description:  Unused area.
    *   `PPS-DATA-ALL`:  This is the data structure passed back to the calling program.  It contains the calculated results.
        *   `PPS-RTC` PIC 9(02).
            *   Description:  Return Code (indicates payment type or error).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description:  Charge Threshold for outlier calculations.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description:  Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description:  Average Length of Stay (from DRG table).
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description:  Relative Weight (from DRG table).
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Outlier Payment Amount (calculated).
            *   `PPS-LOS` PIC 9(03).
                *   Description:  Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  DRG Adjusted Payment Amount (calculated).
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Federal Payment Amount (calculated).
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description:  Final Payment Amount (calculated).
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description:  Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description:  New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description:  Outlier Threshold (calculated).
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description:  Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description:  Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description:  Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description:  Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description:  Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description:  Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description:  Unused area.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description:  National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description:  National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description:  Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description:  Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description:  Unused area.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01).
                *   Description:  Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description:  Unused area.
    *   `PRICER-OPT-VERS-SW`:
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description:  Switch indicating which data is passed back.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description:  Indicates all tables were passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description:  Indicates Provider record was passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
                *   Description:  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure holds provider-specific information.
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  NPI - First 8 digits
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  NPI Filler
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century/Control Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century/Control Code.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Day.
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date - Century/Control