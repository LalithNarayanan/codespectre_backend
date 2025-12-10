Here's the analysis of the provided COBOL programs:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access is done in this program.
    *   It uses a `COPY` statement to include the code from `LTDRG031`. This means the data from `LTDRG031` is incorporated into the program's source code during compilation.

*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal reference or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), assumed to be in days.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short Stay Outlier Threshold, expressed as a number of days.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Return Code for Blend Payment calculation.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend Factor for Facility payment.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend Factor for PPS payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount for outlier calculation.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New Facility Specific Rate.
    *   Data structures defined inside the `COPY LTDRG031` (See below).

*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA`:
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08).
                *   Description: National Provider Identifier (NPI) - First 8 characters.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description: National Provider Identifier (NPI) - Filler, 2 characters.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), assumed to be in days.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Discharge Date - Century/Code.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Discharge Date - Year.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Discharge Date - Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Discharge Date - Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused/Filler space.
    *   `PPS-DATA-ALL`:
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold for Outlier.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description: Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Unused space.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler/Unused Space.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler/Unused Space.
    *   `PRICER-OPT-VERS-SW`:
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Pricer Option Switch.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description:  Indicates all tables were passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates Provider record was passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: New NPI (First 8 characters).
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: New NPI (Filler - 2 characters).
            *   `P-NEW-PROVIDER-NO`:
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description: State Code.
                *   `FILLER` PIC X(04).
                    *   Description: Unused/Filler space.
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century/Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century/Code.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Day.
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date - Century/Code.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date - Year.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date - Month.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date - Day.
                *   `P-NEW-TERMINATION-DATE`:
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination Date - Century/Code.
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination Date - Year.
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination Date - Month.
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination Date - Day.
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   Description: Waiver Code.
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                    *   Description: Waiver State (if 'Y').
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Internal Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Redefines the above field.
            *   `P-NEW-MSA-DATA`:
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geographic Location MSA - Alphanumeric.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description: Geographic Location MSA - Numeric (redefined).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Wage Index Location MSA - Alphanumeric.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Standard Amount Location MSA - Alphanumeric.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA:
                    *   `P-NEW-RURAL-1ST`:
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   Description: Standard Rural (1st part).
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                *   Description:  Check for Standard Rural.
                        *   `P-NEW-RURAL-2ND` PIC XX.
                            *   Description: Standard Rural (2nd part).
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sole Community Hospital Year.
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar (Spanish for Place/Location).
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).
                *   Description: Filler/Unused Space.
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                    *   Description: Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                    *   Description: Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                    *   Description: Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05).
                    *   Description: Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                    *   Description: Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                    *   Description: Case Mix Index.
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                    *   Description: SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                    *   Description: Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                    *   Description: PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                    *   Description: Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                    *   Description: DSH Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: Fiscal Year End Date.
            *   `FILLER` PIC X(23).
                *   Description: Filler/Unused Space.
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description: Passed Amount for Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description: Passed Amount for Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description: Passed Amount for Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description: Passed Amount for Plus Misc.
            *   `P-NEW-CAPI-DATA`:
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   Description: Capital PPS Pay Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   Description: Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   Description: Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   Description: Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   Description: Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   Description: Capital New Hospital.
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   Description: Capital IME (Indirect Medical Education).
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                    *   Description: Capital Exceptions.
            *   `FILLER` PIC X(22).
                *   Description: Filler/Unused Space.
    *   `WAGE-NEW-INDEX-RECORD`:
        *   `W-MSA` PIC X(4).
            *   Description: MSA (Metropolitan Statistical Area) code.
        *   `W-EFF-DATE` PIC X(8).
            *   Description: Effective Date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
            *   Description: Wage Index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
            *   Description: Wage Index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
            *   Description: Wage Index 3.

**Data Structures Defined in `COPY LTDRG031`:**

This `COPY` statement includes the following:
*   `W-DRG-FILLS`:
    *   Multiple PIC X(44) values, each presumably containing a string of data.
*   `W-DRG-TABLE REDEFINES W-DRG-FILLS`:
    *   `WWM-ENTRY OCCURS 502 TIMES INDEXED BY WWM-INDX`:
        *   `WWM-DRG` PIC X(3).
            *   Description: DRG code (3 characters).
        *   `WWM-RELWT` PIC 9(1)V9(4).
            *   Description: Relative Weight.
        *   `WWM-ALOS` PIC 9(2)V9(1).
            *   Description: Average Length of Stay.

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access is done in this program.
    *   It uses a `COPY` statement to include the code from `LTDRG031`. This means the data from `LTDRG031` is incorporated into the program's source code during compilation.

*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal reference or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), assumed to be in days.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short Stay Outlier Threshold, expressed as a number of days.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Return Code for Blend Payment calculation.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend Factor for Facility payment.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend Factor for PPS payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount for outlier calculation.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New Facility Specific Rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description:  LOS Ratio

    *   Data structures defined inside the `COPY LTDRG031` (See below).

*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA`:
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08).
                *   Description: National Provider Identifier (NPI) - First 8 characters.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description: National Provider Identifier (NPI) - Filler, 2 characters.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: Diagnosis Related Group (DRG) code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), assumed to be in days.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Discharge Date - Century/Code.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Discharge Date - Year.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Discharge Date - Month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Discharge Date - Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused/Filler space.
    *   `PPS-DATA-ALL`:
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold for Outlier.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description: Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Unused space.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler/Unused Space.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler/Unused Space.
    *   `PRICER-OPT-VERS-SW`:
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Pricer Option Switch.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description:  Indicates all tables were passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates Provider record was passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: New NPI (First 8 characters).
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: New NPI (Filler - 2 characters).
            *   `P-NEW-PROVIDER-NO`:
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description: State Code.
                *   `FILLER` PIC X(04).
                    *   Description: Unused/Filler space.
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century/Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century/Code.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Day.
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date - Century/Code.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date - Year.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date - Month.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date -