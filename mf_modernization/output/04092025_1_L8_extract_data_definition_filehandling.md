Here's an analysis of the COBOL programs, detailing the files accessed, data structures, and their descriptions:

## LTCAL032

**Files Accessed:**

*   **LTDRG031:** This is included via a `COPY` statement.  It's likely a table containing DRG (Diagnosis Related Group) codes and associated data like relative weights and average length of stay.

**Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:**  PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'. -  A descriptive string, likely for debugging or identification purposes.
*   **CAL-VERSION:** PIC X(05) VALUE 'C03.2'. - Indicates the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS:** This is a group of data items used to store various components related to the Prospective Payment System (PPS) calculations.
    *   **H-LOS:** PIC 9(03). - Length of Stay (in days).
    *   **H-REG-DAYS:** PIC 9(03). - Regular Days (covered days - LTR days).
    *   **H-TOTAL-DAYS:** PIC 9(05). - Total Days (regular days + LTR days).
    *   **H-SSOT:** PIC 9(02). - Short Stay Outlier Threshold (calculated).
    *   **H-BLEND-RTC:** PIC 9(02). - Return Code related to blend payment.
    *   **H-BLEND-FAC:** PIC 9(01)V9(01). - Blend Factor for Facility rate (e.g., 0.8 for 80%).
    *   **H-BLEND-PPS:** PIC 9(01)V9(01). - Blend Factor for PPS payment (e.g., 0.2 for 20%).
    *   **H-SS-PAY-AMT:** PIC 9(07)V9(02). - Short Stay Payment Amount.
    *   **H-SS-COST:** PIC 9(07)V9(02). - Short Stay Cost.
    *   **H-LABOR-PORTION:** PIC 9(07)V9(06). - Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06). - Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02). - Fixed Loss Amount for outlier calculations.
    *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02). - New Facility Specific Rate.

**Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:** This is the main input data structure, representing the bill information passed to the subroutine.
    *   **B-NPI10:**
        *   **B-NPI8:** PIC X(08). - National Provider Identifier (NPI) - first 8 characters.
        *   **B-NPI-FILLER:** PIC X(02). - Filler for NPI.
    *   **B-PROVIDER-NO:** PIC X(06). - Provider Number.
    *   **B-PATIENT-STATUS:** PIC X(02). - Patient Status Code.
    *   **B-DRG-CODE:** PIC X(03). - DRG Code (Diagnosis Related Group).
    *   **B-LOS:** PIC 9(03). - Length of Stay (in days).
    *   **B-COV-DAYS:** PIC 9(03). - Covered Days.
    *   **B-LTR-DAYS:** PIC 9(02). - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** PIC 9(02). - Discharge Date - Century.
        *   **B-DISCHG-YY:** PIC 9(02). - Discharge Date - Year.
        *   **B-DISCHG-MM:** PIC 9(02). - Discharge Date - Month.
        *   **B-DISCHG-DD:** PIC 9(02). - Discharge Date - Day.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02). - Covered Charges.
    *   **B-SPEC-PAY-IND:** PIC X(01). - Special Payment Indicator (e.g., for specific payment arrangements).
    *   **FILLER:** PIC X(13). - Unused space.
*   **PPS-DATA-ALL:** This is the main output data structure, containing the calculated PPS results.
    *   **PPS-RTC:** PIC 9(02). - Return Code (indicates payment status or reason for rejection).
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02). - Charge Threshold for Outlier Payments.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04). - Metropolitan Statistical Area (MSA) code.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04). - Wage Index.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01). - Average Length of Stay (for the DRG).
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04). - Relative Weight (for the DRG).
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02). - Outlier Payment Amount.
        *   **PPS-LOS:** PIC 9(03). - Length of Stay (from the input).
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02). - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02). - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02). - Final Payment Amount.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02). - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02). - New Facility Specific Rate (passed back).
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02). - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03). - Submitted DRG Code (passed back).
        *   **PPS-CALC-VERS-CD:** PIC X(05). - Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** PIC 9(03). - Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03). - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** PIC 9(01). - Blend Year Indicator.
        *   **PPS-COLA:** PIC 9(01)V9(03). - Cost of Living Adjustment.
        *   **FILLER:** PIC X(04). - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05). - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05). - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02). - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03). - Budget Neutrality Rate.
        *   **FILLER:** PIC X(20). - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01). - Cost Outlier Indicator.
        *   **FILLER:** PIC X(20). - Unused space.
*   **PRICER-OPT-VERS-SW:**
    *   **PRICER-OPTION-SW:** PIC X(01). -  Switch for Pricer Options (e.g., to indicate if all tables are passed).
        *   **ALL-TABLES-PASSED:** VALUE 'A'. - Condition: All tables are passed.
        *   **PROV-RECORD-PASSED:** VALUE 'P'. - Condition: Provider record is passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05). - Version of the PPDRV (likely a table or program).
*   **PROV-NEW-HOLD:**  This structure contains the provider-specific information.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08). - New NPI (first 8 characters).
            *   **P-NEW-NPI-FILLER:** PIC X(02). - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02). - State code.
            *   **FILLER:** PIC X(04). - Unused space.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:** PIC 9(02). - Effective Date - Century.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02). - Effective Date - Year.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02). - Effective Date - Month.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02). - Effective Date - Day.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02). - Fiscal Year Begin Date - Century.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02). - Fiscal Year Begin Date - Year.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02). - Fiscal Year Begin Date - Month.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02). - Fiscal Year Begin Date - Day.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02). - Report Date - Century.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02). - Report Date - Year.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02). - Report Date - Month.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02). - Report Date - Day.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:** PIC 9(02). - Termination Date - Century.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02). - Termination Date - Year.
                *   **P-NEW-TERM-DT-MM:** PIC 9(02). - Termination Date - Month.
                *   **P-NEW-TERM-DT-DD:** PIC 9(02). - Termination Date - Day.
        *   **P-NEW-WAIVER-CODE:** PIC X(01). - Waiver Code.
            *   **P-NEW-WAIVER-STATE:** VALUE 'Y'. - Condition: Waiver State is 'Y'.
        *   **P-NEW-INTER-NO:** PIC 9(05). - Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** PIC X(02). - Provider Type Code.
        *   **P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01). - Current Census Division (used for redefinition).
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01). - Redefinition of the above.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** PIC X. - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** PIC X(04) JUST RIGHT. - Geographic Location MSA (Metropolitan Statistical Area) - right justified.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** PIC 9(04). - Numeric Redefinition of the above.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** PIC X(04) JUST RIGHT. - Wage Index Location MSA - right justified.
            *   **P-NEW-STAND-AMT-LOC-MSA:** PIC X(04) JUST RIGHT. - Standard Amount Location MSA - right justified.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** PIC XX. - Standard Rural Value.
                        *   **P-NEW-STD-RURAL-CHECK:** VALUE '  '. - Condition: Standard Rural Check is spaces.
                    *   **P-NEW-RURAL-2ND:** PIC XX. - Second Rural Value.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** PIC XX. - Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** PIC X. - Lugar Indicator.
        *   **P-NEW-TEMP-RELIEF-IND:** PIC X. - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** PIC X. - Federal PPS Blend Indicator.
        *   **FILLER:** PIC X(05). - Unused space.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02). - Facility Specific Rate.
            *   **P-NEW-COLA:** PIC 9(01)V9(03). - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** PIC 9(01)V9(04). - Intern Ratio.
            *   **P-NEW-BED-SIZE:** PIC 9(05). - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** PIC 9(01)V9(03). - Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** PIC 9(01)V9(04). - Case Mix Index.
            *   **P-NEW-SSI-RATIO:** PIC V9(04). - Supplemental Security Income Ratio.
            *   **P-NEW-MEDICAID-RATIO:** PIC V9(04). - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** PIC 9(01). - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** PIC 9(01)V9(05). - Pruf Update Factor.
            *   **P-NEW-DSH-PERCENT:** PIC V9(04). - Disproportionate Share Hospital (DSH) Percent.
            *   **P-NEW-FYE-DATE:** PIC X(08). - Fiscal Year End Date.
        *   **FILLER:** PIC X(23). - Unused space.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** PIC 9(04)V99. - Passed Amount - Capital.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** PIC 9(04)V99. - Passed Amount - Direct Medical Education.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** PIC 9(04)V99. - Passed Amount - Organ Acquisition.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** PIC 9(04)V99. - Passed Amount - Plus Miscellaneous.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** PIC X. - Capital PPS Payment Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** PIC 9(04)V99. - Capital Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** PIC 9(04)V99. - Capital Old Harm Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** PIC 9(01)V9999. - Capital New Harm Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** PIC 9V999. - Capital Cost to Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** PIC X. - Capital New Hospital Indicator.
            *   **P-NEW-CAPI-IME:** PIC 9V9999. - Capital IME (Indirect Medical Education).
            *   **P-NEW-CAPI-EXCEPTIONS:** PIC 9(04)V99. - Capital Exceptions.
        *   **FILLER:** PIC X(22). - Unused space.
*   **WAGE-NEW-INDEX-RECORD:** This structure contains the wage index information.
    *   **W-MSA:** PIC X(4). - MSA code.
    *   **W-EFF-DATE:** PIC X(8). - Effective Date.
    *   **W-WAGE-INDEX1:** PIC S9(02)V9(04). - Wage Index 1.
    *   **W-WAGE-INDEX2:** PIC S9(02)V9(04). - Wage Index 2.
    *   **W-WAGE-INDEX3:** PIC S9(02)V9(04). - Wage Index 3.

## LTCAL042

**Files Accessed:**

*   **LTDRG031:**  This is included via a `COPY` statement.  It's likely a table containing DRG (Diagnosis Related Group) codes and associated data like relative weights and average length of stay.

**Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:**  PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'. -  A descriptive string, likely for debugging or identification purposes.
*   **CAL-VERSION:** PIC X(05) VALUE 'C04.2'. - Indicates the version of the calculation logic.
*   **HOLD-PPS-COMPONENTS:** This is a group of data items used to store various components related to the Prospective Payment System (PPS) calculations.
    *   **H-LOS:** PIC 9(03). - Length of Stay (in days).
    *   **H-REG-DAYS:** PIC 9(03). - Regular Days (covered days - LTR days).
    *   **H-TOTAL-DAYS:** PIC 9(05). - Total Days (regular days + LTR days).
    *   **H-SSOT:** PIC 9(02). - Short Stay Outlier Threshold (calculated).
    *   **H-BLEND-RTC:** PIC 9(02). - Return Code related to blend payment.
    *   **H-BLEND-FAC:** PIC 9(01)V9(01). - Blend Factor for Facility rate (e.g., 0.8 for 80%).
    *   **H-BLEND-PPS:** PIC 9(01)V9(01). - Blend Factor for PPS payment (e.g., 0.2 for 20%).
    *   **H-SS-PAY-AMT:** PIC 9(07)V9(02). - Short Stay Payment Amount.
    *   **H-SS-COST:** PIC 9(07)V9(02). - Short Stay Cost.
    *   **H-LABOR-PORTION:** PIC 9(07)V9(06). - Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06). - Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02). - Fixed Loss Amount for outlier calculations.
    *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02). - New Facility Specific Rate.
    *   **H-LOS-RATIO:** PIC 9(01)V9(05). - Length of Stay Ratio.

**Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:** This is the main input data structure, representing the bill information passed to the subroutine.  (Same as LTCAL032)
    *   **B-NPI10:**
        *   **B-NPI8:** PIC X(08). - National Provider Identifier (NPI) - first 8 characters.
        *   **B-NPI-FILLER:** PIC X(02). - Filler for NPI.
    *   **B-PROVIDER-NO:** PIC X(06). - Provider Number.
    *   **B-PATIENT-STATUS:** PIC X(02). - Patient Status Code.
    *   **B-DRG-CODE:** PIC X(03). - DRG Code (Diagnosis Related Group).
    *   **B-LOS:** PIC 9(03). - Length of Stay (in days).
    *   **B-COV-DAYS:** PIC 9(03). - Covered Days.
    *   **B-LTR-DAYS:** PIC 9(02). - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** PIC 9(02). - Discharge Date - Century.
        *   **B-DISCHG-YY:** PIC 9(02). - Discharge Date - Year.
        *   **B-DISCHG-MM:** PIC 9(02). - Discharge Date - Month.
        *   **B-DISCHG-DD:** PIC 9(02). - Discharge Date - Day.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02). - Covered Charges.
    *   **B-SPEC-PAY-IND:** PIC X(01). - Special Payment Indicator (e.g., for specific payment arrangements).
    *   **FILLER:** PIC X(13). - Unused space.
*   **PPS-DATA-ALL:** This is the main output data structure, containing the calculated PPS results. (Same as LTCAL032)
    *   **PPS-RTC:** PIC 9(02). - Return Code (indicates payment status or reason for rejection).
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02). - Charge Threshold for Outlier Payments.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04). - Metropolitan Statistical Area (MSA) code.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04). - Wage Index.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01). - Average Length of Stay (for the DRG).
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04). - Relative Weight (for the DRG).
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02). - Outlier Payment Amount.
        *   **PPS-LOS:** PIC 9(03). - Length of Stay (from the input).
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02). - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02). - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02). - Final Payment Amount.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02). - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02). - New Facility Specific Rate (passed back).
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02). - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03). - Submitted DRG Code (passed back).
        *   **PPS-CALC-VERS-CD:** PIC X(05). - Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** PIC 9(03). - Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03). - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** PIC 9(01). - Blend Year Indicator.
        *   **PPS-COLA:** PIC 9(01)V9(03). - Cost of Living Adjustment.
        *   **FILLER:** PIC X(04). - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05). - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05). - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02). - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03). - Budget Neutrality Rate.
        *   **FILLER:** PIC X(20). - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01). - Cost Outlier Indicator.
        *   **FILLER:** PIC X(20). - Unused space.
*   **PRICER-OPT-VERS-SW:** (Same as LTCAL032)
    *   **PRICER-OPTION-SW:** PIC X(01). -  Switch for Pricer Options (e.g., to indicate if all tables are passed).
        *   **ALL-TABLES-PASSED:** VALUE 'A'. - Condition: All tables are passed.
        *   **PROV-RECORD-PASSED:** VALUE 'P'. - Condition: Provider record is passed.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05). - Version of the PPDRV (likely a table or program).
*   **PROV-NEW-HOLD:** (Same as LTCAL032)  This structure contains the provider-specific information.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08). - New NPI (first 8 characters).
            *   **P-NEW-NPI-FILLER:** PIC X(02). - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02). - State code.
            *   **FILLER:** PIC X(04). - Unused space.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:**
                *   **P-NEW-EFF-DT-CC:** PIC 9(02). - Effective Date - Century.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02). - Effective Date - Year.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02). - Effective Date - Month.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02). - Effective Date - Day.
            *   **P-NEW-FY-BEGIN-DATE:**
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02). - Fiscal Year Begin Date - Century.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02). - Fiscal Year Begin Date - Year.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02). - Fiscal Year Begin Date - Month.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02). - Fiscal Year Begin Date - Day.
            *   **P-NEW-REPORT-DATE:**
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02). - Report Date - Century.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02). - Report Date - Year.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02). - Report Date - Month.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02). - Report Date - Day.
            *   **P-NEW-TERMINATION-DATE:**
                *   **P-NEW-TERM-DT-CC:** PIC 9(02). - Termination Date - Century.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02). - Termination Date - Year.
                *   **P-NEW-TERM-DT-MM:** PIC 9(02). - Termination Date - Month.
                *   **P-NEW-TERM-DT-DD:** PIC 9(02). - Termination Date - Day.
        *   **P-NEW-WAIVER-CODE:** PIC X(01). - Waiver Code.
            *   **P-NEW-WAIVER-STATE:** VALUE 'Y'. - Condition: Waiver State is 'Y'.
        *   **P-NEW-INTER-NO:** PIC 9(05). - Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** PIC X(02). - Provider Type Code.
        *   **P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01). - Current Census Division (used for redefinition).
        *   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01). - Redefinition of the above.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** PIC X. - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** PIC X(04) JUST RIGHT. - Geographic Location MSA (Metropolitan Statistical Area) - right justified.
            *   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** PIC 9(04). - Numeric Redefinition of the above.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** PIC X(04) JUST RIGHT. - Wage Index Location MSA - right justified.
            *   **P-NEW-STAND-AMT-LOC-MSA:** PIC X(04) JUST RIGHT. - Standard Amount Location MSA - right justified.
            *   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** PIC XX. - Standard Rural Value.
                        *   **P-NEW-STD-RURAL-CHECK:** VALUE '  '. - Condition: Standard Rural Check is spaces.
                    *   **P-NEW-RURAL-2ND:** PIC XX. - Second Rural Value.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** PIC XX. - Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** PIC X. - Lugar Indicator.
        *   **P-NEW-TEMP-RELIEF-IND:** PIC X. - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** PIC X. - Federal PPS Blend Indicator.
        *   **FILLER:** PIC X(05). - Unused space.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02). - Facility Specific Rate.
            *   **P-NEW-COLA:** PIC 9(01)V9(03). - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** PIC 9(01)V9(04). - Intern Ratio.
            *   **P-NEW-BED-SIZE:** PIC 9(05). - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** PIC 9(01)V9(03). - Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** PIC 9(01)V9(04). - Case Mix Index.
            *   **P-NEW-SSI-RATIO:** PIC V9(04). - Supplemental Security Income Ratio.
            *   **P-NEW-MEDICAID-RATIO:** PIC V9(04). - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** PIC 9(01). - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** PIC 9(01)V9(05). - Pruf Update Factor.
            *