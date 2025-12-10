## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  This program likely relies on data passed to it through the `LINKAGE SECTION`.
    *   It uses a `COPY` statement to include `LTDRG031`, which likely contains data used for DRG calculations.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description:  A working storage variable, likely used for program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`
        *   Description: A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS).
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular Days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total Days.
        *   `H-SSOT` PIC 9(02).
            *   Description:  Likely represents the Short Stay Outlier Threshold, calculated based on Average Length of Stay.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return Code for Blend.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description:  Facility Blend Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description:  PPS Blend Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor Portion of the payment calculation.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-Labor Portion of the payment calculation.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed Loss Amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`
        *   Description:  A record structure containing the bill information passed *to* the program.  This is how the calling program provides the input data.
        *   `B-NPI10`
            *   Description: National Provider Identifier (NPI).
            *   `B-NPI8` PIC X(08).
                *   Description: First 8 characters of the NPI.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description: Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: DRG (Diagnosis Related Group) Code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`
            *   Description: Discharge Date.
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Century of the Discharge Date.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Year of the Discharge Date.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Month of the Discharge Date.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Day of the Discharge Date.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Pay Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Filler.
    *   `PPS-DATA-ALL`
        *   Description:  A record structure that is passed *back* to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code indicating the result of the calculation.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold.
        *   `PPS-DATA`
            *   Description: PPS Data
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) Code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay (LOS)
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
                *   Description: Version of the Calculation.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend Year.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Filler
        *   `PPS-OTHER-DATA`
            *   Description: Other PPS Data
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
            *   Description: PPS PC Data
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Used to pass version information of the pricer options.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch indicating if all tables or provider record is passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates the Provider Record is passed.
        *   `PPS-VERSIONS`
            *   Description: Contains the version of the PPS program.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`
        *   Description:  A record structure containing provider-specific information.
        *   `PROV-NEWREC-HOLD1`
            *   Description: Provider Record Hold Area 1
            *   `P-NEW-NPI10`
                *   Description: Provider NPI
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  NPI - First 8 characters
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  NPI - Filler
            *   `P-NEW-PROVIDER-NO`
                *   Description: Provider Number
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description: State Code.
                *   `FILLER` PIC X(04).
                    *   Description: Filler
            *   `P-NEW-DATE-DATA`
                *   Description: Date Data
                *   `P-NEW-EFF-DATE`
                    *   Description: Effective Date
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   Description: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Month
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Day
                *   `P-NEW-REPORT-DATE`
                    *   Description: Report Date
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report Date - Century
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report Date - Year
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report Date - Month
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report Date - Day
                *   `P-NEW-TERMINATION-DATE`
                    *   Description: Termination Date
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination Date - Century
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination Date - Year
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination Date - Month
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination Date - Day
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   Description: Waiver Code
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                    *   Description: Waiver State
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Intern Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Current Census Division
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Current Division.
            *   `P-NEW-MSA-DATA`
                *   Description: MSA Data
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geo Location MSA
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description: Geo Location MSA Redefine
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   Description: Standard Amount Location MSA Redefine
                    *   `P-NEW-RURAL-1ST`
                        *   Description: Rural 1st
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   Description: Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                *   Description: Standard Rural Check
                        *   `P-NEW-RURAL-2ND` PIC XX.
                            *   Description: Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sole Community Dependent Hospital Year
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD2`
            *   Description: Provider Record Hold Area 2
            *   `P-NEW-VARIABLES`
                *   Description: Variables
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
                    *   Description: DSH Percent.
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: Fiscal Year End Date.
            *   `FILLER` PIC X(23).
                *   Description: Filler
        *   `PROV-NEWREC-HOLD3`
            *   Description: Provider Record Hold Area 3
            *   `P-NEW-PASS-AMT-DATA`
                *   Description: Pass Amount Data
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description: Pass Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description: Pass Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description: Pass Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description: Pass Amount Plus Miscellaneous.
            *   `P-NEW-CAPI-DATA`
                *   Description: Capital Data
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
                *   Description: Filler
    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  Wage Index Record
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

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  This program likely relies on data passed to it through the `LINKAGE SECTION`.
    *   It uses a `COPY` statement to include `LTDRG031`, which likely contains data used for DRG calculations.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description:  A working storage variable, likely used for program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`
        *   Description: A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of Stay (LOS).
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular Days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total Days.
        *   `H-SSOT` PIC 9(02).
            *   Description:  Likely represents the Short Stay Outlier Threshold, calculated based on Average Length of Stay.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description:  Return Code for Blend.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description:  Facility Blend Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description:  PPS Blend Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor Portion of the payment calculation.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-Labor Portion of the payment calculation.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed Loss Amount used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New Facility Specific Rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description: Length of Stay Ratio.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`
        *   Description:  A record structure containing the bill information passed *to* the program.  This is how the calling program provides the input data.
        *   `B-NPI10`
            *   Description: National Provider Identifier (NPI).
            *   `B-NPI8` PIC X(08).
                *   Description: First 8 characters of the NPI.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description: Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient Status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: DRG (Diagnosis Related Group) Code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of Stay.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered Days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`
            *   Description: Discharge Date.
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Century of the Discharge Date.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Year of the Discharge Date.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Month of the Discharge Date.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Day of the Discharge Date.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special Pay Indicator.
        *   `FILLER` PIC X(13).
            *   Description: Filler.
    *   `PPS-DATA-ALL`
        *   Description:  A record structure that is passed *back* to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return Code indicating the result of the calculation.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge Threshold.
        *   `PPS-DATA`
            *   Description: PPS Data
            *   `PPS-MSA` PIC X(04).
                *   Description:  Metropolitan Statistical Area (MSA) Code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage Index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of Stay (LOS)
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
                *   Description: Version of the Calculation.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend Year.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Filler
        *   `PPS-OTHER-DATA`
            *   Description: Other PPS Data
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
            *   Description: PPS PC Data
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost Outlier Indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Used to pass version information of the pricer options.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch indicating if all tables or provider record is passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Indicates the Provider Record is passed.
        *   `PPS-VERSIONS`
            *   Description: Contains the version of the PPS program.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`
        *   Description:  A record structure containing provider-specific information.
        *   `PROV-NEWREC-HOLD1`
            *   Description: Provider Record Hold Area 1
            *   `P-NEW-NPI10`
                *   Description: Provider NPI
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description:  NPI - First 8 characters
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description:  NPI - Filler
            *   `P-NEW-PROVIDER-NO`
                *   Description: Provider Number
                *   `P-NEW-STATE` PIC 9(02).
                    *   Description: State Code.
                *   `FILLER` PIC X(04).
                    *   Description: Filler
            *   `P-NEW-DATE-DATA`
                *   Description: Date Data
                *   `P-NEW-EFF-DATE`
                    *   Description: Effective Date
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective Date - Century
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   Description: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Century
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal Year Begin Date - Year
                    *   `P