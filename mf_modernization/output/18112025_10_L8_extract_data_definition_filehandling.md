Here's the analysis of each COBOL program, detailing the files accessed, data structures in the WORKING-STORAGE SECTION, and data structures in the LINKAGE SECTION:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, it's likely that this program interacts with data through the `COPY` statement, which includes the definitions of the DRG table (LTDRG031).
*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` - PIC X(46) - Value: 'LTCAL032 - W O R K I N G S T O R A G E'.  This is a descriptive field, probably for debugging purposes, identifying the program and the storage area.
    *   `CAL-VERSION` - PIC X(05) - Value: 'C03.2'.  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` - A group item used to store various PPS (Prospective Payment System) related calculated values.
        *   `H-LOS` - PIC 9(03) - Length of Stay, in days.
        *   `H-REG-DAYS` - PIC 9(03) - Regular Days, in days.
        *   `H-TOTAL-DAYS` - PIC 9(05) - Total Days, in days.
        *   `H-SSOT` - PIC 9(02) - Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` - PIC 9(02) - Blend Rate Type Code - Indicates the blend year.
        *   `H-BLEND-FAC` - PIC 9(01)V9(01) - Blend Facility Rate Percentage.
        *   `H-BLEND-PPS` - PIC 9(01)V9(01) - Blend PPS Rate Percentage.
        *   `H-SS-PAY-AMT` - PIC 9(07)V9(02) - Short Stay Payment Amount.
        *   `H-SS-COST` - PIC 9(07)V9(02) - Short Stay Cost.
        *   `H-LABOR-PORTION` - PIC 9(07)V9(06) - Labor Portion of the payment.
        *   `H-NONLABOR-PORTION` - PIC 9(07)V9(06) - Non-Labor Portion of the payment.
        *   `H-FIXED-LOSS-AMT` - PIC 9(07)V9(02) - Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` - PIC 9(05)V9(02) - New Facility Specific Rate.
*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA` - This is the input data structure, passed from the calling program, containing billing information.
        *   `B-NPI10` - National Provider Identifier (NPI) - 10 digits
            *   `B-NPI8` - PIC X(08) - The first 8 digits of the NPI.
            *   `B-NPI-FILLER` - PIC X(02) - Filler for the last 2 digits of the NPI.
        *   `B-PROVIDER-NO` - PIC X(06) - Provider Number.
        *   `B-PATIENT-STATUS` - PIC X(02) - Patient Status.
        *   `B-DRG-CODE` - PIC X(03) - DRG (Diagnosis Related Group) Code.
        *   `B-LOS` - PIC 9(03) - Length of Stay (in days).
        *   `B-COV-DAYS` - PIC 9(03) - Covered Days.
        *   `B-LTR-DAYS` - PIC 9(02) - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE` - Discharge Date.
            *   `B-DISCHG-CC` - PIC 9(02) - Century Code.
            *   `B-DISCHG-YY` - PIC 9(02) - Year.
            *   `B-DISCHG-MM` - PIC 9(02) - Month.
            *   `B-DISCHG-DD` - PIC 9(02) - Day.
        *   `B-COV-CHARGES` - PIC 9(07)V9(02) - Covered Charges.
        *   `B-SPEC-PAY-IND` - PIC X(01) - Special Payment Indicator.
        *   `FILLER` - PIC X(13) - Unused space
    *   `PPS-DATA-ALL` - This is the output data structure, passed back to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` - PIC 9(02) - Return Code - Indicates the reason for the payment or why it was not paid.
        *   `PPS-CHRG-THRESHOLD` - PIC 9(07)V9(02) - Charge Threshold.
        *   `PPS-DATA` - Group item containing the PPS related data.
            *   `PPS-MSA` - PIC X(04) - MSA (Metropolitan Statistical Area) code.
            *   `PPS-WAGE-INDEX` - PIC 9(02)V9(04) - Wage Index.
            *   `PPS-AVG-LOS` - PIC 9(02)V9(01) - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` - PIC 9(01)V9(04) - Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` - PIC 9(07)V9(02) - Outlier Payment Amount.
            *   `PPS-LOS` - PIC 9(03) - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` - PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` - PIC 9(07)V9(02) - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` - PIC 9(07)V9(02) - Final Payment Amount.
            *   `PPS-FAC-COSTS` - PIC 9(07)V9(02) - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` - PIC 9(07)V9(02) - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` - PIC 9(07)V9(02) - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` - PIC X(03) - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` - PIC X(05) - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` - PIC 9(03) - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` - PIC 9(03) - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` - PIC 9(01) - Blend Year.
            *   `PPS-COLA` - PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   `FILLER` - PIC X(04) - Unused space.
        *   `PPS-OTHER-DATA` - Group item with other PPS related data
            *   `PPS-NAT-LABOR-PCT` - PIC 9(01)V9(05) - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` - PIC 9(01)V9(05) - National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` - PIC 9(05)V9(02) - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` - PIC 9(01)V9(03) - Budget Neutrality Rate.
            *   `FILLER` - PIC X(20) - Unused space.
        *   `PPS-PC-DATA` - Group item with PPS related data.
            *   `PPS-COT-IND` - PIC X(01) - Cost Outlier Indicator.
            *   `FILLER` - PIC X(20) - Unused space.
    *   `PRICER-OPT-VERS-SW` - This structure probably indicates which version of the pricer options to use.
        *   `PRICER-OPTION-SW` - PIC X(01) - Option switch.
            *   `ALL-TABLES-PASSED` - VALUE 'A'.
            *   `PROV-RECORD-PASSED` - VALUE 'P'.
        *   `PPS-VERSIONS` - Group item for the versions of the programs.
            *   `PPDRV-VERSION` - PIC X(05) - Version of the PPDRV program.
    *   `PROV-NEW-HOLD` - This is the provider record data, passed from the calling program.
        *   `PROV-NEWREC-HOLD1` - Group item for the provider record.
            *   `P-NEW-NPI10` - NPI Data
                *   `P-NEW-NPI8` - PIC X(08) - The first 8 digits of the NPI.
                *   `P-NEW-NPI-FILLER` - PIC X(02) - Filler for the last 2 digits of the NPI.
            *   `P-NEW-PROVIDER-NO` - Provider Number
                *   `P-NEW-STATE` - PIC 9(02) - State Code.
                *   `FILLER` - PIC X(04) - Unused space.
            *   `P-NEW-DATE-DATA` - Date Data
                *   `P-NEW-EFF-DATE` - Effective Date.
                    *   `P-NEW-EFF-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-EFF-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-EFF-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-EFF-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-FY-BEGIN-DATE` - Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-FY-BEG-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-FY-BEG-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-FY-BEG-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-REPORT-DATE` - Report Date.
                    *   `P-NEW-REPORT-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-REPORT-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-REPORT-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-REPORT-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-TERMINATION-DATE` - Termination Date.
                    *   `P-NEW-TERM-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-TERM-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-TERM-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-TERM-DT-DD` - PIC 9(02) - Day.
            *   `P-NEW-WAIVER-CODE` - PIC X(01) - Waiver Code.
                *   `P-NEW-WAIVER-STATE` - VALUE 'Y'.
            *   `P-NEW-INTER-NO` - PIC 9(05) - Intern Number.
            *   `P-NEW-PROVIDER-TYPE` - PIC X(02) - Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` - PIC 9(01) - Current Census Division.
            *   `P-NEW-CURRENT-DIV` - PIC 9(01) - Redefines `P-NEW-CURRENT-CENSUS-DIV`.
            *   `P-NEW-MSA-DATA` - MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` - PIC X - Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` - PIC X(04) - Geographic Location MSA, right-justified.
                *   `P-NEW-GEO-LOC-MSA9` - PIC 9(04) - Redefines `P-NEW-GEO-LOC-MSAX`.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - PIC X(04) - Wage Index Location MSA, right-justified.
                *   `P-NEW-STAND-AMT-LOC-MSA` - PIC X(04) - Standard Amount Location MSA, right-justified.
                *   `P-NEW-STAND-AMT-LOC-MSA9` - Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                    *   `P-NEW-RURAL-1ST` - Rural Indicator.
                        *   `P-NEW-STAND-RURAL` - PIC XX.
                        *   `P-NEW-STD-RURAL-CHECK` - VALUE '  '.
                    *   `P-NEW-RURAL-2ND` - PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - PIC XX.
            *   `P-NEW-LUGAR` - PIC X.
            *   `P-NEW-TEMP-RELIEF-IND` - PIC X.
            *   `P-NEW-FED-PPS-BLEND-IND` - PIC X.
            *   `FILLER` - PIC X(05) - Unused Space.
        *   `PROV-NEWREC-HOLD2` - Group item for the provider record.
            *   `P-NEW-VARIABLES` - Group item for the provider record.
                *   `P-NEW-FAC-SPEC-RATE` - PIC 9(05)V9(02) - Facility Specific Rate.
                *   `P-NEW-COLA` - PIC 9(01)V9(03) - Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` - PIC 9(01)V9(04) - Intern Ratio.
                *   `P-NEW-BED-SIZE` - PIC 9(05) - Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` - PIC 9(01)V9(03) - Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` - PIC 9(01)V9(04) - Case Mix Index.
                *   `P-NEW-SSI-RATIO` - PIC V9(04) - SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` - PIC V9(04) - Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` - PIC 9(01) - PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` - PIC 9(01)V9(05) - Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` - PIC V9(04) - DSH Percentage.
                *   `P-NEW-FYE-DATE` - PIC X(08) - Fiscal Year End Date.
            *   `FILLER` - PIC X(23) - Unused space.
        *   `PROV-NEWREC-HOLD3` - Group item for the provider record.
            *   `P-NEW-PASS-AMT-DATA` - Group item for the provider record.
                *   `P-NEW-PASS-AMT-CAPITAL` - PIC 9(04)V99 - Passed Amount - Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` - PIC 9(04)V99 - Passed Amount - Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` - PIC 9(04)V99 - Passed Amount - Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` - PIC 9(04)V99 - Passed Amount - Plus Miscellaneous.
            *   `P-NEW-CAPI-DATA` - Group item for the provider record.
                *   `P-NEW-CAPI-PPS-PAY-CODE` - PIC X - Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` - PIC 9(04)V99 - Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` - PIC 9(04)V99 - Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` - PIC 9(01)V9999 - Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` - PIC 9V999 - Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` - PIC X - Capital New Hospital.
                *   `P-NEW-CAPI-IME` - PIC 9V9999 - Capital IME.
                *   `P-NEW-CAPI-EXCEPTIONS` - PIC 9(04)V99 - Capital Exceptions.
            *   `FILLER` - PIC X(22) - Unused space.
    *   `WAGE-NEW-INDEX-RECORD` - This is the wage index record, passed from the calling program.
        *   `W-MSA` - PIC X(4) - MSA Code.
        *   `W-EFF-DATE` - PIC X(8) - Effective Date.
        *   `W-WAGE-INDEX1` - PIC S9(02)V9(04) - Wage Index 1.
        *   `W-WAGE-INDEX2` - PIC S9(02)V9(04) - Wage Index 2.
        *   `W-WAGE-INDEX3` - PIC S9(02)V9(04) - Wage Index 3.

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, it's likely that this program interacts with data through the `COPY` statement, which includes the definitions of the DRG table (LTDRG031).
*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` - PIC X(46) - Value: 'LTCAL042 - W O R K I N G S T O R A G E'.  This is a descriptive field, probably for debugging purposes, identifying the program and the storage area.
    *   `CAL-VERSION` - PIC X(05) - Value: 'C04.2'.  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS` - A group item used to store various PPS (Prospective Payment System) related calculated values.
        *   `H-LOS` - PIC 9(03) - Length of Stay, in days.
        *   `H-REG-DAYS` - PIC 9(03) - Regular Days, in days.
        *   `H-TOTAL-DAYS` - PIC 9(05) - Total Days, in days.
        *   `H-SSOT` - PIC 9(02) - Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` - PIC 9(02) - Blend Rate Type Code - Indicates the blend year.
        *   `H-BLEND-FAC` - PIC 9(01)V9(01) - Blend Facility Rate Percentage.
        *   `H-BLEND-PPS` - PIC 9(01)V9(01) - Blend PPS Rate Percentage.
        *   `H-SS-PAY-AMT` - PIC 9(07)V9(02) - Short Stay Payment Amount.
        *   `H-SS-COST` - PIC 9(07)V9(02) - Short Stay Cost.
        *   `H-LABOR-PORTION` - PIC 9(07)V9(06) - Labor Portion of the payment.
        *   `H-NONLABOR-PORTION` - PIC 9(07)V9(06) - Non-Labor Portion of the payment.
        *   `H-FIXED-LOSS-AMT` - PIC 9(07)V9(02) - Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` - PIC 9(05)V9(02) - New Facility Specific Rate.
        *   `H-LOS-RATIO` - PIC 9(01)V9(05) - Length of Stay Ratio.
*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA` - This is the input data structure, passed from the calling program, containing billing information.
        *   `B-NPI10` - National Provider Identifier (NPI) - 10 digits
            *   `B-NPI8` - PIC X(08) - The first 8 digits of the NPI.
            *   `B-NPI-FILLER` - PIC X(02) - Filler for the last 2 digits of the NPI.
        *   `B-PROVIDER-NO` - PIC X(06) - Provider Number.
        *   `B-PATIENT-STATUS` - PIC X(02) - Patient Status.
        *   `B-DRG-CODE` - PIC X(03) - DRG (Diagnosis Related Group) Code.
        *   `B-LOS` - PIC 9(03) - Length of Stay (in days).
        *   `B-COV-DAYS` - PIC 9(03) - Covered Days.
        *   `B-LTR-DAYS` - PIC 9(02) - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE` - Discharge Date.
            *   `B-DISCHG-CC` - PIC 9(02) - Century Code.
            *   `B-DISCHG-YY` - PIC 9(02) - Year.
            *   `B-DISCHG-MM` - PIC 9(02) - Month.
            *   `B-DISCHG-DD` - PIC 9(02) - Day.
        *   `B-COV-CHARGES` - PIC 9(07)V9(02) - Covered Charges.
        *   `B-SPEC-PAY-IND` - PIC X(01) - Special Payment Indicator.
        *   `FILLER` - PIC X(13) - Unused space
    *   `PPS-DATA-ALL` - This is the output data structure, passed back to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` - PIC 9(02) - Return Code - Indicates the reason for the payment or why it was not paid.
        *   `PPS-CHRG-THRESHOLD` - PIC 9(07)V9(02) - Charge Threshold.
        *   `PPS-DATA` - Group item containing the PPS related data.
            *   `PPS-MSA` - PIC X(04) - MSA (Metropolitan Statistical Area) code.
            *   `PPS-WAGE-INDEX` - PIC 9(02)V9(04) - Wage Index.
            *   `PPS-AVG-LOS` - PIC 9(02)V9(01) - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` - PIC 9(01)V9(04) - Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` - PIC 9(07)V9(02) - Outlier Payment Amount.
            *   `PPS-LOS` - PIC 9(03) - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` - PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` - PIC 9(07)V9(02) - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` - PIC 9(07)V9(02) - Final Payment Amount.
            *   `PPS-FAC-COSTS` - PIC 9(07)V9(02) - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` - PIC 9(07)V9(02) - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` - PIC 9(07)V9(02) - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` - PIC X(03) - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` - PIC X(05) - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` - PIC 9(03) - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` - PIC 9(03) - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` - PIC 9(01) - Blend Year.
            *   `PPS-COLA` - PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   `FILLER` - PIC X(04) - Unused space.
        *   `PPS-OTHER-DATA` - Group item with other PPS related data
            *   `PPS-NAT-LABOR-PCT` - PIC 9(01)V9(05) - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` - PIC 9(01)V9(05) - National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` - PIC 9(05)V9(02) - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` - PIC 9(01)V9(03) - Budget Neutrality Rate.
            *   `FILLER` - PIC X(20) - Unused space.
        *   `PPS-PC-DATA` - Group item with PPS related data.
            *   `PPS-COT-IND` - PIC X(01) - Cost Outlier Indicator.
            *   `FILLER` - PIC X(20) - Unused space.
    *   `PRICER-OPT-VERS-SW` - This structure probably indicates which version of the pricer options to use.
        *   `PRICER-OPTION-SW` - PIC X(01) - Option switch.
            *   `ALL-TABLES-PASSED` - VALUE 'A'.
            *   `PROV-RECORD-PASSED` - VALUE 'P'.
        *   `PPS-VERSIONS` - Group item for the versions of the programs.
            *   `PPDRV-VERSION` - PIC X(05) - Version of the PPDRV program.
    *   `PROV-NEW-HOLD` - This is the provider record data, passed from the calling program.
        *   `PROV-NEWREC-HOLD1` - Group item for the provider record.
            *   `P-NEW-NPI10` - NPI Data
                *   `P-NEW-NPI8` - PIC X(08) - The first 8 digits of the NPI.
                *   `P-NEW-NPI-FILLER` - PIC X(02) - Filler for the last 2 digits of the NPI.
            *   `P-NEW-PROVIDER-NO` - Provider Number
                *   `P-NEW-STATE` - PIC 9(02) - State Code.
                *   `FILLER` - PIC X(04) - Unused space.
            *   `P-NEW-DATE-DATA` - Date Data
                *   `P-NEW-EFF-DATE` - Effective Date.
                    *   `P-NEW-EFF-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-EFF-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-EFF-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-EFF-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-FY-BEGIN-DATE` - Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-FY-BEG-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-FY-BEG-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-FY-BEG-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-REPORT-DATE` - Report Date.
                    *   `P-NEW-REPORT-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-REPORT-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-REPORT-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-REPORT-DT-DD` - PIC 9(02) - Day.
                *   `P-NEW-TERMINATION-DATE` - Termination Date.
                    *   `P-NEW-TERM-DT-CC` - PIC 9(02) - Century Code.
                    *   `P-NEW-TERM-DT-YY` - PIC 9(02) - Year.
                    *   `P-NEW-TERM-DT-MM` - PIC 9(02) - Month.
                    *   `P-NEW-TERM-DT-DD` - PIC 9(02) - Day.
            *   `P-NEW-WAIVER-CODE` - PIC X(01) - Waiver Code.
                *   `P-NEW-WAIVER-STATE` - VALUE 'Y'.
            *   `P-NEW-INTER-NO` - PIC 9(05) - Intern Number.
            *   `P-NEW-PROVIDER-TYPE` - PIC X(02) - Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` - PIC 9(01) - Current Census Division.
            *   `P-NEW-CURRENT-DIV` - PIC 9(01) - Redefines `P-NEW-CURRENT-CENSUS-DIV`.
            *   `P-NEW-MSA-DATA` - MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` - PIC X - Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` - PIC X(04) - Geographic Location MSA, right-justified.
                *   `P-NEW-GEO-LOC-MSA9` - PIC 9(04) - Redefines `P-NEW-GEO-LOC-MSAX`.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - PIC X(04) - Wage Index Location MSA, right-justified.
                *   `P-NEW-STAND-AMT-LOC-MSA` - PIC X(04) - Standard Amount Location MSA, right-justified.
                *   `P-NEW-STAND-AMT-LOC-MSA9` - Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                    *   `P-NEW-RURAL-1ST` - Rural Indicator.
                        *   `P-NEW-STAND-RURAL` - PIC XX.
                        *   `P-NEW-STD-RURAL-CHECK` - VALUE '  '.
                    *   `P-NEW-RURAL-2ND` - PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - PIC XX.
            *   `P-NEW-LUGAR` - PIC X.
            *   `P-NEW-TEMP-RELIEF-IND` - PIC X.
            *   `P-NEW-FED-PPS-BLEND-IND` - PIC X.
            *   `FILLER` - PIC X(05) - Unused Space.
        *   `PROV-NEWREC-HOLD2` - Group item for the provider record.
            *   `P-NEW-VARIABLES` - Group item for the provider record.
                *   `P-NEW-FAC-SPEC-RATE` - PIC 9(05)V9(02) - Facility Specific Rate.
                *   `P-NEW-COLA` - PIC 9(01)V9(03) - Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` - PIC 9(01)V9(04) - Intern Ratio.
                *   `P-NEW-BED-SIZE` - PIC 9(05) - Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` - PIC 9(01)V9(03) - Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` - PIC 9(01)V9(04) - Case Mix Index.
                *   `P-NEW-SSI-RATIO` - PIC V