Here's an analysis of the provided COBOL programs, detailing file access, data structures, and their descriptions:

**Program: LTCAL032**

*   **Files Accessed:**

    *   None Explicitly (Uses a COPY member)

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description:  A literal string, likely used for debugging or program identification.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`: (Defined via COPY LTDRG031)
        *   Description:  This group of variables appears to hold intermediate calculation results or components related to the Prospective Payment System (PPS) for Long-Term Care (LTC) DRG calculations.
            *   `H-LOS` PIC 9(03):  Length of Stay (LOS) - Integer, three digits.
            *   `H-REG-DAYS` PIC 9(03): Regular Days - Integer, three digits.
            *   `H-TOTAL-DAYS` PIC 9(05):  Total Days - Integer, five digits.
            *   `H-SSOT` PIC 9(02):  Short Stay Outlier Threshold - Integer, two digits.
            *   `H-BLEND-RTC` PIC 9(02):  Blend Return Code - Integer, two digits.
            *   `H-BLEND-FAC` PIC 9(01)V9(01):  Blend Facility Portion - Decimal, two digits (one before the decimal, one after).
            *   `H-BLEND-PPS` PIC 9(01)V9(01):  Blend PPS Portion - Decimal, two digits (one before the decimal, one after).
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02):  Short Stay Payment Amount - Decimal, nine digits (seven before the decimal, two after).
            *   `H-SS-COST` PIC 9(07)V9(02):  Short Stay Cost - Decimal, nine digits (seven before the decimal, two after).
            *   `H-LABOR-PORTION` PIC 9(07)V9(06):  Labor Portion - Decimal, thirteen digits (seven before the decimal, six after).
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06):  Non-Labor Portion - Decimal, thirteen digits (seven before the decimal, six after).
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02):  Fixed Loss Amount - Decimal, nine digits (seven before the decimal, two after).
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02): New Facility Specific Rate - Decimal, seven digits (five before the decimal, two after).

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:
        *   Description:  This is the main input data structure, representing a bill or claim record passed *into* the LTCAL032 subroutine.
            *   `B-NPI10`:
                *   `B-NPI8` PIC X(08):  National Provider Identifier (NPI) - 8 characters.
                *   `B-NPI-FILLER` PIC X(02):  Filler for NPI - 2 characters.
            *   `B-PROVIDER-NO` PIC X(06):  Provider Number - 6 characters.
            *   `B-PATIENT-STATUS` PIC X(02):  Patient Status - 2 characters.
            *   `B-DRG-CODE` PIC X(03):  Diagnosis Related Group (DRG) Code - 3 characters.
            *   `B-LOS` PIC 9(03):  Length of Stay - Integer, three digits.
            *   `B-COV-DAYS` PIC 9(03):  Covered Days - Integer, three digits.
            *   `B-LTR-DAYS` PIC 9(02):  Lifetime Reserve Days - Integer, two digits.
            *   `B-DISCHARGE-DATE`:
                *   `B-DISCHG-CC` PIC 9(02):  Discharge Century/Year - Integer, two digits.
                *   `B-DISCHG-YY` PIC 9(02):  Discharge Year - Integer, two digits.
                *   `B-DISCHG-MM` PIC 9(02):  Discharge Month - Integer, two digits.
                *   `B-DISCHG-DD` PIC 9(02):  Discharge Day - Integer, two digits.
            *   `B-COV-CHARGES` PIC 9(07)V9(02):  Covered Charges - Decimal, nine digits (seven before the decimal, two after).
            *   `B-SPEC-PAY-IND` PIC X(01):  Special Payment Indicator - 1 character.
            *   `FILLER` PIC X(13):  Filler - 13 characters.
    *   `PPS-DATA-ALL`:
        *   Description:  This structure is used to pass data *back* to the calling program, containing the results of the PPS calculation.
            *   `PPS-RTC` PIC 9(02):  Return Code - Integer, two digits. Indicates the outcome of the calculation (e.g., normal payment, outlier, error).
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02):  Charge Threshold - Decimal, nine digits (seven before the decimal, two after).
            *   `PPS-DATA`:
                *   `PPS-MSA` PIC X(04):  Metropolitan Statistical Area (MSA) - 4 characters.
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04):  Wage Index - Decimal, six digits (two before the decimal, four after).
                *   `PPS-AVG-LOS` PIC 9(02)V9(01):  Average Length of Stay - Decimal, three digits (two before the decimal, one after).
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04):  Relative Weight - Decimal, five digits (one before the decimal, four after).
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02):  Outlier Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-LOS` PIC 9(03):  Length of Stay - Integer, three digits.
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02):  DRG Adjusted Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02):  Federal Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02):  Final Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02):  Facility Costs - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02): New Facility Specific Rate - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02): Outlier Threshold - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-SUBM-DRG-CODE` PIC X(03):  Submitted DRG Code - 3 characters.
                *   `PPS-CALC-VERS-CD` PIC X(05): Calculation Version Code - 5 characters.
                *   `PPS-REG-DAYS-USED` PIC 9(03): Regular Days Used - Integer, three digits.
                *   `PPS-LTR-DAYS-USED` PIC 9(03): Lifetime Reserve Days Used - Integer, three digits.
                *   `PPS-BLEND-YEAR` PIC 9(01): Blend Year - Integer, one digit.
                *   `PPS-COLA` PIC 9(01)V9(03):  Cost of Living Adjustment (COLA) - Decimal, four digits (one before the decimal, three after).
                *   `FILLER` PIC X(04): Filler - 4 characters.
            *   `PPS-OTHER-DATA`:
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05):  National Labor Percentage - Decimal, six digits (one before the decimal, five after).
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05):  National Non-Labor Percentage - Decimal, six digits (one before the decimal, five after).
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02):  Standard Federal Rate - Decimal, seven digits (five before the decimal, two after).
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03):  Budget Neutrality Rate - Decimal, four digits (one before the decimal, three after).
                *   `FILLER` PIC X(20): Filler - 20 characters.
            *   `PPS-PC-DATA`:
                *   `PPS-COT-IND` PIC X(01):  Cost Outlier Indicator - 1 character.
                *   `FILLER` PIC X(20): Filler - 20 characters.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Switch to indicate if all tables or just the provider record are passed
            *   `PRICER-OPTION-SW` PIC X(01):  Pricer Option Switch - 1 character.
            *   `PPS-VERSIONS`:
                *   `PPDRV-VERSION` PIC X(05):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description:  Provider Record data, that is passed from the calling program
            *   `PROV-NEWREC-HOLD1`:
                *   `P-NEW-NPI10`:
                    *   `P-NEW-NPI8` PIC X(08):  NPI - 8 characters.
                    *   `P-NEW-NPI-FILLER` PIC X(02):  Filler for NPI - 2 characters.
                *   `P-NEW-PROVIDER-NO`:
                    *   `P-NEW-STATE` PIC 9(02):  State - Integer, two digits.
                    *   `FILLER` PIC X(04):  Filler - 4 characters.
                *   `P-NEW-DATE-DATA`:
                    *   `P-NEW-EFF-DATE`:
                        *   `P-NEW-EFF-DT-CC` PIC 9(02): Effective Date Century - Integer, two digits.
                        *   `P-NEW-EFF-DT-YY` PIC 9(02): Effective Date Year - Integer, two digits.
                        *   `P-NEW-EFF-DT-MM` PIC 9(02): Effective Date Month - Integer, two digits.
                        *   `P-NEW-EFF-DT-DD` PIC 9(02): Effective Date Day - Integer, two digits.
                    *   `P-NEW-FY-BEGIN-DATE`:
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02): Fiscal Year Begin Date Century - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02): Fiscal Year Begin Date Year - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02): Fiscal Year Begin Date Month - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02): Fiscal Year Begin Date Day - Integer, two digits.
                    *   `P-NEW-REPORT-DATE`:
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02): Report Date Century - Integer, two digits.
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02): Report Date Year - Integer, two digits.
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02): Report Date Month - Integer, two digits.
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02): Report Date Day - Integer, two digits.
                    *   `P-NEW-TERMINATION-DATE`:
                        *   `P-NEW-TERM-DT-CC` PIC 9(02): Termination Date Century - Integer, two digits.
                        *   `P-NEW-TERM-DT-YY` PIC 9(02): Termination Date Year - Integer, two digits.
                        *   `P-NEW-TERM-DT-MM` PIC 9(02): Termination Date Month - Integer, two digits.
                        *   `P-NEW-TERM-DT-DD` PIC 9(02): Termination Date Day - Integer, two digits.
                *   `P-NEW-WAIVER-CODE` PIC X(01):  Waiver Code - 1 character.
                *   `P-NEW-INTER-NO` PIC 9(05):  Internal Number - Integer, five digits.
                *   `P-NEW-PROVIDER-TYPE` PIC X(02):  Provider Type - 2 characters.
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01): Current Census Division - Integer, one digit.
                *   `P-NEW-MSA-DATA`:
                    *   `P-NEW-CHG-CODE-INDEX` PIC X: Charge Code Index - 1 character.
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04):  Geographic Location MSA - 4 characters.
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04): Wage Index Location MSA - 4 characters.
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04): Standard Amount Location MSA - 4 characters.
                    *   `P-NEW-STAND-AMT-LOC-MSA9`:
                        *   `P-NEW-RURAL-1ST`:
                            *   `P-NEW-STAND-RURAL` PIC XX: Standard Rural - 2 characters.
                        *   `P-NEW-RURAL-2ND` PIC XX: Rural - 2 characters.
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX:  Sole Community Dependent Hospital Year - 2 characters.
                *   `P-NEW-LUGAR` PIC X: Lugar - 1 character.
                *   `P-NEW-TEMP-RELIEF-IND` PIC X: Temporary Relief Indicator - 1 character.
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X: Federal PPS Blend Indicator - 1 character.
                *   `FILLER` PIC X(05): Filler - 5 characters.
            *   `PROV-NEWREC-HOLD2`:
                *   `P-NEW-VARIABLES`:
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02):  Facility Specific Rate - Decimal, seven digits (five before the decimal, two after).
                    *   `P-NEW-COLA` PIC 9(01)V9(03):  Cost of Living Adjustment - Decimal, four digits (one before the decimal, three after).
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04):  Intern Ratio - Decimal, five digits (one before the decimal, four after).
                    *   `P-NEW-BED-SIZE` PIC 9(05):  Bed Size - Integer, five digits.
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03):  Operating Cost to Charge Ratio - Decimal, four digits (one before the decimal, three after).
                    *   `P-NEW-CMI` PIC 9(01)V9(04):  Case Mix Index (CMI) - Decimal, five digits (one before the decimal, four after).
                    *   `P-NEW-SSI-RATIO` PIC V9(04):  Supplemental Security Income (SSI) Ratio - Decimal, four digits (four after the decimal).
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04):  Medicaid Ratio - Decimal, four digits (four after the decimal).
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01):  PPS Blend Year Indicator - Integer, one digit.
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05):  Pruf Update Factor - Decimal, six digits (one before the decimal, five after).
                    *   `P-NEW-DSH-PERCENT` PIC V9(04):  Disproportionate Share Hospital (DSH) Percentage - Decimal, four digits (four after the decimal).
                    *   `P-NEW-FYE-DATE` PIC X(08):  Fiscal Year End Date - 8 characters.
                *   `FILLER` PIC X(23): Filler - 23 characters.
            *   `PROV-NEWREC-HOLD3`:
                *   `P-NEW-PASS-AMT-DATA`:
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99:  Pass Through Amount - Capital - Decimal, six digits (four before the decimal, two after).
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99:  Pass Through Amount - Direct Medical Education - Decimal, six digits (four before the decimal, two after).
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99:  Pass Through Amount - Organ Acquisition - Decimal, six digits (four before the decimal, two after).
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99:  Pass Through Amount - Plus Miscellaneous - Decimal, six digits (four before the decimal, two after).
                *   `P-NEW-CAPI-DATA`:
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X:  Capital PPS Payment Code - 1 character.
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99:  Capital Hospital Specific Rate - Decimal, six digits (four before the decimal, two after).
                    *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99:  Capital Old Harm Rate - Decimal, six digits (four before the decimal, two after).
                    *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999:  Capital New Harm Ratio - Decimal, five digits (one before the decimal, four after).
                    *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999:  Capital Cost to Charge Ratio - Decimal, four digits (four after the decimal).
                    *   `P-NEW-CAPI-NEW-HOSP` PIC X:  Capital New Hospital - 1 character.
                    *   `P-NEW-CAPI-IME` PIC 9V9999:  Capital IME - Decimal, five digits (four after the decimal).
                    *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99:  Capital Exceptions - Decimal, six digits (four before the decimal, two after).
                *   `FILLER` PIC X(22): Filler - 22 characters.
    *   `WAGE-NEW-INDEX-RECORD`:
        *   Description:  Wage index record passed from the calling program
            *   `W-MSA` PIC X(4):  Wage Index MSA - 4 characters.
            *   `W-EFF-DATE` PIC X(8):  Wage Index Effective Date - 8 characters.
            *   `W-WAGE-INDEX1` PIC S9(02)V9(04):  Wage Index 1 - Signed Decimal, six digits (two before the decimal, four after).
            *   `W-WAGE-INDEX2` PIC S9(02)V9(04):  Wage Index 2 - Signed Decimal, six digits (two before the decimal, four after).
            *   `W-WAGE-INDEX3` PIC S9(02)V9(04):  Wage Index 3 - Signed Decimal, six digits (two before the decimal, four after).

**Program: LTCAL042**

*   **Files Accessed:**

    *   None Explicitly (Uses a COPY member)

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description:  A literal string, likely used for debugging or program identification.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`: (Defined via COPY LTDRG031)
        *   Description:  This group of variables appears to hold intermediate calculation results or components related to the Prospective Payment System (PPS) for Long-Term Care (LTC) DRG calculations.
            *   `H-LOS` PIC 9(03):  Length of Stay (LOS) - Integer, three digits.
            *   `H-REG-DAYS` PIC 9(03): Regular Days - Integer, three digits.
            *   `H-TOTAL-DAYS` PIC 9(05):  Total Days - Integer, five digits.
            *   `H-SSOT` PIC 9(02):  Short Stay Outlier Threshold - Integer, two digits.
            *   `H-BLEND-RTC` PIC 9(02):  Blend Return Code - Integer, two digits.
            *   `H-BLEND-FAC` PIC 9(01)V9(01):  Blend Facility Portion - Decimal, two digits (one before the decimal, one after).
            *   `H-BLEND-PPS` PIC 9(01)V9(01):  Blend PPS Portion - Decimal, two digits (one before the decimal, one after).
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02):  Short Stay Payment Amount - Decimal, nine digits (seven before the decimal, two after).
            *   `H-SS-COST` PIC 9(07)V9(02):  Short Stay Cost - Decimal, nine digits (seven before the decimal, two after).
            *   `H-LABOR-PORTION` PIC 9(07)V9(06):  Labor Portion - Decimal, thirteen digits (seven before the decimal, six after).
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06):  Non-Labor Portion - Decimal, thirteen digits (seven before the decimal, six after).
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02):  Fixed Loss Amount - Decimal, nine digits (seven before the decimal, two after).
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02): New Facility Specific Rate - Decimal, seven digits (five before the decimal, two after).
            *   `H-LOS-RATIO` PIC 9(01)V9(05):  LOS Ratio - Decimal, six digits (one before the decimal, five after).

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:
        *   Description:  This is the main input data structure, representing a bill or claim record passed *into* the LTCAL042 subroutine.
            *   `B-NPI10`:
                *   `B-NPI8` PIC X(08):  National Provider Identifier (NPI) - 8 characters.
                *   `B-NPI-FILLER` PIC X(02):  Filler for NPI - 2 characters.
            *   `B-PROVIDER-NO` PIC X(06):  Provider Number - 6 characters.
            *   `B-PATIENT-STATUS` PIC X(02):  Patient Status - 2 characters.
            *   `B-DRG-CODE` PIC X(03):  Diagnosis Related Group (DRG) Code - 3 characters.
            *   `B-LOS` PIC 9(03):  Length of Stay - Integer, three digits.
            *   `B-COV-DAYS` PIC 9(03):  Covered Days - Integer, three digits.
            *   `B-LTR-DAYS` PIC 9(02):  Lifetime Reserve Days - Integer, two digits.
            *   `B-DISCHARGE-DATE`:
                *   `B-DISCHG-CC` PIC 9(02):  Discharge Century/Year - Integer, two digits.
                *   `B-DISCHG-YY` PIC 9(02):  Discharge Year - Integer, two digits.
                *   `B-DISCHG-MM` PIC 9(02):  Discharge Month - Integer, two digits.
                *   `B-DISCHG-DD` PIC 9(02):  Discharge Day - Integer, two digits.
            *   `B-COV-CHARGES` PIC 9(07)V9(02):  Covered Charges - Decimal, nine digits (seven before the decimal, two after).
            *   `B-SPEC-PAY-IND` PIC X(01):  Special Payment Indicator - 1 character.
            *   `FILLER` PIC X(13):  Filler - 13 characters.
    *   `PPS-DATA-ALL`:
        *   Description:  This structure is used to pass data *back* to the calling program, containing the results of the PPS calculation.
            *   `PPS-RTC` PIC 9(02):  Return Code - Integer, two digits. Indicates the outcome of the calculation (e.g., normal payment, outlier, error).
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02):  Charge Threshold - Decimal, nine digits (seven before the decimal, two after).
            *   `PPS-DATA`:
                *   `PPS-MSA` PIC X(04):  Metropolitan Statistical Area (MSA) - 4 characters.
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04):  Wage Index - Decimal, six digits (two before the decimal, four after).
                *   `PPS-AVG-LOS` PIC 9(02)V9(01):  Average Length of Stay - Decimal, three digits (two before the decimal, one after).
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04):  Relative Weight - Decimal, five digits (one before the decimal, four after).
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02):  Outlier Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-LOS` PIC 9(03):  Length of Stay - Integer, three digits.
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02):  DRG Adjusted Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02):  Federal Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02):  Final Payment Amount - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02):  Facility Costs - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02): New Facility Specific Rate - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02): Outlier Threshold - Decimal, nine digits (seven before the decimal, two after).
                *   `PPS-SUBM-DRG-CODE` PIC X(03):  Submitted DRG Code - 3 characters.
                *   `PPS-CALC-VERS-CD` PIC X(05): Calculation Version Code - 5 characters.
                *   `PPS-REG-DAYS-USED` PIC 9(03): Regular Days Used - Integer, three digits.
                *   `PPS-LTR-DAYS-USED` PIC 9(03): Lifetime Reserve Days Used - Integer, three digits.
                *   `PPS-BLEND-YEAR` PIC 9(01): Blend Year - Integer, one digit.
                *   `PPS-COLA` PIC 9(01)V9(03):  Cost of Living Adjustment (COLA) - Decimal, four digits (one before the decimal, three after).
                *   `FILLER` PIC X(04): Filler - 4 characters.
            *   `PPS-OTHER-DATA`:
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05):  National Labor Percentage - Decimal, six digits (one before the decimal, five after).
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05):  National Non-Labor Percentage - Decimal, six digits (one before the decimal, five after).
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02):  Standard Federal Rate - Decimal, seven digits (five before the decimal, two after).
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03):  Budget Neutrality Rate - Decimal, four digits (one before the decimal, three after).
                *   `FILLER` PIC X(20): Filler - 20 characters.
            *   `PPS-PC-DATA`:
                *   `PPS-COT-IND` PIC X(01):  Cost Outlier Indicator - 1 character.
                *   `FILLER` PIC X(20): Filler - 20 characters.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Switch to indicate if all tables or just the provider record are passed
            *   `PRICER-OPTION-SW` PIC X(01):  Pricer Option Switch - 1 character.
            *   `PPS-VERSIONS`:
                *   `PPDRV-VERSION` PIC X(05):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description:  Provider Record data, that is passed from the calling program
            *   `PROV-NEWREC-HOLD1`:
                *   `P-NEW-NPI10`:
                    *   `P-NEW-NPI8` PIC X(08):  NPI - 8 characters.
                    *   `P-NEW-NPI-FILLER` PIC X(02):  Filler for NPI - 2 characters.
                *   `P-NEW-PROVIDER-NO`:
                    *   `P-NEW-STATE` PIC 9(02):  State - Integer, two digits.
                    *   `FILLER` PIC X(04):  Filler - 4 characters.
                *   `P-NEW-DATE-DATA`:
                    *   `P-NEW-EFF-DATE`:
                        *   `P-NEW-EFF-DT-CC` PIC 9(02): Effective Date Century - Integer, two digits.
                        *   `P-NEW-EFF-DT-YY` PIC 9(02): Effective Date Year - Integer, two digits.
                        *   `P-NEW-EFF-DT-MM` PIC 9(02): Effective Date Month - Integer, two digits.
                        *   `P-NEW-EFF-DT-DD` PIC 9(02): Effective Date Day - Integer, two digits.
                    *   `P-NEW-FY-BEGIN-DATE`:
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02): Fiscal Year Begin Date Century - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02): Fiscal Year Begin Date Year - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02): Fiscal Year Begin Date Month - Integer, two digits.
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02): Fiscal Year Begin Date Day - Integer, two digits.
                    *   `P-NEW-REPORT-DATE`:
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02): Report Date Century - Integer, two digits.
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02): Report Date Year - Integer, two digits.
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02): Report Date Month - Integer, two digits.
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02): Report Date Day - Integer, two digits.
                    *   `P-NEW-TERMINATION-DATE`:
                        *   `P-NEW-TERM-DT-CC` PIC 9(02): Termination Date Century - Integer, two digits.
                        *   `P-