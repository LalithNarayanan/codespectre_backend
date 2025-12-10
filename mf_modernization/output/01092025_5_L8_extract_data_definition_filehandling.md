## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing the files accessed, data structures, and their descriptions:

### Program: LTCAL032

**Files Accessed:**

*   **COPY LTDRG031.**  This indicates the program includes a copybook named `LTDRG031`. This copybook likely contains data structures related to DRG codes and related pricing information.

**Data Structures in WORKING-STORAGE SECTION:**

*   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL032 - W O R K I N G S T O R A G E'.`
    *   Description:  A descriptive string identifying the program and the working storage section.
*   `01 CAL-VERSION PIC X(05) VALUE 'C03.2'.`
    *   Description:  Stores the version of the calculation logic used by the program.
*   `01 HOLD-PPS-COMPONENTS.`
    *   Description: This is a group item that holds the components used to calculate the PPS payment.
    *   `05 H-LOS PIC 9(03).`
        *   Description: Length of Stay (LOS) - likely in days, with a maximum of 999 days.
    *   `05 H-REG-DAYS PIC 9(03).`
        *   Description: Regular days -  likely covered days minus LTR days.
    *   `05 H-TOTAL-DAYS PIC 9(05).`
        *   Description: Total days -  likely the sum of regular and LTR days.
    *   `05 H-SSOT PIC 9(02).`
        *   Description: Short Stay Outlier threshold.
    *   `05 H-BLEND-RTC PIC 9(02).`
        *   Description: Return code for blend year.
    *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
        *   Description: Factor for Facility.
    *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
        *   Description: Factor for PPS.
    *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
        *   Description: Short Stay Payment Amount.
    *   `05 H-SS-COST PIC 9(07)V9(02).`
        *   Description: Short Stay Cost.
    *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
        *   Description:  Labor portion of the payment.
    *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
        *   Description:  Non-labor portion of the payment.
    *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
        *   Description: Fixed Loss Amount.
    *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
        *   Description: New Facility Specific Rate.

**Data Structures in LINKAGE SECTION:**

*   `01 BILL-NEW-DATA.`
    *   Description: This structure receives bill data from the calling program.
    *   `10 B-NPI10.`
        *   Description: National Provider Identifier (NPI)
        *   `15 B-NPI8 PIC X(08).`
            *   Description:  First 8 characters of the NPI.
        *   `15 B-NPI-FILLER PIC X(02).`
            *   Description:  Filler for NPI.
    *   `10 B-PROVIDER-NO PIC X(06).`
        *   Description: Provider Number.
    *   `10 B-PATIENT-STATUS PIC X(02).`
        *   Description: Patient status code.
    *   `10 B-DRG-CODE PIC X(03).`
        *   Description: DRG (Diagnosis Related Group) code.
    *   `10 B-LOS PIC 9(03).`
        *   Description: Length of Stay (LOS) - in days.
    *   `10 B-COV-DAYS PIC 9(03).`
        *   Description: Covered days.
    *   `10 B-LTR-DAYS PIC 9(02).`
        *   Description: Lifetime Reserve days.
    *   `10 B-DISCHARGE-DATE.`
        *   Description: Patient discharge date.
        *   `15 B-DISCHG-CC PIC 9(02).`
            *   Description: Century of Discharge Date.
        *   `15 B-DISCHG-YY PIC 9(02).`
            *   Description: Year of Discharge Date.
        *   `15 B-DISCHG-MM PIC 9(02).`
            *   Description: Month of Discharge Date.
        *   `15 B-DISCHG-DD PIC 9(02).`
            *   Description: Day of Discharge Date.
    *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
        *   Description: Covered charges.
    *   `10 B-SPEC-PAY-IND PIC X(01).`
        *   Description: Special Payment Indicator.
    *   `10 FILLER PIC X(13).`
        *   Description: Unused Space.
*   `01 PPS-DATA-ALL.`
    *   Description:  This structure returns the calculated PPS data to the calling program.
    *   `05 PPS-RTC PIC 9(02).`
        *   Description:  Return code indicating the payment method or reason for non-payment.
    *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
        *   Description: Charge Threshold.
    *   `05 PPS-DATA.`
        *   Description: PPS Data.
        *   `10 PPS-MSA PIC X(04).`
            *   Description:  MSA (Metropolitan Statistical Area) code.
        *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
            *   Description: Wage index.
        *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
            *   Description: Average Length of Stay (LOS).
        *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
            *   Description: Relative weight for the DRG.
        *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Outlier payment amount.
        *   `10 PPS-LOS PIC 9(03).`
            *   Description: Length of Stay.
        *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
            *   Description: DRG Adjusted Payment Amount.
        *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Federal Payment Amount.
        *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Final Payment Amount.
        *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
            *   Description: Facility Costs.
        *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
            *   Description: New Facility Specific Rate.
        *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
            *   Description: Outlier Threshold.
        *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
            *   Description: Submitted DRG Code.
        *   `10 PPS-CALC-VERS-CD PIC X(05).`
            *   Description: Calculation Version Code.
        *   `10 PPS-REG-DAYS-USED PIC 9(03).`
            *   Description: Regular Days Used.
        *   `10 PPS-LTR-DAYS-USED PIC 9(03).`
            *   Description: LTR Days Used.
        *   `10 PPS-BLEND-YEAR PIC 9(01).`
            *   Description: Blend Year indicator.
        *   `10 PPS-COLA PIC 9(01)V9(03).`
            *   Description: COLA (Cost of Living Adjustment).
        *   `10 FILLER PIC X(04).`
            *   Description: Unused Space.
    *   `05 PPS-OTHER-DATA.`
        *   Description: Other PPS Data.
        *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).`
            *   Description: National Labor Percentage.
        *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).`
            *   Description: National Non-Labor Percentage.
        *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02).`
            *   Description: Standard Federal Rate.
        *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9(03).`
            *   Description: Budget Neutrality Rate.
        *   `10 FILLER PIC X(20).`
            *   Description: Unused Space.
    *   `05 PPS-PC-DATA.`
        *   Description: PPS PC Data.
        *   `10 PPS-COT-IND PIC X(01).`
            *   Description: COT (Cost Outlier) Indicator.
        *   `10 FILLER PIC X(20).`
            *   Description: Unused Space.
*   `01 PRICER-OPT-VERS-SW.`
    *   Description: Switch for Pricer Option Versions.
    *   `05 PRICER-OPTION-SW PIC X(01).`
        *   Description: Pricer Option Switch.
        *   `88 ALL-TABLES-PASSED VALUE 'A'.`
            *   Description: Condition name, true if all tables are passed.
        *   `88 PROV-RECORD-PASSED VALUE 'P'.`
            *   Description: Condition name, true if provider record is passed.
    *   `05 PPS-VERSIONS.`
        *   Description: PPS Versions.
        *   `10 PPDRV-VERSION PIC X(05).`
            *   Description: Version of the PPDRV program.
*   `01 PROV-NEW-HOLD.`
    *   Description:  This structure holds provider-specific data.
    *   `02 PROV-NEWREC-HOLD1.`
        *   Description: Contains Provider Record 1 Information.
        *   `05 P-NEW-NPI10.`
            *   Description: New NPI Information.
            *   `10 P-NEW-NPI8 PIC X(08).`
                *   Description: New NPI - First 8 Characters.
            *   `10 P-NEW-NPI-FILLER PIC X(02).`
                *   Description: New NPI - Filler.
        *   `05 P-NEW-PROVIDER-NO.`
            *   Description: New Provider Number.
            *   `10 P-NEW-STATE PIC 9(02).`
                *   Description: New State.
            *   `10 FILLER PIC X(04).`
                *   Description: Unused Space.
        *   `05 P-NEW-DATE-DATA.`
            *   Description: New Date Data.
            *   `10 P-NEW-EFF-DATE.`
                *   Description: New Effective Date.
                *   `15 P-NEW-EFF-DT-CC PIC 9(02).`
                    *   Description: Century of New Effective Date.
                *   `15 P-NEW-EFF-DT-YY PIC 9(02).`
                    *   Description: Year of New Effective Date.
                *   `15 P-NEW-EFF-DT-MM PIC 9(02).`
                    *   Description: Month of New Effective Date.
                *   `15 P-NEW-EFF-DT-DD PIC 9(02).`
                    *   Description: Day of New Effective Date.
            *   `10 P-NEW-FY-BEGIN-DATE.`
                *   Description: New Fiscal Year Begin Date.
                *   `15 P-NEW-FY-BEG-DT-CC PIC 9(02).`
                    *   Description: Century of New FY Begin Date.
                *   `15 P-NEW-FY-BEG-DT-YY PIC 9(02).`
                    *   Description: Year of New FY Begin Date.
                *   `15 P-NEW-FY-BEG-DT-MM PIC 9(02).`
                    *   Description: Month of New FY Begin Date.
                *   `15 P-NEW-FY-BEG-DT-DD PIC 9(02).`
                    *   Description: Day of New FY Begin Date.
            *   `10 P-NEW-REPORT-DATE.`
                *   Description: New Report Date.
                *   `15 P-NEW-REPORT-DT-CC PIC 9(02).`
                    *   Description: Century of New Report Date.
                *   `15 P-NEW-REPORT-DT-YY PIC 9(02).`
                    *   Description: Year of New Report Date.
                *   `15 P-NEW-REPORT-DT-MM PIC 9(02).`
                    *   Description: Month of New Report Date.
                *   `15 P-NEW-REPORT-DT-DD PIC 9(02).`
                    *   Description: Day of New Report Date.
            *   `10 P-NEW-TERMINATION-DATE.`
                *   Description: New Termination Date.
                *   `15 P-NEW-TERM-DT-CC PIC 9(02).`
                    *   Description: Century of New Termination Date.
                *   `15 P-NEW-TERM-DT-YY PIC 9(02).`
                    *   Description: Year of New Termination Date.
                *   `15 P-NEW-TERM-DT-MM PIC 9(02).`
                    *   Description: Month of New Termination Date.
                *   `15 P-NEW-TERM-DT-DD PIC 9(02).`
                    *   Description: Day of New Termination Date.
        *   `05 P-NEW-WAIVER-CODE PIC X(01).`
            *   Description: New Waiver Code.
            *   `88 P-NEW-WAIVER-STATE VALUE 'Y'.`
                *   Description: Condition name, true if waiver state is 'Y'.
        *   `05 P-NEW-INTER-NO PIC 9(05).`
            *   Description: New Internal Number.
        *   `05 P-NEW-PROVIDER-TYPE PIC X(02).`
            *   Description: New Provider Type.
        *   `05 P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
            *   Description: Current Census Division.
        *   `05 P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).`
            *   Description: Current Division.
        *   `05 P-NEW-MSA-DATA.`
            *   Description: New MSA Data.
            *   `10 P-NEW-CHG-CODE-INDEX PIC X.`
                *   Description: New Charge Code Index.
            *   `10 P-NEW-GEO-LOC-MSAX PIC X(04) JUST RIGHT.`
                *   Description: New Geo Location MSA.
            *   `10 P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).`
                *   Description: New Geo Location MSA.
            *   `10 P-NEW-WAGE-INDEX-LOC-MSA PIC X(04) JUST RIGHT.`
                *   Description: New Wage Index Location MSA.
            *   `10 P-NEW-STAND-AMT-LOC-MSA PIC X(04) JUST RIGHT.`
                *   Description: New Standard Amount Location MSA.
            *   `10 P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.`
                *   Description: New Standard Amount Location MSA.
                *   `15 P-NEW-RURAL-1ST.`
                    *   Description: New Rural 1st.
                    *   `20 P-NEW-STAND-RURAL PIC XX.`
                        *   Description: New Standard Rural.
                        *   `88 P-NEW-STD-RURAL-CHECK VALUE ' '.`
                            *   Description: Condition name, true if standard rural check is space.
                    *   `15 P-NEW-RURAL-2ND PIC XX.`
                        *   Description: New Rural 2nd.
        *   `05 P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.`
            *   Description: New Sol Com Dep Hosp Yr.
        *   `05 P-NEW-LUGAR PIC X.`
            *   Description: New Lugar.
        *   `05 P-NEW-TEMP-RELIEF-IND PIC X.`
            *   Description: New Temporary Relief Indicator.
        *   `05 P-NEW-FED-PPS-BLEND-IND PIC X.`
            *   Description: New Federal PPS Blend Indicator.
        *   `05 FILLER PIC X(05).`
            *   Description: Unused Space.
    *   `02 PROV-NEWREC-HOLD2.`
        *   Description: Contains Provider Record 2 Information.
        *   `05 P-NEW-VARIABLES.`
            *   Description: New Variables.
            *   `10 P-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
                *   Description: New Facility Specific Rate.
            *   `10 P-NEW-COLA PIC 9(01)V9(03).`
                *   Description: New COLA.
            *   `10 P-NEW-INTERN-RATIO PIC 9(01)V9(04).`
                *   Description: New Intern Ratio.
            *   `10 P-NEW-BED-SIZE PIC 9(05).`
                *   Description: New Bed Size.
            *   `10 P-NEW-OPER-CSTCHG-RATIO PIC 9(01)V9(03).`
                *   Description: New Operating Cost to Charge Ratio.
            *   `10 P-NEW-CMI PIC 9(01)V9(04).`
                *   Description: New CMI.
            *   `10 P-NEW-SSI-RATIO PIC V9(04).`
                *   Description: New SSI Ratio.
            *   `10 P-NEW-MEDICAID-RATIO PIC V9(04).`
                *   Description: New Medicaid Ratio.
            *   `10 P-NEW-PPS-BLEND-YR-IND PIC 9(01).`
                *   Description: New PPS Blend Year Indicator.
            *   `10 P-NEW-PRUF-UPDTE-FACTOR PIC 9(01)V9(05).`
                *   Description: New PRUF Update Factor.
            *   `10 P-NEW-DSH-PERCENT PIC V9(04).`
                *   Description: New DSH Percent.
            *   `10 P-NEW-FYE-DATE PIC X(08).`
                *   Description: New FYE Date.
        *   `05 FILLER PIC X(23).`
            *   Description: Unused Space.
    *   `02 PROV-NEWREC-HOLD3.`
        *   Description: Contains Provider Record 3 Information.
        *   `05 P-NEW-PASS-AMT-DATA.`
            *   Description: New Pass Amount Data.
            *   `10 P-NEW-PASS-AMT-CAPITAL PIC 9(04)V99.`
                *   Description: New Pass Amount Capital.
            *   `10 P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.`
                *   Description: New Pass Amount Direct Medical Education.
            *   `10 P-NEW-PASS-AMT-ORGAN-ACQ PIC 9(04)V99.`
                *   Description: New Pass Amount Organ Acquisition.
            *   `10 P-NEW-PASS-AMT-PLUS-MISC PIC 9(04)V99.`
                *   Description: New Pass Amount Plus Misc.
        *   `05 P-NEW-CAPI-DATA.`
            *   Description: New Capital Data.
            *   `15 P-NEW-CAPI-PPS-PAY-CODE PIC X.`
                *   Description: New Capital PPS Pay Code.
            *   `15 P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.`
                *   Description: New Capital Hospital Specific Rate.
            *   `15 P-NEW-CAPI-OLD-HARM-RATE PIC 9(04)V99.`
                *   Description: New Capital Old Harm Rate.
            *   `15 P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.`
                *   Description: New Capital New Harm Ratio.
            *   `15 P-NEW-CAPI-CSTCHG-RATIO PIC 9V999.`
                *   Description: New Capital Cost to Charge Ratio.
            *   `15 P-NEW-CAPI-NEW-HOSP PIC X.`
                *   Description: New Capital New Hospital.
            *   `15 P-NEW-CAPI-IME PIC 9V9999.`
                *   Description: New Capital IME.
            *   `15 P-NEW-CAPI-EXCEPTIONS PIC 9(04)V99.`
                *   Description: New Capital Exceptions.
        *   `05 FILLER PIC X(22).`
            *   Description: Unused Space.
*   `01 WAGE-NEW-INDEX-RECORD.`
    *   Description:  This structure provides wage index data.
    *   `05 W-MSA PIC X(4).`
        *   Description: MSA (Metropolitan Statistical Area) code.
    *   `05 W-EFF-DATE PIC X(8).`
        *   Description: Effective date.
    *   `05 W-WAGE-INDEX1 PIC S9(02)V9(04).`
        *   Description: Wage Index.
    *   `05 W-WAGE-INDEX2 PIC S9(02)V9(04).`
        *   Description: Wage Index.
    *   `05 W-WAGE-INDEX3 PIC S9(02)V9(04).`
        *   Description: Wage Index.

**PROCEDURE DIVISION:**

The procedure division contains the logic for calculating the PPS payment.  Key sections include:

*   `0000-MAINLINE-CONTROL`:  The main control flow, calling various subroutines.
*   `0100-INITIAL-ROUTINE`: Initializes variables.
*   `1000-EDIT-THE-BILL-INFO`: Performs data validation on the input bill data.
*   `1200-DAYS-USED`: Calculates the number of regular and LTR days.
*   `1700-EDIT-DRG-CODE`:  Looks up the DRG code in a table.
*   `1750-FIND-VALUE`: Retrieves values from the DRG table.
*   `2000-ASSEMBLE-PPS-VARIABLES`: Retrieves provider-specific and wage index variables.
*   `3000-CALC-PAYMENT`: Calculates the standard payment amount.
*   `3400-SHORT-STAY`: Calculates short-stay payment.
*   `7000-CALC-OUTLIER`: Calculates outlier payments.
*   `8000-BLEND`: Applies blending logic based on the blend year.
*   `9000-MOVE-RESULTS`: Moves the calculated results to the output structure.

### Program: LTCAL042

**Files Accessed:**

*   **COPY LTDRG031.** This indicates the program includes a copybook named `LTDRG031`. This copybook likely contains data structures related to DRG codes and related pricing information.

**Data Structures in WORKING-STORAGE SECTION:**

*   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL042 - W O R K I N G S T O R A G E'.`
    *   Description: A descriptive string identifying the program and the working storage section.
*   `01 CAL-VERSION PIC X(05) VALUE 'C04.2'.`
    *   Description: Stores the version of the calculation logic used by the program.
*   `01 HOLD-PPS-COMPONENTS.`
    *   Description: This is a group item that holds the components used to calculate the PPS payment.
    *   `05 H-LOS PIC 9(03).`
        *   Description: Length of Stay (LOS) - likely in days, with a maximum of 999 days.
    *   `05 H-REG-DAYS PIC 9(03).`
        *   Description: Regular days -  likely covered days minus LTR days.
    *   `05 H-TOTAL-DAYS PIC 9(05).`
        *   Description: Total days -  likely the sum of regular and LTR days.
    *   `05 H-SSOT PIC 9(02).`
        *   Description: Short Stay Outlier threshold.
    *   `05 H-BLEND-RTC PIC 9(02).`
        *   Description: Return code for blend year.
    *   `05 H-BLEND-FAC PIC 9(01)V9(01).`
        *   Description: Factor for Facility.
    *   `05 H-BLEND-PPS PIC 9(01)V9(01).`
        *   Description: Factor for PPS.
    *   `05 H-SS-PAY-AMT PIC 9(07)V9(02).`
        *   Description: Short Stay Payment Amount.
    *   `05 H-SS-COST PIC 9(07)V9(02).`
        *   Description: Short Stay Cost.
    *   `05 H-LABOR-PORTION PIC 9(07)V9(06).`
        *   Description: Labor portion of the payment.
    *   `05 H-NONLABOR-PORTION PIC 9(07)V9(06).`
        *   Description: Non-labor portion of the payment.
    *   `05 H-FIXED-LOSS-AMT PIC 9(07)V9(02).`
        *   Description: Fixed Loss Amount.
    *   `05 H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02).`
        *   Description: New Facility Specific Rate.
    *   `05 H-LOS-RATIO PIC 9(01)V9(05).`
        *   Description:  Ratio of LOS to Average LOS.

**Data Structures in LINKAGE SECTION:**

*   `01 BILL-NEW-DATA.`
    *   Description: This structure receives bill data from the calling program.
    *   `10 B-NPI10.`
        *   Description: National Provider Identifier (NPI)
        *   `15 B-NPI8 PIC X(08).`
            *   Description: First 8 characters of the NPI.
        *   `15 B-NPI-FILLER PIC X(02).`
            *   Description: Filler for NPI.
    *   `10 B-PROVIDER-NO PIC X(06).`
        *   Description: Provider Number.
    *   `10 B-PATIENT-STATUS PIC X(02).`
        *   Description: Patient status code.
    *   `10 B-DRG-CODE PIC X(03).`
        *   Description: DRG (Diagnosis Related Group) code.
    *   `10 B-LOS PIC 9(03).`
        *   Description: Length of Stay (LOS) - in days.
    *   `10 B-COV-DAYS PIC 9(03).`
        *   Description: Covered days.
    *   `10 B-LTR-DAYS PIC 9(02).`
        *   Description: Lifetime Reserve days.
    *   `10 B-DISCHARGE-DATE.`
        *   Description: Patient discharge date.
        *   `15 B-DISCHG-CC PIC 9(02).`
            *   Description: Century of Discharge Date.
        *   `15 B-DISCHG-YY PIC 9(02).`
            *   Description: Year of Discharge Date.
        *   `15 B-DISCHG-MM PIC 9(02).`
            *   Description: Month of Discharge Date.
        *   `15 B-DISCHG-DD PIC 9(02).`
            *   Description: Day of Discharge Date.
    *   `10 B-COV-CHARGES PIC 9(07)V9(02).`
        *   Description: Covered charges.
    *   `10 B-SPEC-PAY-IND PIC X(01).`
        *   Description: Special Payment Indicator.
    *   `10 FILLER PIC X(13).`
        *   Description: Unused Space.
*   `01 PPS-DATA-ALL.`
    *   Description: This structure returns the calculated PPS data to the calling program.
    *   `05 PPS-RTC PIC 9(02).`
        *   Description: Return code indicating the payment method or reason for non-payment.
    *   `05 PPS-CHRG-THRESHOLD PIC 9(07)V9(02).`
        *   Description: Charge Threshold.
    *   `05 PPS-DATA.`
        *   Description: PPS Data.
        *   `10 PPS-MSA PIC X(04).`
            *   Description: MSA (Metropolitan Statistical Area) code.
        *   `10 PPS-WAGE-INDEX PIC 9(02)V9(04).`
            *   Description: Wage index.
        *   `10 PPS-AVG-LOS PIC 9(02)V9(01).`
            *   Description: Average Length of Stay (LOS).
        *   `10 PPS-RELATIVE-WGT PIC 9(01)V9(04).`
            *   Description: Relative weight for the DRG.
        *   `10 PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Outlier payment amount.
        *   `10 PPS-LOS PIC 9(03).`
            *   Description: Length of Stay.
        *   `10 PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02).`
            *   Description: DRG Adjusted Payment Amount.
        *   `10 PPS-FED-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Federal Payment Amount.
        *   `10 PPS-FINAL-PAY-AMT PIC 9(07)V9(02).`
            *   Description: Final Payment Amount.
        *   `10 PPS-FAC-COSTS PIC 9(07)V9(02).`
            *   Description: Facility Costs.
        *   `10 PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02).`
            *   Description: New Facility Specific Rate.
        *   `10 PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02).`
            *   Description: Outlier Threshold.
        *   `10 PPS-SUBM-DRG-CODE PIC X(03).`
            *   Description: Submitted DRG Code.
        *   `10 PPS-CALC-VERS-CD PIC X(05).`
            *   Description: Calculation Version Code.
        *   `10 PPS-REG-DAYS-USED PIC 9(03).`
            *   Description: Regular Days Used.
        *   `10 PPS-LTR-DAYS-USED PIC 9(03).`
            *   Description: LTR Days Used.
        *   `10 PPS-BLEND-YEAR PIC 9(01).`
            *   Description: Blend Year indicator.
        *   `10 PPS-COLA PIC 9(01)V9(03).`
            *   Description: COLA (Cost of Living Adjustment).
        *   `10 FILLER PIC X(04).`
            *   Description: Unused Space.
    *   `05 PPS-OTHER-DATA.`
        *   Description: Other PPS Data.
        *   `10 PPS-NAT-LABOR-PCT PIC 9(01)V9(05).`
            *   Description: National Labor Percentage.
        *   `10 PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05).`
            *   Description: National Non-Labor Percentage.
        *   `10 PPS-STD-FED-RATE PIC 9(05)V9(02).`
            *   Description: Standard Federal Rate.
        *   `10 PPS-BDGT-NEUT-RATE PIC 9(01)V9