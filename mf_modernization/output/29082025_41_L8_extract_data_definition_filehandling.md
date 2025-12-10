Here's an analysis of the provided COBOL programs:

## Program: LTCAL032

**1. Files Accessed:**

*   **COPY LTDRG031.:** This is a copybook, which is included in the program during compilation.  It likely contains data structures (tables) used for DRG (Diagnosis Related Group) calculations, specific to the 2003 fiscal year.  This copybook is critical for the program's core functionality.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.**  - A descriptive string, likely used for debugging or identification of the program's working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.** -  A version identifier for the calculation logic, indicating version C03.2.
*   **01 HOLD-PPS-COMPONENTS.** - This structure is defined in the copybook `LTDRG031` and is used to store intermediate values and components used in the PPS (Prospective Payment System) calculations.
    *   **05 H-LOS PIC 9(03).** - Length of Stay (LOS), a three-digit numeric field.
    *   **05 H-REG-DAYS PIC 9(03).** - Regular Days, a three-digit numeric field.
    *   **05 H-TOTAL-DAYS PIC 9(05).** - Total Days, a five-digit numeric field.
    *   **05 H-SSOT PIC 9(02).** - Short Stay Outlier Threshold, a two-digit numeric field.
    *   **05 H-BLEND-RTC PIC 9(02).** - Blend Return Code, a two-digit numeric field.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).** - Blend Facility Percentage, a two-digit numeric field with one decimal place (e.g., 0.8).
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).** - Blend PPS Percentage, a two-digit numeric field with one decimal place.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).** - Short Stay Payment Amount, a nine-digit numeric field with two decimal places.
    *   **05 H-SS-COST PIC 9(07)V9(02).** - Short Stay Cost, a nine-digit numeric field with two decimal places.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).** - Labor Portion, a thirteen-digit numeric field with six decimal places.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).** - Non-Labor Portion, a thirteen-digit numeric field with six decimal places.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).** - Fixed Loss Amount, a nine-digit numeric field with two decimal places.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - New Facility Specific Rate, a seven-digit numeric field with two decimal places.
*   The `LTDRG031` copybook is included to define  the `HOLD-PPS-COMPONENTS` structure and likely contains other data used for DRG calculations.

**3. Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.** - This structure represents the input data passed *to* the program from the calling program (likely a claims processing system).  It contains information about the medical bill.
    *   **10 B-NPI10.** - National Provider Identifier (NPI)
        *   **15 B-NPI8 PIC X(08).** - First 8 digits of the NPI.
        *   **15 B-NPI-FILLER PIC X(02).** - Filler, likely used to separate parts of the NPI.
    *   **10 B-PROVIDER-NO PIC X(06).** - Provider Number, a six-character field.
    *   **10 B-PATIENT-STATUS PIC X(02).** - Patient Status, a two-character field.
    *   **10 B-DRG-CODE PIC X(03).** - DRG Code, a three-character field.
    *   **10 B-LOS PIC 9(03).** - Length of Stay, a three-digit numeric field.
    *   **10 B-COV-DAYS PIC 9(03).** - Covered Days, a three-digit numeric field.
    *   **10 B-LTR-DAYS PIC 9(02).** - Lifetime Reserve Days, a two-digit numeric field.
    *   **10 B-DISCHARGE-DATE.** - Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).** - Century and Decade of Discharge Date
        *   **15 B-DISCHG-YY PIC 9(02).** - Year of Discharge Date.
        *   **15 B-DISCHG-MM PIC 9(02).** - Month of Discharge Date.
        *   **15 B-DISCHG-DD PIC 9(02).** - Day of Discharge Date.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).** - Covered Charges, a nine-digit numeric field with two decimal places.
    *   **10 B-SPEC-PAY-IND PIC X(01).** - Special Payment Indicator, a one-character field.
    *   **10 FILLER PIC X(13).** - Unused field, 13 characters
*   **01 PPS-DATA-ALL.** - This structure is passed *back* to the calling program and contains the calculated PPS data.  It's the output of the program.
    *   **05 PPS-RTC PIC 9(02).** - Return Code, a two-digit numeric field, indicating the outcome of the pricing process.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).** - Charge Threshold, a nine-digit numeric field with two decimal places.
    *   **05 PPS-DATA.** - PPS Data.
        *   **10 PPS-MSA PIC X(04).** - Metropolitan Statistical Area (MSA) Code, a four-character field.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).** - Wage Index, a six-digit numeric field with four decimal places.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).** - Average Length of Stay, a three-digit numeric field with one decimal place.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).** - Relative Weight, a five-digit numeric field with four decimal places.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).** - Outlier Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-LOS PIC 9(03).** - Length of Stay, a three-digit numeric field.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).** - DRG Adjusted Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).** - Federal Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).** - Final Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).** - Facility Costs, a nine-digit numeric field with two decimal places.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).** - New Facility Specific Rate, a nine-digit numeric field with two decimal places.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).** - Outlier Threshold, a nine-digit numeric field with two decimal places.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).** - Submitted DRG Code, a three-character field.
        *   **10 PPS-CALC-VERS-CD PIC X(05).** - Calculation Version Code, a five-character field.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).** - Regular Days Used, a three-digit numeric field.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).** - Lifetime Reserve Days Used, a three-digit numeric field.
        *   **10 PPS-BLEND-YEAR PIC 9(01).** - Blend Year, a one-digit numeric field.
        *   **10 PPS-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment, a four-digit numeric field with three decimal places.
        *   **10 FILLER PIC X(04).** - Filler, four characters
    *   **05 PPS-OTHER-DATA.** - Other PPS Data.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).** - National Labor Percentage, a six-digit numeric field with five decimal places.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).** - National Non-Labor Percentage, a six-digit numeric field with five decimal places.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).** - Standard Federal Rate, a seven-digit numeric field with two decimal places.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).** - Budget Neutrality Rate, a four-digit numeric field with three decimal places.
        *   **10 FILLER PIC X(20).** - Filler, 20 characters
    *   **05 PPS-PC-DATA.** - PPS PC Data
        *   **10 PPS-COT-IND PIC X(01).** - Cost Outlier Indicator, a one-character field.
        *   **10 FILLER PIC X(20).** - Filler, 20 characters
*   **01 PRICER-OPT-VERS-SW.** -  Pricer Option and Version Switch. This structure controls how the program behaves, likely related to which tables or data sources are used.
    *   **05 PRICER-OPTION-SW PIC X(01).** - Pricer Option Switch, a one-character field.
        *   **88 ALL-TABLES-PASSED VALUE 'A'.** - Condition: All tables passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.** - Condition: Provider record passed.
    *   **05 PPS-VERSIONS.** - PPS Versions.
        *   **10 PPDRV-VERSION PIC X(05).** - PPDRV Version, a five-character field.
*   **01 PROV-NEW-HOLD.** - Provider Record Hold. This structure contains detailed information about the healthcare provider.
    *   **02 PROV-NEWREC-HOLD1.** - Provider Record Hold 1
        *   **05 P-NEW-NPI10.** - New NPI
            *   **10 P-NEW-NPI8 PIC X(08).** - NPI (first 8 characters)
            *   **10 P-NEW-NPI-FILLER PIC X(02).** - NPI Filler
        *   **05 P-NEW-PROVIDER-NO.** - New Provider Number
            *   **10 P-NEW-STATE PIC 9(02).** - New State
            *   **10 FILLER PIC X(04).** - Filler
        *   **05 P-NEW-DATE-DATA.** - New Date Data
            *   **10 P-NEW-EFF-DATE.** - New Effective Date
                *   **15 P-NEW-EFF-DT-CC PIC 9(02).** - New Effective Date Century and Decade
                *   **15 P-NEW-EFF-DT-YY PIC 9(02).** - New Effective Date Year
                *   **15 P-NEW-EFF-DT-MM PIC 9(02).** - New Effective Date Month
                *   **15 P-NEW-EFF-DT-DD PIC 9(02).** - New Effective Date Day
            *   **10 P-NEW-FY-BEGIN-DATE.** - New Fiscal Year Begin Date
                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).** - New Fiscal Year Begin Date Century and Decade
                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).** - New Fiscal Year Begin Date Year
                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).** - New Fiscal Year Begin Date Month
                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).** - New Fiscal Year Begin Date Day
            *   **10 P-NEW-REPORT-DATE.** - New Report Date
                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).** - New Report Date Century and Decade
                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).** - New Report Date Year
                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).** - New Report Date Month
                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).** - New Report Date Day
            *   **10 P-NEW-TERMINATION-DATE.** - New Termination Date
                *   **15 P-NEW-TERM-DT-CC PIC 9(02).** - New Termination Date Century and Decade
                *   **15 P-NEW-TERM-DT-YY PIC 9(02).** - New Termination Date Year
                *   **15 P-NEW-TERM-DT-MM PIC 9(02).** - New Termination Date Month
                *   **15 P-NEW-TERM-DT-DD PIC 9(02).** - New Termination Date Day
        *   **05 P-NEW-WAIVER-CODE PIC X(01).** - New Waiver Code
            *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.** - Condition:  Waiver State is 'Y'.
        *   **05 P-NEW-INTER-NO PIC 9(05).** - New Internal Number
        *   **05 P-NEW-PROVIDER-TYPE PIC X(02).** - New Provider Type
        *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).** - New Current Census Division
        *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).** - Redefines the previous field.
        *   **05 P-NEW-MSA-DATA.** - New MSA Data
            *   **10 P-NEW-CHG-CODE-INDEX PIC X.** - New Charge Code Index
            *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.** - New Geographic Location MSA X
            *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).** - Redefines the previous field.
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.** - New Wage Index Location MSA
            *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.** - New Standard Amount Location MSA
            *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.** - New Standard Amount Location MSA 9
                *   **15 P-NEW-RURAL-1ST.** - New Rural 1st
                    *   **20 P-NEW-STAND-RURAL PIC XX.** - New Standard Rural
                        *   **88 P-NEW-STD-RURAL-CHECK VALUE '  '.** - Condition: Standard Rural Check
                    *   **15 P-NEW-RURAL-2ND PIC XX.** - New Rural 2nd
        *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.** - New Sol Com Dep Hosp Yr
        *   **05 P-NEW-LUGAR PIC X.** - New Lugar
        *   **05 P-NEW-TEMP-RELIEF-IND PIC X.** - New Temp Relief Ind
        *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.** - New Fed Pps Blend Ind
        *   **05 FILLER PIC X(05).** - Filler
    *   **02 PROV-NEWREC-HOLD2.** - Provider Record Hold 2
        *   **05 P-NEW-VARIABLES.** - New Variables
            *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - New Facility Specific Rate
            *   **10 P-NEW-COLA PIC 9(01)V9(03).** - New COLA
            *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).** - New Intern Ratio
            *   **10 P-NEW-BED-SIZE PIC 9(05).** - New Bed Size
            *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).** - New Operating Cost Charge Ratio
            *   **10 P-NEW-CMI PIC 9(01)V9(04).** - New CMI
            *   **10 P-NEW-SSI-RATIO PIC V9(04).** - New SSI Ratio
            *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).** - New Medicaid Ratio
            *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).** - New PPS Blend Year Indicator
            *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).** - New PRUF Update Factor
            *   **10 P-NEW-DSH-PERCENT PIC V9(04).** - New DSH Percent
            *   **10 P-NEW-FYE-DATE PIC X(08).** - New FYE Date
        *   **05 FILLER PIC X(23).** - Filler
    *   **02 PROV-NEWREC-HOLD3.** - Provider Record Hold 3
        *   **05 P-NEW-PASS-AMT-DATA.** - New Pass Amount Data
            *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.** - New Pass Amount Capital
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.** - New Pass Amount Direct Med Ed
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.** - New Pass Amount Organ Acq
            *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.** - New Pass Amount Plus Misc
        *   **05 P-NEW-CAPI-DATA.** - New Capi Data
            *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X.** - New Capi PPS Pay Code
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.** - New Capi Hosp Spec Rate
            *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.** - New Capi Old Harm Rate
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.** - New Capi New Harm Ratio
            *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.** - New Capi Cost Charge Ratio
            *   **15 P-NEW-CAPI-NEW-HOSP PIC X.** - New Capi New Hosp
            *   **15 P-NEW-CAPI-IME PIC 9V9999.** - New Capi IME
            *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.** - New Capi Exceptions
        *   **05 FILLER PIC X(22).** - Filler
*   **01 WAGE-NEW-INDEX-RECORD.** - Wage Index Record. This structure contains the wage index information for the MSA.
    *   **05 W-MSA PIC X(4).** - MSA Code, a four-character field.
    *   **05 W-EFF-DATE PIC X(8).** - Effective Date, an eight-character field.
    *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04).** - Wage Index 1, a six-digit signed numeric field with four decimal places.
    *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04).** - Wage Index 2, a six-digit signed numeric field with four decimal places.
    *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04).** - Wage Index 3, a six-digit signed numeric field with four decimal places.

**Summary of Program LTCAL032:**

This program appears to be a core module for calculating payments for long-term care (LTC) facilities using the PPS (Prospective Payment System) methodology. It takes bill data, provider information, and wage index data as input and produces a calculated payment amount and return code. It uses various data structures to store intermediate results and final payment information.  It heavily relies on the `LTDRG031` copybook for DRG-related data.

## Program: LTCAL042

**1. Files Accessed:**

*   **COPY LTDRG031.:** This is a copybook, which is included in the program during compilation.  It likely contains data structures (tables) used for DRG (Diagnosis Related Group) calculations, specific to the 2003 fiscal year.  This copybook is critical for the program's core functionality.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.**  - A descriptive string, likely used for debugging or identification of the program's working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.** -  A version identifier for the calculation logic, indicating version C04.2.
*   **01 HOLD-PPS-COMPONENTS.** - This structure is defined in the copybook `LTDRG031` and is used to store intermediate values and components used in the PPS (Prospective Payment System) calculations.
    *   **05 H-LOS PIC 9(03).** - Length of Stay (LOS), a three-digit numeric field.
    *   **05 H-REG-DAYS PIC 9(03).** - Regular Days, a three-digit numeric field.
    *   **05 H-TOTAL-DAYS PIC 9(05).** - Total Days, a five-digit numeric field.
    *   **05 H-SSOT PIC 9(02).** - Short Stay Outlier Threshold, a two-digit numeric field.
    *   **05 H-BLEND-RTC PIC 9(02).** - Blend Return Code, a two-digit numeric field.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).** - Blend Facility Percentage, a two-digit numeric field with one decimal place (e.g., 0.8).
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).** - Blend PPS Percentage, a two-digit numeric field with one decimal place.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).** - Short Stay Payment Amount, a nine-digit numeric field with two decimal places.
    *   **05 H-SS-COST PIC 9(07)V9(02).** - Short Stay Cost, a nine-digit numeric field with two decimal places.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).** - Labor Portion, a thirteen-digit numeric field with six decimal places.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).** - Non-Labor Portion, a thirteen-digit numeric field with six decimal places.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).** - Fixed Loss Amount, a nine-digit numeric field with two decimal places.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - New Facility Specific Rate, a seven-digit numeric field with two decimal places.
    *   **05 H-LOS-RATIO PIC 9(01)V9(05).** - Length of Stay Ratio, a six-digit numeric field with five decimal places.
*   The `LTDRG031` copybook is included to define  the `HOLD-PPS-COMPONENTS` structure and likely contains other data used for DRG calculations.

**3. Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.** - This structure represents the input data passed *to* the program from the calling program (likely a claims processing system).  It contains information about the medical bill.
    *   **10 B-NPI10.** - National Provider Identifier (NPI)
        *   **15 B-NPI8 PIC X(08).** - First 8 digits of the NPI.
        *   **15 B-NPI-FILLER PIC X(02).** - Filler, likely used to separate parts of the NPI.
    *   **10 B-PROVIDER-NO PIC X(06).** - Provider Number, a six-character field.
    *   **10 B-PATIENT-STATUS PIC X(02).** - Patient Status, a two-character field.
    *   **10 B-DRG-CODE PIC X(03).** - DRG Code, a three-character field.
    *   **10 B-LOS PIC 9(03).** - Length of Stay, a three-digit numeric field.
    *   **10 B-COV-DAYS PIC 9(03).** - Covered Days, a three-digit numeric field.
    *   **10 B-LTR-DAYS PIC 9(02).** - Lifetime Reserve Days, a two-digit numeric field.
    *   **10 B-DISCHARGE-DATE.** - Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).** - Century and Decade of Discharge Date
        *   **15 B-DISCHG-YY PIC 9(02).** - Year of Discharge Date.
        *   **15 B-DISCHG-MM PIC 9(02).** - Month of Discharge Date.
        *   **15 B-DISCHG-DD PIC 9(02).** - Day of Discharge Date.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).** - Covered Charges, a nine-digit numeric field with two decimal places.
    *   **10 B-SPEC-PAY-IND PIC X(01).** - Special Payment Indicator, a one-character field.
    *   **10 FILLER PIC X(13).** - Unused field, 13 characters
*   **01 PPS-DATA-ALL.** - This structure is passed *back* to the calling program and contains the calculated PPS data.  It's the output of the program.
    *   **05 PPS-RTC PIC 9(02).** - Return Code, a two-digit numeric field, indicating the outcome of the pricing process.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).** - Charge Threshold, a nine-digit numeric field with two decimal places.
    *   **05 PPS-DATA.** - PPS Data.
        *   **10 PPS-MSA PIC X(04).** - Metropolitan Statistical Area (MSA) Code, a four-character field.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).** - Wage Index, a six-digit numeric field with four decimal places.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).** - Average Length of Stay, a three-digit numeric field with one decimal place.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).** - Relative Weight, a five-digit numeric field with four decimal places.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).** - Outlier Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-LOS PIC 9(03).** - Length of Stay, a three-digit numeric field.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).** - DRG Adjusted Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).** - Federal Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).** - Final Payment Amount, a nine-digit numeric field with two decimal places.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).** - Facility Costs, a nine-digit numeric field with two decimal places.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).** - New Facility Specific Rate, a nine-digit numeric field with two decimal places.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).** - Outlier Threshold, a nine-digit numeric field with two decimal places.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).** - Submitted DRG Code, a three-character field.
        *   **10 PPS-CALC-VERS-CD PIC X(05).** - Calculation Version Code, a five-character field.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).** - Regular Days Used, a three-digit numeric field.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).** - Lifetime Reserve Days Used, a three-digit numeric field.
        *   **10 PPS-BLEND-YEAR PIC 9(01).** - Blend Year, a one-digit numeric field.
        *   **10 PPS-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment, a four-digit numeric field with three decimal places.
        *   **10 FILLER PIC X(04).** - Filler, four characters
    *   **05 PPS-OTHER-DATA.** - Other PPS Data.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).** - National Labor Percentage, a six-digit numeric field with five decimal places.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).** - National Non-Labor Percentage, a six-digit numeric field with five decimal places.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).** - Standard Federal Rate, a seven-digit numeric field with two decimal places.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).** - Budget Neutrality Rate, a four-digit numeric field with three decimal places.
        *   **10 FILLER PIC X(20).** - Filler, 20 characters
    *   **05 PPS-PC-DATA.** - PPS PC Data
        *   **10 PPS-COT-IND PIC X(01).** - Cost Outlier Indicator, a one-character field.
        *   **10 FILLER PIC X(20).** - Filler, 20 characters
*   **01 PRICER-OPT-VERS-SW.** -  Pricer Option and Version Switch. This structure controls how the program behaves, likely related to which tables or data sources are used.
    *   **05 PRICER-OPTION-SW PIC X(01).** - Pricer Option Switch, a one-character field.
        *   **88 ALL-TABLES-PASSED VALUE 'A'.** - Condition: All tables passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.** - Condition: Provider record passed.
    *   **05 PPS-VERSIONS.** - PPS Versions.
        *   **10 PPDRV-VERSION PIC X(05).** - PPDRV Version, a five-character field.
*   **01 PROV-NEW-HOLD.** - Provider Record Hold. This structure contains detailed