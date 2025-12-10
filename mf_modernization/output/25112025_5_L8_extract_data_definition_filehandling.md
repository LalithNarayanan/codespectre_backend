## Analysis of COBOL Programs

Here's an analysis of each COBOL program, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements are present in the code. The program uses a `COPY` statement to include `LTDRG031`, which likely contains data used for calculations (e.g., DRG codes, relative weights, average lengths of stay).

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` (PIC X(46)):  A literal string used for identification purposes.
    *   `CAL-VERSION` (PIC X(05)):  Stores the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`: A group item used to store various components related to PPS calculations.
        *   `H-LOS` (PIC 9(03)): Length of Stay (LOS).
        *   `H-REG-DAYS` (PIC 9(03)): Regular Days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total Days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Facility Factor.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend PPS Factor.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-Labor Portion.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
    *   Data structures defined by `COPY LTDRG031` (See LTDRG031 analysis).

*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:  A group item representing the bill data passed from the calling program.
        *   `B-NPI10`: National Provider Identifier (NPI).
            *   `B-NPI8` (PIC X(08)):  NPI (8 characters).
            *   `B-NPI-FILLER` (PIC X(02)): Filler for NPI.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): DRG Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century/Current Code.
            *   `B-DISCHG-YY` (PIC 9(02)): Year.
            *   `B-DISCHG-MM` (PIC 9(02)): Month.
            *   `B-DISCHG-DD` (PIC 9(02)): Day.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`: A group item to return the calculated PPS data to the calling program.
        *   `PPS-RTC` (PIC 9(02)): Return Code.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge Threshold.
        *   `PPS-DATA`: PPS Data.
            *   `PPS-MSA` (PIC X(04)): MSA Code.
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
            *   `PPS-COLA` (PIC 9(01)V9(03)): COLA (Cost of Living Adjustment).
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Other PPS Data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: PPS PC Data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`:  Pricer Option/Version Switch.
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'):  Indicates all tables passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates provider record passed.
        *   `PPS-VERSIONS`: PPS Versions.
            *   `PPDRV-VERSION` (PIC X(05)):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  Provider Record Hold Area.  Contains provider-specific data.
        *   `PROV-NEWREC-HOLD1`: Provider Record Hold 1.
            *   `P-NEW-NPI10`: New NPI.
                *   `P-NEW-NPI8` (PIC X(08)): NPI (8 Characters).
                *   `P-NEW-NPI-FILLER` (PIC X(02)): Filler.
            *   `P-NEW-PROVIDER-NO`: New Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)): State Code.
                *   `FILLER` (PIC X(04)): Filler.
            *   `P-NEW-DATE-DATA`: New Date Data.
                *   `P-NEW-EFF-DATE`: Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Day.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Census Division.
            *   `P-NEW-CURRENT-DIV` (REDEFINES `P-NEW-CURRENT-CENSUS-DIV`): Census Division (Redefined).
            *   `P-NEW-MSA-DATA`: MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geo Location MSA (Just Right).
                *   `P-NEW-GEO-LOC-MSA9` (REDEFINES `P-NEW-GEO-LOC-MSAX`): Geo Location MSA (Redefined).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA (Just Right).
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA (Just Right).
                *   `P-NEW-STAND-AMT-LOC-MSA9` (REDEFINES `P-NEW-STAND-AMT-LOC-MSA`): Standard Amount Location MSA (Redefined).
                    *   `P-NEW-RURAL-1ST`: Rural 1st.
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural 2nd.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` (PIC X): Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler.
        *   `PROV-NEWREC-HOLD2`: Provider Record Hold 2.
            *   `P-NEW-VARIABLES`: New Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): COLA.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI.
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent.
                *   `P-NEW-FYE-DATE` (PIC X(08)): Fiscal Year End Date.
            *   `FILLER` (PIC X(23)): Filler.
        *   `PROV-NEWREC-HOLD3`: Provider Record Hold 3.
            *   `P-NEW-PASS-AMT-DATA`: Passed Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Passed Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Passed Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Passed Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Passed Amount Plus Misc.
            *   `P-NEW-CAPI-DATA`: Capital Data.
                *   `P-NEW-CAPI-PPS-PAY-CODE` (PIC X): Capital PPS Pay Code.
                *   `P-NEW-CAPI-HOSP-SPEC-RATE` (PIC 9(04)V99): Capital Hospital Specific Rate.
                *   `P-NEW-CAPI-OLD-HARM-RATE` (PIC 9(04)V99): Capital Old Harm Rate.
                *   `P-NEW-CAPI-NEW-HARM-RATIO` (PIC 9(01)V9999): Capital New Harm Ratio.
                *   `P-NEW-CAPI-CSTCHG-RATIO` (PIC 9V999): Capital Cost to Charge Ratio.
                *   `P-NEW-CAPI-NEW-HOSP` (PIC X): Capital New Hospital.
                *   `P-NEW-CAPI-IME` (PIC 9V9999): Capital IME.
                *   `P-NEW-CAPI-EXCEPTIONS` (PIC 9(04)V99): Capital Exceptions.
            *   `FILLER` (PIC X(22)): Filler.
    *   `WAGE-NEW-INDEX-RECORD`: Wage Index Record. Contains wage index data.
        *   `W-MSA` (PIC X(4)): MSA Code.
        *   `W-EFF-DATE` (PIC X(8)): Effective Date.
        *   `W-WAGE-INDEX1` (PIC S9(02)V9(04)): Wage Index 1.
        *   `W-WAGE-INDEX2` (PIC S9(02)V9(04)): Wage Index 2.
        *   `W-WAGE-INDEX3` (PIC S9(02)V9(04)): Wage Index 3.

*   **Procedure Division:**
    *   The `PROCEDURE DIVISION` uses the `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PRICER-OPT-VERS-SW`, `PROV-NEW-HOLD`, and `WAGE-NEW-INDEX-RECORD` data structures defined in the `LINKAGE SECTION`. This indicates that the program is a subroutine (or called program) that receives these data structures as input and returns results through `PPS-DATA-ALL`.

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements are present in the code. The program uses a `COPY` statement to include `LTDRG031`, which likely contains data used for calculations (e.g., DRG codes, relative weights, average lengths of stay).

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF` (PIC X(46)):  A literal string used for identification purposes.
    *   `CAL-VERSION` (PIC X(05)):  Stores the version of the calculation logic.
    *   `HOLD-PPS-COMPONENTS`: A group item used to store various components related to PPS calculations.
        *   `H-LOS` (PIC 9(03)): Length of Stay (LOS).
        *   `H-REG-DAYS` (PIC 9(03)): Regular Days.
        *   `H-TOTAL-DAYS` (PIC 9(05)): Total Days.
        *   `H-SSOT` (PIC 9(02)): Short Stay Outlier Threshold.
        *   `H-BLEND-RTC` (PIC 9(02)): Blend Return Code.
        *   `H-BLEND-FAC` (PIC 9(01)V9(01)): Blend Facility Factor.
        *   `H-BLEND-PPS` (PIC 9(01)V9(01)): Blend PPS Factor.
        *   `H-SS-PAY-AMT` (PIC 9(07)V9(02)): Short Stay Payment Amount.
        *   `H-SS-COST` (PIC 9(07)V9(02)): Short Stay Cost.
        *   `H-LABOR-PORTION` (PIC 9(07)V9(06)): Labor Portion.
        *   `H-NONLABOR-PORTION` (PIC 9(07)V9(06)): Non-Labor Portion.
        *   `H-FIXED-LOSS-AMT` (PIC 9(07)V9(02)): Fixed Loss Amount.
        *   `H-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): New Facility Specific Rate.
        *   `H-LOS-RATIO` (PIC 9(01)V9(05)): Length of Stay Ratio.
    *   Data structures defined by `COPY LTDRG031` (See LTDRG031 analysis).

*   **Data Structures in LINKAGE SECTION:**
    *   `BILL-NEW-DATA`:  A group item representing the bill data passed from the calling program.
        *   `B-NPI10`: National Provider Identifier (NPI).
            *   `B-NPI8` (PIC X(08)):  NPI (8 characters).
            *   `B-NPI-FILLER` (PIC X(02)): Filler for NPI.
        *   `B-PROVIDER-NO` (PIC X(06)): Provider Number.
        *   `B-PATIENT-STATUS` (PIC X(02)): Patient Status.
        *   `B-DRG-CODE` (PIC X(03)): DRG Code.
        *   `B-LOS` (PIC 9(03)): Length of Stay.
        *   `B-COV-DAYS` (PIC 9(03)): Covered Days.
        *   `B-LTR-DAYS` (PIC 9(02)): Lifetime Reserve Days.
        *   `B-DISCHARGE-DATE`: Discharge Date.
            *   `B-DISCHG-CC` (PIC 9(02)): Century/Current Code.
            *   `B-DISCHG-YY` (PIC 9(02)): Year.
            *   `B-DISCHG-MM` (PIC 9(02)): Month.
            *   `B-DISCHG-DD` (PIC 9(02)): Day.
        *   `B-COV-CHARGES` (PIC 9(07)V9(02)): Covered Charges.
        *   `B-SPEC-PAY-IND` (PIC X(01)): Special Payment Indicator.
        *   `FILLER` (PIC X(13)): Filler.
    *   `PPS-DATA-ALL`: A group item to return the calculated PPS data to the calling program.
        *   `PPS-RTC` (PIC 9(02)): Return Code.
        *   `PPS-CHRG-THRESHOLD` (PIC 9(07)V9(02)): Charge Threshold.
        *   `PPS-DATA`: PPS Data.
            *   `PPS-MSA` (PIC X(04)): MSA Code.
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
            *   `PPS-COLA` (PIC 9(01)V9(03)): COLA (Cost of Living Adjustment).
            *   `FILLER` (PIC X(04)): Filler.
        *   `PPS-OTHER-DATA`: Other PPS Data.
            *   `PPS-NAT-LABOR-PCT` (PIC 9(01)V9(05)): National Labor Percentage.
            *   `PPS-NAT-NONLABOR-PCT` (PIC 9(01)V9(05)): National Non-Labor Percentage.
            *   `PPS-STD-FED-RATE` (PIC 9(05)V9(02)): Standard Federal Rate.
            *   `PPS-BDGT-NEUT-RATE` (PIC 9(01)V9(03)): Budget Neutrality Rate.
            *   `FILLER` (PIC X(20)): Filler.
        *   `PPS-PC-DATA`: PPS PC Data.
            *   `PPS-COT-IND` (PIC X(01)): Cost Outlier Indicator.
            *   `FILLER` (PIC X(20)): Filler.
    *   `PRICER-OPT-VERS-SW`:  Pricer Option/Version Switch.
        *   `PRICER-OPTION-SW` (PIC X(01)): Pricer Option Switch.
            *   `ALL-TABLES-PASSED` (VALUE 'A'):  Indicates all tables passed.
            *   `PROV-RECORD-PASSED` (VALUE 'P'): Indicates provider record passed.
        *   `PPS-VERSIONS`: PPS Versions.
            *   `PPDRV-VERSION` (PIC X(05)):  Version of the PPDRV program.
    *   `PROV-NEW-HOLD`:  Provider Record Hold Area.  Contains provider-specific data.
        *   `PROV-NEWREC-HOLD1`: Provider Record Hold 1.
            *   `P-NEW-NPI10`: New NPI.
                *   `P-NEW-NPI8` (PIC X(08)): NPI (8 Characters).
                *   `P-NEW-NPI-FILLER` (PIC X(02)): Filler.
            *   `P-NEW-PROVIDER-NO`: New Provider Number.
                *   `P-NEW-STATE` (PIC 9(02)): State Code.
                *   `FILLER` (PIC X(04)): Filler.
            *   `P-NEW-DATE-DATA`: New Date Data.
                *   `P-NEW-EFF-DATE`: Effective Date.
                    *   `P-NEW-EFF-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-EFF-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-EFF-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-EFF-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `P-NEW-FY-BEG-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-FY-BEG-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-FY-BEG-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-FY-BEG-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-REPORT-DATE`: Report Date.
                    *   `P-NEW-REPORT-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-REPORT-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-REPORT-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-REPORT-DT-DD` (PIC 9(02)): Day.
                *   `P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `P-NEW-TERM-DT-CC` (PIC 9(02)): Century/Current Code.
                    *   `P-NEW-TERM-DT-YY` (PIC 9(02)): Year.
                    *   `P-NEW-TERM-DT-MM` (PIC 9(02)): Month.
                    *   `P-NEW-TERM-DT-DD` (PIC 9(02)): Day.
            *   `P-NEW-WAIVER-CODE` (PIC X(01)): Waiver Code.
                *   `P-NEW-WAIVER-STATE` (VALUE 'Y'): Waiver State.
            *   `P-NEW-INTER-NO` (PIC 9(05)): Internal Number.
            *   `P-NEW-PROVIDER-TYPE` (PIC X(02)): Provider Type.
            *   `P-NEW-CURRENT-CENSUS-DIV` (PIC 9(01)): Census Division.
            *   `P-NEW-CURRENT-DIV` (REDEFINES `P-NEW-CURRENT-CENSUS-DIV`): Census Division (Redefined).
            *   `P-NEW-MSA-DATA`: MSA Data.
                *   `P-NEW-CHG-CODE-INDEX` (PIC X): Charge Code Index.
                *   `P-NEW-GEO-LOC-MSAX` (PIC X(04)): Geo Location MSA (Just Right).
                *   `P-NEW-GEO-LOC-MSA9` (REDEFINES `P-NEW-GEO-LOC-MSAX`): Geo Location MSA (Redefined).
                *   `P-NEW-WAGE-INDEX-LOC-MSA` (PIC X(04)): Wage Index Location MSA (Just Right).
                *   `P-NEW-STAND-AMT-LOC-MSA` (PIC X(04)): Standard Amount Location MSA (Just Right).
                *   `P-NEW-STAND-AMT-LOC-MSA9` (REDEFINES `P-NEW-STAND-AMT-LOC-MSA`): Standard Amount Location MSA (Redefined).
                    *   `P-NEW-RURAL-1ST`: Rural 1st.
                        *   `P-NEW-STAND-RURAL` (PIC XX): Standard Rural.
                            *   `P-NEW-STD-RURAL-CHECK` (VALUE '  '): Standard Rural Check.
                        *   `P-NEW-RURAL-2ND` (PIC XX): Rural 2nd.
            *   `P-NEW-SOL-COM-DEP-HOSP-YR` (PIC XX): Sole Community Dependent Hospital Year.
            *   `P-NEW-LUGAR` (PIC X): Lugar.
            *   `P-NEW-TEMP-RELIEF-IND` (PIC X): Temporary Relief Indicator.
            *   `P-NEW-FED-PPS-BLEND-IND` (PIC X): Federal PPS Blend Indicator.
            *   `FILLER` (PIC X(05)): Filler.
        *   `PROV-NEWREC-HOLD2`: Provider Record Hold 2.
            *   `P-NEW-VARIABLES`: New Variables.
                *   `P-NEW-FAC-SPEC-RATE` (PIC 9(05)V9(02)): Facility Specific Rate.
                *   `P-NEW-COLA` (PIC 9(01)V9(03)): COLA.
                *   `P-NEW-INTERN-RATIO` (PIC 9(01)V9(04)): Intern Ratio.
                *   `P-NEW-BED-SIZE` (PIC 9(05)): Bed Size.
                *   `P-NEW-OPER-CSTCHG-RATIO` (PIC 9(01)V9(03)): Operating Cost to Charge Ratio.
                *   `P-NEW-CMI` (PIC 9(01)V9(04)): CMI.
                *   `P-NEW-SSI-RATIO` (PIC V9(04)): SSI Ratio.
                *   `P-NEW-MEDICAID-RATIO` (PIC V9(04)): Medicaid Ratio.
                *   `P-NEW-PPS-BLEND-YR-IND` (PIC 9(01)): PPS Blend Year Indicator.
                *   `P-NEW-PRUF-UPDTE-FACTOR` (PIC 9(01)V9(05)): Pruf Update Factor.
                *   `P-NEW-DSH-PERCENT` (PIC V9(04)): DSH Percent.
                *   `P-NEW-FYE-DATE` (PIC X(08)): Fiscal Year End Date.
            *   `FILLER` (PIC X(23)): Filler.
        *   `PROV-NEWREC-HOLD3`: Provider Record Hold 3.
            *   `P-NEW-PASS-AMT-DATA`: Passed Amount Data.
                *   `P-NEW-PASS-AMT-CAPITAL` (PIC 9(04)V99): Passed Amount Capital.
                *   `P-NEW-PASS-AMT-DIR-MED-ED` (PIC 9(04)V99): Passed Amount Direct Medical Education.
                *   `P-NEW-PASS-AMT-ORGAN-ACQ` (PIC 9(04)V99): Passed Amount Organ Acquisition.
                *   `P-NEW-PASS-AMT-PLUS-MISC` (PIC 9(04)V99): Passed Amount Plus Misc.
            *   `