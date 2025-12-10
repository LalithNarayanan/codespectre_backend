## Analysis of COBOL Programs

Here's an analysis of each COBOL program, detailing file access, data structures, and their descriptions.

### Program: LTCAL032

#### 1. Files Accessed:

*   **None directly.** This program uses a `COPY` statement to include the data definitions from `LTDRG031`.

#### 2. Data Structures in WORKING-STORAGE SECTION:

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  Stores a descriptive string identifying the program and its purpose ("LTCAL032 - W O R K I N G S T O R A G E").
*   **`CAL-VERSION`**:
    *   `PIC X(05)`: Stores the version of the calculation program ('C03.2').
*   **`HOLD-PPS-COMPONENTS`**: (From `COPY LTDRG031`) - This is a group of data items used to store intermediate calculation results and components.  These are the core working variables for the PPS calculation.
    *   `H-LOS`: `PIC 9(03)` - Length of Stay.
    *   `H-REG-DAYS`: `PIC 9(03)` - Regular Days.
    *   `H-TOTAL-DAYS`: `PIC 9(05)` - Total Days.
    *   `H-SSOT`: `PIC 9(02)` - Short Stay Outlier Threshold.
    *   `H-BLEND-RTC`: `PIC 9(02)` - Blend Return Code.
    *   `H-BLEND-FAC`: `PIC 9(01)V9(01)` - Blend Facility Percentage.
    *   `H-BLEND-PPS`: `PIC 9(01)V9(01)` - Blend PPS Percentage.
    *   `H-SS-PAY-AMT`: `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    *   `H-SS-COST`: `PIC 9(07)V9(02)` - Short Stay Cost.
    *   `H-LABOR-PORTION`: `PIC 9(07)V9(06)` - Labor Portion of Payment.
    *   `H-NONLABOR-PORTION`: `PIC 9(07)V9(06)` - Non-Labor Portion of Payment.
    *   `H-FIXED-LOSS-AMT`: `PIC 9(07)V9(02)` - Fixed Loss Amount.
    *   `H-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)` - New Facility Specific Rate.

#### 3. Data Structures in LINKAGE SECTION:

*   **`BILL-NEW-DATA`**:  This is the main input record passed *to* the program, containing billing information.
    *   `B-NPI10`:  NPI (National Provider Identifier)
        *   `B-NPI8`: `PIC X(08)` - First 8 bytes of NPI.
        *   `B-NPI-FILLER`: `PIC X(02)` - Filler for NPI.
    *   `B-PROVIDER-NO`: `PIC X(06)` - Provider Number.
    *   `B-PATIENT-STATUS`: `PIC X(02)` - Patient Status.
    *   `B-DRG-CODE`: `PIC X(03)` - DRG (Diagnosis Related Group) Code.
    *   `B-LOS`: `PIC 9(03)` - Length of Stay.
    *   `B-COV-DAYS`: `PIC 9(03)` - Covered Days.
    *   `B-LTR-DAYS`: `PIC 9(02)` - Lifetime Reserve Days.
    *   `B-DISCHARGE-DATE`:  Discharge Date
        *   `B-DISCHG-CC`: `PIC 9(02)` - Century/Check for Discharge Date.
        *   `B-DISCHG-YY`: `PIC 9(02)` - Year of Discharge Date.
        *   `B-DISCHG-MM`: `PIC 9(02)` - Month of Discharge Date.
        *   `B-DISCHG-DD`: `PIC 9(02)` - Day of Discharge Date.
    *   `B-COV-CHARGES`: `PIC 9(07)V9(02)` - Covered Charges.
    *   `B-SPEC-PAY-IND`: `PIC X(01)` - Special Payment Indicator.
    *   `FILLER`: `PIC X(13)` - Unused filler.
*   **`PPS-DATA-ALL`**: This structure is passed *to* the program.  It contains the output data and is used to return the calculated PPS information.
    *   `PPS-RTC`: `PIC 9(02)` - Return Code (PPS-RTC).  Indicates the result of the calculation (e.g., normal payment, outlier, short stay, error).
    *   `PPS-CHRG-THRESHOLD`: `PIC 9(07)V9(02)` - Charge Threshold.
    *   `PPS-DATA`:
        *   `PPS-MSA`: `PIC X(04)` - MSA (Metropolitan Statistical Area) Code.
        *   `PPS-WAGE-INDEX`: `PIC 9(02)V9(04)` - Wage Index.
        *   `PPS-AVG-LOS`: `PIC 9(02)V9(01)` - Average Length of Stay.
        *   `PPS-RELATIVE-WGT`: `PIC 9(01)V9(04)` - Relative Weight.
        *   `PPS-OUTLIER-PAY-AMT`: `PIC 9(07)V9(02)` - Outlier Payment Amount.
        *   `PPS-LOS`: `PIC 9(03)` - Length of Stay.
        *   `PPS-DRG-ADJ-PAY-AMT`: `PIC 9(07)V9(02)` - DRG Adjusted Payment Amount.
        *   `PPS-FED-PAY-AMT`: `PIC 9(07)V9(02)` - Federal Payment Amount.
        *   `PPS-FINAL-PAY-AMT`: `PIC 9(07)V9(02)` - Final Payment Amount.
        *   `PPS-FAC-COSTS`: `PIC 9(07)V9(02)` - Facility Costs.
        *   `PPS-NEW-FAC-SPEC-RATE`: `PIC 9(07)V9(02)` - New Facility Specific Rate.
        *   `PPS-OUTLIER-THRESHOLD`: `PIC 9(07)V9(02)` - Outlier Threshold.
        *   `PPS-SUBM-DRG-CODE`: `PIC X(03)` - Submitted DRG Code.
        *   `PPS-CALC-VERS-CD`: `PIC X(05)` - Calculation Version Code.
        *   `PPS-REG-DAYS-USED`: `PIC 9(03)` - Regular Days Used.
        *   `PPS-LTR-DAYS-USED`: `PIC 9(03)` - Lifetime Reserve Days Used.
        *   `PPS-BLEND-YEAR`: `PIC 9(01)` - Blend Year Indicator.
        *   `PPS-COLA`: `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        *   `FILLER`: `PIC X(04)` - Filler.
    *   `PPS-OTHER-DATA`:
        *   `PPS-NAT-LABOR-PCT`: `PIC 9(01)V9(05)` - National Labor Percentage.
        *   `PPS-NAT-NONLABOR-PCT`: `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        *   `PPS-STD-FED-RATE`: `PIC 9(05)V9(02)` - Standard Federal Rate.
        *   `PPS-BDGT-NEUT-RATE`: `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        *   `FILLER`: `PIC X(20)` - Filler.
    *   `PPS-PC-DATA`:
        *   `PPS-COT-IND`: `PIC X(01)` - Cost Outlier Indicator.
        *   `FILLER`: `PIC X(20)` - Filler.
*   **`PRICER-OPT-VERS-SW`**:  This structure provides information on the version of the pricer.
    *   `PRICER-OPTION-SW`: `PIC X(01)` - Pricer Option Switch.
        *   `ALL-TABLES-PASSED`: `VALUE 'A'` - Indicates all tables are passed (likely the default).
        *   `PROV-RECORD-PASSED`: `VALUE 'P'` - Indicates the provider record is passed.
    *   `PPS-VERSIONS`:
        *   `PPDRV-VERSION`: `PIC X(05)` - Version of the PPDRV program.
*   **`PROV-NEW-HOLD`**:  This structure contains the provider record. It's used to pass provider-specific data *to* the program.
    *   `PROV-NEWREC-HOLD1`:
        *   `P-NEW-NPI10`:  NPI
            *   `P-NEW-NPI8`: `PIC X(08)`
            *   `P-NEW-NPI-FILLER`: `PIC X(02)`
        *   `P-NEW-PROVIDER-NO`:  Provider Number
            *   `P-NEW-STATE`: `PIC 9(02)` - State.
            *   `FILLER`: `PIC X(04)`
        *   `P-NEW-DATE-DATA`:
            *   `P-NEW-EFF-DATE`:  Effective Date
                *   `P-NEW-EFF-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-EFF-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-EFF-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-EFF-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                *   `P-NEW-FY-BEG-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-FY-BEG-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-FY-BEG-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-FY-BEG-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-REPORT-DATE`:  Report Date
                *   `P-NEW-REPORT-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-REPORT-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-REPORT-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-REPORT-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-TERMINATION-DATE`: Termination Date
                *   `P-NEW-TERM-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-TERM-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-TERM-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-TERM-DT-DD`: `PIC 9(02)` - Day.
        *   `P-NEW-WAIVER-CODE`: `PIC X(01)` - Waiver Code.
            *   `P-NEW-WAIVER-STATE`: `VALUE 'Y'` - Waiver State.
        *   `P-NEW-INTER-NO`: `PIC 9(05)` - Internal Number.
        *   `P-NEW-PROVIDER-TYPE`: `PIC X(02)` - Provider Type.
        *   `P-NEW-CURRENT-CENSUS-DIV`: `PIC 9(01)` - Current Census Division.
        *   `P-NEW-CURRENT-DIV` REDEFINES `P-NEW-CURRENT-CENSUS-DIV`: `PIC 9(01)`
        *   `P-NEW-MSA-DATA`:
            *   `P-NEW-CHG-CODE-INDEX`: `PIC X` - Charge Code Index.
            *   `P-NEW-GEO-LOC-MSAX`: `PIC X(04)` - Geographic Location MSA (Metropolitan Statistical Area)
            *   `P-NEW-GEO-LOC-MSA9` REDEFINES `P-NEW-GEO-LOC-MSAX`: `PIC 9(04)`
            *   `P-NEW-WAGE-INDEX-LOC-MSA`: `PIC X(04)` - Wage Index Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA`: `PIC X(04)` - Standard Amount Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES `P-NEW-STAND-AMT-LOC-MSA`:
                *   `P-NEW-RURAL-1ST`:
                    *   `P-NEW-STAND-RURAL`: `PIC XX`
                        *   `P-NEW-STD-RURAL-CHECK`: `VALUE '  '`
                    *   `P-NEW-RURAL-2ND`: `PIC XX`
        *   `P-NEW-SOL-COM-DEP-HOSP-YR`: `PIC XX` - Sole Community Hospital Year.
        *   `P-NEW-LUGAR`: `PIC X` - Lugar.
        *   `P-NEW-TEMP-RELIEF-IND`: `PIC X` - Temporary Relief Indicator.
        *   `P-NEW-FED-PPS-BLEND-IND`: `PIC X` - Federal PPS Blend Indicator.
        *   `FILLER`: `PIC X(05)` - Filler.
    *   `PROV-NEWREC-HOLD2`:
        *   `P-NEW-VARIABLES`:
            *   `P-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)` - Facility Specific Rate.
            *   `P-NEW-COLA`: `PIC 9(01)V9(03)` - Cost of Living Adjustment.
            *   `P-NEW-INTERN-RATIO`: `PIC 9(01)V9(04)` - Intern Ratio.
            *   `P-NEW-BED-SIZE`: `PIC 9(05)` - Bed Size.
            *   `P-NEW-OPER-CSTCHG-RATIO`: `PIC 9(01)V9(03)` - Operating Cost to Charge Ratio.
            *   `P-NEW-CMI`: `PIC 9(01)V9(04)` - CMI (Case Mix Index).
            *   `P-NEW-SSI-RATIO`: `PIC V9(04)` - SSI Ratio.
            *   `P-NEW-MEDICAID-RATIO`: `PIC V9(04)` - Medicaid Ratio.
            *   `P-NEW-PPS-BLEND-YR-IND`: `PIC 9(01)` - PPS Blend Year Indicator.
            *   `P-NEW-PRUF-UPDTE-FACTOR`: `PIC 9(01)V9(05)` - Pruf Update Factor.
            *   `P-NEW-DSH-PERCENT`: `PIC V9(04)` - DSH (Disproportionate Share Hospital) Percentage.
            *   `P-NEW-FYE-DATE`: `PIC X(08)` - Fiscal Year End Date.
        *   `FILLER`: `PIC X(23)` - Filler.
    *   `PROV-NEWREC-HOLD3`:
        *   `P-NEW-PASS-AMT-DATA`:
            *   `P-NEW-PASS-AMT-CAPITAL`: `PIC 9(04)V99` - Passed Amount Capital.
            *   `P-NEW-PASS-AMT-DIR-MED-ED`: `PIC 9(04)V99` - Passed Amount Direct Medical Education.
            *   `P-NEW-PASS-AMT-ORGAN-ACQ`: `PIC 9(04)V99` - Passed Amount Organ Acquisition.
            *   `P-NEW-PASS-AMT-PLUS-MISC`: `PIC 9(04)V99` - Passed Amount Plus Miscellaneous.
        *   `P-NEW-CAPI-DATA`:
            *   `P-NEW-CAPI-PPS-PAY-CODE`: `PIC X` - Capital PPS Pay Code.
            *   `P-NEW-CAPI-HOSP-SPEC-RATE`: `PIC 9(04)V99` - Capital Hospital Specific Rate.
            *   `P-NEW-CAPI-OLD-HARM-RATE`: `PIC 9(04)V99` - Capital Old Harm Rate.
            *   `P-NEW-CAPI-NEW-HARM-RATIO`: `PIC 9(01)V9999` - Capital New Harm Ratio.
            *   `P-NEW-CAPI-CSTCHG-RATIO`: `PIC 9V999` - Capital Cost to Charge Ratio.
            *   `P-NEW-CAPI-NEW-HOSP`: `PIC X` - Capital New Hospital.
            *   `P-NEW-CAPI-IME`: `PIC 9V9999` - Capital IME (Indirect Medical Education).
            *   `P-NEW-CAPI-EXCEPTIONS`: `PIC 9(04)V99` - Capital Exceptions.
        *   `FILLER`: `PIC X(22)` - Filler.
*   **`WAGE-NEW-INDEX-RECORD`**: This structure is passed *to* the program and contains the Wage Index information.
    *   `W-MSA`: `PIC X(4)` - MSA Code.
    *   `W-EFF-DATE`: `PIC X(8)` - Effective Date.
    *   `W-WAGE-INDEX1`: `PIC S9(02)V9(04)` - Wage Index.
    *   `W-WAGE-INDEX2`: `PIC S9(02)V9(04)` - Wage Index.
    *   `W-WAGE-INDEX3`: `PIC S9(02)V9(04)` - Wage Index.

### Program: LTCAL042

#### 1. Files Accessed:

*   **None directly.** This program uses a `COPY` statement to include the data definitions from `LTDRG031`.

#### 2. Data Structures in WORKING-STORAGE SECTION:

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`: Stores a descriptive string identifying the program and its purpose ("LTCAL042 - W O R K I N G S T O R A G E").
*   **`CAL-VERSION`**:
    *   `PIC X(05)`: Stores the version of the calculation program ('C04.2').
*   **`HOLD-PPS-COMPONENTS`**: (From `COPY LTDRG031`) - Identical to LTCAL032. This is a group of data items used to store intermediate calculation results and components.  These are the core working variables for the PPS calculation.
    *   `H-LOS`: `PIC 9(03)` - Length of Stay.
    *   `H-REG-DAYS`: `PIC 9(03)` - Regular Days.
    *   `H-TOTAL-DAYS`: `PIC 9(05)` - Total Days.
    *   `H-SSOT`: `PIC 9(02)` - Short Stay Outlier Threshold.
    *   `H-BLEND-RTC`: `PIC 9(02)` - Blend Return Code.
    *   `H-BLEND-FAC`: `PIC 9(01)V9(01)` - Blend Facility Percentage.
    *   `H-BLEND-PPS`: `PIC 9(01)V9(01)` - Blend PPS Percentage.
    *   `H-SS-PAY-AMT`: `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    *   `H-SS-COST`: `PIC 9(07)V9(02)` - Short Stay Cost.
    *   `H-LABOR-PORTION`: `PIC 9(07)V9(06)` - Labor Portion of Payment.
    *   `H-NONLABOR-PORTION`: `PIC 9(07)V9(06)` - Non-Labor Portion of Payment.
    *   `H-FIXED-LOSS-AMT`: `PIC 9(07)V9(02)` - Fixed Loss Amount.
    *   `H-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)` - New Facility Specific Rate.
    *   `H-LOS-RATIO`: `PIC 9(01)V9(05)` - Length of Stay Ratio.

#### 3. Data Structures in LINKAGE SECTION:

*   **`BILL-NEW-DATA`**:  This is the main input record passed *to* the program, containing billing information.  Identical to LTCAL032.
    *   `B-NPI10`:  NPI (National Provider Identifier)
        *   `B-NPI8`: `PIC X(08)` - First 8 bytes of NPI.
        *   `B-NPI-FILLER`: `PIC X(02)` - Filler for NPI.
    *   `B-PROVIDER-NO`: `PIC X(06)` - Provider Number.
    *   `B-PATIENT-STATUS`: `PIC X(02)` - Patient Status.
    *   `B-DRG-CODE`: `PIC X(03)` - DRG (Diagnosis Related Group) Code.
    *   `B-LOS`: `PIC 9(03)` - Length of Stay.
    *   `B-COV-DAYS`: `PIC 9(03)` - Covered Days.
    *   `B-LTR-DAYS`: `PIC 9(02)` - Lifetime Reserve Days.
    *   `B-DISCHARGE-DATE`:  Discharge Date
        *   `B-DISCHG-CC`: `PIC 9(02)` - Century/Check for Discharge Date.
        *   `B-DISCHG-YY`: `PIC 9(02)` - Year of Discharge Date.
        *   `B-DISCHG-MM`: `PIC 9(02)` - Month of Discharge Date.
        *   `B-DISCHG-DD`: `PIC 9(02)` - Day of Discharge Date.
    *   `B-COV-CHARGES`: `PIC 9(07)V9(02)` - Covered Charges.
    *   `B-SPEC-PAY-IND`: `PIC X(01)` - Special Payment Indicator.
    *   `FILLER`: `PIC X(13)` - Unused filler.
*   **`PPS-DATA-ALL`**: This structure is passed *to* the program.  It contains the output data and is used to return the calculated PPS information.  Identical to LTCAL032.
    *   `PPS-RTC`: `PIC 9(02)` - Return Code (PPS-RTC).  Indicates the result of the calculation (e.g., normal payment, outlier, short stay, error).
    *   `PPS-CHRG-THRESHOLD`: `PIC 9(07)V9(02)` - Charge Threshold.
    *   `PPS-DATA`:
        *   `PPS-MSA`: `PIC X(04)` - MSA (Metropolitan Statistical Area) Code.
        *   `PPS-WAGE-INDEX`: `PIC 9(02)V9(04)` - Wage Index.
        *   `PPS-AVG-LOS`: `PIC 9(02)V9(01)` - Average Length of Stay.
        *   `PPS-RELATIVE-WGT`: `PIC 9(01)V9(04)` - Relative Weight.
        *   `PPS-OUTLIER-PAY-AMT`: `PIC 9(07)V9(02)` - Outlier Payment Amount.
        *   `PPS-LOS`: `PIC 9(03)` - Length of Stay.
        *   `PPS-DRG-ADJ-PAY-AMT`: `PIC 9(07)V9(02)` - DRG Adjusted Payment Amount.
        *   `PPS-FED-PAY-AMT`: `PIC 9(07)V9(02)` - Federal Payment Amount.
        *   `PPS-FINAL-PAY-AMT`: `PIC 9(07)V9(02)` - Final Payment Amount.
        *   `PPS-FAC-COSTS`: `PIC 9(07)V9(02)` - Facility Costs.
        *   `PPS-NEW-FAC-SPEC-RATE`: `PIC 9(07)V9(02)` - New Facility Specific Rate.
        *   `PPS-OUTLIER-THRESHOLD`: `PIC 9(07)V9(02)` - Outlier Threshold.
        *   `PPS-SUBM-DRG-CODE`: `PIC X(03)` - Submitted DRG Code.
        *   `PPS-CALC-VERS-CD`: `PIC X(05)` - Calculation Version Code.
        *   `PPS-REG-DAYS-USED`: `PIC 9(03)` - Regular Days Used.
        *   `PPS-LTR-DAYS-USED`: `PIC 9(03)` - Lifetime Reserve Days Used.
        *   `PPS-BLEND-YEAR`: `PIC 9(01)` - Blend Year Indicator.
        *   `PPS-COLA`: `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        *   `FILLER`: `PIC X(04)` - Filler.
    *   `PPS-OTHER-DATA`:
        *   `PPS-NAT-LABOR-PCT`: `PIC 9(01)V9(05)` - National Labor Percentage.
        *   `PPS-NAT-NONLABOR-PCT`: `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        *   `PPS-STD-FED-RATE`: `PIC 9(05)V9(02)` - Standard Federal Rate.
        *   `PPS-BDGT-NEUT-RATE`: `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        *   `FILLER`: `PIC X(20)` - Filler.
    *   `PPS-PC-DATA`:
        *   `PPS-COT-IND`: `PIC X(01)` - Cost Outlier Indicator.
        *   `FILLER`: `PIC X(20)` - Filler.
*   **`PRICER-OPT-VERS-SW`**:  This structure provides information on the version of the pricer.  Identical to LTCAL032.
    *   `PRICER-OPTION-SW`: `PIC X(01)` - Pricer Option Switch.
        *   `ALL-TABLES-PASSED`: `VALUE 'A'` - Indicates all tables are passed (likely the default).
        *   `PROV-RECORD-PASSED`: `VALUE 'P'` - Indicates the provider record is passed.
    *   `PPS-VERSIONS`:
        *   `PPDRV-VERSION`: `PIC X(05)` - Version of the PPDRV program.
*   **`PROV-NEW-HOLD`**:  This structure contains the provider record. It's used to pass provider-specific data *to* the program.  Identical to LTCAL032.
    *   `PROV-NEWREC-HOLD1`:
        *   `P-NEW-NPI10`:  NPI
            *   `P-NEW-NPI8`: `PIC X(08)`
            *   `P-NEW-NPI-FILLER`: `PIC X(02)`
        *   `P-NEW-PROVIDER-NO`:  Provider Number
            *   `P-NEW-STATE`: `PIC 9(02)` - State.
            *   `FILLER`: `PIC X(04)`
        *   `P-NEW-DATE-DATA`:
            *   `P-NEW-EFF-DATE`:  Effective Date
                *   `P-NEW-EFF-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-EFF-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-EFF-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-EFF-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                *   `P-NEW-FY-BEG-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-FY-BEG-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-FY-BEG-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-FY-BEG-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-REPORT-DATE`:  Report Date
                *   `P-NEW-REPORT-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-REPORT-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-REPORT-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-REPORT-DT-DD`: `PIC 9(02)` - Day.
            *   `P-NEW-TERMINATION-DATE`: Termination Date
                *   `P-NEW-TERM-DT-CC`: `PIC 9(02)` - Century/Check.
                *   `P-NEW-TERM-DT-YY`: `PIC 9(02)` - Year.
                *   `P-NEW-TERM-DT-MM`: `PIC 9(02)` - Month.
                *   `P-NEW-TERM-DT-DD`: `PIC 9(02)` - Day.
        *   `P-NEW-WAIVER-CODE`: `PIC X(01)` - Waiver Code.
            *   `P-NEW-WAIVER-STATE`: `VALUE 'Y'` - Waiver State.
        *   `P-NEW-INTER-NO`: `PIC 9(05)` - Internal Number.
        *   `P-NEW-PROVIDER-TYPE`: `PIC X(02)` - Provider Type.
        *   `P-NEW-CURRENT-CENSUS-DIV`: `PIC 9(01)` - Current Census Division.
        *   `P-NEW-CURRENT-DIV` REDEFINES `P-NEW-CURRENT-CENSUS-DIV`: `PIC 9(01)`
        *   `P-NEW-MSA-DATA`:
            *   `P-NEW-CHG-CODE-INDEX`: `PIC X` - Charge Code Index.
            *   `P-NEW-GEO-LOC-MSAX`: `PIC X(04)` - Geographic Location MSA (Metropolitan Statistical Area)
            *   `P-NEW-GEO-LOC-MSA9` REDEFINES `P-NEW-GEO-LOC-MSAX`: `PIC 9(04)`
            *   `P-NEW-WAGE-INDEX-LOC-MSA`: `PIC X(04)` - Wage Index Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA`: `PIC X(04)` - Standard Amount Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES `P-NEW-STAND-AMT-LOC-MSA`:
                *   `P-NEW-RURAL-1ST`:
                    *   `P-NEW-STAND-RURAL`: `PIC XX`
                        *   `P-NEW-STD-RURAL-CHECK`: `VALUE '  '`
                    *   `P-NEW-RURAL-2ND`: `PIC XX`
        *   `P-NEW-SOL-COM-DEP-HOSP-YR`: `PIC XX` - Sole Community Hospital Year.
        *   `P-NEW-LUGAR`: `PIC X` - Lugar.
        *   `P-NEW-TEMP-RELIEF-IND`: `PIC X` - Temporary Relief Indicator.
        *   `P-NEW-FED-PPS-BLEND-IND`: `PIC X` - Federal PPS Blend Indicator.
        *   `FILLER`: `PIC X(05)` - Filler.
    *   `PROV-NEWREC-HOLD2`:
        *   `P-NEW-VARIABLES`:
            *   `P-NEW-FAC-SPEC-RATE`: `PIC 9(05)V9(02)` - Facility Specific Rate.
            *   `P-NEW-COLA`: `PIC 9(01)V9(03)` - Cost of Living Adjustment.
            *   `P-NEW-INTERN-RATIO`: `PIC 9(01)V9(04)` - Intern Ratio.
            *   `P-NEW-BED-SIZE`: `PIC 9(05)` - Bed Size.
            *   `P-NEW-OPER-CSTCHG-RATIO`: `PIC 9(01)V9(03)` - Operating Cost to Charge Ratio.
            *   `P-NEW-CMI`: `PIC 9(01)V9(04)` - CMI (Case Mix Index).
            *   `P-NEW-SSI-RATIO`: `PIC V9(04)` - SSI Ratio.
            *   `P-NEW-MEDICAID-RATIO`: `PIC V9(04)` - Medicaid Ratio.
            *   `P-NEW-PPS-BLEND-YR-IND`: `PIC 9(01)` - PPS Blend Year Indicator.
            *   `P-NEW-PRUF-UPDTE-FACTOR`: `PIC 9(01)V9(05)` - Pruf Update Factor.
            *   `P-NEW-DSH-PERCENT`: `PIC V9(0