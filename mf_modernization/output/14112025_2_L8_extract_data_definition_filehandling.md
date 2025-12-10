Here's an analysis of the COBOL programs provided, detailing file access, data structures, and their descriptions:

**Program: LTCAL032**

*   **Files Accessed:**

    *   No explicit file access statements are present in the code. However, it's highly likely that this program *interacts* with external data sources through the `COPY LTDRG031.` statement, which includes the DRG table information. The program also uses Provider and Wage Index data which are likely accessed via the `USING` clause.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.
        *   Description: A descriptive string identifying the program and the storage area.
    *   `CAL-VERSION` PIC X(05) VALUE 'C03.2'.
        *   Description:  Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description:  A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03).  Length of Stay.
        *   `H-REG-DAYS` PIC 9(03). Regular Days.
        *   `H-TOTAL-DAYS` PIC 9(05). Total Days.
        *   `H-SSOT` PIC 9(02). Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02). Blend Return Code.
        *   `H-BLEND-FAC` PIC 9(01)V9(01). Blend Facility Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01). Blend PPS Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02). Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). Labor Portion of Payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). Non-Labor Portion of Payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). Fixed Loss Amount for Outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:
        *   Description:  This is the main input structure, representing the billing information passed *to* the LTCAL032 subroutine from a calling program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08).  National Provider Identifier (NPI) - first 8 characters.
            *   `B-NPI-FILLER` PIC X(02).  National Provider Identifier (NPI) - last 2 characters.
        *   `B-PROVIDER-NO` PIC X(06). Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02). Patient Status.
        *   `B-DRG-CODE` PIC X(03).  Diagnosis Related Group (DRG) Code.
        *   `B-LOS` PIC 9(03). Length of Stay.
        *   `B-COV-DAYS` PIC 9(03). Covered Days.
        *   `B-LTR-DAYS` PIC 9(02). Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02). Discharge Date - Century/Year (CC).
            *   `B-DISCHG-YY` PIC 9(02). Discharge Date - Year (YY).
            *   `B-DISCHG-MM` PIC 9(02). Discharge Date - Month (MM).
            *   `B-DISCHG-DD` PIC 9(02). Discharge Date - Day (DD).
        *   `B-COV-CHARGES` PIC 9(07)V9(02). Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01). Special Payment Indicator.
        *   `FILLER` PIC X(13). Unused space.
    *   `PPS-DATA-ALL`:
        *   Description:  This structure is used to pass *back* the calculated results from the LTCAL032 subroutine to the calling program. It contains the PPS related information.
        *   `PPS-RTC` PIC 9(02). Return Code.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). Charge Threshold.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). Relative Weight of DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03). Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03). Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05). Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03). Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03). Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01). Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03). Cost of Living Adjustment (COLA).
            *   `FILLER` PIC X(04). Unused space.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). Budget Neutrality Rate.
            *   `FILLER` PIC X(20). Unused space.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01). Cost Outlier Indicator.
            *   `FILLER` PIC X(20). Unused space.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Used to pass version information of the tables.
        *   `PRICER-OPTION-SW` PIC X(01).  Indicates if all tables are passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.  If 'A', all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'. If 'P', provider record is passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05). Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description:  This structure is used to pass the provider specific information to the LTCAL032 subroutine.
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).  Provider's NPI - first 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02).  Provider's NPI - last 2 characters.
            *   `P-NEW-PROVIDER-NO` PIC X(06). Provider Number.
            *   `P-NEW-STATE` PIC 9(02). State.
            *   `FILLER` PIC X(04). Unused space.
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).  Effective Date - Century/Year (CC).
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).  Effective Date - Year (YY).
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).  Effective Date - Month (MM).
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).  Effective Date - Day (DD).
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02). Fiscal Year Begin Date - Century/Year (CC).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02). Fiscal Year Begin Date - Year (YY).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02). Fiscal Year Begin Date - Month (MM).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02). Fiscal Year Begin Date - Day (DD).
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02). Report Date - Century/Year (CC).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02). Report Date - Year (YY).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02). Report Date - Month (MM).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02). Report Date - Day (DD).
                *   `P-NEW-TERMINATION-DATE`:
                    *   `P-NEW-TERM-DT-CC` PIC 9(02). Termination Date - Century/Year (CC).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02). Termination Date - Year (YY).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02). Termination Date - Month (MM).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02). Termination Date - Day (DD).
            *   `P-NEW-WAIVER-CODE` PIC X(01). Waiver Code.
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'. Waiver State.
            *   `P-NEW-INTER-NO` PIC 9(05). Intern Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02). Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01). Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).  Redefines the census division.
            *   `P-NEW-MSA-DATA`:
                *   `P-NEW-CHG-CODE-INDEX` PIC X. Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04). Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).  Redefines Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04). Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04). Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA:
                    *   `P-NEW-RURAL-1ST`:
                        *   `P-NEW-STAND-RURAL` PIC XX. Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '. Standard Rural Check.
                    *   `P-NEW-RURAL-2ND` PIC XX. Rural.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX. Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` PIC X. Location.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X. Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X. Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).  Unused space.
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03). Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04). Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05). Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03). Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04). Case Mix Index.
                *   `P-NEW-SSI-RATIO` PIC V9(04). Supplemental Security Income Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04). Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01). PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05). Proof Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04). Disproportionate Share Hospital (DSH) Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08). Fiscal Year End Date.
            *   `FILLER` PIC X(23). Unused space.
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99. Pass Through Amount - Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` PIC 9(04)V99. Pass Through Amount - Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` PIC 9(04)V99. Pass Through Amount - Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` PIC 9(04)V99. Pass Through Amount - Plus Miscellaneous.
            *   `P-NEW-CAPI-DATA`:
                *   `P-NEW-CAPI-PPS-PAY-CODE` PIC X. Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` PIC 9(04)V99. Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` PIC 9(04)V99. Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` PIC 9(01)V9999. Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` PIC 9V999. Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` PIC X. Capital New Hospital.
                *   `P-NEW-CAPI-IME` PIC 9V9999. Capital IME.
                *   `P-NEW-CAPI-EXCEPTIONS` PIC 9(04)V99. Capital Exceptions.
            *   `FILLER` PIC X(22). Unused space.
    *   `WAGE-NEW-INDEX-RECORD`:
        *   Description:  This structure is used to pass the wage index record to the LTCAL032 subroutine.
        *   `W-MSA` PIC X(4). MSA Code.
        *   `W-EFF-DATE` PIC X(8). Effective Date.
        *   `W-WAGE-INDEX1` PIC S9(02)V9(04). Wage Index 1.
        *   `W-WAGE-INDEX2` PIC S9(02)V9(04). Wage Index 2.
        *   `W-WAGE-INDEX3` PIC S9(02)V9(04). Wage Index 3.

**Program: LTCAL042**

*   **Files Accessed:**

    *   No explicit file access statements are present in the code.  Similar to LTCAL032, it relies on `COPY LTDRG031.` and likely uses `USING` to get Provider and Wage Index data.
*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.
        *   Description: A descriptive string identifying the program and the storage area.
    *   `CAL-VERSION` PIC X(05) VALUE 'C04.2'.
        *   Description:  Indicates the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:
        *   Description: A group of variables used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   `H-LOS` PIC 9(03). Length of Stay.
        *   `H-REG-DAYS` PIC 9(03). Regular Days.
        *   `H-TOTAL-DAYS` PIC 9(05). Total Days.
        *   `H-SSOT` PIC 9(02). Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` PIC 9(02). Blend Return Code.
        *   `H-BLEND-FAC` PIC 9(01)V9(01). Blend Facility Percentage.
        *   `H-BLEND-PPS` PIC 9(01)V9(01). Blend PPS Percentage.
        *   `H-SS-PAY-AMT` PIC 9(07)V9(02). Short Stay Payment Amount.
        *   `H-SS-COST` PIC 9(07)V9(02). Short Stay Cost.
        *   `H-LABOR-PORTION` PIC 9(07)V9(06). Labor Portion of Payment.
        *   `H-NONLABOR-PORTION` PIC 9(07)V9(06). Non-Labor Portion of Payment.
        *   `H-FIXED-LOSS-AMT` PIC 9(07)V9(02). Fixed Loss Amount for Outlier calculations.
        *   `H-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). New Facility Specific Rate.
        *   `H-LOS-RATIO` PIC 9(01)V9(05). Length of Stay Ratio.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:
        *   Description: This is the main input structure, representing the billing information passed *to* the LTCAL042 subroutine from a calling program.
        *   `B-NPI10`:
            *   `B-NPI8` PIC X(08). National Provider Identifier (NPI) - first 8 characters.
            *   `B-NPI-FILLER` PIC X(02). National Provider Identifier (NPI) - last 2 characters.
        *   `B-PROVIDER-NO` PIC X(06). Provider Number.
        *   `B-PATIENT-STATUS` PIC X(02). Patient Status.
        *   `B-DRG-CODE` PIC X(03). Diagnosis Related Group (DRG) Code.
        *   `B-LOS` PIC 9(03). Length of Stay.
        *   `B-COV-DAYS` PIC 9(03). Covered Days.
        *   `B-LTR-DAYS` PIC 9(02). Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:
            *   `B-DISCHG-CC` PIC 9(02). Discharge Date - Century/Year (CC).
            *   `B-DISCHG-YY` PIC 9(02). Discharge Date - Year (YY).
            *   `B-DISCHG-MM` PIC 9(02). Discharge Date - Month (MM).
            *   `B-DISCHG-DD` PIC 9(02). Discharge Date - Day (DD).
        *   `B-COV-CHARGES` PIC 9(07)V9(02). Covered Charges.
        *   `B-SPEC-PAY-IND` PIC X(01). Special Payment Indicator.
        *   `FILLER` PIC X(13). Unused space.
    *   `PPS-DATA-ALL`:
        *   Description:  This structure is used to pass *back* the calculated results from the LTCAL042 subroutine to the calling program. It contains the PPS related information.
        *   `PPS-RTC` PIC 9(02). Return Code.
        *   `PPS-CHRG-THRESHOLD` PIC 9(07)V9(02). Charge Threshold.
        *   `PPS-DATA`:
            *   `PPS-MSA` PIC X(04).  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` PIC 9(02)V9(04). Wage Index.
            *   `PPS-AVG-LOS` PIC 9(02)V9(01). Average Length of Stay.
            *   `PPS-RELATIVE-WGT` PIC 9(01)V9(04). Relative Weight of DRG.
            *   `PPS-OUTLIER-PAY-AMT` PIC 9(07)V9(02). Outlier Payment Amount.
            *   `PPS-LOS` PIC 9(03). Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` PIC 9(07)V9(02). DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` PIC 9(07)V9(02). Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` PIC 9(07)V9(02). Final Payment Amount.
            *   `PPS-FAC-COSTS` PIC 9(07)V9(02). Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` PIC 9(07)V9(02). New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` PIC 9(07)V9(02). Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` PIC X(03). Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` PIC X(05). Calculation Version Code.
            *   `PPS-REG-DAYS-USED` PIC 9(03). Regular Days Used.
            *   `PPS-LTR-DAYS-USED` PIC 9(03). Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` PIC 9(01). Blend Year Indicator.
            *   `PPS-COLA` PIC 9(01)V9(03). Cost of Living Adjustment (COLA).
            *   `FILLER` PIC X(04). Unused space.
        *   `PPS-OTHER-DATA`:
            *   `PPS-NAT-LABOR-PCT` PIC 9(01)V9(05). National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` PIC 9(01)V9(05). National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` PIC 9(05)V9(02). Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` PIC 9(01)V9(03). Budget Neutrality Rate.
            *   `FILLER` PIC X(20). Unused space.
        *   `PPS-PC-DATA`:
            *   `PPS-COT-IND` PIC X(01). Cost Outlier Indicator.
            *   `FILLER` PIC X(20). Unused space.
    *   `PRICER-OPT-VERS-SW`:
        *   Description:  Used to pass version information of the tables.
        *   `PRICER-OPTION-SW` PIC X(01).  Indicates if all tables are passed.
            *   `ALL-TABLES-PASSED` VALUE 'A'.  If 'A', all tables are passed.
            *   `PROV-RECORD-PASSED` VALUE 'P'. If 'P', provider record is passed.
        *   `PPS-VERSIONS`:
            *   `PPDRV-VERSION` PIC X(05). Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:
        *   Description:  This structure is used to pass the provider specific information to the LTCAL042 subroutine.
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`:
                *   `P-NEW-NPI8` PIC X(08).  Provider's NPI - first 8 characters.
                *   `P-NEW-NPI-FILLER` PIC X(02).  Provider's NPI - last 2 characters.
            *   `P-NEW-PROVIDER-NO` PIC X(06). Provider Number.
            *   `P-NEW-STATE` PIC 9(02). State.
            *   `FILLER` PIC X(04). Unused space.
            *   `P-NEW-DATE-DATA`:
                *   `P-NEW-EFF-DATE`:
                    *   `P-NEW-EFF-DT-CC` PIC 9(02).  Effective Date - Century/Year (CC).
                    *   `P-NEW-EFF-DT-YY` PIC 9(02).  Effective Date - Year (YY).
                    *   `P-NEW-EFF-DT-MM` PIC 9(02).  Effective Date - Month (MM).
                    *   `P-NEW-EFF-DT-DD` PIC 9(02).  Effective Date - Day (DD).
                *   `P-NEW-FY-BEGIN-DATE`:
                    *   `P-NEW-FY-BEG-DT-CC` PIC 9(02). Fiscal Year Begin Date - Century/Year (CC).
                    *   `P-NEW-FY-BEG-DT-YY` PIC 9(02). Fiscal Year Begin Date - Year (YY).
                    *   `P-NEW-FY-BEG-DT-MM` PIC 9(02). Fiscal Year Begin Date - Month (MM).
                    *   `P-NEW-FY-BEG-DT-DD` PIC 9(02). Fiscal Year Begin Date - Day (DD).
                *   `P-NEW-REPORT-DATE`:
                    *   `P-NEW-REPORT-DT-CC` PIC 9(02). Report Date - Century/Year (CC).
                    *   `P-NEW-REPORT-DT-YY` PIC 9(02). Report Date - Year (YY).
                    *   `P-NEW-REPORT-DT-MM` PIC 9(02). Report Date - Month (MM).
                    *   `P-NEW-REPORT-DT-DD` PIC 9(02). Report Date - Day (DD).
                *   `P-NEW-TERMINATION-DATE`:
                    *   `P-NEW-TERM-DT-CC` PIC 9(02). Termination Date - Century/Year (CC).
                    *   `P-NEW-TERM-DT-YY` PIC 9(02). Termination Date - Year (YY).
                    *   `P-NEW-TERM-DT-MM` PIC 9(02). Termination Date - Month (MM).
                    *   `P-NEW-TERM-DT-DD` PIC 9(02). Termination Date - Day (DD).
            *   `P-NEW-WAIVER-CODE` PIC X(01). Waiver Code.
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'. Waiver State.
            *   `P-NEW-INTER-NO` PIC 9(05). Intern Number.
            *   `P-NEW-PROVIDER-TYPE` PIC X(02). Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` PIC 9(01). Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).  Redefines the census division.
            *   `P-NEW-MSA-DATA`:
                *   `P-NEW-CHG-CODE-INDEX` PIC X. Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` PIC X(04). Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).  Redefines Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` PIC X(04). Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` PIC X(04). Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA:
                    *   `P-NEW-RURAL-1ST`:
                        *   `P-NEW-STAND-RURAL` PIC XX. Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '. Standard Rural Check.
                    *   `P-NEW-RURAL-2ND` PIC XX. Rural.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` PIC XX. Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` PIC X. Location.
            *   `P-NEW-TEMP-RELIEF-IND` PIC X. Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` PIC X. Federal PPS Blend Indicator.
            *   `FILLER` PIC X(05).  Unused space.
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` PIC 9(05)V9(02). Facility Specific Rate.
                *   `P-NEW-COLA` PIC 9(01)V9(03). Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` PIC 9(01)V9(04). Intern Ratio.
                *   `P-NEW-BED-SIZE` PIC 9(05). Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` PIC 9(01)V9(03). Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` PIC 9(01)V9(04). Case Mix Index.
                *   `P-NEW-SSI-RATIO` PIC V9(04). Supplemental Security Income Ratio.
                *   `P-NEW-MEDICAID-RATIO` PIC V9(04). Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` PIC 9(01). PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` PIC 9(01)V9(05). Proof Update Factor.
                *   `P-NEW-DSH-PERCENT` PIC V9(04). Disproportionate Share Hospital (DSH) Percentage.
                *   `P-NEW-FYE-DATE` PIC X(08). Fiscal Year End Date.
            *   `FILLER` PIC X(23). Unused space.
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` PIC 9(04)V99. Pass Through Amount - Capital.
                *   `P-NEW-PASS