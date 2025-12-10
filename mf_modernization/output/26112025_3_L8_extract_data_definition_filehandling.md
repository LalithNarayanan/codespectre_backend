## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, the program likely interacts with external data through:
        *   **COPY LTDRG031:** This indicates the program includes a COBOL copybook named `LTDRG031`. This copybook almost certainly defines data structures used for DRG (Diagnosis Related Group) information, likely a table of DRG codes, weights, and average lengths of stay.
*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.`
        *   Description: A character field used for internal program reference or identification.
    *   `01 CAL-VERSION PIC X(05) VALUE 'C03.2'.`
        *   Description: Stores the version number of the calculation logic.
    *   `01 HOLD-PPS-COMPONENTS.`
        *   Description: A group of data fields used to hold intermediate calculation values related to the Prospective Payment System (PPS).
            *   `05 H-LOS PIC 9(03).`
                *   Description: Length of Stay (LOS).
            *   `05 H-REG-DAYS PIC 9(03).`
                *   Description: Regular Days.
            *   `05 H-TOTAL-DAYS PIC 9(05).`
                *   Description: Total Days.
            *   `05 H-SSOT PIC 9(02).`
                *   Description: Short Stay Outlier Threshold.
            *   `05 H-BLEND-RTC PIC 9(02).`
                *   Description: Blend Return Code.
            *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
                *   Description: Blend Facility Portion.
            *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
                *   Description: Blend PPS Portion.
            *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
                *   Description: Short Stay Payment Amount.
            *   `05 H-SS-COST PIC 9(07)V9(02).`
                *   Description: Short Stay Cost.
            *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
                *   Description: Labor Portion of the payment.
            *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
                *   Description: Non-Labor Portion of the payment.
            *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
                *   Description: Fixed Loss Amount for outlier calculations.
            *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
                *   Description: New Facility Specific Rate.
    *   Data structures defined in the `LTDRG031` copybook (details are in the `LTDRG031` analysis).
*   **Data Structures in LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA.`
        *   Description: This structure represents the input data (bill information) passed to the program.
            *   `10 B-NPI10.`
                *   Description: National Provider Identifier (NPI) - 10 digits
                    *   `15 B-NPI8 PIC X(08).`
                        *   Description: First 8 digits of the NPI.
                    *   `15 B-NPI-FILLER PIC X(02).`
                        *   Description: Filler for NPI.
            *   `10 B-PROVIDER-NO PIC X(06).`
                *   Description: Provider Number.
            *   `10 B-PATIENT-STATUS PIC X(02).`
                *   Description: Patient Status.
            *   `10 B-DRG-CODE PIC X(03).`
                *   Description: DRG Code.
            *   `10 B-LOS PIC 9(03).`
                *   Description: Length of Stay.
            *   `10 B-COV-DAYS PIC 9(03).`
                *   Description: Covered Days.
            *   `10 B-LTR-DAYS PIC 9(02).`
                *   Description: Lifetime Reserve Days.
            *   `10 B-DISCHARGE-DATE.`
                *   Description: Discharge Date.
                    *   `15 B-DISCHG-CC PIC 9(02).`
                        *   Description: Century Code (Discharge Date).
                    *   `15 B-DISCHG-YY PIC 9(02).`
                        *   Description: Year of Discharge.
                    *   `15 B-DISCHG-MM PIC 9(02).`
                        *   Description: Month of Discharge.
                    *   `15 B-DISCHG-DD PIC 9(02).`
                        *   Description: Day of Discharge.
            *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
                *   Description: Covered Charges.
            *   `10 B-SPEC-PAY-IND PIC X(01).`
                *   Description: Special Payment Indicator.
            *   `10 FILLER PIC X(13).`
                *   Description: Unused filler space
    *   `01 PPS-DATA-ALL.`
        *   Description: This structure is used to return the calculated PPS data to the calling program.
            *   `05 PPS-RTC PIC 9(02).`
                *   Description: Return Code for PPS calculations (indicates payment status or reason for rejection).
            *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
                *   Description: Charge Threshold.
            *   `05 PPS-DATA.`
                *   Description: Group containing main PPS data.
                    *   `10 PPS-MSA PIC X(04).`
                        *   Description: Metropolitan Statistical Area (MSA) code.
                    *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
                        *   Description: Wage Index.
                    *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
                        *   Description: Average Length of Stay.
                    *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
                        *   Description: Relative Weight for the DRG.
                    *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Outlier Payment Amount.
                    *   `10 PPS-LOS PIC 9(03).`
                        *   Description: Length of Stay.
                    *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: DRG Adjusted Payment Amount.
                    *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Federal Payment Amount.
                    *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Final Payment Amount.
                    *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
                        *   Description: Facility Costs.
                    *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
                        *   Description: New Facility Specific Rate.
                    *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
                        *   Description: Outlier Threshold.
                    *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
                        *   Description: Submitted DRG Code.
                    *   `10 PPS-CALC-VERS-CD PIC X(05).`
                        *   Description: Calculation Version Code.
                    *   `10 PPS-REG-DAYS-USED PIC 9(03).`
                        *   Description: Regular Days Used.
                    *   `10 PPS-LTR-DAYS-USED PIC 9(03).`
                        *   Description: Lifetime Reserve Days Used.
                    *   `10 PPS-BLEND-YEAR PIC 9(01).`
                        *   Description: Blend Year.
                    *   `10 PPS-COLA PIC 9(01)V9(03).`
                        *   Description: Cost of Living Adjustment (COLA).
                    *   `10 FILLER PIC X(04).`
                        *   Description: Unused filler space.
            *   `05 PPS-OTHER-DATA.`
                *   Description:  Group containing other PPS data.
                    *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).`
                        *   Description: National Labor Percentage.
                    *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).`
                        *   Description: National Non-Labor Percentage.
                    *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02).`
                        *   Description: Standard Federal Rate.
                    *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).`
                        *   Description: Budget Neutrality Rate.
                    *   `10 FILLER PIC X(20).`
                        *   Description: Unused filler space.
            *   `05 PPS-PC-DATA.`
                *   Description: Group containing PPS PC data.
                    *   `10 PPS-COT-IND PIC X(01).`
                        *   Description: Cost Outlier Indicator.
                    *   `10 FILLER PIC X(20).`
                        *   Description: Unused filler space.
    *   `01 PRICER-OPT-VERS-SW.`
        *   Description:  Switch to indicate which version of LTDRV is being used.
            *   `05 PRICER-OPTION-SW PIC X(01).`
                *   Description: Pricer Option Switch.
                    *   `88 ALL-TABLES-PASSED VALUE 'A'.`
                        *   Description: Indicates all tables are passed.
                    *   `88 PROV-RECORD-PASSED VALUE 'P'.`
                        *   Description: Indicates the provider record is passed.
            *   `05 PPS-VERSIONS.`
                *   Description: Group containing PPS version information.
                    *   `10 PPDRV-VERSION PIC X(05).`
                        *   Description: Version of PPDRV being used.
    *   `01 PROV-NEW-HOLD.`
        *   Description: This structure represents the provider record passed to the program.
            *   `02 PROV-NEWREC-HOLD1.`
                *   Description:  Hold area for provider record part 1.
                    *   `05 P-NEW-NPI10.`
                        *   Description: NPI - 10 digits
                            *   `10 P-NEW-NPI8 PIC X(08).`
                                *   Description: First 8 digits of the NPI.
                            *   `10 P-NEW-NPI-FILLER PIC X(02).`
                                *   Description: Filler for NPI.
                    *   `05 P-NEW-PROVIDER-NO.`
                        *   Description: Provider Number
                            *   `10 P-NEW-STATE PIC 9(02).`
                                *   Description: State Code.
                            *   `10 FILLER PIC X(04).`
                                *   Description: Filler.
                    *   `05 P-NEW-DATE-DATA.`
                        *   Description: Date information.
                            *   `10 P-NEW-EFF-DATE.`
                                *   Description: Effective Date.
                                    *   `15 P-NEW-EFF-DT-CC PIC 9(02).`
                                        *   Description: Century Code (Effective Date).
                                    *   `15 P-NEW-EFF-DT-YY PIC 9(02).`
                                        *   Description: Year of Effective Date.
                                    *   `15 P-NEW-EFF-DT-MM PIC 9(02).`
                                        *   Description: Month of Effective Date.
                                    *   `15 P-NEW-EFF-DT-DD PIC 9(02).`
                                        *   Description: Day of Effective Date.
                            *   `10 P-NEW-FY-BEGIN-DATE.`
                                *   Description: Fiscal Year Begin Date.
                                    *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02).`
                                        *   Description: Century Code (FY Begin Date).
                                    *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02).`
                                        *   Description: Year of FY Begin Date.
                                    *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02).`
                                        *   Description: Month of FY Begin Date.
                                    *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02).`
                                        *   Description: Day of FY Begin Date.
                            *   `10 P-NEW-REPORT-DATE.`
                                *   Description: Report Date.
                                    *   `15 P-NEW-REPORT-DT-CC PIC 9(02).`
                                        *   Description: Century Code (Report Date).
                                    *   `15 P-NEW-REPORT-DT-YY PIC 9(02).`
                                        *   Description: Year of Report Date.
                                    *   `15 P-NEW-REPORT-DT-MM PIC 9(02).`
                                        *   Description: Month of Report Date.
                                    *   `15 P-NEW-REPORT-DT-DD PIC 9(02).`
                                        *   Description: Day of Report Date.
                            *   `10 P-NEW-TERMINATION-DATE.`
                                *   Description: Termination Date.
                                    *   `15 P-NEW-TERM-DT-CC PIC 9(02).`
                                        *   Description: Century Code (Termination Date).
                                    *   `15 P-NEW-TERM-DT-YY PIC 9(02).`
                                        *   Description: Year of Termination Date.
                                    *   `15 P-NEW-TERM-DT-MM PIC 9(02).`
                                        *   Description: Month of Termination Date.
                                    *   `15 P-NEW-TERM-DT-DD PIC 9(02).`
                                        *   Description: Day of Termination Date.
                    *   `05 P-NEW-WAIVER-CODE PIC X(01).`
                        *   Description: Waiver Code
                            *   `88 P-NEW-WAIVER-STATE VALUE 'Y'.`
                                *   Description: Waiver State (if 'Y').
                    *   `05 P-NEW-INTER-NO PIC 9(05).`
                        *   Description: Internal Number.
                    *   `05 P-NEW-PROVIDER-TYPE PIC X(02).`
                        *   Description: Provider Type.
                    *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
                        *   Description: Current Census Division.
                    *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
                        *   Description: Current Division (redefines the census division).
                    *   `05 P-NEW-MSA-DATA.`
                        *   Description: MSA Data
                            *   `10 P-NEW-CHG-CODE-INDEX PIC X.`
                                *   Description: Charge Code Index.
                            *   `10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.`
                                *   Description: Geographic Location MSA Code.
                            *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).`
                                *   Description: Geographic Location MSA Code (numeric).
                            *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.`
                                *   Description: Wage Index Location MSA Code.
                            *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.`
                                *   Description: Standard Amount Location MSA Code.
                            *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.`
                                *   Description: Standard Amount Location MSA Code (numeric).
                                    *   `15 P-NEW-RURAL-1ST.`
                                        *   Description: Rural Indicators.
                                            *   `20 P-NEW-STAND-RURAL PIC XX.`
                                                *   Description:  Rural Indicator.
                                                    *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '.`
                                                        *   Description: Check for Standard Rural.
                                            *   `15 P-NEW-RURAL-2ND PIC XX.`
                                                *   Description: Rural Indicator.
                    *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.`
                        *   Description: Sole Community Hospital Year.
                    *   `05 P-NEW-LUGAR PIC X.`
                        *   Description: Lugar.
                    *   `05 P-NEW-TEMP-RELIEF-IND PIC X.`
                        *   Description: Temporary Relief Indicator.
                    *   `05 P-NEW-FED-PPS-BLEND-IND PIC X.`
                        *   Description: Federal PPS Blend Indicator.
                    *   `05 FILLER PIC X(05).`
                        *   Description: Unused filler space.
            *   `02 PROV-NEWREC-HOLD2.`
                *   Description: Hold area for provider record part 2.
                    *   `05 P-NEW-VARIABLES.`
                        *   Description: Various provider-specific variables.
                            *   `10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
                                *   Description: Facility Specific Rate.
                            *   `10 P-NEW-COLA PIC 9(01)V9(03).`
                                *   Description: COLA.
                            *   `10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).`
                                *   Description: Intern Ratio.
                            *   `10 P-NEW-BED-SIZE PIC 9(05).`
                                *   Description: Bed Size.
                            *   `10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).`
                                *   Description: Operating Cost to Charge Ratio.
                            *   `10 P-NEW-CMI PIC 9(01)V9(04).`
                                *   Description: CMI.
                            *   `10 P-NEW-SSI-RATIO PIC V9(04).`
                                *   Description: SSI Ratio.
                            *   `10 P-NEW-MEDICAID-RATIO PIC V9(04).`
                                *   Description: Medicaid Ratio.
                            *   `10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).`
                                *   Description: PPS Blend Year Indicator.
                            *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).`
                                *   Description: Pruf Update Factor.
                            *   `10 P-NEW-DSH-PERCENT PIC V9(04).`
                                *   Description: DSH Percentage.
                            *   `10 P-NEW-FYE-DATE PIC X(08).`
                                *   Description: Fiscal Year End Date.
                    *   `05 FILLER PIC X(23).`
                        *   Description: Unused filler space.
            *   `02 PROV-NEWREC-HOLD3.`
                *   Description: Hold area for provider record part 3.
                    *   `05 P-NEW-PASS-AMT-DATA.`
                        *   Description: Pass Through Amount Data.
                            *   `10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.`
                                *   Description: Pass Through Amount - Capital.
                            *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.`
                                *   Description: Pass Through Amount - Direct Medical Education.
                            *   `10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.`
                                *   Description: Pass Through Amount - Organ Acquisition.
                            *   `10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.`
                                *   Description: Pass Through Amount - Plus Miscellaneous.
                    *   `05 P-NEW-CAPI-DATA.`
                        *   Description: Capital Data.
                            *   `15 P-NEW-CAPI-PPS-PAY-CODE PIC X.`
                                *   Description: Capital PPS Pay Code.
                            *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.`
                                *   Description: Capital Hospital Specific Rate.
                            *   `15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.`
                                *   Description: Capital Old Harm Rate.
                            *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.`
                                *   Description: Capital New Harm Ratio.
                            *   `15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.`
                                *   Description: Capital Cost to Charge Ratio.
                            *   `15 P-NEW-CAPI-NEW-HOSP PIC X.`
                                *   Description: Capital New Hospital.
                            *   `15 P-NEW-CAPI-IME PIC 9V9999.`
                                *   Description: Capital IME.
                            *   `15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.`
                                *   Description: Capital Exceptions.
                    *   `05 FILLER PIC X(22).`
                        *   Description: Unused filler space.
    *   `01 WAGE-NEW-INDEX-RECORD.`
        *   Description: Wage Index Record.
            *   `05 W-MSA PIC X(4).`
                *   Description: MSA Code.
            *   `05 W-EFF-DATE PIC X(8).`
                *   Description: Effective Date.
            *   `05 W-WAGE-INDEX1 PIC S9(02)V9(04).`
                *   Description: Wage Index 1.
            *   `05 W-WAGE-INDEX2 PIC S9(02)V9(04).`
                *   Description: Wage Index 2.
            *   `05 W-WAGE-INDEX3 PIC S9(02)V9(04).`
                *   Description: Wage Index 3.

*   **Procedure Division:**
    *   The `PROCEDURE DIVISION` contains the program's logic, broken down into paragraphs and sections.  It uses the `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PRICER-OPT-VERS-SW`, `PROV-NEW-HOLD`, and `WAGE-NEW-INDEX-RECORD` data structures defined in the `LINKAGE SECTION`.
    *   The program performs various calculations related to PPS (Prospective Payment System), including edits, DRG code lookups, payment calculations, and outlier determinations.
    *   It calls a subroutine to edit the DRG code.
    *   It calls a subroutine to assemble PPS variables.
    *   It calls a subroutine to calculate payment amount.
    *   It calls a subroutine to calculate outlier amount.
    *   It calls a subroutine to blend the amount.
    *   It calls a subroutine to move the results.

### Program: LTCAL042

*   **File Access:**
    *   Similar to `LTCAL032`, this program doesn't have explicit file access statements, but it interacts with external data.
        *   **COPY LTDRG031:** Includes the same copybook as `LTCAL032`, implying it uses the same DRG table data structures.
*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.`
        *   Description: A character field used for internal program reference or identification.
    *   `01 CAL-VERSION PIC X(05) VALUE 'C04.2'.`
        *   Description: Stores the version number of the calculation logic.
    *   `01 HOLD-PPS-COMPONENTS.`
        *   Description: A group of data fields used to hold intermediate calculation values related to the Prospective Payment System (PPS).
            *   `05 H-LOS PIC 9(03).`
                *   Description: Length of Stay (LOS).
            *   `05 H-REG-DAYS PIC 9(03).`
                *   Description: Regular Days.
            *   `05 H-TOTAL-DAYS PIC 9(05).`
                *   Description: Total Days.
            *   `05 H-SSOT PIC 9(02).`
                *   Description: Short Stay Outlier Threshold.
            *   `05 H-BLEND-RTC PIC 9(02).`
                *   Description: Blend Return Code.
            *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
                *   Description: Blend Facility Portion.
            *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
                *   Description: Blend PPS Portion.
            *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
                *   Description: Short Stay Payment Amount.
            *   `05 H-SS-COST PIC 9(07)V9(02).`
                *   Description: Short Stay Cost.
            *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
                *   Description: Labor Portion of the payment.
            *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
                *   Description: Non-Labor Portion of the payment.
            *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
                *   Description: Fixed Loss Amount for outlier calculations.
            *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
                *   Description: New Facility Specific Rate.
            *   `05 H-LOS-RATIO PIC 9(01)V9(05).`
                *   Description: Length of Stay Ratio.
    *   Data structures defined in the `LTDRG031` copybook (details are in the `LTDRG031` analysis).
*   **Data Structures in LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA.`
        *   Description: This structure represents the input data (bill information) passed to the program.
            *   `10 B-NPI10.`
                *   Description: National Provider Identifier (NPI) - 10 digits
                    *   `15 B-NPI8 PIC X(08).`
                        *   Description: First 8 digits of the NPI.
                    *   `15 B-NPI-FILLER PIC X(02).`
                        *   Description: Filler for NPI.
            *   `10 B-PROVIDER-NO PIC X(06).`
                *   Description: Provider Number.
            *   `10 B-PATIENT-STATUS PIC X(02).`
                *   Description: Patient Status.
            *   `10 B-DRG-CODE PIC X(03).`
                *   Description: DRG Code.
            *   `10 B-LOS PIC 9(03).`
                *   Description: Length of Stay.
            *   `10 B-COV-DAYS PIC 9(03).`
                *   Description: Covered Days.
            *   `10 B-LTR-DAYS PIC 9(02).`
                *   Description: Lifetime Reserve Days.
            *   `10 B-DISCHARGE-DATE.`
                *   Description: Discharge Date.
                    *   `15 B-DISCHG-CC PIC 9(02).`
                        *   Description: Century Code (Discharge Date).
                    *   `15 B-DISCHG-YY PIC 9(02).`
                        *   Description: Year of Discharge.
                    *   `15 B-DISCHG-MM PIC 9(02).`
                        *   Description: Month of Discharge.
                    *   `15 B-DISCHG-DD PIC 9(02).`
                        *   Description: Day of Discharge.
            *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
                *   Description: Covered Charges.
            *   `10 B-SPEC-PAY-IND PIC X(01).`
                *   Description: Special Payment Indicator.
            *   `10 FILLER PIC X(13).`
                *   Description: Unused filler space
    *   `01 PPS-DATA-ALL.`
        *   Description: This structure is used to return the calculated PPS data to the calling program.
            *   `05 PPS-RTC PIC 9(02).`
                *   Description: Return Code for PPS calculations (indicates payment status or reason for rejection).
            *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
                *   Description: Charge Threshold.
            *   `05 PPS-DATA.`
                *   Description: Group containing main PPS data.
                    *   `10 PPS-MSA PIC X(04).`
                        *   Description: Metropolitan Statistical Area (MSA) code.
                    *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
                        *   Description: Wage Index.
                    *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
                        *   Description: Average Length of Stay.
                    *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
                        *   Description: Relative Weight for the DRG.
                    *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Outlier Payment Amount.
                    *   `10 PPS-LOS PIC 9(03).`
                        *   Description: Length of Stay.
                    *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: DRG Adjusted Payment Amount.
                    *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Federal Payment Amount.
                    *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
                        *   Description: Final Payment Amount.
                    *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
                        *   Description: Facility Costs.
                    *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
                        *   Description: New Facility Specific Rate.
                    *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
                        *   Description: Outlier Threshold.
                    *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
                        *   Description: Submitted DRG Code.
                    *   `10 PPS-CALC-VERS-CD PIC X(05).`
                        *   Description: Calculation Version Code.
                    *   `10 PPS-REG-DAYS-USED PIC 9(03).`
                        *   Description: Regular Days Used.
                    *   `10 PPS-LTR-DAYS-USED PIC 9(03).`
                        *   Description: Lifetime Reserve Days Used.
                    *   `10 PPS-BLEND-YEAR PIC 9(01).`
                        *   Description: Blend Year.
                    *   `10 PPS-COLA PIC 9(01)V9(03).`
                        *   Description: Cost of Living Adjustment (COLA).
                    *   `10 FILLER PIC X(04).`
                        *   Description: Unused filler space.
            *   `05 PPS-OTHER-DATA.`
                *   Description:  Group containing other PPS data.
                    *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).`
                        *   Description: National Labor Percentage.
                    *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).`
                        *   Description: National Non-Labor Percentage.
                    *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02).`
                        *   Description: Standard Federal Rate.
                    *   `10 PPS-BDGT-NEUT