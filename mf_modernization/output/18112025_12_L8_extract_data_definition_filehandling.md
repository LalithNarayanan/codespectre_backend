## Analysis of COBOL Programs

Here's a breakdown of the provided COBOL programs, including file access, data structures, and their descriptions:

### Program: LTCAL032

**1. Files Accessed:**

*   **COPY LTDRG031:** This is a copybook (included using `COPY`) containing data structures related to DRG (Diagnosis Related Group) information for the fiscal year 2003.  The exact contents are not visible in this program's source code, but it's essential for DRG calculations.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:** (PIC X(46)) A working storage field containing the program's name and a description. Used for identification or debugging.
*   **CAL-VERSION:** (PIC X(05)) Stores the version of the calculation logic.  Value is 'C03.2'.
*   **HOLD-PPS-COMPONENTS:** This group of fields holds intermediate calculation results.  It is used to store data for the payment calculations.
    *   **H-LOS:** (PIC 9(03)) Length of stay.
    *   **H-REG-DAYS:** (PIC 9(03)) Regular days.
    *   **H-TOTAL-DAYS:** (PIC 9(05)) Total days.
    *   **H-SSOT:** (PIC 9(02)) Short Stay Outlier Threshold.
    *   **H-BLEND-RTC:** (PIC 9(02)) Blend Return Code.
    *   **H-BLEND-FAC:** (PIC 9(01)V9(01)) Blend Facility.
    *   **H-BLEND-PPS:** (PIC 9(01)V9(01)) Blend PPS.
    *   **H-SS-PAY-AMT:** (PIC 9(07)V9(02)) Short Stay Payment Amount.
    *   **H-SS-COST:** (PIC 9(07)V9(02)) Short Stay Cost.
    *   **H-LABOR-PORTION:** (PIC 9(07)V9(06)) Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** (PIC 9(07)V9(06)) Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** (PIC 9(07)V9(02)) Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) New Facility Specific Rate.

**3. Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:** This is the main data structure passed *into* the program, likely from a calling program. It contains the billing information.
    *   **B-NPI10:**  NPI (National Provider Identifier)
        *   **B-NPI8:** (PIC X(08)) NPI - 8 Character
        *   **B-NPI-FILLER:** (PIC X(02)) NPI - Filler
    *   **B-PROVIDER-NO:** (PIC X(06)) Provider Number.
    *   **B-PATIENT-STATUS:** (PIC X(02)) Patient Status.
    *   **B-DRG-CODE:** (PIC X(03)) DRG Code.
    *   **B-LOS:** (PIC 9(03)) Length of Stay.
    *   **B-COV-DAYS:** (PIC 9(03)) Covered Days.
    *   **B-LTR-DAYS:** (PIC 9(02)) Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**  Discharge Date.
        *   **B-DISCHG-CC:** (PIC 9(02)) Discharge Century/Code.
        *   **B-DISCHG-YY:** (PIC 9(02)) Discharge Year.
        *   **B-DISCHG-MM:** (PIC 9(02)) Discharge Month.
        *   **B-DISCHG-DD:** (PIC 9(02)) Discharge Day.
    *   **B-COV-CHARGES:** (PIC 9(07)V9(02)) Covered Charges.
    *   **B-SPEC-PAY-IND:** (PIC X(01)) Special Payment Indicator.
    *   **FILLER:** (PIC X(13)) Unused field.
*   **PPS-DATA-ALL:** This structure is used to pass the calculated PPS (Prospective Payment System) data *back* to the calling program.
    *   **PPS-RTC:** (PIC 9(02)) Return Code.  Indicates the result of the calculation (e.g., normal payment, outlier, short stay, error).
    *   **PPS-CHRG-THRESHOLD:** (PIC 9(07)V9(02)) Charges Threshold.
    *   **PPS-DATA:**  Contains the main PPS calculation results.
        *   **PPS-MSA:** (PIC X(04)) MSA (Metropolitan Statistical Area) code.
        *   **PPS-WAGE-INDEX:** (PIC 9(02)V9(04)) Wage Index.
        *   **PPS-AVG-LOS:** (PIC 9(02)V9(01)) Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** (PIC 9(01)V9(04)) Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT:** (PIC 9(07)V9(02)) Outlier Payment Amount.
        *   **PPS-LOS:** (PIC 9(03)) Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** (PIC 9(07)V9(02)) DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** (PIC 9(07)V9(02)) Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** (PIC 9(07)V9(02)) Final Payment Amount.
        *   **PPS-FAC-COSTS:** (PIC 9(07)V9(02)) Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** (PIC 9(07)V9(02)) New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** (PIC 9(07)V9(02)) Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** (PIC X(03)) Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** (PIC X(05)) Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** (PIC 9(03)) Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** (PIC 9(03)) Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** (PIC 9(01)) Blend Year Indicator.
        *   **PPS-COLA:** (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
        *   **FILLER:** (PIC X(04)) Filler.
    *   **PPS-OTHER-DATA:** Contains other PPS related data.
        *   **PPS-NAT-LABOR-PCT:** (PIC 9(01)V9(05)) National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** (PIC 9(01)V9(05)) National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** (PIC 9(05)V9(02)) Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** (PIC 9(01)V9(03)) Budget Neutrality Rate.
        *   **FILLER:** (PIC X(20)) Filler.
    *   **PPS-PC-DATA:**  PPS PC Data.
        *   **PPS-COT-IND:** (PIC X(01)) COT (Cost of Treatment) Indicator.
        *   **FILLER:** (PIC X(20)) Filler.
*   **PRICER-OPT-VERS-SW:**  Pricer Option Version Switch.
    *   **PRICER-OPTION-SW:** (PIC X(01)) Pricer Option Switch.  Used to indicate if all tables or just the provider record was passed.
        *   **ALL-TABLES-PASSED:** (VALUE 'A') Indicates that all tables were passed.
        *   **PROV-RECORD-PASSED:** (VALUE 'P') Indicates that only the provider record was passed.
    *   **PPS-VERSIONS:** PPS Versions.
        *   **PPDRV-VERSION:** (PIC X(05)) PPDRV Version.
*   **PROV-NEW-HOLD:**  This structure is used to pass provider information *into* the program.
    *   **PROV-NEWREC-HOLD1:** Provider Record Hold 1.
        *   **P-NEW-NPI10:** NPI (National Provider Identifier)
            *   **P-NEW-NPI8:** (PIC X(08)) NPI - 8 Character
            *   **P-NEW-NPI-FILLER:** (PIC X(02)) NPI - Filler
        *   **P-NEW-PROVIDER-NO:**  Provider Number.
            *   **P-NEW-STATE:** (PIC 9(02)) Provider State.
            *   **FILLER:** (PIC X(04)) Filler.
        *   **P-NEW-DATE-DATA:** Date Data
            *   **P-NEW-EFF-DATE:** Effective Date.
                *   **P-NEW-EFF-DT-CC:** (PIC 9(02)) Effective Date - Century/Code.
                *   **P-NEW-EFF-DT-YY:** (PIC 9(02)) Effective Date - Year.
                *   **P-NEW-EFF-DT-MM:** (PIC 9(02)) Effective Date - Month.
                *   **P-NEW-EFF-DT-DD:** (PIC 9(02)) Effective Date - Day.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-CC:** (PIC 9(02)) FY Begin Date - Century/Code.
                *   **P-NEW-FY-BEG-DT-YY:** (PIC 9(02)) FY Begin Date - Year.
                *   **P-NEW-FY-BEG-DT-MM:** (PIC 9(02)) FY Begin Date - Month.
                *   **P-NEW-FY-BEG-DT-DD:** (PIC 9(02)) FY Begin Date - Day.
            *   **P-NEW-REPORT-DATE:** Report Date.
                *   **P-NEW-REPORT-DT-CC:** (PIC 9(02)) Report Date - Century/Code.
                *   **P-NEW-REPORT-DT-YY:** (PIC 9(02)) Report Date - Year.
                *   **P-NEW-REPORT-DT-MM:** (PIC 9(02)) Report Date - Month.
                *   **P-NEW-REPORT-DT-DD:** (PIC 9(02)) Report Date - Day.
            *   **P-NEW-TERMINATION-DATE:** Termination Date.
                *   **P-NEW-TERM-DT-CC:** (PIC 9(02)) Termination Date - Century/Code.
                *   **P-NEW-TERM-DT-YY:** (PIC 9(02)) Termination Date - Year.
                *   **P-NEW-TERM-DT-MM:** (PIC 9(02)) Termination Date - Month.
                *   **P-NEW-TERM-DT-DD:** (PIC 9(02)) Termination Date - Day.
        *   **P-NEW-WAIVER-CODE:** (PIC X(01)) Waiver Code.
            *   **P-NEW-WAIVER-STATE:** (VALUE 'Y') Waiver State.
        *   **P-NEW-INTER-NO:** (PIC 9(05)) Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** (PIC X(02)) Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** (PIC 9(01)) Current Census Division.
        *   **P-NEW-CURRENT-DIV:** REDEFINES P-NEW-CURRENT-CENSUS-DIV.
        *   **P-NEW-MSA-DATA:** MSA Data.
            *   **P-NEW-CHG-CODE-INDEX:** (PIC X) Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** (PIC X(04)) Geographic Location MSA (Metropolitan Statistical Area)
            *   **P-NEW-GEO-LOC-MSA9:** REDEFINES P-NEW-GEO-LOC-MSAX.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** (PIC X(04)) Wage Index Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA:** (PIC X(04)) Standard Amount Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA9:** REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST:** Rural 1st.
                    *   **P-NEW-STAND-RURAL:** (PIC XX) Standard Rural.
                        *   **P-NEW-STD-RURAL-CHECK:** (VALUE '  ') Standard Rural Check.
                    *   **P-NEW-RURAL-2ND:** (PIC XX) Rural 2nd.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** (PIC XX) Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** (PIC X) Lugar.
        *   **P-NEW-TEMP-RELIEF-IND:** (PIC X) Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** (PIC X) Federal PPS Blend Indicator.
        *   **FILLER:** (PIC X(05)) Filler.
    *   **PROV-NEWREC-HOLD2:** Provider Record Hold 2.
        *   **P-NEW-VARIABLES:** Variables.
            *   **P-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) Facility Specific Rate.
            *   **P-NEW-COLA:** (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
            *   **P-NEW-INTERN-RATIO:** (PIC 9(01)V9(04)) Intern Ratio.
            *   **P-NEW-BED-SIZE:** (PIC 9(05)) Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** (PIC 9(01)V9(03)) Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** (PIC 9(01)V9(04)) CMI (Case Mix Index).
            *   **P-NEW-SSI-RATIO:** (PIC V9(04)) SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO:** (PIC V9(04)) Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** (PIC 9(01)) PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** (PIC 9(01)V9(05)) PRUF Update Factor.
            *   **P-NEW-DSH-PERCENT:** (PIC V9(04)) DSH (Disproportionate Share Hospital) Percent.
            *   **P-NEW-FYE-DATE:** (PIC X(08)) Fiscal Year End Date.
        *   **FILLER:** (PIC X(23)) Filler.
    *   **PROV-NEWREC-HOLD3:** Provider Record Hold 3.
        *   **P-NEW-PASS-AMT-DATA:** Pass Amount Data.
            *   **P-NEW-PASS-AMT-CAPITAL:** (PIC 9(04)V99) Capital Pass Through Amount.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** (PIC 9(04)V99) Direct Medical Education Pass Through Amount.
            *   **P-NEW-PASS-AMT-ORGAN-ACQ:** (PIC 9(04)V99) Organ Acquisition Pass Through Amount.
            *   **P-NEW-PASS-AMT-PLUS-MISC:** (PIC 9(04)V99) Plus Miscellaneous Pass Through Amount.
        *   **P-NEW-CAPI-DATA:** Capital Data.
            *   **P-NEW-CAPI-PPS-PAY-CODE:** (PIC X) Capital PPS Pay Code.
            *   **P-NEW-CAPI-HOSP-SPEC-RATE:** (PIC 9(04)V99) Hospital Specific Rate.
            *   **P-NEW-CAPI-OLD-HARM-RATE:** (PIC 9(04)V99) Old HARM (Hold Harmless) Rate.
            *   **P-NEW-CAPI-NEW-HARM-RATIO:** (PIC 9(01)V9999) New HARM Ratio.
            *   **P-NEW-CAPI-CSTCHG-RATIO:** (PIC 9V999) Capital Cost to Charge Ratio.
            *   **P-NEW-CAPI-NEW-HOSP:** (PIC X) New Hospital Indicator.
            *   **P-NEW-CAPI-IME:** (PIC 9V9999) Capital IME (Indirect Medical Education).
            *   **P-NEW-CAPI-EXCEPTIONS:** (PIC 9(04)V99) Capital Exceptions.
        *   **FILLER:** (PIC X(22)) Filler.
*   **WAGE-NEW-INDEX-RECORD:** This structure is used to pass the wage index information *into* the program.
    *   **W-MSA:** (PIC X(4)) MSA Code.
    *   **W-EFF-DATE:** (PIC X(8)) Effective Date.
    *   **W-WAGE-INDEX1:** (PIC S9(02)V9(04)) Wage Index 1.
    *   **W-WAGE-INDEX2:** (PIC S9(02)V9(04)) Wage Index 2.
    *   **W-WAGE-INDEX3:** (PIC S9(02)V9(04)) Wage Index 3.

### Program: LTCAL042

**1. Files Accessed:**

*   **COPY LTDRG031:** Same as LTCAL032.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF:** (PIC X(46)) Same as LTCAL032.
*   **CAL-VERSION:** (PIC X(05)) Stores the version of the calculation logic.  Value is 'C04.2'.
*   **HOLD-PPS-COMPONENTS:** Same as LTCAL032.
    *   **H-LOS:** (PIC 9(03)) Length of stay.
    *   **H-REG-DAYS:** (PIC 9(03)) Regular days.
    *   **H-TOTAL-DAYS:** (PIC 9(05)) Total days.
    *   **H-SSOT:** (PIC 9(02)) Short Stay Outlier Threshold.
    *   **H-BLEND-RTC:** (PIC 9(02)) Blend Return Code.
    *   **H-BLEND-FAC:** (PIC 9(01)V9(01)) Blend Facility.
    *   **H-BLEND-PPS:** (PIC 9(01)V9(01)) Blend PPS.
    *   **H-SS-PAY-AMT:** (PIC 9(07)V9(02)) Short Stay Payment Amount.
    *   **H-SS-COST:** (PIC 9(07)V9(02)) Short Stay Cost.
    *   **H-LABOR-PORTION:** (PIC 9(07)V9(06)) Labor Portion of the payment.
    *   **H-NONLABOR-PORTION:** (PIC 9(07)V9(06)) Non-Labor Portion of the payment.
    *   **H-FIXED-LOSS-AMT:** (PIC 9(07)V9(02)) Fixed Loss Amount.
    *   **H-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) New Facility Specific Rate.
    *   **H-LOS-RATIO:** (PIC 9(01)V9(05)) Length of Stay Ratio.

**3. Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:** Same as LTCAL032.
    *   **B-NPI10:**  NPI (National Provider Identifier)
        *   **B-NPI8:** (PIC X(08)) NPI - 8 Character
        *   **B-NPI-FILLER:** (PIC X(02)) NPI - Filler
    *   **B-PROVIDER-NO:** (PIC X(06)) Provider Number.
    *   **B-PATIENT-STATUS:** (PIC X(02)) Patient Status.
    *   **B-DRG-CODE:** (PIC X(03)) DRG Code.
    *   **B-LOS:** (PIC 9(03)) Length of Stay.
    *   **B-COV-DAYS:** (PIC 9(03)) Covered Days.
    *   **B-LTR-DAYS:** (PIC 9(02)) Lifetime Reserve Days.
    *   **B-DISCHARGE-DATE:**  Discharge Date.
        *   **B-DISCHG-CC:** (PIC 9(02)) Discharge Century/Code.
        *   **B-DISCHG-YY:** (PIC 9(02)) Discharge Year.
        *   **B-DISCHG-MM:** (PIC 9(02)) Discharge Month.
        *   **B-DISCHG-DD:** (PIC 9(02)) Discharge Day.
    *   **B-COV-CHARGES:** (PIC 9(07)V9(02)) Covered Charges.
    *   **B-SPEC-PAY-IND:** (PIC X(01)) Special Payment Indicator.
    *   **FILLER:** (PIC X(13)) Unused field.
*   **PPS-DATA-ALL:** Same as LTCAL032.
    *   **PPS-RTC:** (PIC 9(02)) Return Code.  Indicates the result of the calculation (e.g., normal payment, outlier, short stay, error).
    *   **PPS-CHRG-THRESHOLD:** (PIC 9(07)V9(02)) Charges Threshold.
    *   **PPS-DATA:**  Contains the main PPS calculation results.
        *   **PPS-MSA:** (PIC X(04)) MSA (Metropolitan Statistical Area) code.
        *   **PPS-WAGE-INDEX:** (PIC 9(02)V9(04)) Wage Index.
        *   **PPS-AVG-LOS:** (PIC 9(02)V9(01)) Average Length of Stay.
        *   **PPS-RELATIVE-WGT:** (PIC 9(01)V9(04)) Relative Weight.
        *   **PPS-OUTLIER-PAY-AMT:** (PIC 9(07)V9(02)) Outlier Payment Amount.
        *   **PPS-LOS:** (PIC 9(03)) Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT:** (PIC 9(07)V9(02)) DRG Adjusted Payment Amount.
        *   **PPS-FED-PAY-AMT:** (PIC 9(07)V9(02)) Federal Payment Amount.
        *   **PPS-FINAL-PAY-AMT:** (PIC 9(07)V9(02)) Final Payment Amount.
        *   **PPS-FAC-COSTS:** (PIC 9(07)V9(02)) Facility Costs.
        *   **PPS-NEW-FAC-SPEC-RATE:** (PIC 9(07)V9(02)) New Facility Specific Rate.
        *   **PPS-OUTLIER-THRESHOLD:** (PIC 9(07)V9(02)) Outlier Threshold.
        *   **PPS-SUBM-DRG-CODE:** (PIC X(03)) Submitted DRG Code.
        *   **PPS-CALC-VERS-CD:** (PIC X(05)) Calculation Version Code.
        *   **PPS-REG-DAYS-USED:** (PIC 9(03)) Regular Days Used.
        *   **PPS-LTR-DAYS-USED:** (PIC 9(03)) Lifetime Reserve Days Used.
        *   **PPS-BLEND-YEAR:** (PIC 9(01)) Blend Year Indicator.
        *   **PPS-COLA:** (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
        *   **FILLER:** (PIC X(04)) Filler.
    *   **PPS-OTHER-DATA:** Contains other PPS related data.
        *   **PPS-NAT-LABOR-PCT:** (PIC 9(01)V9(05)) National Labor Percentage.
        *   **PPS-NAT-NONLABOR-PCT:** (PIC 9(01)V9(05)) National Non-Labor Percentage.
        *   **PPS-STD-FED-RATE:** (PIC 9(05)V9(02)) Standard Federal Rate.
        *   **PPS-BDGT-NEUT-RATE:** (PIC 9(01)V9(03)) Budget Neutrality Rate.
        *   **FILLER:** (PIC X(20)) Filler.
    *   **PPS-PC-DATA:**  PPS PC Data.
        *   **PPS-COT-IND:** (PIC X(01)) COT (Cost of Treatment) Indicator.
        *   **FILLER:** (PIC X(20)) Filler.
*   **PRICER-OPT-VERS-SW:**  Pricer Option Version Switch.  Same as LTCAL032.
    *   **PRICER-OPTION-SW:** (PIC X(01)) Pricer Option Switch.  Used to indicate if all tables or just the provider record was passed.
        *   **ALL-TABLES-PASSED:** (VALUE 'A') Indicates that all tables were passed.
        *   **PROV-RECORD-PASSED:** (VALUE 'P') Indicates that only the provider record was passed.
    *   **PPS-VERSIONS:** PPS Versions.
        *   **PPDRV-VERSION:** (PIC X(05)) PPDRV Version.
*   **PROV-NEW-HOLD:**  This structure is used to pass provider information *into* the program.  Same as LTCAL032.
    *   **PROV-NEWREC-HOLD1:** Provider Record Hold 1.
        *   **P-NEW-NPI10:** NPI (National Provider Identifier)
            *   **P-NEW-NPI8:** (PIC X(08)) NPI - 8 Character
            *   **P-NEW-NPI-FILLER:** (PIC X(02)) NPI - Filler
        *   **P-NEW-PROVIDER-NO:**  Provider Number.
            *   **P-NEW-STATE:** (PIC 9(02)) Provider State.
            *   **FILLER:** (PIC X(04)) Filler.
        *   **P-NEW-DATE-DATA:** Date Data
            *   **P-NEW-EFF-DATE:** Effective Date.
                *   **P-NEW-EFF-DT-CC:** (PIC 9(02)) Effective Date - Century/Code.
                *   **P-NEW-EFF-DT-YY:** (PIC 9(02)) Effective Date - Year.
                *   **P-NEW-EFF-DT-MM:** (PIC 9(02)) Effective Date - Month.
                *   **P-NEW-EFF-DT-DD:** (PIC 9(02)) Effective Date - Day.
            *   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date.
                *   **P-NEW-FY-BEG-DT-CC:** (PIC 9(02)) FY Begin Date - Century/Code.
                *   **P-NEW-FY-BEG-DT-YY:** (PIC 9(02)) FY Begin Date - Year.
                *   **P-NEW-FY-BEG-DT-MM:** (PIC 9(02)) FY Begin Date - Month.
                *   **P-NEW-FY-BEG-DT-DD:** (PIC 9(02)) FY Begin Date - Day.
            *   **P-NEW-REPORT-DATE:** Report Date.
                *   **P-NEW-REPORT-DT-CC:** (PIC 9(02)) Report Date - Century/Code.
                *   **P-NEW-REPORT-DT-YY:** (PIC 9(02)) Report Date - Year.
                *   **P-NEW-REPORT-DT-MM:** (PIC 9(02)) Report Date - Month.
                *   **P-NEW-REPORT-DT-DD:** (PIC 9(02)) Report Date - Day.
            *   **P-NEW-TERMINATION-DATE:** Termination Date.
                *   **P-NEW-TERM-DT-CC:** (PIC 9(02)) Termination Date - Century/Code.
                *   **P-NEW-TERM-DT-YY:** (PIC 9(02)) Termination Date - Year.
                *   **P-NEW-TERM-DT-MM:** (PIC 9(02)) Termination Date - Month.
                *   **P-NEW-TERM-DT-DD:** (PIC 9(02)) Termination Date - Day.
        *   **P-NEW-WAIVER-CODE:** (PIC X(01)) Waiver Code.
            *   **P-NEW-WAIVER-STATE:** (VALUE 'Y') Waiver State.
        *   **P-NEW-INTER-NO:** (PIC 9(05)) Internal Number.
        *   **P-NEW-PROVIDER-TYPE:** (PIC X(02)) Provider Type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** (PIC 9(01)) Current Census Division.
        *   **P-NEW-CURRENT-DIV:** REDEFINES P-NEW-CURRENT-CENSUS-DIV.
        *   **P-NEW-MSA-DATA:** MSA Data.
            *   **P-NEW-CHG-CODE-INDEX:** (PIC X) Charge Code Index.
            *   **P-NEW-GEO-LOC-MSAX:** (PIC X(04)) Geographic Location MSA (Metropolitan Statistical Area)
            *   **P-NEW-GEO-LOC-MSA9:** REDEFINES P-NEW-GEO-LOC-MSAX.
            *   **P-NEW-WAGE-INDEX-LOC-MSA:** (PIC X(04)) Wage Index Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA:** (PIC X(04)) Standard Amount Location MSA.
            *   **P-NEW-STAND-AMT-LOC-MSA9:** REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                *   **P-NEW-RURAL-1ST:** Rural 1st.
                    *   **P-NEW-STAND-RURAL:** (PIC XX) Standard Rural.
                        *   **P-NEW-STD-RURAL-CHECK:** (VALUE '  ') Standard Rural Check.
                    *   **P-NEW-RURAL-2ND:** (PIC XX) Rural 2nd.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** (PIC XX) Sole Community Hospital Year.
        *   **P-NEW-LUGAR:** (PIC X) Lugar.
        *   **P-NEW-TEMP-RELIEF-IND:** (PIC X) Temporary Relief Indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** (PIC X) Federal PPS Blend Indicator.
        *   **FILLER:** (PIC X(05)) Filler.
    *   **PROV-NEWREC-HOLD2:** Provider Record Hold 2.
        *   **P-NEW-VARIABLES:** Variables.
            *   **P-NEW-FAC-SPEC-RATE:** (PIC 9(05)V9(02)) Facility Specific Rate.
            *   **P-NEW-COLA:** (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
            *   **P-NEW-INTERN-RATIO:** (PIC 9(01)V9(04)) Intern Ratio.
            *   **P-NEW-BED-SIZE:** (PIC 9(05)) Bed Size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** (PIC 9(01)V9(03)) Operating Cost to Charge Ratio.
            *   **P-NEW-CMI:** (PIC 9(01)V9(04)) CMI (Case Mix Index).
            *   **P-NEW-SSI-RATIO:** (PIC V9(04)) SSI Ratio.
            *   **P-NEW-MEDICAID-RATIO:** (PIC V9(04)) Medicaid Ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** (PIC 9(01)) PPS Blend Year Indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** (PIC 9(01)V9(05)) PRUF Update Factor.
            *   **P-NEW-DSH-PERCENT:** (PIC V9(04)) DSH (Disproportionate Share Hospital) Percent.
            *   **P-NEW-FYE-DATE:** (PIC X(08)) Fiscal Year End Date.
        *   **FILLER:** (PIC X(23)) Filler.
    *   **PROV-NEWREC-HOLD3:** Provider Record Hold 3.
        *   **P-NEW-PASS-AMT-DATA:** Pass Amount Data.
            *   **P-NEW-PASS-AMT-CAPITAL:** (PIC 9(04)V99) Capital Pass Through Amount.
            *   **P-NEW-PASS-AMT-DIR-MED-ED:** (PIC 9(04)V99)