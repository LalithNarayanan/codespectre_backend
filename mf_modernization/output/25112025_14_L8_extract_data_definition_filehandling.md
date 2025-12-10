## Analysis of COBOL Programs

### LTCAL032

#### File Access Details

*   **COPY LTDRG031:** This is a COPYBOOK included in the program.

#### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field storing the program's version.
*   **HOLD-PPS-COMPONENTS:** A group of fields used to store intermediate calculation results.
    *   **H-LOS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing Length of Stay.
    *   **H-REG-DAYS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing Regular Days.
    *   **H-TOTAL-DAYS:**
        *   `PIC 9(05)`: A 5-digit numeric field representing Total Days.
    *   **H-SSOT:**
        *   `PIC 9(02)`: A 2-digit numeric field.
    *   **H-BLEND-RTC:**
        *   `PIC 9(02)`: A 2-digit numeric field related to blending.
    *   **H-BLEND-FAC:**
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field (1 integer, 1 decimal) representing a facility blend factor.
    *   **H-BLEND-PPS:**
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field (1 integer, 1 decimal) representing a PPS blend factor.
    *   **H-SS-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing Short Stay Payment Amount.
    *   **H-SS-COST:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing Short Stay Cost.
    *   **H-LABOR-PORTION:**
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field (7 integer, 6 decimal) representing the labor portion of a calculation.
    *   **H-NONLABOR-PORTION:**
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field (7 integer, 6 decimal) representing the non-labor portion of a calculation.
    *   **H-FIXED-LOSS-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing the fixed loss amount.
    *   **H-NEW-FAC-SPEC-RATE:**
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal).
*   **PPS-NAT-LABOR-PCT:**
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal)
*   **PPS-NAT-NONLABOR-PCT:**
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal)
*   **PPS-STD-FED-RATE:**
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal)
*   **PPS-BDGT-NEUT-RATE:**
        *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal)
*   **PPS-DRG-ADJ-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FED-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FINAL-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FAC-COSTS:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-NEW-FAC-SPEC-RATE:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-OUTLIER-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PRICER-OPT-VERS-SW:**
    *   **PRICER-OPTION-SW:**
        *   `PIC X(01)`: A 1-character alphanumeric field indicating the pricer option.  Uses 88-levels for values 'A' (all tables passed) and 'P' (provider record passed).
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:**
            *   `PIC X(05)`:  A 5-character alphanumeric field representing the version of the PPDRV.

#### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**  This is a group of fields representing the bill data passed *to* the program.
    *   **B-NPI10:**
        *   **B-NPI8:**
            *   `PIC X(08)`:  An 8-character alphanumeric field representing part of the NPI.
        *   **B-NPI-FILLER:**
            *   `PIC X(02)`: A 2-character alphanumeric filler for the NPI.
    *   **B-PROVIDER-NO:**
        *   `PIC X(06)`: A 6-character alphanumeric field representing the provider number.
    *   **B-PATIENT-STATUS:**
        *   `PIC X(02)`: A 2-character alphanumeric field representing the patient status.
    *   **B-DRG-CODE:**
        *   `PIC X(03)`: A 3-character alphanumeric field representing the DRG code.
    *   **B-LOS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing the length of stay.
    *   **B-COV-DAYS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing covered days.
    *   **B-LTR-DAYS:**
        *   `PIC 9(02)`: A 2-digit numeric field representing lifetime reserve days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:**
            *   `PIC 9(02)`: A 2-digit numeric field for the century/decade of the discharge date.
        *   **B-DISCHG-YY:**
            *   `PIC 9(02)`: A 2-digit numeric field for the year of the discharge date.
        *   **B-DISCHG-MM:**
            *   `PIC 9(02)`: A 2-digit numeric field for the month of the discharge date.
        *   **B-DISCHG-DD:**
            *   `PIC 9(02)`: A 2-digit numeric field for the day of the discharge date.
    *   **B-COV-CHARGES:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing covered charges.
    *   **B-SPEC-PAY-IND:**
        *   `PIC X(01)`: A 1-character alphanumeric field representing special payment indicator.
    *   **FILLER:**
        *   `PIC X(13)`: A 13-character alphanumeric filler.
*   **PPS-DATA-ALL:**  This is a group of fields representing data passed *to* and *from* the program.
    *   **PPS-RTC:**
        *   `PIC 9(02)`: A 2-digit numeric field representing the return code.
    *   **PPS-CHRG-THRESHOLD:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
    *   **PPS-DATA:**
        *   **PPS-MSA:**
            *   `PIC X(04)`: A 4-character alphanumeric field representing the MSA.
        *   **PPS-WAGE-INDEX:**
            *   `PIC 9(02)V9(04)`: A 6-digit numeric field (2 integer, 4 decimal) representing the wage index.
        *   **PPS-AVG-LOS:**
            *   `PIC 9(02)V9(01)`: A 3-digit numeric field (2 integer, 1 decimal) representing the average length of stay.
        *   **PPS-RELATIVE-WGT:**
            *   `PIC 9(01)V9(04)`: A 5-digit numeric field (1 integer, 4 decimal) representing the relative weight.
        *   **PPS-OUTLIER-PAY-AMT:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing the outlier payment amount.
        *   **PPS-LOS:**
            *   `PIC 9(03)`: A 3-digit numeric field representing the length of stay.
        *   **PPS-DRG-ADJ-PAY-AMT:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-FED-PAY-AMT:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-FINAL-PAY-AMT:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-FAC-COSTS:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-NEW-FAC-SPEC-RATE:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-OUTLIER-THRESHOLD:**
            *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
        *   **PPS-SUBM-DRG-CODE:**
            *   `PIC X(03)`: A 3-character alphanumeric field representing the submitted DRG code.
        *   **PPS-CALC-VERS-CD:**
            *   `PIC X(05)`:  A 5-character alphanumeric field representing the calculation version code.
        *   **PPS-REG-DAYS-USED:**
            *   `PIC 9(03)`: A 3-digit numeric field.
        *   **PPS-LTR-DAYS-USED:**
            *   `PIC 9(03)`: A 3-digit numeric field.
        *   **PPS-BLEND-YEAR:**
            *   `PIC 9(01)`: A 1-digit numeric field indicating the blend year.
        *   **PPS-COLA:**
            *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal) representing the COLA.
        *   **FILLER:**
            *   `PIC X(04)`: A 4-character alphanumeric filler.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:**
            *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal) representing the national labor percentage.
        *   **PPS-NAT-NONLABOR-PCT:**
            *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal) representing the national non-labor percentage.
        *   **PPS-STD-FED-RATE:**
            *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal) representing the standard federal rate.
        *   **PPS-BDGT-NEUT-RATE:**
            *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal) representing the budget neutrality rate.
        *   **FILLER:**
            *   `PIC X(20)`: A 20-character alphanumeric filler.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:**
            *   `PIC X(01)`: A 1-character alphanumeric field representing the cost outlier indicator.
        *   **FILLER:**
            *   `PIC X(20)`: A 20-character alphanumeric filler.
*   **PROV-NEW-HOLD:**  This is a group of fields representing the provider record data passed *to* the program.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:**
                *   `PIC X(08)`: An 8-character alphanumeric field.
            *   **P-NEW-NPI-FILLER:**
                *   `PIC X(02)`: A 2-character alphanumeric field.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:**
                *   `PIC 9(02)`: A 2-digit numeric field.
            *   **FILLER:**
                *   `PIC X(04)`: A 4-character alphanumeric filler.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-EFF-DT-YY:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-EFF-DT-MM:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-EFF-DT-DD:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-FY-BEG-DT-YY:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-FY-BEG-DT-MM:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-FY-BEG-DT-DD:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-REPORT-DT-YY:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-REPORT-DT-MM:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-REPORT-DT-DD:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-TERM-DT-YY:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-TERM-DT-MM:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
                *   **P-NEW-TERM-DT-DD:**
                    *   `PIC 9(02)`: A 2-digit numeric field.
        *   **P-NEW-WAIVER-CODE:**
            *   `PIC X(01)`: A 1-character alphanumeric field.
            *   **P-NEW-WAIVER-STATE:**
                *   `VALUE 'Y'`: An 88-level that checks if waiver code is 'Y'.
        *   **P-NEW-INTER-NO:**
            *   `PIC 9(05)`: A 5-digit numeric field.
        *   **P-NEW-PROVIDER-TYPE:**
            *   `PIC X(02)`: A 2-character alphanumeric field.
        *   **P-NEW-CURRENT-CENSUS-DIV:**
            *   `PIC 9(01)`: A 1-digit numeric field.
        *   **P-NEW-CURRENT-DIV:**
            *   `PIC 9(01)`: A 1-digit numeric field (REDEFINES P-NEW-CURRENT-CENSUS-DIV).
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:**
                *   `PIC X`: A 1-character alphanumeric field.
            *   **P-NEW-GEO-LOC-MSAX:**
                *   `PIC X(04)`: A 4-character alphanumeric field.
            *   **P-NEW-GEO-LOC-MSA9:**
                *   `PIC 9(04)`: A 4-digit numeric field (REDEFINES P-NEW-GEO-LOC-MSAX).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:**
                *   `PIC X(04)`: A 4-character alphanumeric field.
            *   **P-NEW-STAND-AMT-LOC-MSA:**
                *   `PIC X(04)`: A 4-character alphanumeric field.
            *   **P-NEW-STAND-AMT-LOC-MSA9:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:**
                        *   `PIC XX`: A 2-character alphanumeric field.
                        *   **P-NEW-STD-RURAL-CHECK:**
                            *   `VALUE '  '`: An 88-level that checks if P-NEW-STAND-RURAL is spaces.
                    *   **P-NEW-RURAL-2ND:**
                        *   `PIC XX`: A 2-character alphanumeric field.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:**
            *   `PIC XX`: A 2-character alphanumeric field.
        *   **P-NEW-LUGAR:**
            *   `PIC X`: A 1-character alphanumeric field.
        *   **P-NEW-TEMP-RELIEF-IND:**
            *   `PIC X`: A 1-character alphanumeric field.
        *   **P-NEW-FED-PPS-BLEND-IND:**
            *   `PIC X`: A 1-character alphanumeric field.
        *   **FILLER:**
            *   `PIC X(05)`: A 5-character alphanumeric filler.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:**
                *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal).
            *   **P-NEW-COLA:**
                *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal) representing the COLA.
            *   **P-NEW-INTERN-RATIO:**
                *   `PIC 9(01)V9(04)`: A 5-digit numeric field (1 integer, 4 decimal).
            *   **P-NEW-BED-SIZE:**
                *   `PIC 9(05)`: A 5-digit numeric field.
            *   **P-NEW-OPER-CSTCHG-RATIO:**
                *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal).
            *   **P-NEW-CMI:**
                *   `PIC 9(01)V9(04)`: A 5-digit numeric field (1 integer, 4 decimal).
            *   **P-NEW-SSI-RATIO:**
                *   `PIC V9(04)`: A 4-digit numeric field (4 decimal).
            *   **P-NEW-MEDICAID-RATIO:**
                *   `PIC V9(04)`: A 4-digit numeric field (4 decimal).
            *   **P-NEW-PPS-BLEND-YR-IND:**
                *   `PIC 9(01)`: A 1-digit numeric field.
            *   **P-NEW-PRUF-UPDTE-FACTOR:**
                *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal).
            *   **P-NEW-DSH-PERCENT:**
                *   `PIC V9(04)`: A 4-digit numeric field (4 decimal).
            *   **P-NEW-FYE-DATE:**
                *   `PIC X(08)`: An 8-character alphanumeric field.
        *   **FILLER:**
            *   `PIC X(23)`: A 23-character alphanumeric filler.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
            *   **P-NEW-PASS-AMT-DIR-MED-ED:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
            *   **P-NEW-PASS-AMT-PLUS-MISC:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:**
                *   `PIC X`: A 1-character alphanumeric field.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
            *   **P-NEW-CAPI-OLD-HARM-RATE:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
            *   **P-NEW-CAPI-NEW-HARM-RATIO:**
                *   `PIC 9(01)V9999`: A 6-digit numeric field (1 integer, 4 decimal).
            *   **P-NEW-CAPI-CSTCHG-RATIO:**
                *   `PIC 9V999`: A 5-digit numeric field (3 decimal).
            *   **P-NEW-CAPI-NEW-HOSP:**
                *   `PIC X`: A 1-character alphanumeric field.
            *   **P-NEW-CAPI-IME:**
                *   `PIC 9V9999`: A 5-digit numeric field (4 decimal).
            *   **P-NEW-CAPI-EXCEPTIONS:**
                *   `PIC 9(04)V99`: A 6-digit numeric field (4 integer, 2 decimal).
        *   **FILLER:**
            *   `PIC X(22)`: A 22-character alphanumeric filler.
*   **WAGE-NEW-INDEX-RECORD:**  This is a group of fields representing the wage index data passed *to* the program.
    *   **W-MSA:**
        *   `PIC X(4)`: A 4-character alphanumeric field representing the MSA.
    *   **W-EFF-DATE:**
        *   `PIC X(8)`: An 8-character alphanumeric field representing the effective date.
    *   **W-WAGE-INDEX1:**
        *   `PIC S9(02)V9(04)`: A 6-digit signed numeric field (2 integer, 4 decimal) representing the wage index.
    *   **W-WAGE-INDEX2:**
        *   `PIC S9(02)V9(04)`: A 6-digit signed numeric field (2 integer, 4 decimal) representing the wage index.
    *   **W-WAGE-INDEX3:**
        *   `PIC S9(02)V9(04)`: A 6-digit signed numeric field (2 integer, 4 decimal) representing the wage index.

### LTCAL042

#### File Access Details

*   **COPY LTDRG031:** This is a COPYBOOK included in the program.

#### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF:**
    *   `PIC X(46)`:  A 46-character alphanumeric field containing the program's name and a description.
*   **CAL-VERSION:**
    *   `PIC X(05)`: A 5-character alphanumeric field storing the program's version.
*   **HOLD-PPS-COMPONENTS:** A group of fields used to store intermediate calculation results.
    *   **H-LOS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing Length of Stay.
    *   **H-REG-DAYS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing Regular Days.
    *   **H-TOTAL-DAYS:**
        *   `PIC 9(05)`: A 5-digit numeric field representing Total Days.
    *   **H-SSOT:**
        *   `PIC 9(02)`: A 2-digit numeric field.
    *   **H-BLEND-RTC:**
        *   `PIC 9(02)`: A 2-digit numeric field related to blending.
    *   **H-BLEND-FAC:**
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field (1 integer, 1 decimal) representing a facility blend factor.
    *   **H-BLEND-PPS:**
        *   `PIC 9(01)V9(01)`: A 2-digit numeric field (1 integer, 1 decimal) representing a PPS blend factor.
    *   **H-SS-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing Short Stay Payment Amount.
    *   **H-SS-COST:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing Short Stay Cost.
    *   **H-LABOR-PORTION:**
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field (7 integer, 6 decimal) representing the labor portion of a calculation.
    *   **H-NONLABOR-PORTION:**
        *   `PIC 9(07)V9(06)`: A 13-digit numeric field (7 integer, 6 decimal) representing the non-labor portion of a calculation.
    *   **H-FIXED-LOSS-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal) representing the fixed loss amount.
    *   **H-NEW-FAC-SPEC-RATE:**
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal).
    *   **H-LOS-RATIO:**
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal)
*   **PPS-NAT-LABOR-PCT:**
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal)
*   **PPS-NAT-NONLABOR-PCT:**
        *   `PIC 9(01)V9(05)`: A 6-digit numeric field (1 integer, 5 decimal)
*   **PPS-STD-FED-RATE:**
        *   `PIC 9(05)V9(02)`: A 7-digit numeric field (5 integer, 2 decimal)
*   **PPS-BDGT-NEUT-RATE:**
        *   `PIC 9(01)V9(03)`: A 4-digit numeric field (1 integer, 3 decimal)
*   **PPS-DRG-ADJ-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FED-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FINAL-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-FAC-COSTS:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-NEW-FAC-SPEC-RATE:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PPS-OUTLIER-PAY-AMT:**
        *   `PIC 9(07)V9(02)`: A 9-digit numeric field (7 integer, 2 decimal).
*   **PRICER-OPT-VERS-SW:**
    *   **PRICER-OPTION-SW:**
        *   `PIC X(01)`: A 1-character alphanumeric field indicating the pricer option.  Uses 88-levels for values 'A' (all tables passed) and 'P' (provider record passed).
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:**
            *   `PIC X(05)`:  A 5-character alphanumeric field representing the version of the PPDRV.

#### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA:**  This is a group of fields representing the bill data passed *to* the program.
    *   **B-NPI10:**
        *   **B-NPI8:**
            *   `PIC X(08)`:  An 8-character alphanumeric field representing part of the NPI.
        *   **B-NPI-FILLER:**
            *   `PIC X(02)`: A 2-character alphanumeric filler for the NPI.
    *   **B-PROVIDER-NO:**
        *   `PIC X(06)`: A 6-character alphanumeric field representing the provider number.
    *   **B-PATIENT-STATUS:**
        *   `PIC X(02)`: A 2-character alphanumeric field representing the patient status.
    *   **B-DRG-CODE:**
        *   `PIC X(03)`: A 3-character alphanumeric field representing the DRG code.
    *   **B-LOS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing the length of stay.
    *   **B-COV-DAYS:**
        *   `PIC 9(03)`: A 3-digit numeric field representing covered days.
    *   **B-LTR-DAYS:**
        *   `PIC 9(02)`: A 2-digit numeric field representing lifetime reserve days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:**
            *   `PIC 9(02)`: A 2-digit numeric field for the century/decade of the discharge date.
        *   **B-DISCHG-YY:**
            *   `PIC 9(02)`: A 2-digit numeric field for the year of the discharge date.
        *   **B-DISCHG-MM:**
            *   `PIC 9(02)`: A 2-digit numeric field for the month of the discharge date.
        *   **B-DISCHG-DD:**
            *   `PIC 9(02)`: A 2-digit numeric field for the day of the discharge date.
    *   **B-COV-CHARGES