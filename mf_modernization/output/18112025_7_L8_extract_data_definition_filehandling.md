Here's the analysis of each COBOL program, detailing the files accessed, data structures in the WORKING-STORAGE SECTION, and data structures in the LINKAGE SECTION:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access statements are present in the code. However, the program uses a `COPY` statement to include `LTDRG031`. This implies that `LTCAL032` indirectly accesses the data within the included code, which likely contains DRG (Diagnosis Related Group) information.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description: A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of stay (LOS).
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short stay outlier threshold.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Blend return code, probably related to blend payment calculations.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend factor for facility costs.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend factor for PPS payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount, likely used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.
    *   Data structures defined by `COPY LTDRG031.` (See details in the analysis of `LTDRG031`)
    *   `PPS-DATA-ALL`:
        *   Description: A group of variables to return the calculated data to the calling program.
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return code indicating the payment status.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge threshold.
        *   `PPS-DATA`:
            *   Description: Group to store PPS related data.
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average length of stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier payment amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal payment amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final payment amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description: Calculation version code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular days used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve days used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend year indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
        *   `PPS-OTHER-DATA`:
            *   Description: Group to store other PPS related data.
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National labor percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National non-labor percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget neutrality rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
        *   `PPS-PC-DATA`:
            *   Description: Group to store PC data.
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost outlier indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
    *   `PRICER-OPT-VERS-SW`:
        *   Description: Group of variables to store pricer option and version information
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch to indicate if all tables are passed or just the provider record.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Value for `PRICER-OPTION-SW` when all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Value for `PRICER-OPTION-SW` when only provider record is passed.
        *   `PPS-VERSIONS`:
            *   Description: Group to store PPS versions.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description: Group of variables to store the provider record information.
        *   `PROV-NEWREC-HOLD1`:
            *   Description: Group of variables to store provider record hold 1 information.
            *   `P-NEW-NPI10`:
                *   Description: Group of variables to store NPI information.
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: NPI 8.
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: NPI filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider number.
            *   `P-NEW-STATE` PIC 9(02).
                *   Description: State.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
            *   `P-NEW-DATE-DATA`:
                *   Description: Group of variables to store date information.
                *   `P-NEW-EFF-DATE`:
                    *   Description: Group of variables to store the effective date.
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective date century.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective date year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective date month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective date day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   Description: Group of variables to store fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal year begin date century.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal year begin date year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal year begin date month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal year begin date day.
                *   `P-NEW-REPORT-DATE`:
                    *   Description: Group of variables to store report date.
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report date century.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report date year.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report date month.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report date day.
                *   `P-NEW-TERMINATION-DATE`:
                    *   Description: Group of variables to store termination date.
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                        *   Description: Termination date century.
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                        *   Description: Termination date year.
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                        *   Description: Termination date month.
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
                        *   Description: Termination date day.
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   Description: Waiver code.
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
                    *   Description: Value for waiver state.
            *   `P-NEW-INTER-NO` PIC 9(05).
                *   Description: Internal number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02).
                *   Description: Provider type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).
                *   Description: Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
                *   Description: Current Division.
            *   `P-NEW-MSA-DATA`:
                *   Description: Group of variables to store MSA data.
                *   `P-NEW-CHG-CODE-INDEX` PIC X.
                    *   Description: Charge code index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.
                    *   Description: Geo location MSA X.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                    *   Description: Geo location MSA 9.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Wage index location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.
                    *   Description: Standard amount location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   Description: Standard amount location MSA 9.
                    *   `P-NEW-RURAL-1ST`:
                        *   Description: Group of variables to store rural 1st.
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   Description: Standard rural.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                                *   Description: Check if standard rural.
                        *   `P-NEW-RURAL-2ND` PIC XX.
                            *   Description: Rural 2nd.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.
                *   Description: Sol com dep hosp year.
            *   `P-NEW-LUGAR` PIC X.
                *   Description: Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X.
                *   Description: Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.
                *   Description: Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).
                *   Description: Filler.
        *   `PROV-NEWREC-HOLD2`:
            *   Description: Group of variables to store provider record hold 2 information.
            *   `P-NEW-VARIABLES`:
                *   Description: Group of variables to store variables related to the provider.
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
                    *   Description: Facility specific rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03).
                    *   Description: Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).
                    *   Description: Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05).
                    *   Description: Bed size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).
                    *   Description: Operating cost to charge ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04).
                    *   Description: CMI.
                *   `P-NEW-SSI-RATIO` PIC V9(04).
                    *   Description: SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).
                    *   Description: Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).
                    *   Description: PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).
                    *   Description: PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04).
                    *   Description: DSH Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08).
                    *   Description: Fiscal Year End Date.
            *   `FILLER` PIC X(23).
                *   Description: Filler.
        *   `PROV-NEWREC-HOLD3`:
            *   Description: Group of variables to store provider record hold 3 information.
            *   `P-NEW-PASS-AMT-DATA`:
                *   Description: Group of variables to store pass amount data.
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.
                    *   Description: Pass amount capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.
                    *   Description: Pass amount direct medical education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.
                    *   Description: Pass amount organ acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.
                    *   Description: Pass amount plus misc.
            *   `P-NEW-CAPI-DATA`:
                *   Description: Group of variables to store capital data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.
                    *   Description: Capital PPS pay code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.
                    *   Description: Capital hospital specific rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.
                    *   Description: Capital old harm rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.
                    *   Description: Capital new harm ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.
                    *   Description: Capital cost to charge ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X.
                    *   Description: Capital new hospital.
                *   `P-NEW-CAPI-IME` PIC 9V9999.
                    *   Description: Capital IME.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.
                    *   Description: Capital exceptions.
            *   `FILLER` PIC X(22).
                *   Description: Filler.
    *   `WAGE-NEW-INDEX-RECORD`:
        *   Description: Group of variables to store wage index record.
        *   `W-MSA` PIC X(4).
            *   Description: Wage MSA.
        *   `W-EFF-DATE` PIC X(8).
            *   Description: Effective date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).
            *   Description: Wage index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04).
            *   Description: Wage index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04).
            *   Description: Wage index 3.

*   **LINKAGE SECTION Data Structures:**

    *   `BILL-NEW-DATA`:
        *   Description: A group of variables containing the billing data passed to the program.
        *   `B-NPI10`:
            *   Description: Group to store NPI 10 data.
            *   `B-NPI8` PIC X(08).
                *   Description: NPI 8.
            *   `B-NPI-FILLER` PIC X(02).
                *   Description: NPI filler.
        *   `B-PROVIDER-NO` PIC X(06).
            *   Description: Provider number.
        *   `B-PATIENT-STATUS` PIC X(02).
            *   Description: Patient status.
        *   `B-DRG-CODE` PIC X(03).
            *   Description: DRG code.
        *   `B-LOS` PIC 9(03).
            *   Description: Length of stay.
        *   `B-COV-DAYS` PIC 9(03).
            *   Description: Covered days.
        *   `B-LTR-DAYS` PIC 9(02).
            *   Description: Lifetime Reserve days.
        *   `B-DISCHARGE-DATE`:
            *   Description: Group of variables to store the discharge date.
            *   `B-DISCHG-CC` PIC 9(02).
                *   Description: Discharge date century.
            *   `B-DISCHG-YY` PIC 9(02).
                *   Description: Discharge date year.
            *   `B-DISCHG-MM` PIC 9(02).
                *   Description: Discharge date month.
            *   `B-DISCHG-DD` PIC 9(02).
                *   Description: Discharge date day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02).
            *   Description: Covered charges.
        *   `B-SPEC-PAY-IND` PIC X(01).
            *   Description: Special pay indicator.
        *   `FILLER` PIC X(13).
            *   Description: Filler.
    *   `PPS-DATA-ALL`: (Same as in WORKING-STORAGE, used for passing data back)
    *   `PRICER-OPT-VERS-SW`: (Same as in WORKING-STORAGE, used for passing data back)
    *   `PROV-NEW-HOLD`: (Same as in WORKING-STORAGE, used for passing data back)
    *   `WAGE-NEW-INDEX-RECORD`: (Same as in WORKING-STORAGE, used for passing data back)

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access statements are present in the code. However, the program uses a `COPY` statement to include `LTDRG031`. This implies that `LTCAL042` indirectly accesses the data within the included code, which likely contains DRG (Diagnosis Related Group) information.

*   **WORKING-STORAGE SECTION Data Structures:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A literal string used for internal program identification or debugging.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description: Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description: A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).
            *   Description: Length of stay (LOS).
        *   `H-REG-DAYS` PIC 9(03).
            *   Description: Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05).
            *   Description: Total days.
        *   `H-SSOT` PIC 9(02).
            *   Description: Short stay outlier threshold.
        *   `H-BLEND-RTC` PIC 9(02).
            *   Description: Blend return code, probably related to blend payment calculations.
        *   `H-BLEND-FAC` PIC 9(01)V9(01).
            *   Description: Blend factor for facility costs.
        *   `H-BLEND-PPS` PIC 9(01)V9(01).
            *   Description: Blend factor for PPS payment.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).
            *   Description: Short stay payment amount.
        *   `H-SS-COST` PIC 9(07)V9(02).
            *   Description: Short stay cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).
            *   Description: Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).
            *   Description: Fixed loss amount, likely used in outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).
            *   Description: New facility specific rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05).
            *   Description: Length of Stay Ratio
    *   Data structures defined by `COPY LTDRG031.` (See details in the analysis of `LTDRG031`)
    *   `PPS-DATA-ALL`:
        *   Description: A group of variables to return the calculated data to the calling program.
        *   `PPS-RTC` PIC 9(02).
            *   Description: Return code indicating the payment status.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).
            *   Description: Charge threshold.
        *   `PPS-DATA`:
            *   Description: Group to store PPS related data.
            *   `PPS-MSA` PIC X(04).
                *   Description: Metropolitan Statistical Area code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).
                *   Description: Wage index for the MSA.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01).
                *   Description: Average length of stay for the DRG.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).
                *   Description: Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Outlier payment amount.
            *   `PPS-LOS` PIC 9(03).
                *   Description: Length of stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).
                *   Description: DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Federal payment amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).
                *   Description: Final payment amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).
                *   Description: Facility costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).
                *   Description: New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).
                *   Description: Outlier threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03).
                *   Description: Submitted DRG code.
            *   `PPS-CALC-VERS-CD` PIC X(05).
                *   Description: Calculation version code.
            *   `PPS-REG-DAYS-USED` PIC 9(03).
                *   Description: Regular days used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03).
                *   Description: Lifetime Reserve days used.
            *   `PPS-BLEND-YEAR` PIC 9(01).
                *   Description: Blend year indicator.
            *   `PPS-COLA` PIC 9(01)V9(03).
                *   Description: Cost of Living Adjustment.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
        *   `PPS-OTHER-DATA`:
            *   Description: Group to store other PPS related data.
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).
                *   Description: National labor percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).
                *   Description: National non-labor percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).
                *   Description: Standard Federal rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).
                *   Description: Budget neutrality rate.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
        *   `PPS-PC-DATA`:
            *   Description: Group to store PC data.
            *   `PPS-COT-IND` PIC X(01).
                *   Description: Cost outlier indicator.
            *   `FILLER` PIC X(20).
                *   Description: Filler.
    *   `PRICER-OPT-VERS-SW`:
        *   Description: Group of variables to store pricer option and version information
        *   `PRICER-OPTION-SW` PIC X(01).
            *   Description: Switch to indicate if all tables are passed or just the provider record.
            *   `ALL-TABLES-PASSED` VALUE 'A'.
                *   Description: Value for `PRICER-OPTION-SW` when all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
                *   Description: Value for `PRICER-OPTION-SW` when only provider record is passed.
        *   `PPS-VERSIONS`:
            *   Description: Group to store PPS versions.
            *   `PPDRV-VERSION` PIC X(05).
                *   Description: Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description: Group of variables to store the provider record information.
        *   `PROV-NEWREC-HOLD1`:
            *   Description: Group of variables to store provider record hold 1 information.
            *   `P-NEW-NPI10`:
                *   Description: Group of variables to store NPI information.
                *   `P-NEW-NPI8` PIC X(08).
                    *   Description: NPI 8.
                *   `P-NEW-NPI-FILLER` PIC X(02).
                    *   Description: NPI filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06).
                *   Description: Provider number.
            *   `P-NEW-STATE` PIC 9(02).
                *   Description: State.
            *   `FILLER` PIC X(04).
                *   Description: Filler.
            *   `P-NEW-DATE-DATA`:
                *   Description: Group of variables to store date information.
                *   `P-NEW-EFF-DATE`:
                    *   Description: Group of variables to store the effective date.
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).
                        *   Description: Effective date century.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).
                        *   Description: Effective date year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).
                        *   Description: Effective date month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).
                        *   Description: Effective date day.
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   Description: Group of variables to store fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                        *   Description: Fiscal year begin date century.
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                        *   Description: Fiscal year begin date year.
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                        *   Description: Fiscal year begin date month.
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                        *   Description: Fiscal year begin date day.
                *   `P-NEW-REPORT-DATE`:
                    *   Description: Group of variables to store report date.
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                        *   Description: Report date century.
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                        *   Description: Report date year.
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                        *   Description: Report date month.
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                        *   Description: Report date day.
                *   `P-NEW-TERMIN