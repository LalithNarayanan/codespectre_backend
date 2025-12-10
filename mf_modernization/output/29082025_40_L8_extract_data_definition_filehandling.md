## Analysis of COBOL Programs

Here's an analysis of each COBOL program, detailing the files accessed, data structures, and their descriptions.

### Program: LTCAL032

**1. Files Accessed:**

*   **COPY LTDRG031.** - This program incorporates the data structure definitions from the file `LTDRG031`.  This is a copybook containing DRG-related data, likely a table of DRG codes, relative weights, and average lengths of stay.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.** - A descriptive field, likely for debugging or identification of the program's working storage.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.** -  Stores the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS.** - This group contains intermediate calculation components.
    *   **05 H-LOS PIC 9(03).** - Length of Stay (LOS) - probably from the input bill.
    *   **05 H-REG-DAYS PIC 9(03).** - Regular Days.
    *   **05 H-TOTAL-DAYS PIC 9(05).** - Total Days.
    *   **05 H-SSOT PIC 9(02).** - Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC PIC 9(02).** - Blend Return Code.  Indicates the blend year for blended payments.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).** - Blend Facility Percentage.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).** - Blend PPS Percentage.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).** - Short Stay Payment Amount.
    *   **05 H-SS-COST PIC 9(07)V9(02).** - Short Stay Cost.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).** - Labor Portion of the payment.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).** - Non-Labor Portion of the payment.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).** - Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - New Facility Specific Rate.

**3. Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.** - This is the main input record passed to the program, representing the billing data.
    *   **10 B-NPI10.** - National Provider Identifier (NPI) - A unique identifier for the provider.
        *   **15 B-NPI8 PIC X(08).** -  First 8 characters of NPI.
        *   **15 B-NPI-FILLER PIC X(02).** - Filler for NPI.
    *   **10 B-PROVIDER-NO PIC X(06).** - Provider Number.
    *   **10 B-PATIENT-STATUS PIC X(02).** - Patient Status.
    *   **10 B-DRG-CODE PIC X(03).** - Diagnosis Related Group (DRG) code.
    *   **10 B-LOS PIC 9(03).** - Length of Stay.
    *   **10 B-COV-DAYS PIC 9(03).** - Covered Days.
    *   **10 B-LTR-DAYS PIC 9(02).** - Lifetime Reserve Days.
    *   **10 B-DISCHARGE-DATE.** - Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).** - Century Code of Discharge Date.
        *   **15 B-DISCHG-YY PIC 9(02).** - Year of Discharge Date.
        *   **15 B-DISCHG-MM PIC 9(02).** - Month of Discharge Date.
        *   **15 B-DISCHG-DD PIC 9(02).** - Day of Discharge Date.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).** - Covered Charges.
    *   **10 B-SPEC-PAY-IND PIC X(01).** - Special Payment Indicator.
    *   **10 FILLER PIC X(13).** - Unused filler.
*   **01 PPS-DATA-ALL.** - This is the main output record, containing the calculated payment information.
    *   **05 PPS-RTC PIC 9(02).** - Return Code - Indicates the outcome of the pricing calculation (e.g., normal payment, outlier, error).
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).** - Charge Threshold.
    *   **05 PPS-DATA.** - Contains calculated payment data.
        *   **10 PPS-MSA PIC X(04).** - Metropolitan Statistical Area (MSA) code.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).** - Wage Index.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).** - Average Length of Stay.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).** - Relative Weight.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).** - Outlier Payment Amount.
        *   **10 PPS-LOS PIC 9(03).** - Length of Stay.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).** - DRG Adjusted Payment Amount.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).** - Federal Payment Amount.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).** - Final Payment Amount.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).** - Facility Costs.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).** - New Facility Specific Rate.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).** - Outlier Threshold.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).** - Submitted DRG Code.
        *   **10 PPS-CALC-VERS-CD PIC X(05).** - Calculation Version Code.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).** - Regular Days Used.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).** - Lifetime Reserve Days Used.
        *   **10 PPS-BLEND-YEAR PIC 9(01).** - Blend Year.
        *   **10 PPS-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment (COLA).
        *   **10 FILLER PIC X(04).** - Filler.
    *   **05 PPS-OTHER-DATA.** - Contains other payment-related data.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).** - National Labor Percentage.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).** - National Non-Labor Percentage.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).** - Standard Federal Rate.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).** - Budget Neutrality Rate.
        *   **10 FILLER PIC X(20).** - Filler.
    *   **05 PPS-PC-DATA.** - Contains data related to the Provider Cost.
        *   **10 PPS-COT-IND PIC X(01).** - Cost Outlier Indicator.
        *   **10 FILLER PIC X(20).** - Filler.
*   **01 PRICER-OPT-VERS-SW.** -  Switch to indicate which tables/records are being passed.
    *   **05 PRICER-OPTION-SW PIC X(01).** -  Option Switch
        *   **88 ALL-TABLES-PASSED VALUE 'A'.** -  Indicates all tables are passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.** - Indicates the provider record is passed.
    *   **05 PPS-VERSIONS.** -  Contains the versions of the programs used.
        *   **10 PPDRV-VERSION PIC X(05).** - Version of the PPDRV program.
*   **01 PROV-NEW-HOLD.** -  Provider Record - Contains Provider-specific information.
    *   **02 PROV-NEWREC-HOLD1.** - Grouping of provider record fields.
        *   **05 P-NEW-NPI10.** - NPI.
            *   **10 P-NEW-NPI8 PIC X(08).** - NPI (first 8 characters).
            *   **10 P-NEW-NPI-FILLER PIC X(02).** - NPI Filler.
        *   **05 P-NEW-PROVIDER-NO PIC X(06).** - Provider Number.
        *   **05 P-NEW-DATE-DATA.** - Date information.
            *   **10 P-NEW-EFF-DATE.** - Effective Date.
                *   **15 P-NEW-EFF-DT-CC PIC 9(02).** - Century Code of Effective Date.
                *   **15 P-NEW-EFF-DT-YY PIC 9(02).** - Year of Effective Date.
                *   **15 P-NEW-EFF-DT-MM PIC 9(02).** - Month of Effective Date.
                *   **15 P-NEW-EFF-DT-DD PIC 9(02).** - Day of Effective Date.
            *   **10 P-NEW-FY-BEGIN-DATE.** - Fiscal Year Begin Date.
                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).** - Day.
            *   **10 P-NEW-REPORT-DATE.** - Report Date.
                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).** - Day.
            *   **10 P-NEW-TERMINATION-DATE.** - Termination Date.
                *   **15 P-NEW-TERM-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-TERM-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-TERM-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-TERM-DT-DD PIC 9(02).** - Day.
        *   **05 P-NEW-WAIVER-CODE PIC X(01).** - Waiver Code.
            *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.** - Waiver State.
        *   **05 P-NEW-INTER-NO PIC 9(05).** - Internal Number.
        *   **05 P-NEW-PROVIDER-TYPE PIC X(02).** - Provider Type.
        *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).** - Current Census Division.
        *   **05 P-NEW-MSA-DATA.** - MSA Data.
            *   **10 P-NEW-CHG-CODE-INDEX PIC X.** - Charge Code Index.
            *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.** - Geographical Location MSA.
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.** - Wage Index Location MSA.
            *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.** - Standard Amount Location MSA.
        *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.** -  Sole Community Hospital Year.
        *   **05 P-NEW-LUGAR PIC X.** - Lugar - Location Indicator.
        *   **05 P-NEW-TEMP-RELIEF-IND PIC X.** - Temporary Relief Indicator.
        *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.** - Federal PPS Blend Indicator.
        *   **05 FILLER PIC X(05).** - Filler.
    *   **02 PROV-NEWREC-HOLD2.** - More Provider Record fields.
        *   **05 P-NEW-VARIABLES.** - Provider Variables.
            *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - Facility Specific Rate.
            *   **10 P-NEW-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment.
            *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).** - Intern Ratio.
            *   **10 P-NEW-BED-SIZE PIC 9(05).** - Bed Size.
            *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).** - Operating Cost to Charge Ratio.
            *   **10 P-NEW-CMI PIC 9(01)V9(04).** - Case Mix Index.
            *   **10 P-NEW-SSI-RATIO PIC V9(04).** - Supplemental Security Income Ratio.
            *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).** - Medicaid Ratio.
            *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).** - PPS Blend Year Indicator.
            *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).** - Pruf Update Factor.
            *   **10 P-NEW-DSH-PERCENT PIC V9(04).** - Disproportionate Share Hospital (DSH) Percentage.
            *   **10 P-NEW-FYE-DATE PIC X(08).** - Fiscal Year End Date.
        *   **05 FILLER PIC X(23).** - Filler.
    *   **02 PROV-NEWREC-HOLD3.** - More Provider Record fields.
        *   **05 P-NEW-PASS-AMT-DATA.** - Pass Through Amount Data.
            *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.** - Capital Pass Through Amount.
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.** - Direct Medical Education Pass Through Amount.
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.** - Organ Acquisition Pass Through Amount.
            *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.** - Plus Miscellaneous Pass Through Amount.
        *   **05 P-NEW-CAPI-DATA.** - Capital Data.
            *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X.** - PPS Payment Code.
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.** - Hospital Specific Rate.
            *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.** - Old Harm Rate.
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.** - New Harm Ratio.
            *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.** - Cost to Charge Ratio.
            *   **15 P-NEW-CAPI-NEW-HOSP PIC X.** - New Hospital Indicator.
            *   **15 P-NEW-CAPI-IME PIC 9V9999.** - Indirect Medical Education.
            *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.** - Exceptions.
        *   **05 FILLER PIC X(22).** - Filler.
*   **01 WAGE-NEW-INDEX-RECORD.** - Wage Index Record.
    *   **05 W-MSA PIC X(4).** - MSA Code.
    *   **05 W-EFF-DATE PIC X(8).** - Effective Date.
    *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04).** - Wage Index 1.
    *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04).** - Wage Index 2.
    *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04).** - Wage Index 3.

### Program: LTCAL042

**1. Files Accessed:**

*   **COPY LTDRG031.** - This program also includes the copybook `LTDRG031`, which contains DRG-related data definitions.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.** - A descriptive field for program identification.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.** - Stores the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS.** - Similar to LTCAL032, this group contains intermediate calculation components.
    *   **05 H-LOS PIC 9(03).** - Length of Stay (LOS).
    *   **05 H-REG-DAYS PIC 9(03).** - Regular Days.
    *   **05 H-TOTAL-DAYS PIC 9(05).** - Total Days.
    *   **05 H-SSOT PIC 9(02).** - Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC PIC 9(02).** - Blend Return Code.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).** - Blend Facility Percentage.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).** - Blend PPS Percentage.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).** - Short Stay Payment Amount.
    *   **05 H-SS-COST PIC 9(07)V9(02).** - Short Stay Cost.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).** - Labor Portion.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).** - Non-Labor Portion.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).** - Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - New Facility Specific Rate.
    *   **05 H-LOS-RATIO PIC 9(01)V9(05).** - Length of Stay Ratio.

**3. Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.** - Same as in LTCAL032 - Input Bill Data.
    *   **10 B-NPI10.** - NPI.
        *   **15 B-NPI8 PIC X(08).** - NPI (first 8 characters).
        *   **15 B-NPI-FILLER PIC X(02).** - NPI Filler.
    *   **10 B-PROVIDER-NO PIC X(06).** - Provider Number.
    *   **10 B-PATIENT-STATUS PIC X(02).** - Patient Status.
    *   **10 B-DRG-CODE PIC X(03).** - DRG Code.
    *   **10 B-LOS PIC 9(03).** - Length of Stay.
    *   **10 B-COV-DAYS PIC 9(03).** - Covered Days.
    *   **10 B-LTR-DAYS PIC 9(02).** - Lifetime Reserve Days.
    *   **10 B-DISCHARGE-DATE.** - Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).** - Century Code.
        *   **15 B-DISCHG-YY PIC 9(02).** - Year.
        *   **15 B-DISCHG-MM PIC 9(02).** - Month.
        *   **15 B-DISCHG-DD PIC 9(02).** - Day.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).** - Covered Charges.
    *   **10 B-SPEC-PAY-IND PIC X(01).** - Special Payment Indicator.
    *   **10 FILLER PIC X(13).** - Filler.
*   **01 PPS-DATA-ALL.** - Same as in LTCAL032 - Output Payment Data.
    *   **05 PPS-RTC PIC 9(02).** - Return Code.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).** - Charge Threshold.
    *   **05 PPS-DATA.** - Payment Data.
        *   **10 PPS-MSA PIC X(04).** - MSA Code.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).** - Wage Index.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).** - Average Length of Stay.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).** - Relative Weight.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).** - Outlier Payment Amount.
        *   **10 PPS-LOS PIC 9(03).** - Length of Stay.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).** - DRG Adjusted Payment Amount.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).** - Federal Payment Amount.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).** - Final Payment Amount.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).** - Facility Costs.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).** - New Facility Specific Rate.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).** - Outlier Threshold.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).** - Submitted DRG Code.
        *   **10 PPS-CALC-VERS-CD PIC X(05).** - Calculation Version Code.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).** - Regular Days Used.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).** - Lifetime Reserve Days Used.
        *   **10 PPS-BLEND-YEAR PIC 9(01).** - Blend Year.
        *   **10 PPS-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment.
        *   **10 FILLER PIC X(04).** - Filler.
    *   **05 PPS-OTHER-DATA.** - Other Payment Data.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).** - National Labor Percentage.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).** - National Non-Labor Percentage.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).** - Standard Federal Rate.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).** - Budget Neutrality Rate.
        *   **10 FILLER PIC X(20).** - Filler.
    *   **05 PPS-PC-DATA.** - Provider Cost Data.
        *   **10 PPS-COT-IND PIC X(01).** - Cost Outlier Indicator.
        *   **10 FILLER PIC X(20).** - Filler.
*   **01 PRICER-OPT-VERS-SW.** -  Same as in LTCAL032 - Switch for passing tables.
    *   **05 PRICER-OPTION-SW PIC X(01).** -  Option Switch
        *   **88 ALL-TABLES-PASSED VALUE 'A'.** -  Indicates all tables are passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.** - Indicates the provider record is passed.
    *   **05 PPS-VERSIONS.** - Program Versions.
        *   **10 PPDRV-VERSION PIC X(05).** - Version of the PPDRV program.
*   **01 PROV-NEW-HOLD.** -  Provider Record - Contains Provider-specific information.
    *   **02 PROV-NEWREC-HOLD1.** - Grouping of provider record fields.
        *   **05 P-NEW-NPI10.** - NPI.
            *   **10 P-NEW-NPI8 PIC X(08).** - NPI (first 8 characters).
            *   **10 P-NEW-NPI-FILLER PIC X(02).** - NPI Filler.
        *   **05 P-NEW-PROVIDER-NO PIC X(06).** - Provider Number.
        *   **05 P-NEW-DATE-DATA.** - Date information.
            *   **10 P-NEW-EFF-DATE.** - Effective Date.
                *   **15 P-NEW-EFF-DT-CC PIC 9(02).** - Century Code of Effective Date.
                *   **15 P-NEW-EFF-DT-YY PIC 9(02).** - Year of Effective Date.
                *   **15 P-NEW-EFF-DT-MM PIC 9(02).** - Month of Effective Date.
                *   **15 P-NEW-EFF-DT-DD PIC 9(02).** - Day of Effective Date.
            *   **10 P-NEW-FY-BEGIN-DATE.** - Fiscal Year Begin Date.
                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).** - Day.
            *   **10 P-NEW-REPORT-DATE.** - Report Date.
                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).** - Day.
            *   **10 P-NEW-TERMINATION-DATE.** - Termination Date.
                *   **15 P-NEW-TERM-DT-CC PIC 9(02).** - Century Code.
                *   **15 P-NEW-TERM-DT-YY PIC 9(02).** - Year.
                *   **15 P-NEW-TERM-DT-MM PIC 9(02).** - Month.
                *   **15 P-NEW-TERM-DT-DD PIC 9(02).** - Day.
        *   **05 P-NEW-WAIVER-CODE PIC X(01).** - Waiver Code.
            *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.** - Waiver State.
        *   **05 P-NEW-INTER-NO PIC 9(05).** - Internal Number.
        *   **05 P-NEW-PROVIDER-TYPE PIC X(02).** - Provider Type.
        *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).** - Current Census Division.
        *   **05 P-NEW-MSA-DATA.** - MSA Data.
            *   **10 P-NEW-CHG-CODE-INDEX PIC X.** - Charge Code Index.
            *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.** - Geographical Location MSA.
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.** - Wage Index Location MSA.
            *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.** - Standard Amount Location MSA.
        *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.** -  Sole Community Hospital Year.
        *   **05 P-NEW-LUGAR PIC X.** - Lugar - Location Indicator.
        *   **05 P-NEW-TEMP-RELIEF-IND PIC X.** - Temporary Relief Indicator.
        *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.** - Federal PPS Blend Indicator.
        *   **05 FILLER PIC X(05).** - Filler.
    *   **02 PROV-NEWREC-HOLD2.** - More Provider Record fields.
        *   **05 P-NEW-VARIABLES.** - Provider Variables.
            *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).** - Facility Specific Rate.
            *   **10 P-NEW-COLA PIC 9(01)V9(03).** - Cost of Living Adjustment.
            *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).** - Intern Ratio.
            *   **10 P-NEW-BED-SIZE PIC 9(05).** - Bed Size.
            *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).** - Operating Cost to Charge Ratio.
            *   **10 P-NEW-CMI PIC 9(01)V9(04).** - Case Mix Index.
            *   **10 P-NEW-SSI-RATIO PIC V9(04).** - Supplemental Security Income Ratio.
            *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).** - Medicaid Ratio.
            *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).** - PPS Blend Year Indicator.
            *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).** - Pruf Update Factor.
            *   **10 P-NEW-DSH-PERCENT PIC V9(04).** - Disproportionate Share Hospital (DSH) Percentage.
            *   **10 P-NEW-FYE-DATE PIC X(08).** - Fiscal Year End Date.
        *   **05 FILLER PIC X(23).** - Filler.
    *   **02 PROV-NEWREC-HOLD3.** - More Provider Record fields.
        *   **05 P-NEW-PASS-AMT-DATA.** - Pass Through Amount Data.
            *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.** - Capital Pass Through Amount.
            *   **10 P-NEW-PASS-AMT-