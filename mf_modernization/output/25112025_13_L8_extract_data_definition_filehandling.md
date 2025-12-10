## Analysis of the COBOL Programs

Here's an analysis of each COBOL program, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, the program likely interacts with external data through the `COPY` statement which brings in data structures (likely a table) used for DRG calculations. The `COPY` statement could be pulling in a file definition or a set of data.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01 W-STORAGE-REF`
        *   `PIC X(46)`:  Used to store a literal string identifying the program and the working storage section.
    *   `01 CAL-VERSION`
        *   `PIC X(05)`:  Stores the version of the calculation logic.  Value is 'C03.2'.
    *   `01 HOLD-PPS-COMPONENTS`
        *   This structure holds intermediate calculation results.
        *   `05 H-LOS`
            *   `PIC 9(03)`: Length of Stay
        *   `05 H-REG-DAYS`
            *   `PIC 9(03)`: Regular Days
        *   `05 H-TOTAL-DAYS`
            *   `PIC 9(05)`: Total Days
        *   `05 H-SSOT`
            *   `PIC 9(02)`: Short Stay Outlier Threshold
        *   `05 H-BLEND-RTC`
            *   `PIC 9(02)`: Blend Return Code
        *   `05 H-BLEND-FAC`
            *   `PIC 9(01)V9(01)`: Blend Facility Portion (e.g., 0.8)
        *   `05 H-BLEND-PPS`
            *   `PIC 9(01)V9(01)`: Blend PPS Portion (e.g., 0.2)
        *   `05 H-SS-PAY-AMT`
            *   `PIC 9(07)V9(02)`: Short Stay Payment Amount
        *   `05 H-SS-COST`
            *   `PIC 9(07)V9(02)`: Short Stay Cost
        *   `05 H-LABOR-PORTION`
            *   `PIC 9(07)V9(06)`: Labor Portion of the Payment
        *   `05 H-NONLABOR-PORTION`
            *   `PIC 9(07)V9(06)`: Non-Labor Portion of the Payment
        *   `05 H-FIXED-LOSS-AMT`
            *   `PIC 9(07)V9(02)`: Fixed Loss Amount for Outlier calculation.
        *   `05 H-NEW-FAC-SPEC-RATE`
            *   `PIC 9(05)V9(02)`: New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**

    *   `01 BILL-NEW-DATA`
        *   This structure receives billing information from the calling program.
        *   `10 B-NPI10`
            *   `15 B-NPI8`
                *   `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters
            *   `15 B-NPI-FILLER`
                *   `PIC X(02)`: NPI Filler - last 2 characters
        *   `10 B-PROVIDER-NO`
            *   `PIC X(06)`: Provider Number
        *   `10 B-PATIENT-STATUS`
            *   `PIC X(02)`: Patient Status
        *   `10 B-DRG-CODE`
            *   `PIC X(03)`: DRG Code (Diagnosis Related Group)
        *   `10 B-LOS`
            *   `PIC 9(03)`: Length of Stay
        *   `10 B-COV-DAYS`
            *   `PIC 9(03)`: Covered Days
        *   `10 B-LTR-DAYS`
            *   `PIC 9(02)`: Lifetime Reserve Days
        *   `10 B-DISCHARGE-DATE`
            *   `15 B-DISCHG-CC`
                *   `PIC 9(02)`: Century for Discharge Date
            *   `15 B-DISCHG-YY`
                *   `PIC 9(02)`: Year of Discharge Date
            *   `15 B-DISCHG-MM`
                *   `PIC 9(02)`: Month of Discharge Date
            *   `15 B-DISCHG-DD`
                *   `PIC 9(02)`: Day of Discharge Date
        *   `10 B-COV-CHARGES`
            *   `PIC 9(07)V9(02)`: Covered Charges
        *   `10 B-SPEC-PAY-IND`
            *   `PIC X(01)`: Special Payment Indicator
        *   `10 FILLER`
            *   `PIC X(13)`: Unused filler space.
    *   `01 PPS-DATA-ALL`
        *   This structure passes calculation results back to the calling program.
        *   `05 PPS-RTC`
            *   `PIC 9(02)`: Return Code (indicates payment status/reason)
        *   `05 PPS-CHRG-THRESHOLD`
            *   `PIC 9(07)V9(02)`: Charge Threshold for Outlier
        *   `05 PPS-DATA`
            *   `10 PPS-MSA`
                *   `PIC X(04)`: MSA (Metropolitan Statistical Area)
            *   `10 PPS-WAGE-INDEX`
                *   `PIC 9(02)V9(04)`: Wage Index
            *   `10 PPS-AVG-LOS`
                *   `PIC 9(02)V9(01)`: Average Length of Stay
            *   `10 PPS-RELATIVE-WGT`
                *   `PIC 9(01)V9(04)`: Relative Weight (DRG specific)
            *   `10 PPS-OUTLIER-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Outlier Payment Amount
            *   `10 PPS-LOS`
                *   `PIC 9(03)`: Length of Stay
            *   `10 PPS-DRG-ADJ-PAY-AMT`
                *   `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
            *   `10 PPS-FED-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Federal Payment Amount
            *   `10 PPS-FINAL-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Final Payment Amount
            *   `10 PPS-FAC-COSTS`
                *   `PIC 9(07)V9(02)`: Facility Costs
            *   `10 PPS-NEW-FAC-SPEC-RATE`
                *   `PIC 9(07)V9(02)`: New Facility Specific Rate
            *   `10 PPS-OUTLIER-THRESHOLD`
                *   `PIC 9(07)V9(02)`: Outlier Threshold
            *   `10 PPS-SUBM-DRG-CODE`
                *   `PIC X(03)`: Submitted DRG Code
                *   `10 PPS-CALC-VERS-CD`
                    *   `PIC X(05)`: Calculation Version Code
                *   `10 PPS-REG-DAYS-USED`
                    *   `PIC 9(03)`: Regular Days Used
                *   `10 PPS-LTR-DAYS-USED`
                    *   `PIC 9(03)`: Lifetime Reserve Days Used
                *   `10 PPS-BLEND-YEAR`
                    *   `PIC 9(01)`: Blend Year Indicator
                *   `10 PPS-COLA`
                    *   `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   `10 FILLER`
                *   `PIC X(04)`: Filler
        *   `05 PPS-OTHER-DATA`
            *   `10 PPS-NAT-LABOR-PCT`
                *   `PIC 9(01)V9(05)`: National Labor Percentage
            *   `10 PPS-NAT-NONLABOR-PCT`
                *   `PIC 9(01)V9(05)`: National Non-Labor Percentage
            *   `10 PPS-STD-FED-RATE`
                *   `PIC 9(05)V9(02)`: Standard Federal Rate
            *   `10 PPS-BDGT-NEUT-RATE`
                *   `PIC 9(01)V9(03)`: Budget Neutrality Rate
            *   `10 FILLER`
                *   `PIC X(20)`: Filler
        *   `05 PPS-PC-DATA`
            *   `10 PPS-COT-IND`
                *   `PIC X(01)`: Cost Outlier Indicator
            *   `10 FILLER`
                *   `PIC X(20)`: Filler
    *   `01 PRICER-OPT-VERS-SW`
        *   This structure passes the versions of the pricer options back to the calling program.
        *   `05 PRICER-OPTION-SW`
            *   `PIC X(01)`: Pricer Option Switch.  Used to indicate if all tables were passed.
                *   `88 ALL-TABLES-PASSED`  Value 'A'
                *   `88 PROV-RECORD-PASSED` Value 'P'
        *   `05 PPS-VERSIONS`
            *   `10 PPDRV-VERSION`
                *   `PIC X(05)`: Version of the PPDRV program.
    *   `01 PROV-NEW-HOLD`
        *   This structure receives provider specific data from the calling program.
        *   `02 PROV-NEWREC-HOLD1`
            *   `05 P-NEW-NPI10`
                *   `10 P-NEW-NPI8`
                    *   `PIC X(08)`: New NPI (National Provider Identifier) - first 8 characters
                *   `10 P-NEW-NPI-FILLER`
                    *   `PIC X(02)`: New NPI Filler - last 2 characters
            *   `05 P-NEW-PROVIDER-NO`
                *   `10 P-NEW-STATE`
                    *   `PIC 9(02)`: State of the Provider
                *   `10 FILLER`
                    *   `PIC X(04)`: Filler
            *   `05 P-NEW-DATE-DATA`
                *   `10 P-NEW-EFF-DATE`
                    *   `15 P-NEW-EFF-DT-CC`
                        *   `PIC 9(02)`: Century of the Effective Date
                    *   `15 P-NEW-EFF-DT-YY`
                        *   `PIC 9(02)`: Year of the Effective Date
                    *   `15 P-NEW-EFF-DT-MM`
                        *   `PIC 9(02)`: Month of the Effective Date
                    *   `15 P-NEW-EFF-DT-DD`
                        *   `PIC 9(02)`: Day of the Effective Date
                *   `10 P-NEW-FY-BEGIN-DATE`
                    *   `15 P-NEW-FY-BEG-DT-CC`
                        *   `PIC 9(02)`: Century of the Fiscal Year Begin Date
                    *   `15 P-NEW-FY-BEG-DT-YY`
                        *   `PIC 9(02)`: Year of the Fiscal Year Begin Date
                    *   `15 P-NEW-FY-BEG-DT-MM`
                        *   `PIC 9(02)`: Month of the Fiscal Year Begin Date
                    *   `15 P-NEW-FY-BEG-DT-DD`
                        *   `PIC 9(02)`: Day of the Fiscal Year Begin Date
                *   `10 P-NEW-REPORT-DATE`
                    *   `15 P-NEW-REPORT-DT-CC`
                        *   `PIC 9(02)`: Century of the Report Date
                    *   `15 P-NEW-REPORT-DT-YY`
                        *   `PIC 9(02)`: Year of the Report Date
                    *   `15 P-NEW-REPORT-DT-MM`
                        *   `PIC 9(02)`: Month of the Report Date
                    *   `15 P-NEW-REPORT-DT-DD`
                        *   `PIC 9(02)`: Day of the Report Date
                *   `10 P-NEW-TERMINATION-DATE`
                    *   `15 P-NEW-TERM-DT-CC`
                        *   `PIC 9(02)`: Century of the Termination Date
                    *   `15 P-NEW-TERM-DT-YY`
                        *   `PIC 9(02)`: Year of the Termination Date
                    *   `15 P-NEW-TERM-DT-MM`
                        *   `PIC 9(02)`: Month of the Termination Date
                    *   `15 P-NEW-TERM-DT-DD`
                        *   `PIC 9(02)`: Day of the Termination Date
            *   `05 P-NEW-WAIVER-CODE`
                *   `88 P-NEW-WAIVER-STATE` VALUE 'Y'.
            *   `05 P-NEW-INTER-NO`
                *   `PIC 9(05)`:  Intern Number
            *   `05 P-NEW-PROVIDER-TYPE`
                *   `PIC X(02)`: Provider Type Code
            *   `05 P-NEW-CURRENT-CENSUS-DIV`
                *   `PIC 9(01)`: Current Census Division
            *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV`
                *   `PIC 9(01)`: Current Division (Redefines the above)
            *   `05 P-NEW-MSA-DATA`
                *   `10 P-NEW-CHG-CODE-INDEX`
                    *   `PIC X`: Charge Code Index
                *   `10 P-NEW-GEO-LOC-MSAX`
                    *   `PIC X(04)`: Geographic Location for MSA
                *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX`
                    *   `PIC 9(04)`: Geographic Location for MSA (numeric)
                *   `10 P-NEW-WAGE-INDEX-LOC-MSA`
                    *   `PIC X(04)`: Wage Index Location for MSA
                *   `10 P-NEW-STAND-AMT-LOC-MSA`
                    *   `PIC X(04)`: Standard Amount Location for MSA
                *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`
                    *   `15 P-NEW-RURAL-1ST`
                        *   `20 P-NEW-STAND-RURAL`
                            *   `PIC XX`
                                *   `88 P-NEW-STD-RURAL-CHECK` VALUE '  '
                    *   `15 P-NEW-RURAL-2ND`
                        *   `PIC XX`
            *   `05 P-NEW-SOL-COM-DEP-HOSP-YR`
                *   `PIC XX`: Sole Community Hospital Year
            *   `05 P-NEW-LUGAR`
                *   `PIC X`: Lugar
            *   `05 P-NEW-TEMP-RELIEF-IND`
                *   `PIC X`: Temporary Relief Indicator
            *   `05 P-NEW-FED-PPS-BLEND-IND`
                *   `PIC X`: Federal PPS Blend Indicator
            *   `05 FILLER`
                *   `PIC X(05)`: Filler
        *   `02 PROV-NEWREC-HOLD2`
            *   `05 P-NEW-VARIABLES`
                *   `10 P-NEW-FAC-SPEC-RATE`
                    *   `PIC 9(05)V9(02)`: Facility Specific Rate
                *   `10 P-NEW-COLA`
                    *   `PIC 9(01)V9(03)`: COLA (Cost of Living Adjustment)
                *   `10 P-NEW-INTERN-RATIO`
                    *   `PIC 9(01)V9(04)`: Intern Ratio
                *   `10 P-NEW-BED-SIZE`
                    *   `PIC 9(05)`: Bed Size
                *   `10 P-NEW-OPER-CSTCHG-RATIO`
                    *   `PIC 9(01)V9(03)`: Operating Cost-to-Charge Ratio
                *   `10 P-NEW-CMI`
                    *   `PIC 9(01)V9(04)`: CMI (Case Mix Index)
                *   `10 P-NEW-SSI-RATIO`
                    *   `PIC V9(04)`: SSI Ratio
                *   `10 P-NEW-MEDICAID-RATIO`
                    *   `PIC V9(04)`: Medicaid Ratio
                *   `10 P-NEW-PPS-BLEND-YR-IND`
                    *   `PIC 9(01)`: PPS Blend Year Indicator
                *   `10 P-NEW-PRUF-UPDTE-FACTOR`
                    *   `PIC 9(01)V9(05)`: Pruf Update Factor
                *   `10 P-NEW-DSH-PERCENT`
                    *   `PIC V9(04)`: DSH (Disproportionate Share Hospital) Percent
                *   `10 P-NEW-FYE-DATE`
                    *   `PIC X(08)`: Fiscal Year End Date
            *   `05 FILLER`
                *   `PIC X(23)`: Filler
        *   `02 PROV-NEWREC-HOLD3`
            *   `05 P-NEW-PASS-AMT-DATA`
                *   `10 P-NEW-PASS-AMT-CAPITAL`
                    *   `PIC 9(04)V99`: Capital Pass Through Amount
                *   `10 P-NEW-PASS-AMT-DIR-MED-ED`
                    *   `PIC 9(04)V99`: Direct Medical Education Pass Through Amount
                *   `10 P-NEW-PASS-AMT-ORGAN-ACQ`
                    *   `PIC 9(04)V99`: Organ Acquisition Pass Through Amount
                *   `10 P-NEW-PASS-AMT-PLUS-MISC`
                    *   `PIC 9(04)V99`: Plus Misc Pass Through Amount
            *   `05 P-NEW-CAPI-DATA`
                *   `15 P-NEW-CAPI-PPS-PAY-CODE`
                    *   `PIC X`: Capital PPS Pay Code
                *   `15 P-NEW-CAPI-HOSP-SPEC-RATE`
                    *   `PIC 9(04)V99`: Hospital Specific Rate for Capital
                *   `15 P-NEW-CAPI-OLD-HARM-RATE`
                    *   `PIC 9(04)V99`: Old Harm Rate for Capital
                *   `15 P-NEW-CAPI-NEW-HARM-RATIO`
                    *   `PIC 9(01)V9999`: New Harm Ratio for Capital
                *   `15 P-NEW-CAPI-CSTCHG-RATIO`
                    *   `PIC 9V999`: Cost-to-Charge Ratio for Capital
                *   `15 P-NEW-CAPI-NEW-HOSP`
                    *   `PIC X`: New Hospital Indicator for Capital
                *   `15 P-NEW-CAPI-IME`
                    *   `PIC 9V9999`: IME (Indirect Medical Education) for Capital
                *   `15 P-NEW-CAPI-EXCEPTIONS`
                    *   `PIC 9(04)V99`: Capital Exceptions
            *   `05 FILLER`
                *   `PIC X(22)`: Filler
    *   `01 WAGE-NEW-INDEX-RECORD`
        *   This structure receives wage index data from the calling program.
        *   `05 W-MSA`
            *   `PIC X(4)`: MSA (Metropolitan Statistical Area)
        *   `05 W-EFF-DATE`
            *   `PIC X(8)`: Effective Date
        *   `05 W-WAGE-INDEX1`
            *   `PIC S9(02)V9(04)`: Wage Index 1
        *   `05 W-WAGE-INDEX2`
            *   `PIC S9(02)V9(04)`: Wage Index 2
        *   `05 W-WAGE-INDEX3`
            *   `PIC S9(02)V9(04)`: Wage Index 3

*   **PROCEDURE DIVISION:**
    *   The `PROCEDURE DIVISION` uses the `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PRICER-OPT-VERS-SW`, `PROV-NEW-HOLD`, and `WAGE-NEW-INDEX-RECORD` in the `USING` clause, which means these data structures are passed into the program.
    *   The program's main logic flow:
        1.  Initialization (`0100-INITIAL-ROUTINE`).
        2.  Bill Information Edit (`1000-EDIT-THE-BILL-INFO`).
        3.  DRG Code Edit (`1700-EDIT-DRG-CODE`).
        4.  PPS Variable Assembly (`2000-ASSEMBLE-PPS-VARIABLES`).
        5.  Payment Calculation (`3000-CALC-PAYMENT`).
        6.  Outlier Calculation (`7000-CALC-OUTLIER`).
        7.  Blend Calculation (`8000-BLEND`).
        8.  Move Results (`9000-MOVE-RESULTS`).

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, the program likely interacts with external data through the `COPY` statement which brings in data structures (likely a table) used for DRG calculations. The `COPY` statement could be pulling in a file definition or a set of data.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01 W-STORAGE-REF`
        *   `PIC X(46)`:  Used to store a literal string identifying the program and the working storage section.
    *   `01 CAL-VERSION`
        *   `PIC X(05)`:  Stores the version of the calculation logic.  Value is 'C04.2'.
    *   `01 HOLD-PPS-COMPONENTS`
        *   This structure holds intermediate calculation results.
        *   `05 H-LOS`
            *   `PIC 9(03)`: Length of Stay
        *   `05 H-REG-DAYS`
            *   `PIC 9(03)`: Regular Days
        *   `05 H-TOTAL-DAYS`
            *   `PIC 9(05)`: Total Days
        *   `05 H-SSOT`
            *   `PIC 9(02)`: Short Stay Outlier Threshold
        *   `05 H-BLEND-RTC`
            *   `PIC 9(02)`: Blend Return Code
        *   `05 H-BLEND-FAC`
            *   `PIC 9(01)V9(01)`: Blend Facility Portion (e.g., 0.8)
        *   `05 H-BLEND-PPS`
            *   `PIC 9(01)V9(01)`: Blend PPS Portion (e.g., 0.2)
        *   `05 H-SS-PAY-AMT`
            *   `PIC 9(07)V9(02)`: Short Stay Payment Amount
        *   `05 H-SS-COST`
            *   `PIC 9(07)V9(02)`: Short Stay Cost
        *   `05 H-LABOR-PORTION`
            *   `PIC 9(07)V9(06)`: Labor Portion of the Payment
        *   `05 H-NONLABOR-PORTION`
            *   `PIC 9(07)V9(06)`: Non-Labor Portion of the Payment
        *   `05 H-FIXED-LOSS-AMT`
            *   `PIC 9(07)V9(02)`: Fixed Loss Amount for Outlier calculation.
        *   `05 H-NEW-FAC-SPEC-RATE`
            *   `PIC 9(05)V9(02)`: New Facility Specific Rate.
        *   `05 H-LOS-RATIO`
            *   `PIC 9(01)V9(05)`: Length of Stay Ratio

*   **Data Structures in LINKAGE SECTION:**

    *   `01 BILL-NEW-DATA`
        *   This structure receives billing information from the calling program.
        *   `10 B-NPI10`
            *   `15 B-NPI8`
                *   `PIC X(08)`: NPI (National Provider Identifier) - first 8 characters
            *   `15 B-NPI-FILLER`
                *   `PIC X(02)`: NPI Filler - last 2 characters
        *   `10 B-PROVIDER-NO`
            *   `PIC X(06)`: Provider Number
        *   `10 B-PATIENT-STATUS`
            *   `PIC X(02)`: Patient Status
        *   `10 B-DRG-CODE`
            *   `PIC X(03)`: DRG Code (Diagnosis Related Group)
        *   `10 B-LOS`
            *   `PIC 9(03)`: Length of Stay
        *   `10 B-COV-DAYS`
            *   `PIC 9(03)`: Covered Days
        *   `10 B-LTR-DAYS`
            *   `PIC 9(02)`: Lifetime Reserve Days
        *   `10 B-DISCHARGE-DATE`
            *   `15 B-DISCHG-CC`
                *   `PIC 9(02)`: Century for Discharge Date
            *   `15 B-DISCHG-YY`
                *   `PIC 9(02)`: Year of Discharge Date
            *   `15 B-DISCHG-MM`
                *   `PIC 9(02)`: Month of Discharge Date
            *   `15 B-DISCHG-DD`
                *   `PIC 9(02)`: Day of Discharge Date
        *   `10 B-COV-CHARGES`
            *   `PIC 9(07)V9(02)`: Covered Charges
        *   `10 B-SPEC-PAY-IND`
            *   `PIC X(01)`: Special Payment Indicator
        *   `10 FILLER`
            *   `PIC X(13)`: Unused filler space.
    *   `01 PPS-DATA-ALL`
        *   This structure passes calculation results back to the calling program.
        *   `05 PPS-RTC`
            *   `PIC 9(02)`: Return Code (indicates payment status/reason)
        *   `05 PPS-CHRG-THRESHOLD`
            *   `PIC 9(07)V9(02)`: Charge Threshold for Outlier
        *   `05 PPS-DATA`
            *   `10 PPS-MSA`
                *   `PIC X(04)`: MSA (Metropolitan Statistical Area)
            *   `10 PPS-WAGE-INDEX`
                *   `PIC 9(02)V9(04)`: Wage Index
            *   `10 PPS-AVG-LOS`
                *   `PIC 9(02)V9(01)`: Average Length of Stay
            *   `10 PPS-RELATIVE-WGT`
                *   `PIC 9(01)V9(04)`: Relative Weight (DRG specific)
            *   `10 PPS-OUTLIER-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Outlier Payment Amount
            *   `10 PPS-LOS`
                *   `PIC 9(03)`: Length of Stay
            *   `10 PPS-DRG-ADJ-PAY-AMT`
                *   `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
            *   `10 PPS-FED-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Federal Payment Amount
            *   `10 PPS-FINAL-PAY-AMT`
                *   `PIC 9(07)V9(02)`: Final Payment Amount
            *   `10 PPS-FAC-COSTS`
                *   `PIC 9(07)V9(02)`: Facility Costs
            *   `10 PPS-NEW-FAC-SPEC-RATE`
                *   `PIC 9(07)V9(02)`: New Facility Specific Rate
            *   `10 PPS-OUTLIER-THRESHOLD`
                *   `PIC 9(07)V9(02)`: Outlier Threshold
            *   `10 PPS-SUBM-DRG-CODE`
                *   `PIC X(03)`: Submitted DRG Code
                *   `10 PPS-CALC-VERS-CD`
                    *   `PIC X(05)`: Calculation Version Code
                *   `10 PPS-REG-DAYS-USED`
                    *   `PIC 9(03)`: Regular Days Used
                *   `10 PPS-LTR-DAYS-USED`
                    *   `PIC 9(03)`: Lifetime Reserve Days Used
                *   `10 PPS-BLEND-YEAR`
                    *   `PIC 9(01)`: Blend Year Indicator
                *   `10 PPS-COLA`
                    *   `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   `10 FILLER`
                *   `PIC X(04)`: Filler
        *   `05 PPS-OTHER-DATA`
            *   `10 PPS-NAT-LABOR-PCT`
                *   `PIC 9(01)V9(05)`: National Labor Percentage
            *   `10 PPS-NAT-NONLABOR-PCT`
                *   `PIC 9(01)V9(05)`: National Non-Labor Percentage
            *   `10 PPS-STD-FED-RATE`
                *   `PIC 9(05)V9(02)`: Standard Federal Rate
            *   `10 PPS-BDGT-NEUT-RATE`
                *   `PIC 9(01)V9(03)`: Budget Neutrality Rate
            *   `10 FILLER`
                *   `PIC X(20)`: Filler
        *   `05 PPS-PC-DATA`
            *   `10 PPS-COT-IND`
                *   `PIC X(01)`: Cost Outlier Indicator
            *   `10 FILLER`
                *   `PIC X(20)`: Filler
    *   `01 PRICER-OPT-VERS-SW`
        *   This structure passes the versions of the pricer options back to the calling program.
        *   `05 PRICER-OPTION-SW`
            *   `PIC X(01)`: Pricer Option Switch.  Used to indicate if all tables were passed.
                *   `88 ALL-TABLES-PASSED`  Value 'A'
                *   `88 PROV-RECORD-PASSED` Value 'P'
        *   `05 PPS-VERSIONS`
            *   `10 PPDRV-VERSION`
                *   `PIC X(05)`: Version of the PPDRV program.
    *   `01 PROV-NEW-HOLD`
        *   This structure receives provider specific data from the calling program.
        *   `02 PROV-NEWREC-HOLD1`
            *   `05 P-NEW-NPI10`
                *   `10 P-NEW-NPI8`
                    *   `PIC X(08)`: New NPI (National Provider Identifier) - first 8 characters
                *   `10 P-NEW-NPI-FILLER`
                    *   `PIC X(02)`: New NPI Filler - last 2 characters
            *   `05 P-NEW-PROVIDER-NO`
                *   `10 P-NEW-STATE`
                    *   `PIC 9(02)`: State of the Provider
                *   `10 FILLER`
                    *   `PIC X(04)`: Filler
            *   `05 P-NEW-DATE-DATA`
                *   `10 P-NEW-EFF-DATE`
                    *   `15 P-NEW-EFF-DT-CC`
                        *   `PIC 9(02)`: Century of the Effective Date
                    *   `15 P-NEW-EFF-DT-YY`
                        *   `PIC 9(02)`: Year of the Effective Date
                    *   `15 P-NEW-EFF-DT-MM`