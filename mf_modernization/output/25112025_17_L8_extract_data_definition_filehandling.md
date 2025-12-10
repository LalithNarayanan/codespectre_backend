## Analysis of COBOL Programs

### Program: LTCAL032

#### File Access and Description
*   **COPY LTDRG031:**  This is a COBOL `COPY` member. It's included in the program, likely containing data structures or code related to DRG (Diagnosis Related Group) calculations, specific to the 2003 fiscal year.

#### Data Structures in WORKING-STORAGE SECTION
*   **W-STORAGE-REF:**
    *   `PIC X(46)`
    *   Contains the program name and a description "W O R K I N G S T O R A G E".  Used for identification and debugging purposes.
*   **CAL-VERSION:**
    *   `PIC X(05)`
    *   Stores the version of the calculation logic, set to "C03.2".
*   **HOLD-PPS-COMPONENTS:**
    *   This group of data items likely stores intermediate results and components used in the PPS (Prospective Payment System) calculation.
    *   **H-LOS:** `PIC 9(03)` - Length of Stay.
    *   **H-REG-DAYS:** `PIC 9(03)` - Regular Days.
    *   **H-TOTAL-DAYS:** `PIC 9(05)` - Total Days.
    *   **H-SSOT:** `PIC 9(02)` -  Likely represents a threshold related to Short Stay Outlier.
    *   **H-BLEND-RTC:** `PIC 9(02)` - Return Code for Blended Payment.
    *   **H-BLEND-FAC:** `PIC 9(01)V9(01)` -  Facility Blend Percentage.
    *   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - PPS Blend Percentage.
    *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    *   **H-SS-COST:** `PIC 9(07)V9(02)` - Short Stay Cost.
    *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)` - Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Fixed Loss Amount, used in outlier calculations.
    *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.

#### Data Structures in LINKAGE SECTION
*   **BILL-NEW-DATA:**
    *   This structure receives billing data from the calling program.
    *   **B-NPI10:**
        *   **B-NPI8:** `PIC X(08)` - National Provider Identifier (NPI), 8 characters.
        *   **B-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
    *   **B-PROVIDER-NO:** `PIC X(06)` - Provider Number.
    *   **B-PATIENT-STATUS:** `PIC X(02)` - Patient Status.
    *   **B-DRG-CODE:** `PIC X(03)` - DRG Code.
    *   **B-LOS:** `PIC 9(03)` - Length of Stay.
    *   **B-COV-DAYS:** `PIC 9(03)` - Covered Days.
    *   **B-LTR-DAYS:** `PIC 9(02)` - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** `PIC 9(02)` - Discharge Date Century.
        *   **B-DISCHG-YY:** `PIC 9(02)` - Discharge Date Year.
        *   **B-DISCHG-MM:** `PIC 9(02)` - Discharge Date Month.
        *   **B-DISCHG-DD:** `PIC 9(02)` - Discharge Date Day.
    *   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Covered Charges.
    *   **B-SPEC-PAY-IND:** `PIC X(01)` - Special Payment Indicator.
    *   **FILLER:** `PIC X(13)` - Unused space
*   **PPS-DATA-ALL:**
    *   This is the structure to return the calculated PPS data to the calling program.
    *   **PPS-RTC:** `PIC 9(02)` - Return Code (indicates payment type or error).
    *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Charge Threshold for Outlier Payments.
    *   **PPS-DATA:**
        *   **PPS-MSA:** `PIC X(04)` - Metropolitan Statistical Area (MSA) Code.
        *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Wage Index.
        *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Relative Weight (DRG weight).
        *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Outlier Payment Amount.
        *   **PPS-LOS:** `PIC 9(03)` - Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Final Payment Amount.
        *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** `PIC X(05)` - Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** `PIC 9(01)` - Blend Year Indicator.
        *   **PPS-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        *   **FILLER:** `PIC X(04)` - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)` - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)` - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        *   **FILLER:** `PIC X(20)` - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** `PIC X(01)` - Cost Outlier Indicator.
        *   **FILLER:** `PIC X(20)` - Unused space.
*   **PRICER-OPT-VERS-SW:**
    *   This structure seems to be used to pass version information or flags for the pricing options.
    *   **PRICER-OPTION-SW:** `PIC X(01)` -  Switch for Pricer Option
        *   **ALL-TABLES-PASSED:**  `VALUE 'A'` - Indicates all tables are passed.
        *   **PROV-RECORD-PASSED:** `VALUE 'P'` - Indicates provider record is passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** `PIC X(05)` - Version of the PPDRV program.
*   **PROV-NEW-HOLD:**
    *   This structure passes provider-specific information.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** `PIC X(08)` - New NPI, 8 characters.
            *   **P-NEW-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:** `PIC X(06)` - New Provider Number.
        *   **P-NEW-STATE:** `PIC 9(02)` - New State.
            *   **FILLER:** `PIC X(04)` - Unused space.
        *   **P-NEW-DATE-DATA:** Date information
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:** `PIC 9(02)` - Effective Date Century.
                *   **P-NEW-EFF-DT-YY:** `PIC 9(02)` - Effective Date Year.
                *   **P-NEW-EFF-DT-MM:** `PIC 9(02)` - Effective Date Month.
                *   **P-NEW-EFF-DT-DD:** `PIC 9(02)` - Effective Date Day.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)` - Fiscal Year Begin Date Century.
                *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)` - Fiscal Year Begin Date Year.
                *   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)` - Fiscal Year Begin Date Month.
                *   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)` - Fiscal Year Begin Date Day.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:** `PIC 9(02)` - Report Date Century.
                *   **P-NEW-REPORT-DT-YY:** `PIC 9(02)` - Report Date Year.
                *   **P-NEW-REPORT-DT-MM:** `PIC 9(02)` - Report Date Month.
                *   **P-NEW-REPORT-DT-DD:** `PIC 9(02)` - Report Date Day.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:** `PIC 9(02)` - Termination Date Century.
                *   **P-NEW-TERM-DT-YY:** `PIC 9(02)` - Termination Date Year.
                *   **P-NEW-TERM-DT-MM:** `PIC 9(02)` - Termination Date Month.
                *   **P-NEW-TERM-DT-DD:** `PIC 9(02)` - Termination Date Day.
        *   **P-NEW-WAIVER-CODE:** `PIC X(01)` - Waiver Code.
            *   **P-NEW-WAIVER-STATE:** `VALUE 'Y'` - Waiver State.
        *   **P-NEW-INTER-NO:** `PIC 9(05)` - Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** `PIC X(02)` - Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current Census Division.
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current Division.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** `PIC X` - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** `PIC X(04)` - Geographic Location MSA.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** `PIC 9(04)` - Geographic Location MSA (numeric).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04)` - Wage Index Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04)` - Standard Amount Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** `PIC XX` - Standard Rural.
                    *   **P-NEW-STD-RURAL-CHECK:** `VALUE '  '` - Standard Rural Check.
                *   **P-NEW-RURAL-2ND:** `PIC XX` - Rural 2nd.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX` - Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** `PIC X` - Lugar.
        *   **P-NEW-TEMP-RELIEF-IND:** `PIC X` - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** `PIC X` - Federal PPS Blend Indicator.
        *   **FILLER:** `PIC X(05)` - Unused space.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.
            *   **P-NEW-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)` - Intern Ratio.
            *   **P-NEW-BED-SIZE:** `PIC 9(05)` - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)` - Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** `PIC 9(01)V9(04)` - Case Mix Index.
            *   **P-NEW-SSI-RATIO:** `V9(04)` - SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO:** `V9(04)` - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)` - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)` - Pruf Update Factor.
            *   **P-NEW-DSH-PERCENT:** `V9(04)` - DSH Percentage.
            *   **P-NEW-FYE-DATE:** `PIC X(08)` - Fiscal Year End Date.
        *   **FILLER:** `PIC X(23)` - Unused space.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** `PIC 9(04)V99` - Passed Amount Capital.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** `PIC 9(04)V99` - Passed Amount Direct Medical Education.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** `PIC 9(04)V99` - Passed Amount Organ Acquisition.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** `PIC 9(04)V99` - Passed Amount Plus Miscellaneous.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** `PIC X` - Capital PPS Pay Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** `PIC 9(04)V99` - Capital Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** `PIC 9(04)V99` - Capital Old HARM Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** `PIC 9(01)V9999` - Capital New HARM Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** `PIC 9V999` - Capital Cost to Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** `PIC X` - Capital New Hospital.
            *   **P-NEW-CAPI-IME:** `PIC 9V9999` - Capital IME.
            *   **P-NEW-CAPI-EXCEPTIONS:** `PIC 9(04)V99` - Capital Exceptions.
        *   **FILLER:** `PIC X(22)` - Unused space.
*   **WAGE-NEW-INDEX-RECORD:**
    *   This structure receives wage index data.
    *   **W-MSA:** `PIC X(4)` - MSA Code.
    *   **W-EFF-DATE:** `PIC X(8)` - Effective Date.
    *   **W-WAGE-INDEX1:** `PIC S9(02)V9(04)` - Wage Index 1.
    *   **W-WAGE-INDEX2:** `PIC S9(02)V9(04)` - Wage Index 2.
    *   **W-WAGE-INDEX3:** `PIC S9(02)V9(04)` - Wage Index 3.

### Program: LTCAL042

#### File Access and Description
*   **COPY LTDRG031:** This is a COBOL `COPY` member. It's included in the program, likely containing data structures or code related to DRG (Diagnosis Related Group) calculations, specific to the 2003 fiscal year.

#### Data Structures in WORKING-STORAGE SECTION
*   **W-STORAGE-REF:**
    *   `PIC X(46)`
    *   Contains the program name and a description "W O R K I N G S T O R A G E". Used for identification and debugging purposes.
*   **CAL-VERSION:**
    *   `PIC X(05)`
    *   Stores the version of the calculation logic, set to "C04.2".
*   **HOLD-PPS-COMPONENTS:**
    *   This group of data items likely stores intermediate results and components used in the PPS (Prospective Payment System) calculation.
    *   **H-LOS:** `PIC 9(03)` - Length of Stay.
    *   **H-REG-DAYS:** `PIC 9(03)` - Regular Days.
    *   **H-TOTAL-DAYS:** `PIC 9(05)` - Total Days.
    *   **H-SSOT:** `PIC 9(02)` -  Likely represents a threshold related to Short Stay Outlier.
    *   **H-BLEND-RTC:** `PIC 9(02)` - Return Code for Blended Payment.
    *   **H-BLEND-FAC:** `PIC 9(01)V9(01)` -  Facility Blend Percentage.
    *   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - PPS Blend Percentage.
    *   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    *   **H-SS-COST:** `PIC 9(07)V9(02)` - Short Stay Cost.
    *   **H-LABOR-PORTION:** `PIC 9(07)V9(06)` - Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Fixed Loss Amount, used in outlier calculations.
    *   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.
    *   **H-LOS-RATIO:** `PIC 9(01)V9(05)` - Length of Stay Ratio.

#### Data Structures in LINKAGE SECTION
*   **BILL-NEW-DATA:**
    *   This structure receives billing data from the calling program.
    *   **B-NPI10:**
        *   **B-NPI8:** `PIC X(08)` - National Provider Identifier (NPI), 8 characters.
        *   **B-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
    *   **B-PROVIDER-NO:** `PIC X(06)` - Provider Number.
    *   **B-PATIENT-STATUS:** `PIC X(02)` - Patient Status.
    *   **B-DRG-CODE:** `PIC X(03)` - DRG Code.
    *   **B-LOS:** `PIC 9(03)` - Length of Stay.
    *   **B-COV-DAYS:** `PIC 9(03)` - Covered Days.
    *   **B-LTR-DAYS:** `PIC 9(02)` - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** `PIC 9(02)` - Discharge Date Century.
        *   **B-DISCHG-YY:** `PIC 9(02)` - Discharge Date Year.
        *   **B-DISCHG-MM:** `PIC 9(02)` - Discharge Date Month.
        *   **B-DISCHG-DD:** `PIC 9(02)` - Discharge Date Day.
    *   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Covered Charges.
    *   **B-SPEC-PAY-IND:** `PIC X(01)` - Special Payment Indicator.
    *   **FILLER:** `PIC X(13)` - Unused space
*   **PPS-DATA-ALL:**
    *   This is the structure to return the calculated PPS data to the calling program.
    *   **PPS-RTC:** `PIC 9(02)` - Return Code (indicates payment type or error).
    *   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Charge Threshold for Outlier Payments.
    *   **PPS-DATA:**
        *   **PPS-MSA:** `PIC X(04)` - Metropolitan Statistical Area (MSA) Code.
        *   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Wage Index.
        *   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Relative Weight (DRG weight).
        *   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Outlier Payment Amount.
        *   **PPS-LOS:** `PIC 9(03)` - Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Final Payment Amount.
        *   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** `PIC X(05)` - Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** `PIC 9(01)` - Blend Year Indicator.
        *   **PPS-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        *   **FILLER:** `PIC X(04)` - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)` - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)` - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        *   **FILLER:** `PIC X(20)` - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** `PIC X(01)` - Cost Outlier Indicator.
        *   **FILLER:** `PIC X(20)` - Unused space.
*   **PRICER-OPT-VERS-SW:**
    *   This structure seems to be used to pass version information or flags for the pricing options.
    *   **PRICER-OPTION-SW:** `PIC X(01)` -  Switch for Pricer Option
        *   **ALL-TABLES-PASSED:**  `VALUE 'A'` - Indicates all tables are passed.
        *   **PROV-RECORD-PASSED:** `VALUE 'P'` - Indicates provider record is passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** `PIC X(05)` - Version of the PPDRV program.
*   **PROV-NEW-HOLD:**
    *   This structure passes provider-specific information.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** `PIC X(08)` - New NPI, 8 characters.
            *   **P-NEW-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:** `PIC X(06)` - New Provider Number.
        *   **P-NEW-STATE:** `PIC 9(02)` - New State.
            *   **FILLER:** `PIC X(04)` - Unused space.
        *   **P-NEW-DATE-DATA:** Date information
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:** `PIC 9(02)` - Effective Date Century.
                *   **P-NEW-EFF-DT-YY:** `PIC 9(02)` - Effective Date Year.
                *   **P-NEW-EFF-DT-MM:** `PIC 9(02)` - Effective Date Month.
                *   **P-NEW-EFF-DT-DD:** `PIC 9(02)` - Effective Date Day.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)` - Fiscal Year Begin Date Century.
                *   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)` - Fiscal Year Begin Date Year.
                *   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)` - Fiscal Year Begin Date Month.
                *   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)` - Fiscal Year Begin Date Day.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:** `PIC 9(02)` - Report Date Century.
                *   **P-NEW-REPORT-DT-YY:** `PIC 9(02)` - Report Date Year.
                *   **P-NEW-REPORT-DT-MM:** `PIC 9(02)` - Report Date Month.
                *   **P-NEW-REPORT-DT-DD:** `PIC 9(02)` - Report Date Day.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:** `PIC 9(02)` - Termination Date Century.
                *   **P-NEW-TERM-DT-YY:** `PIC 9(02)` - Termination Date Year.
                *   **P-NEW-TERM-DT-MM:** `PIC 9(02)` - Termination Date Month.
                *   **P-NEW-TERM-DT-DD:** `PIC 9(02)` - Termination Date Day.
        *   **P-NEW-WAIVER-CODE:** `PIC X(01)` - Waiver Code.
            *   **P-NEW-WAIVER-STATE:** `VALUE 'Y'` - Waiver State.
        *   **P-NEW-INTER-NO:** `PIC 9(05)` - Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** `PIC X(02)` - Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current Census Division.
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current Division.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** `PIC X` - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** `PIC X(04)` - Geographic Location MSA.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** `PIC 9(04)` - Geographic Location MSA (numeric).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04)` - Wage Index Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04)` - Standard Amount Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** `PIC XX` - Standard Rural.
                    *   **P-NEW-STD-RURAL-CHECK:** `VALUE '  '` - Standard Rural Check.
                *   **P-NEW-RURAL-2ND:** `PIC XX` - Rural 2nd.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX` - Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** `PIC X` - Lugar.
        *   **P-NEW-TEMP-RELIEF-IND:** `PIC X` - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** `PIC X` - Federal PPS Blend Indicator.
        *   **FILLER:** `PIC X(05)` - Unused space.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.
            *   **P-NEW-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)` - Intern Ratio.
            *   **P-NEW-BED-SIZE:** `PIC 9(05)` - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)` - Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** `PIC 9(01)V9(04)` - Case Mix Index.
            *   **P-NEW-SSI-RATIO:** `V9(04)` - SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO:** `V9(04)` - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)` - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)` - Pruf Update Factor.
            *   **P-NEW-DSH-PERCENT:** `V9(04)` - DSH Percentage.
            *   **P-NEW