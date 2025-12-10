## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

*   **File Access:**
    *   No files are explicitly opened or accessed within this program.
    *   It `COPY`s `LTDRG031`, which implies the inclusion of data definitions (likely a table of DRG codes and related information) from another source.

*   **Data Structures in `WORKING-STORAGE SECTION`:**

    *   `W-STORAGE-REF` - `PIC X(46)`:  A literal string containing the program name and a description, used for informational purposes (e.g., debugging).
    *   `CAL-VERSION` - `PIC X(05)`:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:  A group of variables used to store intermediate calculation results, including:
        *   `H-LOS` - `PIC 9(03)`: Length of Stay
        *   `H-REG-DAYS` - `PIC 9(03)`: Regular Days
        *   `H-TOTAL-DAYS` - `PIC 9(05)`: Total Days
        *   `H-SSOT` - `PIC 9(02)`:  Short Stay Outlier Threshold
        *   `H-BLEND-RTC` - `PIC 9(02)`: Blend Return Code
        *   `H-BLEND-FAC` - `PIC 9(01)V9(01)`: Blend Facility Rate
        *   `H-BLEND-PPS` - `PIC 9(01)V9(01)`: Blend PPS Rate
        *   `H-SS-PAY-AMT` - `PIC 9(07)V9(02)`: Short Stay Payment Amount
        *   `H-SS-COST` - `PIC 9(07)V9(02)`: Short Stay Cost
        *   `H-LABOR-PORTION` - `PIC 9(07)V9(06)`: Labor Portion of Payment
        *   `H-NONLABOR-PORTION` - `PIC 9(07)V9(06)`: Non-Labor Portion of Payment
        *   `H-FIXED-LOSS-AMT` - `PIC 9(07)V9(02)`: Fixed Loss Amount for Outlier Calculations
        *   `H-NEW-FAC-SPEC-RATE` - `PIC 9(05)V9(02)`: New Facility Specific Rate
    *   Data structures defined by `COPY LTDRG031` (See LTDRG031 analysis).

*   **Data Structures in `LINKAGE SECTION`:**

    *   `BILL-NEW-DATA`:  This structure represents the input data passed *to* the program, likely a bill record.
        *   `B-NPI10`: National Provider Identifier (NPI) - 10 digits
            *   `B-NPI8` - `PIC X(08)`: First 8 digits of NPI
            *   `B-NPI-FILLER` - `PIC X(02)`:  Filler for the remaining 2 digits of NPI
        *   `B-PROVIDER-NO` - `PIC X(06)`: Provider Number
        *   `B-PATIENT-STATUS` - `PIC X(02)`: Patient Status Code
        *   `B-DRG-CODE` - `PIC X(03)`:  DRG Code (Diagnosis Related Group)
        *   `B-LOS` - `PIC 9(03)`: Length of Stay
        *   `B-COV-DAYS` - `PIC 9(03)`: Covered Days
        *   `B-LTR-DAYS` - `PIC 9(02)`: Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`:  Discharge Date
            *   `B-DISCHG-CC` - `PIC 9(02)`: Century Component of Discharge Date
            *   `B-DISCHG-YY` - `PIC 9(02)`: Year Component of Discharge Date
            *   `B-DISCHG-MM` - `PIC 9(02)`: Month Component of Discharge Date
            *   `B-DISCHG-DD` - `PIC 9(02)`: Day Component of Discharge Date
        *   `B-COV-CHARGES` - `PIC 9(07)V9(02)`: Covered Charges
        *   `B-SPEC-PAY-IND` - `PIC X(01)`:  Special Payment Indicator
        *   `FILLER` - `PIC X(13)`: Unused space
    *   `PPS-DATA-ALL`: This is the structure for the data returned *from* the program.  This structure contains calculated payment information.
        *   `PPS-RTC` - `PIC 9(02)`: Return Code (Indicates payment status and reason.)
        *   `PPS-CHRG-THRESHOLD` - `PIC 9(07)V9(02)`: Charge Threshold for Outlier
        *   `PPS-DATA`: Group of calculated payment variables.
            *   `PPS-MSA` - `PIC X(04)`:  MSA (Metropolitan Statistical Area) Code
            *   `PPS-WAGE-INDEX` - `PIC 9(02)V9(04)`: Wage Index
            *   `PPS-AVG-LOS` - `PIC 9(02)V9(01)`: Average Length of Stay
            *   `PPS-RELATIVE-WGT` - `PIC 9(01)V9(04)`: Relative Weight (DRG specific)
            *   `PPS-OUTLIER-PAY-AMT` - `PIC 9(07)V9(02)`: Outlier Payment Amount
            *   `PPS-LOS` - `PIC 9(03)`: Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` - `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
            *   `PPS-FED-PAY-AMT` - `PIC 9(07)V9(02)`: Federal Payment Amount
            *   `PPS-FINAL-PAY-AMT` - `PIC 9(07)V9(02)`: Final Payment Amount
            *   `PPS-FAC-COSTS` - `PIC 9(07)V9(02)`: Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` - `PIC 9(07)V9(02)`: New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` - `PIC 9(07)V9(02)`: Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` - `PIC X(03)`: Submitted DRG Code
            *   `PPS-CALC-VERS-CD` - `PIC X(05)`: Calculation Version Code
            *   `PPS-REG-DAYS-USED` - `PIC 9(03)`: Regular Days Used
            *   `PPS-LTR-DAYS-USED` - `PIC 9(03)`: Lifetime Reserve Days Used
            *   `PPS-BLEND-YEAR` - `PIC 9(01)`: Blend Year Indicator
            *   `PPS-COLA` - `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   `FILLER` - `PIC X(04)`: Filler
        *   `PPS-OTHER-DATA`: Group of other data
            *   `PPS-NAT-LABOR-PCT` - `PIC 9(01)V9(05)`: National Labor Percentage
            *   `PPS-NAT-NONLABOR-PCT` - `PIC 9(01)V9(05)`: National Non-Labor Percentage
            *   `PPS-STD-FED-RATE` - `PIC 9(05)V9(02)`: Standard Federal Rate
            *   `PPS-BDGT-NEUT-RATE` - `PIC 9(01)V9(03)`: Budget Neutrality Rate
            *   `FILLER` - `PIC X(20)`: Filler
        *   `PPS-PC-DATA`: Group of PC data
            *   `PPS-COT-IND` - `PIC X(01)`: Cost Outlier Indicator
            *   `FILLER` - `PIC X(20)`: Filler
    *   `PRICER-OPT-VERS-SW`:  This structure is used to indicate the versions of the programs
        *   `PRICER-OPTION-SW` - `PIC X(01)`: Pricer Option Switch.  Used to indicate if all tables or provider records are passed
            *   `ALL-TABLES-PASSED` - `VALUE 'A'`:  Indicates all tables are passed
            *   `PROV-RECORD-PASSED` - `VALUE 'P'`: Indicates provider record passed
        *   `PPS-VERSIONS`: Group of PPS versions
            *   `PPDRV-VERSION` - `PIC X(05)`: Version of the  PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure holds provider specific data passed to the program.
        *   `PROV-NEWREC-HOLD1`: Group of Provider Data
            *   `P-NEW-NPI10`: National Provider Identifier (NPI) - 10 digits
                *   `P-NEW-NPI8` - `PIC X(08)`: First 8 digits of NPI
                *   `P-NEW-NPI-FILLER` - `PIC X(02)`: Filler for the remaining 2 digits of NPI
            *   `P-NEW-PROVIDER-NO` - `PIC X(06)`: Provider Number
                *   `P-NEW-STATE` - `PIC 9(02)`: State Code
                *   `FILLER` - `PIC X(04)`: Filler
            *   `P-NEW-DATE-DATA`: Date Information
                *   `P-NEW-EFF-DATE`:  Effective Date
                    *   `P-NEW-EFF-DT-CC` - `PIC 9(02)`: Century Component of Effective Date
                    *   `P-NEW-EFF-DT-YY` - `PIC 9(02)`: Year Component of Effective Date
                    *   `P-NEW-EFF-DT-MM` - `PIC 9(02)`: Month Component of Effective Date
                    *   `P-NEW-EFF-DT-DD` - `PIC 9(02)`: Day Component of Effective Date
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` - `PIC 9(02)`: Century Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-YY` - `PIC 9(02)`: Year Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-MM` - `PIC 9(02)`: Month Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-DD` - `PIC 9(02)`: Day Component of Fiscal Year Begin Date
                *   `P-NEW-REPORT-DATE`: Report Date
                    *   `P-NEW-REPORT-DT-CC` - `PIC 9(02)`: Century Component of Report Date
                    *   `P-NEW-REPORT-DT-YY` - `PIC 9(02)`: Year Component of Report Date
                    *   `P-NEW-REPORT-DT-MM` - `PIC 9(02)`: Month Component of Report Date
                    *   `P-NEW-REPORT-DT-DD` - `PIC 9(02)`: Day Component of Report Date
                *   `P-NEW-TERMINATION-DATE`: Termination Date
                    *   `P-NEW-TERM-DT-CC` - `PIC 9(02)`: Century Component of Termination Date
                    *   `P-NEW-TERM-DT-YY` - `PIC 9(02)`: Year Component of Termination Date
                    *   `P-NEW-TERM-DT-MM` - `PIC 9(02)`: Month Component of Termination Date
                    *   `P-NEW-TERM-DT-DD` - `PIC 9(02)`: Day Component of Termination Date
            *   `P-NEW-WAIVER-CODE` - `PIC X(01)`: Waiver Code
                *   `P-NEW-WAIVER-STATE` - `VALUE 'Y'`: Waiver State Indicator
            *   `P-NEW-INTER-NO` - `PIC 9(05)`: Internal Number
            *   `P-NEW-PROVIDER-TYPE` - `PIC X(02)`: Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` - `PIC 9(01)`: Current Census Division
            *   `P-NEW-CURRENT-DIV` - `PIC 9(01)`: Redefines Current Census Division
            *   `P-NEW-MSA-DATA`: MSA Data
                *   `P-NEW-CHG-CODE-INDEX` - `PIC X`: Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` - `PIC X(04)`: Geographic Location MSA
                *   `P-NEW-GEO-LOC-MSA9` - `PIC 9(04)`: Redefines Geographic Location MSA
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - `PIC X(04)`: Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` - `PIC X(04)`: Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9`: Redefines Standard Amount Location MSA
                    *   `P-NEW-RURAL-1ST`: Rural 1st
                        *   `P-NEW-STAND-RURAL` - `PIC XX`: Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` - `VALUE '  '`: Standard Rural Check
                    *   `P-NEW-RURAL-2ND` - `PIC XX`: Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - `PIC XX`: Sole Community Dependent Hospital Year
            *   `P-NEW-LUGAR` - `PIC X`: Lugar
            *   `P-NEW-TEMP-RELIEF-IND` - `PIC X`: Temporary Relief Indicator
            *   `P-NEW-FED-PPS-BLEND-IND` - `PIC X`: Federal PPS Blend Indicator
            *   `FILLER` - `PIC X(05)`: Filler
        *   `PROV-NEWREC-HOLD2`: Group of Provider Data
            *   `P-NEW-VARIABLES`: Variables
                *   `P-NEW-FAC-SPEC-RATE` - `PIC 9(05)V9(02)`: Facility Specific Rate
                *   `P-NEW-COLA` - `PIC 9(01)V9(03)`: Cost of Living Adjustment
                *   `P-NEW-INTERN-RATIO` - `PIC 9(01)V9(04)`: Intern Ratio
                *   `P-NEW-BED-SIZE` - `PIC 9(05)`: Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` - `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio
                *   `P-NEW-CMI` - `PIC 9(01)V9(04)`: CMI
                *   `P-NEW-SSI-RATIO` - `PIC V9(04)`: SSI Ratio
                *   `P-NEW-MEDICAID-RATIO` - `PIC V9(04)`: Medicaid Ratio
                *   `P-NEW-PPS-BLEND-YR-IND` - `PIC 9(01)`: PPS Blend Year Indicator
                *   `P-NEW-PRUF-UPDTE-FACTOR` - `PIC 9(01)V9(05)`: PRUF Update Factor
                *   `P-NEW-DSH-PERCENT` - `PIC V9(04)`: DSH Percent
                *   `P-NEW-FYE-DATE` - `PIC X(08)`: FYE Date
            *   `FILLER` - `PIC X(23)`: Filler
        *   `PROV-NEWREC-HOLD3`: Group of Provider Data
            *   `P-NEW-PASS-AMT-DATA`: Pass Amount Data
                *   `P-NEW-PASS-AMT-CAPITAL` - `PIC 9(04)V99`: Pass Amount Capital
                *   `P-NEW-PASS-AMT-DIR-MED-ED` - `PIC 9(04)V99`: Pass Amount Direct Medical Education
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` - `PIC 9(04)V99`: Pass Amount Organ Acquisition
                *   `P-NEW-PASS-AMT-PLUS-MISC` - `PIC 9(04)V99`: Pass Amount Plus Misc
            *   `P-NEW-CAPI-DATA`: Capital Data
                *   `P-NEW-CAPI-PPS-PAY-CODE` - `PIC X`: Capital PPS Pay Code
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` - `PIC 9(04)V99`: Capital Hospital Specific Rate
                *   `P-NEW-CAPI-OLD-HARM-RATE` - `PIC 9(04)V99`: Capital Old Harm Rate
                *   `P-NEW-CAPI-NEW-HARM-RATIO` - `PIC 9(01)V9999`: Capital New Harm Ratio
                *   `P-NEW-CAPI-CSTCHG-RATIO` - `PIC 9V999`: Capital Cost to Charge Ratio
                *   `P-NEW-CAPI-NEW-HOSP` - `PIC X`: Capital New Hospital
                *   `P-NEW-CAPI-IME` - `PIC 9V9999`: Capital IME
                *   `P-NEW-CAPI-EXCEPTIONS` - `PIC 9(04)V99`: Capital Exceptions
            *   `FILLER` - `PIC X(22)`: Filler
    *   `WAGE-NEW-INDEX-RECORD`:  This structure represents wage index data passed to the program.
        *   `W-MSA` - `PIC X(4)`: MSA Code
        *   `W-EFF-DATE` - `PIC X(8)`: Effective Date
        *   `W-WAGE-INDEX1` - `PIC S9(02)V9(04)`: Wage Index 1
        *   `W-WAGE-INDEX2` - `PIC S9(02)V9(04)`: Wage Index 2
        *   `W-WAGE-INDEX3` - `PIC S9(02)V9(04)`: Wage Index 3

### Program: LTCAL042

*   **File Access:**
    *   No files are explicitly opened or accessed within this program.
    *   It `COPY`s `LTDRG031`.

*   **Data Structures in `WORKING-STORAGE SECTION`:**

    *   `W-STORAGE-REF` - `PIC X(46)`:  A literal string containing the program name and a description, used for informational purposes (e.g., debugging).
    *   `CAL-VERSION` - `PIC X(05)`:  Stores the version number of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`:  A group of variables used to store intermediate calculation results, including:
        *   `H-LOS` - `PIC 9(03)`: Length of Stay
        *   `H-REG-DAYS` - `PIC 9(03)`: Regular Days
        *   `H-TOTAL-DAYS` - `PIC 9(05)`: Total Days
        *   `H-SSOT` - `PIC 9(02)`:  Short Stay Outlier Threshold
        *   `H-BLEND-RTC` - `PIC 9(02)`: Blend Return Code
        *   `H-BLEND-FAC` - `PIC 9(01)V9(01)`: Blend Facility Rate
        *   `H-BLEND-PPS` - `PIC 9(01)V9(01)`: Blend PPS Rate
        *   `H-SS-PAY-AMT` - `PIC 9(07)V9(02)`: Short Stay Payment Amount
        *   `H-SS-COST` - `PIC 9(07)V9(02)`: Short Stay Cost
        *   `H-LABOR-PORTION` - `PIC 9(07)V9(06)`: Labor Portion of Payment
        *   `H-NONLABOR-PORTION` - `PIC 9(07)V9(06)`: Non-Labor Portion of Payment
        *   `H-FIXED-LOSS-AMT` - `PIC 9(07)V9(02)`: Fixed Loss Amount for Outlier Calculations
        *   `H-NEW-FAC-SPEC-RATE` - `PIC 9(05)V9(02)`: New Facility Specific Rate
        *   `H-LOS-RATIO` - `PIC 9(01)V9(05)`: LOS Ratio
    *   Data structures defined by `COPY LTDRG031` (See LTDRG031 analysis).

*   **Data Structures in `LINKAGE SECTION`:**

    *   `BILL-NEW-DATA`:  This structure represents the input data passed *to* the program, likely a bill record.
        *   `B-NPI10`: National Provider Identifier (NPI) - 10 digits
            *   `B-NPI8` - `PIC X(08)`: First 8 digits of NPI
            *   `B-NPI-FILLER` - `PIC X(02)`:  Filler for the remaining 2 digits of NPI
        *   `B-PROVIDER-NO` - `PIC X(06)`: Provider Number
        *   `B-PATIENT-STATUS` - `PIC X(02)`: Patient Status Code
        *   `B-DRG-CODE` - `PIC X(03)`:  DRG Code (Diagnosis Related Group)
        *   `B-LOS` - `PIC 9(03)`: Length of Stay
        *   `B-COV-DAYS` - `PIC 9(03)`: Covered Days
        *   `B-LTR-DAYS` - `PIC 9(02)`: Lifetime Reserve Days
        *   `B-DISCHARGE-DATE`:  Discharge Date
            *   `B-DISCHG-CC` - `PIC 9(02)`: Century Component of Discharge Date
            *   `B-DISCHG-YY` - `PIC 9(02)`: Year Component of Discharge Date
            *   `B-DISCHG-MM` - `PIC 9(02)`: Month Component of Discharge Date
            *   `B-DISCHG-DD` - `PIC 9(02)`: Day Component of Discharge Date
        *   `B-COV-CHARGES` - `PIC 9(07)V9(02)`: Covered Charges
        *   `B-SPEC-PAY-IND` - `PIC X(01)`:  Special Payment Indicator
        *   `FILLER` - `PIC X(13)`: Unused space
    *   `PPS-DATA-ALL`: This is the structure for the data returned *from* the program.  This structure contains calculated payment information.
        *   `PPS-RTC` - `PIC 9(02)`: Return Code (Indicates payment status and reason.)
        *   `PPS-CHRG-THRESHOLD` - `PIC 9(07)V9(02)`: Charge Threshold for Outlier
        *   `PPS-DATA`: Group of calculated payment variables.
            *   `PPS-MSA` - `PIC X(04)`:  MSA (Metropolitan Statistical Area) Code
            *   `PPS-WAGE-INDEX` - `PIC 9(02)V9(04)`: Wage Index
            *   `PPS-AVG-LOS` - `PIC 9(02)V9(01)`: Average Length of Stay
            *   `PPS-RELATIVE-WGT` - `PIC 9(01)V9(04)`: Relative Weight (DRG specific)
            *   `PPS-OUTLIER-PAY-AMT` - `PIC 9(07)V9(02)`: Outlier Payment Amount
            *   `PPS-LOS` - `PIC 9(03)`: Length of Stay
            *   `PPS-DRG-ADJ-PAY-AMT` - `PIC 9(07)V9(02)`: DRG Adjusted Payment Amount
            *   `PPS-FED-PAY-AMT` - `PIC 9(07)V9(02)`: Federal Payment Amount
            *   `PPS-FINAL-PAY-AMT` - `PIC 9(07)V9(02)`: Final Payment Amount
            *   `PPS-FAC-COSTS` - `PIC 9(07)V9(02)`: Facility Costs
            *   `PPS-NEW-FAC-SPEC-RATE` - `PIC 9(07)V9(02)`: New Facility Specific Rate
            *   `PPS-OUTLIER-THRESHOLD` - `PIC 9(07)V9(02)`: Outlier Threshold
            *   `PPS-SUBM-DRG-CODE` - `PIC X(03)`: Submitted DRG Code
            *   `PPS-CALC-VERS-CD` - `PIC X(05)`: Calculation Version Code
            *   `PPS-REG-DAYS-USED` - `PIC 9(03)`: Regular Days Used
            *   `PPS-LTR-DAYS-USED` - `PIC 9(03)`: Lifetime Reserve Days Used
            *   `PPS-BLEND-YEAR` - `PIC 9(01)`: Blend Year Indicator
            *   `PPS-COLA` - `PIC 9(01)V9(03)`: Cost of Living Adjustment
            *   `FILLER` - `PIC X(04)`: Filler
        *   `PPS-OTHER-DATA`: Group of other data
            *   `PPS-NAT-LABOR-PCT` - `PIC 9(01)V9(05)`: National Labor Percentage
            *   `PPS-NAT-NONLABOR-PCT` - `PIC 9(01)V9(05)`: National Non-Labor Percentage
            *   `PPS-STD-FED-RATE` - `PIC 9(05)V9(02)`: Standard Federal Rate
            *   `PPS-BDGT-NEUT-RATE` - `PIC 9(01)V9(03)`: Budget Neutrality Rate
            *   `FILLER` - `PIC X(20)`: Filler
        *   `PPS-PC-DATA`: Group of PC data
            *   `PPS-COT-IND` - `PIC X(01)`: Cost Outlier Indicator
            *   `FILLER` - `PIC X(20)`: Filler
    *   `PRICER-OPT-VERS-SW`:  This structure is used to indicate the versions of the programs
        *   `PRICER-OPTION-SW` - `PIC X(01)`: Pricer Option Switch.  Used to indicate if all tables or provider records are passed
            *   `ALL-TABLES-PASSED` - `VALUE 'A'`:  Indicates all tables are passed
            *   `PROV-RECORD-PASSED` - `VALUE 'P'`: Indicates provider record passed
        *   `PPS-VERSIONS`: Group of PPS versions
            *   `PPDRV-VERSION` - `PIC X(05)`: Version of the  PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure holds provider specific data passed to the program.
        *   `PROV-NEWREC-HOLD1`: Group of Provider Data
            *   `P-NEW-NPI10`: National Provider Identifier (NPI) - 10 digits
                *   `P-NEW-NPI8` - `PIC X(08)`: First 8 digits of NPI
                *   `P-NEW-NPI-FILLER` - `PIC X(02)`: Filler for the remaining 2 digits of NPI
            *   `P-NEW-PROVIDER-NO` - `PIC X(06)`: Provider Number
                *   `P-NEW-STATE` - `PIC 9(02)`: State Code
                *   `FILLER` - `PIC X(04)`: Filler
            *   `P-NEW-DATE-DATA`: Date Information
                *   `P-NEW-EFF-DATE`:  Effective Date
                    *   `P-NEW-EFF-DT-CC` - `PIC 9(02)`: Century Component of Effective Date
                    *   `P-NEW-EFF-DT-YY` - `PIC 9(02)`: Year Component of Effective Date
                    *   `P-NEW-EFF-DT-MM` - `PIC 9(02)`: Month Component of Effective Date
                    *   `P-NEW-EFF-DT-DD` - `PIC 9(02)`: Day Component of Effective Date
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-CC` - `PIC 9(02)`: Century Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-YY` - `PIC 9(02)`: Year Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-MM` - `PIC 9(02)`: Month Component of Fiscal Year Begin Date
                    *   `P-NEW-FY-BEG-DT-DD` - `PIC 9(02)`: Day Component of Fiscal Year Begin Date
                *   `P-NEW-REPORT-DATE`: Report Date
                    *   `P-NEW-REPORT-DT-CC` - `PIC 9(02)`: Century Component of Report Date
                    *   `P-NEW-REPORT-DT-YY` - `PIC 9(02)`: Year Component of Report Date
                    *   `P-NEW-REPORT-DT-MM` - `PIC 9(02)`: Month Component of Report Date
                    *   `P-NEW-REPORT-DT-DD` - `PIC 9(02)`: Day Component of Report Date
                *   `P-NEW-TERMINATION-DATE`: Termination Date
                    *   `P-NEW-TERM-DT-CC` - `PIC 9(02)`: Century Component of Termination Date
                    *   `P-NEW-TERM-DT-YY` - `PIC 9(02)`: Year Component of Termination Date
                    *   `P-NEW-TERM-DT-MM` - `PIC 9(02)`: Month Component of Termination Date
                    *   `P-NEW-TERM-DT-DD` - `PIC 9(02)`: Day Component of Termination Date
            *   `P-NEW-WAIVER-CODE` - `PIC X(01)`: Waiver Code
                *   `P-NEW-WAIVER-STATE` - `VALUE 'Y'`: Waiver State Indicator
            *   `P-NEW-INTER-NO` - `PIC 9(05)`: Internal Number
            *   `P-NEW-PROVIDER-TYPE` - `PIC X(02)`: Provider Type
            *   `P-NEW-CURRENT-CENSUS-DIV` - `PIC 9(01)`: Current Census Division
            *   `P-NEW-CURRENT-DIV` - `PIC 9(01)`: Redefines Current Census Division
            *   `P-NEW-MSA-DATA`: MSA Data
                *   `P-NEW-CHG-CODE-INDEX` - `PIC X`: Charge Code Index
                *   `P-NEW-GEO-LOC-MSAX` - `PIC X(04)`: Geographic Location MSA
                *   `P-NEW-GEO-LOC-MSA9` - `PIC 9(04)`: Redefines Geographic Location MSA
                *   `P-NEW-WAGE-INDEX-LOC-MSA` - `PIC X(04)`: Wage Index Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA` - `PIC X(04)`: Standard Amount Location MSA
                *   `P-NEW-STAND-AMT-LOC-MSA9`: Redefines Standard Amount Location MSA
                    *   `P-NEW-RURAL-1ST`: Rural 1st
                        *   `P-NEW-STAND-RURAL` - `PIC XX`: Standard Rural
                            *   `P-NEW-STD-RURAL-CHECK` - `VALUE '  '`: Standard Rural Check
                    *   `P-NEW-RURAL-2ND` - `PIC XX`: Rural 2nd
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` - `PIC XX`: Sole Community Dependent Hospital Year
            *   `P-NEW-LUGAR` - `PIC X`: Lugar
            *   `P-NEW-TEMP-RELIEF-IND` - `PIC X`: Temporary Relief Indicator
            *   `P-NEW-FED-PPS-BLEND-IND` - `PIC X`: Federal PPS Blend Indicator
            *   `FILLER` - `PIC X(05)`: Filler
        *   `PROV-NEWREC-HOLD2`: Group of Provider Data
            *   `P-NEW-VARIABLES`: Variables
                *   `P-NEW-FAC-SPEC-RATE` - `PIC 9(05)V9(02)`: Facility Specific Rate
                *   `P-NEW-COLA` - `PIC 9(01)V9(03)`: Cost of Living Adjustment
                *   `P-NEW-INTERN-RATIO` - `PIC 9(01)V9(04)`: Intern Ratio
                *   `P-NEW-BED-SIZE` - `PIC 9(05)`: Bed Size
                *   `P-NEW-OPER-CSTCHG-RATIO` - `PIC 9(01)V9(03)`: Operating Cost to Charge Ratio
                *   `P-NEW-CMI` - `PIC 9