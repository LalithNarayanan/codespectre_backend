Here's the analysis of each COBOL program:

## Program: LTCAL032

### Files Accessed:

*   **LTDRG031**: This is a `COPY` statement, indicating that the contents of `LTDRG031` are included in this program. Based on the context of the `SEARCH ALL WWM-ENTRY` statement later in the code, `LTDRG031` likely defines a table (likely a DRG lookup table) that is used for processing. The actual file access or loading mechanism for this table is not explicitly defined within this program's `FILE-CONTROL` section, suggesting it might be loaded into memory via other means or is a static table definition.

### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF**:
    *   **Description**: A PIC X(46) field used to hold a descriptive string for the working storage section.
*   **CAL-VERSION**:
    *   **Description**: A PIC X(05) field holding the version of the calling program (LTCAL032), which is 'C03.2'.
*   **HOLD-PPS-COMPONENTS**:
    *   **Description**: A group item used to hold intermediate calculation results and components related to PPS (Prospective Payment System).
    *   **H-LOS**: PIC 9(03) - Length of Stay.
    *   **H-REG-DAYS**: PIC 9(03) - Regular Days.
    *   **H-TOTAL-DAYS**: PIC 9(05) - Total Days.
    *   **H-SSOT**: PIC 9(02) - Short Stay Outlier Threshold.
    *   **H-BLEND-RTC**: PIC 9(02) - Blend Return Code.
    *   **H-BLEND-FAC**: PIC 9(01)V9(01) - Blend Facility Rate component.
    *   **H-BLEND-PPS**: PIC 9(01)V9(01) - Blend PPS component.
    *   **H-SS-PAY-AMT**: PIC 9(07)V9(02) - Short Stay Payment Amount.
    *   **H-SS-COST**: PIC 9(07)V9(02) - Short Stay Cost.
    *   **H-LABOR-PORTION**: PIC 9(07)V9(06) - Labor Portion calculation.
    *   **H-NONLABOR-PORTION**: PIC 9(07)V9(06) - Non-Labor Portion calculation.
    *   **H-FIXED-LOSS-AMT**: PIC 9(07)V9(02) - Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE**: PIC 9(05)V9(02) - New Facility Specific Rate.

### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA**:
    *   **Description**: A group item representing the bill record passed from the calling program.
    *   **B-NPI10**:
        *   **B-NPI8**: PIC X(08) - National Provider Identifier (first 8 characters).
        *   **B-NPI-FILLER**: PIC X(02) - Filler for NPI.
    *   **B-PROVIDER-NO**: PIC X(06) - Provider Number.
    *   **B-PATIENT-STATUS**: PIC X(02) - Patient Status.
    *   **B-DRG-CODE**: PIC X(03) - Diagnosis Related Group Code.
    *   **B-LOS**: PIC 9(03) - Length of Stay.
    *   **B-COV-DAYS**: PIC 9(03) - Covered Days.
    *   **B-LTR-DAYS**: PIC 9(02) - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: PIC 9(02) - Discharge Date Century.
        *   **B-DISCHG-YY**: PIC 9(02) - Discharge Date Year.
        *   **B-DISCHG-MM**: PIC 9(02) - Discharge Date Month.
        *   **B-DISCHG-DD**: PIC 9(02) - Discharge Date Day.
    *   **B-COV-CHARGES**: PIC 9(07)V9(02) - Covered Charges.
    *   **B-SPEC-PAY-IND**: PIC X(01) - Special Payment Indicator.
    *   **FILLER**: PIC X(13) - Unused space.
*   **PPS-DATA-ALL**:
    *   **Description**: A group item containing all PPS (Prospective Payment System) related data, both input and output.
    *   **PPS-RTC**: PIC 9(02) - Return Code (indicates payment status or error).
    *   **PPS-CHRG-THRESHOLD**: PIC 9(07)V9(02) - Charge Threshold.
    *   **PPS-DATA**:
        *   **PPS-MSA**: PIC X(04) - Medical Service Area.
        *   **PPS-WAGE-INDEX**: PIC 9(02)V9(04) - Wage Index.
        *   **PPS-AVG-LOS**: PIC 9(02)V9(01) - Average Length of Stay.
        *   **PPS-RELATIVE-WGT**: PIC 9(01)V9(04) - Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT**: PIC 9(07)V9(02) - Outlier Payment Amount.
        *   **PPS-LOS**: PIC 9(03) - Length of Stay (used for output).
        *   **PPS-DRG-ADJ-PAY-AMT**: PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT**: PIC 9(07)V9(02) - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT**: PIC 9(07)V9(02) - Final Payment Amount.
        *   **PPS-FAC-COSTS**: PIC 9(07)V9(02) - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE**: PIC 9(07)V9(02) - New Facility Specific Rate (output).
        *   **PPS-OUTLIER-THRESHOLD**: PIC 9(07)V9(02) - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE**: PIC X(03) - Submitted DRG Code.
        *   **PPS-CALC-VERS-CD**: PIC X(05) - Calculation Version Code.
        *   **PPS-REG-DAYS-USED**: PIC 9(03) - Regular Days Used.
        *   **PPS-LTR-DAYS-USED**: PIC 9(03) - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR**: PIC 9(01) - Blend Year Indicator.
        *   **PPS-COLA**: PIC 9(01)V9(03) - Cost of Living Adjustment.
        *   **FILLER**: PIC X(04) - Unused space.
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: PIC 9(01)V9(05) - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT**: PIC 9(01)V9(05) - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE**: PIC 9(05)V9(02) - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE**: PIC 9(01)V9(03) - Budget Neutrality Rate.
        *   **FILLER**: PIC X(20) - Unused space.
    *   **PPS-PC-DATA**:
        *   **PPS-COT-IND**: PIC X(01) - Cost Outlier Indicator.
        *   **FILLER**: PIC X(20) - Unused space.
*   **PRICER-OPT-VERS-SW**:
    *   **Description**: A group item related to pricer option versions and switches.
    *   **PRICER-OPTION-SW**: PIC X(01) - Pricer Option Switch.
        *   **ALL-TABLES-PASSED**: 88 level for 'A'.
        *   **PROV-RECORD-PASSED**: 88 level for 'P'.
    *   **PPS-VERSIONS**:
        *   **PPDRV-VERSION**: PIC X(05) - Pricer DRG Version.
*   **PROV-NEW-HOLD**:
    *   **Description**: A group item holding provider-specific data.
    *   **PROV-NEWREC-HOLD1**:
        *   **P-NEW-NPI10**:
            *   **P-NEW-NPI8**: PIC X(08) - Provider NPI (first 8 chars).
            *   **P-NEW-NPI-FILLER**: PIC X(02) - NPI Filler.
        *   **P-NEW-PROVIDER-NO**:
            *   **P-NEW-STATE**: PIC 9(02) - Provider State.
            *   **FILLER**: PIC X(04) - Filler.
        *   **P-NEW-DATE-DATA**:
            *   **P-NEW-EFF-DATE**: Effective Date (CCYYMMDD).
            *   **P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date (CCYYMMDD).
            *   **P-NEW-REPORT-DATE**: Report Date (CCYYMMDD).
            *   **P-NEW-TERMINATION-DATE**: Termination Date (CCYYMMDD).
        *   **P-NEW-WAIVER-CODE**: PIC X(01) - Waiver Code.
            *   **P-NEW-WAIVER-STATE**: 88 level for 'Y'.
        *   **P-NEW-INTER-NO**: PIC 9(05) - Inter Number.
        *   **P-NEW-PROVIDER-TYPE**: PIC X(02) - Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV**: PIC 9(01) - Current Census Division.
        *   **P-NEW-CURRENT-DIV**: Redefines P-NEW-CURRENT-CENSUS-DIV.
        *   **P-NEW-MSA-DATA**:
            *   **P-NEW-CHG-CODE-INDEX**: PIC X - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX**: PIC X(04) - Geographic Location MSA (right justified).
            *   **P-NEW-GEO-LOC-MSA9**: Redefines P-NEW-GEO-LOC-MSAX.
            *   **P-NEW-WAGE-INDEX-LOC-MSA**: PIC X(04) - Wage Index Location MSA (right justified).
            *   **P-NEW-STAND-AMT-LOC-MSA**: PIC X(04) - Standard Amount Location MSA (right justified).
            *   **P-NEW-STAND-AMT-LOC-MSA9**: Redefines P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST**:
                    *   **P-NEW-STAND-RURAL**: PIC XX - Standard Rural.
                        *   **P-NEW-STD-RURAL-CHECK**: 88 level for '  '.
                *   **P-NEW-RURAL-2ND**: PIC XX - Second Rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR**: PIC XX - Hospital Year.
        *   **P-NEW-LUGAR**: PIC X - Lugar indicator.
        *   **P-NEW-TEMP-RELIEF-IND**: PIC X - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND**: PIC X - Federal PPS Blend Indicator.
        *   **FILLER**: PIC X(05) - Filler.
    *   **PROV-NEWREC-HOLD2**:
        *   **P-NEW-VARIABLES**:
            *   **P-NEW-FAC-SPEC-RATE**: PIC 9(05)V9(02) - Facility Specific Rate.
            *   **P-NEW-COLA**: PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO**: PIC 9(01)V9(04) - Intern Ratio.
            *   **P-NEW-BED-SIZE**: PIC 9(05) - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO**: PIC 9(01)V9(03) - Operating Cost-to-Charge Ratio.
            *   **P-NEW-CMI**: PIC 9(01)V9(04) - Case Mix Index.
            *   **P-NEW-SSI-RATIO**: PIC V9(04) - SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO**: PIC V9(04) - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND**: PIC 9(01) - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR**: PIC 9(01)V9(05) - Proof Update Factor.
            *   **P-NEW-DSH-PERCENT**: PIC V9(04) - DSH Percent.
            *   **P-NEW-FYE-DATE**: PIC X(08) - Fiscal Year End Date.
        *   **FILLER**: PIC X(23) - Filler.
    *   **PROV-NEWREC-HOLD3**:
        *   **P-NEW-PASS-AMT-DATA**:
            *   **P-NEW-PASS-AMT-CAPITAL**: PIC 9(04)V99 - Pass Amount Capital.
            *   **P-NEW-PASS-AMT-DIR-MED-ED**: PIC 9(04)V99 - Pass Amount Direct Medical Education.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ**: PIC 9(04)V99 - Pass Amount Organ Acquisition.
            *   **P-NEW-PASS-AMT-PLUS-MISC**: PIC 9(04)V99 - Pass Amount Plus Miscellaneous.
        *   **P-NEW-CAPI-DATA**:
            *   **P-NEW-CAPI-PPS-PAY-CODE**: PIC X - CAPI PPS Payment Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE**: PIC 9(04)V99 - CAPI Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE**: PIC 9(04)V99 - CAPI Old Harm Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO**: PIC 9(01)V9999 - CAPI New Harm Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO**: PIC 9V999 - CAPI Cost-to-Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP**: PIC X - CAPI New Hospital.
            *   **P-NEW-CAPI-IME**: PIC 9V9999 - CAPI Indirect Medical Education.
            *   **P-NEW-CAPI-EXCEPTIONS**: PIC 9(04)V99 - CAPI Exceptions.
        *   **FILLER**: PIC X(22) - Filler.
*   **WAGE-NEW-INDEX-RECORD**:
    *   **Description**: A group item holding wage index information.
    *   **W-MSA**: PIC X(4) - Medical Service Area.
    *   **W-EFF-DATE**: PIC X(8) - Effective Date.
    *   **W-WAGE-INDEX1**: PIC S9(02)V9(04) - Wage Index (primary).
    *   **W-WAGE-INDEX2**: PIC S9(02)V9(04) - Wage Index (secondary).
    *   **W-WAGE-INDEX3**: PIC S9(02)V9(04) - Wage Index (tertiary).

---

## Program: LTCAL042

### Files Accessed:

*   **LTDRG031**: This is a `COPY` statement, indicating that the contents of `LTDRG031` are included in this program. Similar to LTCAL032, this likely defines a DRG lookup table used for processing, with the actual loading mechanism not explicitly shown here.

### Data Structures in WORKING-STORAGE SECTION:

*   **W-STORAGE-REF**:
    *   **Description**: A PIC X(46) field used to hold a descriptive string for the working storage section.
*   **CAL-VERSION**:
    *   **Description**: A PIC X(05) field holding the version of the calling program (LTCAL042), which is 'C04.2'.
*   **HOLD-PPS-COMPONENTS**:
    *   **Description**: A group item used to hold intermediate calculation results and components related to PPS (Prospective Payment System).
    *   **H-LOS**: PIC 9(03) - Length of Stay.
    *   **H-REG-DAYS**: PIC 9(03) - Regular Days.
    *   **H-TOTAL-DAYS**: PIC 9(05) - Total Days.
    *   **H-SSOT**: PIC 9(02) - Short Stay Outlier Threshold.
    *   **H-BLEND-RTC**: PIC 9(02) - Blend Return Code.
    *   **H-BLEND-FAC**: PIC 9(01)V9(01) - Blend Facility Rate component.
    *   **H-BLEND-PPS**: PIC 9(01)V9(01) - Blend PPS component.
    *   **H-SS-PAY-AMT**: PIC 9(07)V9(02) - Short Stay Payment Amount.
    *   **H-SS-COST**: PIC 9(07)V9(02) - Short Stay Cost.
    *   **H-LABOR-PORTION**: PIC 9(07)V9(06) - Labor Portion calculation.
    *   **H-NONLABOR-PORTION**: PIC 9(07)V9(06) - Non-Labor Portion calculation.
    *   **H-FIXED-LOSS-AMT**: PIC 9(07)V9(02) - Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE**: PIC 9(05)V9(02) - New Facility Specific Rate.
    *   **H-LOS-RATIO**: PIC 9(01)V9(05) - Length of Stay Ratio.

### Data Structures in LINKAGE SECTION:

*   **BILL-NEW-DATA**:
    *   **Description**: A group item representing the bill record passed from the calling program.
    *   **B-NPI10**:
        *   **B-NPI8**: PIC X(08) - National Provider Identifier (first 8 characters).
        *   **B-NPI-FILLER**: PIC X(02) - Filler for NPI.
    *   **B-PROVIDER-NO**: PIC X(06) - Provider Number.
    *   **B-PATIENT-STATUS**: PIC X(02) - Patient Status.
    *   **B-DRG-CODE**: PIC X(03) - Diagnosis Related Group Code.
    *   **B-LOS**: PIC 9(03) - Length of Stay.
    *   **B-COV-DAYS**: PIC 9(03) - Covered Days.
    *   **B-LTR-DAYS**: PIC 9(02) - Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE**:
        *   **B-DISCHG-CC**: PIC 9(02) - Discharge Date Century.
        *   **B-DISCHG-YY**: PIC 9(02) - Discharge Date Year.
        *   **B-DISCHG-MM**: PIC 9(02) - Discharge Date Month.
        *   **B-DISCHG-DD**: PIC 9(02) - Discharge Date Day.
    *   **B-COV-CHARGES**: PIC 9(07)V9(02) - Covered Charges.
    *   **B-SPEC-PAY-IND**: PIC X(01) - Special Payment Indicator.
    *   **FILLER**: PIC X(13) - Unused space.
*   **PPS-DATA-ALL**:
    *   **Description**: A group item containing all PPS (Prospective Payment System) related data, both input and output.
    *   **PPS-RTC**: PIC 9(02) - Return Code (indicates payment status or error).
    *   **PPS-CHRG-THRESHOLD**: PIC 9(07)V9(02) - Charge Threshold.
    *   **PPS-DATA**:
        *   **PPS-MSA**: PIC X(04) - Medical Service Area.
        *   **PPS-WAGE-INDEX**: PIC 9(02)V9(04) - Wage Index.
        *   **PPS-AVG-LOS**: PIC 9(02)V9(01) - Average Length of Stay.
        *   **PPS-RELATIVE-WGT**: PIC 9(01)V9(04) - Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT**: PIC 9(07)V9(02) - Outlier Payment Amount.
        *   **PPS-LOS**: PIC 9(03) - Length of Stay (used for output).
        *   **PPS-DRG-ADJ-PAY-AMT**: PIC 9(07)V9(02) - DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT**: PIC 9(07)V9(02) - Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT**: PIC 9(07)V9(02) - Final Payment Amount.
        *   **PPS-FAC-COSTS**: PIC 9(07)V9(02) - Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE**: PIC 9(07)V9(02) - New Facility Specific Rate (output).
        *   **PPS-OUTLIER-THRESHOLD**: PIC 9(07)V9(02) - Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE**: PIC X(03) - Submitted DRG Code.
        *   **PPS-CALC-VERS-CD**: PIC X(05) - Calculation Version Code.
        *   **PPS-REG-DAYS-USED**: PIC 9(03) - Regular Days Used.
        *   **PPS-LTR-DAYS-USED**: PIC 9(03) - Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR**: PIC 9(01) - Blend Year Indicator.
        *   **PPS-COLA**: PIC 9(01)V9(03) - Cost of Living Adjustment.
        *   **FILLER**: PIC X(04) - Unused space.
    *   **PPS-OTHER-DATA**:
        *   **PPS-NAT-LABOR-PCT**: PIC 9(01)V9(05) - National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT**: PIC 9(01)V9(05) - National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE**: PIC 9(05)V9(02) - Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE**: PIC 9(01)V9(03) - Budget Neutrality Rate.
        *   **FILLER**: PIC X(20) - Unused space.
    *   **PPS-PC-DATA**:
        *   **PPS-COT-IND**: PIC X(01) - Cost Outlier Indicator.
        *   **FILLER**: PIC X(20) - Unused space.
*   **PRICER-OPT-VERS-SW**:
    *   **Description**: A group item related to pricer option versions and switches.
    *   **PRICER-OPTION-SW**: PIC X(01) - Pricer Option Switch.
        *   **ALL-TABLES-PASSED**: 88 level for 'A'.
        *   **PROV-RECORD-PASSED**: 88 level for 'P'.
    *   **PPS-VERSIONS**:
        *   **PPDRV-VERSION**: PIC X(05) - Pricer DRG Version.
*   **PROV-NEW-HOLD**:
    *   **Description**: A group item holding provider-specific data.
    *   **PROV-NEWREC-HOLD1**:
        *   **P-NEW-NPI10**:
            *   **P-NEW-NPI8**: PIC X(08) - Provider NPI (first 8 chars).
            *   **P-NEW-NPI-FILLER**: PIC X(02) - NPI Filler.
        *   **P-NEW-PROVIDER-NO**:
            *   **P-NEW-STATE**: PIC 9(02) - Provider State.
            *   **FILLER**: PIC X(04) - Filler.
        *   **P-NEW-DATE-DATA**:
            *   **P-NEW-EFF-DATE**: Effective Date (CCYYMMDD).
            *   **P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date (CCYYMMDD).
            *   **P-NEW-REPORT-DATE**: Report Date (CCYYMMDD).
            *   **P-NEW-TERMINATION-DATE**: Termination Date (CCYYMMDD).
        *   **P-NEW-WAIVER-CODE**: PIC X(01) - Waiver Code.
            *   **P-NEW-WAIVER-STATE**: 88 level for 'Y'.
        *   **P-NEW-INTER-NO**: PIC 9(05) - Inter Number.
        *   **P-NEW-PROVIDER-TYPE**: PIC X(02) - Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV**: PIC 9(01) - Current Census Division.
        *   **P-NEW-CURRENT-DIV**: Redefines P-NEW-CURRENT-CENSUS-DIV.
        *   **P-NEW-MSA-DATA**:
            *   **P-NEW-CHG-CODE-INDEX**: PIC X - Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX**: PIC X(04) - Geographic Location MSA (right justified).
            *   **P-NEW-GEO-LOC-MSA9**: Redefines P-NEW-GEO-LOC-MSAX.
            *   **P-NEW-WAGE-INDEX-LOC-MSA**: PIC X(04) - Wage Index Location MSA (right justified).
            *   **P-NEW-STAND-AMT-LOC-MSA**: PIC X(04) - Standard Amount Location MSA (right justified).
            *   **P-NEW-STAND-AMT-LOC-MSA9**: Redefines P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST**:
                    *   **P-NEW-STAND-RURAL**: PIC XX - Standard Rural.
                        *   **P-NEW-STD-RURAL-CHECK**: 88 level for '  '.
                *   **P-NEW-RURAL-2ND**: PIC XX - Second Rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR**: PIC XX - Hospital Year.
        *   **P-NEW-LUGAR**: PIC X - Lugar indicator.
        *   **P-NEW-TEMP-RELIEF-IND**: PIC X - Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND**: PIC X - Federal PPS Blend Indicator.
        *   **FILLER**: PIC X(05) - Filler.
    *   **PROV-NEWREC-HOLD2**:
        *   **P-NEW-VARIABLES**:
            *   **P-NEW-FAC-SPEC-RATE**: PIC 9(05)V9(02) - Facility Specific Rate.
            *   **P-NEW-COLA**: PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO**: PIC 9(01)V9(04) - Intern Ratio.
            *   **P-NEW-BED-SIZE**: PIC 9(05) - Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO**: PIC 9(01)V9(03) - Operating Cost-to-Charge Ratio.
            *   **P-NEW-CMI**: PIC 9(01)V9(04) - Case Mix Index.
            *   **P-NEW-SSI-RATIO**: PIC V9(04) - SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO**: PIC V9(04) - Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND**: PIC 9(01) - PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR**: PIC 9(01)V9(05) - Proof Update Factor.
            *   **P-NEW-DSH-PERCENT**: PIC V9(04) - DSH Percent.
            *   **P-NEW-FYE-DATE**: PIC X(08) - Fiscal Year End Date.
        *   **FILLER**: PIC X(23) - Filler.
    *   **PROV-NEWREC-HOLD3**:
        *   **P-NEW-PASS-AMT-DATA**:
            *   **P-NEW-PASS-AMT-CAPITAL**: PIC 9(04)V99 - Pass Amount Capital.
            *   **P-NEW-PASS-AMT-DIR-MED-ED**: PIC 9(04)V99 - Pass Amount Direct Medical Education.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ**: PIC 9(04)V99 - Pass Amount Organ Acquisition.
            *   **P-NEW-PASS-AMT-PLUS-MISC**: PIC 9(04)V99 - Pass Amount Plus Miscellaneous.
        *   **P-NEW-CAPI-DATA**:
            *   **P-NEW-CAPI-PPS-PAY-CODE**: PIC X - CAPI PPS Payment Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE**: PIC 9(04)V99 - CAPI Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE**: PIC 9(04)V99 - CAPI Old Harm Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO**: PIC 9(01)V9999 - CAPI New Harm Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO**: PIC 9V999 - CAPI Cost-to-Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP**: PIC X - CAPI New Hospital.
            *   **P-NEW-CAPI-IME**: PIC 9V9999 - CAPI Indirect Medical Education.
            *   **P-NEW-CAPI-EXCEPTIONS**: PIC 9(04)V99 - CAPI Exceptions.
        *   **FILLER**: PIC X(22) - Filler.
*   **WAGE-NEW-INDEX-RECORD**:
    *   **Description**: A group item holding wage index information.
    *   **W-MSA**: PIC X(4) - Medical Service Area.
    *   **W-EFF-DATE**: PIC X(8) - Effective Date.
    *   **W-WAGE-INDEX1**: PIC S9(02)V9(04) - Wage Index (primary).
    *   **W-WAGE-INDEX2**: PIC S9(02)V9(04) - Wage Index (secondary).
    *   **W-WAGE-INDEX3**: PIC S9(02)V9(04) - Wage Index (tertiary).

---

## Program: LTDRG031

### Files Accessed:

*   **None**: This program appears to be a `COPY` file itself, containing only data definitions. It does not explicitly access any external files through the `FILE-CONTROL` section. Its content is intended to be copied into other programs.

### Data Structures in WORKING-STORAGE SECTION:

*   **W-DRG-FILLS**:
    *   **Description**: A series of PIC X(44) fields that collectively define a DRG (Diagnosis Related Group) lookup table. Each record appears to contain a DRG code, a relative weight, and an average length of stay. This data is then redefined by `W-DRG-TABLE`.
*   **W-DRG-TABLE**:
    *   **Description**: This is a `REDEFINES` clause for `W-DRG-FILLS`. It defines a table (array) named `WWM-ENTRY` that can be searched using an index (`WWM-INDX`).
    *   **WWM-ENTRY**: This is a table that occurs 502 times.
        *   **WWM-DRG**: PIC X(3) - Diagnosis Related Group code. This field is used as the `ASCENDING KEY` for searching the table.
        *   **WWM-RELWT**: PIC 9(1)V9(4) - Relative Weight associated with the DRG.
        *   **WWM-ALOS**: PIC 9(2)V9(1) - Average Length of Stay associated with the DRG.