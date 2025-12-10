Here's an analysis of the provided COBOL programs:

**Program: LTCAL032**

*   **Files Accessed:**
    *   None explicitly. This program uses a `COPY` statement to include the definitions from `LTDRG031`.

*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` (PIC X(46)): Stores a program identifier.
    *   `CAL-VERSION` (PIC X(05)): Stores the version of the calculation logic ('C03.2').
    *   `HOLD-PPS-COMPONENTS`: This is a group item used to hold various calculated components of the PPS (Prospective Payment System) calculation:
        *   `H-LOS` (PIC 9(03)):  Length of stay (in days).
        *   `H-REG-DAYS` (PIC 9(03)): Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Return code related to blending.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)):  Blend factor (Facility).
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend factor (PPS).
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short stay payment amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short stay cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
    *   Data structures from `LTDRG031` (See the analysis for that program below).

*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA`:  This is the input data structure, passed from the calling program. It contains billing information:
        *   `B-NPI10`: NPI (National Provider Identifier)
            *   `B-NPI8` (PIC X(08)): NPI, first 8 characters
            *   `B-NPI-FILLER` (PIC X(02)): NPI, last 2 characters
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status
        *   `B-DRG-CODE` (PIC X(03)): DRG (Diagnosis Related Group) Code
        *   `B-LOS` (PIC 9(03)): Length of Stay
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`: Discharge Date
            *   `B-DISCHG-CC` (PIC 9(02)): Century/Year (CC)
            *   `B-DISCHG-YY` (PIC 9(02)): Year (YY)
            *   `B-DISCHG-MM` (PIC 9(02)): Month (MM)
            *   `B-DISCHG-DD` (PIC 9(02)): Day (DD)
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator
        *   `FILLER` (PIC X(13)): Unused filler space.
    *   `PPS-DATA-ALL`: This is the output data structure, passed back to the calling program. It contains the calculated PPS data:
        *   `PPS-RTC` (PIC 9(02)): Return Code. Indicates the result of the calculation (e.g., normal payment, outlier, short stay).
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold.
        *   `PPS-DATA`: Group item containing various PPS-related data:
            *   `PPS-MSA` (PIC X(04)):  MSA (Metropolitan Statistical Area) code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier payment amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular days used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve days used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year.
            *   `PPS-COLA` (PIC 9(01)V9(03)):  Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Group Item
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: Group Item
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW` (PIC X(01)): Switch to determine if all tables are passed or just the provider record
            *   `ALL-TABLES-PASSED` VALUE 'A'
            *   `PROV-RECORD-PASSED` VALUE 'P'
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` (PIC X(05)): Version of the DRG program.
    *   `PROV-NEW-HOLD`: This is the provider record passed to the program.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`:  NPI (National Provider Identifier)
                *   `P-NEW-NPI8` (PIC X(08)): NPI, first 8 characters
                *   `P-NEW-NPI-FILLER` (PIC X(02)): NPI, last 2 characters
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` (PIC 9(02)): State Code
                *   `FILLER` (PIC X(04)): Filler
            *   `P-NEW-DATE-DATA`: Date Data
                *   `P-NEW-EFF-DATE`: Effective Date
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Effective Date, Century/Year
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Effective Date, Year
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Effective Date, Month
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Effective Date, Day
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Fiscal Year Begin Date, Century/Year
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Fiscal Year Begin Date, Year
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Fiscal Year Begin Date, Month
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Fiscal Year Begin Date, Day
                *   `P-NEW-REPORT-DATE`: Reporting Date
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Reporting Date, Century/Year
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Reporting Date, Year
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Reporting Date, Month
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Reporting Date, Day
                *   `P-NEW-TERMINATION-DATE`: Termination Date
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Termination Date, Century/Year
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Termination Date, Year
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Termination Date, Month
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Termination Date, Day
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current Census Division
            *   `P-NEW-CURRENT-DIV` REDEFINES `P-NEW-CURRENT-CENSUS-DIV`: Current Division
            *   `P-NEW-MSA-DATA` : MSA Data
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geographic Location MSA (just right)
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES `P-NEW-GEO-LOC-MSAX` (PIC 9(04)): Geographic Location MSA (numeric)
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES `P-NEW-STAND-AMT-LOC-MSA`
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sole Community Dependent Hospital Year
            *   `P-NEW-LUGAR` (PIC X): Lugar
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary Relief Indicator
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS Blend Indicator
            *   `FILLER` (PIC X(05)): Filler
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): PRUF Update Factor
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent
                *   `P-NEW-FYE-DATE` (PIC X(08)): Fiscal Year End Date
            *   `FILLER` (PIC X(23)): Filler
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Passed Amount Capital
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Passed Amount Direct Medical Education
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Passed Amount Organ Acquisition
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Passed Amount Plus Misc
            *   `P-NEW-CAPI-DATA`: Capital Data
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capital PPS Pay Code
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capital Hospital Specific Rate
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capital Old Harm Rate
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capital New Harm Ratio
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capital Cost to Charge Ratio
                *   `P-NEW-CAPI-NEW-HOSP` (PIC X): Capital New Hospital
                *   `P-NEW-CAPI-IME` (PIC 9V9999): Capital IME
                *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): Capital Exceptions
            *   `FILLER` (PIC X(22)): Filler
    *   `WAGE-NEW-INDEX-RECORD`: Wage Index Record
        *   `W-MSA` (PIC X(4)): MSA
        *   `W-EFF-DATE` (PIC X(8)): Effective Date
        *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage Index 1
        *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage Index 2
        *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage Index 3

**Program: LTCAL042**

*   **Files Accessed:**
    *   None explicitly.  This program, like LTCAL032, uses a `COPY` statement to include the definitions from `LTDRG031`.

*   **WORKING-STORAGE SECTION Data Structures:**
    *   `W-STORAGE-REF` (PIC X(46)): Stores a program identifier.
    *   `CAL-VERSION` (PIC X(05)): Stores the version of the calculation logic ('C04.2').
    *   `HOLD-PPS-COMPONENTS`: This is a group item used to hold various calculated components of the PPS (Prospective Payment System) calculation:
        *   `H-LOS` (PIC 9(03)):  Length of stay (in days).
        *   `H-REG-DAYS` (PIC 9(03)): Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Return code related to blending.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)):  Blend factor (Facility).
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend factor (PPS).
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short stay payment amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short stay cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
        *   `H-LOS-RATIO` (PIC 9(01)V9(05)): LOS Ratio
    *   Data structures from `LTDRG031` (See the analysis for that program below).

*   **LINKAGE SECTION Data Structures:**
    *   `BILL-NEW-DATA`:  This is the input data structure, passed from the calling program. It contains billing information:
        *   `B-NPI10`: NPI (National Provider Identifier)
            *   `B-NPI8` (PIC X(08)): NPI, first 8 characters
            *   `B-NPI-FILLER` (PIC X(02)): NPI, last 2 characters
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status
        *   `B-DRG-CODE` (PIC X(03)): DRG (Diagnosis Related Group) Code
        *   `B-LOS` (PIC 9(03)): Length of Stay
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`: Discharge Date
            *   `B-DISCHG-CC` (PIC 9(02)): Century/Year (CC)
            *   `B-DISCHG-YY` (PIC 9(02)): Year (YY)
            *   `B-DISCHG-MM` (PIC 9(02)): Month (MM)
            *   `B-DISCHG-DD` (PIC 9(02)): Day (DD)
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator
        *   `FILLER` (PIC X(13)): Unused filler space.
    *   `PPS-DATA-ALL`: This is the output data structure, passed back to the calling program. It contains the calculated PPS data:
        *   `PPS-RTC` (PIC 9(02)): Return Code. Indicates the result of the calculation (e.g., normal payment, outlier, short stay).
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge threshold.
        *   `PPS-DATA`: Group item containing various PPS-related data:
            *   `PPS-MSA` (PIC X(04)):  MSA (Metropolitan Statistical Area) code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)): Wage index.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)): Average Length of Stay.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)): Relative weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)): Outlier payment amount.
            *   `PPS-LOS` (PIC 9(03)): Length of Stay.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)): DRG adjusted payment amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)): Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)): Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)): Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New Facility Specific Rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)): Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)): Submitted DRG code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)): Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)): Regular days used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)): Lifetime Reserve days used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)): Blend Year.
            *   `PPS-COLA` (PIC 9(01)V9(03)):  Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Group Item
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: Group Item
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW` (PIC X(01)): Switch to determine if all tables are passed or just the provider record
            *   `ALL-TABLES-PASSED` VALUE 'A'
            *   `PROV-RECORD-PASSED` VALUE 'P'
        *   `PPS-VERSIONS`
            *   `PPDRV-VERSION` (PIC X(05)): Version of the DRG program.
    *   `PROV-NEW-HOLD`: This is the provider record passed to the program.
        *   `PROV-NEWREC-HOLD1`
            *   `P-NEW-NPI10`:  NPI (National Provider Identifier)
                *   `P-NEW-NPI8` (PIC X(08)): NPI, first 8 characters
                *   `P-NEW-NPI-FILLER` (PIC X(02)): NPI, last 2 characters
            *   `P-NEW-PROVIDER-NO`
                *   `P-NEW-STATE` (PIC 9(02)): State Code
                *   `FILLER` (PIC X(04)): Filler
            *   `P-NEW-DATE-DATA`: Date Data
                *   `P-NEW-EFF-DATE`: Effective Date
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Effective Date, Century/Year
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Effective Date, Year
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Effective Date, Month
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Effective Date, Day
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Fiscal Year Begin Date, Century/Year
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Fiscal Year Begin Date, Year
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Fiscal Year Begin Date, Month
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Fiscal Year Begin Date, Day
                *   `P-NEW-REPORT-DATE`: Reporting Date
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Reporting Date, Century/Year
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Reporting Date, Year
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Reporting Date, Month
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Reporting Date, Day
                *   `P-NEW-TERMINATION-DATE`: Termination Date
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Termination Date, Century/Year
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Termination Date, Year
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Termination Date, Month
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Termination Date, Day
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code
                *   `P-NEW-WAIVER-STATE` VALUE 'Y'
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Current Census Division
            *   `P-NEW-CURRENT-DIV` REDEFINES `P-NEW-CURRENT-CENSUS-DIV`: Current Division
            *   `P-NEW-MSA-DATA` : MSA Data
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geographic Location MSA (just right)
                *   `P-NEW-GEO-LOC-MSA9` REDEFINES `P-NEW-GEO-LOC-MSAX` (PIC 9(04)): Geographic Location MSA (numeric)
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES `P-NEW-STAND-AMT-LOC-MSA`
                    *   `P-NEW-RURAL-1ST`
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` VALUE '  '
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sole Community Dependent Hospital Year
            *   `P-NEW-LUGAR` (PIC X): Lugar
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary Relief Indicator
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS Blend Indicator
            *   `FILLER` (PIC X(05)): Filler
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`:
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): Cost of Living Adjustment
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): PRUF Update Factor
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent
                *   `P-NEW-FYE-DATE` (PIC X(08)): Fiscal Year End Date
            *   `FILLER` (PIC X(23)): Filler
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`:
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Passed Amount Capital
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Passed Amount Direct Medical Education
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Passed Amount Organ Acquisition
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Passed Amount Plus Misc
            *   `P-NEW-CAPI-DATA`: Capital Data
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capital PPS Pay Code
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capital Hospital Specific Rate
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capital Old Harm Rate
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capital New Harm Ratio
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capital Cost to Charge Ratio
                *   