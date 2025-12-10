## Analysis of the COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program *logically* accesses data through the `COPY` statement, which includes the data definitions from `LTDRG031`.

*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.`
        *   A descriptive field to identify the program and the section.
    *   `01 CAL-VERSION PIC X(05) VALUE 'C03.2'.`
        *   Stores the version of the calculation logic.
    *   `COPY LTDRG031.`
        *   Includes data structures (DRG related data) from the file named `LTDRG031`.
    *   `01 HOLD-PPS-COMPONENTS.`
        *   `05 H-LOS PIC 9(03).`
            *   Length of Stay, numeric, 3 digits.
        *   `05 H-REG-DAYS PIC 9(03).`
            *   Regular days, numeric, 3 digits.
        *   `05 H-TOTAL-DAYS PIC 9(05).`
            *   Total days, numeric, 5 digits.
        *   `05 H-SSOT PIC 9(02).`
            *   ? (Likely Short Stay Outlier Threshold), numeric, 2 digits.
        *   `05 H-BLEND-RTC PIC 9(02).`
            *   Blend rate code, numeric, 2 digits.
        *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
            *   Blend Facility percentage, numeric, 2 digits (1 integer, 1 decimal).
        *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
            *   Blend PPS percentage, numeric, 2 digits (1 integer, 1 decimal).
        *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
            *   Short Stay Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-SS-COST PIC 9(07)V9(02).`
            *   Short Stay Cost, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
            *   Labor portion, numeric, 13 digits (7 integer, 6 decimal).
        *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
            *   Non-labor portion, numeric, 13 digits (7 integer, 6 decimal).
        *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
            *   Fixed Loss Amount, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
            *   New Facility specific rate, numeric, 7 digits (5 integer, 2 decimal).

*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA.`
        *   `10 B-NPI10.`
            *   `15 B-NPI8 PIC X(08).`
                *   National Provider Identifier (NPI) - 8 digits.
            *   `15 B-NPI-FILLER PIC X(02).`
                *   Filler associated with NPI, 2 characters.
        *   `10 B-PROVIDER-NO PIC X(06).`
            *   Provider Number, 6 characters.
        *   `10 B-PATIENT-STATUS PIC X(02).`
            *   Patient Status, 2 characters.
        *   `10 B-DRG-CODE PIC X(03).`
            *   Diagnosis Related Group (DRG) Code, 3 characters.
        *   `10 B-LOS PIC 9(03).`
            *   Length of Stay, numeric, 3 digits.
        *   `10 B-COV-DAYS PIC 9(03).`
            *   Covered Days, numeric, 3 digits.
        *   `10 B-LTR-DAYS PIC 9(02).`
            *   Lifetime Reserve Days, numeric, 2 digits.
        *   `10 B-DISCHARGE-DATE.`
            *   `15 B-DISCHG-CC PIC 9(02).`
                *   Discharge Date - Century, numeric, 2 digits.
            *   `15 B-DISCHG-YY PIC 9(02).`
                *   Discharge Date - Year, numeric, 2 digits.
            *   `15 B-DISCHG-MM PIC 9(02).`
                *   Discharge Date - Month, numeric, 2 digits.
            *   `15 B-DISCHG-DD PIC 9(02).`
                *   Discharge Date - Day, numeric, 2 digits.
        *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
            *   Covered Charges, numeric, 9 digits (7 integer, 2 decimal).
        *   `10 B-SPEC-PAY-IND PIC X(01).`
            *   Special Payment Indicator, 1 character.
        *   `10 FILLER PIC X(13).`
            *   Filler, 13 characters.
    *   `01 PPS-DATA-ALL.`
        *   `05 PPS-RTC PIC 9(02).`
            *   PPS Return Code, numeric, 2 digits.
        *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
            *   PPS Charge Threshold, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 PPS-DATA.`
            *   `10 PPS-MSA PIC X(04).`
                *   Metropolitan Statistical Area (MSA), 4 characters.
            *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
                *   PPS Wage Index, numeric, 6 digits (2 integer, 4 decimal).
            *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
                *   PPS Average Length of Stay, numeric, 3 digits (2 integer, 1 decimal).
            *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
                *   PPS Relative Weight, numeric, 5 digits (1 integer, 4 decimal).
            *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Outlier Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-LOS PIC 9(03).`
                *   PPS Length of Stay, numeric, 3 digits.
            *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
                *   PPS DRG Adjusted Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Federal Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Final Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
                *   PPS Facility Costs, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
                *   PPS New Facility Specific Rate, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
                *   PPS Outlier Threshold, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
                *   Submitted DRG Code, 3 characters.
            *   `10 PPS-CALC-VERS-CD PIC X(05).`
                *   PPS Calculation Version Code, 5 characters.
            *   `10 PPS-REG-DAYS-USED PIC 9(03).`
                *   PPS Regular Days Used, numeric, 3 digits.
            *   `10 PPS-LTR-DAYS-USED PIC 9(03).`
                *   PPS Lifetime Reserve Days Used, numeric, 3 digits.
            *   `10 PPS-BLEND-YEAR PIC 9(01).`
                *   PPS Blend Year, numeric, 1 digit.
            *   `10 PPS-COLA PIC 9(01)V9(03).`
                *   PPS COLA, numeric, 4 digits (1 integer, 3 decimal).
            *   `10 FILLER PIC X(04).`
                *   Filler, 4 characters.
        *   `05 PPS-OTHER-DATA.`
            *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).`
                *   PPS National Labor Percentage, numeric, 6 digits (1 integer, 5 decimal).
            *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).`
                *   PPS National Non-Labor Percentage, numeric, 6 digits (1 integer, 5 decimal).
            *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02).`
                *   PPS Standard Federal Rate, numeric, 7 digits (5 integer, 2 decimal).
            *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).`
                *   PPS Budget Neutrality Rate, numeric, 4 digits (1 integer, 3 decimal).
            *   `10 FILLER PIC X(20).`
                *   Filler, 20 characters.
        *   `05 PPS-PC-DATA.`
            *   `10 PPS-COT-IND PIC X(01).`
                *   PPS Cost Outlier Indicator, 1 character.
            *   `10 FILLER PIC X(20).`
                *   Filler, 20 characters.
    *   `01 PRICER-OPT-VERS-SW.`
        *   `05 PRICER-OPTION-SW PIC X(01).`
            *   Pricer Option Switch, 1 character.
                *   `88 ALL-TABLES-PASSED VALUE 'A'.`
                    *   Condition: All tables passed.
                *   `88 PROV-RECORD-PASSED VALUE 'P'.`
                    *   Condition: Provider record passed.
        *   `05 PPS-VERSIONS.`
            *   `10 PPDRV-VERSION PIC X(05).`
                *   PPDRV Version, 5 characters.
    *   `01 PROV-NEW-HOLD.`
        *   `02 PROV-NEWREC-HOLD1.`
            *   `05 P-NEW-NPI10.`
                *   `10 P-NEW-NPI8 PIC X(08).`
                    *   New NPI - 8 characters.
                *   `10 P-NEW-NPI-FILLER PIC X(02).`
                    *   New NPI Filler - 2 characters.
            *   `05 P-NEW-PROVIDER-NO.`
                *   `10 P-NEW-STATE PIC 9(02).`
                    *   New Provider State, numeric, 2 digits.
                *   `10 FILLER PIC X(04).`
                    *   Filler, 4 characters.
            *   `05 P-NEW-DATE-DATA.`
                *   `10 P-NEW-EFF-DATE.`
                    *   `15 P-NEW-EFF-DT-CC PIC 9(02).`
                        *   New Effective Date - Century, numeric, 2 digits.
                    *   `15 P-NEW-EFF-DT-YY PIC 9(02).`
                        *   New Effective Date - Year, numeric, 2 digits.
                    *   `15 P-NEW-EFF-DT-MM PIC 9(02).`
                        *   New Effective Date - Month, numeric, 2 digits.
                    *   `15 P-NEW-EFF-DT-DD PIC 9(02).`
                        *   New Effective Date - Day, numeric, 2 digits.
                *   `10 P-NEW-FY-BEGIN-DATE.`
                    *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02).`
                        *   New Fiscal Year Begin Date - Century, numeric, 2 digits.
                    *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02).`
                        *   New Fiscal Year Begin Date - Year, numeric, 2 digits.
                    *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02).`
                        *   New Fiscal Year Begin Date - Month, numeric, 2 digits.
                    *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02).`
                        *   New Fiscal Year Begin Date - Day, numeric, 2 digits.
                *   `10 P-NEW-REPORT-DATE.`
                    *   `15 P-NEW-REPORT-DT-CC PIC 9(02).`
                        *   New Report Date - Century, numeric, 2 digits.
                    *   `15 P-NEW-REPORT-DT-YY PIC 9(02).`
                        *   New Report Date - Year, numeric, 2 digits.
                    *   `15 P-NEW-REPORT-DT-MM PIC 9(02).`
                        *   New Report Date - Month, numeric, 2 digits.
                    *   `15 P-NEW-REPORT-DT-DD PIC 9(02).`
                        *   New Report Date - Day, numeric, 2 digits.
                *   `10 P-NEW-TERMINATION-DATE.`
                    *   `15 P-NEW-TERM-DT-CC PIC 9(02).`
                        *   New Termination Date - Century, numeric, 2 digits.
                    *   `15 P-NEW-TERM-DT-YY PIC 9(02).`
                        *   New Termination Date - Year, numeric, 2 digits.
                    *   `15 P-NEW-TERM-DT-MM PIC 9(02).`
                        *   New Termination Date - Month, numeric, 2 digits.
                    *   `15 P-NEW-TERM-DT-DD PIC 9(02).`
                        *   New Termination Date - Day, numeric, 2 digits.
            *   `05 P-NEW-WAIVER-CODE PIC X(01).`
                *   New Waiver Code, 1 character.
                    *   `88 P-NEW-WAIVER-STATE VALUE 'Y'.`
                        *   Condition: Waiver State is 'Y'.
            *   `05 P-NEW-INTER-NO PIC 9(05).`
                *   New Internal Number, numeric, 5 digits.
            *   `05 P-NEW-PROVIDER-TYPE PIC X(02).`
                *   New Provider Type, 2 characters.
            *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
                *   New Current Census Division, numeric, 1 digit.
            *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
                *   New Current Division, redefines New Current Census Division, numeric, 1 digit.
            *   `05 P-NEW-MSA-DATA.`
                *   `10 P-NEW-CHG-CODE-INDEX PIC X.`
                    *   New Charge Code Index, 1 character.
                *   `10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.`
                    *   New Geo Location MSA X, 4 characters, right justified.
                *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).`
                    *   New Geo Location MSA 9, redefines New Geo Location MSA X, numeric, 4 digits.
                *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.`
                    *   New Wage Index Location MSA, 4 characters, right justified.
                *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.`
                    *   New Standard Amount Location MSA, 4 characters, right justified.
                *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.`
                    *   `15 P-NEW-RURAL-1ST.`
                        *   `20 P-NEW-STAND-RURAL PIC XX.`
                            *   New Standard Rural, 2 characters.
                                *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '.`
                                    *   Condition: New Standard Rural Check is spaces.
                        *   `15 P-NEW-RURAL-2ND PIC XX.`
                            *   New Rural 2nd, 2 characters.
            *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.`
                *   New Sol Com Dep Hosp Year, 2 characters.
            *   `05 P-NEW-LUGAR PIC X.`
                *   New Lugar, 1 character.
            *   `05 P-NEW-TEMP-RELIEF-IND PIC X.`
                *   New Temp Relief Indicator, 1 character.
            *   `05 P-NEW-FED-PPS-BLEND-IND PIC X.`
                *   New Federal PPS Blend Indicator, 1 character.
            *   `05 FILLER PIC X(05).`
                *   Filler, 5 characters.
        *   `02 PROV-NEWREC-HOLD2.`
            *   `05 P-NEW-VARIABLES.`
                *   `10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
                    *   New Facility Specific Rate, numeric, 7 digits (5 integer, 2 decimal).
                *   `10 P-NEW-COLA PIC 9(01)V9(03).`
                    *   New COLA, numeric, 4 digits (1 integer, 3 decimal).
                *   `10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).`
                    *   New Intern Ratio, numeric, 5 digits (1 integer, 4 decimal).
                *   `10 P-NEW-BED-SIZE PIC 9(05).`
                    *   New Bed Size, numeric, 5 digits.
                *   `10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).`
                    *   New Operating Cost to Charge Ratio, numeric, 4 digits (1 integer, 3 decimal).
                *   `10 P-NEW-CMI PIC 9(01)V9(04).`
                    *   New CMI, numeric, 5 digits (1 integer, 4 decimal).
                *   `10 P-NEW-SSI-RATIO PIC V9(04).`
                    *   New SSI Ratio, numeric, 4 digits (4 decimal).
                *   `10 P-NEW-MEDICAID-RATIO PIC V9(04).`
                    *   New Medicaid Ratio, numeric, 4 digits (4 decimal).
                *   `10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).`
                    *   New PPS Blend Year Indicator, numeric, 1 digit.
                *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).`
                    *   New Pruf Update Factor, numeric, 6 digits (1 integer, 5 decimal).
                *   `10 P-NEW-DSH-PERCENT PIC V9(04).`
                    *   New DSH Percent, numeric, 4 digits (4 decimal).
                *   `10 P-NEW-FYE-DATE PIC X(08).`
                    *   New FYE Date, 8 characters.
            *   `05 FILLER PIC X(23).`
                *   Filler, 23 characters.
        *   `02 PROV-NEWREC-HOLD3.`
            *   `05 P-NEW-PASS-AMT-DATA.`
                *   `10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.`
                    *   New Pass Amount Capital, numeric, 6 digits (4 integer, 2 decimal).
                *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.`
                    *   New Pass Amount Direct Medical Education, numeric, 6 digits (4 integer, 2 decimal).
                *   `10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.`
                    *   New Pass Amount Organ Acquisition, numeric, 6 digits (4 integer, 2 decimal).
                *   `10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.`
                    *   New Pass Amount Plus Misc, numeric, 6 digits (4 integer, 2 decimal).
            *   `05 P-NEW-CAPI-DATA.`
                *   `15 P-NEW-CAPI-PPS-PAY-CODE PIC X.`
                    *   New CAPI PPS Pay Code, 1 character.
                *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.`
                    *   New CAPI Hospital Specific Rate, numeric, 6 digits (4 integer, 2 decimal).
                *   `15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.`
                    *   New CAPI Old Harm Rate, numeric, 6 digits (4 integer, 2 decimal).
                *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.`
                    *   New CAPI New Harm Ratio, numeric, 5 digits (1 integer, 4 decimal).
                *   `15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.`
                    *   New CAPI Cost to Charge Ratio, numeric, 4 digits (3 decimal).
                *   `15 P-NEW-CAPI-NEW-HOSP PIC X.`
                    *   New CAPI New Hospital, 1 character.
                *   `15 P-NEW-CAPI-IME PIC 9V9999.`
                    *   New CAPI IME, numeric, 5 digits (4 decimal).
                *   `15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.`
                    *   New CAPI Exceptions, numeric, 6 digits (4 integer, 2 decimal).
            *   `05 FILLER PIC X(22).`
                *   Filler, 22 characters.
    *   `01 WAGE-NEW-INDEX-RECORD.`
        *   `05 W-MSA PIC X(4).`
            *   Wage MSA, 4 characters.
        *   `05 W-EFF-DATE PIC X(8).`
            *   Wage Effective Date, 8 characters.
        *   `05 W-WAGE-INDEX1 PIC S9(02)V9(04).`
            *   Wage Index 1, signed numeric, 6 digits (2 integer, 4 decimal).
        *   `05 W-WAGE-INDEX2 PIC S9(02)V9(04).`
            *   Wage Index 2, signed numeric, 6 digits (2 integer, 4 decimal).
        *   `05 W-WAGE-INDEX3 PIC S9(02)V9(04).`
            *   Wage Index 3, signed numeric, 6 digits (2 integer, 4 decimal).

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (like `SELECT` statements) are present in the provided code. However, the program *logically* accesses data through the `COPY` statement, which includes the data definitions from `LTDRG031`.

*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.`
        *   A descriptive field to identify the program and the section.
    *   `01 CAL-VERSION PIC X(05) VALUE 'C04.2'.`
        *   Stores the version of the calculation logic.
    *   `COPY LTDRG031.`
        *   Includes data structures (DRG related data) from the file named `LTDRG031`.
    *   `01 HOLD-PPS-COMPONENTS.`
        *   `05 H-LOS PIC 9(03).`
            *   Length of Stay, numeric, 3 digits.
        *   `05 H-REG-DAYS PIC 9(03).`
            *   Regular days, numeric, 3 digits.
        *   `05 H-TOTAL-DAYS PIC 9(05).`
            *   Total days, numeric, 5 digits.
        *   `05 H-SSOT PIC 9(02).`
            *   ? (Likely Short Stay Outlier Threshold), numeric, 2 digits.
        *   `05 H-BLEND-RTC PIC 9(02).`
            *   Blend rate code, numeric, 2 digits.
        *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
            *   Blend Facility percentage, numeric, 2 digits (1 integer, 1 decimal).
        *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
            *   Blend PPS percentage, numeric, 2 digits (1 integer, 1 decimal).
        *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
            *   Short Stay Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-SS-COST PIC 9(07)V9(02).`
            *   Short Stay Cost, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
            *   Labor portion, numeric, 13 digits (7 integer, 6 decimal).
        *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
            *   Non-labor portion, numeric, 13 digits (7 integer, 6 decimal).
        *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
            *   Fixed Loss Amount, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
            *   New Facility specific rate, numeric, 7 digits (5 integer, 2 decimal).
        *   `05 H-LOS-RATIO PIC 9(01)V9(05).`
            *   Length of Stay Ratio, numeric, 6 digits (1 integer, 5 decimal).

*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA.`
        *   `10 B-NPI10.`
            *   `15 B-NPI8 PIC X(08).`
                *   National Provider Identifier (NPI) - 8 digits.
            *   `15 B-NPI-FILLER PIC X(02).`
                *   Filler associated with NPI, 2 characters.
        *   `10 B-PROVIDER-NO PIC X(06).`
            *   Provider Number, 6 characters.
        *   `10 B-PATIENT-STATUS PIC X(02).`
            *   Patient Status, 2 characters.
        *   `10 B-DRG-CODE PIC X(03).`
            *   Diagnosis Related Group (DRG) Code, 3 characters.
        *   `10 B-LOS PIC 9(03).`
            *   Length of Stay, numeric, 3 digits.
        *   `10 B-COV-DAYS PIC 9(03).`
            *   Covered Days, numeric, 3 digits.
        *   `10 B-LTR-DAYS PIC 9(02).`
            *   Lifetime Reserve Days, numeric, 2 digits.
        *   `10 B-DISCHARGE-DATE.`
            *   `15 B-DISCHG-CC PIC 9(02).`
                *   Discharge Date - Century, numeric, 2 digits.
            *   `15 B-DISCHG-YY PIC 9(02).`
                *   Discharge Date - Year, numeric, 2 digits.
            *   `15 B-DISCHG-MM PIC 9(02).`
                *   Discharge Date - Month, numeric, 2 digits.
            *   `15 B-DISCHG-DD PIC 9(02).`
                *   Discharge Date - Day, numeric, 2 digits.
        *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
            *   Covered Charges, numeric, 9 digits (7 integer, 2 decimal).
        *   `10 B-SPEC-PAY-IND PIC X(01).`
            *   Special Payment Indicator, 1 character.
        *   `10 FILLER PIC X(13).`
            *   Filler, 13 characters.
    *   `01 PPS-DATA-ALL.`
        *   `05 PPS-RTC PIC 9(02).`
            *   PPS Return Code, numeric, 2 digits.
        *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
            *   PPS Charge Threshold, numeric, 9 digits (7 integer, 2 decimal).
        *   `05 PPS-DATA.`
            *   `10 PPS-MSA PIC X(04).`
                *   Metropolitan Statistical Area (MSA), 4 characters.
            *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
                *   PPS Wage Index, numeric, 6 digits (2 integer, 4 decimal).
            *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
                *   PPS Average Length of Stay, numeric, 3 digits (2 integer, 1 decimal).
            *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
                *   PPS Relative Weight, numeric, 5 digits (1 integer, 4 decimal).
            *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Outlier Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-LOS PIC 9(03).`
                *   PPS Length of Stay, numeric, 3 digits.
            *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
                *   PPS DRG Adjusted Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Federal Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
                *   PPS Final Payment Amount, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
                *   PPS Facility Costs, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
                *   PPS New Facility Specific Rate, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
                *   PPS Outlier Threshold, numeric, 9 digits (7 integer, 2 decimal).
            *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
                *   Submitted DRG Code, 3 characters.
            *   `10 PPS-CALC-VERS-CD PIC X(05).`
                *   PPS Calculation Version Code, 5 characters.
            *   `10 PPS-