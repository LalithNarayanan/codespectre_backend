Here's the analysis of the provided COBOL programs:

**Program: LTCAL032**

*   **Files Accessed:**
    *   No explicit file access is evident in the provided code. However, the program likely interacts with external data sources through the `COPY LTDRG031.` statement, which includes DRG code and related values.
*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'. -  A descriptive string for debugging or identification purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'. -  Stores the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03). -  Length of Stay (LOS) from input.
        *   `H-REG-DAYS` PIC 9(03). - Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05). - Total days.
        *   `H-SSOT` PIC 9(02). -  Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02). - Blend Year Return Code.
        *   `H-BLEND-FAC` PIC 9(01)V9(01). - Blend Facility Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01). - Blend PPS Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). - Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02). - Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). - Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). - Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). - Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - New Facility Specific Rate.
*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:  This is the main input structure, representing the bill data passed to the program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08). - National Provider Identifier (NPI) - 8 characters.
            *   `B-NPI-FILLER` PIC X(02). - Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06). - Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02). - Patient Status.
        *   `B-DRG-CODE` PIC X(03). - Diagnosis Related Group (DRG) Code.
        *   `B-LOS` PIC 9(03). - Length of Stay.
        *   `B-COV-DAYS` PIC 9(03). - Covered Days.
        *   `B-LTR-DAYS` PIC 9(02). - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02). - Discharge Century/Code.
            *   `B-DISCHG-YY` PIC 9(02). - Discharge Year.
            *   `B-DISCHG-MM` PIC 9(02). - Discharge Month.
            *   `B-DISCHG-DD` PIC 9(02). - Discharge Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02). - Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01). - Special Pay Indicator.
        *   `FILLER` PIC X(13). - Filler.
    *   `PPS-DATA-ALL`:  This is the main output structure, containing the calculated PPS data.
        *   `PPS-RTC` PIC 9(02). - Return Code (PPS).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). - Charge Threshold.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04). - Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). - Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). - Relative Weight.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). - Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03). - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). - Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03). - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05). - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03). - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03). - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01). - Blend Year.
            *   `PPS-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment.
            *   `FILLER` PIC X(04). - Filler.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). - National Non-labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). - Budget Neutrality Rate.
            *   `FILLER` PIC X(20). - Filler.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01). - Cost Outlier Indicator.
            *   `FILLER` PIC X(20). - Filler.
    *   `PRICER-OPT-VERS-SW`: Used for passing versions of the LTDRV programs.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   `ALL-TABLES-PASSED` VALUE 'A'.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
    *   `PROV-NEW-HOLD`: This structure holds provider-specific data.
        *   `PROV-NEWREC-HOLD1`: Contains provider information.
            *   `P-NEW-NPI10`: Provider NPI.
                *   `P-NEW-NPI8` PIC X(08). - NPI 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02). - NPI Filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06). - Provider Number.
                *   `P-NEW-STATE` PIC 9(02). - State.
                *   `FILLER` PIC X(04). - Filler.
            *   `P-NEW-DATE-DATA`: Date-related fields.
                *   `P-NEW-EFF-DATE`: Effective Date
                    *   `P-NEW-EFF-DT-CC` PIC 9(02). - Effective Date - Century/Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02). - Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02). - Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02). - Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
            *   `P-NEW-INTER-NO` PIC 9(05). - Internal Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02). - Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01). - Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
            *   `P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data.
                *   `P-NEW-CHG-CODE-INDEX` PIC X. - Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT. - Geographic Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT. - Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT. - Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`:
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                        *   `P-NEW-RURAL-2ND` PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX. - Sole Community, Dependent, Hospital Year.
            *   `P-NEW-LUGAR` PIC X. - Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X. - Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X. - Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05). - Filler.
        *   `PROV-NEWREC-HOLD2`: Contains provider-specific variables.
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04). - Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05). - Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03). - Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04). - Case Mix Index.
                *   `P-NEW-SSI-RATIO` PIC V9(04). - SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04). - Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01). - PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05). - Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04). - DSH Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08). - Fiscal Year End Date.
            *   `FILLER` PIC X(23). - Filler.
        *   `PROV-NEWREC-HOLD3`: Contains pass-through amounts.
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99. - Capital Pass-Through Amount.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99. - Direct Medical Education Pass-Through.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99. - Organ Acquisition Pass-Through.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99. - Plus Miscellaneous Pass-Through.
            *   `P-NEW-CAPI-DATA`: Capital Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X. - Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99. - Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99. - Old HARM Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999. - New HARM Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999. - Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X. - New Hospital Indicator.
                *   `P-NEW-CAPI-IME` PIC 9V9999. - IME.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99. - Exceptions.
            *   `FILLER` PIC X(22). - Filler.
    *   `WAGE-NEW-INDEX-RECORD`:  Wage index data.
        *   `W-MSA` PIC X(4). - MSA (Metropolitan Statistical Area).
        *   `W-EFF-DATE` PIC X(8). - Effective Date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04). - Wage Index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04). - Wage Index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04). - Wage Index 3.

**Program: LTCAL042**

*   **Files Accessed:**
    *   No explicit file access is evident in the provided code. However, the program likely interacts with external data sources through the `COPY LTDRG031.` statement, which includes DRG code and related values.
*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'. -  A descriptive string for debugging or identification purposes.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'. -  Stores the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   `H-LOS` PIC 9(03). -  Length of Stay (LOS) from input.
        *   `H-REG-DAYS` PIC 9(03). - Regular days.
        *   `H-TOTAL-DAYS` PIC 9(05). - Total days.
        *   `H-SSOT` PIC 9(02). -  Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02). - Blend Year Return Code.
        *   `H-BLEND-FAC` PIC 9(01)V9(01). - Blend Facility Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01). - Blend PPS Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). - Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02). - Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). - Labor portion of the payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). - Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). - Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - New Facility Specific Rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05). - Length of Stay Ratio.
*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:  This is the main input structure, representing the bill data passed to the program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08). - National Provider Identifier (NPI) - 8 characters.
            *   `B-NPI-FILLER` PIC X(02). - Filler for NPI.
        *   `B-PROVIDER-NO` PIC X(06). - Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02). - Patient Status.
        *   `B-DRG-CODE` PIC X(03). - Diagnosis Related Group (DRG) Code.
        *   `B-LOS` PIC 9(03). - Length of Stay.
        *   `B-COV-DAYS` PIC 9(03). - Covered Days.
        *   `B-LTR-DAYS` PIC 9(02). - Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02). - Discharge Century/Code.
            *   `B-DISCHG-YY` PIC 9(02). - Discharge Year.
            *   `B-DISCHG-MM` PIC 9(02). - Discharge Month.
            *   `B-DISCHG-DD` PIC 9(02). - Discharge Day.
        *   `B-COV-CHARGES` PIC 9(07)V9(02). - Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01). - Special Pay Indicator.
        *   `FILLER` PIC X(13). - Filler.
    *   `PPS-DATA-ALL`:  This is the main output structure, containing the calculated PPS data.
        *   `PPS-RTC` PIC 9(02). - Return Code (PPS).
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). - Charge Threshold.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04). - Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). - Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). - Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). - Relative Weight.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). - Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03). - Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). - DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). - Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). - Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). - Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). - New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). - Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03). - Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05). - Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03). - Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03). - Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01). - Blend Year.
            *   `PPS-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment.
            *   `FILLER` PIC X(04). - Filler.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). - National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). - National Non-labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). - Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). - Budget Neutrality Rate.
            *   `FILLER` PIC X(20). - Filler.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01). - Cost Outlier Indicator.
            *   `FILLER` PIC X(20). - Filler.
    *   `PRICER-OPT-VERS-SW`: Used for passing versions of the LTDRV programs.
        *   `PRICER-OPTION-SW` PIC X(01).
            *   `ALL-TABLES-PASSED` VALUE 'A'.
            *   `PROV-RECORD-PASSED` VALUE 'P'.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05).
    *   `PROV-NEW-HOLD`: This structure holds provider-specific data.
        *   `PROV-NEWREC-HOLD1`: Contains provider information.
            *   `P-NEW-NPI10`: Provider NPI.
                *   `P-NEW-NPI8` PIC X(08). - NPI 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02). - NPI Filler.
            *   `P-NEW-PROVIDER-NO` PIC X(06). - Provider Number.
                *   `P-NEW-STATE` PIC 9(02). - State.
                *   `FILLER` PIC X(04). - Filler.
            *   `P-NEW-DATE-DATA`: Date-related fields.
                *   `P-NEW-EFF-DATE`: Effective Date
                    *   `P-NEW-EFF-DT-CC` PIC 9(02). - Effective Date - Century/Code.
                    *   `P-NEW-EFF-DT-YY` PIC 9(02). - Effective Date - Year.
                    *   `P-NEW-EFF-DT-MM` PIC 9(02). - Effective Date - Month.
                    *   `P-NEW-EFF-DT-DD` PIC 9(02). - Effective Date - Day.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02).
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02).
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` PIC 9(02).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02).
            *   `P-NEW-WAIVER-CODE` PIC X(01).
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'.
            *   `P-NEW-INTER-NO` PIC 9(05). - Internal Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02). - Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01). - Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
            *   `P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data.
                *   `P-NEW-CHG-CODE-INDEX` PIC X. - Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04) JUST RIGHT. - Geographic Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04) JUST RIGHT. - Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04) JUST RIGHT. - Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`:
                        *   `P-NEW-STAND-RURAL` PIC XX.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '.
                        *   `P-NEW-RURAL-2ND` PIC XX.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX. - Sole Community, Dependent, Hospital Year.
            *   `P-NEW-LUGAR` PIC X. - Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X. - Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X. - Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05). - Filler.
        *   `PROV-NEWREC-HOLD2`: Contains provider-specific variables.
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). - Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03). - Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04). - Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05). - Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03). - Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04). - Case Mix Index.
                *   `P-NEW-SSI-RATIO` PIC V9(04). - SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04). - Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01). - PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05). - Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04). - DSH Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08). - Fiscal Year End Date.
            *   `FILLER` PIC X(23). - Filler.
        *   `PROV-NEWREC-HOLD3`: Contains pass-through amounts.
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99. - Capital Pass-Through Amount.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99. - Direct Medical Education Pass-Through.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99. - Organ Acquisition Pass-Through.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99. - Plus Miscellaneous Pass-Through.
            *   `P-NEW-CAPI-DATA`: Capital Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X. - Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99. - Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99. - Old HARM Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999. - New HARM Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999. - Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X. - New Hospital Indicator.
                *   `P-NEW-CAPI-IME` PIC 9V9999. - IME.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99. - Exceptions.
            *   `FILLER` PIC X(22). - Filler.
    *   `WAGE-NEW-INDEX-RECORD`:  Wage index data.
        *   `W-MSA` PIC X(4). - MSA (Metropolitan Statistical Area).
        *   `W-EFF-DATE` PIC X(8