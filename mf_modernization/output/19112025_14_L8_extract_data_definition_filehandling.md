# Step 1: Program Overview

## Program: LTCAL032

### Overview
- This COBOL program, LTCAL032, is a subroutine that calculates PPS (Prospective Payment System) payments for Long-Term Care (LTC) facilities. It receives bill data and provider information as input, performs edits, assembles pricing components, calculates payments (including outliers and short stay adjustments), and returns the results. It uses a copybook `LTDRG031` for DRG (Diagnosis Related Group) information.

### Business Functions
-   Receives bill and provider data.
-   Validates input data.
-   Retrieves DRG information.
-   Calculates PPS payments.
-   Calculates outlier payments.
-   Handles short-stay payments.
-   Applies blending rules based on the facility's blend year.
-   Returns payment information and return codes.

### Data Structures
-   **BILL-NEW-DATA (LINKAGE SECTION):** Contains bill-related data, including provider information, patient status, DRG code, LOS, covered days, charges, and discharge date.
-   **PPS-DATA-ALL (LINKAGE SECTION):** Contains the PPS calculation results.
-   **PRICER-OPT-VERS-SW (LINKAGE SECTION):** Contains flags for passing different versions.
-   **PROV-NEW-HOLD (LINKAGE SECTION):** Contains provider-specific data.
-   **WAGE-NEW-INDEX-RECORD (LINKAGE SECTION):** Contains Wage index data.
-   **HOLD-PPS-COMPONENTS (WORKING-STORAGE SECTION):**  Intermediate storage for calculation components.
-   **W-STORAGE-REF (WORKING-STORAGE SECTION):** Contains the program name.
-   **CAL-VERSION (WORKING-STORAGE SECTION):** Stores the calculation version.
-   **W-DRG-FILLS (WORKING-STORAGE SECTION):**  Data for DRG lookup table.
-   **W-DRG-TABLE (WORKING-STORAGE SECTION):**  Redefines `W-DRG-FILLS` to access DRG data.
-   **WWM-ENTRY (WORKING-STORAGE SECTION):**  DRG table entry containing WWM-DRG, WWM-RELWT, and WWM-ALOS.

### Execution Order
-   0100-INITIAL-ROUTINE: Initializes variables.
-   1000-EDIT-THE-BILL-INFO: Edits input bill data.
-   1700-EDIT-DRG-CODE: Searches for DRG code in the DRG table.
-   2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables.
-   3000-CALC-PAYMENT: Calculates the standard payment amount.
-   7000-CALC-OUTLIER: Calculates outlier payments.
-   8000-BLEND: Applies blending rules.
-   9000-MOVE-RESULTS: Moves the results to the output variables.

### Rules
-   PPS-RTC values indicate the payment method or error conditions.
-   Blending rules are applied based on the PPS-BLEND-YEAR.
-   Outlier payments are calculated if the facility costs exceed the outlier threshold.
-   Short-stay payments are calculated under certain conditions.

### External System Interactions
-   Uses COPY LTDRG031 to include a DRG table.

## Program: LTCAL042

### Overview
- This COBOL program, LTCAL042, is a subroutine that calculates PPS (Prospective Payment System) payments for Long-Term Care (LTC) facilities. It receives bill data and provider information as input, performs edits, assembles pricing components, calculates payments (including outliers and short stay adjustments), and returns the results. It uses a copybook `LTDRG031` for DRG (Diagnosis Related Group) information.

### Business Functions
-   Receives bill and provider data.
-   Validates input data.
-   Retrieves DRG information.
-   Calculates PPS payments.
-   Calculates outlier payments.
-   Handles short-stay payments.
-   Applies blending rules based on the facility's blend year.
-   Returns payment information and return codes.

### Data Structures
-   **BILL-NEW-DATA (LINKAGE SECTION):** Contains bill-related data, including provider information, patient status, DRG code, LOS, covered days, charges, and discharge date.
-   **PPS-DATA-ALL (LINKAGE SECTION):** Contains the PPS calculation results.
-   **PRICER-OPT-VERS-SW (LINKAGE SECTION):** Contains flags for passing different versions.
-   **PROV-NEW-HOLD (LINKAGE SECTION):** Contains provider-specific data.
-   **WAGE-NEW-INDEX-RECORD (LINKAGE SECTION):** Contains Wage index data.
-   **HOLD-PPS-COMPONENTS (WORKING-STORAGE SECTION):**  Intermediate storage for calculation components.
-   **W-STORAGE-REF (WORKING-STORAGE SECTION):** Contains the program name.
-   **CAL-VERSION (WORKING-STORAGE SECTION):** Stores the calculation version.
-   **W-DRG-FILLS (WORKING-STORAGE SECTION):**  Data for DRG lookup table.
-   **W-DRG-TABLE (WORKING-STORAGE SECTION):**  Redefines `W-DRG-FILLS` to access DRG data.
-   **WWM-ENTRY (WORKING-STORAGE SECTION):**  DRG table entry containing WWM-DRG, WWM-RELWT, and WWM-ALOS.

### Execution Order
-   0100-INITIAL-ROUTINE: Initializes variables.
-   1000-EDIT-THE-BILL-INFO: Edits input bill data.
-   1700-EDIT-DRG-CODE: Searches for DRG code in the DRG table.
-   2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables.
-   3000-CALC-PAYMENT: Calculates the standard payment amount.
-   7000-CALC-OUTLIER: Calculates outlier payments.
-   8000-BLEND: Applies blending rules.
-   9000-MOVE-RESULTS: Moves the results to the output variables.

### Rules
-   PPS-RTC values indicate the payment method or error conditions.
-   Blending rules are applied based on the PPS-BLEND-YEAR.
-   Outlier payments are calculated if the facility costs exceed the outlier threshold.
-   Short-stay payments are calculated under certain conditions.

### External System Interactions
-   Uses COPY LTDRG031 to include a DRG table.

## Program: LTDRG031

### Overview
- This is a COBOL copybook that contains the DRG (Diagnosis Related Group) lookup table used by LTCAL032 and LTCAL042. It stores DRG codes and associated data, such as relative weights and average length of stay.

### Business Functions
-   Provides DRG codes and associated data for payment calculations.

### Data Structures
-   **W-DRG-FILLS (WORKING-STORAGE SECTION):**  Data for DRG lookup table.
-   **W-DRG-TABLE (WORKING-STORAGE SECTION):**  Redefines `W-DRG-FILLS` to access DRG data.
-   **WWM-ENTRY (WORKING-STORAGE SECTION):**  DRG table entry containing WWM-DRG, WWM-RELWT, and WWM-ALOS.

### External System Interactions
-   None.  This is a data definition.

# Step 2: Data Definition and File Handling

## Program: LTCAL032

### Files Accessed
-   None. Uses a copybook (LTDRG031) containing a DRG table.

### Data Structures (WORKING-STORAGE SECTION)
-   **W-STORAGE-REF:**  `PIC X(46)` - Contains the program name, used for identification.
-   **CAL-VERSION:**  `PIC X(05)` -  Stores the calculation version, e.g., 'C03.2'.
-   **HOLD-PPS-COMPONENTS:**  A group of fields used to store intermediate calculation results, including:
    -   **H-LOS:**  `PIC 9(03)` - Length of stay.
    -   **H-REG-DAYS:** `PIC 9(03)` - Regular days.
    -   **H-TOTAL-DAYS:** `PIC 9(05)` - Total days.
    -   **H-SSOT:**  `PIC 9(02)` - Short Stay Outlier Threshold.
    -   **H-BLEND-RTC:** `PIC 9(02)` - Blend Return Code.
    -   **H-BLEND-FAC:** `PIC 9(01)V9(01)` - Blend Facility Factor.
    -   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - Blend PPS Factor.
    -   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    -   **H-SS-COST:**  `PIC 9(07)V9(02)` - Short Stay Cost.
    -   **H-LABOR-PORTION:**  `PIC 9(07)V9(06)` - Labor Portion.
    -   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Non-Labor Portion.
    -   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Fixed Loss Amount.
    -   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.
-   **W-DRG-FILLS:** `PIC X(44) VALUE ...` - Contains the DRG data in a packed format.
-   **W-DRG-TABLE REDEFINES W-DRG-FILLS:**  Provides structured access to the DRG data:
    -   **WWM-ENTRY OCCURS 502 TIMES INDEXED BY WWM-INDX:**  The DRG table entries.
        -   **WWM-DRG:** `PIC X(3)` - DRG code.
        -   **WWM-RELWT:** `PIC 9(1)V9(4)` - Relative weight for the DRG.
        -   **WWM-ALOS:** `PIC 9(2)V9(1)` - Average length of stay for the DRG.

### Data Structures (LINKAGE SECTION)
-   **BILL-NEW-DATA:** Contains bill-related data passed from the calling program:
    -   **B-NPI10:** National Provider Identifier (NPI)
        -   **B-NPI8:** `PIC X(08)` - The NPI (8 characters).
        -   **B-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
    -   **B-PROVIDER-NO:** `PIC X(06)` - Provider number.
    -   **B-PATIENT-STATUS:** `PIC X(02)` - Patient status.
    -   **B-DRG-CODE:** `PIC X(03)` - DRG code.
    -   **B-LOS:** `PIC 9(03)` - Length of stay.
    -   **B-COV-DAYS:** `PIC 9(03)` - Covered days.
    -   **B-LTR-DAYS:** `PIC 9(02)` - Lifetime Reserve Days.
    -   **B-DISCHARGE-DATE:** Discharge date components.
        -   **B-DISCHG-CC:** `PIC 9(02)` - Century.
        -   **B-DISCHG-YY:** `PIC 9(02)` - Year.
        -   **B-DISCHG-MM:** `PIC 9(02)` - Month.
        -   **B-DISCHG-DD:** `PIC 9(02)` - Day.
    -   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Covered charges.
    -   **B-SPEC-PAY-IND:** `PIC X(01)` - Special payment indicator.
    -   **FILLER:** `PIC X(13)` - Unused filler.
-   **PPS-DATA-ALL:**  Contains the results calculated by the program:
    -   **PPS-RTC:** `PIC 9(02)` - Return code (PPS-RTC).
    -   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Charge Threshold.
    -   **PPS-DATA:**  PPS data.
        -   **PPS-MSA:**  `PIC X(04)` - Metropolitan Statistical Area (MSA).
        -   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Wage index.
        -   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Average length of stay.
        -   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Relative weight.
        -   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Outlier payment amount.
        -   **PPS-LOS:** `PIC 9(03)` - Length of stay.
        -   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - DRG adjusted payment amount.
        -   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Federal payment amount.
        -   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Final payment amount.
        -   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Facility Costs.
        -   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - New Facility Specific Rate.
        -   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Outlier Threshold.
        -   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Submitted DRG code.
        -   **PPS-CALC-VERS-CD:** `PIC X(05)` - Calculation version code.
        -   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Regular Days Used.
        -   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Lifetime Reserve Days Used.
        -   **PPS-BLEND-YEAR:** `PIC 9(01)` - Blend Year.
        -   **PPS-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        -   **FILLER:** `PIC X(04)` - Filler
    -   **PPS-OTHER-DATA:** Other PPS data.
        -   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)` - National Labor Percentage.
        -   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        -   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)` - Standard Federal Rate.
        -   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        -   **FILLER:** `PIC X(20)` - Filler.
    -   **PPS-PC-DATA:** PPS PC data.
        -   **PPS-COT-IND:** `PIC X(01)` - Cost Outlier Indicator.
        -   **FILLER:** `PIC X(20)` - Filler.
-   **PRICER-OPT-VERS-SW:**  Pricer Option and Version Switch
    -   **PRICER-OPTION-SW:** `PIC X(01)` - Option Switch.
        -   **ALL-TABLES-PASSED:** `VALUE 'A'`
        -   **PROV-RECORD-PASSED:** `VALUE 'P'`
    -   **PPS-VERSIONS:**  PPS Version.
        -   **PPDRV-VERSION:** `PIC X(05)` - PPDRV Version.
-   **PROV-NEW-HOLD:**  Provider record data.
    -   **PROV-NEWREC-HOLD1:**  Provider record hold 1.
        -   **P-NEW-NPI10:** New NPI data.
            -   **P-NEW-NPI8:** `PIC X(08)` -  New NPI.
            -   **P-NEW-NPI-FILLER:** `PIC X(02)` - NPI Filler.
        -   **P-NEW-PROVIDER-NO:**  Provider number.
            -   **P-NEW-STATE:** `PIC 9(02)` - State.
            -   **FILLER:** `PIC X(04)` - Filler.
        -   **P-NEW-DATE-DATA:** Date Data.
            -   **P-NEW-EFF-DATE:** Effective Date.
                -   **P-NEW-EFF-DT-CC:** `PIC 9(02)` - Century.
                -   **P-NEW-EFF-DT-YY:** `PIC 9(02)` - Year.
                -   **P-NEW-EFF-DT-MM:** `PIC 9(02)` - Month.
                -   **P-NEW-EFF-DT-DD:** `PIC 9(02)` - Day.
            -   **P-NEW-FY-BEGIN-DATE:** Fiscal Year Begin Date.
                -   **P-NEW-FY-BEG-DT-CC:** `PIC 9(02)` - Century.
                -   **P-NEW-FY-BEG-DT-YY:** `PIC 9(02)` - Year.
                -   **P-NEW-FY-BEG-DT-MM:** `PIC 9(02)` - Month.
                -   **P-NEW-FY-BEG-DT-DD:** `PIC 9(02)` - Day.
            -   **P-NEW-REPORT-DATE:** Report Date.
                -   **P-NEW-REPORT-DT-CC:** `PIC 9(02)` - Century.
                -   **P-NEW-REPORT-DT-YY:** `PIC 9(02)` - Year.
                -   **P-NEW-REPORT-DT-MM:** `PIC 9(02)` - Month.
                -   **P-NEW-REPORT-DT-DD:** `PIC 9(02)` - Day.
            -   **P-NEW-TERMINATION-DATE:** Termination date.
                -   **P-NEW-TERM-DT-CC:** `PIC 9(02)` - Century.
                -   **P-NEW-TERM-DT-YY:** `PIC 9(02)` - Year.
                -   **P-NEW-TERM-DT-MM:** `PIC 9(02)` - Month.
                -   **P-NEW-TERM-DT-DD:** `PIC 9(02)` - Day.
        -   **P-NEW-WAIVER-CODE:** `PIC X(01)` - Waiver code.
            -   **P-NEW-WAIVER-STATE:** `VALUE 'Y'` - Waiver state.
        -   **P-NEW-INTER-NO:** `PIC 9(05)` - Internal number.
        -   **P-NEW-PROVIDER-TYPE:** `PIC X(02)` - Provider type.
        -   **P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current census division.
        -   **P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV:** `PIC 9(01)` - Current division.
        -   **P-NEW-MSA-DATA:** MSA Data.
            -   **P-NEW-CHG-CODE-INDEX:** `PIC X` - Charge Code Index.
            -   **P-NEW-GEO-LOC-MSAX:** `PIC X(04) JUST RIGHT` - Geo Location MSA.
            -   **P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX:** `PIC 9(04)` - Geo Location MSA9.
            -   **P-NEW-WAGE-INDEX-LOC-MSA:** `PIC X(04) JUST RIGHT` - Wage Index Location MSA.
            -   **P-NEW-STAND-AMT-LOC-MSA:** `PIC X(04) JUST RIGHT` - Standard Amount Location MSA.
            -   **P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA:** Standard Amount Location MSA9.
                -   **P-NEW-RURAL-1ST:** Rural 1st.
                    -   **P-NEW-STAND-RURAL:** `PIC XX` - Standard Rural.
                        -   **P-NEW-STD-RURAL-CHECK:** `VALUE '  '` - Standard Rural Check.
                    -   **P-NEW-RURAL-2ND:** `PIC XX` - Rural 2nd.
        -   **P-NEW-SOL-COM-DEP-HOSP-YR:** `PIC XX` - Sol Com Dep Hosp Year.
        -   **P-NEW-LUGAR:** `PIC X` - Lugar.
        -   **P-NEW-TEMP-RELIEF-IND:** `PIC X` - Temp Relief Indicator.
        -   **P-NEW-FED-PPS-BLEND-IND:** `PIC X` - Fed PPS Blend Indicator.
        -   **FILLER:** `PIC X(05)` - Filler.
    -   **PROV-NEWREC-HOLD2:**  Provider record hold 2.
        -   **P-NEW-VARIABLES:** Variables.
            -   **P-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - Facility Specific Rate.
            -   **P-NEW-COLA:** `PIC 9(01)V9(03)` - COLA.
            -   **P-NEW-INTERN-RATIO:** `PIC 9(01)V9(04)` - Intern Ratio.
            -   **P-NEW-BED-SIZE:** `PIC 9(05)` - Bed size.
            -   **P-NEW-OPER-CSTCHG-RATIO:** `PIC 9(01)V9(03)` - Operating Cost to Charge Ratio.
            -   **P-NEW-CMI:** `PIC 9(01)V9(04)` - CMI.
            -   **P-NEW-SSI-RATIO:** `PIC V9(04)` - SSI Ratio.
            -   **P-NEW-MEDICAID-RATIO:** `PIC V9(04)` - Medicaid Ratio.
            -   **P-NEW-PPS-BLEND-YR-IND:** `PIC 9(01)` - PPS Blend Year Indicator.
            -   **P-NEW-PRUF-UPDTE-FACTOR:** `PIC 9(01)V9(05)` - PRUF Update Factor.
            -   **P-NEW-DSH-PERCENT:** `PIC V9(04)` - DSH Percent.
            -   **P-NEW-FYE-DATE:** `PIC X(08)` - FYE Date.
        -   **FILLER:** `PIC X(23)` - Filler.
    -   **PROV-NEWREC-HOLD3:** Provider record hold 3.
        -   **P-NEW-PASS-AMT-DATA:** Passed Amount Data.
            -   **P-NEW-PASS-AMT-CAPITAL:** `PIC 9(04)V99` - Capital Amount.
            -   **P-NEW-PASS-AMT-DIR-MED-ED:** `PIC 9(04)V99` - Direct Medical Education Amount.
            -   **P-NEW-PASS-AMT-ORGAN-ACQ:** `PIC 9(04)V99` - Organ Acquisition Amount.
            -   **P-NEW-PASS-AMT-PLUS-MISC:** `PIC 9(04)V99` - Plus Miscellaneous Amount.
        -   **P-NEW-CAPI-DATA:** Capital Data.
            -   **P-NEW-CAPI-PPS-PAY-CODE:** `PIC X` - Capi PPS Pay Code.
            -   **P-NEW-CAPI-HOSP-SPEC-RATE:** `PIC 9(04)V99` - Hospital Specific Rate.
            -   **P-NEW-CAPI-OLD-HARM-RATE:** `PIC 9(04)V99` - Old Harm Rate.
            -   **P-NEW-CAPI-NEW-HARM-RATIO:** `PIC 9(01)V9999` - New Harm Ratio.
            -   **P-NEW-CAPI-CSTCHG-RATIO:** `PIC 9V999` - Cost to Charge Ratio.
            -   **P-NEW-CAPI-NEW-HOSP:** `PIC X` - New Hospital.
            -   **P-NEW-CAPI-IME:** `PIC 9V9999` - IME.
            -   **P-NEW-CAPI-EXCEPTIONS:** `PIC 9(04)V99` - Exceptions.
        -   **FILLER:** `PIC X(22)` - Filler.
-   **WAGE-NEW-INDEX-RECORD:** Wage Index Record.
    -   **W-MSA:** `PIC X(4)` - MSA (Metropolitan Statistical Area).
    -   **W-EFF-DATE:** `PIC X(8)` - Effective date.
    -   **W-WAGE-INDEX1:** `PIC S9(02)V9(04)` - Wage index 1.
    -   **W-WAGE-INDEX2:** `PIC S9(02)V9(04)` - Wage index 2.
    -   **W-WAGE-INDEX3:** `PIC S9(02)V9(04)` - Wage index 3.

## Program: LTCAL042

### Files Accessed
-   None. Uses a copybook (LTDRG031) containing a DRG table.

### Data Structures (WORKING-STORAGE SECTION)
-   **W-STORAGE-REF:**  `PIC X(46)` - Contains the program name, used for identification.
-   **CAL-VERSION:**  `PIC X(05)` -  Stores the calculation version, e.g., 'C04.2'.
-   **HOLD-PPS-COMPONENTS:**  A group of fields used to store intermediate calculation results, including:
    -   **H-LOS:**  `PIC 9(03)` - Length of stay.
    -   **H-REG-DAYS:** `PIC 9(03)` - Regular days.
    -   **H-TOTAL-DAYS:** `PIC 9(05)` - Total days.
    -   **H-SSOT:**  `PIC 9(02)` - Short Stay Outlier Threshold.
    -   **H-BLEND-RTC:** `PIC 9(02)` - Blend Return Code.
    -   **H-BLEND-FAC:** `PIC 9(01)V9(01)` - Blend Facility Factor.
    -   **H-BLEND-PPS:** `PIC 9(01)V9(01)` - Blend PPS Factor.
    -   **H-SS-PAY-AMT:** `PIC 9(07)V9(02)` - Short Stay Payment Amount.
    -   **H-SS-COST:**  `PIC 9(07)V9(02)` - Short Stay Cost.
    -   **H-LABOR-PORTION:**  `PIC 9(07)V9(06)` - Labor Portion.
    -   **H-NONLABOR-PORTION:** `PIC 9(07)V9(06)` - Non-Labor Portion.
    -   **H-FIXED-LOSS-AMT:** `PIC 9(07)V9(02)` - Fixed Loss Amount.
    -   **H-NEW-FAC-SPEC-RATE:** `PIC 9(05)V9(02)` - New Facility Specific Rate.
    -   **H-LOS-RATIO:** `PIC 9(01)V9(05)` - LOS Ratio.
-   **W-DRG-FILLS:** `PIC X(44) VALUE ...` - Contains the DRG data in a packed format.
-   **W-DRG-TABLE REDEFINES W-DRG-FILLS:**  Provides structured access to the DRG data:
    -   **WWM-ENTRY OCCURS 502 TIMES INDEXED BY WWM-INDX:**  The DRG table entries.
        -   **WWM-DRG:** `PIC X(3)` - DRG code.
        -   **WWM-RELWT:** `PIC 9(1)V9(4)` - Relative weight for the DRG.
        -   **WWM-ALOS:** `PIC 9(2)V9(1)` - Average length of stay for the DRG.

### Data Structures (LINKAGE SECTION)
-   **BILL-NEW-DATA:** Contains bill-related data passed from the calling program:
    -   **B-NPI10:** National Provider Identifier (NPI)
        -   **B-NPI8:** `PIC X(08)` - The NPI (8 characters).
        -   **B-NPI-FILLER:** `PIC X(02)` - Filler for NPI.
    -   **B-PROVIDER-NO:** `PIC X(06)` - Provider number.
    -   **B-PATIENT-STATUS:** `PIC X(02)` - Patient status.
    -   **B-DRG-CODE:** `PIC X(03)` - DRG code.
    -   **B-LOS:** `PIC 9(03)` - Length of stay.
    -   **B-COV-DAYS:** `PIC 9(03)` - Covered days.
    -   **B-LTR-DAYS:** `PIC 9(02)` - Lifetime Reserve Days.
    -   **B-DISCHARGE-DATE:** Discharge date components.
        -   **B-DISCHG-CC:** `PIC 9(02)` - Century.
        -   **B-DISCHG-YY:** `PIC 9(02)` - Year.
        -   **B-DISCHG-MM:** `PIC 9(02)` - Month.
        -   **B-DISCHG-DD:** `PIC 9(02)` - Day.
    -   **B-COV-CHARGES:** `PIC 9(07)V9(02)` - Covered charges.
    -   **B-SPEC-PAY-IND:** `PIC X(01)` - Special payment indicator.
    -   **FILLER:** `PIC X(13)` - Unused filler.
-   **PPS-DATA-ALL:**  Contains the results calculated by the program:
    -   **PPS-RTC:** `PIC 9(02)` - Return code (PPS-RTC).
    -   **PPS-CHRG-THRESHOLD:** `PIC 9(07)V9(02)` - Charge Threshold.
    -   **PPS-DATA:**  PPS data.
        -   **PPS-MSA:**  `PIC X(04)` - Metropolitan Statistical Area (MSA).
        -   **PPS-WAGE-INDEX:** `PIC 9(02)V9(04)` - Wage index.
        -   **PPS-AVG-LOS:** `PIC 9(02)V9(01)` - Average length of stay.
        -   **PPS-RELATIVE-WGT:** `PIC 9(01)V9(04)` - Relative weight.
        -   **PPS-OUTLIER-PAY-AMT:** `PIC 9(07)V9(02)` - Outlier payment amount.
        -   **PPS-LOS:** `PIC 9(03)` - Length of stay.
        -   **PPS-DRG-ADJ-PAY-AMT:** `PIC 9(07)V9(02)` - DRG adjusted payment amount.
        -   **PPS-FED-PAY-AMT:** `PIC 9(07)V9(02)` - Federal payment amount.
        -   **PPS-FINAL-PAY-AMT:** `PIC 9(07)V9(02)` - Final payment amount.
        -   **PPS-FAC-COSTS:** `PIC 9(07)V9(02)` - Facility Costs.
        -   **PPS-NEW-FAC-SPEC-RATE:** `PIC 9(07)V9(02)` - New Facility Specific Rate.
        -   **PPS-OUTLIER-THRESHOLD:** `PIC 9(07)V9(02)` - Outlier Threshold.
        -   **PPS-SUBM-DRG-CODE:** `PIC X(03)` - Submitted DRG code.
        -   **PPS-CALC-VERS-CD:** `PIC X(05)` - Calculation version code.
        -   **PPS-REG-DAYS-USED:** `PIC 9(03)` - Regular Days Used.
        -   **PPS-LTR-DAYS-USED:** `PIC 9(03)` - Lifetime Reserve Days Used.
        -   **PPS-BLEND-YEAR:** `PIC 9(01)` - Blend Year.
        -   **PPS-COLA:** `PIC 9(01)V9(03)` - Cost of Living Adjustment.
        -   **FILLER:** `PIC X(04)` - Filler
    -   **PPS-OTHER-DATA:** Other PPS data.
        -   **PPS-NAT-LABOR-PCT:** `PIC 9(01)V9(05)` - National Labor Percentage.
        -   **PPS-NAT-NONLABOR-PCT:** `PIC 9(01)V9(05)` - National Non-Labor Percentage.
        -   **PPS-STD-FED-RATE:** `PIC 9(05)V9(02)` - Standard Federal Rate.
        -   **PPS-BDGT-NEUT-RATE:** `PIC 9(01)V9(03)` - Budget Neutrality Rate.
        -   **FILLER:** `PIC X(20)` - Filler.
    -   **PPS-PC-DATA:** PPS PC data.
        -   **PPS-COT-IND:** `PIC X(01)` - Cost Outlier Indicator.
        -   **FILLER:** `PIC X(20)` - Filler.
-   **PRICER-OPT-VERS-SW:**  Pricer Option and Version Switch
    -   **PRICER-OPTION-SW:** `PIC