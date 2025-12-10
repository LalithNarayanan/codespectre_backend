Here's an analysis of each COBOL program, detailing the files accessed, data structures in WORKING-STORAGE, and data structures in LINKAGE SECTION.

**Program: LTCAL032**

*   **Files Accessed:**
    *   No files are explicitly opened or read in this program. However, it uses a `COPY` statement to include the `LTDRG031` code, which presumably contains data.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for program identification or debugging purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Indicates the version of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`
        *   Description: This group contains calculated intermediate values related to the Prospective Payment System (PPS) calculation.
        *   `H-LOS` PIC 9(03). - Length of Stay
        *   `H-REG-DAYS` PIC 9(03). - Regular Days
        *   `H-TOTAL-DAYS` PIC 9(05). - Total Days
        *   `H-SSOT` PIC 9(02). - Short Stay Outlier Threshold
        *   `H-BLEND-RTC` PIC 9(02). - Blend year return code
        *   `H-BLEND-FAC` PIC 9(01)V9(01). - Blend facility rate
        *   `H-BLEND-PPS` PIC 9(01)V9(01). - Blend PPS rate
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). - Short Stay Payment Amount
        *   `H-SS-COST` PIC 9(07)V9(02). - Short Stay Cost
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). - Labor Portion of payment
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). - Non-labor portion of payment
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). - Fixed Loss Amount
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - Facility Specific Rate

    *   Data structures defined in the `COPY LTDRG031.`
        *   Description: This is a copybook that contains a DRG (Diagnosis Related Group) table.
        *   `W-DRG-FILLS` Contains DRG data.
        *   `W-DRG-TABLE` Redefines `W-DRG-FILLS`
        *   `WWM-ENTRY` OCCURS 502 TIMES.
            *   `WWM-DRG` PIC X(3). - DRG code
            *   `WWM-RELWT` PIC 9(1)V9(4). - Relative Weight
            *   `WWM-ALOS` PIC 9(2)V9(1). - Average Length of Stay

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description: This is the main input data structure passed from the calling program, representing the billing information.
        *   `B-NPI10`
            *   `B-NPI8` PIC X(08). - National Provider Identifier (NPI) - first 8 digits
            *   `B-NPI-FILLER` PIC X(02). - National Provider Identifier (NPI) - last 2 digits
        *   `B-PROVIDER-NO` PIC X(06). - Provider Number
        *   `B-PATIENT-STATUS` PIC X(02). - Patient Status
        *   `B-DRG-CODE` PIC X(03). - DRG Code
        *   `B-LOS` PIC 9(03). - Length of Stay
        *   `B-COV-DAYS` PIC 9(03). - Covered Days
        *   `B-LTR-DAYS` PIC 9(02). - Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` PIC 9(02). - Century of Discharge Date
            *   `B-DISCHG-YY` PIC 9(02). - Year of Discharge Date
            *   `B-DISCHG-MM` PIC 9(02). - Month of Discharge Date
            *   `B-DISCHG-DD` PIC 9(02). - Day of Discharge Date
        *   `B-COV-CHARGES` PIC 9(07)V9(02). - Covered Charges
        *   `B-SPEC-PAY-IND` PIC X(01). - Special Payment Indicator
        *   `FILLER` PIC X(13). - Unused field

    *   `PPS-DATA-ALL`
        *   Description: This is the main output data structure, which passes the calculated PPS data back to the calling program.
        *   `PPS-RTC` PIC 9(02). - Return Code
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). - Charge Threshold
        *   `PPS-DATA`
            *   `PPS-MSA` PIC X(04). - Metropolitan Statistical Area
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). - Wage Index
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). - Average Length of Stay
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). - Relative Weight
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). - Outlier Payment Amount
            *   `PPS-LOS` PIC 9(03). - Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). - DRG Adjusted Payment Amount
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). - Federal Payment Amount
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). - Final Payment Amount
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). - Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). - New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). - Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` PIC X(03). - Submitted DRG Code
            *   `PPS-CALC-VERS-CD` PIC X(05). - Calculation Version Code
            *   `PPS-REG-DAYS-USED` PIC 9(03). - Regular Days Used
            *   `PPS-LTR-DAYS-USED` PIC 9(03). - Lifetime Reserve Days Used
            *   `PPS-BLEND-YEAR` PIC 9(01). - Blend Year
            *   `PPS-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment
            *   `FILLER` PIC X(04). - Unused field
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). - National Labor Percentage
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). - National Non-Labor Percentage
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). - Standard Federal Rate
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). - Budget Neutrality Rate
            *   `FILLER` PIC X(20). - Unused field
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` PIC X(01). - Cost Outlier Indicator
            *   `FILLER` PIC X(20). - Unused field

    *   `PRICER-OPT-VERS-SW`
        *   Description:  Contains flags to pass different versions of the LTDRV programs.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   `ALL-TABLES-PASSED` VALUE 'A'.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` PIC X(05).

    *   `PROV-NEW-HOLD`
        *   Description: This structure holds provider-specific information.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` PIC X(08).
                *   `P-NEW-NPI-FILLER` PIC X(02).
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` PIC 9(02).
                *   `FILLER` PIC X(04).
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
            *   `P-NEW-INTER-NO` PIC 9(05).
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                        *   `P-NEW-RURAL-2ND` PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
            *   `P-NEW-LUGAR` PIC X.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
            *   `FILLER` PIC X(05).
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                *   `P-NEW-BED-SIZE` PIC 9(05).
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                *   `P-NEW-FYE-DATE` PIC X(08).
            *   `FILLER` PIC X(23).
        *   `PROV-NEWREC-HOLD3`
            *   `P-NEW-PASS-AMT-DATA`
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
            *   `P-NEW-CAPI-DATA`
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
            *   `FILLER` PIC X(22).

    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This structure holds wage index information.
        *   `W-MSA` PIC X(4). - MSA (Metropolitan Statistical Area)
        *   `W-EFF-DATE` PIC X(8). - Effective Date
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04). - Wage Index
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04). - Wage Index
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04). - Wage Index

**Program: LTCAL042**

*   **Files Accessed:**
    *   No files are explicitly opened or read in this program. However, it uses a `COPY` statement to include the `LTDRG031` code, which presumably contains data.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for program identification or debugging purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Indicates the version of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`
        *   Description: This group contains calculated intermediate values related to the Prospective Payment System (PPS) calculation.
        *   `H-LOS` PIC 9(03). - Length of Stay
        *   `H-REG-DAYS` PIC 9(03). - Regular Days
        *   `H-TOTAL-DAYS` PIC 9(05). - Total Days
        *   `H-SSOT` PIC 9(02). - Short Stay Outlier Threshold
        *   `H-BLEND-RTC` PIC 9(02). - Blend year return code
        *   `H-BLEND-FAC` PIC 9(01)V9(01). - Blend facility rate
        *   `H-BLEND-PPS` PIC 9(01)V9(01). - Blend PPS rate
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). - Short Stay Payment Amount
        *   `H-SS-COST` PIC 9(07)V9(02). - Short Stay Cost
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). - Labor Portion of payment
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). - Non-labor portion of payment
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). - Fixed Loss Amount
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - Facility Specific Rate
        *   `H-LOS-RATIO` PIC 9(01)V9(05). - Length of Stay Ratio

    *   Data structures defined in the `COPY LTDRG031.`
        *   Description: This is a copybook that contains a DRG (Diagnosis Related Group) table.
        *   `W-DRG-FILLS` Contains DRG data.
        *   `W-DRG-TABLE` Redefines `W-DRG-FILLS`
        *   `WWM-ENTRY` OCCURS 502 TIMES.
            *   `WWM-DRG` PIC X(3). - DRG code
            *   `WWM-RELWT` PIC 9(1)V9(4). - Relative Weight
            *   `WWM-ALOS` PIC 9(2)V9(1). - Average Length of Stay

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`
        *   Description: This is the main input data structure passed from the calling program, representing the billing information.
        *   `B-NPI10`
            *   `B-NPI8` PIC X(08). - National Provider Identifier (NPI) - first 8 digits
            *   `B-NPI-FILLER` PIC X(02). - National Provider Identifier (NPI) - last 2 digits
        *   `B-PROVIDER-NO` PIC X(06). - Provider Number
        *   `B-PATIENT-STATUS` PIC X(02). - Patient Status
        *   `B-DRG-CODE` PIC X(03). - DRG Code
        *   `B-LOS` PIC 9(03). - Length of Stay
        *   `B-COV-DAYS` PIC 9(03). - Covered Days
        *   `B-LTR-DAYS` PIC 9(02). - Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` PIC 9(02). - Century of Discharge Date
            *   `B-DISCHG-YY` PIC 9(02). - Year of Discharge Date
            *   `B-DISCHG-MM` PIC 9(02). - Month of Discharge Date
            *   `B-DISCHG-DD` PIC 9(02). - Day of Discharge Date
        *   `B-COV-CHARGES` PIC 9(07)V9(02). - Covered Charges
        *   `B-SPEC-PAY-IND` PIC X(01). - Special Payment Indicator
        *   `FILLER` PIC X(13). - Unused field

    *   `PPS-DATA-ALL`
        *   Description: This is the main output data structure, which passes the calculated PPS data back to the calling program.
        *   `PPS-RTC` PIC 9(02). - Return Code
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). - Charge Threshold
        *   `PPS-DATA`
            *   `PPS-MSA` PIC X(04). - Metropolitan Statistical Area
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). - Wage Index
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). - Average Length of Stay
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). - Relative Weight
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). - Outlier Payment Amount
            *   `PPS-LOS` PIC 9(03). - Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). - DRG Adjusted Payment Amount
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). - Federal Payment Amount
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). - Final Payment Amount
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). - Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). - New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). - Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` PIC X(03). - Submitted DRG Code
            *   `PPS-CALC-VERS-CD` PIC X(05). - Calculation Version Code
            *   `PPS-REG-DAYS-USED` PIC 9(03). - Regular Days Used
            *   `PPS-LTR-DAYS-USED` PIC 9(03). - Lifetime Reserve Days Used
            *   `PPS-BLEND-YEAR` PIC 9(01). - Blend Year
            *   `PPS-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment
            *   `FILLER` PIC X(04). - Unused field
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). - National Labor Percentage
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). - National Non-Labor Percentage
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). - Standard Federal Rate
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). - Budget Neutrality Rate
            *   `FILLER` PIC X(20). - Unused field
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` PIC X(01). - Cost Outlier Indicator
            *   `FILLER` PIC X(20). - Unused field

    *   `PRICER-OPT-VERS-SW`
        *   Description:  Contains flags to pass different versions of the LTDRV programs.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   `ALL-TABLES-PASSED` VALUE 'A'.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` PIC X(05).

    *   `PROV-NEW-HOLD`
        *   Description: This structure holds provider-specific information.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` PIC X(08).
                *   `P-NEW-NPI-FILLER` PIC X(02).
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` PIC 9(02).
                *   `FILLER` PIC X(04).
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
            *   `P-NEW-INTER-NO` PIC 9(05).
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                        *   `P-NEW-RURAL-2ND` PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
            *   `P-NEW-LUGAR` PIC X.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
            *   `FILLER` PIC X(05).
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                *   `P-NEW-BED-SIZE` PIC 9(05).
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                *   `P-NEW-FYE-DATE` PIC X(08).
            *   `FILLER` PIC X(23).
        *   `PROV-NEWREC-HOLD3`
            *   `P-NEW-PASS-AMT-DATA`
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
            *   `P-NEW-CAPI-DATA`
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
            *   `FILLER` PIC X(22).

    *   `WAGE-NEW-INDEX-RECORD`
        *   Description:  This structure holds wage index information.
        *   `W-MSA` PIC X(4). - MSA (Metropolitan Statistical Area)
        *   `W-EFF-DATE` PIC X(8). - Effective Date
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04). - Wage Index
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04). - Wage Index
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04). - Wage Index

**Program: LTDRG031**

*   **Files Accessed:**
    *   No files are explicitly opened or read in this program. This is a data copybook.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-DRG-FILLS`
        *   Description: This contains a repeating set of data, where each set of 44 bytes represents a row of the DRG table.
        *   PIC X(44) - repeated multiple times.
    *   `W-DRG-TABLE` RED