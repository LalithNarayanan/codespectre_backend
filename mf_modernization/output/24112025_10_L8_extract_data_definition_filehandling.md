Here's an analysis of the provided COBOL programs, formatted as requested:

## Program: LTCAL032

### Files Accessed

*   **COPY LTDRG031:** This is a copybook, likely containing data structures related to DRG (Diagnosis Related Group) information.  It is included in the DATA DIVISION.

### Data Structures in WORKING-STORAGE SECTION

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.**
    *   Description:  A text field used for program identification or debugging, storing the program name and a description.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.**
    *   Description:  Stores the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS.**
    *   Description:  A group item used to store various components related to PPS (Prospective Payment System) calculations.
    *   **05 H-LOS PIC 9(03).**
        *   Description: Length of Stay (LOS), numeric, 3 digits.
    *   **05 H-REG-DAYS PIC 9(03).**
        *   Description: Regular days, numeric, 3 digits.
    *   **05 H-TOTAL-DAYS PIC 9(05).**
        *   Description: Total days, numeric, 5 digits.
    *   **05 H-SSOT PIC 9(02).**
        *   Description: Short Stay Outlier Threshold, numeric, 2 digits.
    *   **05 H-BLEND-RTC PIC 9(02).**
        *   Description: Blend Rate Type Code, numeric, 2 digits.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
        *   Description: Blend Facility Rate, numeric, 1 integer digit and 1 decimal digit.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
        *   Description: Blend PPS Rate, numeric, 1 integer digit and 1 decimal digit.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
        *   Description: Short Stay Payment Amount, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-SS-COST PIC 9(07)V9(02).**
        *   Description: Short Stay Cost, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Labor Portion of the payment, numeric, 7 integer digits and 6 decimal digits.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Non-Labor Portion of the payment, numeric, 7 integer digits and 6 decimal digits.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
        *   Description: Fixed Loss Amount, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
        *   Description: New Facility Specific Rate, numeric, 5 integer digits and 2 decimal digits.

### Data Structures in LINKAGE SECTION

*   **01 BILL-NEW-DATA.**
    *   Description:  This is the main input data structure, passed from the calling program, and contains billing information.
    *   **10 B-NPI10.**
        *   Description:  NPI (National Provider Identifier) data.
        *   **15 B-NPI8 PIC X(08).**
            *   Description:  NPI, alphanumeric, 8 characters.
        *   **15 B-NPI-FILLER PIC X(02).**
            *   Description:  Filler or separator for NPI, alphanumeric, 2 characters.
    *   **10 B-PROVIDER-NO PIC X(06).**
        *   Description:  Provider Number, alphanumeric, 6 characters.
    *   **10 B-PATIENT-STATUS PIC X(02).**
        *   Description:  Patient Status, alphanumeric, 2 characters.
    *   **10 B-DRG-CODE PIC X(03).**
        *   Description:  DRG Code, alphanumeric, 3 characters.
    *   **10 B-LOS PIC 9(03).**
        *   Description: Length of Stay (LOS), numeric, 3 digits.
    *   **10 B-COV-DAYS PIC 9(03).**
        *   Description: Covered Days, numeric, 3 digits.
    *   **10 B-LTR-DAYS PIC 9(02).**
        *   Description: Lifetime Reserve Days, numeric, 2 digits.
    *   **10 B-DISCHARGE-DATE.**
        *   Description:  Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).**
            *   Description:  Discharge Date - Century, numeric, 2 digits.
        *   **15 B-DISCHG-YY PIC 9(02).**
            *   Description:  Discharge Date - Year, numeric, 2 digits.
        *   **15 B-DISCHG-MM PIC 9(02).**
            *   Description:  Discharge Date - Month, numeric, 2 digits.
        *   **15 B-DISCHG-DD PIC 9(02).**
            *   Description:  Discharge Date - Day, numeric, 2 digits.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
        *   Description: Covered Charges, numeric, 7 integer digits and 2 decimal digits.
    *   **10 B-SPEC-PAY-IND PIC X(01).**
        *   Description: Special Payment Indicator, alphanumeric, 1 character.
    *   **10 FILLER PIC X(13).**
        *   Description: Unused filler space, alphanumeric, 13 characters.
*   **01 PPS-DATA-ALL.**
    *   Description:  This is the main output data structure, passed back to the calling program, and contains the PPS calculated data.
    *   **05 PPS-RTC PIC 9(02).**
        *   Description: PPS Return Code, numeric, 2 digits. Indicates the outcome of the calculation.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).**
        *   Description:  Charge Threshold for Outlier calculation, numeric, 7 integer digits and 2 decimal digits.
    *   **05 PPS-DATA.**
        *   Description:  PPS Data details.
        *   **10 PPS-MSA PIC X(04).**
            *   Description:  MSA (Metropolitan Statistical Area) code, alphanumeric, 4 characters.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).**
            *   Description:  Wage Index, numeric, 2 integer digits and 4 decimal digits.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).**
            *   Description:  Average Length of Stay, numeric, 2 integer digits and 1 decimal digit.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).**
            *   Description:  Relative Weight, numeric, 1 integer digit and 4 decimal digits.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).**
            *   Description:  Outlier Payment Amount, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-LOS PIC 9(03).**
            *   Description: Length of Stay, numeric, 3 digits.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).**
            *   Description:  DRG Adjusted Payment Amount, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Federal Payment Amount, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Final Payment Amount, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).**
            *   Description: Facility Costs, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).**
            *   Description: New Facility Specific Rate, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).**
            *   Description: Outlier Threshold, numeric, 7 integer digits and 2 decimal digits.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).**
            *   Description: Submitted DRG Code, alphanumeric, 3 characters.
        *   **10 PPS-CALC-VERS-CD PIC X(05).**
            *   Description: Calculation Version Code, alphanumeric, 5 characters.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).**
            *   Description: Regular Days Used, numeric, 3 digits.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).**
            *   Description: Lifetime Reserve Days Used, numeric, 3 digits.
        *   **10 PPS-BLEND-YEAR PIC 9(01).**
            *   Description: Blend Year, numeric, 1 digit.
        *   **10 PPS-COLA PIC 9(01)V9(03).**
            *   Description: COLA (Cost of Living Adjustment), numeric, 1 integer digit and 3 decimal digits.
        *   **10 FILLER PIC X(04).**
            *   Description: Unused filler space, alphanumeric, 4 characters.
    *   **05 PPS-OTHER-DATA.**
        *   Description:  Other PPS related Data.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Labor Percentage, numeric, 1 integer digit and 5 decimal digits.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Non-Labor Percentage, numeric, 1 integer digit and 5 decimal digits.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).**
            *   Description: Standard Federal Rate, numeric, 5 integer digits and 2 decimal digits.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).**
            *   Description: Budget Neutrality Rate, numeric, 1 integer digit and 3 decimal digits.
        *   **10 FILLER PIC X(20).**
            *   Description: Unused filler space, alphanumeric, 20 characters.
    *   **05 PPS-PC-DATA.**
        *   Description: PPS PC Data.
        *   **10 PPS-COT-IND PIC X(01).**
            *   Description: COT (Cost Outlier Threshold) Indicator, alphanumeric, 1 character.
        *   **10 FILLER PIC X(20).**
            *   Description: Unused filler space, alphanumeric, 20 characters.
*   **01 PRICER-OPT-VERS-SW.**
    *   Description:  Pricer Option Version Switch data.
    *   **05 PRICER-OPTION-SW PIC X(01).**
        *   Description: Pricer Option Switch, alphanumeric, 1 character.
        *   **88 ALL-TABLES-PASSED VALUE 'A'.**
            *   Description: Condition name indicating all tables passed, value 'A'.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.**
            *   Description: Condition name indicating provider record passed, value 'P'.
    *   **05 PPS-VERSIONS.**
        *   Description: PPS versions.
        *   **10 PPDRV-VERSION PIC X(05).**
            *   Description: PPDRV Version, alphanumeric, 5 characters.
*   **01 PROV-NEW-HOLD.**
    *   Description: Provider record data.
    *   **02 PROV-NEWREC-HOLD1.**
        *   Description: Provider record hold area 1.
        *   **05 P-NEW-NPI10.**
            *   Description:  New NPI data.
            *   **10 P-NEW-NPI8 PIC X(08).**
                *   Description: New NPI, alphanumeric, 8 characters.
            *   **10 P-NEW-NPI-FILLER PIC X(02).**
                *   Description: New NPI Filler, alphanumeric, 2 characters.
        *   **05 P-NEW-PROVIDER-NO.**
            *   Description: New Provider Number data.
            *   **10 P-NEW-STATE PIC 9(02).**
                *   Description: New State, numeric, 2 digits.
            *   **10 FILLER PIC X(04).**
                *   Description: Unused filler space, alphanumeric, 4 characters.
        *   **05 P-NEW-DATE-DATA.**
            *   Description: New Date data.
            *   **10 P-NEW-EFF-DATE.**
                *   Description: New Effective Date.
                *   **15 P-NEW-EFF-DT-CC PIC 9(02).**
                    *   Description: New Effective Date - Century, numeric, 2 digits.
                *   **15 P-NEW-EFF-DT-YY PIC 9(02).**
                    *   Description: New Effective Date - Year, numeric, 2 digits.
                *   **15 P-NEW-EFF-DT-MM PIC 9(02).**
                    *   Description: New Effective Date - Month, numeric, 2 digits.
                *   **15 P-NEW-EFF-DT-DD PIC 9(02).**
                    *   Description: New Effective Date - Day, numeric, 2 digits.
            *   **10 P-NEW-FY-BEGIN-DATE.**
                *   Description: New Fiscal Year Begin Date.
                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).**
                    *   Description: New Fiscal Year Begin Date - Century, numeric, 2 digits.
                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).**
                    *   Description: New Fiscal Year Begin Date - Year, numeric, 2 digits.
                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).**
                    *   Description: New Fiscal Year Begin Date - Month, numeric, 2 digits.
                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).**
                    *   Description: New Fiscal Year Begin Date - Day, numeric, 2 digits.
            *   **10 P-NEW-REPORT-DATE.**
                *   Description: New Report Date.
                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).**
                    *   Description: New Report Date - Century, numeric, 2 digits.
                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).**
                    *   Description: New Report Date - Year, numeric, 2 digits.
                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).**
                    *   Description: New Report Date - Month, numeric, 2 digits.
                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).**
                    *   Description: New Report Date - Day, numeric, 2 digits.
            *   **10 P-NEW-TERMINATION-DATE.**
                *   Description: New Termination Date.
                *   **15 P-NEW-TERM-DT-CC PIC 9(02).**
                    *   Description: New Termination Date - Century, numeric, 2 digits.
                *   **15 P-NEW-TERM-DT-YY PIC 9(02).**
                    *   Description: New Termination Date - Year, numeric, 2 digits.
                *   **15 P-NEW-TERM-DT-MM PIC 9(02).**
                    *   Description: New Termination Date - Month, numeric, 2 digits.
                *   **15 P-NEW-TERM-DT-DD PIC 9(02).**
                    *   Description: New Termination Date - Day, numeric, 2 digits.
        *   **05 P-NEW-WAIVER-CODE PIC X(01).**
            *   Description: New Waiver Code, alphanumeric, 1 character.
            *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.**
                *   Description: Condition name indicating waiver state, value 'Y'.
        *   **05 P-NEW-INTER-NO PIC 9(05).**
            *   Description: New Internal Number, numeric, 5 digits.
        *   **05 P-NEW-PROVIDER-TYPE PIC X(02).**
            *   Description: New Provider Type, alphanumeric, 2 characters.
        *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
            *   Description: New Current Census Division, numeric, 1 digit.
        *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
            *   Description: New Current Division Redefines New Current Census Division, numeric, 1 digit.
        *   **05 P-NEW-MSA-DATA.**
            *   Description: New MSA Data.
            *   **10 P-NEW-CHG-CODE-INDEX PIC X.**
                *   Description: New Charge Code Index, alphanumeric, 1 character.
            *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.**
                *   Description: New Geo Location MSA, alphanumeric, 4 characters, right justified.
            *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).**
                *   Description: New Geo Location MSA, numeric, 4 digits, redefines the alphanumeric field.
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.**
                *   Description: New Wage Index Location MSA, alphanumeric, 4 characters, right justified.
            *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.**
                *   Description: New Standard Amount Location MSA, alphanumeric, 4 characters, right justified.
            *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.**
                *   Description:  New Standard Amount Location MSA, redefines the alphanumeric field.
                *   **15 P-NEW-RURAL-1ST.**
                    *   Description: New Rural 1st.
                    *   **20 P-NEW-STAND-RURAL PIC XX.**
                        *   Description: New Standard Rural, alphanumeric, 2 characters.
                    *   **88 P-NEW-STD-RURAL-CHECK VALUE '  '.**
                        *   Description: Condition name indicating standard rural check, value '  '.
                *   **15 P-NEW-RURAL-2ND PIC XX.**
                    *   Description: New Rural 2nd, alphanumeric, 2 characters.
        *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.**
            *   Description: New Sol Com Dep Hosp Year, alphanumeric, 2 characters.
        *   **05 P-NEW-LUGAR PIC X.**
            *   Description: New Lugar, alphanumeric, 1 character.
        *   **05 P-NEW-TEMP-RELIEF-IND PIC X.**
            *   Description: New Temporary Relief Indicator, alphanumeric, 1 character.
        *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.**
            *   Description: New Federal PPS Blend Indicator, alphanumeric, 1 character.
        *   **05 FILLER PIC X(05).**
            *   Description: Unused filler space, alphanumeric, 5 characters.
    *   **02 PROV-NEWREC-HOLD2.**
        *   Description: Provider record hold area 2.
        *   **05 P-NEW-VARIABLES.**
            *   Description: New Variables.
            *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
                *   Description: New Facility Specific Rate, numeric, 5 integer digits and 2 decimal digits.
            *   **10 P-NEW-COLA PIC 9(01)V9(03).**
                *   Description: New COLA, numeric, 1 integer digit and 3 decimal digits.
            *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).**
                *   Description: New Intern Ratio, numeric, 1 integer digit and 4 decimal digits.
            *   **10 P-NEW-BED-SIZE PIC 9(05).**
                *   Description: New Bed Size, numeric, 5 digits.
            *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).**
                *   Description: New Operating Cost to Charge Ratio, numeric, 1 integer digit and 3 decimal digits.
            *   **10 P-NEW-CMI PIC 9(01)V9(04).**
                *   Description: New CMI, numeric, 1 integer digit and 4 decimal digits.
            *   **10 P-NEW-SSI-RATIO PIC V9(04).**
                *   Description: New SSI Ratio, numeric, 4 decimal digits.
            *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).**
                *   Description: New Medicaid Ratio, numeric, 4 decimal digits.
            *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).**
                *   Description: New PPS Blend Year Indicator, numeric, 1 digit.
            *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).**
                *   Description: New Pruf Update Factor, numeric, 1 integer digit and 5 decimal digits.
            *   **10 P-NEW-DSH-PERCENT PIC V9(04).**
                *   Description: New DSH Percent, numeric, 4 decimal digits.
            *   **10 P-NEW-FYE-DATE PIC X(08).**
                *   Description: New Fiscal Year End Date, alphanumeric, 8 characters.
        *   **05 FILLER PIC X(23).**
            *   Description: Unused filler space, alphanumeric, 23 characters.
    *   **02 PROV-NEWREC-HOLD3.**
        *   Description: Provider record hold area 3.
        *   **05 P-NEW-PASS-AMT-DATA.**
            *   Description: New Pass Amount Data.
            *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.**
                *   Description: New Pass Amount Capital, numeric, 4 integer digits and 2 decimal digits.
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.**
                *   Description: New Pass Amount Direct Medical Education, numeric, 4 integer digits and 2 decimal digits.
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.**
                *   Description: New Pass Amount Organ Acquisition, numeric, 4 integer digits and 2 decimal digits.
            *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.**
                *   Description: New Pass Amount Plus Misc, numeric, 4 integer digits and 2 decimal digits.
        *   **05 P-NEW-CAPI-DATA.**
            *   Description: New Capital Data.
            *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X.**
                *   Description: New Capital PPS Pay Code, alphanumeric, 1 character.
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.**
                *   Description: New Capital Hospital Specific Rate, numeric, 4 integer digits and 2 decimal digits.
            *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.**
                *   Description: New Capital Old Harm Rate, numeric, 4 integer digits and 2 decimal digits.
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.**
                *   Description: New Capital New Harm Ratio, numeric, 1 integer digit and 4 decimal digits.
            *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.**
                *   Description: New Capital Cost to Charge Ratio, numeric, 3 decimal digits.
            *   **15 P-NEW-CAPI-NEW-HOSP PIC X.**
                *   Description: New Capital New Hospital, alphanumeric, 1 character.
            *   **15 P-NEW-CAPI-IME PIC 9V9999.**
                *   Description: New Capital IME, numeric, 4 decimal digits.
            *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.**
                *   Description: New Capital Exceptions, numeric, 4 integer digits and 2 decimal digits.
        *   **05 FILLER PIC X(22).**
            *   Description: Unused filler space, alphanumeric, 22 characters.
*   **01 WAGE-NEW-INDEX-RECORD.**
    *   Description:  Wage Index Record
    *   **05 W-MSA PIC X(4).**
        *   Description: Wage MSA, alphanumeric, 4 characters.
    *   **05 W-EFF-DATE PIC X(8).**
        *   Description: Wage Effective Date, alphanumeric, 8 characters.
    *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04).**
        *   Description: Wage Index 1, signed numeric, 2 integer digits and 4 decimal digits.
    *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04).**
        *   Description: Wage Index 2, signed numeric, 2 integer digits and 4 decimal digits.
    *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04).**
        *   Description: Wage Index 3, signed numeric, 2 integer digits and 4 decimal digits.

## Program: LTCAL042

### Files Accessed

*   **COPY LTDRG031:** This is a copybook, likely containing data structures related to DRG (Diagnosis Related Group) information. It is included in the DATA DIVISION.

### Data Structures in WORKING-STORAGE SECTION

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.**
    *   Description: A text field used for program identification or debugging, storing the program name and a description.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.**
    *   Description: Stores the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS.**
    *   Description: A group item used to store various components related to PPS (Prospective Payment System) calculations.
    *   **05 H-LOS PIC 9(03).**
        *   Description: Length of Stay (LOS), numeric, 3 digits.
    *   **05 H-REG-DAYS PIC 9(03).**
        *   Description: Regular days, numeric, 3 digits.
    *   **05 H-TOTAL-DAYS PIC 9(05).**
        *   Description: Total days, numeric, 5 digits.
    *   **05 H-SSOT PIC 9(02).**
        *   Description: Short Stay Outlier Threshold, numeric, 2 digits.
    *   **05 H-BLEND-RTC PIC 9(02).**
        *   Description: Blend Rate Type Code, numeric, 2 digits.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
        *   Description: Blend Facility Rate, numeric, 1 integer digit and 1 decimal digit.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
        *   Description: Blend PPS Rate, numeric, 1 integer digit and 1 decimal digit.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
        *   Description: Short Stay Payment Amount, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-SS-COST PIC 9(07)V9(02).**
        *   Description: Short Stay Cost, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Labor Portion of the payment, numeric, 7 integer digits and 6 decimal digits.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Non-Labor Portion of the payment, numeric, 7 integer digits and 6 decimal digits.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
        *   Description: Fixed Loss Amount, numeric, 7 integer digits and 2 decimal digits.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
        *   Description: New Facility Specific Rate, numeric, 5 integer digits and 2 decimal digits.
    *   **05 H-LOS-RATIO PIC 9(01)V9(05).**
        *   Description: Length of Stay Ratio, numeric, 1 integer digit and 5 decimal digits.

### Data Structures in LINKAGE SECTION

*   **01 BILL-NEW-DATA.**
    *   Description:  This is the main input data structure, passed from the calling program, and contains billing information.
    *   **10 B-NPI10.**
        *   Description:  NPI (National Provider Identifier) data.
        *   **15 B-NPI8 PIC X(08).**
            *   Description:  NPI, alphanumeric, 8 characters.
        *   **15 B-NPI-FILLER PIC X(02).**
            *   Description:  Filler or separator for NPI, alphanumeric, 2 characters.
    *   **10 B-PROVIDER-NO PIC X(06).**
        *   Description:  Provider Number, alphanumeric, 6 characters.
    *   **10 B-PATIENT-STATUS PIC X(02).**
        *   Description:  Patient Status, alphanumeric, 2 characters.
    *   **10 B-DRG-CODE PIC X(03).**
        *   Description:  DRG Code, alphanumeric, 3 characters.
    *   **10 B-LOS PIC 9(03).**
        *   Description: Length of Stay (LOS), numeric, 3 digits.
    *   **10 B-COV-DAYS PIC 9(03).**
        *   Description: Covered Days, numeric, 3 digits.
    *   **10 B-LTR-DAYS PIC 9(02).**
        *   Description: Lifetime Reserve Days, numeric, 2 digits.
    *   **10 B-DISCHARGE-DATE.**
        *   Description:  Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).**
            *   Description:  Discharge Date - Century, numeric, 2 digits.
        *   **15 B-DISCHG-YY PIC 9(02).**
            *   Description:  Discharge Date - Year, numeric, 2 digits.
        *   **15 B-DISCHG-MM PIC 9(02).**
            *   Description:  Discharge Date - Month, numeric, 2 digits.
        *   **15 B-DISCHG-DD PIC 9(02).**
            *   Description:  Discharge Date - Day, numeric, 2 digits.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
        *   Description: Covered Charges, numeric, 7 integer digits and 2 decimal digits.
    *   **10 B-SPEC-PAY-IND PIC X(01).**
        *   Description: Special Payment Indicator, alphanumeric, 1 character.
    *   **10 FILLER PIC X(13).**
        *   Description: Unused filler space, alphanumeric, 13 characters.
*   **01 PPS-DATA-ALL.**
    *   Description:  This is the main output data structure, passed