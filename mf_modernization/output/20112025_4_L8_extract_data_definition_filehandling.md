## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file accesses, data structures in the WORKING-STORAGE SECTION, and data structures in the LINKAGE SECTION.

### Program: LTCAL032

#### Files Accessed:

*   **None Explicitly Defined:** The program doesn't have any explicit `SELECT` statements for file access in the `FILE-CONTROL` section. However, it `COPY`s `LTDRG031`, which likely contains data used in calculations.

#### WORKING-STORAGE SECTION Data Structures:

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  Used for storing a literal string identifying the program and its purpose.
    *   `VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string.

*   **`CAL-VERSION`**:
    *   `PIC X(05)`:  Used to store the version number of the calculation logic.
    *   `VALUE 'C03.2'`:  Initializes the field with the version string.

*   **`HOLD-PPS-COMPONENTS`**: This structure is used to hold intermediate calculation results and components.  It's likely used to store values needed during the PPS (Prospective Payment System) calculation.
    *   `H-LOS` (`PIC 9(03)`): Length of Stay.
    *   `H-REG-DAYS` (`PIC 9(03)`): Regular days.
    *   `H-TOTAL-DAYS` (`PIC 9(05)`): Total days.
    *   `H-SSOT` (`PIC 9(02)`):  Short Stay Outlier Threshold.
    *   `H-BLEND-RTC` (`PIC 9(02)`): Blend Return To Code.
    *   `H-BLEND-FAC` (`PIC 9(01)V9(01)`): Blend Facility Rate.
    *   `H-BLEND-PPS` (`PIC 9(01)V9(01)`): Blend PPS Rate.
    *   `H-SS-PAY-AMT` (`PIC 9(07)V9(02)`): Short Stay Payment Amount.
    *   `H-SS-COST` (`PIC 9(07)V9(02)`): Short Stay Cost.
    *   `H-LABOR-PORTION` (`PIC 9(07)V9(06)`): Labor Portion of the payment.
    *   `H-NONLABOR-PORTION` (`PIC 9(07)V9(06)`): Non-Labor Portion of the payment.
    *   `H-FIXED-LOSS-AMT` (`PIC 9(07)V9(02)`): Fixed Loss Amount.
    *   `H-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`): New facility specific rate.

*   **Data structures defined by COPY LTDRG031:** The program copies the contents of `LTDRG031`. This file contains the DRG table.

*   **`PPS-DATA-ALL`**: This is a large structure that likely holds all the data returned to the calling program.
    *   `PPS-RTC` (`PIC 9(02)`): Return Code, indicating the payment status.
    *   `PPS-CHRG-THRESHOLD` (`PIC 9(07)V9(02)`): Charge Threshold.
    *   `PPS-DATA`: Contains various PPS related data.
        *   `PPS-MSA` (`PIC X(04)`): MSA (Metropolitan Statistical Area) code.
        *   `PPS-WAGE-INDEX` (`PIC 9(02)V9(04)`): Wage Index.
        *   `PPS-AVG-LOS` (`PIC 9(02)V9(01)`): Average Length of Stay.
        *   `PPS-RELATIVE-WGT` (`PIC 9(01)V9(04)`): Relative Weight.
        *   `PPS-OUTLIER-PAY-AMT` (`PIC 9(07)V9(02)`): Outlier Payment Amount.
        *   `PPS-LOS` (`PIC 9(03)`): Length of Stay.
        *   `PPS-DRG-ADJ-PAY-AMT` (`PIC 9(07)V9(02)`): DRG Adjusted Payment Amount.
        *   `PPS-FED-PAY-AMT` (`PIC 9(07)V9(02)`): Federal Payment Amount.
        *   `PPS-FINAL-PAY-AMT` (`PIC 9(07)V9(02)`): Final Payment Amount.
        *   `PPS-FAC-COSTS` (`PIC 9(07)V9(02)`): Facility Costs.
        *   `PPS-NEW-FAC-SPEC-RATE` (`PIC 9(07)V9(02)`): New Facility Specific Rate.
        *   `PPS-OUTLIER-THRESHOLD` (`PIC 9(07)V9(02)`): Outlier Threshold.
        *   `PPS-SUBM-DRG-CODE` (`PIC X(03)`): Submitted DRG Code.
        *   `PPS-CALC-VERS-CD` (`PIC X(05)`): Calculation Version Code.
        *   `PPS-REG-DAYS-USED` (`PIC 9(03)`): Regular Days Used.
        *   `PPS-LTR-DAYS-USED` (`PIC 9(03)`): Lifetime Reserve Days Used.
        *   `PPS-BLEND-YEAR` (`PIC 9(01)`): Blend Year.
        *   `PPS-COLA` (`PIC 9(01)V9(03)`): Cost of Living Adjustment.
        *   `FILLER` (`PIC X(04)`): Filler space.
    *   `PPS-OTHER-DATA`: Contains other PPS data.
        *   `PPS-NAT-LABOR-PCT` (`PIC 9(01)V9(05)`): National Labor Percentage.
        *   `PPS-NAT-NONLABOR-PCT` (`PIC 9(01)V9(05)`): National Non-Labor Percentage.
        *   `PPS-STD-FED-RATE` (`PIC 9(05)V9(02)`): Standard Federal Rate.
        *   `PPS-BDGT-NEUT-RATE` (`PIC 9(01)V9(03)`): Budget Neutrality Rate.
        *   `FILLER` (`PIC X(20)`): Filler space.
    *   `PPS-PC-DATA`: Contains PPS patient care data.
        *   `PPS-COT-IND` (`PIC X(01)`): Cost Outlier Indicator.
        *   `FILLER` (`PIC X(20)`): Filler space.

*   **`PRICER-OPT-VERS-SW`**:
    *   `PRICER-OPTION-SW` (`PIC X(01)`):  A switch that determines which version of the pricer is used.
        *   `ALL-TABLES-PASSED` (`VALUE 'A'`):  Indicates all tables are passed.
        *   `PROV-RECORD-PASSED` (`VALUE 'P'`): Indicates Provider Record is passed.
    *   `PPS-VERSIONS`:
        *   `PPDRV-VERSION` (`PIC X(05)`): Version of the PPDRV program.

#### LINKAGE SECTION Data Structures:

*   **`BILL-NEW-DATA`**:  This is the input data structure passed to the program, likely representing a patient's bill.
    *   `B-NPI10`: NPI (National Provider Identifier)
        *   `B-NPI8` (`PIC X(08)`): The 8-character NPI.
        *   `B-NPI-FILLER` (`PIC X(02)`): Filler for NPI.
    *   `B-PROVIDER-NO` (`PIC X(06)`): Provider Number.
    *   `B-PATIENT-STATUS` (`PIC X(02)`): Patient Status.
    *   `B-DRG-CODE` (`PIC X(03)`): DRG (Diagnosis Related Group) Code.
    *   `B-LOS` (`PIC 9(03)`): Length of Stay.
    *   `B-COV-DAYS` (`PIC 9(03)`): Covered Days.
    *   `B-LTR-DAYS` (`PIC 9(02)`): Lifetime Reserve Days.
    *   `B-DISCHARGE-DATE`: Discharge Date.
        *   `B-DISCHG-CC` (`PIC 9(02)`): Century Code for discharge date.
        *   `B-DISCHG-YY` (`PIC 9(02)`): Year of discharge date.
        *   `B-DISCHG-MM` (`PIC 9(02)`): Month of discharge date.
        *   `B-DISCHG-DD` (`PIC 9(02)`): Day of discharge date.
    *   `B-COV-CHARGES` (`PIC 9(07)V9(02)`): Covered Charges.
    *   `B-SPEC-PAY-IND` (`PIC X(01)`): Special Payment Indicator.
    *   `FILLER` (`PIC X(13)`): Filler space.

*   **`PPS-DATA-ALL`**: This is a large structure that likely holds all the data returned to the calling program. (Identical to the one in Working Storage).

*   **`PRICER-OPT-VERS-SW`**: (Identical to the one in Working Storage)

*   **`PROV-NEW-HOLD`**: This structure likely holds provider-specific information.
    *   `PROV-NEWREC-HOLD1`: Holds provider record information.
        *   `P-NEW-NPI10`: NPI (National Provider Identifier)
            *   `P-NEW-NPI8` (`PIC X(08)`): The 8-character NPI.
            *   `P-NEW-NPI-FILLER` (`PIC X(02)`): Filler for NPI.
        *   `P-NEW-PROVIDER-NO`: Provider Number.
            *   `P-NEW-STATE` (`PIC 9(02)`): State.
            *   `FILLER` (`PIC X(04)`): Filler space.
        *   `P-NEW-DATE-DATA`: Date Information.
            *   `P-NEW-EFF-DATE`: Effective Date.
                *   `P-NEW-EFF-DT-CC` (`PIC 9(02)`): Century Code for effective date.
                *   `P-NEW-EFF-DT-YY` (`PIC 9(02)`): Year of effective date.
                *   `P-NEW-EFF-DT-MM` (`PIC 9(02)`): Month of effective date.
                *   `P-NEW-EFF-DT-DD` (`PIC 9(02)`): Day of effective date.
            *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                *   `P-NEW-FY-BEG-DT-CC` (`PIC 9(02)`): Century Code for fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-YY` (`PIC 9(02)`): Year of fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-MM` (`PIC 9(02)`): Month of fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-DD` (`PIC 9(02)`): Day of fiscal year begin date.
            *   `P-NEW-REPORT-DATE`: Report Date.
                *   `P-NEW-REPORT-DT-CC` (`PIC 9(02)`): Century Code for report date.
                *   `P-NEW-REPORT-DT-YY` (`PIC 9(02)`): Year of report date.
                *   `P-NEW-REPORT-DT-MM` (`PIC 9(02)`): Month of report date.
                *   `P-NEW-REPORT-DT-DD` (`PIC 9(02)`): Day of report date.
            *   `P-NEW-TERMINATION-DATE`: Termination Date.
                *   `P-NEW-TERM-DT-CC` (`PIC 9(02)`): Century Code for termination date.
                *   `P-NEW-TERM-DT-YY` (`PIC 9(02)`): Year of termination date.
                *   `P-NEW-TERM-DT-MM` (`PIC 9(02)`): Month of termination date.
                *   `P-NEW-TERM-DT-DD` (`PIC 9(02)`): Day of termination date.
        *   `P-NEW-WAIVER-CODE` (`PIC X(01)`): Waiver Code.
            *   `P-NEW-WAIVER-STATE` (`VALUE 'Y'`):  Indicates if a waiver state.
        *   `P-NEW-INTER-NO` (`PIC 9(05)`): Intern Number.
        *   `P-NEW-PROVIDER-TYPE` (`PIC X(02)`): Provider Type.
        *   `P-NEW-CURRENT-CENSUS-DIV` (`PIC 9(01)`): Current Census Division.
        *   `P-NEW-CURRENT-DIV` (`PIC 9(01)`): Redefines the current census division.
        *   `P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data.
            *   `P-NEW-CHG-CODE-INDEX` (`PIC X`): Charge Code Index.
            *   `P-NEW-GEO-LOC-MSAX` (`PIC X(04)`): Geographic Location MSA.
            *   `P-NEW-GEO-LOC-MSA9` (`PIC 9(04)`): Redefines the geographic location MSA.
            *   `P-NEW-WAGE-INDEX-LOC-MSA` (`PIC X(04)`): Wage Index Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA` (`PIC X(04)`): Standard Amount Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9`: Redefines the standard amount location MSA.
                *   `P-NEW-RURAL-1ST`: Rural Data First.
                    *   `P-NEW-STAND-RURAL` (`PIC XX`): Standard Rural.
                        *   `P-NEW-STD-RURAL-CHECK` (`VALUE '  '`): Check for standard rural.
                    *   `P-NEW-RURAL-2ND` (`PIC XX`): Rural data second.
        *   `P-NEW-SOL-COM-DEP-HOSP-YR` (`PIC XX`): Sole Community Dep. Hospital Year.
        *   `P-NEW-LUGAR` (`PIC X`): Lugar.
        *   `P-NEW-TEMP-RELIEF-IND` (`PIC X`): Temporary Relief Indicator.
        *   `P-NEW-FED-PPS-BLEND-IND` (`PIC X`): Federal PPS Blend Indicator.
        *   `FILLER` (`PIC X(05)`): Filler space.
    *   `PROV-NEWREC-HOLD2`: Holds provider record information.
        *   `P-NEW-VARIABLES`: Variables for provider.
            *   `P-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`): Facility Specific Rate.
            *   `P-NEW-COLA` (`PIC 9(01)V9(03)`): Cost of Living Adjustment.
            *   `P-NEW-INTERN-RATIO` (`PIC 9(01)V9(04)`): Intern Ratio.
            *   `P-NEW-BED-SIZE` (`PIC 9(05)`): Bed Size.
            *   `P-NEW-OPER-CSTCHG-RATIO` (`PIC 9(01)V9(03)`): Operating Cost to Charge Ratio.
            *   `P-NEW-CMI` (`PIC 9(01)V9(04)`): CMI (Case Mix Index).
            *   `P-NEW-SSI-RATIO` (`PIC V9(04)`): SSI Ratio.
            *   `P-NEW-MEDICAID-RATIO` (`PIC V9(04)`): Medicaid Ratio.
            *   `P-NEW-PPS-BLEND-YR-IND` (`PIC 9(01)`): PPS Blend Year Indicator.
            *   `P-NEW-PRUF-UPDTE-FACTOR` (`PIC 9(01)V9(05)`): PRUF Update Factor.
            *   `P-NEW-DSH-PERCENT` (`PIC V9(04)`): DSH (Disproportionate Share Hospital) Percent.
            *   `P-NEW-FYE-DATE` (`PIC X(08)`): Fiscal Year End Date.
        *   `FILLER` (`PIC X(23)`): Filler space.
    *   `PROV-NEWREC-HOLD3`: Holds provider record information.
        *   `P-NEW-PASS-AMT-DATA`: Passed Amount Data.
            *   `P-NEW-PASS-AMT-CAPITAL` (`PIC 9(04)V99`): Passed Amount Capital.
            *   `P-NEW-PASS-AMT-DIR-MED-ED` (`PIC 9(04)V99`): Passed Amount Direct Medical Education.
            *   `P-NEW-PASS-AMT-ORGAN-ACQ` (`PIC 9(04)V99`): Passed Amount Organ Acquisition.
            *   `P-NEW-PASS-AMT-PLUS-MISC` (`PIC 9(04)V99`): Passed Amount Plus Misc.
        *   `P-NEW-CAPI-DATA`: Capital Data.
            *   `P-NEW-CAPI-PPS-PAY-CODE` (`PIC X`): Capital PPS Payment Code.
            *   `P-NEW-CAPI-HOSP-SPEC-RATE` (`PIC 9(04)V99`): Capital Hospital Specific Rate.
            *   `P-NEW-CAPI-OLD-HARM-RATE` (`PIC 9(04)V99`): Capital Old HARM Rate.
            *   `P-NEW-CAPI-NEW-HARM-RATIO` (`PIC 9(01)V9999`): Capital New HARM Ratio.
            *   `P-NEW-CAPI-CSTCHG-RATIO` (`PIC 9V999`): Capital Cost to Charge Ratio.
            *   `P-NEW-CAPI-NEW-HOSP` (`PIC X`): Capital New Hospital.
            *   `P-NEW-CAPI-IME` (`PIC 9V9999`): Capital IME (Indirect Medical Education).
            *   `P-NEW-CAPI-EXCEPTIONS` (`PIC 9(04)V99`): Capital Exceptions.
        *   `FILLER` (`PIC X(22)`): Filler space.

*   **`WAGE-NEW-INDEX-RECORD`**:  This structure likely holds wage index information.
    *   `W-MSA` (`PIC X(4)`): MSA (Metropolitan Statistical Area) code.
    *   `W-EFF-DATE` (`PIC X(8)`): Effective Date.
    *   `W-WAGE-INDEX1` (`PIC S9(02)V9(04)`): Wage Index 1.
    *   `W-WAGE-INDEX2` (`PIC S9(02)V9(04)`): Wage Index 2.
    *   `W-WAGE-INDEX3` (`PIC S9(02)V9(04)`): Wage Index 3.

### Program: LTCAL042

#### Files Accessed:

*   **None Explicitly Defined:** Similar to LTCAL032, no `SELECT` statements, but the program uses a `COPY` for `LTDRG031`.

#### WORKING-STORAGE SECTION Data Structures:

*   **`W-STORAGE-REF`**:
    *   `PIC X(46)`:  Used for storing a literal string identifying the program and its purpose.
    *   `VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'`:  Initializes the field with a descriptive string.

*   **`CAL-VERSION`**:
    *   `PIC X(05)`:  Used to store the version number of the calculation logic.
    *   `VALUE 'C04.2'`:  Initializes the field with the version string.

*   **`HOLD-PPS-COMPONENTS`**: (Identical to LTCAL032) This structure is used to hold intermediate calculation results and components.  It's likely used to store values needed during the PPS (Prospective Payment System) calculation.
    *   `H-LOS` (`PIC 9(03)`): Length of Stay.
    *   `H-REG-DAYS` (`PIC 9(03)`): Regular days.
    *   `H-TOTAL-DAYS` (`PIC 9(05)`): Total days.
    *   `H-SSOT` (`PIC 9(02)`):  Short Stay Outlier Threshold.
    *   `H-BLEND-RTC` (`PIC 9(02)`): Blend Return To Code.
    *   `H-BLEND-FAC` (`PIC 9(01)V9(01)`): Blend Facility Rate.
    *   `H-BLEND-PPS` (`PIC 9(01)V9(01)`): Blend PPS Rate.
    *   `H-SS-PAY-AMT` (`PIC 9(07)V9(02)`): Short Stay Payment Amount.
    *   `H-SS-COST` (`PIC 9(07)V9(02)`): Short Stay Cost.
    *   `H-LABOR-PORTION` (`PIC 9(07)V9(06)`): Labor Portion of the payment.
    *   `H-NONLABOR-PORTION` (`PIC 9(07)V9(06)`): Non-Labor Portion of the payment.
    *   `H-FIXED-LOSS-AMT` (`PIC 9(07)V9(02)`): Fixed Loss Amount.
    *   `H-NEW-FAC-SPEC-RATE` (`PIC 9(05)V9(02)`): New facility specific rate.
    *   `H-LOS-RATIO` (`PIC 9(01)V9(05)`):  Length of Stay Ratio.

*   **Data structures defined by COPY LTDRG031:** The program copies the contents of `LTDRG031`. This file contains the DRG table.

*   **`PPS-DATA-ALL`**: This is a large structure that likely holds all the data returned to the calling program. (Identical to LTCAL032)
    *   `PPS-RTC` (`PIC 9(02)`): Return Code, indicating the payment status.
    *   `PPS-CHRG-THRESHOLD` (`PIC 9(07)V9(02)`): Charge Threshold.
    *   `PPS-DATA`: Contains various PPS related data.
        *   `PPS-MSA` (`PIC X(04)`): MSA (Metropolitan Statistical Area) code.
        *   `PPS-WAGE-INDEX` (`PIC 9(02)V9(04)`): Wage Index.
        *   `PPS-AVG-LOS` (`PIC 9(02)V9(01)`): Average Length of Stay.
        *   `PPS-RELATIVE-WGT` (`PIC 9(01)V9(04)`): Relative Weight.
        *   `PPS-OUTLIER-PAY-AMT` (`PIC 9(07)V9(02)`): Outlier Payment Amount.
        *   `PPS-LOS` (`PIC 9(03)`): Length of Stay.
        *   `PPS-DRG-ADJ-PAY-AMT` (`PIC 9(07)V9(02)`): DRG Adjusted Payment Amount.
        *   `PPS-FED-PAY-AMT` (`PIC 9(07)V9(02)`): Federal Payment Amount.
        *   `PPS-FINAL-PAY-AMT` (`PIC 9(07)V9(02)`): Final Payment Amount.
        *   `PPS-FAC-COSTS` (`PIC 9(07)V9(02)`): Facility Costs.
        *   `PPS-NEW-FAC-SPEC-RATE` (`PIC 9(07)V9(02)`): New Facility Specific Rate.
        *   `PPS-OUTLIER-THRESHOLD` (`PIC 9(07)V9(02)`): Outlier Threshold.
        *   `PPS-SUBM-DRG-CODE` (`PIC X(03)`): Submitted DRG Code.
        *   `PPS-CALC-VERS-CD` (`PIC X(05)`): Calculation Version Code.
        *   `PPS-REG-DAYS-USED` (`PIC 9(03)`): Regular Days Used.
        *   `PPS-LTR-DAYS-USED` (`PIC 9(03)`): Lifetime Reserve Days Used.
        *   `PPS-BLEND-YEAR` (`PIC 9(01)`): Blend Year.
        *   `PPS-COLA` (`PIC 9(01)V9(03)`): Cost of Living Adjustment.
        *   `FILLER` (`PIC X(04)`): Filler space.
    *   `PPS-OTHER-DATA`: Contains other PPS data.
        *   `PPS-NAT-LABOR-PCT` (`PIC 9(01)V9(05)`): National Labor Percentage.
        *   `PPS-NAT-NONLABOR-PCT` (`PIC 9(01)V9(05)`): National Non-Labor Percentage.
        *   `PPS-STD-FED-RATE` (`PIC 9(05)V9(02)`): Standard Federal Rate.
        *   `PPS-BDGT-NEUT-RATE` (`PIC 9(01)V9(03)`): Budget Neutrality Rate.
        *   `FILLER` (`PIC X(20)`): Filler space.
    *   `PPS-PC-DATA`: Contains PPS patient care data.
        *   `PPS-COT-IND` (`PIC X(01)`): Cost Outlier Indicator.
        *   `FILLER` (`PIC X(20)`): Filler space.

*   **`PRICER-OPT-VERS-SW`**: (Identical to LTCAL032)
    *   `PRICER-OPTION-SW` (`PIC X(01)`):  A switch that determines which version of the pricer is used.
        *   `ALL-TABLES-PASSED` (`VALUE 'A'`):  Indicates all tables are passed.
        *   `PROV-RECORD-PASSED` (`VALUE 'P'`): Indicates Provider Record is passed.
    *   `PPS-VERSIONS`:
        *   `PPDRV-VERSION` (`PIC X(05)`): Version of the PPDRV program.

#### LINKAGE SECTION Data Structures:

*   **`BILL-NEW-DATA`**:  This is the input data structure passed to the program, likely representing a patient's bill. (Identical to LTCAL032)
    *   `B-NPI10`: NPI (National Provider Identifier)
        *   `B-NPI8` (`PIC X(08)`): The 8-character NPI.
        *   `B-NPI-FILLER` (`PIC X(02)`): Filler for NPI.
    *   `B-PROVIDER-NO` (`PIC X(06)`): Provider Number.
    *   `B-PATIENT-STATUS` (`PIC X(02)`): Patient Status.
    *   `B-DRG-CODE` (`PIC X(03)`): DRG (Diagnosis Related Group) Code.
    *   `B-LOS` (`PIC 9(03)`): Length of Stay.
    *   `B-COV-DAYS` (`PIC 9(03)`): Covered Days.
    *   `B-LTR-DAYS` (`PIC 9(02)`): Lifetime Reserve Days.
    *   `B-DISCHARGE-DATE`: Discharge Date.
        *   `B-DISCHG-CC` (`PIC 9(02)`): Century Code for discharge date.
        *   `B-DISCHG-YY` (`PIC 9(02)`): Year of discharge date.
        *   `B-DISCHG-MM` (`PIC 9(02)`): Month of discharge date.
        *   `B-DISCHG-DD` (`PIC 9(02)`): Day of discharge date.
    *   `B-COV-CHARGES` (`PIC 9(07)V9(02)`): Covered Charges.
    *   `B-SPEC-PAY-IND` (`PIC X(01)`): Special Payment Indicator.
    *   `FILLER` (`PIC X(13)`): Filler space.

*   **`PPS-DATA-ALL`**: This is a large structure that likely holds all the data returned to the calling program. (Identical to the one in Working Storage).

*   **`PRICER-OPT-VERS-SW`**: (Identical to the one in Working Storage)

*   **`PROV-NEW-HOLD`**: This structure likely holds provider-specific information. (Identical to LTCAL032)
    *   `PROV-NEWREC-HOLD1`: Holds provider record information.
        *   `P-NEW-NPI10`: NPI (National Provider Identifier)
            *   `P-NEW-NPI8` (`PIC X(08)`): The 8-character NPI.
            *   `P-NEW-NPI-FILLER` (`PIC X(02)`): Filler for NPI.
        *   `P-NEW-PROVIDER-NO`: Provider Number.
            *   `P-NEW-STATE` (`PIC 9(02)`): State.
            *   `FILLER` (`PIC X(04)`): Filler space.
        *   `P-NEW-DATE-DATA`: Date Information.
            *   `P-NEW-EFF-DATE`: Effective Date.
                *   `P-NEW-EFF-DT-CC` (`PIC 9(02)`): Century Code for effective date.
                *   `P-NEW-EFF-DT-YY` (`PIC 9(02)`): Year of effective date.
                *   `P-NEW-EFF-DT-MM` (`PIC 9(02)`): Month of effective date.
                *   `P-NEW-EFF-DT-DD` (`PIC 9(02)`): Day of effective date.
            *   `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                *   `P-NEW-FY-BEG-DT-CC` (`PIC 9(02)`): Century Code for fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-YY` (`PIC 9(02)`): Year of fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-MM` (`PIC 9(02)`): Month of fiscal year begin date.
                *   `P-NEW-FY-BEG-DT-DD` (`PIC 9(02)`): Day of fiscal year begin date.
            *   `P-NEW-REPORT-DATE`: Report Date.
                *   `P-NEW-REPORT-DT-CC` (`PIC 9(02)`): Century Code for report date.
                *   `P-NEW-REPORT-DT-YY` (`PIC 9(02)`): Year of report date.
                *   `P-NEW-REPORT-DT-MM` (`PIC 9(02)`): Month of report date.
                *   `P-NEW-REPORT-DT-DD` (`PIC 9(02)`): Day of report date.
            *   `P-NEW-TERMINATION-DATE`: Termination Date.
                *   `P-NEW-TERM-DT-CC` (`PIC 9(02)`): Century Code for termination date.
                *   `P-NEW-TERM-DT-YY` (`PIC 9(02)`): Year of termination date.
                *   `P-NEW-TERM-DT-MM` (`PIC 9(02)`): Month of termination date.
                *   `P-NEW-TERM-DT-DD` (`PIC 9(02)`): Day of termination date.
        *   `P-NEW-WAIVER-CODE` (`PIC X(01)`): Waiver Code.
            *   `P-NEW-WAIVER-STATE` (`VALUE 'Y'`):  Indicates if a waiver state.
        *   `P-NEW-INTER-NO` (`PIC 9(05)`): Intern Number.
        *   `P-NEW-PROVIDER-TYPE` (`PIC X(02)`): Provider Type.
        *   `P-NEW-CURRENT-CENSUS-DIV` (`PIC 9(01)`): Current Census Division.
        *   `P-NEW-CURRENT-DIV` (`PIC 9(01)`): Redefines the current census division.
        *   `P-NEW-MSA-DATA`: MSA (Metropolitan Statistical Area) Data.
            *   `P-NEW-CHG-CODE-INDEX` (`PIC X`): Charge Code Index.
            *   `P-NEW-GEO-LOC-MSAX` (`PIC X(04)`): Geographic Location MSA.
            *   `P-NEW-GEO-LOC-MSA9` (`PIC 9(04)`): Redefines the geographic location MSA.
            *   `P-NEW-WAGE-INDEX-LOC-MSA` (`PIC X(04)`): Wage Index Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA` (`PIC X(04)`): Standard Amount Location MSA.
            *   `P-NEW-STAND-AMT-LOC-MSA9`: Redefines the standard amount location MSA.
                *   `P-NEW-RURAL-1ST`: Rural Data First.
                    *   `P-NEW-STAND-RURAL` (`PIC XX`): Standard Rural.
                        *   `P-NEW-STD-RURAL-CHECK` (`VALUE '  '`): Check for standard rural.
                    *   `P-NEW-RURAL-2ND` (`PIC XX`): Rural data second.
        *   `P-NEW-SOL-COM-DEP-HOSP-YR` (`PIC XX`