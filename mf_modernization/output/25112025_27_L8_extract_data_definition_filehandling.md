## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

#### Files Accessed and their Descriptions

This program does not explicitly access any files in the `FILE-CONTROL` section. However, it *includes* the file definition `LTDRG031` via a `COPY` statement. This indicates that the program relies on the data structures defined in `LTDRG031`, likely a table of DRG codes and related data.

#### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**
    *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description "W O R K I N G S T O R A G E". Used for internal program identification or debugging.
*   **`CAL-VERSION`**
    *   `PIC X(05)`: A 5-character alphanumeric field containing the version number of the calculation logic, set to 'C03.2'.
*   **`HOLD-PPS-COMPONENTS`**
    *   This is a group item containing various numeric fields used to store intermediate calculation results and input values related to the Patient Payment System (PPS).
        *   `H-LOS` (`PIC 9(03)`): Length of Stay (LOS), a 3-digit numeric field.
        *   `H-REG-DAYS` (`PIC 9(03)`): Regular Days, a 3-digit numeric field.
        *   `H-TOTAL-DAYS` (`PIC 9(05)`): Total Days, a 5-digit numeric field.
        *   `H-SSOT` (`PIC 9(02)`):  Likely Short Stay Outlier Threshold, a 2-digit numeric field.
        *   `H-BLEND-RTC` (`PIC 9(02)`): Blend Return Code, a 2-digit numeric field.
        *   `H-BLEND-FAC` (`PIC 9(01)V9(01)`): Blend Facility Rate, a numeric field with 1 integer and 1 decimal place.
        *   `H-BLEND-PPS` (`PIC 9(01)V9(01)`): Blend PPS Rate, a numeric field with 1 integer and 1 decimal place.
        *   `H-SS-PAY-AMT` (`PIC 9(07)V9(02)`): Short Stay Payment Amount, a numeric field with 7 integer and 2 decimal places.
        *   `H-SS-COST` (`PIC 9(07)V9(02)`): Short Stay Cost, a numeric field with 7 integer and 2 decimal places.
        *   `H-LABOR-PORTION` (`PIC 9(07)V9(06)`): Labor Portion, a numeric field with 7 integer and 6 decimal places.
        *   `H-NONLABOR-PORTION` (`PIC 9(07)V9(06)`): Non-Labor Portion, a numeric field with 7 integer and 6 decimal places.
        *   `H-FIXED-LOSS-AMT` (`PIC 9(07)V9(02)`): Fixed Loss Amount, a numeric field with 7 integer and 2 decimal places.
        *   `H-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`):  New Facility Specific Rate, a numeric field with 5 integer and 2 decimal places.

#### Data Structures in LINKAGE SECTION

*   **`BILL-NEW-DATA`**
    *   This group item represents the input data passed *to* the program, likely a bill record from a calling program.
        *   `B-NPI10`
            *   `B-NPI8` (`PIC X(08)`):  National Provider Identifier (NPI), an 8-character alphanumeric field.
            *   `B-NPI-FILLER` (`PIC X(02)`): Filler for NPI, a 2-character alphanumeric field.
        *   `B-PROVIDER-NO` (`PIC X(06)`): Provider Number, a 6-character alphanumeric field.
        *   `B-PATIENT-STATUS` (`PIC X(02)`): Patient Status, a 2-character alphanumeric field.
        *   `B-DRG-CODE` (`PIC X(03)`): DRG Code, a 3-character alphanumeric field.
        *   `B-LOS` (`PIC 9(03)`): Length of Stay, a 3-digit numeric field.
        *   `B-COV-DAYS` (`PIC 9(03)`): Covered Days, a 3-digit numeric field.
        *   `B-LTR-DAYS` (`PIC 9(02)`): Lifetime Reserve Days, a 2-digit numeric field.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` (`PIC 9(02)`): Discharge Date - Century/Code, a 2-digit numeric field.
            *   `B-DISCHG-YY` (`PIC 9(02)`): Discharge Date - Year, a 2-digit numeric field.
            *   `B-DISCHG-MM` (`PIC 9(02)`): Discharge Date - Month, a 2-digit numeric field.
            *   `B-DISCHG-DD` (`PIC 9(02)`): Discharge Date - Day, a 2-digit numeric field.
        *   `B-COV-CHARGES` (`PIC 9(07)V9(02)`): Covered Charges, a numeric field with 7 integer and 2 decimal places.
        *   `B-SPEC-PAY-IND` (`PIC X(01)`): Special Payment Indicator, a 1-character alphanumeric field.
        *   `FILLER` (`PIC X(13)`): Filler, a 13-character alphanumeric field.
*   **`PPS-DATA-ALL`**
    *   This group item represents the output data passed *back* to the calling program, containing calculated PPS information.
        *   `PPS-RTC` (`PIC 9(02)`): PPS Return Code, a 2-digit numeric field. Indicates the result of the calculation.
        *   `PPS-CHRG-THRESHOLD` (`PIC 9(07)V9(02)`): Charge Threshold, a numeric field with 7 integer and 2 decimal places.
        *   `PPS-DATA`
            *   `PPS-MSA` (`PIC X(04)`):  Metropolitan Statistical Area (MSA) code, a 4-character alphanumeric field.
            *   `PPS-WAGE-INDEX` (`PIC 9(02)V9(04)`): Wage Index, a numeric field with 2 integer and 4 decimal places.
            *   `PPS-AVG-LOS` (`PIC 9(02)V9(01)`): Average Length of Stay, a numeric field with 2 integer and 1 decimal place.
            *   `PPS-RELATIVE-WGT` (`PIC 9(01)V9(04)`): Relative Weight, a numeric field with 1 integer and 4 decimal places.
            *   `PPS-OUTLIER-PAY-AMT` (`PIC 9(07)V9(02)`): Outlier Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-LOS` (`PIC 9(03)`): Length of Stay, a 3-digit numeric field.
            *   `PPS-DRG-ADJ-PAY-AMT` (`PIC 9(07)V9(02)`): DRG Adjusted Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FED-PAY-AMT` (`PIC 9(07)V9(02)`): Federal Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FINAL-PAY-AMT` (`PIC 9(07)V9(02)`): Final Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FAC-COSTS` (`PIC 9(07)V9(02)`): Facility Costs, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-NEW-FAC-SPEC-RATE` (`PIC 9(07)V9(02)`): New Facility Specific Rate, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-OUTLIER-THRESHOLD` (`PIC 9(07)V9(02)`): Outlier Threshold, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-SUBM-DRG-CODE` (`PIC X(03)`): Submitted DRG Code, a 3-character alphanumeric field.
            *   `PPS-CALC-VERS-CD` (`PIC X(05)`): Calculation Version Code, a 5-character alphanumeric field.
            *   `PPS-REG-DAYS-USED` (`PIC 9(03)`): Regular Days Used, a 3-digit numeric field.
            *   `PPS-LTR-DAYS-USED` (`PIC 9(03)`): Lifetime Reserve Days Used, a 3-digit numeric field.
            *   `PPS-BLEND-YEAR` (`PIC 9(01)`): Blend Year, a 1-digit numeric field.
            *   `PPS-COLA` (`PIC 9(01)V9(03)`): Cost of Living Adjustment, a numeric field with 1 integer and 3 decimal places.
            *   `FILLER` (`PIC X(04)`): Filler, a 4-character alphanumeric field.
        *   `PPS-OTHER-DATA`
            *   `PPS-NAT-LABOR-PCT` (`PIC 9(01)V9(05)`): National Labor Percentage, a numeric field with 1 integer and 5 decimal places.
            *   `PPS-NAT-NONLABOR-PCT` (`PIC 9(01)V9(05)`): National Non-Labor Percentage, a numeric field with 1 integer and 5 decimal places.
            *   `PPS-STD-FED-RATE` (`PIC 9(05)V9(02)`): Standard Federal Rate, a numeric field with 5 integer and 2 decimal places.
            *   `PPS-BDGT-NEUT-RATE` (`PIC 9(01)V9(03)`): Budget Neutrality Rate, a numeric field with 1 integer and 3 decimal places.
            *   `FILLER` (`PIC X(20)`): Filler, a 20-character alphanumeric field.
        *   `PPS-PC-DATA`
            *   `PPS-COT-IND` (`PIC X(01)`): Cost Outlier Indicator, a 1-character alphanumeric field.
            *   `FILLER` (`PIC X(20)`): Filler, a 20-character alphanumeric field.
*   **`PRICER-OPT-VERS-SW`**
    *   This group item seems to be for passing pricer options and version information.
        *   `PRICER-OPTION-SW` (`PIC X(01)`): Pricer Option Switch, a 1-character alphanumeric field.
            *   `ALL-TABLES-PASSED` (88 level, `VALUE 'A'`): Condition name indicating all tables are passed.
            *   `PROV-RECORD-PASSED` (88 level, `VALUE 'P'`): Condition name indicating provider record is passed.
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` (`PIC X(05)`):  Version of the PPDRV program, a 5-character alphanumeric field.
*   **`PROV-NEW-HOLD`**
    *   This group item contains provider-specific information.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`
                *   `P-NEW-NPI8` (`PIC X(08)`):  New NPI, an 8-character alphanumeric field.
                *   `P-NEW-NPI-FILLER` (`PIC X(02)`): Filler for new NPI, a 2-character alphanumeric field.
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` (`PIC 9(02)`):  New State, a 2-digit numeric field.
                *   `FILLER` (`PIC X(04)`): Filler, a 4-character alphanumeric field.
            *   `P-NEW-DATE-DATA`
                *   `P-NEW-EFF-DATE`
                    *   `P-NEW-EFF-DT-CC` (`PIC 9(02)`): Effective Date - Century/Code, a 2-digit numeric field.
                    *   `P-NEW-EFF-DT-YY` (`PIC 9(02)`): Effective Date - Year, a 2-digit numeric field.
                    *   `P-NEW-EFF-DT-MM` (`PIC 9(02)`): Effective Date - Month, a 2-digit numeric field.
                    *   `P-NEW-EFF-DT-DD` (`PIC 9(02)`): Effective Date - Day, a 2-digit numeric field.
                *   `P-NEW-FY-BEGIN-DATE`
                    *   `P-NEW-FY-BEG-DT-CC` (`PIC 9(02)`): Fiscal Year Begin Date - Century/Code, a 2-digit numeric field.
                    *   `P-NEW-FY-BEG-DT-YY` (`PIC 9(02)`): Fiscal Year Begin Date - Year, a 2-digit numeric field.
                    *   `P-NEW-FY-BEG-DT-MM` (`PIC 9(02)`): Fiscal Year Begin Date - Month, a 2-digit numeric field.
                    *   `P-NEW-FY-BEG-DT-DD` (`PIC 9(02)`): Fiscal Year Begin Date - Day, a 2-digit numeric field.
                *   `P-NEW-REPORT-DATE`
                    *   `P-NEW-REPORT-DT-CC` (`PIC 9(02)`): Report Date - Century/Code, a 2-digit numeric field.
                    *   `P-NEW-REPORT-DT-YY` (`PIC 9(02)`): Report Date - Year, a 2-digit numeric field.
                    *   `P-NEW-REPORT-DT-MM` (`PIC 9(02)`): Report Date - Month, a 2-digit numeric field.
                    *   `P-NEW-REPORT-DT-DD` (`PIC 9(02)`): Report Date - Day, a 2-digit numeric field.
                *   `P-NEW-TERMINATION-DATE`
                    *   `P-NEW-TERM-DT-CC` (`PIC 9(02)`): Termination Date - Century/Code, a 2-digit numeric field.
                    *   `P-NEW-TERM-DT-YY` (`PIC 9(02)`): Termination Date - Year, a 2-digit numeric field.
                    *   `P-NEW-TERM-DT-MM` (`PIC 9(02)`): Termination Date - Month, a 2-digit numeric field.
                    *   `P-NEW-TERM-DT-DD` (`PIC 9(02)`): Termination Date - Day, a 2-digit numeric field.
            *   `P-NEW-WAIVER-CODE` (`PIC X(01)`): New Waiver Code, a 1-character alphanumeric field.
                *   `P-NEW-WAIVER-STATE` (88 level, `VALUE 'Y'`): Condition name indicating waiver state.
            *   `P-NEW-INTER-NO` (`PIC 9(05)`): New Internal Number, a 5-digit numeric field.
            *   `P-NEW-PROVIDER-TYPE` (`PIC X(02)`): New Provider Type, a 2-character alphanumeric field.
            *   `P-NEW-CURRENT-CENSUS-DIV` (`PIC 9(01)`): New Current Census Division, a 1-digit numeric field.
            *   `P-NEW-CURRENT-DIV` REDEFINES `P-NEW-CURRENT-CENSUS-DIV` (`PIC 9(01)`): Redefines the previous field.
            *   `P-NEW-MSA-DATA`
                *   `P-NEW-CHG-CODE-INDEX` (`PIC X`): New Charge Code Index, a 1-character alphanumeric field.
                *   `P-NEW-GEO-LOC-MSAX` (`PIC X(04)`): New Geo Location MSA X, a 4-character alphanumeric field.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES `P-NEW-GEO-LOC-MSAX` (`PIC 9(04)`):  Redefines the previous field.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (`PIC X(04)`): New Wage Index Location MSA, a 4-character alphanumeric field.
                *   `P-NEW-STAND-AMT-LOC-MSA` (`PIC X(04)`): New Standard Amount Location MSA, a 4-character alphanumeric field.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES `P-NEW-STAND-AMT-LOC-MSA`
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` (`PIC XX`): New Stand Rural, a 2-character alphanumeric field.
                            *   `P-NEW-STD-RURAL-CHECK` (88 level, `VALUE '  '`): Condition name for rural check.
                    *   `P-NEW-RURAL-2ND` (`PIC XX`): New Rural 2nd, a 2-character alphanumeric field.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (`PIC XX`): New Sol Com Dep Hosp Year, a 2-character alphanumeric field.
            *   `P-NEW-LUGAR` (`PIC X`): New Lugar, a 1-character alphanumeric field.
            *   `P-NEW-TEMP-RELIEF-IND` (`PIC X`): New Temp Relief Indicator, a 1-character alphanumeric field.
            *   `P-NEW-FED-PPS-BLEND-IND` (`PIC X`): New Federal PPS Blend Indicator, a 1-character alphanumeric field.
            *   `FILLER` (`PIC X(05)`): Filler, a 5-character alphanumeric field.
        *   `PROV-NEWREC-HOLD2`
            *   `P-NEW-VARIABLES`
                *   `P-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`): New Facility Specific Rate, a numeric field with 5 integer and 2 decimal places.
                *   `P-NEW-COLA` (`PIC 9(01)V9(03)`): New Cost of Living Adjustment, a numeric field with 1 integer and 3 decimal places.
                *   `P-NEW-INTERN-RATIO` (`PIC 9(01)V9(04)`): New Intern Ratio, a numeric field with 1 integer and 4 decimal places.
                *   `P-NEW-BED-SIZE` (`PIC 9(05)`): New Bed Size, a 5-digit numeric field.
                *   `P-NEW-OPER-CSTCHG-RATIO` (`PIC 9(01)V9(03)`): New Operating Cost to Charge Ratio, a numeric field with 1 integer and 3 decimal places.
                *   `P-NEW-CMI` (`PIC 9(01)V9(04)`): New CMI, a numeric field with 1 integer and 4 decimal places.
                *   `P-NEW-SSI-RATIO` (`PIC V9(04)`): New SSI Ratio, a numeric field with 4 decimal places.
                *   `P-NEW-MEDICAID-RATIO` (`PIC V9(04)`): New Medicaid Ratio, a numeric field with 4 decimal places.
                *   `P-NEW-PPS-BLEND-YR-IND` (`PIC 9(01)`): New PPS Blend Year Indicator, a 1-digit numeric field.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (`PIC 9(01)V9(05)`): New PRUF Update Factor, a numeric field with 1 integer and 5 decimal places.
                *   `P-NEW-DSH-PERCENT` (`PIC V9(04)`): New DSH Percent, a numeric field with 4 decimal places.
                *   `P-NEW-FYE-DATE` (`PIC X(08)`): New FYE Date, an 8-character alphanumeric field.
            *   `FILLER` (`PIC X(23)`): Filler, a 23-character alphanumeric field.
        *   `PROV-NEWREC-HOLD3`
            *   `P-NEW-PASS-AMT-DATA`
                *   `P-NEW-PASS-AMT-CAPITAL` (`PIC 9(04)V99`): New Passed Amount Capital, a numeric field with 4 integer and 2 decimal places.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (`PIC 9(04)V99`): New Passed Amount Direct Medical Education, a numeric field with 4 integer and 2 decimal places.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (`PIC 9(04)V99`): New Passed Amount Organ Acquisition, a numeric field with 4 integer and 2 decimal places.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (`PIC 9(04)V99`): New Passed Amount Plus Misc, a numeric field with 4 integer and 2 decimal places.
            *   `P-NEW-CAPI-DATA`
                *   `P-NEW-CAPI-PPS-PAY-CODE` (`PIC X`): New CAPI PPS Pay Code, a 1-character alphanumeric field.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (`PIC 9(04)V99`): New CAPI Hospital Specific Rate, a numeric field with 4 integer and 2 decimal places.
                *   `P-NEW-CAPI-OLD-HARM-RATE` (`PIC 9(04)V99`): New CAPI Old Harm Rate, a numeric field with 4 integer and 2 decimal places.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (`PIC 9(01)V9999`): New CAPI New Harm Ratio, a numeric field with 1 integer and 4 decimal places.
                *   `P-NEW-CAPI-CSTCHG-RATIO` (`PIC 9V999`): New CAPI Cost to Charge Ratio, a numeric field with 3 decimal places.
                *   `P-NEW-CAPI-NEW-HOSP` (`PIC X`): New CAPI New Hospital, a 1-character alphanumeric field.
                *   `P-NEW-CAPI-IME` (`PIC 9V9999`): New CAPI IME, a numeric field with 4 decimal places.
                *   `P-NEW-CAPI-EXCEPTIONS` (`PIC 9(04)V99`): New CAPI Exceptions, a numeric field with 4 integer and 2 decimal places.
            *   `FILLER` (`PIC X(22)`): Filler, a 22-character alphanumeric field.
*   **`WAGE-NEW-INDEX-RECORD`**
    *   This group item contains wage index information.
        *   `W-MSA` (`PIC X(4)`): Wage Index MSA, a 4-character alphanumeric field.
        *   `W-EFF-DATE` (`PIC X(8)`): Wage Index Effective Date, an 8-character alphanumeric field.
        *   `W-WAGE-INDEX1` (`PIC S9(02)V9(04)`): Wage Index 1, a signed numeric field with 2 integer and 4 decimal places.
        *   `W-WAGE-INDEX2` (`PIC S9(02)V9(04)`): Wage Index 2, a signed numeric field with 2 integer and 4 decimal places.
        *   `W-WAGE-INDEX3` (`PIC S9(02)V9(04)`): Wage Index 3, a signed numeric field with 2 integer and 4 decimal places.

#### Procedure Division

The `PROCEDURE DIVISION` processes the input data to calculate the PPS payment. Key steps include:

*   Initialization (`0100-INITIAL-ROUTINE`).
*   Data validation (`1000-EDIT-THE-BILL-INFO`).
*   DRG code lookup (`1700-EDIT-DRG-CODE`).
*   Assembling PPS variables (`2000-ASSEMBLE-PPS-VARIABLES`).
*   Calculating the payment (`3000-CALC-PAYMENT`).
*   Calculating outliers (`7000-CALC-OUTLIER`).
*   Blending rates (8000-BLEND)
*   Moving results to the output area (9000-MOVE-RESULTS)

### Program: LTCAL042

#### Files Accessed and their Descriptions

This program also does *not* explicitly access any files in the `FILE-CONTROL` section. It includes the `LTDRG031` file definition via `COPY` statement. This indicates that the program relies on the data structures defined in `LTDRG031`, likely a table of DRG codes and related data.

#### Data Structures in WORKING-STORAGE SECTION

*   **`W-STORAGE-REF`**
    *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description "W O R K I N G S T O R A G E". Used for internal program identification or debugging.
*   **`CAL-VERSION`**
    *   `PIC X(05)`: A 5-character alphanumeric field containing the version number of the calculation logic, set to 'C04.2'.
*   **`HOLD-PPS-COMPONENTS`**
    *   This is a group item containing various numeric fields used to store intermediate calculation results and input values related to the Patient Payment System (PPS).  This is very similar to the one in LTCAL032.
        *   `H-LOS` (`PIC 9(03)`): Length of Stay (LOS), a 3-digit numeric field.
        *   `H-REG-DAYS` (`PIC 9(03)`): Regular Days, a 3-digit numeric field.
        *   `H-TOTAL-DAYS` (`PIC 9(05)`): Total Days, a 5-digit numeric field.
        *   `H-SSOT` (`PIC 9(02)`):  Likely Short Stay Outlier Threshold, a 2-digit numeric field.
        *   `H-BLEND-RTC` (`PIC 9(02)`): Blend Return Code, a 2-digit numeric field.
        *   `H-BLEND-FAC` (`PIC 9(01)V9(01)`): Blend Facility Rate, a numeric field with 1 integer and 1 decimal place.
        *   `H-BLEND-PPS` (`PIC 9(01)V9(01)`): Blend PPS Rate, a numeric field with 1 integer and 1 decimal place.
        *   `H-SS-PAY-AMT` (`PIC 9(07)V9(02)`): Short Stay Payment Amount, a numeric field with 7 integer and 2 decimal places.
        *   `H-SS-COST` (`PIC 9(07)V9(02)`): Short Stay Cost, a numeric field with 7 integer and 2 decimal places.
        *   `H-LABOR-PORTION` (`PIC 9(07)V9(06)`): Labor Portion, a numeric field with 7 integer and 6 decimal places.
        *   `H-NONLABOR-PORTION` (`PIC 9(07)V9(06)`): Non-Labor Portion, a numeric field with 7 integer and 6 decimal places.
        *   `H-FIXED-LOSS-AMT` (`PIC 9(07)V9(02)`): Fixed Loss Amount, a numeric field with 7 integer and 2 decimal places.
        *   `H-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`):  New Facility Specific Rate, a numeric field with 5 integer and 2 decimal places.
        *   `H-LOS-RATIO` (`PIC 9(01)V9(05)`): LOS Ratio, a numeric field with 1 integer and 5 decimal places.

#### Data Structures in LINKAGE SECTION

*   **`BILL-NEW-DATA`**
    *   This group item represents the input data passed *to* the program, likely a bill record from a calling program. It is identical to the one in LTCAL032.
        *   `B-NPI10`
            *   `B-NPI8` (`PIC X(08)`):  National Provider Identifier (NPI), an 8-character alphanumeric field.
            *   `B-NPI-FILLER` (`PIC X(02)`): Filler for NPI, a 2-character alphanumeric field.
        *   `B-PROVIDER-NO` (`PIC X(06)`): Provider Number, a 6-character alphanumeric field.
        *   `B-PATIENT-STATUS` (`PIC X(02)`): Patient Status, a 2-character alphanumeric field.
        *   `B-DRG-CODE` (`PIC X(03)`): DRG Code, a 3-character alphanumeric field.
        *   `B-LOS` (`PIC 9(03)`): Length of Stay, a 3-digit numeric field.
        *   `B-COV-DAYS` (`PIC 9(03)`): Covered Days, a 3-digit numeric field.
        *   `B-LTR-DAYS` (`PIC 9(02)`): Lifetime Reserve Days, a 2-digit numeric field.
        *   `B-DISCHARGE-DATE`
            *   `B-DISCHG-CC` (`PIC 9(02)`): Discharge Date - Century/Code, a 2-digit numeric field.
            *   `B-DISCHG-YY` (`PIC 9(02)`): Discharge Date - Year, a 2-digit numeric field.
            *   `B-DISCHG-MM` (`PIC 9(02)`): Discharge Date - Month, a 2-digit numeric field.
            *   `B-DISCHG-DD` (`PIC 9(02)`): Discharge Date - Day, a 2-digit numeric field.
        *   `B-COV-CHARGES` (`PIC 9(07)V9(02)`): Covered Charges, a numeric field with 7 integer and 2 decimal places.
        *   `B-SPEC-PAY-IND` (`PIC X(01)`): Special Payment Indicator, a 1-character alphanumeric field.
        *   `FILLER` (`PIC X(13)`): Filler, a 13-character alphanumeric field.
*   **`PPS-DATA-ALL`**
    *   This group item represents the output data passed *back* to the calling program, containing calculated PPS information. It is identical to the one in LTCAL032.
        *   `PPS-RTC` (`PIC 9(02)`): PPS Return Code, a 2-digit numeric field. Indicates the result of the calculation.
        *   `PPS-CHRG-THRESHOLD` (`PIC 9(07)V9(02)`): Charge Threshold, a numeric field with 7 integer and 2 decimal places.
        *   `PPS-DATA`
            *   `PPS-MSA` (`PIC X(04)`):  Metropolitan Statistical Area (MSA) code, a 4-character alphanumeric field.
            *   `PPS-WAGE-INDEX` (`PIC 9(02)V9(04)`): Wage Index, a numeric field with 2 integer and 4 decimal places.
            *   `PPS-AVG-LOS` (`PIC 9(02)V9(01)`): Average Length of Stay, a numeric field with 2 integer and 1 decimal place.
            *   `PPS-RELATIVE-WGT` (`PIC 9(01)V9(04)`): Relative Weight, a numeric field with 1 integer and 4 decimal places.
            *   `PPS-OUTLIER-PAY-AMT` (`PIC 9(07)V9(02)`): Outlier Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-LOS` (`PIC 9(03)`): Length of Stay, a 3-digit numeric field.
            *   `PPS-DRG-ADJ-PAY-AMT` (`PIC 9(07)V9(02)`): DRG Adjusted Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FED-PAY-AMT` (`PIC 9(07)V9(02)`): Federal Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FINAL-PAY-AMT` (`PIC 9(07)V9(02)`): Final Payment Amount, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-FAC-COSTS` (`PIC 9(07)V9(02)`): Facility Costs, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-NEW-FAC-SPEC-RATE` (`PIC 9(07)V9(02)`): New Facility Specific Rate, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-OUTLIER-THRESHOLD` (`PIC 9(07)V9(02)`): Outlier Threshold, a numeric field with 7 integer and 2 decimal places.
            *   `PPS-SUBM-DRG-CODE` (`PIC X(03)`): Submitted DRG Code, a 3-character alphanumeric field.
            *   `PPS-CALC-VERS-CD` (`PIC X(05)`): Calculation Version Code, a 5-character alphanumeric field.
            *   `PPS-REG-DAYS-USED` (`PIC 9(03)`): Regular Days Used, a 3-digit numeric field.
            *   `PPS-LTR-DAYS-USED` (`PIC 9(03)`): Lifetime Reserve Days Used, a 3-digit numeric field.
            *   `PPS-BLEND-YEAR` (`