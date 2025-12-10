## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access is evident in the provided code. However, the program uses a `COPY` statement for `LTDRG031`, which likely includes data definitions related to DRG codes and associated values.

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   **`W-STORAGE-REF`**: (PIC X(46)) -  Stores a descriptive string identifying the program and its purpose.
    *   **`CAL-VERSION`**: (PIC X(05)) - Stores the version number of the calculation program ('C03.2').
    *   **`HOLD-PPS-COMPONENTS`**: This group of data items is used to store calculated components related to the Prospective Payment System (PPS).
        *   **`H-LOS`**: (PIC 9(03)) - Length of Stay.
        *   **`H-REG-DAYS`**: (PIC 9(03)) - Regular Days.
        *   **`H-TOTAL-DAYS`**: (PIC 9(05)) - Total Days.
        *   **`H-SSOT`**: (PIC 9(02)) -  Likely represents a threshold for Short Stay Outlier.
        *   **`H-BLEND-RTC`**: (PIC 9(02)) - Return Code for Blend.
        *   **`H-BLEND-FAC`**: (PIC 9(01)V9(01)) - Blend Factor - Facility.
        *   **`H-BLEND-PPS`**: (PIC 9(01)V9(01)) - Blend Factor - PPS.
        *   **`H-SS-PAY-AMT`**: (PIC 9(07)V9(02)) - Short Stay Payment Amount.
        *   **`H-SS-COST`**: (PIC 9(07)V9(02)) - Short Stay Cost.
        *   **`H-LABOR-PORTION`**: (PIC 9(07)V9(06)) - Labor Portion of the payment.
        *   **`H-NONLABOR-PORTION`**: (PIC 9(07)V9(06)) - Non-Labor Portion of the payment.
        *   **`H-FIXED-LOSS-AMT`**: (PIC 9(07)V9(02)) - Fixed Loss Amount, used in outlier calculations.
        *   **`H-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - New Facility Specific Rate.

*   **Data Structures in LINKAGE SECTION:**
    *   **`BILL-NEW-DATA`**: This is the primary data structure passed *into* the program, representing the billing information.
        *   **`B-NPI10`**:  National Provider Identifier (NPI) - 10 digits
            *   **`B-NPI8`**: (PIC X(08)) - First 8 digits of NPI.
            *   **`B-NPI-FILLER`**: (PIC X(02)) - Filler for the last 2 digits of NPI.
        *   **`B-PROVIDER-NO`**: (PIC X(06)) - Provider Number.
        *   **`B-PATIENT-STATUS`**: (PIC X(02)) - Patient Status.
        *   **`B-DRG-CODE`**: (PIC X(03)) - DRG Code (Diagnosis Related Group).
        *   **`B-LOS`**: (PIC 9(03)) - Length of Stay.
        *   **`B-COV-DAYS`**: (PIC 9(03)) - Covered Days.
        *   **`B-LTR-DAYS`**: (PIC 9(02)) - Lifetime Reserve Days.
        *   **`B-DISCHARGE-DATE`**: Discharge Date.
            *   **`B-DISCHG-CC`**: (PIC 9(02)) - Century of Discharge Date.
            *   **`B-DISCHG-YY`**: (PIC 9(02)) - Year of Discharge Date.
            *   **`B-DISCHG-MM`**: (PIC 9(02)) - Month of Discharge Date.
            *   **`B-DISCHG-DD`**: (PIC 9(02)) - Day of Discharge Date.
        *   **`B-COV-CHARGES`**: (PIC 9(07)V9(02)) - Covered Charges.
        *   **`B-SPEC-PAY-IND`**: (PIC X(01)) - Special Payment Indicator.
        *   **`FILLER`**: (PIC X(13)) - Unused.
    *   **`PPS-DATA-ALL`**:  This is the primary data structure passed *out* of the program, containing the calculated PPS data.
        *   **`PPS-RTC`**: (PIC 9(02)) - Return Code.
        *   **`PPS-CHRG-THRESHOLD`**: (PIC 9(07)V9(02)) - Charge Threshold.
        *   **`PPS-DATA`**: PPS Data
            *   **`PPS-MSA`**: (PIC X(04)) - Metropolitan Statistical Area.
            *   **`PPS-WAGE-INDEX`**: (PIC 9(02)V9(04)) - Wage Index.
            *   **`PPS-AVG-LOS`**: (PIC 9(02)V9(01)) - Average Length of Stay.
            *   **`PPS-RELATIVE-WGT`**: (PIC 9(01)V9(04)) - Relative Weight.
            *   **`PPS-OUTLIER-PAY-AMT`**: (PIC 9(07)V9(02)) - Outlier Payment Amount.
            *   **`PPS-LOS`**: (PIC 9(03)) - Length of Stay.
            *   **`PPS-DRG-ADJ-PAY-AMT`**: (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount.
            *   **`PPS-FED-PAY-AMT`**: (PIC 9(07)V9(02)) - Federal Payment Amount.
            *   **`PPS-FINAL-PAY-AMT`**: (PIC 9(07)V9(02)) - Final Payment Amount.
            *   **`PPS-FAC-COSTS`**: (PIC 9(07)V9(02)) - Facility Costs.
            *   **`PPS-NEW-FAC-SPEC-RATE`**: (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   **`PPS-OUTLIER-THRESHOLD`**: (PIC 9(07)V9(02)) - Outlier Threshold.
            *   **`PPS-SUBM-DRG-CODE`**: (PIC X(03)) - Submitted DRG Code.
            *   **`PPS-CALC-VERS-CD`**: (PIC X(05)) - Calculation Version Code.
            *   **`PPS-REG-DAYS-USED`**: (PIC 9(03)) - Regular Days Used.
            *   **`PPS-LTR-DAYS-USED`**: (PIC 9(03)) - Lifetime Reserve Days Used.
            *   **`PPS-BLEND-YEAR`**: (PIC 9(01)) - Blend Year.
            *   **`PPS-COLA`**: (PIC 9(01)V9(03)) - Cost of Living Adjustment.
            *   **`FILLER`**: (PIC X(04)) - Unused.
        *   **`PPS-OTHER-DATA`**: Other PPS Data
            *   **`PPS-NAT-LABOR-PCT`**: (PIC 9(01)V9(05)) - National Labor Percentage.
            *   **`PPS-NAT-NONLABOR-PCT`**: (PIC 9(01)V9(05)) - National Non-Labor Percentage.
            *   **`PPS-STD-FED-RATE`**: (PIC 9(05)V9(02)) - Standard Federal Rate.
            *   **`PPS-BDGT-NEUT-RATE`**: (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   **`FILLER`**: (PIC X(20)) - Unused.
        *   **`PPS-PC-DATA`**: PPS Payment Component Data
            *   **`PPS-COT-IND`**: (PIC X(01)) - Cost Outlier Indicator.
            *   **`FILLER`**: (PIC X(20)) - Unused.
    *   **`PRICER-OPT-VERS-SW`**:  Pricer Option Version Switch.
        *   **`PRICER-OPTION-SW`**: (PIC X(01)) - Pricer Option Switch.
        *   **`PPS-VERSIONS`**:  PPS Versions
            *   **`PPDRV-VERSION`**: (PIC X(05)) - Version of the PPDRV program.
    *   **`PROV-NEW-HOLD`**: Provider Record information
        *   **`PROV-NEWREC-HOLD1`**: Provider Record Hold 1
            *   **`P-NEW-NPI10`**: NPI
                *   **`P-NEW-NPI8`**: (PIC X(08)) - First 8 digits of NPI.
                *   **`P-NEW-NPI-FILLER`**: (PIC X(02)) - Filler for the last 2 digits of NPI.
            *   **`P-NEW-PROVIDER-NO`**: Provider Number
                *   **`P-NEW-STATE`**: (PIC 9(02)) - State.
                *   **`FILLER`**: (PIC X(04)) - Unused.
            *   **`P-NEW-DATE-DATA`**: Date Data
                *   **`P-NEW-EFF-DATE`**: Effective Date
                    *   **`P-NEW-EFF-DT-CC`**: (PIC 9(02)) - Effective Date - Century
                    *   **`P-NEW-EFF-DT-YY`**: (PIC 9(02)) - Effective Date - Year
                    *   **`P-NEW-EFF-DT-MM`**: (PIC 9(02)) - Effective Date - Month
                    *   **`P-NEW-EFF-DT-DD`**: (PIC 9(02)) - Effective Date - Day
                *   **`P-NEW-FY-BEGIN-DATE`**: Fiscal Year Begin Date
                    *   **`P-NEW-FY-BEG-DT-CC`**: (PIC 9(02)) - Fiscal Year Begin Date - Century
                    *   **`P-NEW-FY-BEG-DT-YY`**: (PIC 9(02)) - Fiscal Year Begin Date - Year
                    *   **`P-NEW-FY-BEG-DT-MM`**: (PIC 9(02)) - Fiscal Year Begin Date - Month
                    *   **`P-NEW-FY-BEG-DT-DD`**: (PIC 9(02)) - Fiscal Year Begin Date - Day
                *   **`P-NEW-REPORT-DATE`**: Report Date
                    *   **`P-NEW-REPORT-DT-CC`**: (PIC 9(02)) - Report Date - Century
                    *   **`P-NEW-REPORT-DT-YY`**: (PIC 9(02)) - Report Date - Year
                    *   **`P-NEW-REPORT-DT-MM`**: (PIC 9(02)) - Report Date - Month
                    *   **`P-NEW-REPORT-DT-DD`**: (PIC 9(02)) - Report Date - Day
                *   **`P-NEW-TERMINATION-DATE`**: Termination Date
                    *   **`P-NEW-TERM-DT-CC`**: (PIC 9(02)) - Termination Date - Century
                    *   **`P-NEW-TERM-DT-YY`**: (PIC 9(02)) - Termination Date - Year
                    *   **`P-NEW-TERM-DT-MM`**: (PIC 9(02)) - Termination Date - Month
                    *   **`P-NEW-TERM-DT-DD`**: (PIC 9(02)) - Termination Date - Day
            *   **`P-NEW-WAIVER-CODE`**: (PIC X(01)) - Waiver Code.
            *   **`P-NEW-INTER-NO`**: (PIC 9(05)) - Internal Number.
            *   **`P-NEW-PROVIDER-TYPE`**: (PIC X(02)) - Provider Type.
            *   **`P-NEW-CURRENT-CENSUS-DIV`**: (PIC 9(01)) - Current Census Division.
            *   **`P-NEW-MSA-DATA`**: MSA Data
                *   **`P-NEW-CHG-CODE-INDEX`**: (PIC X) - Charge Code Index.
                *   **`P-NEW-GEO-LOC-MSAX`**: (PIC X(04)) - Geographic Location MSA.
                *   **`P-NEW-WAGE-INDEX-LOC-MSA`**: (PIC X(04)) - Wage Index Location MSA.
                *   **`P-NEW-STAND-AMT-LOC-MSA`**: (PIC X(04)) - Standard Amount Location MSA.
                *   **`P-NEW-SOL-COM-DEP-HOSP-YR`**: (PIC XX) - Sol Com Dep Hosp Year.
                *   **`P-NEW-LUGAR`**: (PIC X) - Lugar.
                *   **`P-NEW-TEMP-RELIEF-IND`**: (PIC X) - Temporary Relief Indicator.
                *   **`P-NEW-FED-PPS-BLEND-IND`**: (PIC X) - Federal PPS Blend Indicator.
                *   **`FILLER`**: (PIC X(05)) - Unused.
        *   **`PROV-NEWREC-HOLD2`**: Provider Record Hold 2
            *   **`P-NEW-VARIABLES`**:  Variables
                *   **`P-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - Facility Specific Rate.
                *   **`P-NEW-COLA`**: (PIC 9(01)V9(03)) - Cost of Living Adjustment.
                *   **`P-NEW-INTERN-RATIO`**: (PIC 9(01)V9(04)) - Intern Ratio.
                *   **`P-NEW-BED-SIZE`**: (PIC 9(05)) - Bed Size.
                *   **`P-NEW-OPER-CSTCHG-RATIO`**: (PIC 9(01)V9(03)) - Operating Cost to Charge Ratio.
                *   **`P-NEW-CMI`**: (PIC 9(01)V9(04)) - CMI.
                *   **`P-NEW-SSI-RATIO`**: (PIC V9(04)) - SSI Ratio.
                *   **`P-NEW-MEDICAID-RATIO`**: (PIC V9(04)) - Medicaid Ratio.
                *   **`P-NEW-PPS-BLEND-YR-IND`**: (PIC 9(01)) - PPS Blend Year Indicator.
                *   **`P-NEW-PRUF-UPDTE-FACTOR`**: (PIC 9(01)V9(05)) - PRUF Update Factor.
                *   **`P-NEW-DSH-PERCENT`**: (PIC V9(04)) - DSH Percentage.
                *   **`P-NEW-FYE-DATE`**: (PIC X(08)) - Fiscal Year End Date.
            *   **`FILLER`**: (PIC X(23)) - Unused.
        *   **`PROV-NEWREC-HOLD3`**: Provider Record Hold 3
            *   **`P-NEW-PASS-AMT-DATA`**:  Pass Through Amount Data
                *   **`P-NEW-PASS-AMT-CAPITAL`**: (PIC 9(04)V99) - Capital Pass Through Amount.
                *   **`P-NEW-PASS-AMT-DIR-MED-ED`**: (PIC 9(04)V99) - Direct Medical Education Pass Through Amount.
                *   **`P-NEW-PASS-AMT-ORGAN-ACQ`**: (PIC 9(04)V99) - Organ Acquisition Pass Through Amount.
                *   **`P-NEW-PASS-AMT-PLUS-MISC`**: (PIC 9(04)V99) - Plus Misc Pass Through Amount.
            *   **`P-NEW-CAPI-DATA`**: Capital Data
                *   **`P-NEW-CAPI-PPS-PAY-CODE`**: (PIC X) - Capital PPS Payment Code.
                *   **`P-NEW-CAPI-HOSP-SPEC-RATE`**: (PIC 9(04)V99) - Hospital Specific Rate.
                *   **`P-NEW-CAPI-OLD-HARM-RATE`**: (PIC 9(04)V99) - Old Harm Rate.
                *   **`P-NEW-CAPI-NEW-HARM-RATIO`**: (PIC 9(01)V9999) - New Harm Ratio.
                *   **`P-NEW-CAPI-CSTCHG-RATIO`**: (PIC 9V999) - Cost to Charge Ratio.
                *   **`P-NEW-CAPI-NEW-HOSP`**: (PIC X) - New Hospital.
                *   **`P-NEW-CAPI-IME`**: (PIC 9V9999) - IME.
                *   **`P-NEW-CAPI-EXCEPTIONS`**: (PIC 9(04)V99) - Exceptions.
            *   **`FILLER`**: (PIC X(22)) - Unused.
    *   **`WAGE-NEW-INDEX-RECORD`**: Wage Index Record.
        *   **`W-MSA`**: (PIC X(4)) - MSA.
        *   **`W-EFF-DATE`**: (PIC X(8)) - Effective Date.
        *   **`W-WAGE-INDEX1`**: (PIC S9(02)V9(04)) - Wage Index 1.
        *   **`W-WAGE-INDEX2`**: (PIC S9(02)V9(04)) - Wage Index 2.
        *   **`W-WAGE-INDEX3`**: (PIC S9(02)V9(04)) - Wage Index 3.

*   **Procedure Division:** The Procedure Division contains the logic for processing the billing data, calculating payments, and determining outlier amounts.  It includes sections for initialization, data validation, DRG code lookup, assembling PPS variables, payment calculation, outlier calculation, and blending.

---

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access is evident in the provided code.  It also uses a `COPY` statement for `LTDRG031`.

*   **Data Structures in WORKING-STORAGE SECTION:**
    *   **`W-STORAGE-REF`**: (PIC X(46)) - Stores a descriptive string identifying the program and its purpose.
    *   **`CAL-VERSION`**: (PIC X(05)) - Stores the version number of the calculation program ('C04.2').
    *   **`HOLD-PPS-COMPONENTS`**: This group of data items is used to store calculated components related to the Prospective Payment System (PPS).
        *   **`H-LOS`**: (PIC 9(03)) - Length of Stay.
        *   **`H-REG-DAYS`**: (PIC 9(03)) - Regular Days.
        *   **`H-TOTAL-DAYS`**: (PIC 9(05)) - Total Days.
        *   **`H-SSOT`**: (PIC 9(02)) -  Likely represents a threshold for Short Stay Outlier.
        *   **`H-BLEND-RTC`**: (PIC 9(02)) - Return Code for Blend.
        *   **`H-BLEND-FAC`**: (PIC 9(01)V9(01)) - Blend Factor - Facility.
        *   **`H-BLEND-PPS`**: (PIC 9(01)V9(01)) - Blend Factor - PPS.
        *   **`H-SS-PAY-AMT`**: (PIC 9(07)V9(02)) - Short Stay Payment Amount.
        *   **`H-SS-COST`**: (PIC 9(07)V9(02)) - Short Stay Cost.
        *   **`H-LABOR-PORTION`**: (PIC 9(07)V9(06)) - Labor Portion of the payment.
        *   **`H-NONLABOR-PORTION`**: (PIC 9(07)V9(06)) - Non-Labor Portion of the payment.
        *   **`H-FIXED-LOSS-AMT`**: (PIC 9(07)V9(02)) - Fixed Loss Amount, used in outlier calculations.
        *   **`H-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - New Facility Specific Rate.
        *   **`H-LOS-RATIO`**: (PIC 9(01)V9(05)) - Length of Stay Ratio.

*   **Data Structures in LINKAGE SECTION:**
    *   **`BILL-NEW-DATA`**: This is the primary data structure passed *into* the program, representing the billing information.
        *   **`B-NPI10`**:  National Provider Identifier (NPI) - 10 digits
            *   **`B-NPI8`**: (PIC X(08)) - First 8 digits of NPI.
            *   **`B-NPI-FILLER`**: (PIC X(02)) - Filler for the last 2 digits of NPI.
        *   **`B-PROVIDER-NO`**: (PIC X(06)) - Provider Number.
        *   **`B-PATIENT-STATUS`**: (PIC X(02)) - Patient Status.
        *   **`B-DRG-CODE`**: (PIC X(03)) - DRG Code (Diagnosis Related Group).
        *   **`B-LOS`**: (PIC 9(03)) - Length of Stay.
        *   **`B-COV-DAYS`**: (PIC 9(03)) - Covered Days.
        *   **`B-LTR-DAYS`**: (PIC 9(02)) - Lifetime Reserve Days.
        *   **`B-DISCHARGE-DATE`**: Discharge Date.
            *   **`B-DISCHG-CC`**: (PIC 9(02)) - Century of Discharge Date.
            *   **`B-DISCHG-YY`**: (PIC 9(02)) - Year of Discharge Date.
            *   **`B-DISCHG-MM`**: (PIC 9(02)) - Month of Discharge Date.
            *   **`B-DISCHG-DD`**: (PIC 9(02)) - Day of Discharge Date.
        *   **`B-COV-CHARGES`**: (PIC 9(07)V9(02)) - Covered Charges.
        *   **`B-SPEC-PAY-IND`**: (PIC X(01)) - Special Payment Indicator.
        *   **`FILLER`**: (PIC X(13)) - Unused.
    *   **`PPS-DATA-ALL`**:  This is the primary data structure passed *out* of the program, containing the calculated PPS data.
        *   **`PPS-RTC`**: (PIC 9(02)) - Return Code.
        *   **`PPS-CHRG-THRESHOLD`**: (PIC 9(07)V9(02)) - Charge Threshold.
        *   **`PPS-DATA`**: PPS Data
            *   **`PPS-MSA`**: (PIC X(04)) - Metropolitan Statistical Area.
            *   **`PPS-WAGE-INDEX`**: (PIC 9(02)V9(04)) - Wage Index.
            *   **`PPS-AVG-LOS`**: (PIC 9(02)V9(01)) - Average Length of Stay.
            *   **`PPS-RELATIVE-WGT`**: (PIC 9(01)V9(04)) - Relative Weight.
            *   **`PPS-OUTLIER-PAY-AMT`**: (PIC 9(07)V9(02)) - Outlier Payment Amount.
            *   **`PPS-LOS`**: (PIC 9(03)) - Length of Stay.
            *   **`PPS-DRG-ADJ-PAY-AMT`**: (PIC 9(07)V9(02)) - DRG Adjusted Payment Amount.
            *   **`PPS-FED-PAY-AMT`**: (PIC 9(07)V9(02)) - Federal Payment Amount.
            *   **`PPS-FINAL-PAY-AMT`**: (PIC 9(07)V9(02)) - Final Payment Amount.
            *   **`PPS-FAC-COSTS`**: (PIC 9(07)V9(02)) - Facility Costs.
            *   **`PPS-NEW-FAC-SPEC-RATE`**: (PIC 9(07)V9(02)) - New Facility Specific Rate.
            *   **`PPS-OUTLIER-THRESHOLD`**: (PIC 9(07)V9(02)) - Outlier Threshold.
            *   **`PPS-SUBM-DRG-CODE`**: (PIC X(03)) - Submitted DRG Code.
            *   **`PPS-CALC-VERS-CD`**: (PIC X(05)) - Calculation Version Code.
            *   **`PPS-REG-DAYS-USED`**: (PIC 9(03)) - Regular Days Used.
            *   **`PPS-LTR-DAYS-USED`**: (PIC 9(03)) - Lifetime Reserve Days Used.
            *   **`PPS-BLEND-YEAR`**: (PIC 9(01)) - Blend Year.
            *   **`PPS-COLA`**: (PIC 9(01)V9(03)) - Cost of Living Adjustment.
            *   **`FILLER`**: (PIC X(04)) - Unused.
        *   **`PPS-OTHER-DATA`**: Other PPS Data
            *   **`PPS-NAT-LABOR-PCT`**: (PIC 9(01)V9(05)) - National Labor Percentage.
            *   **`PPS-NAT-NONLABOR-PCT`**: (PIC 9(01)V9(05)) - National Non-Labor Percentage.
            *   **`PPS-STD-FED-RATE`**: (PIC 9(05)V9(02)) - Standard Federal Rate.
            *   **`PPS-BDGT-NEUT-RATE`**: (PIC 9(01)V9(03)) - Budget Neutrality Rate.
            *   **`FILLER`**: (PIC X(20)) - Unused.
        *   **`PPS-PC-DATA`**: PPS Payment Component Data
            *   **`PPS-COT-IND`**: (PIC X(01)) - Cost Outlier Indicator.
            *   **`FILLER`**: (PIC X(20)) - Unused.
    *   **`PRICER-OPT-VERS-SW`**:  Pricer Option Version Switch.
        *   **`PRICER-OPTION-SW`**: (PIC X(01)) - Pricer Option Switch.
        *   **`PPS-VERSIONS`**:  PPS Versions
            *   **`PPDRV-VERSION`**: (PIC X(05)) - Version of the PPDRV program.
    *   **`PROV-NEW-HOLD`**: Provider Record information
        *   **`PROV-NEWREC-HOLD1`**: Provider Record Hold 1
            *   **`P-NEW-NPI10`**: NPI
                *   **`P-NEW-NPI8`**: (PIC X(08)) - First 8 digits of NPI.
                *   **`P-NEW-NPI-FILLER`**: (PIC X(02)) - Filler for the last 2 digits of NPI.
            *   **`P-NEW-PROVIDER-NO`**: Provider Number
                *   **`P-NEW-STATE`**: (PIC 9(02)) - State.
                *   **`FILLER`**: (PIC X(04)) - Unused.
            *   **`P-NEW-DATE-DATA`**: Date Data
                *   **`P-NEW-EFF-DATE`**: Effective Date
                    *   **`P-NEW-EFF-DT-CC`**: (PIC 9(02)) - Effective Date - Century
                    *   **`P-NEW-EFF-DT-YY`**: (PIC 9(02)) - Effective Date - Year
                    *   **`P-NEW-EFF-DT-MM`**: (PIC 9(02)) - Effective Date - Month
                    *   **`P-NEW-EFF-DT-DD`**: (PIC 9(02)) - Effective Date - Day
                *   **`P-NEW-FY-BEGIN-DATE`**: Fiscal Year Begin Date
                    *   **`P-NEW-FY-BEG-DT-CC`**: (PIC 9(02)) - Fiscal Year Begin Date - Century
                    *   **`P-NEW-FY-BEG-DT-YY`**: (PIC 9(02)) - Fiscal Year Begin Date - Year
                    *   **`P-NEW-FY-BEG-DT-MM`**: (PIC 9(02)) - Fiscal Year Begin Date - Month
                    *   **`P-NEW-FY-BEG-DT-DD`**: (PIC 9(02)) - Fiscal Year Begin Date - Day
                *   **`P-NEW-REPORT-DATE`**: Report Date
                    *   **`P-NEW-REPORT-DT-CC`**: (PIC 9(02)) - Report Date - Century
                    *   **`P-NEW-REPORT-DT-YY`**: (PIC 9(02)) - Report Date - Year
                    *   **`P-NEW-REPORT-DT-MM`**: (PIC 9(02)) - Report Date - Month
                    *   **`P-NEW-REPORT-DT-DD`**: (PIC 9(02)) - Report Date - Day
                *   **`P-NEW-TERMINATION-DATE`**: Termination Date
                    *   **`P-NEW-TERM-DT-CC`**: (PIC 9(02)) - Termination Date - Century
                    *   **`P-NEW-TERM-DT-YY`**: (PIC 9(02)) - Termination Date - Year
                    *   **`P-NEW-TERM-DT-MM`**: (PIC 9(02)) - Termination Date - Month
                    *   **`P-NEW-TERM-DT-DD`**: (PIC 9(02)) - Termination Date - Day
            *   **`P-NEW-WAIVER-CODE`**: (PIC X(01)) - Waiver Code.
            *   **`P-NEW-INTER-NO`**: (PIC 9(05)) - Internal Number.
            *   **`P-NEW-PROVIDER-TYPE`**: (PIC X(02)) - Provider Type.
            *   **`P-NEW-CURRENT-CENSUS-DIV`**: (PIC 9(01)) - Current Census Division.
            *   **`P-NEW-MSA-DATA`**: MSA Data
                *   **`P-NEW-CHG-CODE-INDEX`**: (PIC X) - Charge Code Index.
                *   **`P-NEW-GEO-LOC-MSAX`**: (PIC X(04)) - Geographic Location MSA.
                *   **`P-NEW-WAGE-INDEX-LOC-MSA`**: (PIC X(04)) - Wage Index Location MSA.
                *   **`P-NEW-STAND-AMT-LOC-MSA`**: (PIC X(04)) - Standard Amount Location MSA.
                *   **`P-NEW-SOL-COM-DEP-HOSP-YR`**: (PIC XX) - Sol Com Dep Hosp Year.
                *   **`P-NEW-LUGAR`**: (PIC X) - Lugar.
                *   **`P-NEW-TEMP-RELIEF-IND`**: (PIC X) - Temporary Relief Indicator.
                *   **`P-NEW-FED-PPS-BLEND-IND`**: (PIC X) - Federal PPS Blend Indicator.
                *   **`FILLER`**: (PIC X(05)) - Unused.
        *   **`PROV-NEWREC-HOLD2`**: Provider Record Hold 2
            *   **`P-NEW-VARIABLES`**:  Variables
                *   **`P-NEW-FAC-SPEC-RATE`**: (PIC 9(05)V9(02)) - Facility Specific Rate.
                *   **`P-NEW-COLA`**: (PIC 9(01)V9(03)) - Cost of Living Adjustment.
                *   **`P-NEW-INTERN-RATIO`**: (PIC 9(01)V9(04)) - Intern Ratio.
                *   **`P-NEW-BED-SIZE`**: (PIC 9(05)) - Bed Size.
                *   **`P-NEW-OPER-CSTCHG-RATIO`**: (PIC 9(01)V9(03)) - Operating Cost to Charge Ratio.
                *   **`P-NEW-CMI`**: (PIC 9(01)V9(04)) - CMI.
                *   **`P-NEW-SSI-RATIO`**: (PIC V9(04)) - SSI Ratio.
                *   **`P-NEW-MEDICAID-RATIO`**: (PIC V9(04)) - Medicaid Ratio.
                *   **`P-NEW-PPS-BLEND-YR-IND`**: (PIC 9(01)) - PPS Blend Year Indicator.
                *   **`P-NEW-PRUF-UPDTE-FACTOR`**: (PIC 9(01)V9(05)) - PRUF Update Factor.
                *   **`P-NEW-DSH-PERCENT`**: (PIC V