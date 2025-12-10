Here's an analysis of each COBOL program provided:

## Program: LTCAL032

**Files Accessed:**

*   **No external files are explicitly opened or accessed within this program.** The program relies on data passed through the `LINKAGE SECTION` and uses a `COPY` statement which likely includes definitions for a data structure used in the `SEARCH ALL` statement, but the actual file for `LTDRG031` is not directly handled here.

**Data Structures in WORKING-STORAGE SECTION:**

*   `W-STORAGE-REF`:
    *   **Description:** A PIC X(46) field used for informational purposes, containing a descriptive string about the program's working storage.
*   `CAL-VERSION`:
    *   **Description:** A PIC X(05) field holding the version number of the calculation module, set to 'C03.2'.
*   `HOLD-PPS-COMPONENTS`:
    *   **Description:** A group item used to hold intermediate calculation results and components related to the Prospective Payment System (PPS).
    *   `H-LOS` (PIC 9(03)): Holds the Length of Stay.
    *   `H-REG-DAYS` (PIC 9(03)): Holds the number of regular days.
    *   `H-TOTAL-DAYS` (PIC 9(05)): Holds the total number of days.
    *   `H-SSOT` (PIC 9(02)): Holds the Short Stay Outlier Threshold.
    *   `H-BLEND-RTC` (PIC 9(02)): Holds the blend return code.
    *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Holds the facility rate component of the blend.
    *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Holds the PPS component of the blend.
    *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Holds the calculated short stay payment amount.
    *   `H-SS-COST` (PIC 9(07)V9(02)): Holds the calculated short stay cost.
    *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Holds the labor portion of the payment.
    *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Holds the non-labor portion of the payment.
    *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Holds a fixed amount related to loss calculations.
    *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Holds a new facility-specific rate.

**Data Structures in LINKAGE SECTION:**

*   `BILL-NEW-DATA`:
    *   **Description:** A group item representing the input bill record passed from the calling program.
    *   `B-NPI10`: A group item for National Provider Identifier (NPI).
        *   `B-NPI8` (PIC X(08)): The main part of the NPI.
        *   `B-NPI-FILLER` (PIC X(02)): A filler for the NPI.
    *   `B-PROVIDER-NO` (PIC X(06)): The provider's unique number.
    *   `B-PATIENT-STATUS` (PIC X(02)): The patient's status.
    *   `B-DRG-CODE` (PIC X(03)): The Diagnosis Related Group (DRG) code.
    *   `B-LOS` (PIC 9(03)): Length of Stay for the bill.
    *   `B-COV-DAYS` (PIC 9(03)): Covered days for the bill.
    *   `B-LTR-DAYS` (PIC 9(02)): Lifetime reserve days for the bill.
    *   `B-DISCHARGE-DATE`: A group item for the discharge date.
        *   `B-DISCHG-CC` (PIC 9(02)): Discharge date century.
        *   `B-DISCHG-YY` (PIC 9(02)): Discharge date year.
        *   `B-DISCHG-MM` (PIC 9(02)): Discharge date month.
        *   `B-DISCHG-DD` (PIC 9(02)): Discharge date day.
    *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Total covered charges for the bill.
    *   `B-SPEC-PAY-IND` (PIC X(01)): Special payment indicator.
    *   `FILLER` (PIC X(13)): Unused space.
*   `PPS-DATA-ALL`:
    *   **Description:** A group item containing all the PPS-related data that is calculated or modified by this subroutine and passed back to the caller.
    *   `PPS-RTC` (PIC 9(02)): The return code indicating the processing status or payment method.
    *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold for outliers.
    *   `PPS-DATA`: A subgroup containing various PPS calculation data.
        *   `PPS-MSA` (PIC X(04)): Metropolitan Statistical Area code.
        *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): The wage index value.
        *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay for the DRG.
        *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative weight for the DRG.
        *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Calculated outlier payment amount.
        *   `PPS-LOS` (PIC 9(03)): Length of Stay used in calculations.
        *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG adjusted payment amount.
        *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal payment amount.
        *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): The final calculated payment amount.
        *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility costs.
        *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility-specific rate.
        *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Calculated outlier threshold.
        *   `PPS-SUBM-DRG-CODE` (PIC X(03)): DRG code submitted for processing.
        *   `PPS-CALC-VERS-CD` (PIC X(05)): Version code for the calculation.
        *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular days used in calculation.
        *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime reserve days used in calculation.
        *   `PPS-BLEND-YEAR` (PIC 9(01)): Indicator for the PPS blend year.
        *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
        *   `FILLER` (PIC X(04)): Unused space.
    *   `PPS-OTHER-DATA`: A subgroup for other PPS-related data.
        *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National labor percentage.
        *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National non-labor percentage.
        *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard federal rate.
        *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget neutrality rate.
        *   `FILLER` (PIC X(20)): Unused space.
    *   `PPS-PC-DATA`: A subgroup for PC (Payment Component) data.
        *   `PPS-COT-IND` (PIC X(01)): Cost Outlier indicator.
        *   `FILLER` (PIC X(20)): Unused space.
*   `PRICER-OPT-VERS-SW`:
    *   **Description:** A group item for pricier option versions and switch.
    *   `PRICER-OPTION-SW` (PIC X(01)): Switch for pricier options.
        *   `ALL-TABLES-PASSED` (88 level): Condition value 'A'.
        *   `PROV-RECORD-PASSED` (88 level): Condition value 'P'.
    *   `PPS-VERSIONS`: A subgroup for PPS versions.
        *   `PPDRV-VERSION` (PIC X(05)): Version of the DRG pricier program.
*   `PROV-NEW-HOLD`:
    *   **Description:** A group item holding provider-specific data.
    *   `PROV-NEWREC-HOLD1`: First part of the provider record.
        *   `P-NEW-NPI10`: NPI data.
            *   `P-NEW-NPI8` (PIC X(08)): NPI.
            *   `P-NEW-NPI-FILLER` (PIC X(02)): NPI filler.
        *   `P-NEW-PROVIDER-NO`: Provider number details.
            *   `P-NEW-STATE` (PIC 9(02)): Provider state.
            *   `FILLER` (PIC X(04)): Filler.
        *   `P-NEW-DATE-DATA`: Provider date information.
            *   `P-NEW-EFF-DATE`: Provider effective date.
                *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Effective date century.
                *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Effective date year.
                *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Effective date month.
                *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Effective date day.
            *   `P-NEW-FY-BEGIN-DATE`: Provider fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): FY begin date century.
                *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): FY begin date year.
                *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): FY begin date month.
                *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): FY begin date day.
            *   `P-NEW-REPORT-DATE`: Provider report date.
                *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Report date century.
                *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Report date year.
                *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Report date month.
                *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Report date day.
            *   `P-NEW-TERMINATION-DATE`: Provider termination date.
                *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Termination date century.
                *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Termination date year.
                *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Termination date month.
                *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Termination date day.
        *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver code.
            *   `P-NEW-WAIVER-STATE` (88 level): Condition value 'Y'.
        *   `P-NEW-INTER-NO` (PIC 9(05)): Intern number.
        *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider type.
        *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current census division.
        *   `P-NEW-CURRENT-DIV` (PIC 9(01)): Redefines `P-NEW-CURRENT-CENSUS-DIV`.
        *   `P-NEW-MSA-DATA`: MSA data for the provider.
            *   `P-NEW-CHG-CODE-INDEX` (PIC X): Change code index.
            *   `P-NEW-GEO-LOC-MSAX` (PIC X(04) JUST RIGHT): Geographic location MSA.
            *   `P-NEW-GEO-LOC-MSA9` (PIC 9(04)): Redefines `P-NEW-GEO-LOC-MSAX`.
            *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04) JUST RIGHT): Wage index location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04) JUST RIGHT): Standard amount location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9` (PIC X(04)): Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                *   `P-NEW-RURAL-1ST`: Rural data.
                    *   `P-NEW-STAND-RURAL` (PIC XX): Standard rural indicator.
                        *   `P-NEW-STD-RURAL-CHECK` (88 level): Condition value ' '.
                    *   `P-NEW-RURAL-2ND` (PIC XX): Second part of rural data.
        *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): SOL/COM/DEP Hospital Year.
        *   `P-NEW-LUGAR` (PIC X): Lugar indicator.
        *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary relief indicator.
        *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS blend indicator.
        *   `FILLER` (PIC X(05)): Unused space.
    *   `PROV-NEWREC-HOLD2`: Second part of the provider record.
        *   `P-NEW-VARIABLES`: Provider calculation variables.
            *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility-specific rate.
            *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern ratio.
            *   `P-NEW-BED-SIZE` (PIC 9(05)): Provider bed size.
            *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating cost-to-charge ratio.
            *   `P-NEW-CMI` (PIC 9(01)V9(04)): Case Mix Index.
            *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
            *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
            *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
            *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): Proof update factor.
            *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percentage.
            *   `P-NEW-FYE-DATE` (PIC X(08)): FY End Date.
        *   `FILLER` (PIC X(23)): Unused space.
    *   `PROV-NEWREC-HOLD3`: Third part of the provider record.
        *   `P-NEW-PASS-AMT-DATA`: Passed amount data.
            *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Capital pass amount.
            *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Direct medical education pass amount.
            *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Organ acquisition pass amount.
            *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Pass amount plus misc.
        *   `P-NEW-CAPI-DATA`: Capital data.
            *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capital PPS pay code.
            *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capital hospital specific rate.
            *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capital old harm rate.
            *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capital new harm ratio.
            *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capital cost-change ratio.
            *   `P-NEW-CAPI-NEW-HOSP` (PIC X): Capital new hospital indicator.
            *   `P-NEW-CAPI-IME` (PIC 9V9999): Capital IME.
            *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): Capital exceptions.
        *   `FILLER` (PIC X(22)): Unused space.
*   `WAGE-NEW-INDEX-RECORD`:
    *   **Description:** A record containing wage index information.
    *   `W-MSA` (PIC X(4)): MSA code.
    *   `W-EFF-DATE` (PIC X(8)): Effective date.
    *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage index value (primary).
    *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage index value (secondary).
    *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage index value (tertiary).

## Program: LTCAL042

**Files Accessed:**

*   **No external files are explicitly opened or accessed within this program.** Similar to LTCAL032, it relies on data passed via `LINKAGE SECTION` and a `COPY` statement for `LTDRG031`.

**Data Structures in WORKING-STORAGE SECTION:**

*   `W-STORAGE-REF`:
    *   **Description:** A PIC X(46) field used for informational purposes, containing a descriptive string about the program's working storage.
*   `CAL-VERSION`:
    *   **Description:** A PIC X(05) field holding the version number of the calculation module, set to 'C04.2'.
*   `HOLD-PPS-COMPONENTS`:
    *   **Description:** A group item used to hold intermediate calculation results and components related to the Prospective Payment System (PPS).
    *   `H-LOS` (PIC 9(03)): Holds the Length of Stay.
    *   `H-REG-DAYS` (PIC 9(03)): Holds the number of regular days.
    *   `H-TOTAL-DAYS` (PIC 9(05)): Holds the total number of days.
    *   `H-SSOT` (PIC 9(02)): Holds the Short Stay Outlier Threshold.
    *   `H-BLEND-RTC` (PIC 9(02)): Holds the blend return code.
    *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Holds the facility rate component of the blend.
    *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Holds the PPS component of the blend.
    *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Holds the calculated short stay payment amount.
    *   `H-SS-COST` (PIC 9(07)V9(02)): Holds the calculated short stay cost.
    *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Holds the labor portion of the payment.
    *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Holds the non-labor portion of the payment.
    *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Holds a fixed amount related to loss calculations.
    *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Holds a new facility-specific rate.
    *   `H-LOS-RATIO` (PIC 9(01)V9(05)): Holds the ratio of LOS to Average LOS.

**Data Structures in LINKAGE SECTION:**

*   `BILL-NEW-DATA`:
    *   **Description:** A group item representing the input bill record passed from the calling program.
    *   `B-NPI10`: A group item for National Provider Identifier (NPI).
        *   `B-NPI8` (PIC X(08)): The main part of the NPI.
        *   `B-NPI-FILLER` (PIC X(02)): A filler for the NPI.
    *   `B-PROVIDER-NO` (PIC X(06)): The provider's unique number.
    *   `B-PATIENT-STATUS` (PIC X(02)): The patient's status.
    *   `B-DRG-CODE` (PIC X(03)): The Diagnosis Related Group (DRG) code.
    *   `B-LOS` (PIC 9(03)): Length of Stay for the bill.
    *   `B-COV-DAYS` (PIC 9(03)): Covered days for the bill.
    *   `B-LTR-DAYS` (PIC 9(02)): Lifetime reserve days for the bill.
    *   `B-DISCHARGE-DATE`: A group item for the discharge date.
        *   `B-DISCHG-CC` (PIC 9(02)): Discharge date century.
        *   `B-DISCHG-YY` (PIC 9(02)): Discharge date year.
        *   `B-DISCHG-MM` (PIC 9(02)): Discharge date month.
        *   `B-DISCHG-DD` (PIC 9(02)): Discharge date day.
    *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Total covered charges for the bill.
    *   `B-SPEC-PAY-IND` (PIC X(01)): Special payment indicator.
    *   `FILLER` (PIC X(13)): Unused space.
*   `PPS-DATA-ALL`:
    *   **Description:** A group item containing all the PPS-related data that is calculated or modified by this subroutine and passed back to the caller.
    *   `PPS-RTC` (PIC 9(02)): The return code indicating the processing status or payment method.
    *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold for outliers.
    *   `PPS-DATA`: A subgroup containing various PPS calculation data.
        *   `PPS-MSA` (PIC X(04)): Metropolitan Statistical Area code.
        *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): The wage index value.
        *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay for the DRG.
        *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative weight for the DRG.
        *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Calculated outlier payment amount.
        *   `PPS-LOS` (PIC 9(03)): Length of Stay used in calculations.
        *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG adjusted payment amount.
        *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal payment amount.
        *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): The final calculated payment amount.
        *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility costs.
        *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility-specific rate.
        *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Calculated outlier threshold.
        *   `PPS-SUBM-DRG-CODE` (PIC X(03)): DRG code submitted for processing.
        *   `PPS-CALC-VERS-CD` (PIC X(05)): Version code for the calculation.
        *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular days used in calculation.
        *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime reserve days used in calculation.
        *   `PPS-BLEND-YEAR` (PIC 9(01)): Indicator for the PPS blend year.
        *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
        *   `FILLER` (PIC X(04)): Unused space.
    *   `PPS-OTHER-DATA`: A subgroup for other PPS-related data.
        *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National labor percentage.
        *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National non-labor percentage.
        *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard federal rate.
        *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget neutrality rate.
        *   `FILLER` (PIC X(20)): Unused space.
    *   `PPS-PC-DATA`: A subgroup for PC (Payment Component) data.
        *   `PPS-COT-IND` (PIC X(01)): Cost Outlier indicator.
        *   `FILLER` (PIC X(20)): Unused space.
*   `PRICER-OPT-VERS-SW`:
    *   **Description:** A group item for pricier option versions and switch.
    *   `PRICER-OPTION-SW` (PIC X(01)): Switch for pricier options.
        *   `ALL-TABLES-PASSED` (88 level): Condition value 'A'.
        *   `PROV-RECORD-PASSED` (88 level): Condition value 'P'.
    *   `PPS-VERSIONS`: A subgroup for PPS versions.
        *   `PPDRV-VERSION` (PIC X(05)): Version of the DRG pricier program.
*   `PROV-NEW-HOLD`:
    *   **Description:** A group item holding provider-specific data.
    *   `PROV-NEWREC-HOLD1`: First part of the provider record.
        *   `P-NEW-NPI10`: NPI data.
            *   `P-NEW-NPI8` (PIC X(08)): The main part of the NPI.
            *   `P-NEW-NPI-FILLER` (PIC X(02)): A filler for the NPI.
        *   `P-NEW-PROVIDER-NO`: Provider number details.
            *   `P-NEW-STATE` (PIC 9(02)): Provider state.
            *   `FILLER` (PIC X(04)): Filler.
        *   `P-NEW-DATE-DATA`: Provider date information.
            *   `P-NEW-EFF-DATE`: Provider effective date.
                *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Effective date century.
                *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Effective date year.
                *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Effective date month.
                *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Effective date day.
            *   `P-NEW-FY-BEGIN-DATE`: Provider fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): FY begin date century.
                *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): FY begin date year.
                *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): FY begin date month.
                *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): FY begin date day.
            *   `P-NEW-REPORT-DATE`: Provider report date.
                *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Report date century.
                *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Report date year.
                *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Report date month.
                *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Report date day.
            *   `P-NEW-TERMINATION-DATE`: Provider termination date.
                *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Termination date century.
                *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Termination date year.
                *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Termination date month.
                *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Termination date day.
        *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver code.
            *   `P-NEW-WAIVER-STATE` (88 level): Condition value 'Y'.
        *   `P-NEW-INTER-NO` (PIC 9(05)): Intern number.
        *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider type.
        *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current census division.
        *   `P-NEW-CURRENT-DIV` (PIC 9(01)): Redefines `P-NEW-CURRENT-CENSUS-DIV`.
        *   `P-NEW-MSA-DATA`: MSA data for the provider.
            *   `P-NEW-CHG-CODE-INDEX` (PIC X): Change code index.
            *   `P-NEW-GEO-LOC-MSAX` (PIC X(04) JUST RIGHT): Geographic location MSA.
            *   `P-NEW-GEO-LOC-MSA9` (PIC 9(04)): Redefines `P-NEW-GEO-LOC-MSAX`.
            *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04) JUST RIGHT): Wage index location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04) JUST RIGHT): Standard amount location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9` (PIC X(04)): Redefines `P-NEW-STAND-AMT-LOC-MSA`.
                *   `P-NEW-RURAL-1ST`: Rural data.
                    *   `P-NEW-STAND-RURAL` (PIC XX): Standard rural indicator.
                        *   `P-NEW-STD-RURAL-CHECK` (88 level): Condition value ' '.
                    *   `P-NEW-RURAL-2ND` (PIC XX): Second part of rural data.
        *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): SOL/COM/DEP Hospital Year.
        *   `P-NEW-LUGAR` (PIC X): Lugar indicator.
        *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary relief indicator.
        *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS blend indicator.
        *   `FILLER` (PIC X(05)): Unused space.
    *   `PROV-NEWREC-HOLD2`: Second part of the provider record.
        *   `P-NEW-VARIABLES`: Provider calculation variables.
            *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility-specific rate.
            *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern ratio.
            *   `P-NEW-BED-SIZE` (PIC 9(05)): Provider bed size.
            *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating cost-to-charge ratio.
            *   `P-NEW-CMI` (PIC 9(01)V9(04)): Case Mix Index.
            *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
            *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
            *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
            *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): Proof update factor.
            *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percentage.
            *   `P-NEW-FYE-DATE` (PIC X(08)): FY End Date.
        *   `FILLER` (PIC X(23)): Unused space.
    *   `PROV-NEWREC-HOLD3`: Third part of the provider record.
        *   `P-NEW-PASS-AMT-DATA`: Passed amount data.
            *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Capital pass amount.
            *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Direct medical education pass amount.
            *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Organ acquisition pass amount.
            *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Pass amount plus misc.
        *   `P-NEW-CAPI-DATA`: Capital data.
            *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capital PPS pay code.
            *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capital hospital specific rate.
            *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capital old harm rate.
            *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capital new harm ratio.
            *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capital cost-change ratio.
            *   `P-NEW-CAPI-NEW-HOSP` (PIC X): Capital new hospital indicator.
            *   `P-NEW-CAPI-IME` (PIC 9V9999): Capital IME.
            *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): Capital exceptions.
        *   `FILLER` (PIC X(22)): Unused space.
*   `WAGE-NEW-INDEX-RECORD`:
    *   **Description:** A record containing wage index information.
    *   `W-MSA` (PIC X(4)): MSA code.
    *   `W-EFF-DATE` (PIC X(8)): Effective date.
    *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage index value (primary).
    *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage index value (secondary).
    *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage index value (tertiary).

## Program: LTDRG031

**Files Accessed:**

*   **No external files are explicitly opened or accessed within this program.** This program segment appears to be a `COPY` member, likely included by other programs (like LTCAL032 and LTCAL042) to define a DRG (Diagnosis Related Group) table.

**Data Structures in WORKING-STORAGE SECTION:**

*   `W-DRG-FILLS`:
    *   **Description:** This is a series of PIC X(44) fields that collectively hold the data for the DRG table. Each field contains concatenated DRG information (DRG code, relative weight, average LOS).
*   `W-DRG-TABLE`:
    *   **Description:** This is a redefinition of `W-DRG-FILLS` to create a table structure.
    *   `WWM-ENTRY` (OCCURS 502 TIMES): Represents a single entry in the DRG table.
        *   `WWM-DRG` (PIC X(3)): The DRG code. This field is used as the ascending key for the table.
        *   `WWM-RELWT` (PIC 9(1)V9(4)): The relative weight associated with the DRG.
        *   `WWM-ALOS` (PIC 9(2)V9(1)): The average Length of Stay associated with the DRG.

**Data Structures in LINKAGE SECTION:**

*   **None.** This program segment does not define a `LINKAGE SECTION`.