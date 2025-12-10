## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures in the WORKING-STORAGE SECTION, and data structures in the LINKAGE SECTION.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access is evident in the provided code. However, the program utilizes a `COPY` statement (`COPY LTDRG031.`) indicating that it includes data definitions from another file/member named `LTDRG031`.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A character field used for internal program identification or debugging purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description: Stores the version number of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`
        *   Description:  A group of fields to hold various PPS (Prospective Payment System) component values.
            *   `H-LOS` PIC 9(03) - Length of Stay.
            *   `H-REG-DAYS` PIC 9(03) - Regular Days.
            *   `H-TOTAL-DAYS` PIC 9(05) - Total Days.
            *   `H-SSOT` PIC 9(02) - Short Stay Outlier Threshold.
            *   `H-BLEND-RTC` PIC 9(02) - Blend Rate Type Code
            *   `H-BLEND-FAC` PIC 9(01)V9(01) - Blend Facility Portion
            *   `H-BLEND-PPS` PIC 9(01)V9(01) - Blend PPS Portion
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02) - Short Stay Payment Amount.
            *   `H-SS-COST` PIC 9(07)V9(02) - Short Stay Cost.
            *   `H-LABOR-PORTION` PIC 9(07)V9(06) - Labor Portion of the payment.
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06) - Non-Labor Portion of the payment.
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02) - Fixed Loss Amount.
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02) - New Facility Specific Rate.

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  Structure to receive bill-related data from the calling program.
            *   `B-NPI10`
                *   `B-NPI8` PIC X(08) - National Provider Identifier (NPI) - first 8 characters.
                *   `B-NPI-FILLER` PIC X(02) - Filler for NPI.
            *   `B-PROVIDER-NO` PIC X(06) - Provider Number.
            *   `B-PATIENT-STATUS` PIC X(02) - Patient Status.
            *   `B-DRG-CODE` PIC X(03) - Diagnosis Related Group (DRG) Code.
            *   `B-LOS` PIC 9(03) - Length of Stay.
            *   `B-COV-DAYS` PIC 9(03) - Covered Days.
            *   `B-LTR-DAYS` PIC 9(02) - Lifetime Reserve Days.
            *   `B-DISCHARGE-DATE`
                *   `B-DISCHG-CC` PIC 9(02) - Discharge Century/Code.
                *   `B-DISCHG-YY` PIC 9(02) - Discharge Year.
                *   `B-DISCHG-MM` PIC 9(02) - Discharge Month.
                *   `B-DISCHG-DD` PIC 9(02) - Discharge Day.
            *   `B-COV-CHARGES` PIC 9(07)V9(02) - Covered Charges.
            *   `B-SPEC-PAY-IND` PIC X(01) - Special Payment Indicator.
            *   `FILLER` PIC X(13) - Unused space.

    *   `PPS-DATA-ALL`
        *   Description: Structure to return calculated PPS data to the calling program.
            *   `PPS-RTC` PIC 9(02) - Return Code.
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02) - Charge Threshold.
            *   `PPS-DATA`
                *   `PPS-MSA` PIC X(04) - Metropolitan Statistical Area (MSA)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04) - Wage Index.
                *   `PPS-AVG-LOS` PIC 9(02)V9(01) - Average Length of Stay.
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04) - Relative Weight.
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02) - Outlier Payment Amount.
                *   `PPS-LOS` PIC 9(03) - Length of Stay.
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02) - Federal Payment Amount.
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02) - Final Payment Amount.
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02) - Facility Costs.
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02) - New Facility Specific Rate.
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02) - Outlier Threshold.
                *   `PPS-SUBM-DRG-CODE` PIC X(03) - Submitted DRG Code.
                *   `PPS-CALC-VERS-CD` PIC X(05) - Calculation Version Code.
                *   `PPS-REG-DAYS-USED` PIC 9(03) - Regular Days Used.
                *   `PPS-LTR-DAYS-USED` PIC 9(03) - Lifetime Reserve Days Used.
                *   `PPS-BLEND-YEAR` PIC 9(01) - Blend Year.
                *   `PPS-COLA` PIC 9(01)V9(03) - Cost of Living Adjustment.
                *   `FILLER` PIC X(04) - Unused space.
            *   `PPS-OTHER-DATA`
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05) - National Labor Percentage.
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05) - National Non-Labor Percentage.
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02) - Standard Federal Rate.
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03) - Budget Neutrality Rate.
                *   `FILLER` PIC X(20) - Unused space.
            *   `PPS-PC-DATA`
                *   `PPS-COT-IND` PIC X(01) - Cost Outlier Indicator.
                *   `FILLER` PIC X(20) - Unused space.

    *   `PRICER-OPT-VERS-SW`
        *   Description: Switch to indicate whether all tables or just the provider record are passed
            *   `PRICER-OPTION-SW` PIC X(01) - Option switch for Pricer.
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   `PROV-RECORD-PASSED` VALUE 'P'.
            *   `PPS-VERSIONS`
                *   `PPDRV-VERSION` PIC X(05) - Version of the PPDRV (Pricing Driver) program.

    *   `PROV-NEW-HOLD`
        *   Description:  Structure to receive provider-specific data from the calling program.
            *   `PROV-NEWREC-HOLD1`
                *   `P-NEW-NPI10`
                    *   `P-NEW-NPI8` PIC X(08) - New NPI - first 8 characters.
                    *   `P-NEW-NPI-FILLER` PIC X(02) - Filler for New NPI.
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02) - New State.
                    *   `FILLER` PIC X(04) - Unused space.
                *   `P-NEW-DATE-DATA`
                    *   `P-NEW-EFF-DATE`
                        *   `P-NEW-EFF-DT-CC` PIC 9(02) - Effective Date Century/Code.
                        *   `P-NEW-EFF-DT-YY` PIC 9(02) - Effective Date Year.
                        *   `P-NEW-EFF-DT-MM` PIC 9(02) - Effective Date Month.
                        *   `P-NEW-EFF-DT-DD` PIC 9(02) - Effective Date Day.
                    *   `P-NEW-FY-BEGIN-DATE`
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02) - Fiscal Year Begin Date Century/Code.
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02) - Fiscal Year Begin Date Year.
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02) - Fiscal Year Begin Date Month.
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02) - Fiscal Year Begin Date Day.
                    *   `P-NEW-REPORT-DATE`
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02) - Report Date Century/Code.
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02) - Report Date Year.
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02) - Report Date Month.
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02) - Report Date Day.
                    *   `P-NEW-TERMINATION-DATE`
                        *   `P-NEW-TERM-DT-CC` PIC 9(02) - Termination Date Century/Code.
                        *   `P-NEW-TERM-DT-YY` PIC 9(02) - Termination Date Year.
                        *   `P-NEW-TERM-DT-MM` PIC 9(02) - Termination Date Month.
                        *   `P-NEW-TERM-DT-DD` PIC 9(02) - Termination Date Day.
                *   `P-NEW-WAIVER-CODE` PIC X(01) - Waiver Code.
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                *   `P-NEW-INTER-NO` PIC 9(05) - Internal Number.
                *   `P-NEW-PROVIDER-TYPE` PIC X(02) - Provider Type.
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01) - Current Census Division.
                *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01) - Current Division.
                *   `P-NEW-MSA-DATA`
                    *   `P-NEW-CHG-CODE-INDEX` PIC X - Charge Code Index.
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT. - Geo Location MSA.
                    *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04) - Geo Location MSA - numeric.
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT. - Wage Index Location MSA.
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT. - Standard Amount Location MSA.
                    *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                        *   `P-NEW-RURAL-1ST`
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                            *   `P-NEW-RURAL-2ND` PIC XX.
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   `P-NEW-LUGAR` PIC X - Lugar.
                *   `P-NEW-TEMP-RELIEF-IND` PIC X - Temporary Relief Indicator.
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X - Federal PPS Blend Indicator.
                *   `FILLER` PIC X(05) - Unused space.
            *   `PROV-NEWREC-HOLD2`
                *   `P-NEW-VARIABLES`
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02) - New Facility Specific Rate.
                    *   `P-NEW-COLA` PIC 9(01)V9(03) - Cost of Living Adjustment.
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04) - Intern Ratio.
                    *   `P-NEW-BED-SIZE` PIC 9(05) - Bed Size.
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03) - Operating Cost-to-Charge Ratio.
                    *   `P-NEW-CMI` PIC 9(01)V9(04) - Case Mix Index.
                    *   `P-NEW-SSI-RATIO` PIC V9(04) - Supplemental Security Income Ratio.
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04) - Medicaid Ratio.
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01) - PPS Blend Year Indicator.
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05) - Provider Update Factor.
                    *   `P-NEW-DSH-PERCENT` PIC V9(04) - Disproportionate Share Hospital (DSH) Percentage.
                    *   `P-NEW-FYE-DATE` PIC X(08) - Fiscal Year End Date.
                *   `FILLER` PIC X(23) - Unused space.
            *   `PROV-NEWREC-HOLD3`
                *   `P-NEW-PASS-AMT-DATA`
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99 - Passed Amount for Capital.
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99 - Passed Amount for Direct Medical Education.
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99 - Passed Amount for Organ Acquisition.
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99 - Passed Amount for Plus Miscellaneous.
                *   `P-NEW-CAPI-DATA`
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X - Capital PPS Payment Code.
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99 - Capital Hospital Specific Rate.
                    *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99 - Capital Old Harm Rate.
                    *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999 - Capital New Harm Ratio.
                    *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999 - Capital Cost-to-Charge Ratio.
                    *   `P-NEW-CAPI-NEW-HOSP` PIC X - Capital New Hospital.
                    *   `P-NEW-CAPI-IME` PIC 9V9999 - Capital Indirect Medical Education.
                    *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99 - Capital Exceptions.
                *   `FILLER` PIC X(22) - Unused space.

    *   `WAGE-NEW-INDEX-RECORD`
        *   Description: Structure to receive wage index data from the calling program.
            *   `W-MSA` PIC X(4) - MSA.
            *   `W-EFF-DATE` PIC X(8) - Effective Date.
            *   `W-WAGE-INDEX1` PIC S9(02)V9(04) - Wage Index 1.
            *   `W-WAGE-INDEX2` PIC S9(02)V9(04) - Wage Index 2.
            *   `W-WAGE-INDEX3` PIC S9(02)V9(04) - Wage Index 3.

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access is evident in the provided code. However, the program utilizes a `COPY` statement (`COPY LTDRG031.`) indicating that it includes data definitions from another file/member named `LTDRG031`.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A character field used for internal program identification or debugging purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Stores the version number of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`
        *   Description:  A group of fields to hold various PPS (Prospective Payment System) component values.
            *   `H-LOS` PIC 9(03) - Length of Stay.
            *   `H-REG-DAYS` PIC 9(03) - Regular Days.
            *   `H-TOTAL-DAYS` PIC 9(05) - Total Days.
            *   `H-SSOT` PIC 9(02) - Short Stay Outlier Threshold.
            *   `H-BLEND-RTC` PIC 9(02) - Blend Rate Type Code
            *   `H-BLEND-FAC` PIC 9(01)V9(01) - Blend Facility Portion
            *   `H-BLEND-PPS` PIC 9(01)V9(01) - Blend PPS Portion
            *   `H-SS-PAY-AMT` PIC 9(07)V9(02) - Short Stay Payment Amount.
            *   `H-SS-COST` PIC 9(07)V9(02) - Short Stay Cost.
            *   `H-LABOR-PORTION` PIC 9(07)V9(06) - Labor Portion of the payment.
            *   `H-NONLABOR-PORTION` PIC 9(07)V9(06) - Non-Labor Portion of the payment.
            *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02) - Fixed Loss Amount.
            *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02) - New Facility Specific Rate.
            *   `H-LOS-RATIO` PIC 9(01)V9(05) - Length of Stay Ratio.

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description:  Structure to receive bill-related data from the calling program.
            *   `B-NPI10`
                *   `B-NPI8` PIC X(08) - National Provider Identifier (NPI) - first 8 characters.
                *   `B-NPI-FILLER` PIC X(02) - Filler for NPI.
            *   `B-PROVIDER-NO` PIC X(06) - Provider Number.
            *   `B-PATIENT-STATUS` PIC X(02) - Patient Status.
            *   `B-DRG-CODE` PIC X(03) - Diagnosis Related Group (DRG) Code.
            *   `B-LOS` PIC 9(03) - Length of Stay.
            *   `B-COV-DAYS` PIC 9(03) - Covered Days.
            *   `B-LTR-DAYS` PIC 9(02) - Lifetime Reserve Days.
            *   `B-DISCHARGE-DATE`
                *   `B-DISCHG-CC` PIC 9(02) - Discharge Century/Code.
                *   `B-DISCHG-YY` PIC 9(02) - Discharge Year.
                *   `B-DISCHG-MM` PIC 9(02) - Discharge Month.
                *   `B-DISCHG-DD` PIC 9(02) - Discharge Day.
            *   `B-COV-CHARGES` PIC 9(07)V9(02) - Covered Charges.
            *   `B-SPEC-PAY-IND` PIC X(01) - Special Payment Indicator.
            *   `FILLER` PIC X(13) - Unused space.

    *   `PPS-DATA-ALL`
        *   Description: Structure to return calculated PPS data to the calling program.
            *   `PPS-RTC` PIC 9(02) - Return Code.
            *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02) - Charge Threshold.
            *   `PPS-DATA`
                *   `PPS-MSA` PIC X(04) - Metropolitan Statistical Area (MSA)
                *   `PPS-WAGE-INDEX` PIC 9(02)V9(04) - Wage Index.
                *   `PPS-AVG-LOS` PIC 9(02)V9(01) - Average Length of Stay.
                *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04) - Relative Weight.
                *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02) - Outlier Payment Amount.
                *   `PPS-LOS` PIC 9(03) - Length of Stay.
                *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
                *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02) - Federal Payment Amount.
                *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02) - Final Payment Amount.
                *   `PPS-FAC-COSTS` PIC 9(07)V9(02) - Facility Costs.
                *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02) - New Facility Specific Rate.
                *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02) - Outlier Threshold.
                *   `PPS-SUBM-DRG-CODE` PIC X(03) - Submitted DRG Code.
                *   `PPS-CALC-VERS-CD` PIC X(05) - Calculation Version Code.
                *   `PPS-REG-DAYS-USED` PIC 9(03) - Regular Days Used.
                *   `PPS-LTR-DAYS-USED` PIC 9(03) - Lifetime Reserve Days Used.
                *   `PPS-BLEND-YEAR` PIC 9(01) - Blend Year.
                *   `PPS-COLA` PIC 9(01)V9(03) - Cost of Living Adjustment.
                *   `FILLER` PIC X(04) - Unused space.
            *   `PPS-OTHER-DATA`
                *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05) - National Labor Percentage.
                *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05) - National Non-Labor Percentage.
                *   `PPS-STD-FED-RATE` PIC 9(05)V9(02) - Standard Federal Rate.
                *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03) - Budget Neutrality Rate.
                *   `FILLER` PIC X(20) - Unused space.
            *   `PPS-PC-DATA`
                *   `PPS-COT-IND` PIC X(01) - Cost Outlier Indicator.
                *   `FILLER` PIC X(20) - Unused space.

    *   `PRICER-OPT-VERS-SW`
        *   Description: Switch to indicate whether all tables or just the provider record are passed
            *   `PRICER-OPTION-SW` PIC X(01) - Option switch for Pricer.
                *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   `PROV-RECORD-PASSED` VALUE 'P'.
            *   `PPS-VERSIONS`
                *   `PPDRV-VERSION` PIC X(05) - Version of the PPDRV (Pricing Driver) program.

    *   `PROV-NEW-HOLD`
        *   Description:  Structure to receive provider-specific data from the calling program.
            *   `PROV-NEWREC-HOLD1`
                *   `P-NEW-NPI10`
                    *   `P-NEW-NPI8` PIC X(08) - New NPI - first 8 characters.
                    *   `P-NEW-NPI-FILLER` PIC X(02) - Filler for New NPI.
                *   `P-NEW-PROVIDER-NO`
                    *   `P-NEW-STATE` PIC 9(02) - New State.
                    *   `FILLER` PIC X(04) - Unused space.
                *   `P-NEW-DATE-DATA`
                    *   `P-NEW-EFF-DATE`
                        *   `P-NEW-EFF-DT-CC` PIC 9(02) - Effective Date Century/Code.
                        *   `P-NEW-EFF-DT-YY` PIC 9(02) - Effective Date Year.
                        *   `P-NEW-EFF-DT-MM` PIC 9(02) - Effective Date Month.
                        *   `P-NEW-EFF-DT-DD` PIC 9(02) - Effective Date Day.
                    *   `P-NEW-FY-BEGIN-DATE`
                        *   `P-NEW-FY-BEG-DT-CC` PIC 9(02) - Fiscal Year Begin Date Century/Code.
                        *   `P-NEW-FY-BEG-DT-YY` PIC 9(02) - Fiscal Year Begin Date Year.
                        *   `P-NEW-FY-BEG-DT-MM` PIC 9(02) - Fiscal Year Begin Date Month.
                        *   `P-NEW-FY-BEG-DT-DD` PIC 9(02) - Fiscal Year Begin Date Day.
                    *   `P-NEW-REPORT-DATE`
                        *   `P-NEW-REPORT-DT-CC` PIC 9(02) - Report Date Century/Code.
                        *   `P-NEW-REPORT-DT-YY` PIC 9(02) - Report Date Year.
                        *   `P-NEW-REPORT-DT-MM` PIC 9(02) - Report Date Month.
                        *   `P-NEW-REPORT-DT-DD` PIC 9(02) - Report Date Day.
                    *   `P-NEW-TERMINATION-DATE`
                        *   `P-NEW-TERM-DT-CC` PIC 9(02) - Termination Date Century/Code.
                        *   `P-NEW-TERM-DT-YY` PIC 9(02) - Termination Date Year.
                        *   `P-NEW-TERM-DT-MM` PIC 9(02) - Termination Date Month.
                        *   `P-NEW-TERM-DT-DD` PIC 9(02) - Termination Date Day.
                *   `P-NEW-WAIVER-CODE` PIC X(01) - Waiver Code.
                    *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                *   `P-NEW-INTER-NO` PIC 9(05) - Internal Number.
                *   `P-NEW-PROVIDER-TYPE` PIC X(02) - Provider Type.
                *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01) - Current Census Division.
                *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01) - Current Division.
                *   `P-NEW-MSA-DATA`
                    *   `P-NEW-CHG-CODE-INDEX` PIC X - Charge Code Index.
                    *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT. - Geo Location MSA.
                    *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04) - Geo Location MSA - numeric.
                    *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT. - Wage Index Location MSA.
                    *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT. - Standard Amount Location MSA.
                    *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                        *   `P-NEW-RURAL-1ST`
                            *   `P-NEW-STAND-RURAL` PIC XX.
                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                            *   `P-NEW-RURAL-2ND` PIC XX.
                *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   `P-NEW-LUGAR` PIC X - Lugar.
                *   `P-NEW-TEMP-RELIEF-IND` PIC X - Temporary Relief Indicator.
                *   `P-NEW-FED-PPS-BLEND-IND` PIC X - Federal PPS Blend Indicator.
                *   `FILLER` PIC X(05) - Unused space.
            *   `PROV-NEWREC-HOLD2`
                *   `P-NEW-VARIABLES`
                    *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02) - New Facility Specific Rate.
                    *   `P-NEW-COLA` PIC 9(01)V9(03) - Cost of Living Adjustment.
                    *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04) - Intern Ratio.
                    *   `P-NEW-BED-SIZE` PIC 9(05) - Bed Size.
                    *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03) - Operating Cost-to-Charge Ratio.
                    *   `P-NEW-CMI` PIC 9(01)V9(04) - Case Mix Index.
                    *   `P-NEW-SSI-RATIO` PIC V9(04) - Supplemental Security Income Ratio.
                    *   `P-NEW-MEDICAID-RATIO` PIC V9(04) - Medicaid Ratio.
                    *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01) - PPS Blend Year Indicator.
                    *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05) - Provider Update Factor.
                    *   `P-NEW-DSH-PERCENT` PIC V9(04) - Disproportionate Share Hospital (DSH) Percentage.
                    *   `P-NEW-FYE-DATE` PIC X(08) - Fiscal Year End Date.
                *   `FILLER` PIC X(23) - Unused space.
            *   `PROV-NEWREC-HOLD3`
                *   `P-NEW-PASS-AMT-DATA`
                    *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99 - Passed Amount for Capital.
                    *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99 - Passed Amount for Direct Medical Education.
                    *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99 - Passed Amount for Organ Acquisition.
                    *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99 - Passed Amount for Plus Miscellaneous.
                *   `P-NEW-CAPI-DATA`
                    *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X - Capital PPS Payment Code.
                    *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99 - Capital Hospital Specific Rate.
                    