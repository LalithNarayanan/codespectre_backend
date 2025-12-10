Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

**COBOL Program: LTCAL032**

*   **Files Accessed:**
    *   None explicitly. This program is a subroutine and doesn't directly access any files. It uses a `COPY` statement to include `LTDRG031`, which likely contains data (DRG codes, weights, etc.) used in calculations.
*   **Data Structures (WORKING-STORAGE SECTION):**
    *   `W-STORAGE-REF` (PIC X(46)):  A descriptive field, storing a string identifying the program and its working storage.
    *   `CAL-VERSION` (PIC X(05)): Stores the version of the calculation logic. Value is 'C03.2'.
    *   `HOLD-PPS-COMPONENTS`: A group item used to hold intermediate calculation results related to PPS (Prospective Payment System) components.
        *   `H-LOS` (PIC 9(03)): Length of Stay.
        *   `H-REG-DAYS` (PIC 9(03)): Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Facility Portion.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend PPS Portion.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
    *   Data structures defined by `COPY LTDRG031` (See below for details)
*   **Data Structures (LINKAGE SECTION):**
    *   `BILL-NEW-DATA`:  This is the main data structure passed *into* the subroutine from the calling program, containing billing information.
        *   `B-NPI10`: National Provider Identifier (NPI)
            *   `B-NPI8` (PIC X(08)): NPI (first 8 characters).
            *   `B-NPI-FILLER` (PIC X(02)): NPI Filler.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): Diagnosis Related Group (DRG) Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century component of the discharge date.
            *   `B-DISCHG-YY` (PIC 9(02)): Year component of the discharge date.
            *   `B-DISCHG-MM` (PIC 9(02)): Month component of the discharge date.
            *   `B-DISCHG-DD` (PIC 9(02)): Day component of the discharge date.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`: This is the main data structure passed *back* to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` (PIC 9(02)): Return Code indicating the payment method.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold.
        *   `PPS-DATA`: PPS data.
            *   `PPS-MSA` (PIC X(04)): Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage Index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative Weight.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular Days Used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year.
            *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Other PPS data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: PPS PC Data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`: Pricer Option Version Switch.
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'): Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates provider record is passed.
        *   `PPS-VERSIONS`: PPS Versions.
            *   `PPDRV-VERSION` (PIC X(05)): PPDRV Version.
    *   `PROV-NEW-HOLD`:  This structure holds provider-specific information passed *into* the subroutine.
        *   `PROV-NEWREC-HOLD1`: Holds provider record information.
            *   `P-NEW-NPI10`: New NPI information.
                *   `P-NEW-NPI8` (PIC X(08)): New NPI (first 8 characters).
                *   `P-NEW-NPI-FILLER` (PIC X(02)): New NPI Filler.
            *   `P-NEW-PROVIDER-NO` : New Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)): New State.
                *   `FILLER` (PIC X(04)): Filler.
            *   `P-NEW-DATE-DATA`: New Date Data.
                *   `P-NEW-EFF-DATE`: New Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): New Effective Date - Century
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): New Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): New Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): New Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`: New Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): New Fiscal Year Begin Date - Century
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): New Fiscal Year Begin Date - Year
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): New Fiscal Year Begin Date - Month
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): New Fiscal Year Begin Date - Day
                *   `P-NEW-REPORT-DATE`: New Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): New Report Date - Century
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): New Report Date - Year
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): New Report Date - Month
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): New Report Date - Day
                *   `P-NEW-TERMINATION-DATE`: New Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): New Termination Date - Century
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): New Termination Date - Year
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): New Termination Date - Month
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): New Termination Date - Day
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): New Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): New Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): New Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): New Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): New Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV: New Current Division.
            *   `P-NEW-MSA-DATA`: New MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): New Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): New Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX: New Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): New Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): New Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`: New Rural First.
                        *   `P-NEW-STAND-RURAL` (PIC XX): New Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): New Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): New Rural Second.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): New SOL COM DEP HOSP YR.
            *   `P-NEW-LUGAR` (PIC X): New Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): New Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): New Fed PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler.
        *   `PROV-NEWREC-HOLD2`: Holds provider record information.
            *   `P-NEW-VARIABLES`: New Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): New COLA.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): New Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): New Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): New Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): New CMI.
                *   `P-NEW-SSI-RATIO` (V9(04)): New SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (V9(04)): New Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): New PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): New PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` (V9(04)): New DSH Percent.
                *   `P-NEW-FYE-DATE` (PIC X(08)): New FYE Date.
            *   `FILLER` (PIC X(23)): Filler.
        *   `PROV-NEWREC-HOLD3`: Holds provider record information.
            *   `P-NEW-PASS-AMT-DATA`: New Pass Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): New Pass Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): New Pass Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): New Pass Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): New Pass Amount Plus Misc.
            *   `P-NEW-CAPI-DATA`: New CAPI Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): New CAPI PPS Pay Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): New CAPI Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): New CAPI Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): New CAPI New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): New CAPI Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` (PIC X): New CAPI New Hospital.
                *   `P-NEW-CAPI-IME` (PIC 9V9999): New CAPI IME.
                *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): New CAPI Exceptions.
            *   `FILLER` (PIC X(22)): Filler.
    *   `WAGE-NEW-INDEX-RECORD`:  This structure holds wage index information passed *into* the subroutine.
        *   `W-MSA` (PIC X(4)): Wage Index MSA.
        *   `W-EFF-DATE` (PIC X(8)): Wage Index Effective Date.
        *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage Index 1.
        *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage Index 2.
        *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage Index 3.

*   **Data Structures Defined by COPY LTDRG031:**
    *   This `COPY` statement includes a set of DRG-related data, likely a table.  The exact structure is defined within the `LTDRG031` source code.  Based on the code, it appears to be a table of DRG codes and associated values.
        *   `W-DRG-FILLS`: Contains repeating values, likely DRG codes and related data, packed as a long string.
        *   `W-DRG-TABLE`:  A table that redefines `W-DRG-FILLS` to provide an indexed structure for accessing the DRG data.
            *   `WWM-ENTRY`:  An entry in the DRG table, repeated.  `OCCURS 502 TIMES` suggests there are 502 different DRG codes in the table.
                *   `WWM-DRG` (PIC X(3)): The DRG code itself.
                *   `WWM-RELWT` (PIC 9(1)V9(4)):  The relative weight associated with the DRG.
                *   `WWM-ALOS` (PIC 9(2)V9(1)):  The average length of stay for the DRG.

**COBOL Program: LTCAL042**

*   **Files Accessed:**
    *   None explicitly. This program is similar to `LTCAL032` in that it is a subroutine and doesn't directly access any files. It uses a `COPY` statement to include `LTDRG031`, which likely contains data (DRG codes, weights, etc.) used in calculations.
*   **Data Structures (WORKING-STORAGE SECTION):**
    *   `W-STORAGE-REF` (PIC X(46)):  A descriptive field, storing a string identifying the program and its working storage.
    *   `CAL-VERSION` (PIC X(05)): Stores the version of the calculation logic. Value is 'C04.2'.
    *   `HOLD-PPS-COMPONENTS`: A group item used to hold intermediate calculation results related to PPS (Prospective Payment System) components.
        *   `H-LOS` (PIC 9(03)): Length of Stay.
        *   `H-REG-DAYS` (PIC 9(03)): Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Facility Portion.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend PPS Portion.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
        *   `H-LOS-RATIO` (PIC 9(01)V9(05)): Length of Stay Ratio.
    *   Data structures defined by `COPY LTDRG031` (See below for details)
*   **Data Structures (LINKAGE SECTION):**
    *   `BILL-NEW-DATA`:  This is the main data structure passed *into* the subroutine from the calling program, containing billing information.
        *   `B-NPI10`: National Provider Identifier (NPI)
            *   `B-NPI8` (PIC X(08)): NPI (first 8 characters).
            *   `B-NPI-FILLER` (PIC X(02)): NPI Filler.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): Diagnosis Related Group (DRG) Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century component of the discharge date.
            *   `B-DISCHG-YY` (PIC 9(02)): Year component of the discharge date.
            *   `B-DISCHG-MM` (PIC 9(02)): Month component of the discharge date.
            *   `B-DISCHG-DD` (PIC 9(02)): Day component of the discharge date.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`: This is the main data structure passed *back* to the calling program, containing the calculated PPS data.
        *   `PPS-RTC` (PIC 9(02)): Return Code indicating the payment method.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold.
        *   `PPS-DATA`: PPS data.
            *   `PPS-MSA` (PIC X(04)): Metropolitan Statistical Area (MSA).
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage Index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative Weight.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular Days Used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve Days Used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year.
            *   `PPS-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Other PPS data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: PPS PC Data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`: Pricer Option Version Switch.
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'): Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates provider record is passed.
        *   `PPS-VERSIONS`: PPS Versions.
            *   `PPDRV-VERSION` (PIC X(05)): PPDRV Version.
    *   `PROV-NEW-HOLD`:  This structure holds provider-specific information passed *into* the subroutine.
        *   `PROV-NEWREC-HOLD1`: Holds provider record information.
            *   `P-NEW-NPI10`: New NPI information.
                *   `P-NEW-NPI8` (PIC X(08)): New NPI (first 8 characters).
                *   `P-NEW-NPI-FILLER` (PIC X(02)): New NPI Filler.
            *   `P-NEW-PROVIDER-NO` : New Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)): New State.
                *   `FILLER` (PIC X(04)): Filler.
            *   `P-NEW-DATE-DATA`: New Date Data.
                *   `P-NEW-EFF-DATE`: New Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): New Effective Date - Century
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): New Effective Date - Year
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): New Effective Date - Month
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): New Effective Date - Day
                *   `P-NEW-FY-BEGIN-DATE`: New Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): New Fiscal Year Begin Date - Century
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): New Fiscal Year Begin Date - Year
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): New Fiscal Year Begin Date - Month
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): New Fiscal Year Begin Date - Day
                *   `P-NEW-REPORT-DATE`: New Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): New Report Date - Century
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): New Report Date - Year
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): New Report Date - Month
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): New Report Date - Day
                *   `P-NEW-TERMINATION-DATE`: New Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): New Termination Date - Century
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): New Termination Date - Year
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): New Termination Date - Month
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): New Termination Date - Day
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): New Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): New Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): New Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): New Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): New Current Census Division.
            *   `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV: New Current Division.
            *   `P-NEW-MSA-DATA`: New MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): New Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): New Geo Location MSA.
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX: New Geo Location MSA.
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): New Wage Index Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): New Standard Amount Location MSA.
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    *   `P-NEW-RURAL-1ST`: New Rural First.
                        *   `P-NEW-STAND-RURAL` (PIC XX): New Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): New Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): New Rural Second.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): New SOL COM DEP HOSP YR.
            *   `P-NEW-LUGAR` (PIC X): New Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): New Temp Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): New Fed PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler.
        *   `PROV-NEWREC-HOLD2`: Holds provider record information.
            *   `P-NEW-VARIABLES`: New Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): New COLA.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): New Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): New Bed Size.