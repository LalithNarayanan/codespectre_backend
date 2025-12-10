## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program likely interacts with external data through the `COPY` statement, which includes the `LTDRG031` copybook. It seems that this program retrieves DRG related data from the `LTDRG031` copybook.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `01 W-STORAGE-REF`
        *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description ("W O R K I N G S T O R A G E").
    *   `01 CAL-VERSION`
        *   `PIC X(05)`: A 5-character alphanumeric field storing the calculation version ('C03.2').
    *   `01 HOLD-PPS-COMPONENTS`
        *   This structure holds intermediate calculation results.
            *   `05 H-LOS`: `PIC 9(03)`: Length of Stay (LOS) - 3 digit numeric.
            *   `05 H-REG-DAYS`: `PIC 9(03)`: Regular Days - 3 digit numeric.
            *   `05 H-TOTAL-DAYS`: `PIC 9(05)`: Total Days - 5 digit numeric.
            *   `05 H-SSOT`: `PIC 9(02)`: Short Stay Outlier Threshold - 2 digit numeric.
            *   `05 H-BLEND-RTC`: `PIC 9(02)`: Blend Return Code - 2 digit numeric.
            *   `05 H-BLEND-FAC`: `PIC 9(01)V9(01)`: Blend Facility Portion - 1 integer, 1 decimal.
            *   `05 H-BLEND-PPS`: `PIC 9(01)V9(01)`: Blend PPS Portion - 1 integer, 1 decimal.
            *   `05 H-SS-PAY-AMT`: `PIC 9(07)V9(02)`: Short Stay Payment Amount - 7 integer, 2 decimal.
            *   `05 H-SS-COST`: `PIC 9(07)V9(02)`: Short Stay Cost - 7 integer, 2 decimal.
            *   `05 H-LABOR-PORTION`: `PIC 9(07)V9(06)`: Labor Portion - 7 integer, 6 decimal.
            *   `05 H-NONLABOR-PORTION`: `PIC 9(07)V9(06)`: Non-Labor Portion - 7 integer, 6 decimal.
            *   `05 H-FIXED-LOSS-AMT`: `PIC 9(07)V9(02)`: Fixed Loss Amount - 7 integer, 2 decimal.
            *   `05 H-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)`: New Facility Specific Rate - 5 integer, 2 decimal.
    *   Data structures defined in the `LTDRG031` copybook are included here.
        *   This copybook likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay.
        *   The exact structure of this data is not visible in the provided code, but it is accessed via the `SEARCH ALL` statement in the procedure division.

*   **LINKAGE SECTION Data Structures:**

    *   `01 BILL-NEW-DATA`
        *   This structure represents the input data passed to the program.
            *   `10 B-NPI10`: NPI (National Provider Identifier)
                *   `15 B-NPI8`: `PIC X(08)`:  First 8 characters of NPI.
                *   `15 B-NPI-FILLER`: `PIC X(02)`: Filler for NPI.
            *   `10 B-PROVIDER-NO`: `PIC X(06)`: Provider Number - 6 character alphanumeric.
            *   `10 B-PATIENT-STATUS`: `PIC X(02)`: Patient Status - 2 character alphanumeric.
            *   `10 B-DRG-CODE`: `PIC X(03)`: DRG Code - 3 character alphanumeric.
            *   `10 B-LOS`: `PIC 9(03)`: Length of Stay - 3 digit numeric.
            *   `10 B-COV-DAYS`: `PIC 9(03)`: Covered Days - 3 digit numeric.
            *   `10 B-LTR-DAYS`: `PIC 9(02)`: Lifetime Reserve Days - 2 digit numeric.
            *   `10 B-DISCHARGE-DATE`: Discharge Date
                *   `15 B-DISCHG-CC`: `PIC 9(02)`: Century of Discharge date.
                *   `15 B-DISCHG-YY`: `PIC 9(02)`: Year of Discharge date.
                *   `15 B-DISCHG-MM`: `PIC 9(02)`: Month of Discharge date.
                *   `15 B-DISCHG-DD`: `PIC 9(02)`: Day of Discharge date.
            *   `10 B-COV-CHARGES`: `PIC 9(07)V9(02)`: Covered Charges - 7 integer, 2 decimal.
            *   `10 B-SPEC-PAY-IND`: `PIC X(01)`: Special Payment Indicator - 1 character alphanumeric.
            *   `10 FILLER`: `PIC X(13)`: Filler - 13 character alphanumeric.
    *   `01 PPS-DATA-ALL`
        *   This structure is used to pass the calculated PPS related data back to the calling program.
            *   `05 PPS-RTC`: `PIC 9(02)`: Return Code - 2 digit numeric.
            *   `05 PPS-CHRG-THRESHOLD`: `PIC 9(07)V9(02)`: Charges Threshold - 7 integer, 2 decimal.
            *   `05 PPS-DATA`: PPS data structure
                *   `10 PPS-MSA`: `PIC X(04)`: MSA (Metropolitan Statistical Area) - 4 character alphanumeric.
                *   `10 PPS-WAGE-INDEX`: `PIC 9(02)V9(04)`: Wage Index - 2 integer, 4 decimal.
                *   `10 PPS-AVG-LOS`: `PIC 9(02)V9(01)`: Average Length of Stay - 2 integer, 1 decimal.
                *   `10 PPS-RELATIVE-WGT`: `PIC 9(01)V9(04)`: Relative Weight - 1 integer, 4 decimal.
                *   `10 PPS-OUTLIER-PAY-AMT`: `PIC 9(07)V9(02)`: Outlier Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-LOS`: `PIC 9(03)`: Length of Stay - 3 digit numeric.
                *   `10 PPS-DRG-ADJ-PAY-AMT`: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FED-PAY-AMT`: `PIC 9(07)V9(02)`: Federal Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FINAL-PAY-AMT`: `PIC 9(07)V9(02)`: Final Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FAC-COSTS`: `PIC 9(07)V9(02)`: Facility Costs - 7 integer, 2 decimal.
                *   `10 PPS-NEW-FAC-SPEC-RATE`: `PIC 9(07)V9(02)`: New Facility Specific Rate - 7 integer, 2 decimal.
                *   `10 PPS-OUTLIER-THRESHOLD`: `PIC 9(07)V9(02)`: Outlier Threshold - 7 integer, 2 decimal.
                *   `10 PPS-SUBM-DRG-CODE`: `PIC X(03)`: Submitted DRG Code - 3 character alphanumeric.
                *   `10 PPS-CALC-VERS-CD`: `PIC X(05)`: Calculation Version Code - 5 character alphanumeric.
                *   `10 PPS-REG-DAYS-USED`: `PIC 9(03)`: Regular Days Used - 3 digit numeric.
                *   `10 PPS-LTR-DAYS-USED`: `PIC 9(03)`: Lifetime Reserve Days Used - 3 digit numeric.
                *   `10 PPS-BLEND-YEAR`: `PIC 9(01)`: Blend Year - 1 digit numeric.
                *   `10 PPS-COLA`: `PIC 9(01)V9(03)`: Cost of Living Adjustment (COLA) - 1 integer, 3 decimal.
                *   `10 FILLER`: `PIC X(04)`: Filler - 4 character alphanumeric.
            *   `05 PPS-OTHER-DATA`: Other PPS data
                *   `10 PPS-NAT-LABOR-PCT`: `PIC 9(01)V9(05)`: National Labor Percentage - 1 integer, 5 decimal.
                *   `10 PPS-NAT-NONLABOR-PCT`: `PIC 9(01)V9(05)`: National Non-Labor Percentage - 1 integer, 5 decimal.
                *   `10 PPS-STD-FED-RATE`: `PIC 9(05)V9(02)`: Standard Federal Rate - 5 integer, 2 decimal.
                *   `10 PPS-BDGT-NEUT-RATE`: `PIC 9(01)V9(03)`: Budget Neutrality Rate - 1 integer, 3 decimal.
                *   `10 FILLER`: `PIC X(20)`: Filler - 20 character alphanumeric.
            *   `05 PPS-PC-DATA`: PPS PC Data
                *   `10 PPS-COT-IND`: `PIC X(01)`: Cost Outlier Indicator - 1 character alphanumeric.
                *   `10 FILLER`: `PIC X(20)`: Filler - 20 character alphanumeric.
    *   `01 PRICER-OPT-VERS-SW`
        *   Used to pass the versions of the LTDRV031 programs back to the calling program.
            *   `05 PRICER-OPTION-SW`: `PIC X(01)`: Pricer Option Switch.
                *   `88 ALL-TABLES-PASSED`: `VALUE 'A'`:  Condition to check if all tables passed.
                *   `88 PROV-RECORD-PASSED`: `VALUE 'P'`: Condition to check if provider record passed.
            *   `05 PPS-VERSIONS`:
                *   `10 PPDRV-VERSION`: `PIC X(05)`: Version of the PPDRV program.
    *   `01 PROV-NEW-HOLD`
        *   This structure represents the provider record passed to the program.
            *   `02 PROV-NEWREC-HOLD1`:
                *   `05 P-NEW-NPI10`: NPI (National Provider Identifier)
                    *   `10 P-NEW-NPI8`: `PIC X(08)`:  First 8 characters of NPI.
                    *   `10 P-NEW-NPI-FILLER`: `PIC X(02)`: Filler for NPI.
                *   `05 P-NEW-PROVIDER-NO`:
                    *   `10 P-NEW-STATE`: `PIC 9(02)`: State Code - 2 digit numeric.
                    *   `10 FILLER`: `PIC X(04)`: Filler - 4 character alphanumeric.
                *   `05 P-NEW-DATE-DATA`: Date data
                    *   `10 P-NEW-EFF-DATE`: Effective Date
                        *   `15 P-NEW-EFF-DT-CC`: `PIC 9(02)`: Century of Effective Date.
                        *   `15 P-NEW-EFF-DT-YY`: `PIC 9(02)`: Year of Effective Date.
                        *   `15 P-NEW-EFF-DT-MM`: `PIC 9(02)`: Month of Effective Date.
                        *   `15 P-NEW-EFF-DT-DD`: `PIC 9(02)`: Day of Effective Date.
                    *   `10 P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                        *   `15 P-NEW-FY-BEG-DT-CC`: `PIC 9(02)`: Century of Fiscal Year Begin Date.
                        *   `15 P-NEW-FY-BEG-DT-YY`: `PIC 9(02)`: Year of Fiscal Year Begin Date.
                        *   `15 P-NEW-FY-BEG-DT-MM`: `PIC 9(02)`: Month of Fiscal Year Begin Date.
                        *   `15 P-NEW-FY-BEG-DT-DD`: `PIC 9(02)`: Day of Fiscal Year Begin Date.
                    *   `10 P-NEW-REPORT-DATE`: Report Date
                        *   `15 P-NEW-REPORT-DT-CC`: `PIC 9(02)`: Century of Report Date.
                        *   `15 P-NEW-REPORT-DT-YY`: `PIC 9(02)`: Year of Report Date.
                        *   `15 P-NEW-REPORT-DT-MM`: `PIC 9(02)`: Month of Report Date.
                        *   `15 P-NEW-REPORT-DT-DD`: `PIC 9(02)`: Day of Report Date.
                    *   `10 P-NEW-TERMINATION-DATE`: Termination Date
                        *   `15 P-NEW-TERM-DT-CC`: `PIC 9(02)`: Century of Termination Date.
                        *   `15 P-NEW-TERM-DT-YY`: `PIC 9(02)`: Year of Termination Date.
                        *   `15 P-NEW-TERM-DT-MM`: `PIC 9(02)`: Month of Termination Date.
                        *   `15 P-NEW-TERM-DT-DD`: `PIC 9(02)`: Day of Termination Date.
                *   `05 P-NEW-WAIVER-CODE`: `PIC X(01)`: Waiver Code.
                    *   `88 P-NEW-WAIVER-STATE`: `VALUE 'Y'`: Condition to check if waiver state.
                *   `05 P-NEW-INTER-NO`: `PIC 9(05)`: Internal Number - 5 digit numeric.
                *   `05 P-NEW-PROVIDER-TYPE`: `PIC X(02)`: Provider Type - 2 character alphanumeric.
                *   `05 P-NEW-CURRENT-CENSUS-DIV`: `PIC 9(01)`: Current Census Division - 1 digit numeric.
                *   `05 P-NEW-CURRENT-DIV`: `REDEFINES P-NEW-CURRENT-CENSUS-DIV`: Redefines the current census division.
                *   `05 P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data
                    *   `10 P-NEW-CHG-CODE-INDEX`: `PIC X`: Charge Code Index - 1 character alphanumeric.
                    *   `10 P-NEW-GEO-LOC-MSAX`: `PIC X(04)`: Geographic Location MSA - 4 character alphanumeric.
                    *   `10 P-NEW-GEO-LOC-MSA9`:  `REDEFINES P-NEW-GEO-LOC-MSAX`: Redefines the geographic location MSA - 4 digit numeric.
                    *   `10 P-NEW-WAGE-INDEX-LOC-MSA`: `PIC X(04)`: Wage Index Location MSA - 4 character alphanumeric.
                    *   `10 P-NEW-STAND-AMT-LOC-MSA`: `PIC X(04)`: Standard Amount Location MSA - 4 character alphanumeric.
                    *   `10 P-NEW-STAND-AMT-LOC-MSA9`: `REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Redefines the standard amount location MSA.
                        *   `15 P-NEW-RURAL-1ST`:
                            *   `20 P-NEW-STAND-RURAL`: `PIC XX`: Standard Rural - 2 character alphanumeric.
                                *   `88 P-NEW-STD-RURAL-CHECK`: `VALUE '  '`: Condition to check standard rural check.
                        *   `15 P-NEW-RURAL-2ND`: `PIC XX`:  Rural 2nd - 2 character alphanumeric.
                *   `05 P-NEW-SOL-COM-DEP-HOSP-YR`: `PIC XX`:  SOL COM DEP HOSP YR - 2 character alphanumeric.
                *   `05 P-NEW-LUGAR`: `PIC X`: Lugar - 1 character alphanumeric.
                *   `05 P-NEW-TEMP-RELIEF-IND`: `PIC X`: Temporary Relief Indicator - 1 character alphanumeric.
                *   `05 P-NEW-FED-PPS-BLEND-IND`: `PIC X`: Federal PPS Blend Indicator - 1 character alphanumeric.
                *   `05 FILLER`: `PIC X(05)`: Filler - 5 character alphanumeric.
            *   `02 PROV-NEWREC-HOLD2`:
                *   `05 P-NEW-VARIABLES`:
                    *   `10 P-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)`: Facility Specific Rate - 5 integer, 2 decimal.
                    *   `10 P-NEW-COLA`: `PIC 9(01)V9(03)`: Cost of Living Adjustment (COLA) - 1 integer, 3 decimal.
                    *   `10 P-NEW-INTERN-RATIO`: `PIC 9(01)V9(04)`: Intern Ratio - 1 integer, 4 decimal.
                    *   `10 P-NEW-BED-SIZE`: `PIC 9(05)`: Bed Size - 5 digit numeric.
                    *   `10 P-NEW-OPER-CSTCHG-RATIO`: `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio - 1 integer, 3 decimal.
                    *   `10 P-NEW-CMI`: `PIC 9(01)V9(04)`: CMI (Case Mix Index) - 1 integer, 4 decimal.
                    *   `10 P-NEW-SSI-RATIO`: `PIC V9(04)`: SSI Ratio - 4 decimal.
                    *   `10 P-NEW-MEDICAID-RATIO`: `PIC V9(04)`: Medicaid Ratio - 4 decimal.
                    *   `10 P-NEW-PPS-BLEND-YR-IND`: `PIC 9(01)`: PPS Blend Year Indicator - 1 digit numeric.
                    *   `10 P-NEW-PRUF-UPDTE-FACTOR`: `PIC 9(01)V9(05)`: PRUF Update Factor - 1 integer, 5 decimal.
                    *   `10 P-NEW-DSH-PERCENT`: `PIC V9(04)`: DSH Percentage - 4 decimal.
                    *   `10 P-NEW-FYE-DATE`: `PIC X(08)`: Fiscal Year End Date - 8 character alphanumeric.
                *   `05 FILLER`: `PIC X(23)`: Filler - 23 character alphanumeric.
            *   `02 PROV-NEWREC-HOLD3`:
                *   `05 P-NEW-PASS-AMT-DATA`:
                    *   `10 P-NEW-PASS-AMT-CAPITAL`: `PIC 9(04)V99`: Passed Amount Capital - 4 integer, 2 decimal.
                    *   `10 P-NEW-PASS-AMT-DIR-MED-ED`: `PIC 9(04)V99`: Passed Amount Direct Medical Education - 4 integer, 2 decimal.
                    *   `10 P-NEW-PASS-AMT-ORGAN-ACQ`: `PIC 9(04)V99`: Passed Amount Organ Acquisition - 4 integer, 2 decimal.
                    *   `10 P-NEW-PASS-AMT-PLUS-MISC`: `PIC 9(04)V99`: Passed Amount Plus Misc - 4 integer, 2 decimal.
                *   `05 P-NEW-CAPI-DATA`: Capital Data
                    *   `15 P-NEW-CAPI-PPS-PAY-CODE`: `PIC X`: Capital PPS Pay Code - 1 character alphanumeric.
                    *   `15 P-NEW-CAPI-HOSP-SPEC-RATE`: `PIC 9(04)V99`: Capital Hospital Specific Rate - 4 integer, 2 decimal.
                    *   `15 P-NEW-CAPI-OLD-HARM-RATE`: `PIC 9(04)V99`: Capital Old Harm Rate - 4 integer, 2 decimal.
                    *   `15 P-NEW-CAPI-NEW-HARM-RATIO`: `PIC 9(01)V9999`: Capital New Harm Ratio - 1 integer, 4 decimal.
                    *   `15 P-NEW-CAPI-CSTCHG-RATIO`: `PIC 9V999`: Capital Cost to Charge Ratio - 3 decimal.
                    *   `15 P-NEW-CAPI-NEW-HOSP`: `PIC X`: Capital New Hospital - 1 character alphanumeric.
                    *   `15 P-NEW-CAPI-IME`: `PIC 9V9999`: Capital IME - 4 decimal.
                    *   `15 P-NEW-CAPI-EXCEPTIONS`: `PIC 9(04)V99`: Capital Exceptions - 4 integer, 2 decimal.
                *   `05 FILLER`: `PIC X(22)`: Filler - 22 character alphanumeric.
    *   `01 WAGE-NEW-INDEX-RECORD`
        *   This structure represents the wage index record passed to the program.
            *   `05 W-MSA`: `PIC X(4)`: MSA (Metropolitan Statistical Area) - 4 character alphanumeric.
            *   `05 W-EFF-DATE`: `PIC X(8)`: Effective Date - 8 character alphanumeric.
            *   `05 W-WAGE-INDEX1`: `PIC S9(02)V9(04)`: Wage Index 1 - 2 integer, 4 decimal (signed).
            *   `05 W-WAGE-INDEX2`: `PIC S9(02)V9(04)`: Wage Index 2 - 2 integer, 4 decimal (signed).
            *   `05 W-WAGE-INDEX3`: `PIC S9(02)V9(04)`: Wage Index 3 - 2 integer, 4 decimal (signed).

*   **PROCEDURE DIVISION:**

    *   The `PROCEDURE DIVISION` uses the following `USING` parameters:
        *   `BILL-NEW-DATA`: Input bill data.
        *   `PPS-DATA-ALL`:  Output PPS data.
        *   `PRICER-OPT-VERS-SW`: Pricer Option and Version Switch.
        *   `PROV-NEW-HOLD`: Provider record.
        *   `WAGE-NEW-INDEX-RECORD`: Wage Index Record.

    *   The program's logic includes:
        *   Initialization (`0100-INITIAL-ROUTINE`).
        *   Bill data edits (`1000-EDIT-THE-BILL-INFO`).
        *   DRG code editing (`1700-EDIT-DRG-CODE`).  This likely involves looking up the DRG code in a table (defined in the included copybook `LTDRG031`).
        *   Assembling PPS variables (`2000-ASSEMBLE-PPS-VARIABLES`).
        *   Calculating the payment (`3000-CALC-PAYMENT`).
        *   Calculating outliers (`7000-CALC-OUTLIER`).
        *   Blending rates (`8000-BLEND`).
        *   Moving results to the output structure (`9000-MOVE-RESULTS`).

### Program: LTCAL042

*   **File Access:**
    *   Similar to LTCAL032, no explicit `SELECT` statements are present.  It accesses data through the `COPY` statement, including the `LTDRG031` copybook, and likely interacts with external data.

*   **WORKING-STORAGE SECTION Data Structures:**
    *   `01 W-STORAGE-REF`
        *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description ("W O R K I N G S T O R A G E").
    *   `01 CAL-VERSION`
        *   `PIC X(05)`: A 5-character alphanumeric field storing the calculation version ('C04.2').
    *   `01 HOLD-PPS-COMPONENTS`
        *   This structure holds intermediate calculation results.
            *   `05 H-LOS`: `PIC 9(03)`: Length of Stay (LOS) - 3 digit numeric.
            *   `05 H-REG-DAYS`: `PIC 9(03)`: Regular Days - 3 digit numeric.
            *   `05 H-TOTAL-DAYS`: `PIC 9(05)`: Total Days - 5 digit numeric.
            *   `05 H-SSOT`: `PIC 9(02)`: Short Stay Outlier Threshold - 2 digit numeric.
            *   `05 H-BLEND-RTC`: `PIC 9(02)`: Blend Return Code - 2 digit numeric.
            *   `05 H-BLEND-FAC`: `PIC 9(01)V9(01)`: Blend Facility Portion - 1 integer, 1 decimal.
            *   `05 H-BLEND-PPS`: `PIC 9(01)V9(01)`: Blend PPS Portion - 1 integer, 1 decimal.
            *   `05 H-SS-PAY-AMT`: `PIC 9(07)V9(02)`: Short Stay Payment Amount - 7 integer, 2 decimal.
            *   `05 H-SS-COST`: `PIC 9(07)V9(02)`: Short Stay Cost - 7 integer, 2 decimal.
            *   `05 H-LABOR-PORTION`: `PIC 9(07)V9(06)`: Labor Portion - 7 integer, 6 decimal.
            *   `05 H-NONLABOR-PORTION`: `PIC 9(07)V9(06)`: Non-Labor Portion - 7 integer, 6 decimal.
            *   `05 H-FIXED-LOSS-AMT`: `PIC 9(07)V9(02)`: Fixed Loss Amount - 7 integer, 2 decimal.
            *   `05 H-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)`: New Facility Specific Rate - 5 integer, 2 decimal.
            *   `05 H-LOS-RATIO`: `PIC 9(01)V9(05)`: Length of Stay Ratio - 1 integer, 5 decimal.
    *   Data structures defined in the `LTDRG031` copybook are included here.
        *   This copybook likely contains DRG (Diagnosis Related Group) information, such as relative weights and average lengths of stay.
        *   The exact structure of this data is not visible in the provided code, but it is accessed via the `SEARCH ALL` statement in the procedure division.

*   **LINKAGE SECTION Data Structures:**
    *   `01 BILL-NEW-DATA`
        *   This structure represents the input data passed to the program.
            *   `10 B-NPI10`: NPI (National Provider Identifier)
                *   `15 B-NPI8`: `PIC X(08)`:  First 8 characters of NPI.
                *   `15 B-NPI-FILLER`: `PIC X(02)`: Filler for NPI.
            *   `10 B-PROVIDER-NO`: `PIC X(06)`: Provider Number - 6 character alphanumeric.
            *   `10 B-PATIENT-STATUS`: `PIC X(02)`: Patient Status - 2 character alphanumeric.
            *   `10 B-DRG-CODE`: `PIC X(03)`: DRG Code - 3 character alphanumeric.
            *   `10 B-LOS`: `PIC 9(03)`: Length of Stay - 3 digit numeric.
            *   `10 B-COV-DAYS`: `PIC 9(03)`: Covered Days - 3 digit numeric.
            *   `10 B-LTR-DAYS`: `PIC 9(02)`: Lifetime Reserve Days - 2 digit numeric.
            *   `10 B-DISCHARGE-DATE`: Discharge Date
                *   `15 B-DISCHG-CC`: `PIC 9(02)`: Century of Discharge date.
                *   `15 B-DISCHG-YY`: `PIC 9(02)`: Year of Discharge date.
                *   `15 B-DISCHG-MM`: `PIC 9(02)`: Month of Discharge date.
                *   `15 B-DISCHG-DD`: `PIC 9(02)`: Day of Discharge date.
            *   `10 B-COV-CHARGES`: `PIC 9(07)V9(02)`: Covered Charges - 7 integer, 2 decimal.
            *   `10 B-SPEC-PAY-IND`: `PIC X(01)`: Special Payment Indicator - 1 character alphanumeric.
            *   `10 FILLER`: `PIC X(13)`: Filler - 13 character alphanumeric.
    *   `01 PPS-DATA-ALL`
        *   This structure is used to pass the calculated PPS related data back to the calling program.
            *   `05 PPS-RTC`: `PIC 9(02)`: Return Code - 2 digit numeric.
            *   `05 PPS-CHRG-THRESHOLD`: `PIC 9(07)V9(02)`: Charges Threshold - 7 integer, 2 decimal.
            *   `05 PPS-DATA`: PPS data structure
                *   `10 PPS-MSA`: `PIC X(04)`: MSA (Metropolitan Statistical Area) - 4 character alphanumeric.
                *   `10 PPS-WAGE-INDEX`: `PIC 9(02)V9(04)`: Wage Index - 2 integer, 4 decimal.
                *   `10 PPS-AVG-LOS`: `PIC 9(02)V9(01)`: Average Length of Stay - 2 integer, 1 decimal.
                *   `10 PPS-RELATIVE-WGT`: `PIC 9(01)V9(04)`: Relative Weight - 1 integer, 4 decimal.
                *   `10 PPS-OUTLIER-PAY-AMT`: `PIC 9(07)V9(02)`: Outlier Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-LOS`: `PIC 9(03)`: Length of Stay - 3 digit numeric.
                *   `10 PPS-DRG-ADJ-PAY-AMT`: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FED-PAY-AMT`: `PIC 9(07)V9(02)`: Federal Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FINAL-PAY-AMT`: `PIC 9(07)V9(02)`: Final Payment Amount - 7 integer, 2 decimal.
                *   `10 PPS-FAC-COSTS`: `PIC 9(07)V9(02)`: Facility Costs - 7 integer, 2 decimal.
                *   `10 PPS-NEW-FAC-SPEC-RATE`: `PIC 9(07)V9(02)`: New Facility Specific Rate - 7 integer, 2 decimal.
                *   `10 PPS-OUTLIER-THRESHOLD`: `PIC 9(07)V9(02)`: Outlier Threshold - 7 integer, 2 decimal.
                *   `10 PPS-SUBM-DRG-CODE`: `PIC X(03)`: Submitted DRG Code - 3 character alphanumeric.
                *   `10 PPS-CALC-VERS-CD`: `PIC X(05)`: Calculation Version Code - 5 character alphanumeric.
                *   `10 PPS-REG-DAYS-USED`: `PIC 9(03)`: Regular Days Used - 3 digit numeric.
                *   `10 PPS-LTR-DAYS-USED`: `PIC 9(03)`: Lifetime Reserve Days Used - 3 digit numeric.
                *   `10 PPS-BLEND-YEAR`: `PIC 9(01)`: Blend Year - 1 digit numeric.
                *   `10 PPS-COLA`: `PIC 9(01)V9(03)`: Cost of Living Adjustment (COLA) - 1 integer, 3 decimal.
                *   `10 FILLER`: `PIC X(04)`: Filler - 4 character alphanumeric.
            *   `05 PPS-OTHER-DATA`: Other PPS data
                *   `10 PPS-NAT-LABOR-PCT`: `PIC 9(01)V9(05)`: National Labor Percentage - 1 integer, 5 decimal.
                *   `10 PPS-NAT-NONLABOR-PCT`: `PIC 9(01)V9(05)`: National Non-Labor Percentage - 1 integer, 5 decimal.
                *   `10 PPS-STD-FED-RATE`: `PIC 9(05)V9(02)`: Standard Federal Rate - 5 integer, 2 decimal.
                *   `10 PPS-BDGT-NEUT-RATE`: `PIC 9(01)V9(03)`: Budget Neutrality Rate -