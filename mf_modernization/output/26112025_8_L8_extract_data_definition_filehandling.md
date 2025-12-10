## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

### Program: LTCAL032

*   **File Accesses:**

    *   No explicit file accesses are defined in the `FILE-CONTROL` section. The program relies on data passed via the `LINKAGE SECTION`.
    *   Implicitly uses the `COPY LTDRG031` which likely contains data for DRG codes, relative weights, and average lengths of stay.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01 W-STORAGE-REF PIC X(46)`:  A working storage reference, likely for program identification.
    *   `01 CAL-VERSION PIC X(05)`: Stores the version of the calculation program.
    *   `COPY LTDRG031`: Includes the data structures defined in `LTDRG031` (DRG data).
    *   `01 HOLD-PPS-COMPONENTS`: This group holds intermediate calculation results and components.
        *   `05 H-LOS PIC 9(03)`: Length of Stay (LOS) from the input bill data.
        *   `05 H-REG-DAYS PIC 9(03)`: Regular Days, calculated as Cov Days - LTR Days.
        *   `05 H-TOTAL-DAYS PIC 9(05)`: Total Days, calculated as Reg Days + LTR Days.
        *   `05 H-SSOT PIC 9(02)`: Short Stay Threshold, calculated as 5/6 of Average LOS.
        *   `05 H-BLEND-RTC PIC 9(02)`: Return code for blending.
        *   `05 H-BLEND-FAC PIC 9(01)V9(01)`: Facility blend percentage.
        *   `05 H-BLEND-PPS PIC 9(01)V9(01)`: PPS blend percentage.
        *   `05 H-SS-PAY-AMT PIC 9(07)V9(02)`: Short Stay Payment Amount.
        *   `05 H-SS-COST PIC 9(07)V9(02)`: Short Stay Cost.
        *   `05 H-LABOR-PORTION PIC 9(07)V9(06)`: Labor portion of the payment.
        *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06)`: Non-labor portion of the payment.
        *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02)`: Fixed Loss Amount used for outlier calculation.
        *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: New Facility Specific Rate.
    *   `01  PRICER-OPT-VERS-SW`: This group holds the pricer option switch and version information.
        *   `05 PRICER-OPTION-SW PIC X(01)`:  Switch to determine if all tables or provider record is passed.
            *   `88 ALL-TABLES-PASSED VALUE 'A'`: Indicates that all tables are passed.
            *   `88 PROV-RECORD-PASSED VALUE 'P'`: Indicates that provider record is passed.
        *   `05 PPS-VERSIONS`: Group to hold the version of the PPS related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version of the DRG program.
    *   `01  PPS-DATA-ALL`: This group contains the data passed back to the calling program with the results.
        *   `05 PPS-RTC PIC 9(02)`: Return Code.
        *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02)`: Charge Threshold for outliers.
        *   `05 PPS-DATA`: Group containing PPS related data.
            *   `10 PPS-MSA PIC X(04)`: MSA code.
            *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04)`: Wage index.
            *   `10 PPS-AVG-LOS PIC 9(02)V9(01)`: Average Length of Stay.
            *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04)`: Relative weight for the DRG.
            *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02)`: Outlier Payment Amount.
            *   `10 PPS-LOS PIC 9(03)`: Length of Stay.
            *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02)`: DRG Adjusted Payment Amount.
            *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02)`: Federal Payment Amount.
            *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02)`: Final Payment Amount.
            *   `10 PPS-FAC-COSTS PIC 9(07)V9(02)`: Facility Costs.
            *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02)`: New Facility Specific Rate.
            *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02)`: Outlier Threshold.
            *   `10 PPS-SUBM-DRG-CODE PIC X(03)`: Submitted DRG code.
            *   `10 PPS-CALC-VERS-CD PIC X(05)`: Calculation Version Code.
            *   `10 PPS-REG-DAYS-USED PIC 9(03)`: Regular Days Used.
            *   `10 PPS-LTR-DAYS-USED PIC 9(03)`: Lifetime Reserve Days Used.
            *   `10 PPS-BLEND-YEAR PIC 9(01)`: Blend year indicator.
            *   `10 PPS-COLA PIC 9(01)V9(03)`: Cost of Living Adjustment.
            *   `10 FILLER PIC X(04)`: Filler.
        *   `05 PPS-OTHER-DATA`: Group containing other PPS related data.
            *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05)`: National Labor Percentage.
            *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05)`: National Non-labor Percentage.
            *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02)`: Standard Federal Rate.
            *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03)`: Budget Neutrality Rate.
            *   `10 FILLER PIC X(20)`: Filler.
        *   `05 PPS-PC-DATA`: Group containing PPS related data.
            *   `10 PPS-COT-IND PIC X(01)`: Cost Outlier Indicator.
            *   `10 FILLER PIC X(20)`: Filler.

*   **Data Structures in LINKAGE SECTION:**

    *   `01 BILL-NEW-DATA`:  This is the input data structure representing the bill information passed *to* this program.
        *   `10 B-NPI10`: National Provider Identifier (NPI) - 10 characters.
            *   `15 B-NPI8 PIC X(08)`:  NPI - First 8 characters.
            *   `15 B-NPI-FILLER PIC X(02)`: NPI - Filler/last 2 characters.
        *   `10 B-PROVIDER-NO PIC X(06)`: Provider Number.
        *   `10 B-PATIENT-STATUS PIC X(02)`: Patient Status.
        *   `10 B-DRG-CODE PIC X(03)`: DRG Code.
        *   `10 B-LOS PIC 9(03)`: Length of Stay.
        *   `10 B-COV-DAYS PIC 9(03)`: Covered Days.
        *   `10 B-LTR-DAYS PIC 9(02)`: Lifetime Reserve Days.
        *   `10 B-DISCHARGE-DATE`: Discharge Date.
            *   `15 B-DISCHG-CC PIC 9(02)`: Century code of the discharge date.
            *   `15 B-DISCHG-YY PIC 9(02)`: Year of the discharge date.
            *   `15 B-DISCHG-MM PIC 9(02)`: Month of the discharge date.
            *   `15 B-DISCHG-DD PIC 9(02)`: Day of the discharge date.
        *   `10 B-COV-CHARGES PIC 9(07)V9(02)`: Covered Charges.
        *   `10 B-SPEC-PAY-IND PIC X(01)`: Special Payment Indicator.
        *   `10 FILLER PIC X(13)`: Filler.
    *   `01  PROV-NEW-HOLD`:  This is the Provider record passed *to* this program.
        *   `02 PROV-NEWREC-HOLD1`: Group containing provider record data.
            *   `05 P-NEW-NPI10`: National Provider Identifier (NPI) - 10 characters.
                *   `10 P-NEW-NPI8 PIC X(08)`:  NPI - First 8 characters.
                *   `10 P-NEW-NPI-FILLER PIC X(02)`: NPI - Filler/last 2 characters.
            *   `05 P-NEW-PROVIDER-NO`: Provider Number.
                *   `10 P-NEW-STATE PIC 9(02)`: State Code.
                *   `10 FILLER PIC X(04)`: Filler.
            *   `05 P-NEW-DATE-DATA`: Date data group.
                *   `10 P-NEW-EFF-DATE`: Effective Date.
                    *   `15 P-NEW-EFF-DT-CC PIC 9(02)`: Century code of the effective date.
                    *   `15 P-NEW-EFF-DT-YY PIC 9(02)`: Year of the effective date.
                    *   `15 P-NEW-EFF-DT-MM PIC 9(02)`: Month of the effective date.
                    *   `15 P-NEW-EFF-DT-DD PIC 9(02)`: Day of the effective date.
                *   `10 P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02)`: Century code of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02)`: Year of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02)`: Month of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02)`: Day of the FY begin date.
                *   `10 P-NEW-REPORT-DATE`: Report Date.
                    *   `15 P-NEW-REPORT-DT-CC PIC 9(02)`: Century code of the report date.
                    *   `15 P-NEW-REPORT-DT-YY PIC 9(02)`: Year of the report date.
                    *   `15 P-NEW-REPORT-DT-MM PIC 9(02)`: Month of the report date.
                    *   `15 P-NEW-REPORT-DT-DD PIC 9(02)`: Day of the report date.
                *   `10 P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `15 P-NEW-TERM-DT-CC PIC 9(02)`: Century code of the termination date.
                    *   `15 P-NEW-TERM-DT-YY PIC 9(02)`: Year of the termination date.
                    *   `15 P-NEW-TERM-DT-MM PIC 9(02)`: Month of the termination date.
                    *   `15 P-NEW-TERM-DT-DD PIC 9(02)`: Day of the termination date.
            *   `05 P-NEW-WAIVER-CODE PIC X(01)`: Waiver Code.
                *   `88 P-NEW-WAIVER-STATE VALUE 'Y'`: Waiver State Indicator.
            *   `05 P-NEW-INTER-NO PIC 9(05)`: Internal Number.
            *   `05 P-NEW-PROVIDER-TYPE PIC X(02)`: Provider Type.
            *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Current Census Division.
            *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Redefinition of Current Census Division.
            *   `05 P-NEW-MSA-DATA`: MSA Data group.
                *   `10 P-NEW-CHG-CODE-INDEX PIC X`: Charge Code Index.
                *   `10 P-NEW-GEO-LOC-MSAX PIC X(04)`: Geographical Location MSA.
                *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04)`: Redefinition of Geographical Location MSA.
                *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04)`: Wage Index Location MSA.
                *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04)`: Standard Amount Location MSA.
                *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Redefinition of Standard Amount Location MSA.
                    *   `15 P-NEW-RURAL-1ST`: Rural Indicator 1st.
                        *   `20 P-NEW-STAND-RURAL PIC XX`: Rural Standard.
                            *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '`: Rural Check.
                    *   `15 P-NEW-RURAL-2ND PIC XX`: Rural Indicator 2nd.
            *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX`: Sole Community Hospital Year.
            *   `05 P-NEW-LUGAR PIC X`: Lugar.
            *   `05 P-NEW-TEMP-RELIEF-IND PIC X`: Temporary Relief Indicator.
            *   `05 P-NEW-FED-PPS-BLEND-IND PIC X`: Federal PPS Blend Indicator.
            *   `05 FILLER PIC X(05)`: Filler.
        *   `02 PROV-NEWREC-HOLD2`: Group containing provider record data.
            *   `05 P-NEW-VARIABLES`: Variables group.
                *   `10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: Facility Specific Rate.
                *   `10 P-NEW-COLA PIC 9(01)V9(03)`: Cost of Living Adjustment.
                *   `10 P-NEW-INTERN-RATIO PIC 9(01)V9(04)`: Intern Ratio.
                *   `10 P-NEW-BED-SIZE PIC 9(05)`: Bed Size.
                *   `10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03)`: Operating Cost to Charge Ratio.
                *   `10 P-NEW-CMI PIC 9(01)V9(04)`: CMI.
                *   `10 P-NEW-SSI-RATIO PIC V9(04)`: SSI Ratio.
                *   `10 P-NEW-MEDICAID-RATIO PIC V9(04)`: Medicaid Ratio.
                *   `10 P-NEW-PPS-BLEND-YR-IND PIC 9(01)`: PPS Blend Year Indicator.
                *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05)`: Pruf Update Factor.
                *   `10 P-NEW-DSH-PERCENT PIC V9(04)`: DSH Percentage.
                *   `10 P-NEW-FYE-DATE PIC X(08)`: Fiscal Year End Date.
            *   `05 FILLER PIC X(23)`: Filler.
        *   `02 PROV-NEWREC-HOLD3`: Group containing provider record data.
            *   `05 P-NEW-PASS-AMT-DATA`: Passed Amount Data.
                *   `10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99`: Capital Passed Amount.
                *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99`: Direct Medical Education Passed Amount.
                *   `10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99`: Organ Acquisition Passed Amount.
                *   `10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99`: Plus Misc Passed Amount.
            *   `05 P-NEW-CAPI-DATA`: Capital Data.
                *   `15 P-NEW-CAPI-PPS-PAY-CODE PIC X`: Capital PPS Pay Code.
                *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99`: Hospital Specific Rate.
                *   `15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99`: Old Harm Rate.
                *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999`: New Harm Ratio.
                *   `15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999`: Capital Cost to Charge Ratio.
                *   `15 P-NEW-CAPI-NEW-HOSP PIC X`: New Hospital.
                *   `15 P-NEW-CAPI-IME PIC 9V9999`: Capital IME.
                *   `15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99`: Capital Exceptions.
            *   `05 FILLER PIC X(22)`: Filler.
    *   `01 WAGE-NEW-INDEX-RECORD`:  This is the Wage Index record passed *to* this program.
        *   `05 W-MSA PIC X(4)`: MSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective Date.
        *   `05 W-WAGE-INDEX1 PIC S9(02)V9(04)`: Wage Index 1.
        *   `05 W-WAGE-INDEX2 PIC S9(02)V9(04)`: Wage Index 2.
        *   `05 W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage Index 3.

### Program: LTCAL042

*   **File Accesses:**

    *   No explicit file accesses are defined in the `FILE-CONTROL` section.
    *   Implicitly uses the `COPY LTDRG031` which likely contains data for DRG codes, relative weights, and average lengths of stay.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01 W-STORAGE-REF PIC X(46)`:  A working storage reference, likely for program identification.
    *   `01 CAL-VERSION PIC X(05)`: Stores the version of the calculation program.
    *   `COPY LTDRG031`: Includes the data structures defined in `LTDRG031` (DRG data).
    *   `01 HOLD-PPS-COMPONENTS`: This group holds intermediate calculation results and components.
        *   `05 H-LOS PIC 9(03)`: Length of Stay (LOS) from the input bill data.
        *   `05 H-REG-DAYS PIC 9(03)`: Regular Days, calculated as Cov Days - LTR Days.
        *   `05 H-TOTAL-DAYS PIC 9(05)`: Total Days, calculated as Reg Days + LTR Days.
        *   `05 H-SSOT PIC 9(02)`: Short Stay Threshold, calculated as 5/6 of Average LOS.
        *   `05 H-BLEND-RTC PIC 9(02)`: Return code for blending.
        *   `05 H-BLEND-FAC PIC 9(01)V9(01)`: Facility blend percentage.
        *   `05 H-BLEND-PPS PIC 9(01)V9(01)`: PPS blend percentage.
        *   `05 H-SS-PAY-AMT PIC 9(07)V9(02)`: Short Stay Payment Amount.
        *   `05 H-SS-COST PIC 9(07)V9(02)`: Short Stay Cost.
        *   `05 H-LABOR-PORTION PIC 9(07)V9(06)`: Labor portion of the payment.
        *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06)`: Non-labor portion of the payment.
        *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02)`: Fixed Loss Amount used for outlier calculation.
        *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02)`: New Facility Specific Rate.
        *   `05 H-LOS-RATIO PIC 9(01)V9(05)`: Length of stay ratio.
    *   `01  PRICER-OPT-VERS-SW`: This group holds the pricer option switch and version information.
        *   `05 PRICER-OPTION-SW PIC X(01)`:  Switch to determine if all tables or provider record is passed.
            *   `88 ALL-TABLES-PASSED VALUE 'A'`: Indicates that all tables are passed.
            *   `88 PROV-RECORD-PASSED VALUE 'P'`: Indicates that provider record is passed.
        *   `05 PPS-VERSIONS`: Group to hold the version of the PPS related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version of the DRG program.
    *   `01  PPS-DATA-ALL`: This group contains the data passed back to the calling program with the results.
        *   `05 PPS-RTC PIC 9(02)`: Return Code.
        *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02)`: Charge Threshold for outliers.
        *   `05 PPS-DATA`: Group containing PPS related data.
            *   `10 PPS-MSA PIC X(04)`: MSA code.
            *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04)`: Wage index.
            *   `10 PPS-AVG-LOS PIC 9(02)V9(01)`: Average Length of Stay.
            *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04)`: Relative weight for the DRG.
            *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02)`: Outlier Payment Amount.
            *   `10 PPS-LOS PIC 9(03)`: Length of Stay.
            *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02)`: DRG Adjusted Payment Amount.
            *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02)`: Federal Payment Amount.
            *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02)`: Final Payment Amount.
            *   `10 PPS-FAC-COSTS PIC 9(07)V9(02)`: Facility Costs.
            *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02)`: New Facility Specific Rate.
            *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02)`: Outlier Threshold.
            *   `10 PPS-SUBM-DRG-CODE PIC X(03)`: Submitted DRG code.
            *   `10 PPS-CALC-VERS-CD PIC X(05)`: Calculation Version Code.
            *   `10 PPS-REG-DAYS-USED PIC 9(03)`: Regular Days Used.
            *   `10 PPS-LTR-DAYS-USED PIC 9(03)`: Lifetime Reserve Days Used.
            *   `10 PPS-BLEND-YEAR PIC 9(01)`: Blend year indicator.
            *   `10 PPS-COLA PIC 9(01)V9(03)`: Cost of Living Adjustment.
            *   `10 FILLER PIC X(04)`: Filler.
        *   `05 PPS-OTHER-DATA`: Group containing other PPS related data.
            *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05)`: National Labor Percentage.
            *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05)`: National Non-labor Percentage.
            *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02)`: Standard Federal Rate.
            *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03)`: Budget Neutrality Rate.
            *   `10 FILLER PIC X(20)`: Filler.
        *   `05 PPS-PC-DATA`: Group containing PPS related data.
            *   `10 PPS-COT-IND PIC X(01)`: Cost Outlier Indicator.
            *   `10 FILLER PIC X(20)`: Filler.

*   **Data Structures in LINKAGE SECTION:**

    *   `01 BILL-NEW-DATA`:  This is the input data structure representing the bill information passed *to* this program.
        *   `10 B-NPI10`: National Provider Identifier (NPI) - 10 characters.
            *   `15 B-NPI8 PIC X(08)`:  NPI - First 8 characters.
            *   `15 B-NPI-FILLER PIC X(02)`: NPI - Filler/last 2 characters.
        *   `10 B-PROVIDER-NO PIC X(06)`: Provider Number.
        *   `10 B-PATIENT-STATUS PIC X(02)`: Patient Status.
        *   `10 B-DRG-CODE PIC X(03)`: DRG Code.
        *   `10 B-LOS PIC 9(03)`: Length of Stay.
        *   `10 B-COV-DAYS PIC 9(03)`: Covered Days.
        *   `10 B-LTR-DAYS PIC 9(02)`: Lifetime Reserve Days.
        *   `10 B-DISCHARGE-DATE`: Discharge Date.
            *   `15 B-DISCHG-CC PIC 9(02)`: Century code of the discharge date.
            *   `15 B-DISCHG-YY PIC 9(02)`: Year of the discharge date.
            *   `15 B-DISCHG-MM PIC 9(02)`: Month of the discharge date.
            *   `15 B-DISCHG-DD PIC 9(02)`: Day of the discharge date.
        *   `10 B-COV-CHARGES PIC 9(07)V9(02)`: Covered Charges.
        *   `10 B-SPEC-PAY-IND PIC X(01)`: Special Payment Indicator.
        *   `10 FILLER PIC X(13)`: Filler.
    *   `01  PROV-NEW-HOLD`:  This is the Provider record passed *to* this program.
        *   `02 PROV-NEWREC-HOLD1`: Group containing provider record data.
            *   `05 P-NEW-NPI10`: National Provider Identifier (NPI) - 10 characters.
                *   `10 P-NEW-NPI8 PIC X(08)`:  NPI - First 8 characters.
                *   `10 P-NEW-NPI-FILLER PIC X(02)`: NPI - Filler/last 2 characters.
            *   `05 P-NEW-PROVIDER-NO`: Provider Number.
                *   `10 P-NEW-STATE PIC 9(02)`: State Code.
                *   `10 FILLER PIC X(04)`: Filler.
            *   `05 P-NEW-DATE-DATA`: Date data group.
                *   `10 P-NEW-EFF-DATE`: Effective Date.
                    *   `15 P-NEW-EFF-DT-CC PIC 9(02)`: Century code of the effective date.
                    *   `15 P-NEW-EFF-DT-YY PIC 9(02)`: Year of the effective date.
                    *   `15 P-NEW-EFF-DT-MM PIC 9(02)`: Month of the effective date.
                    *   `15 P-NEW-EFF-DT-DD PIC 9(02)`: Day of the effective date.
                *   `10 P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
                    *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02)`: Century code of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02)`: Year of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02)`: Month of the FY begin date.
                    *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02)`: Day of the FY begin date.
                *   `10 P-NEW-REPORT-DATE`: Report Date.
                    *   `15 P-NEW-REPORT-DT-CC PIC 9(02)`: Century code of the report date.
                    *   `15 P-NEW-REPORT-DT-YY PIC 9(02)`: Year of the report date.
                    *   `15 P-NEW-REPORT-DT-MM PIC 9(02)`: Month of the report date.
                    *   `15 P-NEW-REPORT-DT-DD PIC 9(02)`: Day of the report date.
                *   `10 P-NEW-TERMINATION-DATE`: Termination Date.
                    *   `15 P-NEW-TERM-DT-CC PIC 9(02)`: Century code of the termination date.
                    *   `15 P-NEW-TERM-DT-YY PIC 9(02)`: Year of the termination date.
                    *   `15 P-NEW-TERM-DT-MM PIC 9(02)`: Month of the termination date.
                    *   `15 P-NEW-TERM-DT-DD PIC 9(02)`: Day of the termination date.
            *   `05 P-NEW-WAIVER-CODE PIC X(01)`: Waiver Code.
                *   `88 P-NEW-WAIVER-STATE VALUE 'Y'`: Waiver State Indicator.
            *   `05 P-NEW-INTER-NO PIC 9(05)`: Internal Number.
            *   `05 P-NEW-PROVIDER-TYPE PIC X(02)`: Provider Type.
            *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Current Census Division.
            *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01)`: Redefinition of Current Census Division.
            *   `05 P-NEW-MSA-DATA`: MSA Data group.
                *   `10 P-NEW-CHG-CODE-INDEX PIC X`: Charge Code Index.
                *   `10 P-NEW-GEO-LOC-MSAX PIC X(04)`: Geographical Location MSA.
                *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04)`: Redefinition of Geographical Location MSA.
                *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04)`: Wage Index Location MSA.
                *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04)`: Standard Amount Location MSA.
                *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA`: Redefinition of Standard Amount Location MSA.
                    *   `15 P-NEW-RURAL-1ST`: Rural Indicator 1st.
                        *   `20 P-NEW-STAND-RURAL PIC XX`: Rural Standard.
                            *   `88 P-NEW-STD-RURAL-CHECK VALUE '  '`: Rural Check.
                    *   `15 P-NEW-RURAL-2ND PIC XX`: Rural Indicator 2nd.
            *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX`: Sole Community Hospital Year.
            *   `05 P-NEW-LUGAR PIC X`: Lugar.
            *   `05 P-NEW-TEMP-RELIEF-IND PIC X`: Temporary Relief Indicator.
            *   `05 P-NEW-FED-PPS-BLEND-IND PIC X`: Federal PPS Blend Indicator.
