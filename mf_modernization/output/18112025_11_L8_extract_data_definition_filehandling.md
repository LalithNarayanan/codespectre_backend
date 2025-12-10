Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

**Program: LTCAL032**

*   **Files Accessed:**

    *   This program doesn't directly access any external files. However, it *includes* the `LTDRG031` copybook, which likely contains data used for DRG calculations.  This copybook can be considered a file (table) containing DRG information.

*   **Data Structures (WORKING-STORAGE SECTION):**

    *   `W-STORAGE-REF` (PIC X(46)):  A working storage variable that likely holds a program identification string.
    *   `CAL-VERSION` (PIC X(05)): Stores the version number of the calculation logic (e.g., 'C03.2').
    *   `HOLD-PPS-COMPONENTS`:  A group item used to hold intermediate calculation values related to PPS (Prospective Payment System) components.
        *   `H-LOS` (PIC 9(03)): Length of Stay (in days).
        *   `H-REG-DAYS` (PIC 9(03)): Regular Days
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total Days
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Factor for Facility Rate.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend Factor for PPS Payment.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion of payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-Labor Portion of payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed loss amount for outlier calculation.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
    *   (From copybook `LTDRG031`):  This section, included via `COPY LTDRG031`, likely defines a table or data structure containing DRG (Diagnosis Related Group) information. The exact structure is defined in `LTDRG031`
    *   `PPS-DATA-ALL`: A group item to hold all the PPS calculation results and related data that will be passed back to the calling program.
        *   `PPS-RTC` (PIC 9(02)): Return Code indicating the payment status.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charges Threshold
        *   `PPS-DATA`: A group item to hold PPS data.
            *   `PPS-MSA` (PIC X(04)):  Metropolitan Statistical Area code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage Index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay (used in return).
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular Days Used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year indicator.
            *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler
        *   `PPS-OTHER-DATA`: A group item for other PPS data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler
        *   `PPS-PC-DATA`: A group item for PPS PC data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler
    *   `PRICER-OPT-VERS-SW`: A group item for pricer option switch.
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'): Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates Provider record is passed.
        *   `PPS-VERSIONS`: A group item for PPS versions.
            *   `PPDRV-VERSION` (PIC X(05)): The version of the PPDRV program.

*   **Data Structures (LINKAGE SECTION):**

    *   `BILL-NEW-DATA`:  This is the input data passed *to* the program from the calling program. It represents the billing information.
        *   `B-NPI10`: NPI Number.
            *   `B-NPI8` (PIC X(08)): NPI Number 8 digits
            *   `B-NPI-FILLER` (PIC X(02)): Filler for NPI.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): DRG Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century of the discharge date.
            *   `B-DISCHG-YY` (PIC 9(02)): Year of the discharge date.
            *   `B-DISCHG-MM` (PIC 9(02)): Month of the discharge date.
            *   `B-DISCHG-DD` (PIC 9(02)): Day of the discharge date.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Pay Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`: This is the output data passed *back* to the calling program. It contains the calculated PPS results.  (Same structure as in WORKING-STORAGE).
    *   `PRICER-OPT-VERS-SW`: This is the same as the data structure in WORKING-STORAGE, but is now input.
    *   `PROV-NEW-HOLD`:  Provider Record.  This is the input provider information passed to the program.
        *   `PROV-NEWREC-HOLD1`: Provider record hold area 1.
            *   `P-NEW-NPI10`: NPI Number.
                *   `P-NEW-NPI8` (PIC X(08)): NPI Number 8 digits
                *   `P-NEW-NPI-FILLER` (PIC X(02)): Filler for NPI.
            *   `P-NEW-PROVIDER-NO` (PIC X(06)): Provider Number.
            *   `P-NEW-DATE-DATA`: Date Data.
                *   `P-NEW-EFF-DATE`: Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Century of the effective date.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Year of the effective date.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Month of the effective date.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Day of the effective date.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Century of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Year of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Month of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Day of the fiscal year begin date.
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Century of the report date.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Year of the report date.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Month of the report date.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Day of the report date.
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Century of the termination date.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Year of the termination date.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Month of the termination date.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Day of the termination date.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV (PIC 9(01)): Current Division.
            *   `P-NEW-MSA-DATA`: MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX (PIC 9(04)): Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA: Standard Amount Location MSA.
                    *   `P-NEW-RURAL-1ST`: Rural First.
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural Second.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sol Com Dep Hosp Yr.
            *   `P-NEW-LUGAR` (PIC X): Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Fed PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler
        *   `PROV-NEWREC-HOLD2`: Provider record hold area 2.
            *   `P-NEW-VARIABLES`: Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI.
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent.
                *   `P-NEW-FYE-DATE` (PIC X(08)): FYE Date.
            *   `FILLER` (PIC X(23)): Filler
        *   `PROV-NEWREC-HOLD3`: Provider record hold area 3.
            *   `P-NEW-PASS-AMT-DATA`: Pass Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Pass Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Pass Amount Dir Med Ed.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Pass Amount Organ Acq.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Pass Amount Plus Misc.
            *   `P-NEW-CAPI-DATA`: Capi Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capi PPS Pay Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capi Hosp Spec Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capi Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capi New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capi Cost Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` (PIC X): Capi New Hosp.
                *   `P-NEW-CAPI-IME` (PIC 9V9999): Capi IME.
                *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): Capi Exceptions.
            *   `FILLER` (PIC X(22)): Filler
    *   `WAGE-NEW-INDEX-RECORD`: Wage Index Record. This is the input wage index information passed to the program.
        *   `W-MSA` (PIC X(4)): MSA code.
        *   `W-EFF-DATE` (PIC X(8)): Effective Date.
        *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage Index.
        *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage Index.
        *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage Index.

**Program: LTCAL042**

*   **Files Accessed:**

    *   Similar to LTCAL032, this program *includes* `LTDRG031`.

*   **Data Structures (WORKING-STORAGE SECTION):**

    *   `W-STORAGE-REF` (PIC X(46)): Program identification string.
    *   `CAL-VERSION` (PIC X(05)): Calculation logic version (e.g., 'C04.2').
    *   `HOLD-PPS-COMPONENTS`:  Same structure as in LTCAL032.
        *   `H-LOS` (PIC 9(03)): Length of Stay (in days).
        *   `H-REG-DAYS` (PIC 9(03)): Regular Days
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total Days
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold (calculated).
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Factor for Facility Rate.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend Factor for PPS Payment.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion of payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-Labor Portion of payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed loss amount for outlier calculation.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
        *   `H-LOS-RATIO` (PIC 9(01)V9(05)): LOS Ratio
    *   (From copybook `LTDRG031`):  DRG information table.
    *   `PPS-DATA-ALL`:  PPS calculation results (same structure as in LTCAL032).
        *   `PPS-RTC` (PIC 9(02)): Return Code indicating the payment status.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charges Threshold
        *   `PPS-DATA`: A group item to hold PPS data.
            *   `PPS-MSA` (PIC X(04)):  Metropolitan Statistical Area code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage Index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay (used in return).
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular Days Used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year indicator.
            *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler
        *   `PPS-OTHER-DATA`: A group item for other PPS data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler
        *   `PPS-PC-DATA`: A group item for PPS PC data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler
    *   `PRICER-OPT-VERS-SW`:  Pricer option switch. (Same structure as in LTCAL032).
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'): Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates Provider record is passed.
        *   `PPS-VERSIONS`: A group item for PPS versions.
            *   `PPDRV-VERSION` (PIC X(05)): The version of the PPDRV program.

*   **Data Structures (LINKAGE SECTION):**

    *   `BILL-NEW-DATA`: Input billing data (same structure as in LTCAL032).
        *   `B-NPI10`: NPI Number.
            *   `B-NPI8` (PIC X(08)): NPI Number 8 digits
            *   `B-NPI-FILLER` (PIC X(02)): Filler for NPI.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): DRG Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century of the discharge date.
            *   `B-DISCHG-YY` (PIC 9(02)): Year of the discharge date.
            *   `B-DISCHG-MM` (PIC 9(02)): Month of the discharge date.
            *   `B-DISCHG-DD` (PIC 9(02)): Day of the discharge date.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Pay Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`:  Output PPS results (same structure as in LTCAL032).
    *   `PRICER-OPT-VERS-SW`: Pricer option switch (same structure as in LTCAL032).
    *   `PROV-NEW-HOLD`:  Provider Record (same structure as in LTCAL032).
        *   `PROV-NEWREC-HOLD1`: Provider record hold area 1.
            *   `P-NEW-NPI10`: NPI Number.
                *   `P-NEW-NPI8` (PIC X(08)): NPI Number 8 digits
                *   `P-NEW-NPI-FILLER` (PIC X(02)): Filler for NPI.
            *   `P-NEW-PROVIDER-NO` (PIC X(06)): Provider Number.
            *   `P-NEW-DATE-DATA`: Date Data.
                *   `P-NEW-EFF-DATE`: Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Century of the effective date.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Year of the effective date.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Month of the effective date.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Day of the effective date.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Century of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Year of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Month of the fiscal year begin date.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Day of the fiscal year begin date.
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Century of the report date.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Year of the report date.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Month of the report date.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Day of the report date.
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Century of the termination date.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Year of the termination date.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Month of the termination date.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Day of the termination date.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV (PIC 9(01)): Current Division.
            *   `P-NEW-MSA-DATA`: MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX (PIC 9(04)): Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA: Standard Amount Location MSA.
                    *   `P-NEW-RURAL-1ST`: Rural First.
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural Second.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sol Com Dep Hosp Yr.
            *   `P-NEW-LUGAR` (PIC X): Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Fed PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler
        *   `PROV-NEWREC-HOLD2`: Provider record hold area 2.
            *   `P-NEW-VARIABLES`: Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI.
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent.
                *   `P