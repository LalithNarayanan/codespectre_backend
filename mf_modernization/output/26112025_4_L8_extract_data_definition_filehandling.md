## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, it's highly probable that this program interacts with data through calls to other programs (like LTDRG031) or through the `LINKAGE SECTION`.
*   **WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` - (PIC X(46)) -  Contains a descriptive string identifying the program and the storage area.
    *   `CAL-VERSION` - (PIC X(05)) - Stores the version of the calculation logic, "C03.2".
    *   `HOLD-PPS-COMPONENTS` -  A group item used to store various components relevant to the PPS (Prospective Payment System) calculation.
        *   `H-LOS` - (PIC 9(03)) - Length of Stay.
        *   `H-REG-DAYS` - (PIC 9(03)) - Regular Days.
        *   `H-TOTAL-DAYS` - (PIC 9(05)) - Total Days.
        *   `H-SSOT` - (PIC 9(02)) - Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` - (PIC 9(02)) - Blend Return Code.
        *   `H-BLEND-FAC` - (PIC 9(01)V9(01)) - Blend Facility Percentage.
        *   `H-BLEND-PPS` - (PIC 9(01)V9(01)) - Blend PPS Percentage.
        *   `H-SS-PAY-AMT` - (PIC 9(07)V9(02)) - Short Stay Payment Amount.
        *   `H-SS-COST` - (PIC 9(07)V9(02)) - Short Stay Cost.
        *   `H-LABOR-PORTION` - (PIC 9(07)V9(06)) - Labor Portion of the Payment.
        *   `H-NONLABOR-PORTION` - (PIC 9(07)V9(06)) - Non-Labor Portion of the Payment.
        *   `H-FIXED-LOSS-AMT` - (PIC 9(07)V9(02)) - Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` - (PIC 9(05)V9(02)) - New Facility Specific Rate.
    *   The `COPY LTDRG031` statement indicates that the program includes the data structures defined in the LTDRG031 file.
*   **LINKAGE SECTION:**
    *   `BILL-NEW-DATA` -  A group item representing the input data (bill record) passed to the program.
        *   `B-NPI10`
            *   `B-NPI8` - (PIC X(08)) - National Provider Identifier (NPI) - First 8 characters.
            *   `B-NPI-FILLER` - (PIC X(02)) - National Provider Identifier (NPI) - Last 2 characters.
        *   `B-PROVIDER-NO` - (PIC X(06)) - Provider Number.
        *   `B-PATIENT-STATUS` - (PIC X(02)) - Patient Status.
        *   `B-DRG-CODE` - (PIC X(03)) - Diagnosis Related Group (DRG) Code.
        *   `B-LOS` - (PIC 9(03)) - Length of Stay.
        *   `B-COV-DAYS` - (PIC 9(03)) - Covered Days.
        *   `B-LTR-DAYS` - (PIC 9(02)) - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` - (PIC 9(02)) - Discharge Date - Century/Score.
            *   `B-DISCHG-YY` - (PIC 9(02)) - Discharge Date - Year.
            *   `B-DISCHG-MM` - (PIC 9(02)) - Discharge Date - Month.
            *   `B-DISCHG-DD` - (PIC 9(02)) - Discharge Date - Day.
        *   `B-COV-CHARGES` - (PIC 9(07)V9(02)) - Covered Charges.
        *   `B-SPEC-PAY-IND` - (PIC X(01)) - Special Payment Indicator.
        *   `FILLER` - (PIC X(13)) - Unused.
    *   `PPS-DATA-ALL` - A group item used to return the calculated PPS data to the calling program.
        *   `PPS-RTC` - (PIC 9(02)) - Return Code (PPS-RTC).  Indicates the payment status and reason.
        *   `PPS-CHRG-THRESHOLD` - (PIC 9(07)V9(02)) - Charge Threshold.
        *   `PPS-DATA`
            *   `PPS-MSA` - (PIC X(04)) - Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` - (PIC 9(02)V9(04)) - Wage Index.
            *   `PPS-AVG-LOS` - (PIC 9(02)V9(01)) - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` - (PIC 9(01)V9(04)) - Relative Weight (DRG Weight).
            *   `PPS-OUTLIER-PAY-AMT` - (PIC 9(07)V9(02)) - Outlier Payment Amount.
            *   `PPS-LOS` - (PIC 9(03)) - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` - (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` - (PIC 9(07)V9(02)) - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` - (PIC 9(07)V9(02)) - Final Payment Amount.
            *   `PPS-FAC-COSTS` - (PIC 9(07)V9(02)) - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` - (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` - (PIC 9(07)V9(02)) - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` - (PIC X(03)) - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` - (PIC X(05)) - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` - (PIC 9(03)) - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` - (PIC 9(03)) - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` - (PIC 9(01)) - Blend Year Indicator.
            *   `PPS-COLA` - (PIC 9(01)V9(03)) - Cost of Living Adjustment.
            *   `FILLER` - (PIC X(04)) - Unused.
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` - (PIC 9(01)V9(05)) - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` - (PIC 9(01)V9(05)) - National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` - (PIC 9(05)V9(02)) - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` - (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   `FILLER` - (PIC X(20)) - Unused.
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` - (PIC X(01)) - Cost Outlier Indicator.
            *   `FILLER` - (PIC X(20)) - Unused.
    *   `PRICER-OPT-VERS-SW` -  A group item used to pass the versions of the LTDRV031 programs that will be passed back.
        *   `PRICER-OPTION-SW` - (PIC X(01)) - Pricer Option Switch.
            *   `ALL-TABLES-PASSED` - (VALUE 'A') - Indicates that all tables are passed
            *   `PROV-RECORD-PASSED` - (VALUE 'P') - Indicates that the provider record is passed
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` - (PIC X(05)) - The version of the PPDRV.
    *   `PROV-NEW-HOLD` - A group item representing the provider record passed to the program.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` - (PIC X(08)) - New NPI - First 8 characters
                *   `P-NEW-NPI-FILLER` - (PIC X(02)) - New NPI - Last 2 characters
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` - (PIC 9(02)) - New State
                *   `FILLER` - (PIC X(04)) - Unused
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` - (PIC 9(02)) - New Effective Date - Century/Score
                    *   `P-NEW-EFF-DT-YY` - (PIC 9(02)) - New Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` - (PIC 9(02)) - New Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` - (PIC 9(02)) - New Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` - (PIC 9(02)) - New FY Begin Date - Century/Score
                    *   `P-NEW-FY-BEG-DT-YY` - (PIC 9(02)) - New FY Begin Date - Year
                    *   `P-NEW-FY-BEG-DT-MM` - (PIC 9(02)) - New FY Begin Date - Month
                    *   `P-NEW-FY-BEG-DT-DD` - (PIC 9(02)) - New FY Begin Date - Day
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` - (PIC 9(02)) - New Report Date - Century/Score
                    *   `P-NEW-REPORT-DT-YY` - (PIC 9(02)) - New Report Date - Year
                    *   `P-NEW-REPORT-DT-MM` - (PIC 9(02)) - New Report Date - Month
                    *   `P-NEW-REPORT-DT-DD` - (PIC 9(02)) - New Report Date - Day
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` - (PIC 9(02)) - New Termination Date - Century/Score
                    *   `P-NEW-TERM-DT-YY` - (PIC 9(02)) - New Termination Date - Year
                    *   `P-NEW-TERM-DT-MM` - (PIC 9(02)) - New Termination Date - Month
                    *   `P-NEW-TERM-DT-DD` - (PIC 9(02)) - New Termination Date - Day
            *   `P-NEW-WAIVER-CODE` - (PIC X(01)) - New Waiver Code.
                *   `P-NEW-WAIVER-STATE` - (VALUE 'Y') - Waiver State
            *   `P-NEW-INTER-NO` - (PIC 9(05)) - New Intern Number.
            *   `P-NEW-PROVIDER-TYPE` - (PIC X(02)) - New Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` - (PIC 9(01)) - New Current Census Division.
            *   `P-NEW-CURRENT-DIV` - (PIC 9(01)) - Redefines New Current Census Division.
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` - (PIC X) - New Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` - (PIC X(04)) - New Geo Location MSA X.
                *   `P-NEW-GEO-LOC-MSA9` - (PIC 9(04)) - Redefines New Geo Location MSA X.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - (PIC X(04)) - New Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` - (PIC X(04)) - New Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` -
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` - (PIC XX) - New Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` - (VALUE '  ') - New Standard Rural Check
                        *   `P-NEW-RURAL-2ND` - (PIC XX) - New Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - (PIC XX) - New Sol Com Dep Hosp Year.
            *   `P-NEW-LUGAR` - (PIC X) - New Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` - (PIC X) - New Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` - (PIC X) - New Fed PPS Blend Indicator.
            *   `FILLER` - (PIC X(05)) - Unused.
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` - (PIC 9(05)V9(02)) - New Facility Specific Rate.
                *   `P-NEW-COLA` - (PIC 9(01)V9(03)) - New COLA.
                *   `P-NEW-INTERN-RATIO` - (PIC 9(01)V9(04)) - New Intern Ratio.
                *   `P-NEW-BED-SIZE` - (PIC 9(05)) - New Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` - (PIC 9(01)V9(03)) - New Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` - (PIC 9(01)V9(04)) - New CMI.
                *   `P-NEW-SSI-RATIO` - (PIC V9(04)) - New SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` - (PIC V9(04)) - New Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` - (PIC 9(01)) - New PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` - (PIC 9(01)V9(05)) - New PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` - (PIC V9(04)) - New DSH Percent.
                *   `P-NEW-FYE-DATE` - (PIC X(08)) - New FYE Date.
            *   `FILLER` - (PIC X(23)) - Unused.
        *   `PROV-NEWREC-HOLD3`
            *   `P-NEW-PASS-AMT-DATA`
                *   `P-NEW-PASS-AMT-CAPITAL` - (PIC 9(04)V99) - New Passed Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` - (PIC 9(04)V99) - New Passed Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` - (PIC 9(04)V99) - New Passed Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` - (PIC 9(04)V99) - New Passed Amount Plus Misc.
            *   `P-NEW-CAPI-DATA`
                *   `P-NEW-CAPI-PPS-PAY-CODE` - (PIC X) - New CAPI PPS Pay Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` - (PIC 9(04)V99) - New CAPI Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` - (PIC 9(04)V99) - New CAPI Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` - (PIC 9(01)V9999) - New CAPI New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` - (PIC 9V999) - New CAPI Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` - (PIC X) - New CAPI New Hospital.
                *   `P-NEW-CAPI-IME` - (PIC 9V9999) - New CAPI IME.
                *   `P-NEW-CAPI-EXCEPTIONS` - (PIC 9(04)V99) - New CAPI Exceptions.
            *   `FILLER` - (PIC X(22)) - Unused.
    *   `WAGE-NEW-INDEX-RECORD` - A group item representing wage index data.
        *   `W-MSA` - (PIC X(4)) - MSA Code.
        *   `W-EFF-DATE` - (PIC X(8)) - Effective Date.
        *   `W-WAGE-INDEX1` - (PIC S9(02)V9(04)) - Wage Index 1.
        *   `W-WAGE-INDEX2` - (PIC S9(02)V9(04)) - Wage Index 2.
        *   `W-WAGE-INDEX3` - (PIC S9(02)V9(04)) - Wage Index 3.

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, it's highly probable that this program interacts with data through calls to other programs (like LTDRG031) or through the `LINKAGE SECTION`.
*   **WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` - (PIC X(46)) -  Contains a descriptive string identifying the program and the storage area.
    *   `CAL-VERSION` - (PIC X(05)) - Stores the version of the calculation logic, "C04.2".
    *   `HOLD-PPS-COMPONENTS` -  A group item used to store various components relevant to the PPS (Prospective Payment System) calculation.
        *   `H-LOS` - (PIC 9(03)) - Length of Stay.
        *   `H-REG-DAYS` - (PIC 9(03)) - Regular Days.
        *   `H-TOTAL-DAYS` - (PIC 9(05)) - Total Days.
        *   `H-SSOT` - (PIC 9(02)) - Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` - (PIC 9(02)) - Blend Return Code.
        *   `H-BLEND-FAC` - (PIC 9(01)V9(01)) - Blend Facility Percentage.
        *   `H-BLEND-PPS` - (PIC 9(01)V9(01)) - Blend PPS Percentage.
        *   `H-SS-PAY-AMT` - (PIC 9(07)V9(02)) - Short Stay Payment Amount.
        *   `H-SS-COST` - (PIC 9(07)V9(02)) - Short Stay Cost.
        *   `H-LABOR-PORTION` - (PIC 9(07)V9(06)) - Labor Portion of the Payment.
        *   `H-NONLABOR-PORTION` - (PIC 9(07)V9(06)) - Non-Labor Portion of the Payment.
        *   `H-FIXED-LOSS-AMT` - (PIC 9(07)V9(02)) - Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` - (PIC 9(05)V9(02)) - New Facility Specific Rate.
        *   `H-LOS-RATIO` - (PIC 9(01)V9(05)) - Length of Stay Ratio.
    *   The `COPY LTDRG031` statement indicates that the program includes the data structures defined in the LTDRG031 file.
*   **LINKAGE SECTION:**
    *   `BILL-NEW-DATA` -  A group item representing the input data (bill record) passed to the program.
        *   `B-NPI10`
            *   `B-NPI8` - (PIC X(08)) - National Provider Identifier (NPI) - First 8 characters.
            *   `B-NPI-FILLER` - (PIC X(02)) - National Provider Identifier (NPI) - Last 2 characters.
        *   `B-PROVIDER-NO` - (PIC X(06)) - Provider Number.
        *   `B-PATIENT-STATUS` - (PIC X(02)) - Patient Status.
        *   `B-DRG-CODE` - (PIC X(03)) - Diagnosis Related Group (DRG) Code.
        *   `B-LOS` - (PIC 9(03)) - Length of Stay.
        *   `B-COV-DAYS` - (PIC 9(03)) - Covered Days.
        *   `B-LTR-DAYS` - (PIC 9(02)) - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` - (PIC 9(02)) - Discharge Date - Century/Score.
            *   `B-DISCHG-YY` - (PIC 9(02)) - Discharge Date - Year.
            *   `B-DISCHG-MM` - (PIC 9(02)) - Discharge Date - Month.
            *   `B-DISCHG-DD` - (PIC 9(02)) - Discharge Date - Day.
        *   `B-COV-CHARGES` - (PIC 9(07)V9(02)) - Covered Charges.
        *   `B-SPEC-PAY-IND` - (PIC X(01)) - Special Payment Indicator.
        *   `FILLER` - (PIC X(13)) - Unused.
    *   `PPS-DATA-ALL` - A group item used to return the calculated PPS data to the calling program.
        *   `PPS-RTC` - (PIC 9(02)) - Return Code (PPS-RTC).  Indicates the payment status and reason.
        *   `PPS-CHRG-THRESHOLD` - (PIC 9(07)V9(02)) - Charge Threshold.
        *   `PPS-DATA`
            *   `PPS-MSA` - (PIC X(04)) - Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` - (PIC 9(02)V9(04)) - Wage Index.
            *   `PPS-AVG-LOS` - (PIC 9(02)V9(01)) - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` - (PIC 9(01)V9(04)) - Relative Weight (DRG Weight).
            *   `PPS-OUTLIER-PAY-AMT` - (PIC 9(07)V9(02)) - Outlier Payment Amount.
            *   `PPS-LOS` - (PIC 9(03)) - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` - (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` - (PIC 9(07)V9(02)) - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` - (PIC 9(07)V9(02)) - Final Payment Amount.
            *   `PPS-FAC-COSTS` - (PIC 9(07)V9(02)) - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` - (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` - (PIC 9(07)V9(02)) - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` - (PIC X(03)) - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` - (PIC X(05)) - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` - (PIC 9(03)) - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` - (PIC 9(03)) - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` - (PIC 9(01)) - Blend Year Indicator.
            *   `PPS-COLA` - (PIC 9(01)V9(03)) - Cost of Living Adjustment.
            *   `FILLER` - (PIC X(04)) - Unused.
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` - (PIC 9(01)V9(05)) - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` - (PIC 9(01)V9(05)) - National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` - (PIC 9(05)V9(02)) - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` - (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   `FILLER` - (PIC X(20)) - Unused.
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` - (PIC X(01)) - Cost Outlier Indicator.
            *   `FILLER` - (PIC X(20)) - Unused.
    *   `PRICER-OPT-VERS-SW` -  A group item used to pass the versions of the LTDRV040 programs that will be passed back.
        *   `PRICER-OPTION-SW` - (PIC X(01)) - Pricer Option Switch.
            *   `ALL-TABLES-PASSED` - (VALUE 'A') - Indicates that all tables are passed
            *   `PROV-RECORD-PASSED` - (VALUE 'P') - Indicates that the provider record is passed
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` - (PIC X(05)) - The version of the PPDRV.
    *   `PROV-NEW-HOLD` - A group item representing the provider record passed to the program.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` - (PIC X(08)) - New NPI - First 8 characters
                *   `P-NEW-NPI-FILLER` - (PIC X(02)) - New NPI - Last 2 characters
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` - (PIC 9(02)) - New State
                *   `FILLER` - (PIC X(04)) - Unused
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` - (PIC 9(02)) - New Effective Date - Century/Score
                    *   `P-NEW-EFF-DT-YY` - (PIC 9(02)) - New Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` - (PIC 9(02)) - New Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` - (PIC 9(02)) - New Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` - (PIC 9(02)) - New FY Begin Date - Century/Score
                    *   `P-NEW-FY-BEG-DT-YY` - (PIC 9(02)) - New FY Begin Date - Year
                    *   `P-NEW-FY-BEG-DT-MM` - (PIC 9(02)) - New FY Begin Date - Month
                    *   `P-NEW-FY-BEG-DT-DD` - (PIC 9(02)) - New FY Begin Date - Day
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` - (PIC 9(02)) - New Report Date - Century/Score
                    *   `P-NEW-REPORT-DT-YY` - (PIC 9(02)) - New Report Date - Year
                    *   `P-NEW-REPORT-DT-MM` - (PIC 9(02)) - New Report Date - Month
                    *   `P-NEW-REPORT-DT-DD` - (PIC 9(02)) - New Report Date - Day
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` - (PIC 9(02)) - New Termination Date - Century/Score
                    *   `P-NEW-TERM-DT-YY` - (PIC 9(02)) - New Termination Date - Year
                    *   `P-NEW-TERM-DT-MM` - (PIC 9(02)) - New Termination Date - Month
                    *   `P-NEW-TERM-DT-DD` - (PIC 9(02)) - New Termination Date - Day
            *   `P-NEW-WAIVER-CODE` - (PIC X(01)) - New Waiver Code.
                *   `P-NEW-WAIVER-STATE` - (VALUE 'Y') - Waiver State
            *   `P-NEW-INTER-NO` - (PIC 9(05)) - New Intern Number.
            *   `P-NEW-PROVIDER-TYPE` - (PIC X(02)) - New Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` - (PIC 9(01)) - New Current Census Division.
            *   `P-NEW-CURRENT-DIV` - (PIC 9(01)) - Redefines New Current Census Division.
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` - (PIC X) - New Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` - (PIC X(04)) - New Geo Location MSA X.
                *   `P-NEW-GEO-LOC-MSA9` - (PIC 9(04)) - Redefines New Geo Location MSA X.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - (PIC X(04)) - New Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` - (PIC X(04)) - New Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` -
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` - (PIC XX) - New Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` - (VALUE '  ') - New Standard Rural Check
                        *   `P-NEW-RURAL-2ND` - (PIC XX) - New Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - (PIC XX) - New Sol Com Dep Hosp Year.
            *   `P-NEW-LUGAR` - (PIC X) - New Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` - (PIC X) - New Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` - (PIC X) - New Fed PPS Blend Indicator.
            *   `FILLER` - (PIC X(05)) - Unused.
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` - (PIC 9(05)V9(02)) - New Facility Specific Rate.
                *   `P-NEW-COLA` - (PIC 9(01)V9(03)) - New COLA.
                *   `P-NEW-