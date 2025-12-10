Here's an analysis of each COBOL program provided, detailing the files accessed, and the data structures defined in the WORKING-STORAGE SECTION and LINKAGE SECTION.

---

## Program: LTCAL032

### Files Accessed:

*   **LTDRG031:** This is a COPYBOOK that is included in the WORKING-STORAGE SECTION. It defines the W-DRG-TABLE which is used for searching DRG codes. It's not a file in the traditional sense of being opened and read/written by this program, but rather a static data definition.

### WORKING-STORAGE SECTION Data Structures:

*   **W-STORAGE-REF:**
    *   **Description:** A PIC X(46) field used to hold a descriptive string indicating the program's working storage area.
*   **CAL-VERSION:**
    *   **Description:** A PIC X(05) field holding the version of the calculation program ('C03.2').
*   **HOLD-PPS-COMPONENTS:**
    *   **Description:** A group item used to hold intermediate calculation results related to PPS (Prospective Payment System) components.
    *   **H-LOS:** PIC 9(03) - Length of Stay.
    *   **H-REG-DAYS:** PIC 9(03) - Regular days.
    *   **H-TOTAL-DAYS:** PIC 9(05) - Total days.
    *   **H-SSOT:** PIC 9(02) - Short Stay Occupancy Threshold.
    *   **H-BLEND-RTC:** PIC 9(02) - Blend return code.
    *   **H-BLEND-FAC:** PIC 9(01)V9(01) - Blend facility percentage.
    *   **H-BLEND-PPS:** PIC 9(01)V9(01) - Blend PPS percentage.
    *   **H-SS-PAY-AMT:** PIC 9(07)V9(02) - Short Stay Payment Amount.
    *   **H-SS-COST:** PIC 9(07)V9(02) - Short Stay Cost.
    *   **H-LABOR-PORTION:** PIC 9(07)V9(06) - Labor portion of payment.
    *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06) - Non-labor portion of payment.
    *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02) - Fixed loss amount.
    *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - New facility specific rate.

### LINKAGE SECTION Data Structures:

*   **BILL-NEW-DATA:**
    *   **Description:** A group item representing the bill record passed from the calling program.
    *   **B-NPI10:**
        *   **B-NPI8:** PIC X(08) - National Provider Identifier (first 8 chars).
        *   **B-NPI-FILLER:** PIC X(02) - Filler for NPI.
    *   **B-PROVIDER-NO:** PIC X(06) - Provider number.
    *   **B-PATIENT-STATUS:** PIC X(02) - Patient status code.
    *   **B-DRG-CODE:** PIC X(03) - Diagnosis Related Group code.
    *   **B-LOS:** PIC 9(03) - Length of Stay.
    *   **B-COV-DAYS:** PIC 9(03) - Covered days.
    *   **B-LTR-DAYS:** PIC 9(02) - Lifetime reserve days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** PIC 9(02) - Discharge date century.
        *   **B-DISCHG-YY:** PIC 9(02) - Discharge date year.
        *   **B-DISCHG-MM:** PIC 9(02) - Discharge date month.
        *   **B-DISCHG-DD:** PIC 9(02) - Discharge date day.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02) - Total covered charges.
    *   **B-SPEC-PAY-IND:** PIC X(01) - Special payment indicator.
    *   **FILLER:** PIC X(13) - Unused space.
*   **PPS-DATA-ALL:**
    *   **Description:** A group item holding all PPS (Prospective Payment System) data calculated or used by the program.
    *   **PPS-RTC:** PIC 9(02) - PPS Return Code.
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02) - Charge threshold.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04) - Medicare Statistical Area code.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04) - Wage index value.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01) - Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04) - Relative weight for DRG.
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02) - Outlier payment amount.
        *   **PPS-LOS:** PIC 9(03) - Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02) - DRG adjusted payment amount.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02) - Federal payment amount.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02) - Final payment amount.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02) - Facility costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02) - New facility specific rate.
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02) - Outlier threshold amount.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03) - Submitted DRG code.
        *   **PPS-CALC-VERS-CD:** PIC X(05) - Calculation version code.
        *   **PPS-REG-DAYS-USED:** PIC 9(03) - Regular days used.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03) - Lifetime reserve days used.
        *   **PPS-BLEND-YEAR:** PIC 9(01) - Blend year indicator.
        *   **PPS-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment.
        *   **FILLER:** PIC X(04) - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05) - National labor percentage.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05) - National non-labor percentage.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02) - Standard federal rate.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03) - Budget neutrality rate.
        *   **FILLER:** PIC X(20) - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01) - Cost outlier indicator.
        *   **FILLER:** PIC X(20) - Unused space.
*   **PRICER-OPT-VERS-SW:**
    *   **Description:** A group item related to pricer option versions and switch.
    *   **PRICER-OPTION-SW:** PIC X(01) - Pricer option switch.
        *   **ALL-TABLES-PASSED:** 88 level, VALUE 'A'.
        *   **PROV-RECORD-PASSED:** 88 level, VALUE 'P'.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05) - Pricer program version.
*   **PROV-NEW-HOLD:**
    *   **Description:** A group item holding provider-specific data.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08) - National Provider Identifier (first 8 chars).
            *   **P-NEW-NPI-FILLER:** PIC X(02) - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02) - Provider state code.
            *   **FILLER:** PIC X(04) - Filler.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:** Effective date (CCYYMMDD).
                *   **P-NEW-EFF-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date (CCYYMMDD).
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-REPORT-DATE:** Report Date (CCYYMMDD).
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-TERMINATION-DATE:** Termination Date (CCYYMMDD).
                *   **P-NEW-TERM-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-TERM-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-TERM-DT-DD:** PIC 9(02) - Day.
        *   **P-NEW-WAIVER-CODE:** PIC X(01) - Waiver code.
            *   **P-NEW-WAIVER-STATE:** 88 level, VALUE 'Y'.
        *   **P-NEW-INTER-NO:** PIC 9(05) - Intern number.
        *   **P-NEW-PROVIDER-TYPE:** PIC X(02) - Provider type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01) - Current census division.
        *   **P-NEW-CURRENT-DIV:** REDEFINES P-NEW-CURRENT-CENSUS-DIV, PIC 9(01) - Current division.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** PIC X - Charge code index.
            *   **P-NEW-GEO-LOC-MSAX:** PIC X(04) - Geographic location MSA (right-justified).
            *   **P-NEW-GEO-LOC-MSA9:** REDEFINES P-NEW-GEO-LOC-MSAX, PIC 9(04) - Geographic location MSA (numeric).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** PIC X(04) - Wage index location MSA (right-justified).
            *   **P-NEW-STAND-AMT-LOC-MSA:** PIC X(04) - Standard amount location MSA (right-justified).
            *   **P-NEW-STAND-AMT-LOC-MSA9:** REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** PIC XX - Standard rural indicator.
                        *   **P-NEW-STD-RURAL-CHECK:** 88 level, VALUE '  '.
                *   **P-NEW-RURAL-2ND:** PIC XX - Second standard rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** PIC XX - Sole community-dependent hospital year.
        *   **P-NEW-LUGAR:** PIC X - Lugar indicator.
        *   **P-NEW-TEMP-RELIEF-IND:** PIC X - Temporary relief indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** PIC X - Federal PPS blend indicator.
        *   **FILLER:** PIC X(05) - Filler.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - Facility specific rate.
            *   **P-NEW-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** PIC 9(01)V9(04) - Intern ratio.
            *   **P-NEW-BED-SIZE:** PIC 9(05) - Bed size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** PIC 9(01)V9(03) - Operating cost-to-charge ratio.
            *   **P-NEW-CMI:** PIC 9(01)V9(04) - Case-mix index.
            *   **P-NEW-SSI-RATIO:** PIC V9(04) - SSI ratio.
            *   **P-NEW-MEDICAID-RATIO:** PIC V9(04) - Medicaid ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** PIC 9(01) - PPS blend year indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** PIC 9(01)V9(05) - Proof update factor.
            *   **P-NEW-DSH-PERCENT:** PIC V9(04) - DSH percentage.
            *   **P-NEW-FYE-DATE:** PIC X(08) - Fiscal Year End Date.
        *   **FILLER:** PIC X(23) - Filler.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** PIC 9(04)V99 - Capital pass amount.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** PIC 9(04)V99 - Direct medical education pass amount.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** PIC 9(04)V99 - Organ acquisition pass amount.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** PIC 9(04)V99 - Plus miscellaneous pass amount.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** PIC X - Capital PPS pay code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** PIC 9(04)V99 - Capital hospital specific rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** PIC 9(04)V99 - Capital old harm rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** PIC 9(01)V9999 - Capital new harm ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** PIC 9V999 - Capital cost-to-charge ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** PIC X - Capital new hospital indicator.
            *   **P-NEW-CAPI-IME:** PIC 9V9999 - Capital Indirect Medical Education.
            *   **P-NEW-CAPI-EXCEPTIONS:** PIC 9(04)V99 - Capital exceptions.
        *   **FILLER:** PIC X(22) - Filler.
*   **WAGE-NEW-INDEX-RECORD:**
    *   **Description:** A group item holding wage index information.
    *   **W-MSA:** PIC X(4) - Medicare Statistical Area code.
    *   **W-EFF-DATE:** PIC X(8) - Effective date.
    *   **W-WAGE-INDEX1:** PIC S9(02)V9(04) - Wage index value (primary).
    *   **W-WAGE-INDEX2:** PIC S9(02)V9(04) - Wage index value (secondary).
    *   **W-WAGE-INDEX3:** PIC S9(02)V9(04) - Wage index value (tertiary).

---

## Program: LTCAL042

### Files Accessed:

*   **LTDRG031:** This is a COPYBOOK that is included in the WORKING-STORAGE SECTION. It defines the W-DRG-TABLE which is used for searching DRG codes. It's not a file in the traditional sense of being opened and read/written by this program, but rather a static data definition.

### WORKING-STORAGE SECTION Data Structures:

*   **W-STORAGE-REF:**
    *   **Description:** A PIC X(46) field used to hold a descriptive string indicating the program's working storage area.
*   **CAL-VERSION:**
    *   **Description:** A PIC X(05) field holding the version of the calculation program ('C04.2').
*   **HOLD-PPS-COMPONENTS:**
    *   **Description:** A group item used to hold intermediate calculation results related to PPS (Prospective Payment System) components.
    *   **H-LOS:** PIC 9(03) - Length of Stay.
    *   **H-REG-DAYS:** PIC 9(03) - Regular days.
    *   **H-TOTAL-DAYS:** PIC 9(05) - Total days.
    *   **H-SSOT:** PIC 9(02) - Short Stay Occupancy Threshold.
    *   **H-BLEND-RTC:** PIC 9(02) - Blend return code.
    *   **H-BLEND-FAC:** PIC 9(01)V9(01) - Blend facility percentage.
    *   **H-BLEND-PPS:** PIC 9(01)V9(01) - Blend PPS percentage.
    *   **H-SS-PAY-AMT:** PIC 9(07)V9(02) - Short Stay Payment Amount.
    *   **H-SS-COST:** PIC 9(07)V9(02) - Short Stay Cost.
    *   **H-LABOR-PORTION:** PIC 9(07)V9(06) - Labor portion of payment.
    *   **H-NONLABOR-PORTION:** PIC 9(07)V9(06) - Non-labor portion of payment.
    *   **H-FIXED-LOSS-AMT:** PIC 9(07)V9(02) - Fixed loss amount.
    *   **H-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - New facility specific rate.
    *   **H-LOS-RATIO:** PIC 9(01)V9(05) - Length of Stay Ratio.

### LINKAGE SECTION Data Structures:

*   **BILL-NEW-DATA:**
    *   **Description:** A group item representing the bill record passed from the calling program.
    *   **B-NPI10:**
        *   **B-NPI8:** PIC X(08) - National Provider Identifier (first 8 chars).
        *   **B-NPI-FILLER:** PIC X(02) - Filler for NPI.
    *   **B-PROVIDER-NO:** PIC X(06) - Provider number.
    *   **B-PATIENT-STATUS:** PIC X(02) - Patient status code.
    *   **B-DRG-CODE:** PIC X(03) - Diagnosis Related Group code.
    *   **B-LOS:** PIC 9(03) - Length of Stay.
    *   **B-COV-DAYS:** PIC 9(03) - Covered days.
    *   **B-LTR-DAYS:** PIC 9(02) - Lifetime reserve days.
    *   **B-DISCHARGE-DATE:**
        *   **B-DISCHG-CC:** PIC 9(02) - Discharge date century.
        *   **B-DISCHG-YY:** PIC 9(02) - Discharge date year.
        *   **B-DISCHG-MM:** PIC 9(02) - Discharge date month.
        *   **B-DISCHG-DD:** PIC 9(02) - Discharge date day.
    *   **B-COV-CHARGES:** PIC 9(07)V9(02) - Total covered charges.
    *   **B-SPEC-PAY-IND:** PIC X(01) - Special payment indicator.
    *   **FILLER:** PIC X(13) - Unused space.
*   **PPS-DATA-ALL:**
    *   **Description:** A group item holding all PPS (Prospective Payment System) data calculated or used by the program.
    *   **PPS-RTC:** PIC 9(02) - PPS Return Code.
    *   **PPS-CHRG-THRESHOLD:** PIC 9(07)V9(02) - Charge threshold.
    *   **PPS-DATA:**
        *   **PPS-MSA:** PIC X(04) - Medicare Statistical Area code.
        *   **PPS-WAGE-INDEX:** PIC 9(02)V9(04) - Wage index value.
        *   **PPS-AVG-LOS:** PIC 9(02)V9(01) - Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** PIC 9(01)V9(04) - Relative weight for DRG.
        *   **PPS-OUTLIER-PAY-AMT:** PIC 9(07)V9(02) - Outlier payment amount.
        *   **PPS-LOS:** PIC 9(03) - Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** PIC 9(07)V9(02) - DRG adjusted payment amount.
        *   **PPS-FED-PAY-AMT:** PIC 9(07)V9(02) - Federal payment amount.
        *   **PPS-FINAL-PAY-AMT:** PIC 9(07)V9(02) - Final payment amount.
        *   **PPS-FAC-COSTS:** PIC 9(07)V9(02) - Facility costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** PIC 9(07)V9(02) - New facility specific rate.
        *   **PPS-OUTLIER-THRESHOLD:** PIC 9(07)V9(02) - Outlier threshold amount.
        *   **PPS-SUBM-DRG-CODE:** PIC X(03) - Submitted DRG code.
        *   **PPS-CALC-VERS-CD:** PIC X(05) - Calculation version code.
        *   **PPS-REG-DAYS-USED:** PIC 9(03) - Regular days used.
        *   **PPS-LTR-DAYS-USED:** PIC 9(03) - Lifetime reserve days used.
        *   **PPS-BLEND-YEAR:** PIC 9(01) - Blend year indicator.
        *   **PPS-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment.
        *   **FILLER:** PIC X(04) - Unused space.
    *   **PPS-OTHER-DATA:**
        *   **PPS-NAT-LABOR-PCT:** PIC 9(01)V9(05) - National labor percentage.
        *   **PPS-NAT-NONLABOR-PCT:** PIC 9(01)V9(05) - National non-labor percentage.
        *   **PPS-STD-FED-RATE:** PIC 9(05)V9(02) - Standard federal rate.
        *   **PPS-BDGT-NEUT-RATE:** PIC 9(01)V9(03) - Budget neutrality rate.
        *   **FILLER:** PIC X(20) - Unused space.
    *   **PPS-PC-DATA:**
        *   **PPS-COT-IND:** PIC X(01) - Cost outlier indicator.
        *   **FILLER:** PIC X(20) - Unused space.
*   **PRICER-OPT-VERS-SW:**
    *   **Description:** A group item related to pricer option versions and switch.
    *   **PRICER-OPTION-SW:** PIC X(01) - Pricer option switch.
        *   **ALL-TABLES-PASSED:** 88 level, VALUE 'A'.
        *   **PROV-RECORD-PASSED:** 88 level, VALUE 'P'.
    *   **PPS-VERSIONS:**
        *   **PPDRV-VERSION:** PIC X(05) - Pricer program version.
*   **PROV-NEW-HOLD:**
    *   **Description:** A group item holding provider-specific data.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:**
            *   **P-NEW-NPI8:** PIC X(08) - National Provider Identifier (first 8 chars).
            *   **P-NEW-NPI-FILLER:** PIC X(02) - Filler for NPI.
        *   **P-NEW-PROVIDER-NO:**
            *   **P-NEW-STATE:** PIC 9(02) - Provider state code.
            *   **FILLER:** PIC X(04) - Filler.
        *   **P-NEW-DATE-DATA:**
            *   **P-NEW-EFF-DATE:** Effective date (CCYYMMDD).
                *   **P-NEW-EFF-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-EFF-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-EFF-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-EFF-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date (CCYYMMDD).
                *   **P-NEW-FY-BEG-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-FY-BEG-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-FY-BEG-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-FY-BEG-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-REPORT-DATE:** Report Date (CCYYMMDD).
                *   **P-NEW-REPORT-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-REPORT-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-REPORT-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-REPORT-DT-DD:** PIC 9(02) - Day.
            *   **P-NEW-TERMINATION-DATE:** Termination Date (CCYYMMDD).
                *   **P-NEW-TERM-DT-CC:** PIC 9(02) - Century.
                *   **P-NEW-TERM-DT-YY:** PIC 9(02) - Year.
                *   **P-NEW-TERM-DT-MM:** PIC 9(02) - Month.
                *   **P-NEW-TERM-DT-DD:** PIC 9(02) - Day.
        *   **P-NEW-WAIVER-CODE:** PIC X(01) - Waiver code.
            *   **P-NEW-WAIVER-STATE:** 88 level, VALUE 'Y'.
        *   **P-NEW-INTER-NO:** PIC 9(05) - Intern number.
        *   **P-NEW-PROVIDER-TYPE:** PIC X(02) - Provider type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** PIC 9(01) - Current census division.
        *   **P-NEW-CURRENT-DIV:** REDEFINES P-NEW-CURRENT-CENSUS-DIV, PIC 9(01) - Current division.
        *   **P-NEW-MSA-DATA:**
            *   **P-NEW-CHG-CODE-INDEX:** PIC X - Charge code index.
            *   **P-NEW-GEO-LOC-MSAX:** PIC X(04) - Geographic location MSA (right-justified).
            *   **P-NEW-GEO-LOC-MSA9:** REDEFINES P-NEW-GEO-LOC-MSAX, PIC 9(04) - Geographic location MSA (numeric).
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** PIC X(04) - Wage index location MSA (right-justified).
            *   **P-NEW-STAND-AMT-LOC-MSA:** PIC X(04) - Standard amount location MSA (right-justified).
            *   **P-NEW-STAND-AMT-LOC-MSA9:** REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST:**
                    *   **P-NEW-STAND-RURAL:** PIC XX - Standard rural indicator.
                        *   **P-NEW-STD-RURAL-CHECK:** 88 level, VALUE '  '.
                *   **P-NEW-RURAL-2ND:** PIC XX - Second standard rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** PIC XX - Sole community-dependent hospital year.
        *   **P-NEW-LUGAR:** PIC X - Lugar indicator.
        *   **P-NEW-TEMP-RELIEF-IND:** PIC X - Temporary relief indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** PIC X - Federal PPS blend indicator.
        *   **FILLER:** PIC X(05) - Filler.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:**
            *   **P-NEW-FAC-SPEC-RATE:** PIC 9(05)V9(02) - Facility specific rate.
            *   **P-NEW-COLA:** PIC 9(01)V9(03) - Cost of Living Adjustment.
            *   **P-NEW-INTERN-RATIO:** PIC 9(01)V9(04) - Intern ratio.
            *   **P-NEW-BED-SIZE:** PIC 9(05) - Bed size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** PIC 9(01)V9(03) - Operating cost-to-charge ratio.
            *   **P-NEW-CMI:** PIC 9(01)V9(04) - Case-mix index.
            *   **P-NEW-SSI-RATIO:** PIC V9(04) - SSI ratio.
            *   **P-NEW-MEDICAID-RATIO:** PIC V9(04) - Medicaid ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** PIC 9(01) - PPS blend year indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** PIC 9(01)V9(05) - Proof update factor.
            *   **P-NEW-DSH-PERCENT:** PIC V9(04) - DSH percentage.
            *   **P-NEW-FYE-DATE:** PIC X(08) - Fiscal Year End Date.
        *   **FILLER:** PIC X(23) - Filler.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:**
            *   **P-NEW-PASS-AMT-CAPITAL:** PIC 9(04)V99 - Capital pass amount.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** PIC 9(04)V99 - Direct medical education pass amount.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** PIC 9(04)V99 - Organ acquisition pass amount.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** PIC 9(04)V99 - Plus miscellaneous pass amount.
        *   **P-NEW-CAPI-DATA:**
            *   **P-NEW-CAPI-PPS-PAY-CODE:** PIC X - Capital PPS pay code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** PIC 9(04)V99 - Capital hospital specific rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** PIC 9(04)V99 - Capital old harm rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** PIC 9(01)V9999 - Capital new harm ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** PIC 9V999 - Capital cost-to-charge ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** PIC X - Capital new hospital indicator.
            *   **P-NEW-CAPI-IME:** PIC 9V9999 - Capital Indirect Medical Education.
            *   **P-NEW-CAPI-EXCEPTIONS:** PIC 9(04)V99 - Capital exceptions.
        *   **FILLER:** PIC X(22) - Filler.
*   **WAGE-NEW-INDEX-RECORD:**
    *   **Description:** A group item holding wage index information.
    *   **W-MSA:** PIC X(4) - Medicare Statistical Area code.
    *   **W-EFF-DATE:** PIC X(8) - Effective date.
    *   **W-WAGE-INDEX1:** PIC S9(02)V9(04) - Wage index value (primary).
    *   **W-WAGE-INDEX2:** PIC S9(02)V9(04) - Wage index value (secondary).
    *   **W-WAGE-INDEX3:** PIC S9(02)V9(04) - Wage index value (tertiary).

---

## Program: LTDRG031

### Files Accessed:

*   This program does not explicitly access any files through `FILE-CONTROL`. It appears to be a data definition file (a COPYBOOK) that is intended to be included in other programs.

### WORKING-STORAGE SECTION Data Structures:

*   **W-DRG-FILLS:**
    *   **Description:** This is a series of PIC X(44) fields that collectively contain raw data for a DRG (Diagnosis Related Group) table. These are initialized with literal values.
*   **W-DRG-TABLE:**
    *   **Description:** This is a table structure that `REDEFINES` W-DRG-FILLS. It's designed to hold DRG data, allowing for searching.
    *   **WWM-ENTRY:**
        *   **Description:** An array (table) of 502 entries. The table is sorted by `WWM-DRG` and can be accessed using an index `WWM-INDX`.
        *   **WWM-DRG:** PIC X(3) - Diagnosis Related Group code. This is the key for the table.
        *   **WWM-RELWT:** PIC 9(1)V9(4) - Relative weight associated with the DRG.
        *   **WWM-ALOS:** PIC 9(2)V9(1) - Average Length of Stay for the DRG.

### LINKAGE SECTION Data Structures:

*   **No LINKAGE SECTION is defined in this program.** This confirms it's likely a data definition or utility program rather than a main processing module that receives parameters.