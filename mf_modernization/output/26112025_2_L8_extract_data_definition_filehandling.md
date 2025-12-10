## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, working storage, and linkage sections.

### Program: LTCAL032

#### Files Accessed and their Description:

This program implicitly accesses the following:
*   **LTDRG031**: This is a `COPY` file, which is included in the program.

#### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF**:
    *   `PIC X(46)`:  Used to store a descriptive string identifying the program and its working storage.
*   **CAL-VERSION**:
    *   `PIC X(05)`: Stores the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS**:
    *   **H-LOS**: `PIC 9(03)`: Length of Stay
    *   **H-REG-DAYS**: `PIC 9(03)`: Regular Days
    *   **H-TOTAL-DAYS**: `PIC 9(05)`: Total Days
    *   **H-SSOT**: `PIC 9(02)`: Short Stay Outlier Threshold
    *   **H-BLEND-RTC**: `PIC 9(02)`: Blend Return Code
    *   **H-BLEND-FAC**: `PIC 9(01)V9(01)`: Blend Facility Rate
    *   **H-BLEND-PPS**: `PIC 9(01)V9(01)`: Blend PPS Rate
    *   **H-SS-PAY-AMT**: `PIC 9(07)V9(02)`: Short Stay Payment Amount
    *   **H-SS-COST**: `PIC 9(07)V9(02)`: Short Stay Cost
    *   **H-LABOR-PORTION**: `PIC 9(07)V9(06)`: Labor Portion of Payment
    *   **H-NONLABOR-PORTION**: `PIC 9(07)V9(06)`: Non-Labor Portion of Payment
    *   **H-FIXED-LOSS-AMT**: `PIC 9(07)V9(02)`: Fixed Loss Amount
    *   **H-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: New Facility Specific Rate
*   **PPS-DATA-ALL**:
    *   **PPS-RTC**: `PIC 9(02)`: Return Code
    *   **PPS-CHRG-THRESHOLD**: `PIC 9(07)V9(02)`: Charges Threshold
    *   **PPS-DATA**:
        *   **PPS-MSA**: `PIC X(04)`: Metropolitan Statistical Area
        *   **PPS-WAGE-INDEX**: `PIC 9(02)V9(04)`: Wage Index
        *   **PPS-AVG-LOS**: `PIC 9(02)V9(01)`: Average Length of Stay
        *   **PPS-RELATIVE-WGT**: `PIC 9(01)V9(04)`: Relative Weight
        *   **PPS-OUTLIER-PAY-AMT**: `PIC 9(07)V9(02)`: Outlier Payment Amount
        *   **PPS-LOS**: `PIC 9(03)`: Length of Stay
        *   **PPS-DRG-ADJ-PAY-AMT**: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
        *   **PPS-FED-PAY-AMT**: `PIC 9(07)V9(02)`: Federal Payment Amount
        *   **PPS-FINAL-PAY-AMT**: `PIC 9(07)V9(02)`: Final Payment Amount
        *   **PPS-FAC-COSTS**: `PIC 9(07)V9(02)`: Facility Costs
        *   **PPS-NEW-FAC-SPEC-RATE**: `PIC 9(07)V9(02)`: New Facility Specific Rate
        *   **PPS-OUTLIER-THRESHOLD**: `PIC 9(07)V9(02)`: Outlier Threshold
        *   **PPS-SUBM-DRG-CODE**: `PIC X(03)`: Submitted DRG Code
        *   **PPS-CALC-VERS-CD**: `PIC X(05)`: Calculation Version Code
        *   **PPS-REG-DAYS-USED**: `PIC 9(03)`: Regular Days Used
        *   **PPS-LTR-DAYS-USED**: `PIC 9(03)`: Lifetime Reserve Days Used
        *   **PPS-BLEND-YEAR**: `PIC 9(01)`: Blend Year
        *   **PPS-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment
        *   **FILLER**: `PIC X(04)`: Filler
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: `PIC 9(01)V9(05)`: National Labor Percentage
        *   **PPS-NAT-NONLABOR-PCT**: `PIC 9(01)V9(05)`: National Non-Labor Percentage
        *   **PPS-STD-FED-RATE**: `PIC 9(05)V9(02)`: Standard Federal Rate
        *   **PPS-BDGT-NEUT-RATE**: `PIC 9(01)V9(03)`: Budget Neutrality Rate
        *   **FILLER**: `PIC X(20)`: Filler
    *   **PPS-PC-DATA**:
        *   **PPS-COT-IND**: `PIC X(01)`: Cost Outlier Indicator
        *   **FILLER**: `PIC X(20)`: Filler
*   **PRICER-OPT-VERS-SW**:
    *   **PRICER-OPTION-SW**: `PIC X(01)`: Pricer Option Switch
        *   **ALL-TABLES-PASSED**: `VALUE 'A'`:  Indicates all tables passed.
        *   **PROV-RECORD-PASSED**: `VALUE 'P'`: Indicates provider record passed.
    *   **PPS-VERSIONS**:
        *   **PPDRV-VERSION**: `PIC X(05)`: Version of the PPDRV program.
*   **PROV-NEW-HOLD**:
    *   **PROV-NEWREC-HOLD1**:
        *   **P-NEW-NPI10**:
            *   **P-NEW-NPI8**: `PIC X(08)`: NPI (National Provider Identifier)
            *   **P-NEW-NPI-FILLER**: `PIC X(02)`: Filler for NPI
        *   **P-NEW-PROVIDER-NO**: `PIC X(06)`: Provider Number
        *   **P-NEW-DATE-DATA**:
            *   **P-NEW-EFF-DATE**:
                *   **P-NEW-EFF-DT-CC**: `PIC 9(02)`: Century of Effective Date
                *   **P-NEW-EFF-DT-YY**: `PIC 9(02)`: Year of Effective Date
                *   **P-NEW-EFF-DT-MM**: `PIC 9(02)`: Month of Effective Date
                *   **P-NEW-EFF-DT-DD**: `PIC 9(02)`: Day of Effective Date
            *   **P-NEW-FY-BEGIN-DATE**:
                *   **P-NEW-FY-BEG-DT-CC**: `PIC 9(02)`: Century of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-YY**: `PIC 9(02)`: Year of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-MM**: `PIC 9(02)`: Month of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-DD**: `PIC 9(02)`: Day of Fiscal Year Begin Date
            *   **P-NEW-REPORT-DATE**:
                *   **P-NEW-REPORT-DT-CC**: `PIC 9(02)`: Century of Report Date
                *   **P-NEW-REPORT-DT-YY**: `PIC 9(02)`: Year of Report Date
                *   **P-NEW-REPORT-DT-MM**: `PIC 9(02)`: Month of Report Date
                *   **P-NEW-REPORT-DT-DD**: `PIC 9(02)`: Day of Report Date
            *   **P-NEW-TERMINATION-DATE**:
                *   **P-NEW-TERM-DT-CC**: `PIC 9(02)`: Century of Termination Date
                *   **P-NEW-TERM-DT-YY**: `PIC 9(02)`: Year of Termination Date
                *   **P-NEW-TERM-DT-MM**: `PIC 9(02)`: Month of Termination Date
                *   **P-NEW-TERM-DT-DD**: `PIC 9(02)`: Day of Termination Date
        *   **P-NEW-WAIVER-CODE**: `PIC X(01)`: Waiver Code
            *   **P-NEW-WAIVER-STATE**: `VALUE 'Y'`: Waiver State
        *   **P-NEW-INTER-NO**: `PIC 9(05)`: Internal Number
        *   **P-NEW-PROVIDER-TYPE**: `PIC X(02)`: Provider Type
        *   **P-NEW-CURRENT-CENSUS-DIV**: `PIC 9(01)`: Census Division (Current)
        *   **P-NEW-CURRENT-DIV** REDEFINES **P-NEW-CURRENT-CENSUS-DIV**: `PIC 9(01)`: Census Division (Current)
        *   **P-NEW-MSA-DATA**:
            *   **P-NEW-CHG-CODE-INDEX**: `PIC X`: Charge Code Index
            *   **P-NEW-GEO-LOC-MSAX**: `PIC X(04)`: Geographic Location MSA - JUST RIGHT
            *   **P-NEW-GEO-LOC-MSA9** REDEFINES **P-NEW-GEO-LOC-MSAX**: `PIC 9(04)`: Geographic Location MSA - JUST RIGHT
            *   **P-NEW-WAGE-INDEX-LOC-MSA**: `PIC X(04)`: Wage Index Location MSA - JUST RIGHT
            *   **P-NEW-STAND-AMT-LOC-MSA**: `PIC X(04)`: Standard Amount Location MSA - JUST RIGHT
            *   **P-NEW-STAND-AMT-LOC-MSA9** REDEFINES **P-NEW-STAND-AMT-LOC-MSA**:
                *   **P-NEW-RURAL-1ST**:
                    *   **P-NEW-STAND-RURAL**: `PIC XX`: Rural Standard
                        *   **P-NEW-STD-RURAL-CHECK**: `VALUE '  '`: Rural Standard Check
                    *   **P-NEW-RURAL-2ND**: `PIC XX`: Rural Standard
        *   **P-NEW-SOL-COM-DEP-HOSP-YR**: `PIC XX`: Sole Community Hospital Year
        *   **P-NEW-LUGAR**: `PIC X`: Lugar
        *   **P-NEW-TEMP-RELIEF-IND**: `PIC X`: Temporary Relief Indicator
        *   **P-NEW-FED-PPS-BLEND-IND**: `PIC X`: Federal PPS Blend Indicator
        *   **FILLER**: `PIC X(05)`: Filler
    *   **PROV-NEWREC-HOLD2**:
        *   **P-NEW-VARIABLES**:
            *   **P-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: Facility Specific Rate
            *   **P-NEW-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   **P-NEW-INTERN-RATIO**: `PIC 9(01)V9(04)`: Intern Ratio
            *   **P-NEW-BED-SIZE**: `PIC 9(05)`: Bed Size
            *   **P-NEW-OPER-CSTCHG-RATIO**: `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio
            *   **P-NEW-CMI**: `PIC 9(01)V9(04)`: CMI (Case Mix Index)
            *   **P-NEW-SSI-RATIO**: `V9(04)`: SSI Ratio
            *   **P-NEW-MEDICAID-RATIO**: `V9(04)`: Medicaid Ratio
            *   **P-NEW-PPS-BLEND-YR-IND**: `PIC 9(01)`: PPS Blend Year Indicator
            *   **P-NEW-PRUF-UPDTE-FACTOR**: `PIC 9(01)V9(05)`: Pruf Update Factor
            *   **P-NEW-DSH-PERCENT**: `V9(04)`: DSH (Disproportionate Share Hospital) Percent
            *   **P-NEW-FYE-DATE**: `PIC X(08)`: Fiscal Year End Date
        *   **FILLER**: `PIC X(23)`: Filler
    *   **PROV-NEWREC-HOLD3**:
        *   **P-NEW-PASS-AMT-DATA**:
            *   **P-NEW-PASS-AMT-CAPITAL**: `PIC 9(04)V99`: Capital Passed Amount
            *   **P-NEW-PASS-AMT-DIR-MED-ED**: `PIC 9(04)V99`: Direct Medical Education Passed Amount
            *   **P-NEW-PASS-AMT-ORGAN-ACQ**: `PIC 9(04)V99`: Organ Acquisition Passed Amount
            *   **P-NEW-PASS-AMT-PLUS-MISC**: `PIC 9(04)V99`: Plus Miscellaneous Passed Amount
        *   **P-NEW-CAPI-DATA**:
            *   **P-NEW-CAPI-PPS-PAY-CODE**: `PIC X`: Capital PPS Payment Code
            *   **P-NEW-CAPI-HOSP-SPEC-RATE**: `PIC 9(04)V99`: Hospital Specific Rate
            *   **P-NEW-CAPI-OLD-HARM-RATE**: `PIC 9(04)V99`: Old Harm Rate
            *   **P-NEW-CAPI-NEW-HARM-RATIO**: `PIC 9(01)V9999`: New Harm Ratio
            *   **P-NEW-CAPI-CSTCHG-RATIO**: `PIC 9V999`: Capital Cost to Charge Ratio
            *   **P-NEW-CAPI-NEW-HOSP**: `PIC X`: New Hospital Indicator
            *   **P-NEW-CAPI-IME**: `PIC 9V9999`: Capital IME (Indirect Medical Education)
            *   **P-NEW-CAPI-EXCEPTIONS**: `PIC 9(04)V99`: Capital Exceptions
        *   **FILLER**: `PIC X(22)`: Filler
*   **WAGE-NEW-INDEX-RECORD**:
    *   **W-MSA**: `PIC X(4)`: MSA (Metropolitan Statistical Area)
    *   **W-EFF-DATE**: `PIC X(8)`: Effective Date
    *   **W-WAGE-INDEX1**: `PIC S9(02)V9(04)`: Wage Index 1
    *   **W-WAGE-INDEX2**: `PIC S9(02)V9(04)`: Wage Index 2
    *   **W-WAGE-INDEX3**: `PIC S9(02)V9(04)`: Wage Index 3

#### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA**:  This is the input data structure passed to the program.
    *   **B-NPI10**:
        *   **B-NPI8**: `PIC X(08)`: NPI (National Provider Identifier)
        *   **B-NPI-FILLER**: `PIC X(02)`: Filler for NPI
    *   **B-PROVIDER-NO**: `PIC X(06)`: Provider Number
    *   **B-PATIENT-STATUS**: `PIC X(02)`: Patient Status
    *   **B-DRG-CODE**: `PIC X(03)`: DRG Code
    *   **B-LOS**: `PIC 9(03)`: Length of Stay
    *   **B-COV-DAYS**: `PIC 9(03)`: Covered Days
    *   **B-LTR-DAYS**: `PIC 9(02)`: Lifetime Reserve Days
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: `PIC 9(02)`: Century of Discharge Date
        *   **B-DISCHG-YY**: `PIC 9(02)`: Year of Discharge Date
        *   **B-DISCHG-MM**: `PIC 9(02)`: Month of Discharge Date
        *   **B-DISCHG-DD**: `PIC 9(02)`: Day of Discharge Date
    *   **B-COV-CHARGES**: `PIC 9(07)V9(02)`: Covered Charges
    *   **B-SPEC-PAY-IND**: `PIC X(01)`: Special Payment Indicator
    *   **FILLER**: `PIC X(13)`: Filler

*   **PPS-DATA-ALL**: This is an output data structure passed back from the program.  (Same as the WORKING-STORAGE definition.)

*   **PRICER-OPT-VERS-SW**:  This is an output data structure passed back from the program. (Same as the WORKING-STORAGE definition.)

*   **PROV-NEW-HOLD**: This is an input data structure passed to the program. (Same as the WORKING-STORAGE definition.)

*   **WAGE-NEW-INDEX-RECORD**: This is an input data structure passed to the program. (Same as the WORKING-STORAGE definition.)

### Program: LTCAL042

#### Files Accessed and their Description:

This program implicitly accesses the following:
*   **LTDRG031**: This is a `COPY` file, which is included in the program.

#### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF**:
    *   `PIC X(46)`:  Used to store a descriptive string identifying the program and its working storage.
*   **CAL-VERSION**:
    *   `PIC X(05)`: Stores the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS**:
    *   **H-LOS**: `PIC 9(03)`: Length of Stay
    *   **H-REG-DAYS**: `PIC 9(03)`: Regular Days
    *   **H-TOTAL-DAYS**: `PIC 9(05)`: Total Days
    *   **H-SSOT**: `PIC 9(02)`: Short Stay Outlier Threshold
    *   **H-BLEND-RTC**: `PIC 9(02)`: Blend Return Code
    *   **H-BLEND-FAC**: `PIC 9(01)V9(01)`: Blend Facility Rate
    *   **H-BLEND-PPS**: `PIC 9(01)V9(01)`: Blend PPS Rate
    *   **H-SS-PAY-AMT**: `PIC 9(07)V9(02)`: Short Stay Payment Amount
    *   **H-SS-COST**: `PIC 9(07)V9(02)`: Short Stay Cost
    *   **H-LABOR-PORTION**: `PIC 9(07)V9(06)`: Labor Portion of Payment
    *   **H-NONLABOR-PORTION**: `PIC 9(07)V9(06)`: Non-Labor Portion of Payment
    *   **H-FIXED-LOSS-AMT**: `PIC 9(07)V9(02)`: Fixed Loss Amount
    *   **H-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: New Facility Specific Rate
    *   **H-LOS-RATIO**: `PIC 9(01)V9(05)`: Length of Stay Ratio
*   **PPS-DATA-ALL**:
    *   **PPS-RTC**: `PIC 9(02)`: Return Code
    *   **PPS-CHRG-THRESHOLD**: `PIC 9(07)V9(02)`: Charges Threshold
    *   **PPS-DATA**:
        *   **PPS-MSA**: `PIC X(04)`: Metropolitan Statistical Area
        *   **PPS-WAGE-INDEX**: `PIC 9(02)V9(04)`: Wage Index
        *   **PPS-AVG-LOS**: `PIC 9(02)V9(01)`: Average Length of Stay
        *   **PPS-RELATIVE-WGT**: `PIC 9(01)V9(04)`: Relative Weight
        *   **PPS-OUTLIER-PAY-AMT**: `PIC 9(07)V9(02)`: Outlier Payment Amount
        *   **PPS-LOS**: `PIC 9(03)`: Length of Stay
        *   **PPS-DRG-ADJ-PAY-AMT**: `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
        *   **PPS-FED-PAY-AMT**: `PIC 9(07)V9(02)`: Federal Payment Amount
        *   **PPS-FINAL-PAY-AMT**: `PIC 9(07)V9(02)`: Final Payment Amount
        *   **PPS-FAC-COSTS**: `PIC 9(07)V9(02)`: Facility Costs
        *   **PPS-NEW-FAC-SPEC-RATE**: `PIC 9(07)V9(02)`: New Facility Specific Rate
        *   **PPS-OUTLIER-THRESHOLD**: `PIC 9(07)V9(02)`: Outlier Threshold
        *   **PPS-SUBM-DRG-CODE**: `PIC X(03)`: Submitted DRG Code
        *   **PPS-CALC-VERS-CD**: `PIC X(05)`: Calculation Version Code
        *   **PPS-REG-DAYS-USED**: `PIC 9(03)`: Regular Days Used
        *   **PPS-LTR-DAYS-USED**: `PIC 9(03)`: Lifetime Reserve Days Used
        *   **PPS-BLEND-YEAR**: `PIC 9(01)`: Blend Year
        *   **PPS-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment
        *   **FILLER**: `PIC X(04)`: Filler
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: `PIC 9(01)V9(05)`: National Labor Percentage
        *   **PPS-NAT-NONLABOR-PCT**: `PIC 9(01)V9(05)`: National Non-Labor Percentage
        *   **PPS-STD-FED-RATE**: `PIC 9(05)V9(02)`: Standard Federal Rate
        *   **PPS-BDGT-NEUT-RATE**: `PIC 9(01)V9(03)`: Budget Neutrality Rate
        *   **FILLER**: `PIC X(20)`: Filler
    *   **PPS-PC-DATA**:
        *   **PPS-COT-IND**: `PIC X(01)`: Cost Outlier Indicator
        *   **FILLER**: `PIC X(20)`: Filler
*   **PRICER-OPT-VERS-SW**:
    *   **PRICER-OPTION-SW**: `PIC X(01)`: Pricer Option Switch
        *   **ALL-TABLES-PASSED**: `VALUE 'A'`:  Indicates all tables passed.
        *   **PROV-RECORD-PASSED**: `VALUE 'P'`: Indicates provider record passed.
    *   **PPS-VERSIONS**:
        *   **PPDRV-VERSION**: `PIC X(05)`: Version of the PPDRV program.
*   **PROV-NEW-HOLD**:
    *   **PROV-NEWREC-HOLD1**:
        *   **P-NEW-NPI10**:
            *   **P-NEW-NPI8**: `PIC X(08)`: NPI (National Provider Identifier)
            *   **P-NEW-NPI-FILLER**: `PIC X(02)`: Filler for NPI
        *   **P-NEW-PROVIDER-NO**: `PIC X(06)`: Provider Number
        *   **P-NEW-DATE-DATA**:
            *   **P-NEW-EFF-DATE**:
                *   **P-NEW-EFF-DT-CC**: `PIC 9(02)`: Century of Effective Date
                *   **P-NEW-EFF-DT-YY**: `PIC 9(02)`: Year of Effective Date
                *   **P-NEW-EFF-DT-MM**: `PIC 9(02)`: Month of Effective Date
                *   **P-NEW-EFF-DT-DD**: `PIC 9(02)`: Day of Effective Date
            *   **P-NEW-FY-BEGIN-DATE**:
                *   **P-NEW-FY-BEG-DT-CC**: `PIC 9(02)`: Century of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-YY**: `PIC 9(02)`: Year of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-MM**: `PIC 9(02)`: Month of Fiscal Year Begin Date
                *   **P-NEW-FY-BEG-DT-DD**: `PIC 9(02)`: Day of Fiscal Year Begin Date
            *   **P-NEW-REPORT-DATE**:
                *   **P-NEW-REPORT-DT-CC**: `PIC 9(02)`: Century of Report Date
                *   **P-NEW-REPORT-DT-YY**: `PIC 9(02)`: Year of Report Date
                *   **P-NEW-REPORT-DT-MM**: `PIC 9(02)`: Month of Report Date
                *   **P-NEW-REPORT-DT-DD**: `PIC 9(02)`: Day of Report Date
            *   **P-NEW-TERMINATION-DATE**:
                *   **P-NEW-TERM-DT-CC**: `PIC 9(02)`: Century of Termination Date
                *   **P-NEW-TERM-DT-YY**: `PIC 9(02)`: Year of Termination Date
                *   **P-NEW-TERM-DT-MM**: `PIC 9(02)`: Month of Termination Date
                *   **P-NEW-TERM-DT-DD**: `PIC 9(02)`: Day of Termination Date
        *   **P-NEW-WAIVER-CODE**: `PIC X(01)`: Waiver Code
            *   **P-NEW-WAIVER-STATE**: `VALUE 'Y'`: Waiver State
        *   **P-NEW-INTER-NO**: `PIC 9(05)`: Internal Number
        *   **P-NEW-PROVIDER-TYPE**: `PIC X(02)`: Provider Type
        *   **P-NEW-CURRENT-CENSUS-DIV**: `PIC 9(01)`: Census Division (Current)
        *   **P-NEW-CURRENT-DIV** REDEFINES **P-NEW-CURRENT-CENSUS-DIV**: `PIC 9(01)`: Census Division (Current)
        *   **P-NEW-MSA-DATA**:
            *   **P-NEW-CHG-CODE-INDEX**: `PIC X`: Charge Code Index
            *   **P-NEW-GEO-LOC-MSAX**: `PIC X(04)`: Geographic Location MSA - JUST RIGHT
            *   **P-NEW-GEO-LOC-MSA9** REDEFINES **P-NEW-GEO-LOC-MSAX**: `PIC 9(04)`: Geographic Location MSA - JUST RIGHT
            *   **P-NEW-WAGE-INDEX-LOC-MSA**: `PIC X(04)`: Wage Index Location MSA - JUST RIGHT
            *   **P-NEW-STAND-AMT-LOC-MSA**: `PIC X(04)`: Standard Amount Location MSA - JUST RIGHT
            *   **P-NEW-STAND-AMT-LOC-MSA9** REDEFINES **P-NEW-STAND-AMT-LOC-MSA**:
                *   **P-NEW-RURAL-1ST**:
                    *   **P-NEW-STAND-RURAL**: `PIC XX`: Rural Standard
                        *   **P-NEW-STD-RURAL-CHECK**: `VALUE '  '`: Rural Standard Check
                    *   **P-NEW-RURAL-2ND**: `PIC XX`: Rural Standard
        *   **P-NEW-SOL-COM-DEP-HOSP-YR**: `PIC XX`: Sole Community Hospital Year
        *   **P-NEW-LUGAR**: `PIC X`: Lugar
        *   **P-NEW-TEMP-RELIEF-IND**: `PIC X`: Temporary Relief Indicator
        *   **P-NEW-FED-PPS-BLEND-IND**: `PIC X`: Federal PPS Blend Indicator
        *   **FILLER**: `PIC X(05)`: Filler
    *   **PROV-NEWREC-HOLD2**:
        *   **P-NEW-VARIABLES**:
            *   **P-NEW-FAC-SPEC-RATE**: `PIC 9(05)V9(02)`: Facility Specific Rate
            *   **P-NEW-COLA**: `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   **P-NEW-INTERN-RATIO**: `PIC 9(01)V9(04)`: Intern Ratio
            *   **P-NEW-BED-SIZE**: `PIC 9(05)`: Bed Size
            *   **P-NEW-OPER-CSTCHG-RATIO**: `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio
            *   **P-NEW-CMI**: `PIC 9(01)V9(04)`: CMI (Case Mix Index)
            *   **P-NEW-SSI-RATIO**: `V9(04)`: SSI Ratio
            *   **P-NEW-MEDICAID-RATIO**: `V9(04)`: Medicaid Ratio
            *   **P-NEW-PPS-BLEND-YR-IND**: `PIC 9(01)`: PPS Blend Year Indicator
            *   **P-NEW-PRUF-UPDTE-FACTOR**: `PIC 9(01)V9(05)`: Pruf Update Factor
            *   **P-NEW-DSH-PERCENT**: `V9(04)`: DSH (Disproportionate Share Hospital) Percent
            *   **P-NEW-FYE-DATE**: `PIC X(08)`: Fiscal Year End Date
        *   **FILLER**: `PIC X(23)`: Filler
    *   **PROV-NEWREC-HOLD3**:
        *   **P-NEW-PASS-AMT-DATA**:
            *   **P-NEW-PASS-AMT-CAPITAL**: `PIC 9(04)V99`: Capital Passed Amount
            *   **P-NEW-PASS-AMT-DIR-MED-ED**: `PIC 9(04)V99`: Direct Medical Education Passed Amount
            *   **P-NEW-PASS-AMT-ORGAN-ACQ**: `PIC 9(04)V99`: Organ Acquisition Passed Amount
            *   **P-NEW-PASS-AMT-PLUS-MISC**: `PIC 9(04)V99`: Plus Miscellaneous Passed Amount
        *   **P-NEW-CAPI-DATA**:
            *   **P-NEW-CAPI-PPS-PAY-CODE**: `PIC X`: Capital PPS Payment Code
            *   **P-NEW-CAPI-HOSP-SPEC-RATE**: `PIC 9(04)V99`: Hospital Specific Rate
            *   **P-NEW-CAPI-OLD-HARM-RATE**: `PIC 9(04)V99`: Old Harm Rate
            *   **P-NEW-CAPI-NEW-HARM-RATIO**: `PIC 9(01)V9999`: New Harm Ratio
            *   **P-NEW-CAPI-CSTCHG-RATIO**: `PIC 9V999`: Capital Cost to Charge Ratio
            *   **P-NEW-CAPI-NEW-HOSP**: `PIC X`: New Hospital Indicator
            *   **P-NEW-CAPI-IME**: `PIC 9V9999`: Capital IME (Indirect Medical Education)
            *   **P-NEW-CAPI-EXCEPTIONS**: `PIC 9(04)V99`: Capital Exceptions
        *   **FILLER**: `PIC X(22)`: Filler
*   **WAGE-NEW-INDEX-RECORD**:
    *   **W-MSA**: `PIC X(4)`: MSA (Metropolitan Statistical Area)
    *   **W-EFF-DATE**: `PIC X(8)`: Effective Date
    *   **W-WAGE-INDEX1**: `PIC S9(02)V9(04)`: Wage Index 1
    *   **W-WAGE-INDEX2**: `PIC S9(02)V9(04)`: Wage Index 2
    *   **W-WAGE-INDEX3**: `PIC S9(02)V9(04)`: Wage Index 3

#### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA**:  This is the input data structure passed to the program.
    *   **B-NPI10**:
        *   **B-NPI8**: `PIC X(08)`: NPI (National Provider Identifier)
        *   **B-NPI-FILLER**: `PIC X(02)`: Filler for NPI
    *   **B-PROVIDER-NO**: `PIC X(06)`: Provider Number
    *   **B-PATIENT-STATUS**: `PIC X(02)`: Patient Status
    *   **B-DRG-CODE**: `PIC X(03)`: DRG Code
    *   **B-LOS**: `PIC 9(03)`: Length of Stay
    *   **B-COV-DAYS**: `PIC 9(03)`: Covered Days
    *   **B-LTR-DAYS**: `PIC 9(02)`: Lifetime Reserve Days
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: `PIC 9(