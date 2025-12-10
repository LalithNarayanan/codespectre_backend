Here's an analysis of each COBOL program, detailing the files accessed, data structures, and their descriptions:

## Program: LTCAL032

**Files Accessed:**

*   **COPY LTDRG031:** This is a copybook (a file containing pre-written COBOL code) that's included in the program.  It likely contains DRG (Diagnosis Related Group) related data, such as relative weights and average lengths of stay.

**Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.**
    *   *Description:*  A descriptive field, likely for debugging or identification purposes.  It holds the program's name and a label indicating it's the working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.**
    *   *Description:*  Stores the version of the calculation logic used by the program.
*   **COPY LTDRG031:** (Included from the copybook)
    *   *Description:* This section contains data structures related to DRG codes.  The exact content depends on the `LTDRG031` copybook.
*   **01 HOLD-PPS-COMPONENTS.**
    *   *Description:* This group of data items is used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   **05 H-LOS PIC 9(03).**
            *   *Description:*  Length of stay (in days).
        *   **05 H-REG-DAYS PIC 9(03).**
            *   *Description:* Regular days (covered days minus LTR days).
        *   **05 H-TOTAL-DAYS PIC 9(05).**
            *   *Description:* Total days (regular days plus LTR days).
        *   **05 H-SSOT PIC 9(02).**
            *   *Description:* Short Stay Outlier Threshold.
        *   **05 H-BLEND-RTC PIC 9(02).**
            *   *Description:* Return code for Blending.
        *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
            *   *Description:* Blend Factor for Facility Rate.
        *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
            *   *Description:* Blend Factor for PPS.
        *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
            *   *Description:* Short Stay Payment Amount.
        *   **05 H-SS-COST PIC 9(07)V9(02).**
            *   *Description:* Short Stay Cost.
        *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
            *   *Description:* Labor Portion of the payment.
        *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
            *   *Description:* Non-Labor Portion of the payment.
        *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
            *   *Description:* Fixed Loss Amount.
        *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
            *   *Description:* New Facility Specific Rate.

**Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.**
    *   *Description:*  This is the main data structure passed *into* the program from the calling program.  It contains information about the bill being processed.
        *   **10 B-NPI10.**
            *   *Description:*  NPI (National Provider Identifier) information.
                *   **15 B-NPI8 PIC X(08).**
                    *   *Description:*  The 8-character NPI number.
                *   **15 B-NPI-FILLER PIC X(02).**
                    *   *Description:*  Filler for NPI.
        *   **10 B-PROVIDER-NO PIC X(06).**
            *   *Description:*  Provider Number.
        *   **10 B-PATIENT-STATUS PIC X(02).**
            *   *Description:*  Patient Status Code.
        *   **10 B-DRG-CODE PIC X(03).**
            *   *Description:*  The DRG code for the patient's stay.
        *   **10 B-LOS PIC 9(03).**
            *   *Description:* Length of Stay (in days).
        *   **10 B-COV-DAYS PIC 9(03).**
            *   *Description:* Covered Days.
        *   **10 B-LTR-DAYS PIC 9(02).**
            *   *Description:* Lifetime Reserve Days.
        *   **10 B-DISCHARGE-DATE.**
            *   *Description:*  Discharge Date.
                *   **15 B-DISCHG-CC PIC 9(02).**
                    *   *Description:* Century of the discharge date.
                *   **15 B-DISCHG-YY PIC 9(02).**
                    *   *Description:* Year of the discharge date (last two digits).
                *   **15 B-DISCHG-MM PIC 9(02).**
                    *   *Description:* Month of the discharge date.
                *   **15 B-DISCHG-DD PIC 9(02).**
                    *   *Description:* Day of the discharge date.
        *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
            *   *Description:* Covered Charges (dollar amount).
        *   **10 B-SPEC-PAY-IND PIC X(01).**
            *   *Description:* Special Payment Indicator (e.g., for outlier payments).
        *   **10 FILLER PIC X(13).**
            *   *Description:* Unused space.
*   **01 PPS-DATA-ALL.**
    *   *Description:* This structure is passed *back* to the calling program and contains the calculated PPS data.
        *   **05 PPS-RTC PIC 9(02).**
            *   *Description:* Return Code (indicating payment status, errors, etc.).
        *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).**
            *   *Description:* Charge Threshold.
        *   **05 PPS-DATA.**
            *   *Description:*  PPS-related data.
                *   **10 PPS-MSA PIC X(04).**
                    *   *Description:* MSA (Metropolitan Statistical Area) code.
                *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).**
                    *   *Description:* Wage Index.
                *   **10 PPS-AVG-LOS PIC 9(02)V9(01).**
                    *   *Description:* Average Length of Stay for the DRG.
                *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).**
                    *   *Description:* Relative Weight for the DRG.
                *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Outlier Payment Amount.
                *   **10 PPS-LOS PIC 9(03).**
                    *   *Description:* Length of Stay.
                *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* DRG Adjusted Payment Amount.
                *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Federal Payment Amount.
                *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Final Payment Amount.
                *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).**
                    *   *Description:* Facility Costs.
                *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).**
                    *   *Description:* New Facility Specific Rate.
                *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).**
                    *   *Description:* Outlier Threshold.
                *   **10 PPS-SUBM-DRG-CODE PIC X(03).**
                    *   *Description:* Submitted DRG Code.
                *   **10 PPS-CALC-VERS-CD PIC X(05).**
                    *   *Description:* Calculation Version Code.
                *   **10 PPS-REG-DAYS-USED PIC 9(03).**
                    *   *Description:* Regular Days Used.
                *   **10 PPS-LTR-DAYS-USED PIC 9(03).**
                    *   *Description:* Lifetime Reserve Days Used.
                *   **10 PPS-BLEND-YEAR PIC 9(01).**
                    *   *Description:* Blend Year.
                *   **10 PPS-COLA PIC 9(01)V9(03).**
                    *   *Description:* Cost of Living Adjustment.
                *   **10 FILLER PIC X(04).**
                    *   *Description:* Unused space.
        *   **05 PPS-OTHER-DATA.**
            *   *Description:* Other PPS data.
                *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).**
                    *   *Description:* National Labor Percentage.
                *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).**
                    *   *Description:* National Non-Labor Percentage.
                *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).**
                    *   *Description:* Standard Federal Rate.
                *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).**
                    *   *Description:* Budget Neutrality Rate.
                *   **10 FILLER PIC X(20).**
                    *   *Description:* Unused space.
        *   **05 PPS-PC-DATA.**
            *   *Description:* PPS related data.
                *   **10 PPS-COT-IND PIC X(01).**
                    *   *Description:* Cost Outlier Indicator.
                *   **10 FILLER PIC X(20).**
                    *   *Description:* Unused space.
*   **01 PRICER-OPT-VERS-SW.**
    *   *Description:*  Switch to indicate which versions of tables are passed back.
        *   **05 PRICER-OPTION-SW PIC X(01).**
            *   *Description:*  Option switch.
                *   **88 ALL-TABLES-PASSED VALUE 'A'.**
                    *   *Description:*  Condition name: All tables passed.
                *   **88 PROV-RECORD-PASSED VALUE 'P'.**
                    *   *Description:*  Condition name: Provider record passed.
        *   **05 PPS-VERSIONS.**
            *   *Description:*  PPS Version.
                *   **10 PPDRV-VERSION PIC X(05).**
                    *   *Description:*  Version of the PPDRV program.
*   **01 PROV-NEW-HOLD.**
    *   *Description:*  Provider record information passed back.
        *   **02 PROV-NEWREC-HOLD1.**
            *   *Description:*  Provider record hold area 1.
                *   **05 P-NEW-NPI10.**
                    *   *Description:*  New NPI Information.
                        *   **10 P-NEW-NPI8 PIC X(08).**
                            *   *Description:*  New NPI 8 character.
                        *   **10 P-NEW-NPI-FILLER PIC X(02).**
                            *   *Description:*  Filler for NPI.
                *   **05 P-NEW-PROVIDER-NO.**
                    *   *Description:*  New Provider Number.
                        *   **10 P-NEW-STATE PIC 9(02).**
                            *   *Description:*  New State.
                        *   **10 FILLER PIC X(04).**
                            *   *Description:*  Filler.
                *   **05 P-NEW-DATE-DATA.**
                    *   *Description:*  Date data.
                        *   **10 P-NEW-EFF-DATE.**
                            *   *Description:*  Effective Date.
                                *   **15 P-NEW-EFF-DT-CC PIC 9(02).**
                                    *   *Description:*  Century.
                                *   **15 P-NEW-EFF-DT-YY PIC 9(02).**
                                    *   *Description:*  Year.
                                *   **15 P-NEW-EFF-DT-MM PIC 9(02).**
                                    *   *Description:*  Month.
                                *   **15 P-NEW-EFF-DT-DD PIC 9(02).**
                                    *   *Description:*  Day.
                        *   **10 P-NEW-FY-BEGIN-DATE.**
                            *   *Description:*  Fiscal Year Begin Date.
                                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).**
                                    *   *Description:*  Century.
                                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).**
                                    *   *Description:*  Year.
                                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).**
                                    *   *Description:*  Month.
                                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).**
                                    *   *Description:*  Day.
                        *   **10 P-NEW-REPORT-DATE.**
                            *   *Description:*  Report Date.
                                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).**
                                    *   *Description:*  Century.
                                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).**
                                    *   *Description:*  Year.
                                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).**
                                    *   *Description:*  Month.
                                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).**
                                    *   *Description:*  Day.
                        *   **10 P-NEW-TERMINATION-DATE.**
                            *   *Description:*  Termination Date.
                                *   **15 P-NEW-TERM-DT-CC PIC 9(02).**
                                    *   *Description:*  Century.
                                *   **15 P-NEW-TERM-DT-YY PIC 9(02).**
                                    *   *Description:*  Year.
                                *   **15 P-NEW-TERM-DT-MM PIC 9(02).**
                                    *   *Description:*  Month.
                                *   **15 P-NEW-TERM-DT-DD PIC 9(02).**
                                    *   *Description:*  Day.
                *   **05 P-NEW-WAIVER-CODE PIC X(01).**
                    *   *Description:*  Waiver Code.
                        *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.**
                            *   *Description:*  Condition name: Waiver State is 'Y'.
                *   **05 P-NEW-INTER-NO PIC 9(05).**
                    *   *Description:*  Intern Number.
                *   **05 P-NEW-PROVIDER-TYPE PIC X(02).**
                    *   *Description:*  Provider Type.
                *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
                    *   *Description:*  Current Census Division.
                *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
                    *   *Description:*  Redefines the same memory location as P-NEW-CURRENT-CENSUS-DIV.
                *   **05 P-NEW-MSA-DATA.**
                    *   *Description:*  MSA data.
                        *   **10 P-NEW-CHG-CODE-INDEX PIC X.**
                            *   *Description:*  Charge Code Index.
                        *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.**
                            *   *Description:*  Geographic Location MSA.
                        *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).**
                            *   *Description:*  Redefines the same memory location as P-NEW-GEO-LOC-MSAX.
                        *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.**
                            *   *Description:*  Wage Index Location MSA.
                        *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.**
                            *   *Description:*  Standard Amount Location MSA.
                        *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.**
                            *   *Description:*  Redefines the same memory location as P-NEW-STAND-AMT-LOC-MSA.
                                *   **15 P-NEW-RURAL-1ST.**
                                    *   *Description:*  Rural 1st.
                                        *   **20 P-NEW-STAND-RURAL PIC XX.**
                                            *   *Description:*  Standard Rural.
                                                *   **88 P-NEW-STD-RURAL-CHECK VALUE ' '.**
                                                    *   *Description:*  Condition name: Standard Rural Check.
                                *   **15 P-NEW-RURAL-2ND PIC XX.**
                                    *   *Description:*  Rural 2nd.
                *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.**
                    *   *Description:*  Sole Community Dependent Hospital Year.
                *   **05 P-NEW-LUGAR PIC X.**
                    *   *Description:*  Lugar.
                *   **05 P-NEW-TEMP-RELIEF-IND PIC X.**
                    *   *Description:*  Temporary Relief Indicator.
                *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.**
                    *   *Description:*  Federal PPS Blend Indicator.
                *   **05 FILLER PIC X(05).**
                    *   *Description:*  Filler.
        *   **02 PROV-NEWREC-HOLD2.**
            *   *Description:*  Provider record hold area 2.
                *   **05 P-NEW-VARIABLES.**
                    *   *Description:*  New Variables.
                        *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
                            *   *Description:*  New Facility Specific Rate.
                        *   **10 P-NEW-COLA PIC 9(01)V9(03).**
                            *   *Description:*  Cost of Living Adjustment.
                        *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).**
                            *   *Description:*  Intern Ratio.
                        *   **10 P-NEW-BED-SIZE PIC 9(05).**
                            *   *Description:*  Bed Size.
                        *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).**
                            *   *Description:*  Operating Cost to Charge Ratio.
                        *   **10 P-NEW-CMI PIC 9(01)V9(04).**
                            *   *Description:*  Case Mix Index.
                        *   **10 P-NEW-SSI-RATIO PIC V9(04).**
                            *   *Description:*  SSI Ratio.
                        *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).**
                            *   *Description:*  Medicaid Ratio.
                        *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).**
                            *   *Description:*  PPS Blend Year Indicator.
                        *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).**
                            *   *Description:*  PRUF Update Factor.
                        *   **10 P-NEW-DSH-PERCENT PIC V9(04).**
                            *   *Description:*  DSH (Disproportionate Share Hospital) Percentage.
                        *   **10 P-NEW-FYE-DATE PIC X(08).**
                            *   *Description:*  Fiscal Year End Date.
                *   **05 FILLER PIC X(23).**
                    *   *Description:*  Filler.
        *   **02 PROV-NEWREC-HOLD3.**
            *   *Description:*  Provider record hold area 3.
                *   **05 P-NEW-PASS-AMT-DATA.**
                    *   *Description:*  Pass Through Amount Data.
                        *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.**
                            *   *Description:*  Pass Through Amount for Capital.
                        *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.**
                            *   *Description:*  Pass Through Amount for Direct Medical Education.
                        *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.**
                            *   *Description:*  Pass Through Amount for Organ Acquisition.
                        *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.**
                            *   *Description:*  Pass Through Amount for Plus Miscellaneous.
                *   **05 P-NEW-CAPI-DATA.**
                    *   *Description:*  Capital Data.
                        *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X.**
                            *   *Description:*  Capital PPS Pay Code.
                        *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.**
                            *   *Description:*  Capital Hospital Specific Rate.
                        *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.**
                            *   *Description:*  Capital Old Harm Rate.
                        *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.**
                            *   *Description:*  Capital New Harm Ratio.
                        *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.**
                            *   *Description:*  Capital Cost to Charge Ratio.
                        *   **15 P-NEW-CAPI-NEW-HOSP PIC X.**
                            *   *Description:*  Capital New Hospital.
                        *   **15 P-NEW-CAPI-IME PIC 9V9999.**
                            *   *Description:*  Capital IME (Indirect Medical Education).
                        *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.**
                            *   *Description:*  Capital Exceptions.
                *   **05 FILLER PIC X(22).**
                    *   *Description:*  Filler.
*   **01 WAGE-NEW-INDEX-RECORD.**
    *   *Description:*  Wage Index record to be passed.
        *   **05 W-MSA PIC X(4).**
            *   *Description:*  MSA (Metropolitan Statistical Area) code.
        *   **05 W-EFF-DATE PIC X(8).**
            *   *Description:*  Effective Date.
        *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04).**
            *   *Description:*  Wage Index 1.
        *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04).**
            *   *Description:*  Wage Index 2.
        *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04).**
            *   *Description:*  Wage Index 3.

## Program: LTCAL042

**Files Accessed:**

*   **COPY LTDRG031:**  A copybook containing DRG-related data.

**Data Structures in WORKING-STORAGE SECTION:**

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.**
    *   *Description:*  A descriptive field, likely for debugging or identification purposes.  It holds the program's name and a label indicating it's the working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.**
    *   *Description:*  Stores the version of the calculation logic used by the program.
*   **COPY LTDRG031:** (Included from the copybook)
    *   *Description:* This section contains data structures related to DRG codes.  The exact content depends on the `LTDRG031` copybook.
*   **01 HOLD-PPS-COMPONENTS.**
    *   *Description:* This group of data items is used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
        *   **05 H-LOS PIC 9(03).**
            *   *Description:*  Length of stay (in days).
        *   **05 H-REG-DAYS PIC 9(03).**
            *   *Description:* Regular days (covered days minus LTR days).
        *   **05 H-TOTAL-DAYS PIC 9(05).**
            *   *Description:* Total days (regular days plus LTR days).
        *   **05 H-SSOT PIC 9(02).**
            *   *Description:* Short Stay Outlier Threshold.
        *   **05 H-BLEND-RTC PIC 9(02).**
            *   *Description:* Return code for Blending.
        *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
            *   *Description:* Blend Factor for Facility Rate.
        *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
            *   *Description:* Blend Factor for PPS.
        *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
            *   *Description:* Short Stay Payment Amount.
        *   **05 H-SS-COST PIC 9(07)V9(02).**
            *   *Description:* Short Stay Cost.
        *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
            *   *Description:* Labor Portion of the payment.
        *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
            *   *Description:* Non-Labor Portion of the payment.
        *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
            *   *Description:* Fixed Loss Amount.
        *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
            *   *Description:* New Facility Specific Rate.
        *   **05 H-LOS-RATIO PIC 9(01)V9(05).**
            *   *Description:* Ratio of Length of Stay.

**Data Structures in LINKAGE SECTION:**

*   **01 BILL-NEW-DATA.**
    *   *Description:*  This is the main data structure passed *into* the program from the calling program.  It contains information about the bill being processed.
        *   **10 B-NPI10.**
            *   *Description:*  NPI (National Provider Identifier) information.
                *   **15 B-NPI8 PIC X(08).**
                    *   *Description:*  The 8-character NPI number.
                *   **15 B-NPI-FILLER PIC X(02).**
                    *   *Description:*  Filler for NPI.
        *   **10 B-PROVIDER-NO PIC X(06).**
            *   *Description:*  Provider Number.
        *   **10 B-PATIENT-STATUS PIC X(02).**
            *   *Description:*  Patient Status Code.
        *   **10 B-DRG-CODE PIC X(03).**
            *   *Description:*  The DRG code for the patient's stay.
        *   **10 B-LOS PIC 9(03).**
            *   *Description:* Length of Stay (in days).
        *   **10 B-COV-DAYS PIC 9(03).**
            *   *Description:* Covered Days.
        *   **10 B-LTR-DAYS PIC 9(02).**
            *   *Description:* Lifetime Reserve Days.
        *   **10 B-DISCHARGE-DATE.**
            *   *Description:*  Discharge Date.
                *   **15 B-DISCHG-CC PIC 9(02).**
                    *   *Description:* Century of the discharge date.
                *   **15 B-DISCHG-YY PIC 9(02).**
                    *   *Description:* Year of the discharge date (last two digits).
                *   **15 B-DISCHG-MM PIC 9(02).**
                    *   *Description:* Month of the discharge date.
                *   **15 B-DISCHG-DD PIC 9(02).**
                    *   *Description:* Day of the discharge date.
        *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
            *   *Description:* Covered Charges (dollar amount).
        *   **10 B-SPEC-PAY-IND PIC X(01).**
            *   *Description:* Special Payment Indicator (e.g., for outlier payments).
        *   **10 FILLER PIC X(13).**
            *   *Description:* Unused space.
*   **01 PPS-DATA-ALL.**
    *   *Description:* This structure is passed *back* to the calling program and contains the calculated PPS data.
        *   **05 PPS-RTC PIC 9(02).**
            *   *Description:* Return Code (indicating payment status, errors, etc.).
        *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).**
            *   *Description:* Charge Threshold.
        *   **05 PPS-DATA.**
            *   *Description:*  PPS-related data.
                *   **10 PPS-MSA PIC X(04).**
                    *   *Description:* MSA (Metropolitan Statistical Area) code.
                *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).**
                    *   *Description:* Wage Index.
                *   **10 PPS-AVG-LOS PIC 9(02)V9(01).**
                    *   *Description:* Average Length of Stay for the DRG.
                *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).**
                    *   *Description:* Relative Weight for the DRG.
                *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Outlier Payment Amount.
                *   **10 PPS-LOS PIC 9(03).**
                    *   *Description:* Length of Stay.
                *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* DRG Adjusted Payment Amount.
                *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Federal Payment Amount.
                *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).**
                    *   *Description:* Final Payment Amount.
                *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).**
                    *   *Description:* Facility Costs.
                *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).**
                    *   *Description:* New Facility Specific Rate.
                *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).**
                    *   *Description:* Outlier Threshold.
                *   **10 PPS-SUBM-DRG-CODE PIC X(03).**
                    *   *Description:* Submitted DRG Code.
                *   **10 PPS-CALC-VERS-CD PIC X(05).**
                    *   *Description:* Calculation Version Code.
                *   **10 PPS-REG-DAYS-USED PIC 9(03).**
                    *   *Description:* Regular Days Used.
                *   **10 PPS-LTR-DAYS-USED PIC 9(03).**
                    *   *Description:* Lifetime Reserve Days Used.
                *   **10 PPS-BLEND-YEAR PIC 9(01).**
                    *   *Description:* Blend Year.
                *   **10 PPS-COLA PIC 9(01)V9(03).**
                    *   *Description:* Cost of Living Adjustment.
                *   **10 FILLER PIC