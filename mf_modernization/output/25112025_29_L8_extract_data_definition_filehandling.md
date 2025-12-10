## Analysis of COBOL Programs

Here's an analysis of the provided COBOL programs, detailing file access, data structures, and other relevant information.

### Program: LTCAL032

*   **File Access:**
    *   No explicit file access statements (e.g., `SELECT`, `OPEN`) are present in this program. It's likely that file interactions are handled by the calling program or another module.
    *   **COPY LTDRG031:** This statement includes the contents of the `LTDRG031` copybook, which likely contains DRG (Diagnosis Related Group) data.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01  W-STORAGE-REF                  PIC X(46)  VALUE 'LTCAL032      - W O R K I N G   S T O R A G E'.`
        *   Description: A working storage variable used for program identification or debugging purposes.

    *   `01  CAL-VERSION                    PIC X(05)  VALUE 'C03.2'.`
        *   Description:  Stores the version number of the calculation logic.

    *   **COPY LTDRG031:**  (The contents of this copybook are included, see below)
        *   Description: This copybook contains the DRG (Diagnosis Related Group) related data structures.

    *   `01  HOLD-PPS-COMPONENTS.`
        *   Description: This group of variables stores intermediate calculation results.
            *   `05  H-LOS                        PIC 9(03).`  Description: Length of Stay
            *   `05  H-REG-DAYS                   PIC 9(03).`  Description: Regular Days
            *   `05  H-TOTAL-DAYS                 PIC 9(05).`  Description: Total Days
            *   `05  H-SSOT                       PIC 9(02).`  Description: Short Stay Outlier Threshold
            *   `05  H-BLEND-RTC                  PIC 9(02).`  Description: Blend Return Code
            *   `05  H-BLEND-FAC                  PIC 9(01)V9(01).`  Description: Blend Facility Portion
            *   `05  H-BLEND-PPS                  PIC 9(01)V9(01).`  Description: Blend PPS Portion
            *   `05  H-SS-PAY-AMT                 PIC 9(07)V9(02).`  Description: Short Stay Payment Amount
            *   `05  H-SS-COST                    PIC 9(07)V9(02).`  Description: Short Stay Cost
            *   `05  H-LABOR-PORTION              PIC 9(07)V9(06).`  Description: Labor Portion of Payment
            *   `05  H-NONLABOR-PORTION           PIC 9(07)V9(06).`  Description: Non-Labor Portion of Payment
            *   `05  H-FIXED-LOSS-AMT             PIC 9(07)V9(02).`  Description: Fixed Loss Amount
            *   `05  H-NEW-FAC-SPEC-RATE          PIC 9(05)V9(02).`  Description: New Facility Specific Rate

*   **Data Structures in LINKAGE SECTION:**

    *   `01  BILL-NEW-DATA.`
        *   Description: This structure receives bill data from the calling program.
            *   `10  B-NPI10.`
                *   `15  B-NPI8             PIC X(08).`  Description: National Provider Identifier (NPI) - First 8 characters
                *   `15  B-NPI-FILLER       PIC X(02).`  Description: National Provider Identifier (NPI) - Filler
            *   `10  B-PROVIDER-NO          PIC X(06).`  Description: Provider Number
            *   `10  B-PATIENT-STATUS       PIC X(02).`  Description: Patient Status
            *   `10  B-DRG-CODE             PIC X(03).`  Description: DRG Code
            *   `10  B-LOS                  PIC 9(03).`  Description: Length of Stay
            *   `10  B-COV-DAYS             PIC 9(03).`  Description: Covered Days
            *   `10  B-LTR-DAYS             PIC 9(02).`  Description: Lifetime Reserve Days
            *   `10  B-DISCHARGE-DATE.`
                *   `15  B-DISCHG-CC              PIC 9(02).`  Description: Discharge Date - Century
                *   `15  B-DISCHG-YY              PIC 9(02).`  Description: Discharge Date - Year
                *   `15  B-DISCHG-MM              PIC 9(02).`  Description: Discharge Date - Month
                *   `15  B-DISCHG-DD              PIC 9(02).`  Description: Discharge Date - Day
            *   `10  B-COV-CHARGES                PIC 9(07)V9(02).`  Description: Covered Charges
            *   `10  B-SPEC-PAY-IND               PIC X(01).`  Description: Special Payment Indicator
            *   `10  FILLER                       PIC X(13).`  Description: Filler

    *   `01  PPS-DATA-ALL.`
        *   Description: This structure is used to pass calculated PPS (Prospective Payment System) data back to the calling program.
            *   `05  PPS-RTC                       PIC 9(02).`  Description: Return Code (PPS)
            *   `05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02).` Description: Charge Threshold
            *   `05  PPS-DATA.`
                *   `10  PPS-MSA                   PIC X(04).`  Description: Metropolitan Statistical Area (MSA)
                *   `10  PPS-WAGE-INDEX            PIC 9(02)V9(04).` Description: Wage Index
                *   `10  PPS-AVG-LOS               PIC 9(02)V9(01).` Description: Average Length of Stay
                *   `10  PPS-RELATIVE-WGT          PIC 9(01)V9(04).` Description: Relative Weight
                *   `10  PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02).` Description: Outlier Payment Amount
                *   `10  PPS-LOS                   PIC 9(03).`  Description: Length of Stay
                *   `10  PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02).` Description: DRG Adjusted Payment Amount
                *   `10  PPS-FED-PAY-AMT           PIC 9(07)V9(02).` Description: Federal Payment Amount
                *   `10  PPS-FINAL-PAY-AMT         PIC 9(07)V9(02).` Description: Final Payment Amount
                *   `10  PPS-FAC-COSTS             PIC 9(07)V9(02).` Description: Facility Costs
                *   `10  PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02).` Description: New Facility Specific Rate
                *   `10  PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02).` Description: Outlier Threshold
                *   `10  PPS-SUBM-DRG-CODE         PIC X(03).`  Description: Submitted DRG Code
                *   `10  PPS-CALC-VERS-CD          PIC X(05).`  Description: Calculation Version Code
                *   `10  PPS-REG-DAYS-USED         PIC 9(03).`  Description: Regular Days Used
                *   `10  PPS-LTR-DAYS-USED         PIC 9(03).`  Description: Lifetime Reserve Days Used
                *   `10  PPS-BLEND-YEAR            PIC 9(01).`  Description: Blend Year
                *   `10  PPS-COLA                  PIC 9(01)V9(03).` Description: Cost of Living Adjustment
                *   `10  FILLER                    PIC X(04).`  Description: Filler
            *   `05  PPS-OTHER-DATA.`
                *   `10  PPS-NAT-LABOR-PCT         PIC 9(01)V9(05).` Description: National Labor Percentage
                *   `10  PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05).` Description: National Non-Labor Percentage
                *   `10  PPS-STD-FED-RATE          PIC 9(05)V9(02).` Description: Standard Federal Rate
                *   `10  PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03).` Description: Budget Neutrality Rate
                *   `10  FILLER                    PIC X(20).`  Description: Filler
            *   `05  PPS-PC-DATA.`
                *   `10  PPS-COT-IND               PIC X(01).`  Description: Cost Outlier Indicator
                *   `10  FILLER                    PIC X(20).`  Description: Filler

    *   `01  PRICER-OPT-VERS-SW.`
        *   Description:  Used to indicate which version of the pricer options is being used.
            *   `05  PRICER-OPTION-SW          PIC X(01).`  Description: Pricer Option Switch
                *   `88  ALL-TABLES-PASSED          VALUE 'A'.`  Description: All tables passed indicator
                *   `88  PROV-RECORD-PASSED         VALUE 'P'.`  Description: Provider record passed indicator
            *   `05  PPS-VERSIONS.`
                *   `10  PPDRV-VERSION         PIC X(05).`  Description: Version of the PPDRV program

    *   `01  PROV-NEW-HOLD.`
        *   Description:  Provider record data passed from calling program.
            *   `02  PROV-NEWREC-HOLD1.`
                *   `05  P-NEW-NPI10.`
                    *   `10  P-NEW-NPI8             PIC X(08).`  Description: New NPI - First 8 characters
                    *   `10  P-NEW-NPI-FILLER       PIC X(02).`  Description: New NPI - Filler
                *   `05  P-NEW-PROVIDER-NO.`
                    *   `10  P-NEW-STATE            PIC 9(02).`  Description: New State
                    *   `10  FILLER                 PIC X(04).`  Description: Filler
                *   `05  P-NEW-DATE-DATA.`
                    *   `10  P-NEW-EFF-DATE.`
                        *   `15  P-NEW-EFF-DT-CC    PIC 9(02).`  Description: Effective Date - Century
                        *   `15  P-NEW-EFF-DT-YY    PIC 9(02).`  Description: Effective Date - Year
                        *   `15  P-NEW-EFF-DT-MM    PIC 9(02).`  Description: Effective Date - Month
                        *   `15  P-NEW-EFF-DT-DD    PIC 9(02).`  Description: Effective Date - Day
                    *   `10  P-NEW-FY-BEGIN-DATE.`
                        *   `15  P-NEW-FY-BEG-DT-CC PIC 9(02).`  Description: Fiscal Year Begin Date - Century
                        *   `15  P-NEW-FY-BEG-DT-YY PIC 9(02).`  Description: Fiscal Year Begin Date - Year
                        *   `15  P-NEW-FY-BEG-DT-MM PIC 9(02).`  Description: Fiscal Year Begin Date - Month
                        *   `15  P-NEW-FY-BEG-DT-DD PIC 9(02).`  Description: Fiscal Year Begin Date - Day
                    *   `10  P-NEW-REPORT-DATE.`
                        *   `15  P-NEW-REPORT-DT-CC PIC 9(02).`  Description: Report Date - Century
                        *   `15  P-NEW-REPORT-DT-YY PIC 9(02).`  Description: Report Date - Year
                        *   `15  P-NEW-REPORT-DT-MM PIC 9(02).`  Description: Report Date - Month
                        *   `15  P-NEW-REPORT-DT-DD PIC 9(02).`  Description: Report Date - Day
                    *   `10  P-NEW-TERMINATION-DATE.`
                        *   `15  P-NEW-TERM-DT-CC   PIC 9(02).`  Description: Termination Date - Century
                        *   `15  P-NEW-TERM-DT-YY   PIC 9(02).`  Description: Termination Date - Year
                        *   `15  P-NEW-TERM-DT-MM   PIC 9(02).`  Description: Termination Date - Month
                        *   `15  P-NEW-TERM-DT-DD   PIC 9(02).`  Description: Termination Date - Day
                *   `05  P-NEW-WAIVER-CODE          PIC X(01).`  Description: Waiver Code
                    *   `88  P-NEW-WAIVER-STATE       VALUE 'Y'.`  Description: Waiver State Flag
                *   `05  P-NEW-INTER-NO             PIC 9(05).`  Description: Interim Number
                *   `05  P-NEW-PROVIDER-TYPE        PIC X(02).`  Description: Provider Type
                *   `05  P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).`  Description: Current Census Division
                *   `05  P-NEW-MSA-DATA.`
                    *   `10  P-NEW-CHG-CODE-INDEX       PIC X. ` Description: Charge Code Index
                    *   `10  P-NEW-GEO-LOC-MSAX         PIC X(04) JUST RIGHT.` Description: Geographic Location MSA
                    *   `10  P-NEW-WAGE-INDEX-LOC-MSA   PIC X(04) JUST RIGHT.` Description: Wage Index Location MSA
                    *   `10  P-NEW-STAND-AMT-LOC-MSA    PIC X(04) JUST RIGHT.` Description: Standard Amount Location MSA
                    *   `10  P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.` Description: Sole Community Dependent Hospital Year
                *   `05  P-NEW-LUGAR                    PIC X.`  Description: Lugar
                *   `05  P-NEW-TEMP-RELIEF-IND          PIC X.`  Description: Temporary Relief Indicator
                *   `05  P-NEW-FED-PPS-BLEND-IND        PIC X.` Description: Federal PPS Blend Indicator
                *   `05  FILLER                         PIC X(05).`  Description: Filler
            *   `02  PROV-NEWREC-HOLD2.`
                *   `05  P-NEW-VARIABLES.`
                    *   `10  P-NEW-FAC-SPEC-RATE     PIC  9(05)V9(02).`  Description: Facility Specific Rate
                    *   `10  P-NEW-COLA              PIC  9(01)V9(03).`  Description: COLA
                    *   `10  P-NEW-INTERN-RATIO      PIC  9(01)V9(04).`  Description: Intern Ratio
                    *   `10  P-NEW-BED-SIZE          PIC  9(05).`  Description: Bed Size
                    *   `10  P-NEW-OPER-CSTCHG-RATIO PIC  9(01)V9(03).`  Description: Operating Cost to Charge Ratio
                    *   `10  P-NEW-CMI               PIC  9(01)V9(04).`  Description: CMI
                    *   `10  P-NEW-SSI-RATIO         PIC  V9(04).`  Description: SSI Ratio
                    *   `10  P-NEW-MEDICAID-RATIO    PIC  V9(04).`  Description: Medicaid Ratio
                    *   `10  P-NEW-PPS-BLEND-YR-IND  PIC  9(01).`  Description: PPS Blend Year Indicator
                    *   `10  P-NEW-PRUF-UPDTE-FACTOR PIC  9(01)V9(05).`  Description: PRUF Update Factor
                    *   `10  P-NEW-DSH-PERCENT       PIC  V9(04).`  Description: DSH Percent
                    *   `10  P-NEW-FYE-DATE          PIC  X(08).`  Description: Fiscal Year End Date
                *   `05  FILLER                      PIC  X(23).`  Description: Filler
            *   `02  PROV-NEWREC-HOLD3.`
                *   `05  P-NEW-PASS-AMT-DATA.`
                    *   `10  P-NEW-PASS-AMT-CAPITAL    PIC 9(04)V99.` Description: Passed Amount Capital
                    *   `10  P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.` Description: Passed Amount Direct Medical Education
                    *   `10  P-NEW-PASS-AMT-ORGAN-ACQ  PIC 9(04)V99.` Description: Passed Amount Organ Acquisition
                    *   `10  P-NEW-PASS-AMT-PLUS-MISC  PIC 9(04)V99.` Description: Passed Amount Plus Miscellaneous
                *   `05  P-NEW-CAPI-DATA.`
                    *   `15  P-NEW-CAPI-PPS-PAY-CODE   PIC X.` Description: Capital PPS Pay Code
                    *   `15  P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.` Description: Capital Hospital Specific Rate
                    *   `15  P-NEW-CAPI-OLD-HARM-RATE  PIC 9(04)V99.` Description: Capital Old Harm Rate
                    *   `15  P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.` Description: Capital New Harm Ratio
                    *   `15  P-NEW-CAPI-CSTCHG-RATIO   PIC 9V999.` Description: Capital Cost to Charge Ratio
                    *   `15  P-NEW-CAPI-NEW-HOSP       PIC X.` Description: Capital New Hospital
                    *   `15  P-NEW-CAPI-IME            PIC 9V9999.` Description: Capital IME
                    *   `15  P-NEW-CAPI-EXCEPTIONS     PIC 9(04)V99.` Description: Capital Exceptions
                *   `05  FILLER                        PIC X(22).`  Description: Filler

    *   `01  WAGE-NEW-INDEX-RECORD.`
        *   Description: Wage index record data passed from the calling program.
            *   `05  W-MSA                         PIC X(4).`  Description: MSA
            *   `05  W-EFF-DATE                    PIC X(8).`  Description: Effective Date
            *   `05  W-WAGE-INDEX1                 PIC S9(02)V9(04).` Description: Wage Index 1
            *   `05  W-WAGE-INDEX2                 PIC S9(02)V9(04).` Description: Wage Index 2
            *   `05  W-WAGE-INDEX3                 PIC S9(02)V9(04).` Description: Wage Index 3

*   **Procedure Division:**
    *   The program's main logic is contained within the `PROCEDURE DIVISION`.
    *   It calls several sections:
        *   `0100-INITIAL-ROUTINE`: Initializes working storage variables.
        *   `1000-EDIT-THE-BILL-INFO`: Performs edits on the bill data and sets the return code (`PPS-RTC`) if errors are found.
        *   `1700-EDIT-DRG-CODE`:  Looks up the DRG code in a table (likely from the `LTDRG031` copybook).
        *   `2000-ASSEMBLE-PPS-VARIABLES`: Assembles the PPS variables based on provider and wage index information.
        *   `3000-CALC-PAYMENT`: Calculates the standard payment amount,  and calls 3400-SHORT-STAY if applicable.
        *   `7000-CALC-OUTLIER`: Calculates outlier payments.
        *   `8000-BLEND`: Applies blending logic based on the blend year.
        *   `9000-MOVE-RESULTS`: Moves the calculated results to the `PPS-DATA-ALL` structure for the calling program.

### Program: LTCAL042

*   **File Access:**
    *   No explicit file access statements (e.g., `SELECT`, `OPEN`) are present in this program. It's likely that file interactions are handled by the calling program or another module.
    *   **COPY LTDRG031:** This statement includes the contents of the `LTDRG031` copybook, which likely contains DRG (Diagnosis Related Group) data.

*   **Data Structures in WORKING-STORAGE SECTION:**

    *   `01  W-STORAGE-REF                  PIC X(46)  VALUE 'LTCAL042      - W O R K I N G   S T O R A G E'.`
        *   Description: A working storage variable used for program identification or debugging purposes.

    *   `01  CAL-VERSION                    PIC X(05)  VALUE 'C04.2'.`
        *   Description:  Stores the version number of the calculation logic.

    *   **COPY LTDRG031:** (The contents of this copybook are included, see below)
        *   Description: This copybook contains the DRG (Diagnosis Related Group) related data structures.

    *   `01  HOLD-PPS-COMPONENTS.`
        *   Description: This group of variables stores intermediate calculation results.
            *   `05  H-LOS                        PIC 9(03).`  Description: Length of Stay
            *   `05  H-REG-DAYS                   PIC 9(03).`  Description: Regular Days
            *   `05  H-TOTAL-DAYS                 PIC 9(05).`  Description: Total Days
            *   `05  H-SSOT                       PIC 9(02).`  Description: Short Stay Outlier Threshold
            *   `05  H-BLEND-RTC                  PIC 9(02).`  Description: Blend Return Code
            *   `05  H-BLEND-FAC                  PIC 9(01)V9(01).`  Description: Blend Facility Portion
            *   `05  H-BLEND-PPS                  PIC 9(01)V9(01).`  Description: Blend PPS Portion
            *   `05  H-SS-PAY-AMT                 PIC 9(07)V9(02).`  Description: Short Stay Payment Amount
            *   `05  H-SS-COST                    PIC 9(07)V9(02).`  Description: Short Stay Cost
            *   `05  H-LABOR-PORTION              PIC 9(07)V9(06).`  Description: Labor Portion of Payment
            *   `05  H-NONLABOR-PORTION           PIC 9(07)V9(06).`  Description: Non-Labor Portion of Payment
            *   `05  H-FIXED-LOSS-AMT             PIC 9(07)V9(02).`  Description: Fixed Loss Amount
            *   `05  H-NEW-FAC-SPEC-RATE          PIC 9(05)V9(02).`  Description: New Facility Specific Rate
            *   `05  H-LOS-RATIO                  PIC 9(01)V9(05).`  Description: Length of Stay Ratio

*   **Data Structures in LINKAGE SECTION:**

    *   `01  BILL-NEW-DATA.`
        *   Description: This structure receives bill data from the calling program.
            *   `10  B-NPI10.`
                *   `15  B-NPI8             PIC X(08).`  Description: National Provider Identifier (NPI) - First 8 characters
                *   `15  B-NPI-FILLER       PIC X(02).`  Description: National Provider Identifier (NPI) - Filler
            *   `10  B-PROVIDER-NO          PIC X(06).`  Description: Provider Number
            *   `10  B-PATIENT-STATUS       PIC X(02).`  Description: Patient Status
            *   `10  B-DRG-CODE             PIC X(03).`  Description: DRG Code
            *   `10  B-LOS                  PIC 9(03).`  Description: Length of Stay
            *   `10  B-COV-DAYS             PIC 9(03).`  Description: Covered Days
            *   `10  B-LTR-DAYS             PIC 9(02).`  Description: Lifetime Reserve Days
            *   `10  B-DISCHARGE-DATE.`
                *   `15  B-DISCHG-CC              PIC 9(02).`  Description: Discharge Date - Century
                *   `15  B-DISCHG-YY              PIC 9(02).`  Description: Discharge Date - Year
                *   `15  B-DISCHG-MM              PIC 9(02).`  Description: Discharge Date - Month
                *   `15  B-DISCHG-DD              PIC 9(02).`  Description: Discharge Date - Day
            *   `10  B-COV-CHARGES                PIC 9(07)V9(02).`  Description: Covered Charges
            *   `10  B-SPEC-PAY-IND               PIC X(01).`  Description: Special Payment Indicator
            *   `10  FILLER                       PIC X(13).`  Description: Filler

    *   `01  PPS-DATA-ALL.`
        *   Description: This structure is used to pass calculated PPS (Prospective Payment System) data back to the calling program.
            *   `05  PPS-RTC                       PIC 9(02).`  Description: Return Code (PPS)
            *   `05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02).` Description: Charge Threshold
            *   `05  PPS-DATA.`
                *   `10  PPS-MSA                   PIC X(04).`  Description: Metropolitan Statistical Area (MSA)
                *   `10  PPS-WAGE-INDEX            PIC 9(02)V9(04).` Description: Wage Index
                *   `10  PPS-AVG-LOS               PIC 9(02)V9(01).` Description: Average Length of Stay
                *   `10  PPS-RELATIVE-WGT          PIC 9(01)V9(04).` Description: Relative Weight
                *   `10  PPS-OUTLIER-PAY-AMT       PIC 9(07)V9(02).` Description: Outlier Payment Amount
                *   `10  PPS-LOS                   PIC 9(03).`  Description: Length of Stay
                *   `10  PPS-DRG-ADJ-PAY-AMT       PIC 9(07)V9(02).` Description: DRG Adjusted Payment Amount
                *   `10  PPS-FED-PAY-AMT           PIC 9(07)V9(02).` Description: Federal Payment Amount
                *   `10  PPS-FINAL-PAY-AMT         PIC 9(07)V9(02).` Description: Final Payment Amount
                *   `10  PPS-FAC-COSTS             PIC 9(07)V9(02).` Description: Facility Costs
                *   `10  PPS-NEW-FAC-SPEC-RATE     PIC 9(07)V9(02).` Description: New Facility Specific Rate
                *   `10  PPS-OUTLIER-THRESHOLD     PIC 9(07)V9(02).` Description: Outlier Threshold
                *   `10  PPS-SUBM-DRG-CODE         PIC X(03).`  Description: Submitted DRG Code
                *   `10  PPS-CALC-VERS-CD          PIC X(05).`  Description: Calculation Version Code
                *   `10  PPS-REG-DAYS-USED         PIC 9(03).`  Description: Regular Days Used
                *   `10  PPS-LTR-DAYS-USED         PIC 9(03).`  Description: Lifetime Reserve Days Used
                *   `10  PPS-BLEND-YEAR            PIC 9(01).`  Description: Blend Year
                *   `10  PPS-COLA                  PIC 9(01)V9(03).` Description: Cost of Living Adjustment
                *   `10  FILLER                    PIC X(04).`  Description: Filler
            *   `05  PPS-OTHER-DATA.`
                *   `10  PPS-NAT-LABOR-PCT         PIC 9(01)V9(05).` Description: National Labor Percentage
                *   `10  PPS-NAT-NONLABOR-PCT      PIC 9(01)V9(05).` Description: National Non-Labor Percentage
                *   `10  PPS-STD-FED-RATE          PIC 9(05)V9(02).` Description: Standard Federal Rate
                *   `10  PPS-BDGT-NEUT-RATE        PIC 9(01)V9(03).` Description: Budget Neutrality Rate
                *   `10  FILLER                    PIC X(20).`  Description: Filler
            *   `05  PPS-PC-DATA.`
                *   `10  PPS-COT-IND               PIC X(01).`  Description: Cost Outlier Indicator
                *   `10  FILLER                    PIC X(20).`  Description: Filler

    *   `01  PRICER-OPT-VERS-SW.`
        *   Description:  Used to indicate which version of the pricer options is being used.
            *   `05  PRICER-OPTION-SW          PIC X(01).`  Description: Pricer Option Switch
                *   `88  ALL-TABLES-PASSED          VALUE 'A'.`  Description: All tables passed indicator
                *   `88  PROV-RECORD-PASSED         VALUE 'P'.`  Description: Provider record passed indicator
            *   `05  PPS-VERSIONS.`
                *   `10  PPDRV-VERSION         PIC X(05).`  Description: Version of the PPDRV program

    *   `01  PROV-NEW-HOLD.`
        *   Description:  Provider record data passed from calling program.
            *   `02  PROV-NEWREC-HOLD1.`
                *   `05  P-NEW-NPI10.`
                    *   `10  P-NEW-NPI8             PIC X(08).`  Description: New NPI - First 8 characters
                    *   `10  P-NEW-NPI-FILLER       PIC X(02).`  Description: New NPI - Filler
                *   `05  P-NEW-PROVIDER-NO.`
                    *   `10  P-NEW-STATE            PIC 9(02).`  Description: New State
                    *   `10  FILLER                 PIC X(04).`  Description: Filler
                *   `05  P-NEW-DATE-DATA.`
                    *   `10  P-NEW-EFF-DATE.`
                        *   `15  P-NEW-EFF-DT-CC    PIC 9(02).`  Description: Effective Date - Century
                        *   `15  P-NEW-EFF-DT-YY    PIC 9(02).`  Description: Effective Date - Year
                        *   `15  P-NEW-EFF-DT-MM    PIC 9(02).`  Description: Effective Date - Month
                        *   `15  P-NEW-EFF-DT-DD    PIC 9(02).`  Description: Effective Date - Day
                    *   `10  P-NEW-FY-BEGIN-DATE.`
                        *   `15  P-NEW-FY-BEG-DT-CC PIC 9(02).`  Description: Fiscal Year Begin Date - Century
                        *   `15  P-NEW-FY-BEG-DT-YY PIC 9(02).`  Description: Fiscal Year Begin Date - Year
                        *   `15  P-NEW-FY-BEG-DT-MM PIC 9(02).`  Description: Fiscal Year Begin Date - Month
                        *   `15  P-NEW-FY-BEG-DT-DD PIC 9(02).`  Description: Fiscal Year Begin Date - Day
                    *   `10  P-NEW-REPORT-DATE.`
                        *   `15  P-NEW-REPORT-DT-CC PIC 9(02).`  Description: Report Date - Century
                        *   `15  P-NEW-REPORT-DT-YY PIC 9(02).`  Description: Report Date - Year
                        *   `15  P-NEW-REPORT-DT-MM PIC 9(02).`  Description: Report Date - Month
                        *   `15  P-NEW-