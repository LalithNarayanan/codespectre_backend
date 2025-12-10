## Analysis of COBOL Programs

Here's an analysis of each COBOL program provided, detailing the files accessed, data structures, and their descriptions:

### Program: LTCAL032

*   **Files Accessed:**

    *   No explicit file access is evident in the code provided.  The program uses a `COPY` statement to include `LTDRG031`, which likely contains data in a working-storage data structure.  This included data might be considered as an implicit file.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` (PIC X(46)):  A literal string used for identification, likely for debugging or informational purposes.  Contains the program name and a description.
    *   `CAL-VERSION` (PIC X(05)):  Stores the version number of the calculation logic, "C03.2".
    *   `HOLD-PPS-COMPONENTS`:  A group of variables used to store intermediate calculation results and components of the PPS (Prospective Payment System) calculation.
        *   `H-LOS` (PIC 9(03)):  Length of Stay (LOS), likely in days.
        *   `H-REG-DAYS` (PIC 9(03)):  Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)):  Short Stay Outlier Threshold, expressed as number of days.
        *   `H-BLEND-RTC` (PIC 9(02)):  Blend Return Code, indicating the blend year and payment method.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)):  Blend Factor for Facility Rate (percentage).
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)):  Blend Factor for PPS Payment (percentage).
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)):  Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)):  Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)):  Labor portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)):  Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)):  Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
    *   `W-DRG-FILLS`:  This is a large data structure (defined by the `COPY LTDRG031` statement) likely containing DRG (Diagnosis Related Group) information. The structure's content is not visible in the provided code, but it is used to look up DRG-related data.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: This data structure is used to access the DRG table.
        *   `WWM-ENTRY OCCURS 502 TIMES`:  An array of DRG entries, each with the following structure:
            *   `WWM-DRG` (PIC X(3)):  The DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)):  Relative Weight for the DRG.
            *   `WWM-ALOS` (PIC 9(2)V9(1)):  Average Length of Stay for the DRG.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the main input data structure, passed from the calling program.  It contains the bill information.
        *   `B-NPI10`:  National Provider Identifier (NPI) - 10 characters.
            *   `B-NPI8` (PIC X(08)):  First 8 digits of the NPI.
            *   `B-NPI-FILLER` (PIC X(02)):  Filler for the NPI, likely used for formatting.
        *   `B-PROVIDER-NO` (PIC X(06)):  Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)):  Patient Status.
        *   `B-DRG-CODE` (PIC X(03)):  The DRG code for the patient's stay.
        *   `B-LOS` (PIC 9(03)):  Length of Stay (LOS) in days.
        *   `B-COV-DAYS` (PIC 9(03)):  Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)):  Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:  Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)):  Century component of the discharge year.
            *   `B-DISCHG-YY` (PIC 9(02)):  Year of discharge.
            *   `B-DISCHG-MM` (PIC 9(02)):  Month of discharge.
            *   `B-DISCHG-DD` (PIC 9(02)):  Day of discharge.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)):  Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)):  Special Payment Indicator.
        *   `FILLER` (PIC X(13)):  Unused filler space.
    *   `PPS-DATA-ALL`:  This structure is used to return the calculated PPS data back to the calling program.
        *   `PPS-RTC` (PIC 9(02)):  Return Code, indicating the result of the calculation (e.g., success, various error conditions).
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)):  Charge Threshold.
        *   `PPS-DATA`:  Contains the main PPS calculation results.
            *   `PPS-MSA` (PIC X(04)):  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)):  Wage Index for the MSA.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)):  Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)):  Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)):  Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)):  Length of Stay (LOS) used in the calculation.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)):  DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)):  Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)):  Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)):  Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)):  Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)):  Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)):  Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)):  Regular days used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)):  Lifetime Reserve Days used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)):  Blend Year Indicator.
            *   `PPS-COLA` (PIC 9(01)V9(03)):  Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)):  Filler space.
        *   `PPS-OTHER-DATA`:  Contains other PPS-related data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)):  National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)):  National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)):  Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)):  Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)):  Filler space.
        *   `PPS-PC-DATA`:  PPS Payment Component Data.
            *   `PPS-COT-IND` (PIC X(01)):  Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)):  Filler space.
    *   `PRICER-OPT-VERS-SW`:  Contains flags for which data tables are being passed.
        *   `PRICER-OPTION-SW` (PIC X(01)):  Option switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'):  Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'):  Indicates provider record is passed.
        *   `PPS-VERSIONS`:  PPS Version information.
            *   `PPDRV-VERSION` (PIC X(05)):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure contains provider-specific information.
        *   `PROV-NEWREC-HOLD1`:  Holds the provider record.
            *   `P-NEW-NPI10`:  Provider NPI (National Provider Identifier).
                *   `P-NEW-NPI8` (PIC X(08)):  First 8 digits of the NPI.
                *   `P-NEW-NPI-FILLER` (PIC X(02)):  Filler for the NPI.
            *   `P-NEW-PROVIDER-NO`:  Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)):  State code.
                *   `FILLER` (PIC X(04)):  Filler.
            *   `P-NEW-DATE-DATA`:  Date information.
                *   `P-NEW-EFF-DATE`:  Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)):  Effective Date Century.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)):  Effective Date Year.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)):  Effective Date Month.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)):  Effective Date Day.
                *   `P-NEW-FY-BEGIN-DATE`:  Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)):  Fiscal Year Begin Date Century.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)):  Fiscal Year Begin Date Year.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)):  Fiscal Year Begin Date Month.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)):  Fiscal Year Begin Date Day.
                *   `P-NEW-REPORT-DATE`:  Reporting Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)):  Reporting Date Century.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)):  Reporting Date Year.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)):  Reporting Date Month.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)):  Reporting Date Day.
                *   `P-NEW-TERMINATION-DATE`:  Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)):  Termination Date Century.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)):  Termination Date Year.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)):  Termination Date Month.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)):  Termination Date Day.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)):  Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'):  Waiver State indicator (value is 'Y').
            *   `P-NEW-INTER-NO` (PIC 9(05)):  Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)):  Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)):  Current Census Division.
            *   `P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Redefines the current census division.
            *   `P-NEW-MSA-DATA`:  MSA (Metropolitan Statistical Area) related data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X):  Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)):  Geographic Location MSA (alphanumeric).
                *   `P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX` (PIC 9(04)):  Geographic Location MSA (numeric).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)):  Wage Index Location MSA (alphanumeric).
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)):  Standard Amount Location MSA (alphanumeric).
                *   `P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`:  Standard Amount Location MSA (numeric).
                    *   `P-NEW-RURAL-1ST`: Rural indicator.
                        *   `P-NEW-STAND-RURAL` (PIC XX): Rural indicator.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): Value for rural check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural indicator.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX):  Sole Community Hospital Year.
            *   `P-NEW-LUGAR` (PIC X):  Lugar indicator.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X):  Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X):  Federal PPS Blend Indicator.
            *   `FILLER` (PIC X(05)):  Filler.
        *   `PROV-NEWREC-HOLD2`:  Holds provider variables.
            *   `P-NEW-VARIABLES`:  Provider variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)):  Cost of Living Adjustment.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)):  Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)):  Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)):  Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)):  Case Mix Index.
                *   `P-NEW-SSI-RATIO` (PIC V9(04)):  SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)):  Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)):  PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)):  PRUF Update Factor.
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)):  DSH Percentage.
                *   `P-NEW-FYE-DATE` (PIC X(08)):  Fiscal Year End Date.
            *   `FILLER` (PIC X(23)):  Filler.
        *   `PROV-NEWREC-HOLD3`:  Holds pass amount data.
            *   `P-NEW-PASS-AMT-DATA`:  Pass-through Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99):  Capital Pass-Through Amount.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99):  Direct Medical Education Pass-Through Amount.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99):  Organ Acquisition Pass-Through Amount.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99):  Plus Miscellaneous Pass-Through Amount.
            *   `P-NEW-CAPI-DATA`:  Capital Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X):  Capital PPS Payment Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99):  Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99):  Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999):  Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999):  Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` (PIC X):  Capital New Hospital Indicator.
                *   `P-NEW-CAPI-IME` (PIC 9V9999):  Capital IME (Indirect Medical Education).
                *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99):  Capital Exceptions.
            *   `FILLER` (PIC X(22)):  Filler.
    *   `WAGE-NEW-INDEX-RECORD`:  Wage index record.
        *   `W-MSA` (PIC X(4)):  MSA code.
        *   `W-EFF-DATE` (PIC X(8)):  Effective Date.
        *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage Index 1.
        *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage Index 2.
        *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage Index 3.

### Program: LTCAL042

*   **Files Accessed:**

    *   No explicit file access is evident in the code provided.  The program uses a `COPY` statement to include `LTDRG031`, which likely contains data in a working-storage data structure.  This included data might be considered as an implicit file.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `W-STORAGE-REF` (PIC X(46)):  A literal string used for identification, likely for debugging or informational purposes.  Contains the program name and a description.
    *   `CAL-VERSION` (PIC X(05)):  Stores the version number of the calculation logic, "C04.2".
    *   `HOLD-PPS-COMPONENTS`:  A group of variables used to store intermediate calculation results and components of the PPS (Prospective Payment System) calculation.
        *   `H-LOS` (PIC 9(03)):  Length of Stay (LOS), likely in days.
        *   `H-REG-DAYS` (PIC 9(03)):  Regular days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total days.
        *   `H-SSOT` (PIC 9(02)):  Short Stay Outlier Threshold, expressed as number of days.
        *   `H-BLEND-RTC` (PIC 9(02)):  Blend Return Code, indicating the blend year and payment method.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)):  Blend Factor for Facility Rate (percentage).
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)):  Blend Factor for PPS Payment (percentage).
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)):  Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)):  Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)):  Labor portion of the payment.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)):  Non-labor portion of the payment.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)):  Fixed loss amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New facility specific rate.
        *   `H-LOS-RATIO` (PIC 9(01)V9(05)): Length of Stay Ratio.
    *   `W-DRG-FILLS`:  This is a large data structure (defined by the `COPY LTDRG031` statement) likely containing DRG (Diagnosis Related Group) information. The structure's content is not visible in the provided code, but it is used to look up DRG-related data.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: This data structure is used to access the DRG table.
        *   `WWM-ENTRY OCCURS 502 TIMES`:  An array of DRG entries, each with the following structure:
            *   `WWM-DRG` (PIC X(3)):  The DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)):  Relative Weight for the DRG.
            *   `WWM-ALOS` (PIC 9(2)V9(1)):  Average Length of Stay for the DRG.

*   **Data Structures in LINKAGE SECTION:**

    *   `BILL-NEW-DATA`:  This is the main input data structure, passed from the calling program.  It contains the bill information.
        *   `B-NPI10`:  National Provider Identifier (NPI) - 10 characters.
            *   `B-NPI8` (PIC X(08)):  First 8 digits of the NPI.
            *   `B-NPI-FILLER` (PIC X(02)):  Filler for the NPI, likely used for formatting.
        *   `B-PROVIDER-NO` (PIC X(06)):  Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)):  Patient Status.
        *   `B-DRG-CODE` (PIC X(03)):  The DRG code for the patient's stay.
        *   `B-LOS` (PIC 9(03)):  Length of Stay (LOS) in days.
        *   `B-COV-DAYS` (PIC 9(03)):  Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)):  Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`:  Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)):  Century component of the discharge year.
            *   `B-DISCHG-YY` (PIC 9(02)):  Year of discharge.
            *   `B-DISCHG-MM` (PIC 9(02)):  Month of discharge.
            *   `B-DISCHG-DD` (PIC 9(02)):  Day of discharge.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)):  Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)):  Special Payment Indicator.
        *   `FILLER` (PIC X(13)):  Unused filler space.
    *   `PPS-DATA-ALL`:  This structure is used to return the calculated PPS data back to the calling program.
        *   `PPS-RTC` (PIC 9(02)):  Return Code, indicating the result of the calculation (e.g., success, various error conditions).
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)):  Charge Threshold.
        *   `PPS-DATA`:  Contains the main PPS calculation results.
            *   `PPS-MSA` (PIC X(04)):  Metropolitan Statistical Area (MSA) code.
            *   `PPS-WAGE-INDEX` (PIC 9(02)V9(04)):  Wage Index for the MSA.
            *   `PPS-AVG-LOS` (PIC 9(02)V9(01)):  Average Length of Stay for the DRG.
            *   `PPS-RELATIVE-WGT` (PIC 9(01)V9(04)):  Relative Weight for the DRG.
            *   `PPS-OUTLIER-PAY-AMT` (PIC 9(07)V9(02)):  Outlier Payment Amount.
            *   `PPS-LOS` (PIC 9(03)):  Length of Stay (LOS) used in the calculation.
            *   `PPS-DRG-ADJ-PAY-AMT` (PIC 9(07)V9(02)):  DRG Adjusted Payment Amount.
            *   `PPS-FED-PAY-AMT` (PIC 9(07)V9(02)):  Federal Payment Amount.
            *   `PPS-FINAL-PAY-AMT` (PIC 9(07)V9(02)):  Final Payment Amount.
            *   `PPS-FAC-COSTS` (PIC 9(07)V9(02)):  Facility Costs.
            *   `PPS-NEW-FAC-SPEC-RATE` (PIC 9(07)V9(02)): New facility specific rate.
            *   `PPS-OUTLIER-THRESHOLD` (PIC 9(07)V9(02)):  Outlier Threshold.
            *   `PPS-SUBM-DRG-CODE` (PIC X(03)):  Submitted DRG Code.
            *   `PPS-CALC-VERS-CD` (PIC X(05)):  Calculation Version Code.
            *   `PPS-REG-DAYS-USED` (PIC 9(03)):  Regular days used.
            *   `PPS-LTR-DAYS-USED` (PIC 9(03)):  Lifetime Reserve Days used.
            *   `PPS-BLEND-YEAR` (PIC 9(01)):  Blend Year Indicator.
            *   `PPS-COLA` (PIC 9(01)V9(03)):  Cost of Living Adjustment.
            *   `FILLER` (PIC X(04)):  Filler space.
        *   `PPS-OTHER-DATA`:  Contains other PPS-related data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)):  National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)):  National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)):  Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)):  Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)):  Filler space.
        *   `PPS-PC-DATA`:  PPS Payment Component Data.
            *   `PPS-COT-IND` (PIC X(01)):  Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)):  Filler space.
    *   `PRICER-OPT-VERS-SW`:  Contains flags for which data tables are being passed.
        *   `PRICER-OPTION-SW` (PIC X(01)):  Option switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'):  Indicates all tables are passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'):  Indicates provider record is passed.
        *   `PPS-VERSIONS`:  PPS Version information.
            *   `PPDRV-VERSION` (PIC X(05)):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  This structure contains provider-specific information.
        *   `PROV-NEWREC-HOLD1`:  Holds the provider record.
            *   `P-NEW-NPI10`:  Provider NPI (National Provider Identifier).
                *   `P-NEW-NPI8` (PIC X(08)):  First 8 digits of the NPI.
                *   `P-NEW-NPI-FILLER` (PIC X(02)):  Filler for the NPI.
            *   `P-NEW-PROVIDER-NO`:  Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)):  State code.
                *   `FILLER` (PIC X(04)):  Filler.
            *   `P-NEW-DATE-DATA`:  Date information.
                *   `P-NEW-EFF-DATE`:  Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)):  Effective Date Century.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)):  Effective Date Year.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)):  Effective Date Month.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)):  Effective Date Day.
                *   `P-NEW-FY-BEGIN-DATE`:  Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)):  Fiscal Year Begin Date Century.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)):  Fiscal Year Begin Date Year.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)):  Fiscal Year Begin Date Month.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)):  Fiscal Year Begin Date Day.
                *   `P-NEW-REPORT-DATE`:  Reporting Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)):  Reporting Date Century.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)):  Reporting Date Year.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)):  Reporting Date Month.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)):  Reporting Date Day.
                *   `P-NEW-TERMINATION-DATE`:  Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)):  Termination Date Century.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)):  Termination Date Year.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)):  Termination Date Month.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)):  Termination Date Day.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)):  Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'):  Waiver State indicator (value is 'Y').
            *   `P-NEW-INTER-NO` (PIC 9(05)):  Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)):  Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)):  Current Census Division.
            *   `P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Redefines the current census division.
            *   `P-NEW-MSA-DATA`:  MSA (Metropolitan Statistical Area) related data