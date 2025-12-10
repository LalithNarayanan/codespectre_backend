## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and their descriptions:

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements are present in the code. The program calls a copybook which may contain file definitions.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   **`W-STORAGE-REF`**: (PIC X(46)) -  A working storage reference string, likely for program identification or debugging purposes.  It contains the program name and a label indicating it's working storage.
    *   **`CAL-VERSION`**: (PIC X(05)) -  Stores the version number of the calculation logic, set to 'C03.2'.
    *   **`HOLD-PPS-COMPONENTS`**:
        *   **`H-LOS`**: (PIC 9(03)) -  Holds the Length of Stay (LOS) value, likely in days.
        *   **`H-REG-DAYS`**: (PIC 9(03)) - Holds regular days
        *   **`H-TOTAL-DAYS`**: (PIC 9(05)) - Holds the total days
        *   **`H-SSOT`**: (PIC 9(02)) -  Holds the Short Stay Outlier Threshold value.
        *   **`H-BLEND-RTC`**: (PIC 9(02)) -  Holds the Blend Return Code value.
        *   **`H-BLEND-FAC`**: (PIC 9(01)V9(01)) - Holds the Blend Facility Rate.
        *   **`H-BLEND-PPS`**: (PIC 9(01)V9(01)) - Holds the Blend PPS Rate
        *   **`H-SS-PAY-AMT`**: (PIC 9(07)V9(02)) -  Holds Short Stay Payment Amount.
        *   **`H-SS-COST`**: (PIC 9(07)V9(02)) -  Holds Short Stay Cost.
        *   **`H-LABOR-PORTION`**: (PIC 9(07)V9(06)) -  Holds the Labor Portion of a calculation, with six decimal places.
        *   **`H-NONLABOR-PORTION`**: (PIC 9(07)V9(06)) -  Holds the Non-Labor Portion of a calculation, with six decimal places.
        *   **`H-FIXED-LOSS-AMT`**: (PIC 9(07)V9(02)) - Holds the fixed loss amount with two decimal places.
        *   **`H-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) -  Holds the New Facility Specific Rate.

*   **LINKAGE SECTION Data Structures:**

    *   **`BILL-NEW-DATA`**:  This structure receives data from the calling program, representing the billing information.
        *   **`B-NPI10`**:  NPI (National Provider Identifier)
            *   **`B-NPI8`**: (PIC X(08)) -  First 8 digits of the NPI.
            *   **`B-NPI-FILLER`**: (PIC X(02)) -  Filler for the NPI.
        *   **`B-PROVIDER-NO`**: (PIC X(06)) -  Provider Number.
        *   **`B-PATIENT-STATUS`**: (PIC X(02)) -  Patient Status code.
        *   **`B-DRG-CODE`**: (PIC X(03)) -  DRG (Diagnosis Related Group) Code.
        *   **`B-LOS`**: (PIC 9(03)) -  Length of Stay (LOS) in days.
        *   **`B-COV-DAYS`**: (PIC 9(03)) -  Covered Days.
        *   **`B-LTR-DAYS`**: (PIC 9(02)) -  Lifetime Reserve Days.
        *   **`B-DISCHARGE-DATE`**:  Discharge Date.
            *   **`B-DISCHG-CC`**: (PIC 9(02)) -  Discharge Century/Year.
            *   **`B-DISCHG-YY`**: (PIC 9(02)) -  Discharge Year.
            *   **`B-DISCHG-MM`**: (PIC 9(02)) -  Discharge Month.
            *   **`B-DISCHG-DD`**: (PIC 9(02)) -  Discharge Day.
        *   **`B-COV-CHARGES`**: (PIC 9(07)V9(02)) -  Covered Charges.
        *   **`B-SPEC-PAY-IND`**: (PIC X(01)) -  Special Pay Indicator.
        *   **`FILLER`**: (PIC X(13)) -  Filler.
    *   **`PPS-DATA-ALL`**:  This structure is used to return calculated PPS (Prospective Payment System) data to the calling program.
        *   **`PPS-RTC`**: (PIC 9(02)) -  PPS Return Code. Indicates the outcome of the calculation.
        *   **`PPS-CHRG-THRESHOLD`**: (PIC 9(07)V9(02)) - Charges Threshold
        *   **`PPS-DATA`**:  PPS Data.
            *   **`PPS-MSA`**: (PIC X(04)) -  MSA (Metropolitan Statistical Area) code.
            *   **`PPS-WAGE-INDEX`**: (PIC 9(02)V9(04)) -  Wage Index.
            *   **`PPS-AVG-LOS`**: (PIC 9(02)V9(01)) -  Average Length of Stay.
            *   **`PPS-RELATIVE-WGT`**: (PIC 9(01)V9(04)) -  Relative Weight.
            *   **`PPS-OUTLIER-PAY-AMT`**: (PIC 9(07)V9(02)) -  Outlier Payment Amount.
            *   **`PPS-LOS`**: (PIC 9(03)) -  Length of Stay.
            *   **`PPS-DRG-ADJ-PAY-AMT`**: (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount
            *   **`PPS-FED-PAY-AMT`**: (PIC 9(07)V9(02)) - Federal Payment Amount
            *   **`PPS-FINAL-PAY-AMT`**: (PIC 9(07)V9(02)) - Final Payment Amount.
            *   **`PPS-FAC-COSTS`**: (PIC 9(07)V9(02)) - Facility costs.
            *   **`PPS-NEW-FAC-SPEC-RATE`**: (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   **`PPS-OUTLIER-THRESHOLD`**: (PIC 9(07)V9(02)) - Outlier Threshold.
            *   **`PPS-SUBM-DRG-CODE`**: (PIC X(03)) - Submitted DRG Code.
            *   **`PPS-CALC-VERS-CD`**: (PIC X(05)) - Calculation Version Code.
            *   **`PPS-REG-DAYS-USED`**: (PIC 9(03)) - Regular Days used.
            *   **`PPS-LTR-DAYS-USED`**: (PIC 9(03)) - Lifetime Reserve Days used.
            *   **`PPS-BLEND-YEAR`**: (PIC 9(01)) - Blend Year
            *   **`PPS-COLA`**: (PIC 9(01)V9(03)) - COLA (Cost of Living Adjustment).
            *   **`FILLER`**: (PIC X(04)) - Filler.
        *   **`PPS-OTHER-DATA`**:  Other PPS Data.
            *   **`PPS-NAT-LABOR-PCT`**: (PIC 9(01)V9(05)) -  National Labor Percentage.
            *   **`PPS-NAT-NONLABOR-PCT`**: (PIC 9(01)V9(05)) -  National Non-Labor Percentage.
            *   **`PPS-STD-FED-RATE`**: (PIC 9(05)V9(02)) -  Standard Federal Rate.
            *   **`PPS-BDGT-NEUT-RATE`**: (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   **`FILLER`**: (PIC X(20)) - Filler.
        *   **`PPS-PC-DATA`**:  PPS PC Data.
            *   **`PPS-COT-IND`**: (PIC X(01)) -  Cost Outlier Indicator.
            *   **`FILLER`**: (PIC X(20)) - Filler.
    *   **`PRICER-OPT-VERS-SW`**:  Pricer Option/Version Switch. Controls which version of the LTDRV031 programs are passed back.
        *   **`PRICER-OPTION-SW`**: (PIC X(01)) - Pricer Option Switch.
            *   **`ALL-TABLES-PASSED`**:  (VALUE 'A') - Indicates all tables are passed.
            *   **`PROV-RECORD-PASSED`**:  (VALUE 'P') - Indicates the provider record is passed.
        *   **`PPS-VERSIONS`**:  PPS Versions.
            *   **`PPDRV-VERSION`**: (PIC X(05)) -  Version of the PPDRV program.
    *   **`PROV-NEW-HOLD`**:  Provider Record Data.  This structure is used to pass provider-specific information.
        *   **`PROV-NEWREC-HOLD1`**: Provider Record Hold 1.
            *   **`P-NEW-NPI10`**:  New NPI
                *   **`P-NEW-NPI8`**: (PIC X(08)) -  NPI (National Provider Identifier) - first 8 digits.
                *   **`P-NEW-NPI-FILLER`**: (PIC X(02)) -  NPI filler
            *   **`P-NEW-PROVIDER-NO`**:  Provider Number.
                *   **`P-NEW-STATE`**: (PIC 9(02)) -  Provider State.
                *   **`FILLER`**: (PIC X(04)) - Filler.
            *   **`P-NEW-DATE-DATA`**: Date Data.
                *   **`P-NEW-EFF-DATE`**: Effective Date.
                    *   **`P-NEW-EFF-DT-CC`**: (PIC 9(02)) - Effective Date Century/Year.
                    *   **`P-NEW-EFF-DT-YY`**: (PIC 9(02)) - Effective Date Year.
                    *   **`P-NEW-EFF-DT-MM`**: (PIC 9(02)) - Effective Date Month.
                    *   **`P-NEW-EFF-DT-DD`**: (PIC 9(02)) - Effective Date Day.
                *   **`P-NEW-FY-BEGIN-DATE`**: Fiscal Year Begin Date.
                    *   **`P-NEW-FY-BEG-DT-CC`**: (PIC 9(02)) - FY Begin Date Century/Year.
                    *   **`P-NEW-FY-BEG-DT-YY`**: (PIC 9(02)) - FY Begin Date Year.
                    *   **`P-NEW-FY-BEG-DT-MM`**: (PIC 9(02)) - FY Begin Date Month.
                    *   **`P-NEW-FY-BEG-DT-DD`**: (PIC 9(02)) - FY Begin Date Day.
                *   **`P-NEW-REPORT-DATE`**: Report Date.
                    *   **`P-NEW-REPORT-DT-CC`**: (PIC 9(02)) - Report Date Century/Year.
                    *   **`P-NEW-REPORT-DT-YY`**: (PIC 9(02)) - Report Date Year.
                    *   **`P-NEW-REPORT-DT-MM`**: (PIC 9(02)) - Report Date Month.
                    *   **`P-NEW-REPORT-DT-DD`**: (PIC 9(02)) - Report Date Day.
                *   **`P-NEW-TERMINATION-DATE`**: Termination Date.
                    *   **`P-NEW-TERM-DT-CC`**: (PIC 9(02)) - Termination Date Century/Year.
                    *   **`P-NEW-TERM-DT-YY`**: (PIC 9(02)) - Termination Date Year.
                    *   **`P-NEW-TERM-DT-MM`**: (PIC 9(02)) - Termination Date Month.
                    *   **`P-NEW-TERM-DT-DD`**: (PIC 9(02)) - Termination Date Day.
            *   **`P-NEW-WAIVER-CODE`**: (PIC X(01)) -  Waiver Code.
                *   **`P-NEW-WAIVER-STATE`**:  (VALUE 'Y') - Waiver State.
            *   **`P-NEW-INTER-NO`**: (PIC 9(05)) -  Interim Number.
            *   **`P-NEW-PROVIDER-TYPE`**: (PIC X(02)) -  Provider Type.
            *   **`P-NEW-CURRENT-CENSUS-DIV`**: (PIC 9(01)) - Current Census Division.
            *   **`P-NEW-CURRENT-DIV`**: (REDEFINES `P-NEW-CURRENT-CENSUS-DIV`) - Redefines the current census division.
            *   **`P-NEW-MSA-DATA`**: MSA Data.
                *   **`P-NEW-CHG-CODE-INDEX`**: (PIC X) - Charge Code Index.
                *   **`P-NEW-GEO-LOC-MSAX`**: (PIC X(04)) - Geo Location MSA.
                *   **`P-NEW-GEO-LOC-MSA9`**: (REDEFINES `P-NEW-GEO-LOC-MSAX`, PIC 9(04)) - Redefines geo location MSA.
                *   **`P-NEW-WAGE-INDEX-LOC-MSA`**: (PIC X(04)) - Wage Index Location MSA.
                *   **`P-NEW-STAND-AMT-LOC-MSA`**: (PIC X(04)) - Standard Amount Location MSA.
                *   **`P-NEW-STAND-AMT-LOC-MSA9`**: (REDEFINES `P-NEW-STAND-AMT-LOC-MSA`) - Redefines standard amount location MSA.
                    *   **`P-NEW-RURAL-1ST`**: Rural 1st
                        *   **`P-NEW-STAND-RURAL`**: (PIC XX) - Standard Rural.
                            *   **`P-NEW-STD-RURAL-CHECK`**: (VALUE '  ') - Rural Check
                        *   **`P-NEW-RURAL-2ND`**: (PIC XX) - Rural 2nd
            *   **`P-NEW-SOL-COM-DEP-HOSP-YR`**: (PIC XX) -  Sole Community Dependent Hospital Year.
            *   **`P-NEW-LUGAR`**: (PIC X) - Lugar.
            *   **`P-NEW-TEMP-RELIEF-IND`**: (PIC X) - Temporary Relief Indicator.
            *   **`P-NEW-FED-PPS-BLEND-IND`**: (PIC X) - Federal PPS Blend Indicator.
            *   **`FILLER`**: (PIC X(05)) - Filler.
        *   **`PROV-NEWREC-HOLD2`**: Provider Record Hold 2.
            *   **`P-NEW-VARIABLES`**:  New Variables.
                *   **`P-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - Facility Specific Rate.
                *   **`P-NEW-COLA`**: (PIC 9(01)V9(03)) - COLA (Cost of Living Adjustment).
                *   **`P-NEW-INTERN-RATIO`**: (PIC 9(01)V9(04)) - Intern Ratio.
                *   **`P-NEW-BED-SIZE`**: (PIC 9(05)) -  Bed Size.
                *   **`P-NEW-OPER-CSTCHG-RATIO`**: (PIC 9(01)V9(03)) - Operating Cost to Charge Ratio.
                *   **`P-NEW-CMI`**: (PIC 9(01)V9(04)) -  CMI.
                *   **`P-NEW-SSI-RATIO`**: (PIC V9(04)) - SSI Ratio.
                *   **`P-NEW-MEDICAID-RATIO`**: (PIC V9(04)) - Medicaid Ratio.
                *   **`P-NEW-PPS-BLEND-YR-IND`**: (PIC 9(01)) - PPS Blend Year Indicator.
                *   **`P-NEW-PRUF-UPDTE-FACTOR`**: (PIC 9(01)V9(05)) - Pruf Update Factor.
                *   **`P-NEW-DSH-PERCENT`**: (PIC V9(04)) - DSH Percentage.
                *   **`P-NEW-FYE-DATE`**: (PIC X(08)) - FYE Date.
            *   **`FILLER`**: (PIC X(23)) - Filler.
        *   **`PROV-NEWREC-HOLD3`**: Provider Record Hold 3.
            *   **`P-NEW-PASS-AMT-DATA`**: Passed Amount Data.
                *   **`P-NEW-PASS-AMT-CAPITAL`**: (PIC 9(04)V99) - Passed Amount Capital.
                *   **`P-NEW-PASS-AMT-DIR-MED-ED`**: (PIC 9(04)V99) - Passed Amount Direct Medical Education.
                *   **`P-NEW-PASS-AMT-ORGAN-ACQ`**: (PIC 9(04)V99) - Passed Amount Organ Acquisition.
                *   **`P-NEW-PASS-AMT-PLUS-MISC`**: (PIC 9(04)V99) - Passed Amount Plus Miscellaneous.
            *   **`P-NEW-CAPI-DATA`**: Capital Data.
                *   **`P-NEW-CAPI-PPS-PAY-CODE`**: (PIC X) - Capital PPS Pay Code.
                *   **`P-NEW-CAPI-HOSP-SPEC-RATE`**: (PIC 9(04)V99) - Capital Hospital Specific Rate.
                *   **`P-NEW-CAPI-OLD-HARM-RATE`**: (PIC 9(04)V99) - Capital Old Harm Rate.
                *   **`P-NEW-CAPI-NEW-HARM-RATIO`**: (PIC 9(01)V9999) - Capital New Harm Ratio.
                *   **`P-NEW-CAPI-CSTCHG-RATIO`**: (PIC 9V999) - Capital Cost to Charge Ratio.
                *   **`P-NEW-CAPI-NEW-HOSP`**: (PIC X) - Capital New Hospital.
                *   **`P-NEW-CAPI-IME`**: (PIC 9V9999) - Capital IME.
                *   **`P-NEW-CAPI-EXCEPTIONS`**: (PIC 9(04)V99) - Capital Exceptions.
            *   **`FILLER`**: (PIC X(22)) - Filler.
    *   **`WAGE-NEW-INDEX-RECORD`**: Wage Index Record.  This structure is used to pass wage index information.
        *   **`W-MSA`**: (PIC X(4)) -  MSA (Metropolitan Statistical Area) code.
        *   **`W-EFF-DATE`**: (PIC X(8)) - Effective Date.
        *   **`W-WAGE-INDEX1`**: (PIC S9(02)V9(04)) - Wage Index 1.
        *   **`W-WAGE-INDEX2`**: (PIC S9(02)V9(04)) - Wage Index 2
        *   **`W-WAGE-INDEX3`**: (PIC S9(02)V9(04)) - Wage Index 3.

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements are present in the code. The program calls a copybook which may contain file definitions.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   **`W-STORAGE-REF`**: (PIC X(46)) - A working storage reference string, likely for program identification or debugging purposes. It contains the program name and a label indicating it's working storage.
    *   **`CAL-VERSION`**: (PIC X(05)) - Stores the version number of the calculation logic, set to 'C04.2'.
    *   **`HOLD-PPS-COMPONENTS`**:
        *   **`H-LOS`**: (PIC 9(03)) - Length of Stay (LOS) in days.
        *   **`H-REG-DAYS`**: (PIC 9(03)) - Regular days
        *   **`H-TOTAL-DAYS`**: (PIC 9(05)) - Total Days
        *   **`H-SSOT`**: (PIC 9(02)) - Short Stay Outlier Threshold.
        *   **`H-BLEND-RTC`**: (PIC 9(02)) - Blend Return Code.
        *   **`H-BLEND-FAC`**: (PIC 9(01)V9(01)) - Blend Facility Rate.
        *   **`H-BLEND-PPS`**: (PIC 9(01)V9(01)) - Blend PPS Rate.
        *   **`H-SS-PAY-AMT`**: (PIC 9(07)V9(02)) - Short Stay Payment Amount.
        *   **`H-SS-COST`**: (PIC 9(07)V9(02)) - Short Stay Cost.
        *   **`H-LABOR-PORTION`**: (PIC 9(07)V9(06)) - Labor Portion (with six decimal places).
        *   **`H-NONLABOR-PORTION`**: (PIC 9(07)V9(06)) - Non-Labor Portion (with six decimal places).
        *   **`H-FIXED-LOSS-AMT`**: (PIC 9(07)V9(02)) - Fixed Loss Amount.
        *   **`H-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - New Facility Specific Rate.
        *   **`H-LOS-RATIO`**: (PIC 9(01)V9(05)) -  LOS Ratio

*   **LINKAGE SECTION Data Structures:**

    *   **`BILL-NEW-DATA`**:  This structure receives data from the calling program, representing the billing information.
        *   **`B-NPI10`**:  NPI (National Provider Identifier)
            *   **`B-NPI8`**: (PIC X(08)) -  First 8 digits of the NPI.
            *   **`B-NPI-FILLER`**: (PIC X(02)) -  Filler for the NPI.
        *   **`B-PROVIDER-NO`**: (PIC X(06)) -  Provider Number.
        *   **`B-PATIENT-STATUS`**: (PIC X(02)) -  Patient Status code.
        *   **`B-DRG-CODE`**: (PIC X(03)) -  DRG (Diagnosis Related Group) Code.
        *   **`B-LOS`**: (PIC 9(03)) -  Length of Stay (LOS) in days.
        *   **`B-COV-DAYS`**: (PIC 9(03)) -  Covered Days.
        *   **`B-LTR-DAYS`**: (PIC 9(02)) -  Lifetime Reserve Days.
        *   **`B-DISCHARGE-DATE`**:  Discharge Date.
            *   **`B-DISCHG-CC`**: (PIC 9(02)) -  Discharge Century/Year.
            *   **`B-DISCHG-YY`**: (PIC 9(02)) -  Discharge Year.
            *   **`B-DISCHG-MM`**: (PIC 9(02)) -  Discharge Month.
            *   **`B-DISCHG-DD`**: (PIC 9(02)) -  Discharge Day.
        *   **`B-COV-CHARGES`**: (PIC 9(07)V9(02)) -  Covered Charges.
        *   **`B-SPEC-PAY-IND`**: (PIC X(01)) -  Special Pay Indicator.
        *   **`FILLER`**: (PIC X(13)) -  Filler.
    *   **`PPS-DATA-ALL`**:  This structure is used to return calculated PPS (Prospective Payment System) data to the calling program.
        *   **`PPS-RTC`**: (PIC 9(02)) -  PPS Return Code. Indicates the outcome of the calculation.
        *   **`PPS-CHRG-THRESHOLD`**: (PIC 9(07)V9(02)) - Charges Threshold
        *   **`PPS-DATA`**:  PPS Data.
            *   **`PPS-MSA`**: (PIC X(04)) -  MSA (Metropolitan Statistical Area) code.
            *   **`PPS-WAGE-INDEX`**: (PIC 9(02)V9(04)) -  Wage Index.
            *   **`PPS-AVG-LOS`**: (PIC 9(02)V9(01)) -  Average Length of Stay.
            *   **`PPS-RELATIVE-WGT`**: (PIC 9(01)V9(04)) -  Relative Weight.
            *   **`PPS-OUTLIER-PAY-AMT`**: (PIC 9(07)V9(02)) -  Outlier Payment Amount.
            *   **`PPS-LOS`**: (PIC 9(03)) -  Length of Stay.
            *   **`PPS-DRG-ADJ-PAY-AMT`**: (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount
            *   **`PPS-FED-PAY-AMT`**: (PIC 9(07)V9(02)) - Federal Payment Amount
            *   **`PPS-FINAL-PAY-AMT`**: (PIC 9(07)V9(02)) - Final Payment Amount.
            *   **`PPS-FAC-COSTS`**: (PIC 9(07)V9(02)) - Facility costs.
            *   **`PPS-NEW-FAC-SPEC-RATE`**: (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   **`PPS-OUTLIER-THRESHOLD`**: (PIC 9(07)V9(02)) - Outlier Threshold.
            *   **`PPS-SUBM-DRG-CODE`**: (PIC X(03)) - Submitted DRG Code.
            *   **`PPS-CALC-VERS-CD`**: (PIC X(05)) - Calculation Version Code.
            *   **`PPS-REG-DAYS-USED`**: (PIC 9(03)) - Regular Days used.
            *   **`PPS-LTR-DAYS-USED`**: (PIC 9(03)) - Lifetime Reserve Days used.
            *   **`PPS-BLEND-YEAR`**: (PIC 9(01)) - Blend Year
            *   **`PPS-COLA`**: (PIC 9(01)V9(03)) - COLA (Cost of Living Adjustment).
            *   **`FILLER`**: (PIC X(04)) - Filler.
        *   **`PPS-OTHER-DATA`**:  Other PPS Data.
            *   **`PPS-NAT-LABOR-PCT`**: (PIC 9(01)V9(05)) -  National Labor Percentage.
            *   **`PPS-NAT-NONLABOR-PCT`**: (PIC 9(01)V9(05)) -  National Non-Labor Percentage.
            *   **`PPS-STD-FED-RATE`**: (PIC 9(05)V9(02)) -  Standard Federal Rate.
            *   **`PPS-BDGT-NEUT-RATE`**: (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   **`FILLER`**: (PIC X(20)) - Filler.
        *   **`PPS-PC-DATA`**:  PPS PC Data.
            *   **`PPS-COT-IND`**: (PIC X(01)) -  Cost Outlier Indicator.
            *   **`FILLER`**: (PIC X(20)) - Filler.
    *   **`PRICER-OPT-VERS-SW`**:  Pricer Option/Version Switch. Controls which version of the LTDRV040 programs are passed back.
        *   **`PRICER-OPTION-SW`**: (PIC X(01)) - Pricer Option Switch.
            *   **`ALL-TABLES-PASSED`**:  (VALUE 'A') - Indicates all tables are passed.
            *   **`PROV-RECORD-PASSED`**:  (VALUE 'P') - Indicates the provider record is passed.
        *   **`PPS-VERSIONS`**:  PPS Versions.
            *   **`PPDRV-VERSION`**: (PIC X(05)) -  Version of the PPDRV program.
    *   **`PROV-NEW-HOLD`**:  Provider Record Data.  This structure is used to pass provider-specific information.
        *   **`PROV-NEWREC-HOLD1`**: Provider Record Hold 1.
            *   **`P-NEW-NPI10`**:  New NPI
                *   **`P-NEW-NPI8`**: (PIC X(08)) -  NPI (National Provider Identifier) - first 8 digits.
                *   **`P-NEW-NPI-FILLER`**: (PIC X(02)) -  NPI filler
            *   **`P-NEW-PROVIDER-NO`**:  Provider Number.
                *   **`P-NEW-STATE`**: (PIC 9(02)) -  Provider State.
                *   **`FILLER`**: (PIC X(04)) - Filler.
            *   **`P-NEW-DATE-DATA`**: Date Data.
                *   **`P-NEW-EFF-DATE`**: Effective Date.
                    *   **`P-NEW-EFF-DT-CC`**: (PIC 9(02)) - Effective Date Century/Year.
                    *   **`P-NEW-EFF-DT-YY`**: (PIC 9(02)) - Effective Date Year.
                    *   **`P-NEW-EFF-DT-MM`**: (PIC 9(02)) - Effective Date Month.
                    *   **`P-NEW-EFF-DT-DD`**: (PIC 9(02)) - Effective Date Day.
                *   **`P-NEW-FY-BEGIN-DATE`**: Fiscal Year Begin Date.
                    *   **`P-NEW-FY-BEG-DT-CC`**: (PIC 9(02)) - FY Begin Date Century/Year.
                    *   **`P-NEW-FY-BEG-DT-YY`**: (PIC 9(02)) - FY Begin Date Year.
                    *   **`P-NEW-FY-BEG-DT-MM`**: (PIC 9(02)) - FY Begin Date Month.
                    *   **`P-NEW-FY-BEG-DT-DD`**: (PIC 9(02)) - FY Begin Date Day.
                *   **`P-NEW-REPORT-DATE`**: Report Date.
                    *   **`P-NEW-REPORT-DT-CC`**: (PIC 9(02)) - Report Date Century/Year.
                    *   **`P-NEW-REPORT-DT-YY`**: (PIC 9(02)) - Report Date Year.
                    *   **`P-NEW-REPORT-DT-MM`**: (PIC 9(02)) - Report Date Month.
                    *   **`P-NEW-REPORT-DT-DD`**: (PIC 9(02)) - Report Date Day.
                *   **`P-NEW-TERMINATION-DATE`**: Termination Date.
                    *   **`P-NEW-TERM-DT-CC`**: (PIC 9(02)) - Termination Date Century/Year.
                    *   **`P-NEW-TERM-DT-YY`**: (PIC 9(02)) - Termination Date Year.
                    *   **`P-NEW-TERM-DT-MM`**: (PIC 9(02)) - Termination Date Month.
                    *   **`P-NEW-TERM-DT-DD`**: (PIC 9(02)) - Termination Date Day.
            *   **`P-NEW-WAIVER-CODE`**: (PIC X(01)) -  Waiver Code.
                *   **`P-NEW-WAIVER-STATE`**:  (VALUE 'Y') - Waiver State.
            *   **`P-NEW-INTER-NO`**: (PIC 9(05)) -  Interim Number.
            *   **`P-NEW-PROVIDER-TYPE`**: (PIC X(02)) -  Provider Type.
            *   **`P-NEW-CURRENT-CENSUS-DIV`**: (PIC 9(01)) - Current Census Division.
            *   **`P-NEW-CURRENT-DIV`**: (REDEFINES `P-NEW-CURRENT-CENSUS-DIV`) - Redefines the current census division.
            *   **`P-NEW-MSA-DATA`**: MSA Data.
                *   **`P-NEW-CHG-CODE-INDEX`**: (PIC X) - Charge Code Index.
                *   **`P-NEW-GEO-LOC-MSAX`**: (PIC X(04)) - Geo