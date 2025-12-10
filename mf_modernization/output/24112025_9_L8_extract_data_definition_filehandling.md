Here's an analysis of the provided COBOL programs, formatted in markdown:

## Program: LTCAL032

### Files Accessed and Descriptions:

*   **COPY LTDRG031:** This is a copybook included in the program. It likely contains data structures or code related to DRG (Diagnosis Related Group) information, specific to the FY2003 LTC-DRG.
*   No other files are explicitly accessed in the provided code.

### Data Structures in WORKING-STORAGE SECTION:

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.**
    *   Description: A character field used for internal reference or identification of the working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.**
    *   Description:  A character field storing the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS:** (Defined in COPY LTDRG031)
    *   Description: A group of fields used to hold various components related to the Prospective Payment System (PPS) calculations.  The fields include:
        *   **05 H-LOS PIC 9(03):**  Length of Stay (LOS).
        *   **05 H-REG-DAYS PIC 9(03):** Regular Days.
        *   **05 H-TOTAL-DAYS PIC 9(05):** Total Days.
        *   **05 H-SSOT PIC 9(02):**  Short Stay Outlier Threshold.
        *   **05 H-BLEND-RTC PIC 9(02):** Blend Rate Type Code.
        *   **05 H-BLEND-FAC PIC 9(01)V9(01):** Blend Facility Rate.
        *   **05 H-BLEND-PPS PIC 9(01)V9(01):** Blend PPS Rate.
        *   **05 H-SS-PAY-AMT PIC 9(07)V9(02):** Short Stay Payment Amount.
        *   **05 H-SS-COST PIC 9(07)V9(02):** Short Stay Cost.
        *   **05 H-LABOR-PORTION PIC 9(07)V9(06):** Labor Portion.
        *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06):** Non-Labor Portion.
        *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02):** Fixed Loss Amount.
        *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02):** New Facility Specific Rate.

### Data Structures in LINKAGE SECTION:

*   **01 BILL-NEW-DATA:**
    *   Description:  This data structure represents the input bill data passed to the program.
        *   **10 B-NPI10:**
            *   **15 B-NPI8 PIC X(08):**  NPI (National Provider Identifier) - first 8 characters.
            *   **15 B-NPI-FILLER PIC X(02):** NPI - filler characters.
        *   **10 B-PROVIDER-NO PIC X(06):** Provider Number.
        *   **10 B-PATIENT-STATUS PIC X(02):** Patient Status.
        *   **10 B-DRG-CODE PIC X(03):** DRG Code.
        *   **10 B-LOS PIC 9(03):** Length of Stay.
        *   **10 B-COV-DAYS PIC 9(03):** Covered Days.
        *   **10 B-LTR-DAYS PIC 9(02):** Lifetime Reserve Days.
        *   **10 B-DISCHARGE-DATE:**
            *   **15 B-DISCHG-CC PIC 9(02):** Discharge Date - Century/Code.
            *   **15 B-DISCHG-YY PIC 9(02):** Discharge Date - Year.
            *   **15 B-DISCHG-MM PIC 9(02):** Discharge Date - Month.
            *   **15 B-DISCHG-DD PIC 9(02):** Discharge Date - Day.
        *   **10 B-COV-CHARGES PIC 9(07)V9(02):** Covered Charges.
        *   **10 B-SPEC-PAY-IND PIC X(01):** Special Payment Indicator.
        *   **10 FILLER PIC X(13):** Unused filler space.
*   **01 PPS-DATA-ALL:**
    *   Description: This data structure is used to pass calculated PPS data back to the calling program.
        *   **05 PPS-RTC PIC 9(02):**  PPS Return Code.
        *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02):** PPS Charge Threshold.
        *   **05 PPS-DATA:**
            *   **10 PPS-MSA PIC X(04):**  MSA (Metropolitan Statistical Area) Code.
            *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04):** PPS Wage Index.
            *   **10 PPS-AVG-LOS PIC 9(02)V9(01):** PPS Average Length of Stay.
            *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04):** PPS Relative Weight.
            *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02):** PPS Outlier Payment Amount.
            *   **10 PPS-LOS PIC 9(03):** PPS Length of Stay.
            *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02):** PPS DRG Adjusted Payment Amount.
            *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02):** PPS Federal Payment Amount.
            *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02):** PPS Final Payment Amount.
            *   **10 PPS-FAC-COSTS PIC 9(07)V9(02):** PPS Facility Costs.
            *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02):** PPS New Facility Specific Rate.
            *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02):** PPS Outlier Threshold.
            *   **10 PPS-SUBM-DRG-CODE PIC X(03):** Submitted DRG Code.
            *   **10 PPS-CALC-VERS-CD PIC X(05):**  Calculation Version Code.
            *   **10 PPS-REG-DAYS-USED PIC 9(03):** Regular Days Used for PPS calculation.
            *   **10 PPS-LTR-DAYS-USED PIC 9(03):** Lifetime Reserve Days Used for PPS calculation.
            *   **10 PPS-BLEND-YEAR PIC 9(01):** Blend Year.
            *   **10 PPS-COLA PIC 9(01)V9(03):** COLA (Cost of Living Adjustment).
            *   **10 FILLER PIC X(04):** Filler.
        *   **05 PPS-OTHER-DATA:**
            *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05):** National Labor Percentage.
            *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05):** National Non-Labor Percentage.
            *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02):** Standard Federal Rate.
            *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03):** Budget Neutrality Rate.
            *   **10 FILLER PIC X(20):** Filler.
        *   **05 PPS-PC-DATA:**
            *   **10 PPS-COT-IND PIC X(01):** COT (Cost Outlier Threshold) Indicator.
            *   **10 FILLER PIC X(20):** Filler.
*   **01 PRICER-OPT-VERS-SW:**
    *   Description:  This data structure is used to pass the Pricer option switch.
        *   **05 PRICER-OPTION-SW PIC X(01):** Pricer Option Switch.
            *   **88 ALL-TABLES-PASSED VALUE 'A':** Indicates all tables are passed.
            *   **88 PROV-RECORD-PASSED VALUE 'P':** Indicates provider record is passed.
        *   **05 PPS-VERSIONS:**
            *   **10 PPDRV-VERSION PIC X(05):**  Version of the PPDRV (likely a related program).
*   **01 PROV-NEW-HOLD:**
    *   Description: This data structure represents the provider record passed to the program.
        *   **02 PROV-NEWREC-HOLD1:**
            *   **05 P-NEW-NPI10:**
                *   **10 P-NEW-NPI8 PIC X(08):** New NPI - First 8 characters.
                *   **10 P-NEW-NPI-FILLER PIC X(02):** New NPI - Filler.
            *   **05 P-NEW-PROVIDER-NO:**
                *   **10 P-NEW-STATE PIC 9(02):** New State.
                *   **10 FILLER PIC X(04):** Filler.
            *   **05 P-NEW-DATE-DATA:**
                *   **10 P-NEW-EFF-DATE:**
                    *   **15 P-NEW-EFF-DT-CC PIC 9(02):** New Effective Date - Century/Code.
                    *   **15 P-NEW-EFF-DT-YY PIC 9(02):** New Effective Date - Year.
                    *   **15 P-NEW-EFF-DT-MM PIC 9(02):** New Effective Date - Month.
                    *   **15 P-NEW-EFF-DT-DD PIC 9(02):** New Effective Date - Day.
                *   **10 P-NEW-FY-BEGIN-DATE:**
                    *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02):** New Fiscal Year Begin Date - Century/Code.
                    *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02):** New Fiscal Year Begin Date - Year.
                    *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02):** New Fiscal Year Begin Date - Month.
                    *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02):** New Fiscal Year Begin Date - Day.
                *   **10 P-NEW-REPORT-DATE:**
                    *   **15 P-NEW-REPORT-DT-CC PIC 9(02):** New Report Date - Century/Code.
                    *   **15 P-NEW-REPORT-DT-YY PIC 9(02):** New Report Date - Year.
                    *   **15 P-NEW-REPORT-DT-MM PIC 9(02):** New Report Date - Month.
                    *   **15 P-NEW-REPORT-DT-DD PIC 9(02):** New Report Date - Day.
                *   **10 P-NEW-TERMINATION-DATE:**
                    *   **15 P-NEW-TERM-DT-CC PIC 9(02):** New Termination Date - Century/Code.
                    *   **15 P-NEW-TERM-DT-YY PIC 9(02):** New Termination Date - Year.
                    *   **15 P-NEW-TERM-DT-MM PIC 9(02):** New Termination Date - Month.
                    *   **15 P-NEW-TERM-DT-DD PIC 9(02):** New Termination Date - Day.
            *   **05 P-NEW-WAIVER-CODE PIC X(01):** New Waiver Code.
                *   **88 P-NEW-WAIVER-STATE VALUE 'Y':** Indicates Waiver State.
            *   **05 P-NEW-INTER-NO PIC 9(05):** New Internal Number.
            *   **05 P-NEW-PROVIDER-TYPE PIC X(02):** New Provider Type.
            *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01):** New Current Census Division.
            *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01):**  Redefines the census division.
            *   **05 P-NEW-MSA-DATA:**
                *   **10 P-NEW-CHG-CODE-INDEX PIC X:** New Charge Code Index.
                *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT:** New Geographic Location MSA - Right justified.
                *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04):** Redefines the geographic location as numeric.
                *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT:** New Wage Index Location MSA - Right justified.
                *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT:** New Standard Amount Location MSA - Right justified.
                *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**  Redefines the standard amount as numeric.
                    *   **15 P-NEW-RURAL-1ST:**
                        *   **20 P-NEW-STAND-RURAL PIC XX:** New Rural Standard.
                            *   **88 P-NEW-STD-RURAL-CHECK VALUE '  ':** Rural Check
                        *   **15 P-NEW-RURAL-2ND PIC XX:** New Rural Second.
            *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX:** New SOL Com Dep Hosp Year.
            *   **05 P-NEW-LUGAR PIC X:** New Lugar.
            *   **05 P-NEW-TEMP-RELIEF-IND PIC X:** New Temporary Relief Indicator.
            *   **05 P-NEW-FED-PPS-BLEND-IND PIC X:** New Federal PPS Blend Indicator.
            *   **05 FILLER PIC X(05):** Filler.
        *   **02 PROV-NEWREC-HOLD2:**
            *   **05 P-NEW-VARIABLES:**
                *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02):** New Facility Specific Rate.
                *   **10 P-NEW-COLA PIC 9(01)V9(03):** New COLA.
                *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04):** New Intern Ratio.
                *   **10 P-NEW-BED-SIZE PIC 9(05):** New Bed Size.
                *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03):** New Operating Cost-to-Charge Ratio.
                *   **10 P-NEW-CMI PIC 9(01)V9(04):** New CMI.
                *   **10 P-NEW-SSI-RATIO PIC V9(04):** New SSI Ratio.
                *   **10 P-NEW-MEDICAID-RATIO PIC V9(04):** New Medicaid Ratio.
                *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01):** New PPS Blend Year Indicator.
                *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05):** New PRUF Update Factor.
                *   **10 P-NEW-DSH-PERCENT PIC V9(04):** New DSH Percent.
                *   **10 P-NEW-FYE-DATE PIC X(08):** New FYE Date.
            *   **05 FILLER PIC X(23):** Filler.
        *   **02 PROV-NEWREC-HOLD3:**
            *   **05 P-NEW-PASS-AMT-DATA:**
                *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99:** New Pass Amount Capital.
                *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99:** New Pass Amount Direct Med Ed.
                *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99:** New Pass Amount Organ Acquisition.
                *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99:** New Pass Amount Plus Misc.
            *   **05 P-NEW-CAPI-DATA:**
                *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X:** New Capi PPS Pay Code.
                *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99:** New Capi Hosp Specific Rate.
                *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99:** New Capi Old Harm Rate.
                *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999:** New Capi New Harm Ratio.
                *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999:** New Capi Cost/Charge Ratio.
                *   **15 P-NEW-CAPI-NEW-HOSP PIC X:** New Capi New Hosp.
                *   **15 P-NEW-CAPI-IME PIC 9V9999:** New Capi IME.
                *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99:** New Capi Exceptions.
            *   **05 FILLER PIC X(22):** Filler.
*   **01 WAGE-NEW-INDEX-RECORD:**
    *   Description: This data structure represents the wage index record passed to the program.
        *   **05 W-MSA PIC X(4):** MSA Code.
        *   **05 W-EFF-DATE PIC X(8):** Effective Date.
        *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04):** Wage Index 1.
        *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04):** Wage Index 2.
        *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04):** Wage Index 3.

## Program: LTCAL042

### Files Accessed and Descriptions:

*   **COPY LTDRG031:** This is a copybook included in the program. It likely contains data structures or code related to DRG (Diagnosis Related Group) information, specific to the FY2003 LTC-DRG.
*   No other files are explicitly accessed in the provided code.

### Data Structures in WORKING-STORAGE SECTION:

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.**
    *   Description: A character field used for internal reference or identification of the working storage area.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.**
    *   Description:  A character field storing the version number of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS:** (Defined in COPY LTDRG031)
    *   Description: A group of fields used to hold various components related to the Prospective Payment System (PPS) calculations.  The fields include:
        *   **05 H-LOS PIC 9(03):**  Length of Stay (LOS).
        *   **05 H-REG-DAYS PIC 9(03):** Regular Days.
        *   **05 H-TOTAL-DAYS PIC 9(05):** Total Days.
        *   **05 H-SSOT PIC 9(02):**  Short Stay Outlier Threshold.
        *   **05 H-BLEND-RTC PIC 9(02):** Blend Rate Type Code.
        *   **05 H-BLEND-FAC PIC 9(01)V9(01):** Blend Facility Rate.
        *   **05 H-BLEND-PPS PIC 9(01)V9(01):** Blend PPS Rate.
        *   **05 H-SS-PAY-AMT PIC 9(07)V9(02):** Short Stay Payment Amount.
        *   **05 H-SS-COST PIC 9(07)V9(02):** Short Stay Cost.
        *   **05 H-LABOR-PORTION PIC 9(07)V9(06):** Labor Portion.
        *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06):** Non-Labor Portion.
        *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02):** Fixed Loss Amount.
        *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02):** New Facility Specific Rate.
        *   **05 H-LOS-RATIO PIC 9(01)V9(05):** LOS Ratio.

### Data Structures in LINKAGE SECTION:

*   **01 BILL-NEW-DATA:**
    *   Description:  This data structure represents the input bill data passed to the program.
        *   **10 B-NPI10:**
            *   **15 B-NPI8 PIC X(08):**  NPI (National Provider Identifier) - first 8 characters.
            *   **15 B-NPI-FILLER PIC X(02):** NPI - filler characters.
        *   **10 B-PROVIDER-NO PIC X(06):** Provider Number.
        *   **10 B-PATIENT-STATUS PIC X(02):** Patient Status.
        *   **10 B-DRG-CODE PIC X(03):** DRG Code.
        *   **10 B-LOS PIC 9(03):** Length of Stay.
        *   **10 B-COV-DAYS PIC 9(03):** Covered Days.
        *   **10 B-LTR-DAYS PIC 9(02):** Lifetime Reserve Days.
        *   **10 B-DISCHARGE-DATE:**
            *   **15 B-DISCHG-CC PIC 9(02):** Discharge Date - Century/Code.
            *   **15 B-DISCHG-YY PIC 9(02):** Discharge Date - Year.
            *   **15 B-DISCHG-MM PIC 9(02):** Discharge Date - Month.
            *   **15 B-DISCHG-DD PIC 9(02):** Discharge Date - Day.
        *   **10 B-COV-CHARGES PIC 9(07)V9(02):** Covered Charges.
        *   **10 B-SPEC-PAY-IND PIC X(01):** Special Payment Indicator.
        *   **10 FILLER PIC X(13):** Unused filler space.
*   **01 PPS-DATA-ALL:**
    *   Description: This data structure is used to pass calculated PPS data back to the calling program.
        *   **05 PPS-RTC PIC 9(02):**  PPS Return Code.
        *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02):** PPS Charge Threshold.
        *   **05 PPS-DATA:**
            *   **10 PPS-MSA PIC X(04):**  MSA (Metropolitan Statistical Area) Code.
            *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04):** PPS Wage Index.
            *   **10 PPS-AVG-LOS PIC 9(02)V9(01):** PPS Average Length of Stay.
            *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04):** PPS Relative Weight.
            *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02):** PPS Outlier Payment Amount.
            *   **10 PPS-LOS PIC 9(03):** PPS Length of Stay.
            *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02):** PPS DRG Adjusted Payment Amount.
            *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02):** PPS Federal Payment Amount.
            *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02):** PPS Final Payment Amount.
            *   **10 PPS-FAC-COSTS PIC 9(07)V9(02):** PPS Facility Costs.
            *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02):** PPS New Facility Specific Rate.
            *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02):** PPS Outlier Threshold.
            *   **10 PPS-SUBM-DRG-CODE PIC X(03):** Submitted DRG Code.
            *   **10 PPS-CALC-VERS-CD PIC X(05):**  Calculation Version Code.
            *   **10 PPS-REG-DAYS-USED PIC 9(03):** Regular Days Used for PPS calculation.
            *   **10 PPS-LTR-DAYS-USED PIC 9(03):** Lifetime Reserve Days Used for PPS calculation.
            *   **10 PPS-BLEND-YEAR PIC 9(01):** Blend Year.
            *   **10 PPS-COLA PIC 9(01)V9(03):** COLA (Cost of Living Adjustment).
            *   **10 FILLER PIC X(04):** Filler.
        *   **05 PPS-OTHER-DATA:**
            *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05):** National Labor Percentage.
            *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05):** National Non-Labor Percentage.
            *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02):** Standard Federal Rate.
            *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03):** Budget Neutrality Rate.
            *   **10 FILLER PIC X(20):** Filler.
        *   **05 PPS-PC-DATA:**
            *   **10 PPS-COT-IND PIC X(01):** COT (Cost Outlier Threshold) Indicator.
            *   **10 FILLER PIC X(20):** Filler.
*   **01 PRICER-OPT-VERS-SW:**
    *   Description:  This data structure is used to pass the Pricer option switch.
        *   **05 PRICER-OPTION-SW PIC X(01):** Pricer Option Switch.
            *   **88 ALL-TABLES-PASSED VALUE 'A':** Indicates all tables are passed.
            *   **88 PROV-RECORD-PASSED VALUE 'P':** Indicates provider record is passed.
        *   **05 PPS-VERSIONS:**
            *   **10 PPDRV-VERSION PIC X(05):**  Version of the PPDRV (likely a related program).
*   **01 PROV-NEW-HOLD:**
    *   Description: This data structure represents the provider record passed to the program.
        *   **02 PROV-NEWREC-HOLD1:**
            *   **05 P-NEW-NPI10:**
                *   **10 P-NEW-NPI8 PIC X(08):** New NPI - First 8 characters.
                *   **10 P-NEW-NPI-FILLER PIC X(02):** New NPI - Filler.
            *   **05 P-NEW-PROVIDER-NO:**
                *   **10 P-NEW-STATE PIC 9(02):** New State.
                *   **10 FILLER PIC X(04):** Filler.
            *   **05 P-NEW-DATE-DATA:**
                *   **10 P-NEW-EFF-DATE:**
                    *   **15 P-NEW-EFF-DT-CC PIC 9(02):** New Effective Date - Century/Code.
                    *   **15 P-NEW-EFF-DT-YY PIC 9(02):** New Effective Date - Year.
                    *   **15 P-NEW-EFF-DT-MM PIC 9(02):** New Effective Date - Month.
                    *   **15 P-NEW-EFF-DT-DD PIC 9(02):** New Effective Date - Day.
                *   **10 P-NEW-FY-BEGIN-DATE:**
                    *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02):** New Fiscal Year Begin Date - Century/Code.
                    *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02):** New Fiscal Year Begin Date - Year.
                    *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02):** New Fiscal Year Begin Date - Month.
                    *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02):** New Fiscal Year Begin Date - Day.
                *   **10 P-NEW-REPORT-DATE:**
                    *   **15 P-NEW-REPORT-DT-CC PIC 9(02):** New Report Date - Century/Code.
                    *   **15 P-NEW-REPORT-DT-YY PIC 9(02):** New Report Date - Year.
                    *   **15 P-NEW-REPORT-DT-MM PIC 9(02):** New Report Date - Month.
                    *   **15 P-NEW-REPORT-DT-DD PIC 9(02):** New Report Date - Day.
                *   **10 P-NEW-TERMINATION-DATE:**
                    *   **15 P-NEW-TERM-DT-CC PIC 9(02):** New Termination Date - Century/Code.
                    *   **15 P-NEW-TERM-DT-YY PIC 9(02):** New Termination Date - Year.
                    *   **15 P-NEW-TERM-DT-MM PIC 9(02):** New Termination Date - Month.
                    *   **15 P-NEW-TERM-DT-DD PIC 9(02):** New Termination Date - Day.
            *   **05 P-NEW-WAIVER-CODE PIC X(01):** New Waiver Code.
                *   **88 P-NEW-WAIVER-STATE VALUE 'Y':** Indicates Waiver State.
            *   **05 P-NEW-INTER-NO PIC 9(05):** New Internal Number.
            *   **05 P-NEW-PROVIDER-TYPE PIC X(02):** New Provider Type.
            *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01):** New Current Census Division.
            *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01):**  Redefines the census division.
            *   **05 P-NEW-MSA-DATA:**
                *   **10 P-NEW-CHG-CODE-INDEX PIC X:** New Charge Code Index.
                *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT:** New Geographic Location MSA - Right justified.
                *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04):** Redefines the geographic location as numeric.
                *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT:** New Wage Index Location MSA - Right justified.
                *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT:** New Standard Amount Location MSA - Right justified.
                *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:**  Redefines the standard amount as numeric.
                    *   **15 P-NEW-RURAL-1ST:**
                        *   **20 P-NEW-STAND-RURAL PIC XX:** New Rural Standard.
                            *   **88 P-NEW-STD-RURAL-CHECK VALUE '  ':** Rural Check
                        *   **15 P-NEW-RURAL-2ND PIC XX:** New Rural Second.
            *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX:** New SOL Com Dep Hosp Year.
            *   **05 P-NEW-LUGAR PIC X:** New Lugar.
            *   **05 P-NEW-TEMP-RELIEF-IND PIC X:** New Temporary Relief Indicator.
            *   **05 P-NEW-FED-PPS-BLEND-IND PIC X:** New Federal PPS Blend Indicator.
            *   **05 FILLER PIC X(05):** Filler.
        *   **0