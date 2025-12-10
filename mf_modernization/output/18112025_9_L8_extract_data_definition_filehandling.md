Here's the analysis of each COBOL program, including file access, data structures, and their descriptions:

**COBOL Program: LTCAL032**

*   **Files Accessed:**

    *   No explicit file access statements (like `SELECT` statements) are present in the provided code.  However, it's highly likely that this program interacts with external data sources through:
        *   **COPY LTDRG031:** This suggests the program uses a copybook (likely containing data definitions for DRG codes, weights, and average lengths of stay)
        *   **PROV-NEW-HOLD, WAGE-NEW-INDEX-RECORD:** This suggests the program uses provider and wage index records
*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.

        *   *Description:*  A descriptive string, likely used for debugging or identification purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.

        *   *Description:*  Indicates the version of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`:

        *   `H-LOS` PIC 9(03).

            *   *Description:* Length of Stay from input

        *   `H-REG-DAYS` PIC 9(03).

            *   *Description:* Regular days.

        *   `H-TOTAL-DAYS` PIC 9(05).

            *   *Description:* Total days.

        *   `H-SSOT` PIC 9(02).

            *   *Description:* Short Stay Outlier Threshold.

        *   `H-BLEND-RTC` PIC 9(02).

            *   *Description:* Blend Return Code.

        *   `H-BLEND-FAC` PIC 9(01)V9(01).

            *   *Description:* Blend Facility Percentage.

        *   `H-BLEND-PPS` PIC 9(01)V9(01).

            *   *Description:* Blend PPS Percentage.

        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).

            *   *Description:* Short Stay Payment Amount.

        *   `H-SS-COST` PIC 9(07)V9(02).

            *   *Description:* Short Stay Cost.

        *   `H-LABOR-PORTION` PIC 9(07)V9(06).

            *   *Description:* Labor Portion of the payment calculation.

        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).

            *   *Description:* Non-Labor Portion of the payment calculation.

        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).

            *   *Description:* Fixed Loss Amount for outlier calculation.

        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).

            *   *Description:* New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the input data passed *to* the program.

        *   `B-NPI10`:

            *   `B-NPI8` PIC X(08).

                *   *Description:* National Provider Identifier (NPI) - first 8 characters.

            *   `B-NPI-FILLER` PIC X(02).

                *   *Description:* Filler for the NPI.

        *   `B-PROVIDER-NO` PIC X(06).

            *   *Description:* Provider Number.

        *   `B-PATIENT-STATUS` PIC X(02).

            *   *Description:* Patient Status.

        *   `B-DRG-CODE` PIC X(03).

            *   *Description:* Diagnosis Related Group (DRG) Code.

        *   `B-LOS` PIC 9(03).

            *   *Description:* Length of Stay (in days).

        *   `B-COV-DAYS` PIC 9(03).

            *   *Description:* Covered Days.

        *   `B-LTR-DAYS` PIC 9(02).

            *   *Description:* Lifetime Reserve Days.

        *   `B-DISCHARGE-DATE`:

            *   `B-DISCHG-CC` PIC 9(02).

                *   *Description:* Discharge Century Code.

            *   `B-DISCHG-YY` PIC 9(02).

                *   *Description:* Discharge Year (last two digits).

            *   `B-DISCHG-MM` PIC 9(02).

                *   *Description:* Discharge Month.

            *   `B-DISCHG-DD` PIC 9(02).

                *   *Description:* Discharge Day.

        *   `B-COV-CHARGES` PIC 9(07)V9(02).

            *   *Description:* Covered Charges.

        *   `B-SPEC-PAY-IND` PIC X(01).

            *   *Description:* Special Payment Indicator.

        *   `FILLER` PIC X(13).

            *   *Description:* Filler.

    *   `PPS-DATA-ALL`: This is the output data passed *back* to the calling program. It contains the results of the PPS (Prospective Payment System) calculation.

        *   `PPS-RTC` PIC 9(02).

            *   *Description:* Return Code.  Indicates the result of the calculation (e.g., success, various error conditions, and payment types).

        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).

            *   *Description:* Charge Threshold.

        *   `PPS-DATA`:

            *   `PPS-MSA` PIC X(04).

                *   *Description:* Metropolitan Statistical Area (MSA) code.

            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).

                *   *Description:* Wage Index.

            *   `PPS-AVG-LOS` PIC 9(02)V9(01).

                *   *Description:* Average Length of Stay.

            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).

                *   *Description:* Relative Weight for the DRG.

            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Outlier Payment Amount.

            *   `PPS-LOS` PIC 9(03).

                *   *Description:* Length of stay.

            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* DRG Adjusted Payment Amount.

            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Federal Payment Amount.

            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Final Payment Amount.

            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).

                *   *Description:* Facility Costs.

            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).

                *   *Description:* New Facility Specific Rate.

            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).

                *   *Description:* Outlier Threshold.

            *   `PPS-SUBM-DRG-CODE` PIC X(03).

                *   *Description:* Submitted DRG Code.

            *   `PPS-CALC-VERS-CD` PIC X(05).

                *   *Description:* Calculation Version Code.

            *   `PPS-REG-DAYS-USED` PIC 9(03).

                *   *Description:* Regular Days Used.

            *   `PPS-LTR-DAYS-USED` PIC 9(03).

                *   *Description:* Lifetime Reserve Days Used.

            *   `PPS-BLEND-YEAR` PIC 9(01).

                *   *Description:* Blend Year Indicator.

            *   `PPS-COLA` PIC 9(01)V9(03).

                *   *Description:* Cost of Living Adjustment.

            *   `FILLER` PIC X(04).

                *   *Description:* Filler.

        *   `PPS-OTHER-DATA`:

            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).

                *   *Description:* National Labor Percentage.

            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).

                *   *Description:* National Non-Labor Percentage.

            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).

                *   *Description:* Standard Federal Rate.

            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).

                *   *Description:* Budget Neutrality Rate.

            *   `FILLER` PIC X(20).

                *   *Description:* Filler.

        *   `PPS-PC-DATA`:

            *   `PPS-COT-IND` PIC X(01).

                *   *Description:* Cost Outlier Indicator.

            *   `FILLER` PIC X(20).

                *   *Description:* Filler.

    *   `PRICER-OPT-VERS-SW`:

        *   `PRICER-OPTION-SW` PIC X(01).

            *   *Description:* Pricer Option Switch.  Used to determine if all tables or just the provider record is passed

                *   `ALL-TABLES-PASSED` VALUE 'A'.

                    *   *Description:* All tables passed option

                *   `PROV-RECORD-PASSED` VALUE 'P'.

                    *   *Description:* Provider record passed option.

        *   `PPS-VERSIONS`:

            *   `PPDRV-VERSION` PIC X(05).

                *   *Description:* Version of the PPDRV program.

    *   `PROV-NEW-HOLD`: This is the Provider record passed to the program

        *   `PROV-NEWREC-HOLD1`:

            *   `P-NEW-NPI10`:

                *   `P-NEW-NPI8` PIC X(08).

                    *   *Description:* New NPI (first 8 characters).

                *   `P-NEW-NPI-FILLER` PIC X(02).

                    *   *Description:* Filler for the new NPI.

            *   `P-NEW-PROVIDER-NO`:

                *   `P-NEW-STATE` PIC 9(02).

                    *   *Description:* New State.

                *   `FILLER` PIC X(04).

                    *   *Description:* Filler.

            *   `P-NEW-DATE-DATA`:

                *   `P-NEW-EFF-DATE`:

                    *   `P-NEW-EFF-DT-CC` PIC 9(02).

                        *   *Description:* New Effective Date Century Code.

                    *   `P-NEW-EFF-DT-YY` PIC 9(02).

                        *   *Description:* New Effective Date Year.

                    *   `P-NEW-EFF-DT-MM` PIC 9(02).

                        *   *Description:* New Effective Date Month.

                    *   `P-NEW-EFF-DT-DD` PIC 9(02).

                        *   *Description:* New Effective Date Day.

                *   `P-NEW-FY-BEGIN-DATE`:

                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Century Code.

                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Year.

                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Month.

                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Day.

                *   `P-NEW-REPORT-DATE`:

                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).

                        *   *Description:* New Report Date Century Code.

                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).

                        *   *Description:* New Report Date Year.

                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).

                        *   *Description:* New Report Date Month.

                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).

                        *   *Description:* New Report Date Day.

                *   `P-NEW-TERMINATION-DATE`:

                    *   `P-NEW-TERM-DT-CC` PIC 9(02).

                        *   *Description:* New Termination Date Century Code.

                    *   `P-NEW-TERM-DT-YY` PIC 9(02).

                        *   *Description:* New Termination Date Year.

                    *   `P-NEW-TERM-DT-MM` PIC 9(02).

                        *   *Description:* New Termination Date Month.

                    *   `P-NEW-TERM-DT-DD` PIC 9(02).

                        *   *Description:* New Termination Date Day.

            *   `P-NEW-WAIVER-CODE` PIC X(01).

                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.

                    *   *Description:* New Waiver State.

            *   `P-NEW-INTER-NO` PIC 9(05).

                *   *Description:* New Internal Number.

            *   `P-NEW-PROVIDER-TYPE` PIC X(02).

                *   *Description:* New Provider Type.

            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01).

                *   *Description:* New Current Census Division.

            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).

                *   *Description:* New Current Division (redefines the census division).

            *   `P-NEW-MSA-DATA`:

                *   `P-NEW-CHG-CODE-INDEX` PIC X.

                    *   *Description:* New Charge Code Index.

                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT.

                    *   *Description:* New Geo Location MSA X.

                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).

                    *   *Description:* New Geo Location MSA 9 (redefines the X version).

                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT.

                    *   *Description:* New Wage Index Location MSA.

                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT.

                    *   *Description:* New Standard Amount Location MSA.

                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.

                    *   *Description:* New Standard Amount Location MSA 9 (redefines the X version).

                    *   `P-NEW-RURAL-1ST`:

                        *   `P-NEW-STAND-RURAL` PIC XX.

                            *   *Description:* New Standard Rural.

                                *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.

                                    *   *Description:* Standard Rural Check.

                        *   `P-NEW-RURAL-2ND` PIC XX.

                            *   *Description:* New Rural 2nd.

            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX.

                *   *Description:* New Sol Com Dep Hosp Year.

            *   `P-NEW-LUGAR` PIC X.

                *   *Description:* New Lugar.

            *   `P-NEW-TEMP-RELIEF-IND` PIC X.

                *   *Description:* New Temporary Relief Indicator.

            *   `P-NEW-FED-PPS-BLEND-IND` PIC X.

                *   *Description:* New Federal PPS Blend Indicator.

            *   `FILLER` PIC X(05).

                *   *Description:* Filler.

        *   `PROV-NEWREC-HOLD2`:

            *   `P-NEW-VARIABLES`:

                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).

                    *   *Description:* New Facility Specific Rate.

                *   `P-NEW-COLA` PIC 9(01)V9(03).

                    *   *Description:* New COLA.

                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04).

                    *   *Description:* New Intern Ratio.

                *   `P-NEW-BED-SIZE` PIC 9(05).

                    *   *Description:* New Bed Size.

                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03).

                    *   *Description:* New Operating Cost to Charge Ratio.

                *   `P-NEW-CMI` PIC 9(01)V9(04).

                    *   *Description:* New CMI.

                *   `P-NEW-SSI-RATIO` PIC V9(04).

                    *   *Description:* New SSI Ratio.

                *   `P-NEW-MEDICAID-RATIO` PIC V9(04).

                    *   *Description:* New Medicaid Ratio.

                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01).

                    *   *Description:* New PPS Blend Year Indicator.

                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05).

                    *   *Description:* New PRUF Update Factor.

                *   `P-NEW-DSH-PERCENT` PIC V9(04).

                    *   *Description:* New DSH Percent.

                *   `P-NEW-FYE-DATE` PIC X(08).

                    *   *Description:* New FYE Date.

            *   `FILLER` PIC X(23).

                *   *Description:* Filler.

        *   `PROV-NEWREC-HOLD3`:

            *   `P-NEW-PASS-AMT-DATA`:

                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99.

                    *   *Description:* New Pass Amount Capital.

                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99.

                    *   *Description:* New Pass Amount Direct Med Ed.

                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99.

                    *   *Description:* New Pass Amount Organ Acq.

                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99.

                    *   *Description:* New Pass Amount Plus Misc.

            *   `P-NEW-CAPI-DATA`:

                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X.

                    *   *Description:* New CAPI PPS Pay Code.

                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99.

                    *   *Description:* New CAPI Hospital Specific Rate.

                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99.

                    *   *Description:* New CAPI Old Harm Rate.

                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999.

                    *   *Description:* New CAPI New Harm Ratio.

                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999.

                    *   *Description:* New CAPI Cost to Charge Ratio.

                *   `P-NEW-CAPI-NEW-HOSP` PIC X.

                    *   *Description:* New CAPI New Hospital.

                *   `P-NEW-CAPI-IME` PIC 9V9999.

                    *   *Description:* New CAPI IME.

                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99.

                    *   *Description:* New CAPI Exceptions.

            *   `FILLER` PIC X(22).

                *   *Description:* Filler.

    *   `WAGE-NEW-INDEX-RECORD`:

        *   `W-MSA` PIC X(4).

            *   *Description:* Wage Index MSA.

        *   `W-EFF-DATE` PIC X(8).

            *   *Description:* Effective Date for the Wage Index.

        *   `W-WAGE-INDEX1` PIC S9(02)V9(04).

            *   *Description:* Wage Index 1.

        *   `W-WAGE-INDEX2` PIC S9(02)V9(04).

            *   *Description:* Wage Index 2.

        *   `W-WAGE-INDEX3` PIC S9(02)V9(04).

            *   *Description:* Wage Index 3.

**COBOL Program: LTCAL042**

*   **Files Accessed:**

    *   No explicit `SELECT` statements, but likely interactions with external data sources as in LTCAL032.
        *   **COPY LTDRG031:** This suggests the program uses a copybook (likely containing data definitions for DRG codes, weights, and average lengths of stay)
        *   **PROV-NEW-HOLD, WAGE-NEW-INDEX-RECORD:** This suggests the program uses provider and wage index records
*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.

        *   *Description:*  A descriptive string, likely used for debugging or identification purposes.

    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.

        *   *Description:*  Indicates the version of the calculation logic.

    *   `HOLD-PPS-COMPONENTS`:

        *   `H-LOS` PIC 9(03).

            *   *Description:* Length of Stay from input

        *   `H-REG-DAYS` PIC 9(03).

            *   *Description:* Regular days.

        *   `H-TOTAL-DAYS` PIC 9(05).

            *   *Description:* Total days.

        *   `H-SSOT` PIC 9(02).

            *   *Description:* Short Stay Outlier Threshold.

        *   `H-BLEND-RTC` PIC 9(02).

            *   *Description:* Blend Return Code.

        *   `H-BLEND-FAC` PIC 9(01)V9(01).

            *   *Description:* Blend Facility Percentage.

        *   `H-BLEND-PPS` PIC 9(01)V9(01).

            *   *Description:* Blend PPS Percentage.

        *   `H-SS-PAY-AMT` PIC 9(07)V9(02).

            *   *Description:* Short Stay Payment Amount.

        *   `H-SS-COST` PIC 9(07)V9(02).

            *   *Description:* Short Stay Cost.

        *   `H-LABOR-PORTION` PIC 9(07)V9(06).

            *   *Description:* Labor Portion of the payment calculation.

        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06).

            *   *Description:* Non-Labor Portion of the payment calculation.

        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02).

            *   *Description:* Fixed Loss Amount for outlier calculation.

        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02).

            *   *Description:* New Facility Specific Rate.

        *   `H-LOS-RATIO` PIC 9(01)V9(05).

            *   *Description:* Length of Stay Ratio.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the input data passed *to* the program.

        *   `B-NPI10`:

            *   `B-NPI8` PIC X(08).

                *   *Description:* National Provider Identifier (NPI) - first 8 characters.

            *   `B-NPI-FILLER` PIC X(02).

                *   *Description:* Filler for the NPI.

        *   `B-PROVIDER-NO` PIC X(06).

            *   *Description:* Provider Number.

        *   `B-PATIENT-STATUS` PIC X(02).

            *   *Description:* Patient Status.

        *   `B-DRG-CODE` PIC X(03).

            *   *Description:* Diagnosis Related Group (DRG) Code.

        *   `B-LOS` PIC 9(03).

            *   *Description:* Length of Stay (in days).

        *   `B-COV-DAYS` PIC 9(03).

            *   *Description:* Covered Days.

        *   `B-LTR-DAYS` PIC 9(02).

            *   *Description:* Lifetime Reserve Days.

        *   `B-DISCHARGE-DATE`:

            *   `B-DISCHG-CC` PIC 9(02).

                *   *Description:* Discharge Century Code.

            *   `B-DISCHG-YY` PIC 9(02).

                *   *Description:* Discharge Year (last two digits).

            *   `B-DISCHG-MM` PIC 9(02).

                *   *Description:* Discharge Month.

            *   `B-DISCHG-DD` PIC 9(02).

                *   *Description:* Discharge Day.

        *   `B-COV-CHARGES` PIC 9(07)V9(02).

            *   *Description:* Covered Charges.

        *   `B-SPEC-PAY-IND` PIC X(01).

            *   *Description:* Special Payment Indicator.

        *   `FILLER` PIC X(13).

            *   *Description:* Filler.

    *   `PPS-DATA-ALL`: This is the output data passed *back* to the calling program. It contains the results of the PPS (Prospective Payment System) calculation.

        *   `PPS-RTC` PIC 9(02).

            *   *Description:* Return Code.  Indicates the result of the calculation (e.g., success, various error conditions, and payment types).

        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02).

            *   *Description:* Charge Threshold.

        *   `PPS-DATA`:

            *   `PPS-MSA` PIC X(04).

                *   *Description:* Metropolitan Statistical Area (MSA) code.

            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04).

                *   *Description:* Wage Index.

            *   `PPS-AVG-LOS` PIC 9(02)V9(01).

                *   *Description:* Average Length of Stay.

            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04).

                *   *Description:* Relative Weight for the DRG.

            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Outlier Payment Amount.

            *   `PPS-LOS` PIC 9(03).

                *   *Description:* Length of stay.

            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* DRG Adjusted Payment Amount.

            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Federal Payment Amount.

            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02).

                *   *Description:* Final Payment Amount.

            *   `PPS-FAC-COSTS` PIC 9(07)V9(02).

                *   *Description:* Facility Costs.

            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02).

                *   *Description:* New Facility Specific Rate.

            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02).

                *   *Description:* Outlier Threshold.

            *   `PPS-SUBM-DRG-CODE` PIC X(03).

                *   *Description:* Submitted DRG Code.

            *   `PPS-CALC-VERS-CD` PIC X(05).

                *   *Description:* Calculation Version Code.

            *   `PPS-REG-DAYS-USED` PIC 9(03).

                *   *Description:* Regular Days Used.

            *   `PPS-LTR-DAYS-USED` PIC 9(03).

                *   *Description:* Lifetime Reserve Days Used.

            *   `PPS-BLEND-YEAR` PIC 9(01).

                *   *Description:* Blend Year Indicator.

            *   `PPS-COLA` PIC 9(01)V9(03).

                *   *Description:* Cost of Living Adjustment.

            *   `FILLER` PIC X(04).

                *   *Description:* Filler.

        *   `PPS-OTHER-DATA`:

            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05).

                *   *Description:* National Labor Percentage.

            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05).

                *   *Description:* National Non-Labor Percentage.

            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02).

                *   *Description:* Standard Federal Rate.

            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03).

                *   *Description:* Budget Neutrality Rate.

            *   `FILLER` PIC X(20).

                *   *Description:* Filler.

        *   `PPS-PC-DATA`:

            *   `PPS-COT-IND` PIC X(01).

                *   *Description:* Cost Outlier Indicator.

            *   `FILLER` PIC X(20).

                *   *Description:* Filler.

    *   `PRICER-OPT-VERS-SW`:

        *   `PRICER-OPTION-SW` PIC X(01).

            *   *Description:* Pricer Option Switch.  Used to determine if all tables or just the provider record is passed

                *   `ALL-TABLES-PASSED` VALUE 'A'.

                    *   *Description:* All tables passed option

                *   `PROV-RECORD-PASSED` VALUE 'P'.

                    *   *Description:* Provider record passed option.

        *   `PPS-VERSIONS`:

            *   `PPDRV-VERSION` PIC X(05).

                *   *Description:* Version of the PPDRV program.

    *   `PROV-NEW-HOLD`: This is the Provider record passed to the program

        *   `PROV-NEWREC-HOLD1`:

            *   `P-NEW-NPI10`:

                *   `P-NEW-NPI8` PIC X(08).

                    *   *Description:* New NPI (first 8 characters).

                *   `P-NEW-NPI-FILLER` PIC X(02).

                    *   *Description:* Filler for the new NPI.

            *   `P-NEW-PROVIDER-NO`:

                *   `P-NEW-STATE` PIC 9(02).

                    *   *Description:* New State.

                *   `FILLER` PIC X(04).

                    *   *Description:* Filler.

            *   `P-NEW-DATE-DATA`:

                *   `P-NEW-EFF-DATE`:

                    *   `P-NEW-EFF-DT-CC` PIC 9(02).

                        *   *Description:* New Effective Date Century Code.

                    *   `P-NEW-EFF-DT-YY` PIC 9(02).

                        *   *Description:* New Effective Date Year.

                    *   `P-NEW-EFF-DT-MM` PIC 9(02).

                        *   *Description:* New Effective Date Month.

                    *   `P-NEW-EFF-DT-DD` PIC 9(02).

                        *   *Description:* New Effective Date Day.

                *   `P-NEW-FY-BEGIN-DATE`:

                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Century Code.

                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Year.

                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Month.

                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).

                        *   *Description:* New Fiscal Year Begin Date Day.

                *   `P-NEW-REPORT-DATE`:

                    *   `P-NEW-REPORT