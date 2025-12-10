Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement:
        *   `COPY LTDRG031.` This implies that the program includes the contents of the `LTDRG031` file, which likely contains DRG (Diagnosis Related Group) data, such as DRG codes, relative weights, and average lengths of stay.  While not a file access *within* LTCAL032, it's a critical data source.

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description:  A literal string used for internal program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description:  A group of data items used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), likely in days.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days of stay.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days of stay.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return code for blended payment (facility and DRG).
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Percentage of facility rate for blended payment.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Percentage of PPS payment for blended payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment amount.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment amount.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.

*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:
        *   Description:  This is the main data structure passed *into* the program from the calling program.  It contains billing information.
        *   `B-NPI10`:
            *   Description: National Provider Identifier (NPI) - 10 characters.
            *   `B-NPI8` PIC X(08).
                *   Description: First 8 characters of NPI.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: DRG Code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), likely in days.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   Description: Patient Discharge Date.
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Century/Component of Discharge Date.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Year of Discharge Date.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Month of Discharge Date.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Day of Discharge Date.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused filler.
    *   `PPS-DATA-ALL`:
        *   Description:  This data structure is passed *back* to the calling program. It contains the calculated PPS results.
        *   `PPS-RTC` PIC 9(02).
            *   Description: PPS Return Code (indicates payment status or error).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold.
        *   `PPS-DATA`:
            *   Description: Group containing PPS data.
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight (DRG specific).
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay (LOS).
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New facility specific rate.
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
                *   Description: Unused filler.
        *   `PPS-OTHER-DATA`:
            *   Description: Group containing other PPS data.
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Unused filler.
        *   `PPS-PC-DATA`:
            *   Description: Group containing PPS PC data.
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Unused filler.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Switch to indicate which versions of tables are passed.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch to indicate whether all tables or just the provider record are passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Indicates that all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates that only the provider record is passed.
        *   `PPS-VERSIONS`:
            *   Description: Group containing PPS versions.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description:  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description: Contains provider-specific information, passed *into* the program.
        *   `PROV-NEWREC-HOLD1`:
            *   Description: Hold for provider record 1.
            *   `P-NEW-NPI10`:
                *   Description: New NPI.
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: NPI - First 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: NPI - Filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number.
            *   `P-NEW-STATE` PIC 9(02).
                *   Description: State Code.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
            *   `P-NEW-DATE-DATA`:
                *   Description:  Date information.
                *   `P-NEW-EFF-DATE`:
                    *   Description: Effective Date.
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Century/Component of Effective Date.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Year of Effective Date.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Month of Effective Date.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Day of Effective Date.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   Description: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Century/Component of FY Begin Date.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Year of FY Begin Date.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Month of FY Begin Date.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Day of FY Begin Date.
                *   `P-NEW-REPORT-DATE`:
                    *   Description: Report Date.
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Century/Component of Report Date.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Year of Report Date.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Month of Report Date.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Day of Report Date.
                *   `P-NEW-TERMINATION-DATE`:
                    *   Description: Termination Date.
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Century/Component of Termination Date.
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Year of Termination Date.
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Month of Termination Date.
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Day of Termination Date.
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   Description: Waiver Code.
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                    *   Description: Waiver State.
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Internal Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Census Division (Redefined).
            *   `P-NEW-MSA-DATA`:
                *   Description: MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geographic Location MSA (right justified).
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description: Geographic Location MSA (numeric, redefined).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Wage Index Location MSA (right justified).
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Standard Amount Location MSA (right justified).
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   Description: Standard Amount Location MSA (numeric, redefined).
                    *   `P-NEW-RURAL-1ST`:
                        *   Description: Rural Flag 1st.
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   Description: Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                *   Description: Check for Standard Rural.
                        *   `P-NEW-RURAL-2ND` PIC XX.
                            *   Description: Rural Flag 2nd.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).
                *   Description: Filler.
        *   `PROV-NEWREC-HOLD2`:
            *   Description: Hold for provider record 2.
            *   `P-NEW-VARIABLES`:
                *   Description: Group containing provider variables.
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                    *   Description: Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                    *   Description: COLA.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                    *   Description: Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05).
                    *   Description: Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                    *   Description: Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                    *   Description: CMI.
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                    *   Description: SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                    *   Description: Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                    *   Description: PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                    *   Description: PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                    *   Description: DSH Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: FYE Date.
            *   `FILLER` PIC X(23).
                *   Description: Filler.
        *   `PROV-NEWREC-HOLD3`:
            *   Description: Hold for provider record 3.
            *   `P-NEW-PASS-AMT-DATA`:
                *   Description: Passed Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description: Passed Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description: Passed Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description: Passed Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description: Passed Amount Plus Misc.
            *   `P-NEW-CAPI-DATA`:
                *   Description: Capital Data.
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
                    *   Description: Capital IME.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                    *   Description: Capital Exceptions.
            *   `FILLER` PIC X(22).
                *   Description: Filler.
    *   `WAGE-NEW-INDEX-RECORD`:
        *   Description:  Wage index record.
        *   `W-MSA` PIC X(4).
            *   Description: MSA Code.
        *   `W-EFF-DATE` PIC X(8).
            *   Description: Effective Date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
            *   Description: Wage Index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
            *   Description: Wage Index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
            *   Description: Wage Index 3.

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program uses a `COPY` statement:
        *   `COPY LTDRG031.` This implies that the program includes the contents of the `LTDRG031` file, which likely contains DRG (Diagnosis Related Group) data, such as DRG codes, relative weights, and average lengths of stay.  While not a file access *within* LTCAL042, it's a critical data source.

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description:  A literal string used for internal program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description:  A group of data items used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), likely in days.
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days of stay.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days of stay.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return code for blended payment (facility and DRG).
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Percentage of facility rate for blended payment.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Percentage of PPS payment for blended payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment amount.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment amount.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description: LOS Ratio.

*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:
        *   Description:  This is the main data structure passed *into* the program from the calling program.  It contains billing information.
        *   `B-NPI10`:
            *   Description: National Provider Identifier (NPI) - 10 characters.
            *   `B-NPI8` PIC X(08).
                *   Description: First 8 characters of NPI.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description:  Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: DRG Code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS), likely in days.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   Description: Patient Discharge Date.
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Century/Component of Discharge Date.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Year of Discharge Date.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Month of Discharge Date.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Day of Discharge Date.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Payment Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Unused filler.
    *   `PPS-DATA-ALL`:
        *   Description:  This data structure is passed *back* to the calling program. It contains the calculated PPS results.
        *   `PPS-RTC` PIC 9(02).
            *   Description: PPS Return Code (indicates payment status or error).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold.
        *   `PPS-DATA`:
            *   Description: Group containing PPS data.
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight (DRG specific).
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay (LOS).
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New facility specific rate.
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
                *   Description: Unused filler.
        *   `PPS-OTHER-DATA`:
            *   Description: Group containing other PPS data.
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget Neutrality Rate.
            *   `FILLER` PIC X(20).
                *   Description: Unused filler.
        *   `PPS-PC-DATA`:
            *   Description: Group containing PPS PC data.
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Unused filler.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Switch to indicate which versions of tables are passed.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch to indicate whether all tables or just the provider record are passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Indicates that all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates that only the provider record is passed.
        *   `PPS-VERSIONS`:
            *   Description: Group containing PPS versions.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description:  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description: Contains provider-specific information, passed *into* the program.
        *   `PROV-NEWREC-HOLD1`:
            *   Description: Hold for provider record 1.
            *   `P-NEW-NPI10`:
                *   Description: New NPI.
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: NPI - First 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: NPI - Filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number.
            *   `P-NEW-STATE` PIC 9(02).
                *   Description: State Code.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
            *   `P-NEW-DATE-DATA`:
                *   Description:  Date information.
                *   `P-NEW-EFF-DATE`:
                    *   Description: Effective Date.