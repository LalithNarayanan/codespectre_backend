## Analysis of LTCAL032

### Files Accessed and Description

*   **LTDRG031**: This is a COPY member. It is included in the program and contains data used for DRG calculations. This data is likely a table of DRG codes, relative weights, and average lengths of stay.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF**:
    *   `PIC X(46)`:  A 46-character alphanumeric field.
    *   `VALUE 'LTCAL032 - W O R K I N G S T O R A G E'`: Initializes the field with a descriptive string, likely for debugging or identification.
*   **CAL-VERSION**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C03.2'`:  Stores the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS**:
    *   This group of fields is used to store intermediate calculation values.
    *   **H-LOS**: `PIC 9(03)`: Length of Stay (LOS), a 3-digit numeric field (integer).
    *   **H-REG-DAYS**: `PIC 9(03)`: Regular Days, a 3-digit numeric field (integer).
    *   **H-TOTAL-DAYS**: `PIC 9(05)`: Total Days, a 5-digit numeric field (integer).
    *   **H-SSOT**: `PIC 9(02)`:  Likely represents the Short Stay Outlier Threshold, a 2-digit numeric field (integer).
    *   **H-BLEND-RTC**: `PIC 9(02)`: Blend Return Code, a 2-digit numeric field (integer).
    *   **H-BLEND-FAC**: `PIC 9(01)V9(01)`: Blend Facility Rate, a 2-digit numeric field with 1 decimal place.
    *   **H-BLEND-PPS**: `PIC 9(01)V9(01)`: Blend PPS Rate, a 2-digit numeric field with 1 decimal place.
    *   **H-SS-PAY-AMT**: `PIC 9(07)V9(02)`: Short Stay Payment Amount, a 9-digit numeric field with 2 decimal places.
    *   **H-SS-COST**: `PIC 9(07)V9(02)`: Short Stay Cost, a 9-digit numeric field with 2 decimal places.
    *   **H-LABOR-PORTION**: `PIC 9(07)V9(06)`: Labor Portion, a 13-digit numeric field with 6 decimal places.
    *   **H-NONLABOR-PORTION**: `PIC 9(07)V9(06)`: Non-Labor Portion, a 13-digit numeric field with 6 decimal places.
    *   **H-FIXED-LOSS-AMT**: `PIC 9(07)V9(02)`: Fixed Loss Amount, a 9-digit numeric field with 2 decimal places.
    *   **H-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: New Facility Specific Rate, a 7-digit numeric field with 2 decimal places.
*   **W-DRG-FILLS**:
    *   This structure contains a series of 44-character strings.  These strings likely hold the DRG table data.
*   **W-DRG-TABLE**:
    *   This structure REDEFINES `W-DRG-FILLS` and provides a more usable format for the DRG data.
    *   **WWM-ENTRY**: `OCCURS 502 TIMES`: An array that repeats 502 times. Each entry represents a DRG code.
    *   **WWM-DRG**: `PIC X(3)`: The DRG code, a 3-character alphanumeric field.
    *   **WWM-RELWT**: `PIC 9(1)V9(4)`: Relative Weight for the DRG, a 5-digit numeric field with 4 decimal places.
    *   **WWM-ALOS**: `PIC 9(2)V9(1)`: Average Length of Stay for the DRG, a 3-digit numeric field with 1 decimal place.

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA**:
    *   This structure represents the input data passed to the program.
    *   **B-NPI10**:
        *   **B-NPI8**: `PIC X(08)`: First 8 characters of the NPI (National Provider Identifier).
        *   **B-NPI-FILLER**: `PIC X(02)`: Filler for the NPI, 2 characters.
    *   **B-PROVIDER-NO**: `PIC X(06)`: Provider Number, a 6-character alphanumeric field.
    *   **B-PATIENT-STATUS**: `PIC X(02)`: Patient Status, a 2-character alphanumeric field.
    *   **B-DRG-CODE**: `PIC X(03)`: DRG Code, a 3-character alphanumeric field.
    *   **B-LOS**: `PIC 9(03)`: Length of Stay, a 3-digit numeric field (integer).
    *   **B-COV-DAYS**: `PIC 9(03)`: Covered Days, a 3-digit numeric field (integer).
    *   **B-LTR-DAYS**: `PIC 9(02)`: Lifetime Reserve Days, a 2-digit numeric field (integer).
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: `PIC 9(02)`: Century code of Discharge Date.
        *   **B-DISCHG-YY**: `PIC 9(02)`: Year of Discharge Date.
        *   **B-DISCHG-MM**: `PIC 9(02)`: Month of Discharge Date.
        *   **B-DISCHG-DD**: `PIC 9(02)`: Day of Discharge Date.
    *   **B-COV-CHARGES**: `PIC 9(07)V9(02)`: Covered Charges, a 9-digit numeric field with 2 decimal places.
    *   **B-SPEC-PAY-IND**: `PIC X(01)`: Special Payment Indicator, a 1-character alphanumeric field.
    *   **FILLER**: `PIC X(13)`: Filler, 13 characters.
*   **PPS-DATA-ALL**:
    *   This is the output structure, holding the calculated results.
    *   **PPS-RTC**: `PIC 9(02)`: Return Code, a 2-digit numeric field (integer) indicating the outcome of the calculation.
    *   **PPS-CHRG-THRESHOLD**: `PIC 9(07)V9(02)`: Charge Threshold, a 9-digit numeric field with 2 decimal places.
    *   **PPS-DATA**:
        *   **PPS-MSA**: `PIC X(04)`: MSA (Metropolitan Statistical Area) code, a 4-character alphanumeric field.
        *   **PPS-WAGE-INDEX**: `PIC 9(02)V9(04)`: Wage Index, a 6-digit numeric field with 4 decimal places.
        *   **PPS-AVG-LOS**: `PIC 9(02)V9(01)`: Average Length of Stay, a 3-digit numeric field with 1 decimal place.
        *   **PPS-RELATIVE-WGT**: `PIC 9(01)V9(04)`: Relative Weight, a 5-digit numeric field with 4 decimal places.
        *   **PPS-OUTLIER-PAY-AMT**: `PIC 9(07)V9(02)`: Outlier Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-LOS**: `PIC 9(03)`: Length of Stay, a 3-digit numeric field (integer).
        *   **PPS-DRG-ADJ-PAY-AMT**: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FED-PAY-AMT**: `PIC 9(07)V9(02)`: Federal Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FINAL-PAY-AMT**: `PIC 9(07)V9(02)`: Final Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FAC-COSTS**: `PIC 9(07)V9(02)`: Facility Costs, a 9-digit numeric field with 2 decimal places.
        *   **PPS-NEW-FAC-SPEC-RATE**: `PIC 9(07)V9(02)`: New Facility Specific Rate, a 9-digit numeric field with 2 decimal places.
        *   **PPS-OUTLIER-THRESHOLD**: `PIC 9(07)V9(02)`: Outlier Threshold, a 9-digit numeric field with 2 decimal places.
        *   **PPS-SUBM-DRG-CODE**: `PIC X(03)`: Submitted DRG Code, a 3-character alphanumeric field.
        *   **PPS-CALC-VERS-CD**: `PIC X(05)`: Calculation Version Code, a 5-character alphanumeric field.
        *   **PPS-REG-DAYS-USED**: `PIC 9(03)`: Regular Days Used, a 3-digit numeric field (integer).
        *   **PPS-LTR-DAYS-USED**: `PIC 9(03)`: Lifetime Reserve Days Used, a 3-digit numeric field (integer).
        *   **PPS-BLEND-YEAR**: `PIC 9(01)`: Blend Year Indicator, a 1-digit numeric field (integer).
        *   **PPS-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment, a 4-digit numeric field with 3 decimal places.
        *   **FILLER**: `PIC X(04)`: Filler, 4 characters.
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: `PIC 9(01)V9(05)`: National Labor Percentage, a 6-digit numeric field with 5 decimal places.
        *   **PPS-NAT-NONLABOR-PCT**: `PIC 9(01)V9(05)`: National Non-Labor Percentage, a 6-digit numeric field with 5 decimal places.
        *   **PPS-STD-FED-RATE**: `PIC 9(05)V9(02)`: Standard Federal Rate, a 7-digit numeric field with 2 decimal places.
        *   **PPS-BDGT-NEUT-RATE**: `PIC 9(01)V9(03)`: Budget Neutrality Rate, a 4-digit numeric field with 3 decimal places.
        *   **FILLER**: `PIC X(20)`: Filler, 20 characters.
    *   **PPS-PC-DATA**:
        *   **PPS-COT-IND**: `PIC X(01)`: Cost Outlier Indicator, a 1-character alphanumeric field.
        *   **FILLER**: `PIC X(20)`: Filler, 20 characters.
*   **PRICER-OPT-VERS-SW**:
    *   This structure seems to indicate the version of the pricing logic and whether all tables are passed.
    *   **PRICER-OPTION-SW**: `PIC X(01)`:  Option switch, 1 character.
        *   `88 ALL-TABLES-PASSED VALUE 'A'`:  Condition to indicate all tables were passed.
        *   `88 PROV-RECORD-PASSED VALUE 'P'`: Condition to indicate the provider record was passed.
    *   **PPS-VERSIONS**:
        *   **PPDRV-VERSION**: `PIC X(05)`:  Version of the PPDRV program, a 5-character alphanumeric field.
*   **PROV-NEW-HOLD**:
    *   This structure holds provider-specific data.
    *   **PROV-NEWREC-HOLD1**:
        *   **P-NEW-NPI10**:
            *   **P-NEW-NPI8**: `PIC X(08)`:  Provider NPI (first 8 characters).
            *   **P-NEW-NPI-FILLER**: `PIC X(02)`: Filler for Provider NPI.
        *   **P-NEW-PROVIDER-NO**:
            *   **P-NEW-STATE**: `PIC 9(02)`: Provider State, a 2-digit numeric field (integer).
            *   **FILLER**: `PIC X(04)`: Filler, 4 characters.
        *   **P-NEW-DATE-DATA**:
            *   **P-NEW-EFF-DATE**:
                *   **P-NEW-EFF-DT-CC**: `PIC 9(02)`: Century code of Effective Date.
                *   **P-NEW-EFF-DT-YY**: `PIC 9(02)`: Year of Effective Date.
                *   **P-NEW-EFF-DT-MM**: `PIC 9(02)`: Month of Effective Date.
                *   **P-NEW-EFF-DT-DD**: `PIC 9(02)`: Day of Effective Date.
            *   **P-NEW-FY-BEGIN-DATE**:
                *   **P-NEW-FY-BEG-DT-CC**: `PIC 9(02)`: Century code of Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-YY**: `PIC 9(02)`: Year of Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-MM**: `PIC 9(02)`: Month of Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-DD**: `PIC 9(02)`: Day of Fiscal Year Begin Date.
            *   **P-NEW-REPORT-DATE**:
                *   **P-NEW-REPORT-DT-CC**: `PIC 9(02)`: Century code of Report Date.
                *   **P-NEW-REPORT-DT-YY**: `PIC 9(02)`: Year of Report Date.
                *   **P-NEW-REPORT-DT-MM**: `PIC 9(02)`: Month of Report Date.
                *   **P-NEW-REPORT-DT-DD**: `PIC 9(02)`: Day of Report Date.
            *   **P-NEW-TERMINATION-DATE**:
                *   **P-NEW-TERM-DT-CC**: `PIC 9(02)`: Century code of Termination Date.
                *   **P-NEW-TERM-DT-YY**: `PIC 9(02)`: Year of Termination Date.
                *   **P-NEW-TERM-DT-MM**: `PIC 9(02)`: Month of Termination Date.
                *   **P-NEW-TERM-DT-DD**: `PIC 9(02)`: Day of Termination Date.
        *   **P-NEW-WAIVER-CODE**: `PIC X(01)`: Waiver Code, 1 character.
            *   `88 P-NEW-WAIVER-STATE VALUE 'Y'`: Condition to check if waiver state is 'Y'.
        *   **P-NEW-INTER-NO**: `PIC 9(05)`: Internal Number, a 5-digit numeric field (integer).
        *   **P-NEW-PROVIDER-TYPE**: `PIC X(02)`: Provider Type, a 2-character alphanumeric field.
        *   **P-NEW-CURRENT-CENSUS-DIV**: `PIC 9(01)`: Current Census Division, a 1-digit numeric field (integer).
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV**: Redefines the previous field.
        *   **P-NEW-MSA-DATA**:
            *   **P-NEW-CHG-CODE-INDEX**: `PIC X`: Charge Code Index, 1 character.
            *   **P-NEW-GEO-LOC-MSAX**: `PIC X(04)`: Geo Location MSA, 4 characters.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX**: Redefines the previous field.
            *   **P-NEW-WAGE-INDEX-LOC-MSA**: `PIC X(04)`: Wage Index Location MSA, 4 characters.
            *   **P-NEW-STAND-AMT-LOC-MSA**: `PIC X(04)`: Standard Amount Location MSA, 4 characters.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA**: Redefines the previous field.
                *   **P-NEW-RURAL-1ST**:
                    *   **P-NEW-STAND-RURAL**: `PIC XX`: Standard Rural, 2 characters.
                        *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '`: Condition to check if standard rural is spaces.
                    *   **P-NEW-RURAL-2ND**: `PIC XX`: Rural 2nd, 2 characters.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR**: `PIC XX`:  Sol Com Dep Hosp Year, 2 characters.
        *   **P-NEW-LUGAR**: `PIC X`: Lugar, 1 character.
        *   **P-NEW-TEMP-RELIEF-IND**: `PIC X`: Temporary Relief Indicator, 1 character.
        *   **P-NEW-FED-PPS-BLEND-IND**: `PIC X`: Federal PPS Blend Indicator, 1 character.
        *   **FILLER**: `PIC X(05)`: Filler, 5 characters.
    *   **PROV-NEWREC-HOLD2**:
        *   **P-NEW-VARIABLES**:
            *   **P-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: Facility Specific Rate, a 7-digit numeric field with 2 decimal places.
            *   **P-NEW-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment, a 4-digit numeric field with 3 decimal places.
            *   **P-NEW-INTERN-RATIO**: `PIC 9(01)V9(04)`: Intern Ratio, a 5-digit numeric field with 4 decimal places.
            *   **P-NEW-BED-SIZE**: `PIC 9(05)`: Bed Size, a 5-digit numeric field (integer).
            *   **P-NEW-OPER-CSTCHG-RATIO**: `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio, a 4-digit numeric field with 3 decimal places.
            *   **P-NEW-CMI**: `PIC 9(01)V9(04)`: CMI, a 5-digit numeric field with 4 decimal places.
            *   **P-NEW-SSI-RATIO**: `PIC V9(04)`: SSI Ratio, a 4-digit numeric field with 4 decimal places.
            *   **P-NEW-MEDICAID-RATIO**: `PIC V9(04)`: Medicaid Ratio, a 4-digit numeric field with 4 decimal places.
            *   **P-NEW-PPS-BLEND-YR-IND**: `PIC 9(01)`: PPS Blend Year Indicator, a 1-digit numeric field (integer).
            *   **P-NEW-PRUF-UPDTE-FACTOR**: `PIC 9(01)V9(05)`: PRUF Update Factor, a 6-digit numeric field with 5 decimal places.
            *   **P-NEW-DSH-PERCENT**: `PIC V9(04)`: DSH Percentage, a 4-digit numeric field with 4 decimal places.
            *   **P-NEW-FYE-DATE**: `PIC X(08)`: Fiscal Year End Date, an 8-character alphanumeric field.
        *   **FILLER**: `PIC X(23)`: Filler, 23 characters.
    *   **PROV-NEWREC-HOLD3**:
        *   **P-NEW-PASS-AMT-DATA**:
            *   **P-NEW-PASS-AMT-CAPITAL**: `PIC 9(04)V99`: Passed Amount Capital, a 6-digit numeric field with 2 decimal places.
            *   **P-NEW-PASS-AMT-DIR-MED-ED**: `PIC 9(04)V99`: Passed Amount Direct Medical Education, a 6-digit numeric field with 2 decimal places.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ**: `PIC 9(04)V99`: Passed Amount Organ Acquisition, a 6-digit numeric field with 2 decimal places.
            *   **P-NEW-PASS-AMT-PLUS-MISC**: `PIC 9(04)V99`: Passed Amount Plus Misc, a 6-digit numeric field with 2 decimal places.
        *   **P-NEW-CAPI-DATA**:
            *   **P-NEW-CAPI-PPS-PAY-CODE**: `PIC X`: Capi PPS Pay Code, 1 character.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE**: `PIC 9(04)V99`: Capi Hospital Specific Rate, a 6-digit numeric field with 2 decimal places.
            *   **P-NEW-CAPI-OLD-HARM-RATE**: `PIC 9(04)V99`: Capi Old Harm Rate, a 6-digit numeric field with 2 decimal places.
            *   **P-NEW-CAPI-NEW-HARM-RATIO**: `PIC 9(01)V9999`: Capi New Harm Ratio, a 5-digit numeric field with 4 decimal places.
            *   **P-NEW-CAPI-CSTCHG-RATIO**: `PIC 9V999`: Capi Cost to Charge Ratio, a 4-digit numeric field with 3 decimal places.
            *   **P-NEW-CAPI-NEW-HOSP**: `PIC X`: Capi New Hosp, 1 character.
            *   **P-NEW-CAPI-IME**: `PIC 9V9999`: Capi IME, a 5-digit numeric field with 4 decimal places.
            *   **P-NEW-CAPI-EXCEPTIONS**: `PIC 9(04)V99`: Capi Exceptions, a 6-digit numeric field with 2 decimal places.
        *   **FILLER**: `PIC X(22)`: Filler, 22 characters.
*   **WAGE-NEW-INDEX-RECORD**:
    *   This structure contains wage index data.
    *   **W-MSA**: `PIC X(4)`: MSA Code, a 4-character alphanumeric field.
    *   **W-EFF-DATE**: `PIC X(8)`: Effective Date, an 8-character alphanumeric field.
    *   **W-WAGE-INDEX1**: `PIC S9(02)V9(04)`: Wage Index 1, a 6-digit signed numeric field with 4 decimal places.
    *   **W-WAGE-INDEX2**: `PIC S9(02)V9(04)`: Wage Index 2, a 6-digit signed numeric field with 4 decimal places.
    *   **W-WAGE-INDEX3**: `PIC S9(02)V9(04)`: Wage Index 3, a 6-digit signed numeric field with 4 decimal places.

## Analysis of LTCAL042

### Files Accessed and Description

*   **LTDRG031**: This is a COPY member. It is included in the program and contains data used for DRG calculations. This data is likely a table of DRG codes, relative weights, and average lengths of stay.

### Data Structures in WORKING-STORAGE SECTION

*   **W-STORAGE-REF**:
    *   `PIC X(46)`: A 46-character alphanumeric field.
    *   `VALUE 'LTCAL042 - W O R K I N G S T O R A G E'`: Initializes the field with a descriptive string, likely for debugging or identification.
*   **CAL-VERSION**:
    *   `PIC X(05)`: A 5-character alphanumeric field.
    *   `VALUE 'C04.2'`: Stores the version number of the calculation logic.
*   **HOLD-PPS-COMPONENTS**:
    *   This group of fields is used to store intermediate calculation values.
    *   **H-LOS**: `PIC 9(03)`: Length of Stay (LOS), a 3-digit numeric field (integer).
    *   **H-REG-DAYS**: `PIC 9(03)`: Regular Days, a 3-digit numeric field (integer).
    *   **H-TOTAL-DAYS**: `PIC 9(05)`: Total Days, a 5-digit numeric field (integer).
    *   **H-SSOT**: `PIC 9(02)`:  Likely represents the Short Stay Outlier Threshold, a 2-digit numeric field (integer).
    *   **H-BLEND-RTC**: `PIC 9(02)`: Blend Return Code, a 2-digit numeric field (integer).
    *   **H-BLEND-FAC**: `PIC 9(01)V9(01)`: Blend Facility Rate, a 2-digit numeric field with 1 decimal place.
    *   **H-BLEND-PPS**: `PIC 9(01)V9(01)`: Blend PPS Rate, a 2-digit numeric field with 1 decimal place.
    *   **H-SS-PAY-AMT**: `PIC 9(07)V9(02)`: Short Stay Payment Amount, a 9-digit numeric field with 2 decimal places.
    *   **H-SS-COST**: `PIC 9(07)V9(02)`: Short Stay Cost, a 9-digit numeric field with 2 decimal places.
    *   **H-LABOR-PORTION**: `PIC 9(07)V9(06)`: Labor Portion, a 13-digit numeric field with 6 decimal places.
    *   **H-NONLABOR-PORTION**: `PIC 9(07)V9(06)`: Non-Labor Portion, a 13-digit numeric field with 6 decimal places.
    *   **H-FIXED-LOSS-AMT**: `PIC 9(07)V9(02)`: Fixed Loss Amount, a 9-digit numeric field with 2 decimal places.
    *   **H-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: New Facility Specific Rate, a 7-digit numeric field with 2 decimal places.
    *   **H-LOS-RATIO**: `PIC 9(01)V9(05)`: Length of Stay Ratio, a 6-digit numeric field with 5 decimal places.
*   **W-DRG-FILLS**:
    *   This structure contains a series of 44-character strings.  These strings likely hold the DRG table data.
*   **W-DRG-TABLE**:
    *   This structure REDEFINES `W-DRG-FILLS` and provides a more usable format for the DRG data.
    *   **WWM-ENTRY**: `OCCURS 502 TIMES`: An array that repeats 502 times. Each entry represents a DRG code.
    *   **WWM-DRG**: `PIC X(3)`: The DRG code, a 3-character alphanumeric field.
    *   **WWM-RELWT**: `PIC 9(1)V9(4)`: Relative Weight for the DRG, a 5-digit numeric field with 4 decimal places.
    *   **WWM-ALOS**: `PIC 9(2)V9(1)`: Average Length of Stay for the DRG, a 3-digit numeric field with 1 decimal place.

### Data Structures in LINKAGE SECTION

*   **BILL-NEW-DATA**:
    *   This structure represents the input data passed to the program.
    *   **B-NPI10**:
        *   **B-NPI8**: `PIC X(08)`: First 8 characters of the NPI (National Provider Identifier).
        *   **B-NPI-FILLER**: `PIC X(02)`: Filler for the NPI, 2 characters.
    *   **B-PROVIDER-NO**: `PIC X(06)`: Provider Number, a 6-character alphanumeric field.
    *   **B-PATIENT-STATUS**: `PIC X(02)`: Patient Status, a 2-character alphanumeric field.
    *   **B-DRG-CODE**: `PIC X(03)`: DRG Code, a 3-character alphanumeric field.
    *   **B-LOS**: `PIC 9(03)`: Length of Stay, a 3-digit numeric field (integer).
    *   **B-COV-DAYS**: `PIC 9(03)`: Covered Days, a 3-digit numeric field (integer).
    *   **B-LTR-DAYS**: `PIC 9(02)`: Lifetime Reserve Days, a 2-digit numeric field (integer).
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: `PIC 9(02)`: Century code of Discharge Date.
        *   **B-DISCHG-YY**: `PIC 9(02)`: Year of Discharge Date.
        *   **B-DISCHG-MM**: `PIC 9(02)`: Month of Discharge Date.
        *   **B-DISCHG-DD**: `PIC 9(02)`: Day of Discharge Date.
    *   **B-COV-CHARGES**: `PIC 9(07)V9(02)`: Covered Charges, a 9-digit numeric field with 2 decimal places.
    *   **B-SPEC-PAY-IND**: `PIC X(01)`: Special Payment Indicator, a 1-character alphanumeric field.
    *   **FILLER**: `PIC X(13)`: Filler, 13 characters.
*   **PPS-DATA-ALL**:
    *   This is the output structure, holding the calculated results.
    *   **PPS-RTC**: `PIC 9(02)`: Return Code, a 2-digit numeric field (integer) indicating the outcome of the calculation.
    *   **PPS-CHRG-THRESHOLD**: `PIC 9(07)V9(02)`: Charge Threshold, a 9-digit numeric field with 2 decimal places.
    *   **PPS-DATA**:
        *   **PPS-MSA**: `PIC X(04)`: MSA (Metropolitan Statistical Area) code, a 4-character alphanumeric field.
        *   **PPS-WAGE-INDEX**: `PIC 9(02)V9(04)`: Wage Index, a 6-digit numeric field with 4 decimal places.
        *   **PPS-AVG-LOS**: `PIC 9(02)V9(01)`: Average Length of Stay, a 3-digit numeric field with 1 decimal place.
        *   **PPS-RELATIVE-WGT**: `PIC 9(01)V9(04)`: Relative Weight, a 5-digit numeric field with 4 decimal places.
        *   **PPS-OUTLIER-PAY-AMT**: `PIC 9(07)V9(02)`: Outlier Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-LOS**: `PIC 9(03)`: Length of Stay, a 3-digit numeric field (integer).
        *   **PPS-DRG-ADJ-PAY-AMT**: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FED-PAY-AMT**: `PIC 9(07)V9(02)`: Federal Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FINAL-PAY-AMT**: `PIC 9(07)V9(02)`: Final Payment Amount, a 9-digit numeric field with 2 decimal places.
        *   **PPS-FAC-COSTS**: `PIC 9(07)V9(02)`: Facility Costs, a 9-digit numeric field with 2 decimal places.
        *   **PPS-NEW-FAC-SPEC-RATE**: `PIC 9(07)V9(02)`: New Facility Specific Rate, a 9-digit numeric field with 2 decimal places.
        *   **PPS-OUTLIER-THRESHOLD**: `PIC 9(07)V9(02)`: Outlier Threshold, a 9-digit numeric field with 2 decimal places.
        *   **PPS-SUBM-DRG-CODE**: `PIC X(03)`: Submitted DRG Code, a 3-character alphanumeric field.
        *   **PPS-CALC-VERS-CD**: `PIC X(05)`: Calculation Version Code, a 5-character alphanumeric field.
        *   **PPS-REG-DAYS-USED**: `PIC 9(03)`: Regular Days Used, a 3-digit numeric field (integer).
        *   **PPS-LTR-DAYS-USED**: `PIC 9(03)`: Lifetime Reserve Days Used, a 3-digit numeric field (integer).
        *   **PPS-BLEND-YEAR**: `PIC 9(01)`: Blend Year Indicator, a 1-digit numeric field (integer).
        *   **PPS-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment, a 4-digit numeric field with 3 decimal places.
        *   **FILLER**: `PIC X(04)`: Filler, 4 characters.
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: `PIC 9(01)V9(05)`: National Labor Percentage, a 6-digit numeric field with 5 decimal places.
        *   **PPS-NAT-NONLABOR-PCT**: `PIC 9(01)V9(05)`: National Non-Labor Percentage, a 6-digit numeric