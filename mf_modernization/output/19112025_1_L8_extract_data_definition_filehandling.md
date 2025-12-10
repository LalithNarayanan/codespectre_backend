# Step 1: Program Overview

## Program: LTCAL032

### Overview
This COBOL program, LTCAL032, is a subroutine designed to calculate Long-Term Care (LTC) payments based on the Prospective Payment System (PPS) for the fiscal year 2003. It receives bill data and provider information as input, performs edits, assembles pricing components, calculates payments (including outliers and short stay adjustments), and returns the results to the calling program. The program uses a copybook (LTDRG031) which contains DRG (Diagnosis Related Group) information.

### Files Accessed
- No explicit file access is defined in the `FILE-CONTROL` section. However, it uses a `COPY` statement to include `LTDRG031` which implies that the DRG table is part of the program.

### Data Structures in WORKING-STORAGE SECTION
-   **W-STORAGE-REF**:  A 46-character field containing the program's name and a description.
-   **CAL-VERSION**: A 5-character field storing the calculation version ('C03.2').
-   **HOLD-PPS-COMPONENTS**: Group of fields to hold intermediate PPS calculation values.
    -   **H-LOS**: Length of Stay (3 digits).
    -   **H-REG-DAYS**: Regular Days (3 digits).
    -   **H-TOTAL-DAYS**: Total Days (5 digits).
    -   **H-SSOT**: Short Stay Outlier Threshold (2 digits).
    -   **H-BLEND-RTC**: Blend Return Code (2 digits).
    -   **H-BLEND-FAC**: Blend Facility Portion (1V1).
    -   **H-BLEND-PPS**: Blend PPS Portion (1V1).
    -   **H-SS-PAY-AMT**: Short Stay Payment Amount (7V2).
    -   **H-SS-COST**: Short Stay Cost (7V2).
    -   **H-LABOR-PORTION**: Labor Portion (7V6).
    -   **H-NONLABOR-PORTION**: Non-Labor Portion (7V6).
    -   **H-FIXED-LOSS-AMT**: Fixed Loss Amount (7V2).
    -   **H-NEW-FAC-SPEC-RATE**: New Facility Specific Rate (5V2).
-   **PRICER-OPT-VERS-SW**:  Group of fields related to pricer option and version switches.
    -   **PRICER-OPTION-SW**: Switch indicating if all tables or just provider record is passed (1 character).
    -   **PPS-VERSIONS**: Group containing PPS versions.
        -   **PPDRV-VERSION**:  PPS Version (5 characters).
-   **W-DRG-FILLS**: contains the DRG data from the COPY LTDRG031.
-   **W-DRG-TABLE**:  Redefines W-DRG-FILLS, structuring the DRG data for efficient access.
    -   **WWM-ENTRY**:  An OCCURS clause defining entries for each DRG.
        -   **WWM-DRG**: DRG Code (3 characters).
        -   **WWM-RELWT**: Relative Weight (1V4).
        -   **WWM-ALOS**: Average Length of Stay (2V1).

### Data Structures in LINKAGE SECTION
-   **BILL-NEW-DATA**:  Structure containing the bill data passed to the subroutine.
    -   **B-NPI10**: National Provider Identifier (NPI) - 10 characters.
        -   **B-NPI8**:  NPI (8 characters).
        -   **B-NPI-FILLER**: Filler for NPI (2 characters).
    -   **B-PROVIDER-NO**: Provider Number (6 characters).
    -   **B-PATIENT-STATUS**: Patient Status (2 characters).
    -   **B-DRG-CODE**: DRG Code (3 characters).
    -   **B-LOS**: Length of Stay (3 digits).
    -   **B-COV-DAYS**: Covered Days (3 digits).
    -   **B-LTR-DAYS**: Lifetime Reserve Days (2 digits).
    -   **B-DISCHARGE-DATE**: Discharge Date.
        -   **B-DISCHG-CC**: Century Code (2 digits).
        -   **B-DISCHG-YY**: Year (2 digits).
        -   **B-DISCHG-MM**: Month (2 digits).
        -   **B-DISCHG-DD**: Day (2 digits).
    -   **B-COV-CHARGES**: Covered Charges (7V2).
    -   **B-SPEC-PAY-IND**: Special Payment Indicator (1 character).
    -   **FILLER**: Filler (13 characters).
-   **PPS-DATA-ALL**: Structure to return PPS calculated data.
    -   **PPS-RTC**: Return Code (2 digits).
    -   **PPS-CHRG-THRESHOLD**: Charge Threshold (7V2).
    -   **PPS-DATA**: Group of PPS data.
        -   **PPS-MSA**: MSA (Metropolitan Statistical Area) Code (4 characters).
        -   **PPS-WAGE-INDEX**: Wage Index (2V4).
        -   **PPS-AVG-LOS**: Average Length of Stay (2V1).
        -   **PPS-RELATIVE-WGT**: Relative Weight (1V4).
        -   **PPS-OUTLIER-PAY-AMT**: Outlier Payment Amount (7V2).
        -   **PPS-LOS**: Length of Stay (3 digits).
        -   **PPS-DRG-ADJ-PAY-AMT**: DRG Adjusted Payment Amount (7V2).
        -   **PPS-FED-PAY-AMT**: Federal Payment Amount (7V2).
        -   **PPS-FINAL-PAY-AMT**: Final Payment Amount (7V2).
        -   **PPS-FAC-COSTS**: Facility Costs (7V2).
        -   **PPS-NEW-FAC-SPEC-RATE**: New Facility Specific Rate (7V2).
        -   **PPS-OUTLIER-THRESHOLD**: Outlier Threshold (7V2).
        -   **PPS-SUBM-DRG-CODE**: Submitted DRG Code (3 characters).
        -   **PPS-CALC-VERS-CD**: Calculation Version Code (5 characters).
        -   **PPS-REG-DAYS-USED**: Regular Days Used (3 digits).
        -   **PPS-LTR-DAYS-USED**: Lifetime Reserve Days Used (3 digits).
        -   **PPS-BLEND-YEAR**: Blend Year (1 digit).
        -   **PPS-COLA**:  Cost of Living Adjustment (1V3).
        -   **FILLER**: Filler (4 characters).
    -   **PPS-OTHER-DATA**: Group of other PPS data.
        -   **PPS-NAT-LABOR-PCT**: National Labor Percentage (1V5).
        -   **PPS-NAT-NONLABOR-PCT**: National Non-Labor Percentage (1V5).
        -   **PPS-STD-FED-RATE**: Standard Federal Rate (5V2).
        -   **PPS-BDGT-NEUT-RATE**: Budget Neutrality Rate (1V3).
        -   **FILLER**: Filler (20 characters).
    -   **PPS-PC-DATA**: Group of PPS PC data.
        -   **PPS-COT-IND**: Cost Outlier Indicator (1 character).
        -   **FILLER**: Filler (20 characters).
-   **PROV-NEW-HOLD**: Structure containing the provider-specific data passed to the subroutine.
    -   **PROV-NEWREC-HOLD1**: Group of provider record data.
        -   **P-NEW-NPI10**: National Provider Identifier (NPI) - 10 characters.
            -   **P-NEW-NPI8**:  NPI (8 characters).
            -   **P-NEW-NPI-FILLER**: Filler for NPI (2 characters).
        -   **P-NEW-PROVIDER-NO**: Provider Number (6 characters).
        -   **P-NEW-DATE-DATA**: Date Data.
            -   **P-NEW-EFF-DATE**: Effective Date.
                -   **P-NEW-EFF-DT-CC**: Century Code (2 digits).
                -   **P-NEW-EFF-DT-YY**: Year (2 digits).
                -   **P-NEW-EFF-DT-MM**: Month (2 digits).
                -   **P-NEW-EFF-DT-DD**: Day (2 digits).
            -   **P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date.
                -   **P-NEW-FY-BEG-DT-CC**: Century Code (2 digits).
                -   **P-NEW-FY-BEG-DT-YY**: Year (2 digits).
                -   **P-NEW-FY-BEG-DT-MM**: Month (2 digits).
                -   **P-NEW-FY-BEG-DT-DD**: Day (2 digits).
            -   **P-NEW-REPORT-DATE**: Reporting Date.
                -   **P-NEW-REPORT-DT-CC**: Century Code (2 digits).
                -   **P-NEW-REPORT-DT-YY**: Year (2 digits).
                -   **P-NEW-REPORT-DT-MM**: Month (2 digits).
                -   **P-NEW-REPORT-DT-DD**: Day (2 digits).
            -   **P-NEW-TERMINATION-DATE**: Termination Date.
                -   **P-NEW-TERM-DT-CC**: Century Code (2 digits).
                -   **P-NEW-TERM-DT-YY**: Year (2 digits).
                -   **P-NEW-TERM-DT-MM**: Month (2 digits).
                -   **P-NEW-TERM-DT-DD**: Day (2 digits).
        -   **P-NEW-WAIVER-CODE**:  Waiver Code (1 character).
        -   **P-NEW-INTER-NO**: Intern Number (5 digits).
        -   **P-NEW-PROVIDER-TYPE**: Provider Type (2 characters).
        -   **P-NEW-CURRENT-CENSUS-DIV**: Current Census Division (1 digit)
        -   **P-NEW-MSA-DATA**: MSA Data.
            -   **P-NEW-CHG-CODE-INDEX**: Charge Code Index (1 character).
            -   **P-NEW-GEO-LOC-MSAX**: Geographic Location MSA (4 characters).
            -   **P-NEW-WAGE-INDEX-LOC-MSA**: Wage Index Location MSA (4 characters).
            -   **P-NEW-STAND-AMT-LOC-MSA**: Standard Amount Location MSA (4 characters).
            -   **P-NEW-SOL-COM-DEP-HOSP-YR**:  SOL COM DEP HOSP YR (2 characters).
        -   **P-NEW-LUGAR**: Lugar (1 character).
        -   **P-NEW-TEMP-RELIEF-IND**: Temporary Relief Indicator (1 character).
        -   **P-NEW-FED-PPS-BLEND-IND**: Federal PPS Blend Indicator (1 character).
        -   **FILLER**: Filler (5 characters).
    -   **PROV-NEWREC-HOLD2**: Group of provider record data.
        -   **P-NEW-VARIABLES**: Variables.
            -   **P-NEW-FAC-SPEC-RATE**: Facility Specific Rate (5V2).
            -   **P-NEW-COLA**: Cost of Living Adjustment (1V3).
            -   **P-NEW-INTERN-RATIO**: Intern Ratio (1V4).
            -   **P-NEW-BED-SIZE**: Bed Size (5 digits).
            -   **P-NEW-OPER-CSTCHG-RATIO**: Operating Cost-to-Charge Ratio (1V3).
            -   **P-NEW-CMI**: CMI (Case Mix Index) (1V4).
            -   **P-NEW-SSI-RATIO**: SSI Ratio (V9(04)).
            -   **P-NEW-MEDICAID-RATIO**: Medicaid Ratio (V9(04)).
            -   **P-NEW-PPS-BLEND-YR-IND**: PPS Blend Year Indicator (1 digit).
            -   **P-NEW-PRUF-UPDTE-FACTOR**: PRUF Update Factor (1V5).
            -   **P-NEW-DSH-PERCENT**: DSH Percent (V9(04)).
            -   **P-NEW-FYE-DATE**: Fiscal Year End Date (8 characters).
        -   **FILLER**: Filler (23 characters).
    -   **PROV-NEWREC-HOLD3**: Group of provider record data.
        -   **P-NEW-PASS-AMT-DATA**: Pass Through Amount Data.
            -   **P-NEW-PASS-AMT-CAPITAL**: Capital Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-DIR-MED-ED**: Direct Medical Education Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-ORGAN-ACQ**: Organ Acquisition Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-PLUS-MISC**: Plus Miscellaneous Pass Through Amount (4V2).
        -   **P-NEW-CAPI-DATA**: Capital Data.
            -   **P-NEW-CAPI-PPS-PAY-CODE**: Capital PPS Pay Code (1 character).
            -   **P-NEW-CAPI-HOSP-SPEC-RATE**: Hospital Specific Rate (4V2).
            -   **P-NEW-CAPI-OLD-HARM-RATE**: Old Harm Rate (4V2).
            -   **P-NEW-CAPI-NEW-HARM-RATIO**: New Harm Ratio (1V4).
            -   **P-NEW-CAPI-CSTCHG-RATIO**: Cost-to-Charge Ratio (V999).
            -   **P-NEW-CAPI-NEW-HOSP**: New Hospital (1 character).
            -   **P-NEW-CAPI-IME**: IME (Indirect Medical Education) (V9999).
            -   **P-NEW-CAPI-EXCEPTIONS**: Exceptions (4V2).
        -   **FILLER**: Filler (22 characters).
-   **WAGE-NEW-INDEX-RECORD**: Structure containing the wage index data.
    -   **W-MSA**: MSA Code (4 characters).
    -   **W-EFF-DATE**: Effective Date (8 characters).
    -   **W-WAGE-INDEX1**: Wage Index 1 (S9(02)V9(04)).
    -   **W-WAGE-INDEX2**: Wage Index 2 (S9(02)V9(04)).
    -   **W-WAGE-INDEX3**: Wage Index 3 (S9(02)V9(04)).

## Program: LTCAL042

### Overview
This COBOL program, LTCAL042, is a subroutine designed to calculate Long-Term Care (LTC) payments based on the Prospective Payment System (PPS) for the fiscal year 2004 (effective July 1, 2003). It receives bill data and provider information as input, performs edits, assembles pricing components, calculates payments (including outliers and short stay adjustments), and returns the results to the calling program. The program uses a copybook (LTDRG031) which contains DRG (Diagnosis Related Group) information. The core logic is similar to LTCAL032, with adjustments for the specific fiscal year's rates and rules.

### Files Accessed
- No explicit file access is defined in the `FILE-CONTROL` section. However, it uses a `COPY` statement to include `LTDRG031` which implies that the DRG table is part of the program.

### Data Structures in WORKING-STORAGE SECTION
-   **W-STORAGE-REF**:  A 46-character field containing the program's name and a description.
-   **CAL-VERSION**: A 5-character field storing the calculation version ('C04.2').
-   **HOLD-PPS-COMPONENTS**: Group of fields to hold intermediate PPS calculation values.
    -   **H-LOS**: Length of Stay (3 digits).
    -   **H-REG-DAYS**: Regular Days (3 digits).
    -   **H-TOTAL-DAYS**: Total Days (5 digits).
    -   **H-SSOT**: Short Stay Outlier Threshold (2 digits).
    -   **H-BLEND-RTC**: Blend Return Code (2 digits).
    -   **H-BLEND-FAC**: Blend Facility Portion (1V1).
    -   **H-BLEND-PPS**: Blend PPS Portion (1V1).
    -   **H-SS-PAY-AMT**: Short Stay Payment Amount (7V2).
    -   **H-SS-COST**: Short Stay Cost (7V2).
    -   **H-LABOR-PORTION**: Labor Portion (7V6).
    -   **H-NONLABOR-PORTION**: Non-Labor Portion (7V6).
    -   **H-FIXED-LOSS-AMT**: Fixed Loss Amount (7V2).
    -   **H-NEW-FAC-SPEC-RATE**: New Facility Specific Rate (5V2).
    -   **H-LOS-RATIO**: Length of Stay Ratio (1V5).
-   **PRICER-OPT-VERS-SW**:  Group of fields related to pricer option and version switches.
    -   **PRICER-OPTION-SW**: Switch indicating if all tables or just provider record is passed (1 character).
    -   **PPS-VERSIONS**: Group containing PPS versions.
        -   **PPDRV-VERSION**:  PPS Version (5 characters).
-   **W-DRG-FILLS**: contains the DRG data from the COPY LTDRG031.
-   **W-DRG-TABLE**:  Redefines W-DRG-FILLS, structuring the DRG data for efficient access.
    -   **WWM-ENTRY**:  An OCCURS clause defining entries for each DRG.
        -   **WWM-DRG**: DRG Code (3 characters).
        -   **WWM-RELWT**: Relative Weight (1V4).
        -   **WWM-ALOS**: Average Length of Stay (2V1).

### Data Structures in LINKAGE SECTION
-   **BILL-NEW-DATA**:  Structure containing the bill data passed to the subroutine.
    -   **B-NPI10**: National Provider Identifier (NPI) - 10 characters.
        -   **B-NPI8**:  NPI (8 characters).
        -   **B-NPI-FILLER**: Filler for NPI (2 characters).
    -   **B-PROVIDER-NO**: Provider Number (6 characters).
    -   **B-PATIENT-STATUS**: Patient Status (2 characters).
    -   **B-DRG-CODE**: DRG Code (3 characters).
    -   **B-LOS**: Length of Stay (3 digits).
    -   **B-COV-DAYS**: Covered Days (3 digits).
    -   **B-LTR-DAYS**: Lifetime Reserve Days (2 digits).
    -   **B-DISCHARGE-DATE**: Discharge Date.
        -   **B-DISCHG-CC**: Century Code (2 digits).
        -   **B-DISCHG-YY**: Year (2 digits).
        -   **B-DISCHG-MM**: Month (2 digits).
        -   **B-DISCHG-DD**: Day (2 digits).
    -   **B-COV-CHARGES**: Covered Charges (7V2).
    -   **B-SPEC-PAY-IND**: Special Payment Indicator (1 character).
    -   **FILLER**: Filler (13 characters).
-   **PPS-DATA-ALL**: Structure to return PPS calculated data.
    -   **PPS-RTC**: Return Code (2 digits).
    -   **PPS-CHRG-THRESHOLD**: Charge Threshold (7V2).
    -   **PPS-DATA**: Group of PPS data.
        -   **PPS-MSA**: MSA (Metropolitan Statistical Area) Code (4 characters).
        -   **PPS-WAGE-INDEX**: Wage Index (2V4).
        -   **PPS-AVG-LOS**: Average Length of Stay (2V1).
        -   **PPS-RELATIVE-WGT**: Relative Weight (1V4).
        -   **PPS-OUTLIER-PAY-AMT**: Outlier Payment Amount (7V2).
        -   **PPS-LOS**: Length of Stay (3 digits).
        -   **PPS-DRG-ADJ-PAY-AMT**: DRG Adjusted Payment Amount (7V2).
        -   **PPS-FED-PAY-AMT**: Federal Payment Amount (7V2).
        -   **PPS-FINAL-PAY-AMT**: Final Payment Amount (7V2).
        -   **PPS-FAC-COSTS**: Facility Costs (7V2).
        -   **PPS-NEW-FAC-SPEC-RATE**: New Facility Specific Rate (7V2).
        -   **PPS-OUTLIER-THRESHOLD**: Outlier Threshold (7V2).
        -   **PPS-SUBM-DRG-CODE**: Submitted DRG Code (3 characters).
        -   **PPS-CALC-VERS-CD**: Calculation Version Code (5 characters).
        -   **PPS-REG-DAYS-USED**: Regular Days Used (3 digits).
        -   **PPS-LTR-DAYS-USED**: Lifetime Reserve Days Used (3 digits).
        -   **PPS-BLEND-YEAR**: Blend Year (1 digit).
        -   **PPS-COLA**:  Cost of Living Adjustment (1V3).
        -   **FILLER**: Filler (4 characters).
    -   **PPS-OTHER-DATA**: Group of other PPS data.
        -   **PPS-NAT-LABOR-PCT**: National Labor Percentage (1V5).
        -   **PPS-NAT-NONLABOR-PCT**: National Non-Labor Percentage (1V5).
        -   **PPS-STD-FED-RATE**: Standard Federal Rate (5V2).
        -   **PPS-BDGT-NEUT-RATE**: Budget Neutrality Rate (1V3).
        -   **FILLER**: Filler (20 characters).
    -   **PPS-PC-DATA**: Group of PPS PC data.
        -   **PPS-COT-IND**: Cost Outlier Indicator (1 character).
        -   **FILLER**: Filler (20 characters).
-   **PROV-NEW-HOLD**: Structure containing the provider-specific data passed to the subroutine.
    -   **PROV-NEWREC-HOLD1**: Group of provider record data.
        -   **P-NEW-NPI10**: National Provider Identifier (NPI) - 10 characters.
            -   **P-NEW-NPI8**:  NPI (8 characters).
            -   **P-NEW-NPI-FILLER**: Filler for NPI (2 characters).
        -   **P-NEW-PROVIDER-NO**: Provider Number (6 characters).
        -   **P-NEW-DATE-DATA**: Date Data.
            -   **P-NEW-EFF-DATE**: Effective Date.
                -   **P-NEW-EFF-DT-CC**: Century Code (2 digits).
                -   **P-NEW-EFF-DT-YY**: Year (2 digits).
                -   **P-NEW-EFF-DT-MM**: Month (2 digits).
                -   **P-NEW-EFF-DT-DD**: Day (2 digits).
            -   **P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date.
                -   **P-NEW-FY-BEG-DT-CC**: Century Code (2 digits).
                -   **P-NEW-FY-BEG-DT-YY**: Year (2 digits).
                -   **P-NEW-FY-BEG-DT-MM**: Month (2 digits).
                -   **P-NEW-FY-BEG-DT-DD**: Day (2 digits).
            -   **P-NEW-REPORT-DATE**: Reporting Date.
                -   **P-NEW-REPORT-DT-CC**: Century Code (2 digits).
                -   **P-NEW-REPORT-DT-YY**: Year (2 digits).
                -   **P-NEW-REPORT-DT-MM**: Month (2 digits).
                -   **P-NEW-REPORT-DT-DD**: Day (2 digits).
            -   **P-NEW-TERMINATION-DATE**: Termination Date.
                -   **P-NEW-TERM-DT-CC**: Century Code (2 digits).
                -   **P-NEW-TERM-DT-YY**: Year (2 digits).
                -   **P-NEW-TERM-DT-MM**: Month (2 digits).
                -   **P-NEW-TERM-DT-DD**: Day (2 digits).
        -   **P-NEW-WAIVER-CODE**:  Waiver Code (1 character).
        -   **P-NEW-INTER-NO**: Intern Number (5 digits).
        -   **P-NEW-PROVIDER-TYPE**: Provider Type (2 characters).
        -   **P-NEW-CURRENT-CENSUS-DIV**: Current Census Division (1 digit)
        -   **P-NEW-MSA-DATA**: MSA Data.
            -   **P-NEW-CHG-CODE-INDEX**: Charge Code Index (1 character).
            -   **P-NEW-GEO-LOC-MSAX**: Geographic Location MSA (4 characters).
            -   **P-NEW-WAGE-INDEX-LOC-MSA**: Wage Index Location MSA (4 characters).
            -   **P-NEW-STAND-AMT-LOC-MSA**: Standard Amount Location MSA (4 characters).
            -   **P-NEW-SOL-COM-DEP-HOSP-YR**:  SOL COM DEP HOSP YR (2 characters).
        -   **P-NEW-LUGAR**: Lugar (1 character).
        -   **P-NEW-TEMP-RELIEF-IND**: Temporary Relief Indicator (1 character).
        -   **P-NEW-FED-PPS-BLEND-IND**: Federal PPS Blend Indicator (1 character).
        -   **FILLER**: Filler (5 characters).
    -   **PROV-NEWREC-HOLD2**: Group of provider record data.
        -   **P-NEW-VARIABLES**: Variables.
            -   **P-NEW-FAC-SPEC-RATE**: Facility Specific Rate (5V2).
            -   **P-NEW-COLA**: Cost of Living Adjustment (1V3).
            -   **P-NEW-INTERN-RATIO**: Intern Ratio (1V4).
            -   **P-NEW-BED-SIZE**: Bed Size (5 digits).
            -   **P-NEW-OPER-CSTCHG-RATIO**: Operating Cost-to-Charge Ratio (1V3).
            -   **P-NEW-CMI**: CMI (Case Mix Index) (1V4).
            -   **P-NEW-SSI-RATIO**: SSI Ratio (V9(04)).
            -   **P-NEW-MEDICAID-RATIO**: Medicaid Ratio (V9(04)).
            -   **P-NEW-PPS-BLEND-YR-IND**: PPS Blend Year Indicator (1 digit).
            -   **P-NEW-PRUF-UPDTE-FACTOR**: PRUF Update Factor (1V5).
            -   **P-NEW-DSH-PERCENT**: DSH Percent (V9(04)).
            -   **P-NEW-FYE-DATE**: Fiscal Year End Date (8 characters).
        -   **FILLER**: Filler (23 characters).
    -   **PROV-NEWREC-HOLD3**: Group of provider record data.
        -   **P-NEW-PASS-AMT-DATA**: Pass Through Amount Data.
            -   **P-NEW-PASS-AMT-CAPITAL**: Capital Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-DIR-MED-ED**: Direct Medical Education Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-ORGAN-ACQ**: Organ Acquisition Pass Through Amount (4V2).
            -   **P-NEW-PASS-AMT-PLUS-MISC**: Plus Miscellaneous Pass Through Amount (4V2).
        -   **P-NEW-CAPI-DATA**: Capital Data.
            -   **P-NEW-CAPI-PPS-PAY-CODE**: Capital PPS Pay Code (1 character).
            -   **P-NEW-CAPI-HOSP-SPEC-RATE**: Hospital Specific Rate (4V2).
            -   **P-NEW-CAPI-OLD-HARM-RATE**: Old Harm Rate (4V2).
            -   **P-NEW-CAPI-NEW-HARM-RATIO**: New Harm Ratio (1V4).
            -   **P-NEW-CAPI-CSTCHG-RATIO**: Cost-to-Charge Ratio (V999).
            -   **P-NEW-CAPI-NEW-HOSP**: New Hospital (1 character).
            -   **P-NEW-CAPI-IME**: IME (Indirect Medical Education) (V9999).
            -   **P-NEW-CAPI-EXCEPTIONS**: Exceptions (4V2).
        -   **FILLER**: Filler (22 characters).
-   **WAGE-NEW-INDEX-RECORD**: Structure containing the wage index data.
    -   **W-MSA**: MSA Code (4 characters).
    -   **W-EFF-DATE**: Effective Date (8 characters).
    -   **W-WAGE-INDEX1**: Wage Index 1 (S9(02)V9(04)).
    -   **W-WAGE-INDEX2**: Wage Index 2 (S9(02)V9(04)).
    -   **W-WAGE-INDEX3**: Wage Index 3 (S9(02)V9(04)).

## Program: LTDRG031

### Overview

This COBOL program is a data file, that stores DRG (Diagnosis Related Group) information for a specific fiscal year (2003). It is included via a `COPY` statement in LTCAL032 and LTCAL042.  The data is structured to be accessed via an index.

### Files Accessed
-   This is a data file, not a program that accesses files.

### Data Structures in WORKING-STORAGE SECTION
-   **W-DRG-FILLS**: A repeating group that holds the raw data for each DRG entry.
-   **W-DRG-TABLE**:  A redefinition of `W-DRG-FILLS` providing a structured format for accessing the DRG data.
    -   **WWM-ENTRY**: An OCCURS clause defining the structure of each DRG entry.
        -   **WWM-DRG**: DRG Code (3 characters). This is the key field.
        -   **WWM-RELWT**: Relative Weight (1V4).
        -   **WWM-ALOS**: Average Length of Stay (2V1).

### Data Structures in LINKAGE SECTION
-   No linkage section is defined as the program is a data file.

# Summary

-   **LTCAL032 and LTCAL042**: These programs calculate LTC payments based on the PPS system for different fiscal years. They take bill and provider data as input, perform edits, calculate payments, and return results. They both use the `LTDRG031` copybook for DRG data.
-   **LTDRG031**: This is a data file containing DRG information used by the LTCAL programs. It provides the DRG codes, relative weights, and average lengths of stay required for payment calculations.

