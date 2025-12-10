## Analysis of COBOL Programs

### Program: LTCAL032

#### Files Accessed and Descriptions:

*   **COPY LTDRG031:** This is a copybook (included using the `COPY` statement) likely containing data structures related to DRG (Diagnosis Related Group) information for the fiscal year 2003.  It contains DRG codes, relative weights, and average length of stay.

#### Data Structures in WORKING-STORAGE SECTION:

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.**
    *   Description: A character string used for identification of the program's working storage.
*   **01 CAL-VERSION PIC X(05) VALUE 'C03.2'.**
    *   Description:  Stores the version of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS:**
    *   Description: A group of data items used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
    *   **05 H-LOS PIC 9(03).**
        *   Description: Length of stay (LOS), likely in days.
    *   **05 H-REG-DAYS PIC 9(03).**
        *   Description: Regular days.
    *   **05 H-TOTAL-DAYS PIC 9(05).**
        *   Description: Total days.
    *   **05 H-SSOT PIC 9(02).**
        *   Description:  Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC PIC 9(02).**
        *   Description: Blend Return Code.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
        *   Description: Blend Facility Rate.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
        *   Description: Blend PPS Rate.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
        *   Description: Short Stay Payment Amount.
    *   **05 H-SS-COST PIC 9(07)V9(02).**
        *   Description: Short Stay Cost.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Labor Portion of the payment.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Non-Labor Portion of the payment.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
        *   Description: Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
        *   Description: New Facility Specific Rate.

#### Data Structures in LINKAGE SECTION:

*   **01 BILL-NEW-DATA:**
    *   Description:  A data structure passed *into* the subroutine (LTCAL032). This represents the billing data from the calling program.
    *   **10 B-NPI10:**
        *   Description: National Provider Identifier (NPI)
        *   **15 B-NPI8 PIC X(08).**
            *   Description:  First 8 digits of the NPI.
        *   **15 B-NPI-FILLER PIC X(02).**
            *   Description: Filler for the NPI
    *   **10 B-PROVIDER-NO PIC X(06).**
        *   Description: Provider Number.
    *   **10 B-PATIENT-STATUS PIC X(02).**
        *   Description: Patient Status.
    *   **10 B-DRG-CODE PIC X(03).**
        *   Description:  DRG Code.
    *   **10 B-LOS PIC 9(03).**
        *   Description: Length of Stay.
    *   **10 B-COV-DAYS PIC 9(03).**
        *   Description: Covered Days.
    *   **10 B-LTR-DAYS PIC 9(02).**
        *   Description: Lifetime Reserve Days.
    *   **10 B-DISCHARGE-DATE:**
        *   Description:  Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).**
            *   Description: Century of Discharge Date.
        *   **15 B-DISCHG-YY PIC 9(02).**
            *   Description: Year of Discharge Date.
        *   **15 B-DISCHG-MM PIC 9(02).**
            *   Description: Month of Discharge Date.
        *   **15 B-DISCHG-DD PIC 9(02).**
            *   Description: Day of Discharge Date.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
        *   Description: Covered Charges.
    *   **10 B-SPEC-PAY-IND PIC X(01).**
        *   Description: Special Payment Indicator.
    *   **10 FILLER PIC X(13).**
        *   Description: Filler.
*   **01 PPS-DATA-ALL:**
    *   Description:  A data structure passed *to* the subroutine (LTCAL032).  This structure is used to return the calculated PPS data back to the calling program.
    *   **05 PPS-RTC PIC 9(02).**
        *   Description: Return Code (PPS-RTC). Indicates how the bill was paid or the reason for non-payment.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).**
        *   Description: Charge Threshold.
    *   **05 PPS-DATA:**
        *   Description: Group of data elements related to PPS calculation.
        *   **10 PPS-MSA PIC X(04).**
            *   Description: Metropolitan Statistical Area (MSA) code.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).**
            *   Description: Wage Index.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).**
            *   Description: Average Length of Stay.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).**
            *   Description: Relative Weight.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Outlier Payment Amount.
        *   **10 PPS-LOS PIC 9(03).**
            *   Description: Length of Stay.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).**
            *   Description: DRG Adjusted Payment Amount.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Federal Payment Amount.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Final Payment Amount.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).**
            *   Description: Facility Costs.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).**
            *   Description: New Facility Specific Rate.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).**
            *   Description: Outlier Threshold.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).**
            *   Description: Submitted DRG Code.
        *   **10 PPS-CALC-VERS-CD PIC X(05).**
            *   Description: Calculation Version Code.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).**
            *   Description: Regular Days Used.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).**
            *   Description: Lifetime Reserve Days Used.
        *   **10 PPS-BLEND-YEAR PIC 9(01).**
            *   Description: Blend Year.
        *   **10 PPS-COLA PIC 9(01)V9(03).**
            *   Description: Cost of Living Adjustment.
        *   **10 FILLER PIC X(04).**
            *   Description: Filler.
    *   **05 PPS-OTHER-DATA:**
        *   Description: Group of data elements related to PPS calculation.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Labor Percentage.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Non-Labor Percentage.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).**
            *   Description: Standard Federal Rate.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).**
            *   Description: Budget Neutrality Rate.
        *   **10 FILLER PIC X(20).**
            *   Description: Filler.
    *   **05 PPS-PC-DATA:**
        *   Description: PPS data for PC.
        *   **10 PPS-COT-IND PIC X(01).**
            *   Description: Cost Outlier Indicator.
        *   **10 FILLER PIC X(20).**
            *   Description: Filler.
*   **01 PRICER-OPT-VERS-SW:**
    *   Description:  Used to indicate which versions of the tables are passed.
    *   **05 PRICER-OPTION-SW PIC X(01).**
        *   Description: Switch to indicate whether all tables or just the provider record are passed.
        *   **88 ALL-TABLES-PASSED VALUE 'A'.**
            *   Description: Condition name indicating all tables are passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.**
            *   Description: Condition name indicating only the provider record is passed.
    *   **05 PPS-VERSIONS:**
        *   Description: Group of data elements related to the PPS Versions.
        *   **10 PPDRV-VERSION PIC X(05).**
            *   Description: Version of the PPDRV program.
*   **01 PROV-NEW-HOLD:**
    *   Description:  Provider Record data, passed *to* the subroutine.
    *   **02 PROV-NEWREC-HOLD1:**
        *   Description: Provider Record Data - Part 1
        *   **05 P-NEW-NPI10:**
            *   Description: New NPI
            *   **10 P-NEW-NPI8 PIC X(08).**
                *   Description: New NPI 8 digits
            *   **10 P-NEW-NPI-FILLER PIC X(02).**
                *   Description: New NPI Filler
        *   **05 P-NEW-PROVIDER-NO.**
            *   Description: New Provider Number
            *   **10 P-NEW-STATE PIC 9(02).**
                *   Description: New State
            *   **10 FILLER PIC X(04).**
                *   Description: Filler
        *   **05 P-NEW-DATE-DATA:**
            *   Description: Date Data
            *   **10 P-NEW-EFF-DATE:**
                *   Description: Effective Date
                *   **15 P-NEW-EFF-DT-CC PIC 9(02).**
                    *   Description: Effective Date CC
                *   **15 P-NEW-EFF-DT-YY PIC 9(02).**
                    *   Description: Effective Date YY
                *   **15 P-NEW-EFF-DT-MM PIC 9(02).**
                    *   Description: Effective Date MM
                *   **15 P-NEW-EFF-DT-DD PIC 9(02).**
                    *   Description: Effective Date DD
            *   **10 P-NEW-FY-BEGIN-DATE:**
                *   Description: Fiscal Year Begin Date
                *   **15 P-NEW-FY-BEG-DT-CC PIC 9(02).**
                    *   Description: FY Begin Date CC
                *   **15 P-NEW-FY-BEG-DT-YY PIC 9(02).**
                    *   Description: FY Begin Date YY
                *   **15 P-NEW-FY-BEG-DT-MM PIC 9(02).**
                    *   Description: FY Begin Date MM
                *   **15 P-NEW-FY-BEG-DT-DD PIC 9(02).**
                    *   Description: FY Begin Date DD
            *   **10 P-NEW-REPORT-DATE:**
                *   Description: Report Date
                *   **15 P-NEW-REPORT-DT-CC PIC 9(02).**
                    *   Description: Report Date CC
                *   **15 P-NEW-REPORT-DT-YY PIC 9(02).**
                    *   Description: Report Date YY
                *   **15 P-NEW-REPORT-DT-MM PIC 9(02).**
                    *   Description: Report Date MM
                *   **15 P-NEW-REPORT-DT-DD PIC 9(02).**
                    *   Description: Report Date DD
            *   **10 P-NEW-TERMINATION-DATE:**
                *   Description: Termination Date
                *   **15 P-NEW-TERM-DT-CC PIC 9(02).**
                    *   Description: Termination Date CC
                *   **15 P-NEW-TERM-DT-YY PIC 9(02).**
                    *   Description: Termination Date YY
                *   **15 P-NEW-TERM-DT-MM PIC 9(02).**
                    *   Description: Termination Date MM
                *   **15 P-NEW-TERM-DT-DD PIC 9(02).**
                    *   Description: Termination Date DD
        *   **05 P-NEW-WAIVER-CODE PIC X(01).**
            *   Description: Waiver Code
            *   **88 P-NEW-WAIVER-STATE VALUE 'Y'.**
                *   Description: Waiver State.
        *   **05 P-NEW-INTER-NO PIC 9(05).**
            *   Description: New Internal Number
        *   **05 P-NEW-PROVIDER-TYPE PIC X(02).**
            *   Description: New Provider Type.
        *   **05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
            *   Description: New Current Census Division.
        *   **05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).**
            *   Description: New Current Division.
        *   **05 P-NEW-MSA-DATA:**
            *   Description: MSA Data
            *   **10 P-NEW-CHG-CODE-INDEX PIC X.**
                *   Description: New Charge Code Index
            *   **10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.**
                *   Description: New Geo Location MSA X
            *   **10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).**
                *   Description: New Geo Location MSA 9
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.**
                *   Description: New Wage Index Location MSA
            *   **10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.**
                *   Description: New Standard Amount Location MSA
            *   **10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.**
                *   Description: New Standard Amount Location MSA 9
                *   **15 P-NEW-RURAL-1ST:**
                    *   Description: Rural 1st
                    *   **20 P-NEW-STAND-RURAL PIC XX.**
                        *   Description: New Standard Rural
                    *   **88 P-NEW-STD-RURAL-CHECK VALUE '  '.**
                        *   Description: New STD Rural Check
                *   **15 P-NEW-RURAL-2ND PIC XX.**
                    *   Description: Rural 2nd
        *   **05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.**
            *   Description: New Sol Com Dep Hosp Yr
        *   **05 P-NEW-LUGAR PIC X.**
            *   Description: New Lugar
        *   **05 P-NEW-TEMP-RELIEF-IND PIC X.**
            *   Description: New Temp Relief Ind
        *   **05 P-NEW-FED-PPS-BLEND-IND PIC X.**
            *   Description: New Fed PPS Blend Ind
        *   **05 FILLER PIC X(05).**
            *   Description: Filler
    *   **02 PROV-NEWREC-HOLD2:**
        *   Description: Provider Record Data - Part 2
        *   **05 P-NEW-VARIABLES:**
            *   Description: New Variables
            *   **10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
                *   Description: New Facility Specific Rate
            *   **10 P-NEW-COLA PIC 9(01)V9(03).**
                *   Description: New COLA
            *   **10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).**
                *   Description: New Intern Ratio
            *   **10 P-NEW-BED-SIZE PIC 9(05).**
                *   Description: New Bed Size
            *   **10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).**
                *   Description: New Operating Cost Charge Ratio
            *   **10 P-NEW-CMI PIC 9(01)V9(04).**
                *   Description: New CMI
            *   **10 P-NEW-SSI-RATIO PIC V9(04).**
                *   Description: New SSI Ratio
            *   **10 P-NEW-MEDICAID-RATIO PIC V9(04).**
                *   Description: New Medicaid Ratio
            *   **10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).**
                *   Description: New PPS Blend Year Ind
            *   **10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).**
                *   Description: New PRUF Update Factor
            *   **10 P-NEW-DSH-PERCENT PIC V9(04).**
                *   Description: New DSH Percent
            *   **10 P-NEW-FYE-DATE PIC X(08).**
                *   Description: New FYE Date
        *   **05 FILLER PIC X(23).**
            *   Description: Filler
    *   **02 PROV-NEWREC-HOLD3:**
        *   Description: Provider Record Data - Part 3
        *   **05 P-NEW-PASS-AMT-DATA:**
            *   Description: Pass Amount Data
            *   **10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.**
                *   Description: New Pass Amount Capital
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.**
                *   Description: New Pass Amount Direct Medical Education
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.**
                *   Description: New Pass Amount Organ Acquisition
            *   **10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.**
                *   Description: New Pass Amount Plus Misc
        *   **05 P-NEW-CAPI-DATA:**
            *   Description: Capital Data
            *   **15 P-NEW-CAPI-PPS-PAY-CODE PIC X.**
                *   Description: New Capital PPS Pay Code
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.**
                *   Description: New Capital Hospital Specific Rate
            *   **15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.**
                *   Description: New Capital Old Harm Rate
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.**
                *   Description: New Capital New Harm Ratio
            *   **15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.**
                *   Description: New Capital Cost Charge Ratio
            *   **15 P-NEW-CAPI-NEW-HOSP PIC X.**
                *   Description: New Capital New Hospital
            *   **15 P-NEW-CAPI-IME PIC 9V9999.**
                *   Description: New Capital IME
            *   **15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.**
                *   Description: New Capital Exceptions
        *   **05 FILLER PIC X(22).**
            *   Description: Filler
*   **01 WAGE-NEW-INDEX-RECORD:**
    *   Description: Wage Index record, passed *to* the subroutine.
    *   **05 W-MSA PIC X(4).**
        *   Description: MSA Code.
    *   **05 W-EFF-DATE PIC X(8).**
        *   Description: Effective Date.
    *   **05 W-WAGE-INDEX1 PIC S9(02)V9(04).**
        *   Description: Wage Index 1.
    *   **05 W-WAGE-INDEX2 PIC S9(02)V9(04).**
        *   Description: Wage Index 2.
    *   **05 W-WAGE-INDEX3 PIC S9(02)V9(04).**
        *   Description: Wage Index 3.

### Program: LTCAL042

#### Files Accessed and Descriptions:

*   **COPY LTDRG031:** This is a copybook (included using the `COPY` statement) likely containing data structures related to DRG (Diagnosis Related Group) information for the fiscal year 2003.  It contains DRG codes, relative weights, and average length of stay.

#### Data Structures in WORKING-STORAGE SECTION:

*   **01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.**
    *   Description: A character string used for identification of the program's working storage.
*   **01 CAL-VERSION PIC X(05) VALUE 'C04.2'.**
    *   Description:  Stores the version of the calculation logic.
*   **01 HOLD-PPS-COMPONENTS:**
    *   Description: A group of data items used to store intermediate calculation results and components related to the Prospective Payment System (PPS).
    *   **05 H-LOS PIC 9(03).**
        *   Description: Length of stay (LOS), likely in days.
    *   **05 H-REG-DAYS PIC 9(03).**
        *   Description: Regular days.
    *   **05 H-TOTAL-DAYS PIC 9(05).**
        *   Description: Total days.
    *   **05 H-SSOT PIC 9(02).**
        *   Description:  Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC PIC 9(02).**
        *   Description: Blend Return Code.
    *   **05 H-BLEND-FAC PIC 9(01)V9(01).**
        *   Description: Blend Facility Rate.
    *   **05 H-BLEND-PPS PIC 9(01)V9(01).**
        *   Description: Blend PPS Rate.
    *   **05 H-SS-PAY-AMT PIC 9(07)V9(02).**
        *   Description: Short Stay Payment Amount.
    *   **05 H-SS-COST PIC 9(07)V9(02).**
        *   Description: Short Stay Cost.
    *   **05 H-LABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Labor Portion of the payment.
    *   **05 H-NONLABOR-PORTION PIC 9(07)V9(06).**
        *   Description: Non-Labor Portion of the payment.
    *   **05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).**
        *   Description: Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).**
        *   Description: New Facility Specific Rate.
    *   **05 H-LOS-RATIO PIC 9(01)V9(05).**
        *   Description: Length of Stay Ratio.

#### Data Structures in LINKAGE SECTION:

*   **01 BILL-NEW-DATA:**
    *   Description:  A data structure passed *into* the subroutine (LTCAL042). This represents the billing data from the calling program.
    *   **10 B-NPI10:**
        *   Description: National Provider Identifier (NPI)
        *   **15 B-NPI8 PIC X(08).**
            *   Description:  First 8 digits of the NPI.
        *   **15 B-NPI-FILLER PIC X(02).**
            *   Description: Filler for the NPI
    *   **10 B-PROVIDER-NO PIC X(06).**
        *   Description: Provider Number.
    *   **10 B-PATIENT-STATUS PIC X(02).**
        *   Description: Patient Status.
    *   **10 B-DRG-CODE PIC X(03).**
        *   Description:  DRG Code.
    *   **10 B-LOS PIC 9(03).**
        *   Description: Length of Stay.
    *   **10 B-COV-DAYS PIC 9(03).**
        *   Description: Covered Days.
    *   **10 B-LTR-DAYS PIC 9(02).**
        *   Description: Lifetime Reserve Days.
    *   **10 B-DISCHARGE-DATE:**
        *   Description:  Discharge Date.
        *   **15 B-DISCHG-CC PIC 9(02).**
            *   Description: Century of Discharge Date.
        *   **15 B-DISCHG-YY PIC 9(02).**
            *   Description: Year of Discharge Date.
        *   **15 B-DISCHG-MM PIC 9(02).**
            *   Description: Month of Discharge Date.
        *   **15 B-DISCHG-DD PIC 9(02).**
            *   Description: Day of Discharge Date.
    *   **10 B-COV-CHARGES PIC 9(07)V9(02).**
        *   Description: Covered Charges.
    *   **10 B-SPEC-PAY-IND PIC X(01).**
        *   Description: Special Payment Indicator.
    *   **10 FILLER PIC X(13).**
        *   Description: Filler.
*   **01 PPS-DATA-ALL:**
    *   Description:  A data structure passed *to* the subroutine (LTCAL042).  This structure is used to return the calculated PPS data back to the calling program.
    *   **05 PPS-RTC PIC 9(02).**
        *   Description: Return Code (PPS-RTC). Indicates how the bill was paid or the reason for non-payment.
    *   **05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).**
        *   Description: Charge Threshold.
    *   **05 PPS-DATA:**
        *   Description: Group of data elements related to PPS calculation.
        *   **10 PPS-MSA PIC X(04).**
            *   Description: Metropolitan Statistical Area (MSA) code.
        *   **10 PPS-WAGE-INDEX PIC 9(02)V9(04).**
            *   Description: Wage Index.
        *   **10 PPS-AVG-LOS PIC 9(02)V9(01).**
            *   Description: Average Length of Stay.
        *   **10 PPS-RELATIVE-WGT PIC 9(01)V9(04).**
            *   Description: Relative Weight.
        *   **10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Outlier Payment Amount.
        *   **10 PPS-LOS PIC 9(03).**
            *   Description: Length of Stay.
        *   **10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).**
            *   Description: DRG Adjusted Payment Amount.
        *   **10 PPS-FED-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Federal Payment Amount.
        *   **10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).**
            *   Description: Final Payment Amount.
        *   **10 PPS-FAC-COSTS PIC 9(07)V9(02).**
            *   Description: Facility Costs.
        *   **10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).**
            *   Description: New Facility Specific Rate.
        *   **10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).**
            *   Description: Outlier Threshold.
        *   **10 PPS-SUBM-DRG-CODE PIC X(03).**
            *   Description: Submitted DRG Code.
        *   **10 PPS-CALC-VERS-CD PIC X(05).**
            *   Description: Calculation Version Code.
        *   **10 PPS-REG-DAYS-USED PIC 9(03).**
            *   Description: Regular Days Used.
        *   **10 PPS-LTR-DAYS-USED PIC 9(03).**
            *   Description: Lifetime Reserve Days Used.
        *   **10 PPS-BLEND-YEAR PIC 9(01).**
            *   Description: Blend Year.
        *   **10 PPS-COLA PIC 9(01)V9(03).**
            *   Description: Cost of Living Adjustment.
        *   **10 FILLER PIC X(04).**
            *   Description: Filler.
    *   **05 PPS-OTHER-DATA:**
        *   Description: Group of data elements related to PPS calculation.
        *   **10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Labor Percentage.
        *   **10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).**
            *   Description: National Non-Labor Percentage.
        *   **10 PPS-STD-FED-RATE PIC 9(05)V9(02).**
            *   Description: Standard Federal Rate.
        *   **10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).**
            *   Description: Budget Neutrality Rate.
        *   **10 FILLER PIC X(20).**
            *   Description: Filler.
    *   **05 PPS-PC-DATA:**
        *   Description: PPS data for PC.
        *   **10 PPS-COT-IND PIC X(01).**
            *   Description: Cost Outlier Indicator.
        *   **10 FILLER PIC X(20).**
            *   Description: Filler.
*   **01 PRICER-OPT-VERS-SW:**
    *   Description:  Used to indicate which versions of the tables are passed.
    *   **05 PRICER-OPTION-SW PIC X(01).**
        *   Description: Switch to indicate whether all tables or just the provider record are passed.
        *   **88 ALL-TABLES-PASSED VALUE 'A'.**
            *   Description: Condition name indicating all tables are passed.
        *   **88 PROV-RECORD-PASSED VALUE 'P'.**
            *   Description: Condition name indicating only the provider record is passed.
    *   **05 PPS-VERSIONS:**
        *   Description: Group of data elements related to the PPS Versions.
        *   **10 PPDRV-VERSION PIC X(05).**
            *   Description: Version of the PPDRV program.
*   **01 PROV-NEW-HOLD:**
    *   Description:  Provider Record data, passed *to* the subroutine.
    *   **02 PROV-NEWREC-HOLD1:**
        *   Description: Provider Record Data - Part 1
        *   **05