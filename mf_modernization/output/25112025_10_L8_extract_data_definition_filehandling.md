## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and their descriptions.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access is defined in the `FILE-CONTROL` section. It is likely that this program is a subroutine and receives data through the `LINKAGE SECTION`.
    *   It uses a `COPY` statement to include `LTDRG031`, which likely contains DRG (Diagnosis Related Group) data.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal program reference or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` (Defined by the COPY LTDRG031, which is not provided but is described below).
        *   Description:  Holds various components used in the PPS (Prospective Payment System) calculation.
            *   `H-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `H-REG-DAYS` PIC 9(03).
                *   Description: Regular Days
            *   `H-TOTAL-DAYS` PIC 9(05).
                *   Description: Total Days
            *   `H-SSOT` PIC 9(02).
                *   Description: Short Stay Outlier Threshold
            *   `H-BLEND-RTC` PIC 9(02).
                *   Description: Blend Return Code
            *   `H-BLEND-FAC` PIC 9(01)V9(01).
                *   Description: Blend Facility Rate
            *   `H-BLEND-PPS` PIC 9(01)V9(01).
                *   Description: Blend PPS Rate
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Short Stay Payment Amount
            *   `H-SS-COST` PIC 9(07)V9(02).
                *   Description: Short Stay Cost
            *   `H-LABOR-PORTION` PIC 9(07)V9(06).
                *   Description: Labor Portion
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
                *   Description: Non-Labor Portion
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
                *   Description: Fixed Loss Amount
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                *   Description: New Facility Specific Rate

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  This structure is passed from the calling program and contains billing information.
            *   `B-NPI10`
                *   `B-NPI8` PIC X(08).
                    *   Description: National Provider Identifier (NPI) - First 8 characters
                *   `B-NPI-FILLER` PIC X(02).
                    *   Description: National Provider Identifier (NPI) - Last 2 characters
            *   `B-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number
            *   `B-PATIENT-STATUS` PIC X(02).
                *   Description: Patient Status
            *   `B-DRG-CODE` PIC X(03).
                *   Description: DRG Code
            *   `B-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `B-COV-DAYS` PIC 9(03).
                *   Description: Covered Days
            *   `B-LTR-DAYS` PIC 9(02).
                *   Description: Lifetime Reserve Days
            *   `B-DISCHARGE-DATE`
                *   `B-DISCHG-CC` PIC 9(02).
                    *   Description: Discharge Date - Century/Code
                *   `B-DISCHG-YY` PIC 9(02).
                    *   Description: Discharge Date - Year
                *   `B-DISCHG-MM` PIC 9(02).
                    *   Description: Discharge Date - Month
                *   `B-DISCHG-DD` PIC 9(02).
                    *   Description: Discharge Date - Day
            *   `B-COV-CHARGES` PIC 9(07)V9(02).
                *   Description: Covered Charges
            *   `B-SPEC-PAY-IND` PIC X(01).
                *   Description: Special Payment Indicator
            *   `FILLER` PIC X(13).
                *   Description: Unused/Filler space
    *   `PPS-DATA-ALL`
        *   Description: This structure is passed from the calling program and contains PPS calculation results and related data.
            *   `PPS-RTC` PIC 9(02).
                *   Description: PPS Return Code
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
                *   Description: PPS Charge Threshold
            *   `PPS-DATA`
                *   `PPS-MSA` PIC X(04).
                    *   Description: Metropolitan Statistical Area (MSA)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                    *   Description: PPS Wage Index
                *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                    *   Description: PPS Average Length of Stay
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                    *   Description: PPS Relative Weight
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Outlier Payment Amount
                *   `PPS-LOS` PIC 9(03).
                    *   Description: PPS Length of Stay
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS DRG Adjusted Payment Amount
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Federal Payment Amount
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Final Payment Amount
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                    *   Description: PPS Facility Costs
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                    *   Description: PPS New Facility Specific Rate
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                    *   Description: PPS Outlier Threshold
                *   `PPS-SUBM-DRG-CODE` PIC X(03).
                    *   Description: Submitted DRG Code
                *   `PPS-CALC-VERS-CD` PIC X(05).
                    *   Description: Calculation Version Code
                *   `PPS-REG-DAYS-USED` PIC 9(03).
                    *   Description: PPS Regular Days Used
                *   `PPS-LTR-DAYS-USED` PIC 9(03).
                    *   Description: PPS Lifetime Reserve Days Used
                *   `PPS-BLEND-YEAR` PIC 9(01).
                    *   Description: PPS Blend Year
                *   `PPS-COLA` PIC 9(01)V9(03).
                    *   Description: PPS Cost of Living Adjustment
                *   `FILLER` PIC X(04).
                    *   Description: Unused/Filler space
            *   `PPS-OTHER-DATA`
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                    *   Description: PPS National Labor Percentage
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                    *   Description: PPS National Non-Labor Percentage
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                    *   Description: PPS Standard Federal Rate
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                    *   Description: PPS Budget Neutrality Rate
                *   `FILLER` PIC X(20).
                    *   Description: Unused/Filler space
            *   `PPS-PC-DATA`
                *   `PPS-COT-IND` PIC X(01).
                    *   Description: Cost Outlier Indicator
                *   `FILLER` PIC X(20).
                    *   Description: Unused/Filler space
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Indicates which version of the pricer options to use.
            *   `PRICER-OPTION-SW` PIC X(01).
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                    *   Description: Indicates all tables are passed
                *   `PROV-RECORD-PASSED` VALUE 'P'.
                    *   Description: Indicates provider record is passed
            *   `PPS-VERSIONS`
                *   `PPDRV-VERSION` PIC X(05).
                    *   Description:  PPS version.
    *   `PROV-NEW-HOLD`
        *   Description:  This structure is passed from the calling program and contains provider information.
            *   `PROV-NEWREC-HOLD1`
                *   `P-NEW-NPI10`
                    *   `P-NEW-NPI8` PIC X(08).
                        *   Description: New NPI - First 8 characters
                    *   `P-NEW-NPI-FILLER` PIC X(02).
                        *   Description: New NPI - Last 2 characters
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02).
                        *   Description: New Provider State
                    *   `FILLER` PIC X(04).
                        *   Description: Unused/Filler space
                *   `P-NEW-DATE-DATA`
                    *   `P-NEW-EFF-DATE`
                        *   `P-NEW-EFF-DT-CC` PIC 9(02).
                            *   Description: New Effective Date - Century
                        *   `P-NEW-EFF-DT-YY` PIC 9(02).
                            *   Description: New Effective Date - Year
                        *   `P-NEW-EFF-DT-MM` PIC 9(02).
                            *   Description: New Effective Date - Month
                        *   `P-NEW-EFF-DT-DD` PIC 9(02).
                            *   Description: New Effective Date - Day
                    *   `P-NEW-FY-BEGIN-DATE`
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Century
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Year
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Month
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Day
                    *   `P-NEW-REPORT-DATE`
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                            *   Description: New Report Date - Century
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                            *   Description: New Report Date - Year
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                            *   Description: New Report Date - Month
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                            *   Description: New Report Date - Day
                    *   `P-NEW-TERMINATION-DATE`
                        *   `P-NEW-TERM-DT-CC` PIC 9(02).
                            *   Description: New Termination Date - Century
                        *   `P-NEW-TERM-DT-YY` PIC 9(02).
                            *   Description: New Termination Date - Year
                        *   `P-NEW-TERM-DT-MM` PIC 9(02).
                            *   Description: New Termination Date - Month
                        *   `P-NEW-TERM-DT-DD` PIC 9(02).
                            *   Description: New Termination Date - Day
                *   `P-NEW-WAIVER-CODE` PIC X(01).
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                        *   Description: New Waiver State
                *   `P-NEW-INTER-NO` PIC 9(05).
                    *   Description: New Intern Number
                *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                    *   Description: New Provider Type
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                    *   Description: New Current Census Division
                *   `P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                    *   Description: New Current Division - Redefines Census Division
                *   `P-NEW-MSA-DATA`
                    *   `P-NEW-CHG-CODE-INDEX` PIC X.
                        *   Description: New Charge Code Index
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                        *   Description: New Geographic Location MSA - Alphanumeric
                    *   `P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX` PIC 9(04).
                        *   Description: New Geographic Location MSA - Numeric
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                        *   Description: New Wage Index Location MSA
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                        *   Description: New Standard Amount Location MSA
                    *   `P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`
                        *   `P-NEW-RURAL-1ST`
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                    *   Description: New Standard Rural Check
                            *   `P-NEW-RURAL-2ND` PIC XX.
                                *   Description: New Rural 2nd
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                    *   Description: New Sole Community Dependent Hospital Year
                *   `P-NEW-LUGAR` PIC X.
                    *   Description: New Lugar
                *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                    *   Description: New Temporary Relief Indicator
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                    *   Description: New Federal PPS Blend Indicator
                *   `FILLER` PIC X(05).
                    *   Description: Unused/Filler space
            *   `PROV-NEWREC-HOLD2`
                *   `P-NEW-VARIABLES`
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                        *   Description: New Facility Specific Rate
                    *   `P-NEW-COLA` PIC 9(01)V9(03).
                        *   Description: New Cost of Living Adjustment
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                        *   Description: New Intern Ratio
                    *   `P-NEW-BED-SIZE` PIC 9(05).
                        *   Description: New Bed Size
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                        *   Description: New Operating Cost to Charge Ratio
                    *   `P-NEW-CMI` PIC 9(01)V9(04).
                        *   Description: New CMI
                    *   `P-NEW-SSI-RATIO` PIC V9(04).
                        *   Description: New SSI Ratio
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                        *   Description: New Medicaid Ratio
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                        *   Description: New PPS Blend Year Indicator
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                        *   Description: New Pruf Update Factor
                    *   `P-NEW-DSH-PERCENT` PIC V9(04).
                        *   Description: New DSH Percent
                    *   `P-NEW-FYE-DATE` PIC X(08).
                        *   Description: New Fiscal Year End Date
                *   `FILLER` PIC X(23).
                    *   Description: Unused/Filler space
            *   `PROV-NEWREC-HOLD3`
                *   `P-NEW-PASS-AMT-DATA`
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                        *   Description: New Pass Through Amount Capital
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                        *   Description: New Pass Through Amount Direct Medical Education
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                        *   Description: New Pass Through Amount Organ Acquisition
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                        *   Description: New Pass Through Amount Plus Miscellaneous
                *   `P-NEW-CAPI-DATA`
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                        *   Description: New Capital PPS Pay Code
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                        *   Description: New Capital Hospital Specific Rate
                    *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                        *   Description: New Capital Old Harm Rate
                    *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                        *   Description: New Capital New Harm Ratio
                    *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                        *   Description: New Capital Cost to Charge Ratio
                    *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                        *   Description: New Capital New Hospital
                    *   `P-NEW-CAPI-IME` PIC 9V9999.
                        *   Description: New Capital IME
                    *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                        *   Description: New Capital Exceptions
                *   `FILLER` PIC X(22).
                    *   Description: Unused/Filler space
    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This structure is passed from the calling program and contains wage index information.
            *   `W-MSA` PIC X(4).
                *   Description: Wage Index MSA
            *   `W-EFF-DATE` PIC X(8).
                *   Description: Wage Index Effective Date
            *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
                *   Description: Wage Index 1
            *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
                *   Description: Wage Index 2
            *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
                *   Description: Wage Index 3

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access is defined in the `FILE-CONTROL` section. It is likely that this program is a subroutine and receives data through the `LINKAGE SECTION`.
    *   It uses a `COPY` statement to include `LTDRG031`, which likely contains DRG (Diagnosis Related Group) data.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal program reference or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description:  Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` (Defined by the COPY LTDRG031, which is not provided but is described below).
        *   Description:  Holds various components used in the PPS (Prospective Payment System) calculation.
            *   `H-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `H-REG-DAYS` PIC 9(03).
                *   Description: Regular Days
            *   `H-TOTAL-DAYS` PIC 9(05).
                *   Description: Total Days
            *   `H-SSOT` PIC 9(02).
                *   Description: Short Stay Outlier Threshold
            *   `H-BLEND-RTC` PIC 9(02).
                *   Description: Blend Return Code
            *   `H-BLEND-FAC` PIC 9(01)V9(01).
                *   Description: Blend Facility Rate
            *   `H-BLEND-PPS` PIC 9(01)V9(01).
                *   Description: Blend PPS Rate
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Short Stay Payment Amount
            *   `H-SS-COST` PIC 9(07)V9(02).
                *   Description: Short Stay Cost
            *   `H-LABOR-PORTION` PIC 9(07)V9(06).
                *   Description: Labor Portion
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
                *   Description: Non-Labor Portion
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
                *   Description: Fixed Loss Amount
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                *   Description: New Facility Specific Rate
            *   `H-LOS-RATIO` PIC 9(01)V9(05).
                *   Description: Length of Stay Ratio

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  This structure is passed from the calling program and contains billing information.
            *   `B-NPI10`
                *   `B-NPI8` PIC X(08).
                    *   Description: National Provider Identifier (NPI) - First 8 characters
                *   `B-NPI-FILLER` PIC X(02).
                    *   Description: National Provider Identifier (NPI) - Last 2 characters
            *   `B-PROVIDER-NO` PIC X(06).
                *   Description: Provider Number
            *   `B-PATIENT-STATUS` PIC X(02).
                *   Description: Patient Status
            *   `B-DRG-CODE` PIC X(03).
                *   Description: DRG Code
            *   `B-LOS` PIC 9(03).
                *   Description: Length of Stay
            *   `B-COV-DAYS` PIC 9(03).
                *   Description: Covered Days
            *   `B-LTR-DAYS` PIC 9(02).
                *   Description: Lifetime Reserve Days
            *   `B-DISCHARGE-DATE`
                *   `B-DISCHG-CC` PIC 9(02).
                    *   Description: Discharge Date - Century/Code
                *   `B-DISCHG-YY` PIC 9(02).
                    *   Description: Discharge Date - Year
                *   `B-DISCHG-MM` PIC 9(02).
                    *   Description: Discharge Date - Month
                *   `B-DISCHG-DD` PIC 9(02).
                    *   Description: Discharge Date - Day
            *   `B-COV-CHARGES` PIC 9(07)V9(02).
                *   Description: Covered Charges
            *   `B-SPEC-PAY-IND` PIC X(01).
                *   Description: Special Payment Indicator
            *   `FILLER` PIC X(13).
                *   Description: Unused/Filler space
    *   `PPS-DATA-ALL`
        *   Description: This structure is passed from the calling program and contains PPS calculation results and related data.
            *   `PPS-RTC` PIC 9(02).
                *   Description: PPS Return Code
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
                *   Description: PPS Charge Threshold
            *   `PPS-DATA`
                *   `PPS-MSA` PIC X(04).
                    *   Description: Metropolitan Statistical Area (MSA)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                    *   Description: PPS Wage Index
                *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                    *   Description: PPS Average Length of Stay
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                    *   Description: PPS Relative Weight
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Outlier Payment Amount
                *   `PPS-LOS` PIC 9(03).
                    *   Description: PPS Length of Stay
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS DRG Adjusted Payment Amount
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Federal Payment Amount
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                    *   Description: PPS Final Payment Amount
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                    *   Description: PPS Facility Costs
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                    *   Description: PPS New Facility Specific Rate
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                    *   Description: PPS Outlier Threshold
                *   `PPS-SUBM-DRG-CODE` PIC X(03).
                    *   Description: Submitted DRG Code
                *   `PPS-CALC-VERS-CD` PIC X(05).
                    *   Description: Calculation Version Code
                *   `PPS-REG-DAYS-USED` PIC 9(03).
                    *   Description: PPS Regular Days Used
                *   `PPS-LTR-DAYS-USED` PIC 9(03).
                    *   Description: PPS Lifetime Reserve Days Used
                *   `PPS-BLEND-YEAR` PIC 9(01).
                    *   Description: PPS Blend Year
                *   `PPS-COLA` PIC 9(01)V9(03).
                    *   Description: PPS Cost of Living Adjustment
                *   `FILLER` PIC X(04).
                    *   Description: Unused/Filler space
            *   `PPS-OTHER-DATA`
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                    *   Description: PPS National Labor Percentage
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                    *   Description: PPS National Non-Labor Percentage
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                    *   Description: PPS Standard Federal Rate
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                    *   Description: PPS Budget Neutrality Rate
                *   `FILLER` PIC X(20).
                    *   Description: Unused/Filler space
            *   `PPS-PC-DATA`
                *   `PPS-COT-IND` PIC X(01).
                    *   Description: Cost Outlier Indicator
                *   `FILLER` PIC X(20).
                    *   Description: Unused/Filler space
    *   `PRICER-OPT-VERS-SW`
        *   Description:  Indicates which version of the pricer options to use.
            *   `PRICER-OPTION-SW` PIC X(01).
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                    *   Description: Indicates all tables are passed
                *   `PROV-RECORD-PASSED` VALUE 'P'.
                    *   Description: Indicates provider record is passed
            *   `PPS-VERSIONS`
                *   `PPDRV-VERSION` PIC X(05).
                    *   Description:  PPS version.
    *   `PROV-NEW-HOLD`
        *   Description:  This structure is passed from the calling program and contains provider information.
            *   `PROV-NEWREC-HOLD1`
                *   `P-NEW-NPI10`
                    *   `P-NEW-NPI8` PIC X(08).
                        *   Description: New NPI - First 8 characters
                    *   `P-NEW-NPI-FILLER` PIC X(02).
                        *   Description: New NPI - Last 2 characters
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02).
                        *   Description: New Provider State
                    *   `FILLER` PIC X(04).
                        *   Description: Unused/Filler space
                *   `P-NEW-DATE-DATA`
                    *   `P-NEW-EFF-DATE`
                        *   `P-NEW-EFF-DT-CC` PIC 9(02).
                            *   Description: New Effective Date - Century
                        *   `P-NEW-EFF-DT-YY` PIC 9(02).
                            *   Description: New Effective Date - Year
                        *   `P-NEW-EFF-DT-MM` PIC 9(02).
                            *   Description: New Effective Date - Month
                        *   `P-NEW-EFF-DT-DD` PIC 9(02).
                            *   Description: New Effective Date - Day
                    *   `P-NEW-FY-BEGIN-DATE`
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Century
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Year
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Month
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                            *   Description: New Fiscal Year Begin Date - Day
                    *   `P-NEW-REPORT-DATE`
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                            *   Description: New Report Date - Century
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                            *   Description: New Report Date - Year
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                            *   Description: New Report Date - Month
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                            *   Description: New Report Date - Day
                    *   `P-NEW-TERMINATION-DATE`
                        *   `P-NEW-TERM-DT-CC` PIC 9(02).
                            *   Description: New Termination Date - Century
                        *   `P-NEW-TERM-DT-YY` PIC 9(02).
                            *   Description: New Termination Date - Year
                        *   `P-NEW-TERM-DT-MM` PIC 9(02).
                            *   Description: New Termination Date - Month
                        *   `P-NEW-TERM-DT-DD` PIC 9(02).
                            *   Description: New Termination Date - Day
                *   `P-NEW-WAIVER-CODE` PIC X(01).
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                        *   Description: New Waiver State
                *   `P-NEW-INTER-NO` PIC 9(05).
                    *   Description: New Intern Number
                *   `P-