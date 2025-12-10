Here's an analysis of each COBOL program provided:

---

### Program: IPDRG080

**1. Files Accessed:**

*   **None:** This program appears to be a data definition program. It defines data structures within its own WORKING-STORAGE SECTION, likely intended to be `COPY`-ed into other programs. There are no `SELECT` statements or `FILE SECTION` entries indicating file access.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **DRG-TABLE:**
    *   **Description:** This is the main data structure, acting as a large table.
    *   **D-TAB:**
        *   **Description:** A contiguous block of data, likely representing a table of DRG (Diagnosis Related Group) information. It starts with an 8-byte date and is followed by multiple 56-byte records.
        *   **FILLER (8 bytes):** Likely holds an effective date for the DRG table.
        *   **FILLER (56 bytes):** Repeats many times, each holding a segment of DRG data. The exact interpretation of these 56-byte segments would depend on how they are processed by other programs.
    *   **DRGX-TAB REDEFINES D-TAB:**
        *   **Description:** This redefines the `D-TAB` to provide a more structured view of the DRG data, allowing for indexed access.
        *   **DRGX-PERIOD OCCURS 1 INDEXED BY DX5:**
            *   **Description:** Represents a single period for the DRG table. The `INDEXED BY DX5` clause indicates it can be accessed using an index named `DX5`.
            *   **DRGX-EFF-DATE PIC X(08):** Holds the effective date for this period of the DRG table.
            *   **DRG-DATA OCCURS 1000 INDEXED BY DX6:**
                *   **Description:** An array of 1000 records, each representing specific DRG data points. It can be accessed using an index named `DX6`.
                *   **DRG-WT PIC 9(02)V9(04):** Likely represents the relative weight for a DRG.
                *   **DRG-ALOS PIC 9(02)V9(01):** Likely represents the Average Length of Stay for a DRG.
                *   **DRG-DAYS-TRIM PIC 9(02):** Likely represents trimmed days for a DRG.
                *   **DRG-ARITH-ALOS PIC 9(02)V9(01):** Likely represents an arithmetic Average Length of Stay for a DRG.

**3. Data Structures in LINKAGE SECTION:**

*   **None:** This program does not have a `LINKAGE SECTION`.

---

### Program: IPDRG090

**1. Files Accessed:**

*   **None:** Similar to IPDRG080, this program defines data structures that are likely intended to be `COPY`-ed into other programs. There are no file control entries or file section definitions.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **DRG-TABLE:**
    *   **Description:** This is the main data structure, similar to the one in IPDRG080, representing a table of DRG information.
    *   **D-TAB:**
        *   **Description:** A contiguous block of data, likely a table of DRG information. It starts with an 8-byte date and is followed by multiple 56-byte records.
        *   **FILLER (8 bytes):** Likely holds an effective date for the DRG table.
        *   **FILLER (56 bytes):** Repeats many times, each holding a segment of DRG data. The exact interpretation of these 56-byte segments would depend on how they are processed by other programs.
    *   **DRGX-TAB REDEFINES D-TAB:**
        *   **Description:** This redefines the `D-TAB` to provide a more structured view of the DRG data, allowing for indexed access.
        *   **DRGX-PERIOD OCCURS 1 INDEXED BY DX5:**
            *   **Description:** Represents a single period for the DRG table. The `INDEXED BY DX5` clause indicates it can be accessed using an index named `DX5`.
            *   **DRGX-EFF-DATE PIC X(08):** Holds the effective date for this period of the DRG table.
            *   **DRG-DATA OCCURS 1000 INDEXED BY DX6:**
                *   **Description:** An array of 1000 records, each representing specific DRG data points. It can be accessed using an index named `DX6`.
                *   **DRG-WT PIC 9(02)V9(04):** Likely represents the relative weight for a DRG.
                *   **DRG-ALOS PIC 9(02)V9(01):** Likely represents the Average Length of Stay for a DRG.
                *   **DRG-DAYS-TRIM PIC 9(02):** Likely represents trimmed days for a DRG.
                *   **DRG-ARITH-ALOS PIC 9(02)V9(01):** Likely represents an arithmetic Average Length of Stay for a DRG.

**3. Data Structures in LINKAGE SECTION:**

*   **None:** This program does not have a `LINKAGE SECTION`.

---

### Program: IRFBN091

**1. Files Accessed:**

*   **None:** This program defines data structures, and there are no file access statements. It appears to be a data definition program.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **PPS-SSRFBN-TABLE:**
    *   **Description:** A table containing SSRFBN (State Specific Rate File - Benefit?) data, likely for different states and their associated rates.
    *   **WK-SSRFBN-DATA:**
        *   **Description:** A raw data area holding the SSRFBN table entries.
        *   **FILLER (PIC X(57)):** Each of these 57-byte fields represents a single record in the SSRFBN table, containing a state code, rate, and other information.
    *   **WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA:**
        *   **Description:** Redefines `WK-SSRFBN-DATA` to provide a structured, tabular view of the SSRFBN data.
        *   **SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX:**
            *   **Description:** An array of 72 records, sorted by `WK-SSRFBN-STATE`, which can be accessed using the index `SSRFBN-IDX`.
            *   **WK-SSRFBN-REASON-ALL:** A group item containing the individual fields for each SSRFBN record.
                *   **WK-SSRFBN-STATE PIC 99:** The state code (likely a two-digit numeric code).
                *   **FILLER PIC XX:** Unused characters.
                *   **WK-SSRFBN-RATE PIC 9(1)V9(5):** The specific rate associated with the state and reason.
                *   **FILLER PIC XX:** Unused characters.
                *   **WK-SSRFBN-CODE2 PIC 99:** A secondary code, possibly related to the reason or rate.
                *   **FILLER PIC X:** Unused character.
                *   **WK-SSRFBN-STNAM PIC X(20):** The name of the state.
                *   **WK-SSRFBN-REST PIC X(22):** Remaining data for the record.

*   **MES-ADD-PROV PIC X(53) VALUE SPACES:** A working variable, likely for holding messages related to adding providers.
*   **MES-CHG-PROV PIC X(53) VALUE SPACES:** A working variable, likely for holding messages related to changing providers.
*   **MES-PPS-STATE PIC X(02):** A working variable for a PPS state code.
*   **MES-INTRO PIC X(53) VALUE SPACES:** A working variable, likely for holding introductory messages.
*   **MES-TOT-PAY PIC 9(07)V9(02) VALUE 0:** A working variable to hold a total payment amount, initialized to zero.
*   **MES-SSRFBN:**
    *   **Description:** A structure that mirrors the `SSRFBN-TAB` record layout, likely used to hold a single SSRFBN record for processing or display.
    *   **MES-SSRFBN-STATE PIC 99:** State code.
    *   **FILLER PIC XX:** Unused characters.
    *   **MES-SSRFBN-RATE PIC 9(1)V9(5):** Rate.
    *   **FILLER PIC XX:** Unused characters.
    *   **MES-SSRFBN-CODE2 PIC 99:** Secondary code.
    *   **FILLER PIC X:** Unused character.
    *   **MES-SSRFBN-STNAM PIC X(20):** State name.
    *   **MES-SSRFBN-REST PIC X(22):** Remaining data.

**3. Data Structures in LINKAGE SECTION:**

*   **None:** This program does not have a `LINKAGE SECTION`.

---

### Program: LTCAL087

**1. Files Accessed:**

*   **None:** This program does not explicitly define any files in the `FILE SECTION`. It utilizes `COPY` statements for data definitions and uses variables passed through the `PROCEDURE DIVISION USING` clause.

**2. Data Structures in WORKING-STORAGE SECTION:**

*   **W-STORAGE-REF PIC X(46) VALUE 'LTCAL087 - W O R K I N G S T O R A G E':** A descriptive field indicating the program's working storage.
*   **CAL-VERSION PIC X(05) VALUE 'V08.7':** Stores the version of the calculation program.
*   **PROGRAM-CONSTANTS:**
    *   **Description:** Holds constant values for fiscal year beginnings.
    *   **FED-FY-BEGIN-03 PIC 9(08) VALUE 20021001:** Fiscal Year beginning date (YYYYMMDD).
    *   **FED-FY-BEGIN-04 PIC 9(08) VALUE 20031001:** Fiscal Year beginning date (YYYYMMDD).
    *   **FED-FY-BEGIN-05 PIC 9(08) VALUE 20041001:** Fiscal Year beginning date (YYYYMMDD).
    *   **FED-FY-BEGIN-06 PIC 9(08) VALUE 20051001:** Fiscal Year beginning date (YYYYMMDD).
    *   **FED-FY-BEGIN-07 PIC 9(08) VALUE 20061001:** Fiscal Year beginning date (YYYYMMDD).
*   **LTDRG086:**
    *   **Description:** This `COPY` statement includes data structures defined in the `LTDRG086` program. Based on the context, this likely contains tables and definitions related to Long-Term Care Hospital (LTCH) DRG pricing.
*   **IPDRG080:**
    *   **Description:** This `COPY` statement includes data structures defined in the `IPDRG080` program. This likely contains tables and definitions related to Inpatient Prospective Payment System (IPPS) DRG pricing.
*   **HOLD-PPS-COMPONENTS:**
    *   **Description:** A group of variables used to hold calculated components for PPS (Prospective Payment System) pricing and outlier calculations.
    *   **H-LOS PIC 9(03):** Length of Stay.
    *   **H-REG-DAYS PIC 9(03):** Regular days.
    *   **H-TOTAL-DAYS PIC 9(05):** Total days.
    *   **H-SSOT PIC 9(02)V9(01):** Short Stay Outlier Threshold.
    *   **H-BLEND-RTC PIC 9(02):** Blend Return Code.
    *   **H-BLEND-FAC PIC 9(01)V9(01):** Blend factor for facility rate.
    *   **H-BLEND-PPS PIC 9(01)V9(01):** Blend factor for PPS rate.
    *   **H-SS-PAY-AMT PIC 9(07)V9(02):** Short Stay payment amount.
    *   **H-SS-COST PIC 9(07)V9(02):** Short Stay cost.
    *   **H-LABOR-PORTION PIC 9(07)V9(06):** Labor portion of payment.
    *   **H-NONLABOR-PORTION PIC 9(07)V9(06):** Non-labor portion of payment.
    *   **H-FIXED-LOSS-AMT PIC 9(07)V9(02):** Fixed loss amount for outliers.
    *   **H-NEW-FAC-SPEC-RATE PIC 9(05)V9(02):** New facility specific rate.
    *   **H-LOS-RATIO PIC 9(01)V9(05):** Length of Stay ratio.
    *   **H-OPER-IME-TEACH PIC 9(06)V9(09):** Operating Indirect Medical Education (IME) teaching adjustment.
    *   **H-CAPI-IME-TEACH PIC 9(06)V9(09):** Capital IME teaching adjustment.
    *   **H-LTCH-BLEND-PCT PIC 9(03)V9(04):** LTCH blend percentage.
    *   **H-IPPS-BLEND-PCT PIC 9(03)V9(04):** IPPS blend percentage.
    *   **H-LTCH-BLEND-AMT PIC 9(07)V9(02):** LTCH blend amount.
    *   **H-IPPS-BLEND-AMT PIC 9(07)V9(02):** IPPS blend amount.
    *   **H-INTERN-RATIO PIC 9(01)V9(04):** Intern ratio.
    *   **H-CAPI-IME-RATIO PIC 9V9999:** Capital IME ratio.
    *   **H-BED-SIZE PIC 9(05):** Hospital bed size.
    *   **H-OPER-DSH-PCT PIC V9(04):** Operating Direct Support to Hospitals (DSH) percentage.
    *   **H-SSI-RATIO PIC V9(04):** Supplemental Security Income (SSI) ratio.
    *   **H-MEDICAID-RATIO PIC V9(04):** Medicaid ratio.
    *   **H-OPER-DSH PIC 9(01)V9(04):** Operating DSH amount.
    *   **H-CAPI-DSH PIC 9(01)V9(04):** Capital DSH amount.
    *   **H-GEO-CLASS PIC X(01):** Geographic classification.
    *   **H-URBAN-IND PIC X(01):** Urban indicator.
        *   **URBAN-CBSA (81):** Condition flag for urban CBSA.
        *   **RURAL-CBSA (82):** Condition flag for rural CBSA.
    *   **H-STAND-AMT-OPER-PMT PIC 9(07)V9(02):** Standard amount for operating payment.
    *   **H-PR-STAND-AMT-OPER-PMT PIC 9(07)V9(02):** Puerto Rico standard amount for operating payment.
    *   **H-CAPI-PMT PIC 9(07)V9(02):** Capital payment amount.
    *   **H-PR-CAPI-PMT PIC 9(07)V9(02):** Puerto Rico capital payment amount.
    *   **H-CAPI-GAF PIC 9(05)V9(04):** Capital GAF (Geographic Adjustment Factor).
    *   **H-PR-CAPI-GAF PIC 9(05)V9(04):** Puerto Rico Capital GAF.
    *   **H-LRGURB-ADD-ON PIC 9(01)V9(02):** Large urban add-on.
    *   **H-IPPS-PAY-AMT PIC 9(07)V9(02):** IPPS payment amount.
    *   **H-IPPS-PR-PAY-AMT PIC 9(07)V9(02):** Puerto Rico IPPS payment amount.
    *   **H-IPPS-PER-DIEM PIC 9(07)V9(02):** IPPS per diem amount.
    *   **H-IPPS-PR-PER-DIEM PIC 9(07)V9(02):** Puerto Rico IPPS per diem amount.
    *   **H-SS-BLENDED-PMT PIC 9(07)V9(02):** Short Stay blended payment.
    *   **H-OPER-COLA PIC 9(01)V9(03):** Operating Cost of Living Adjustment (COLA).
    *   **H-CAPI-COLA PIC 9(01)V9(03):** Capital COLA.
    *   **H-IPPS-NAT-LABOR-SHR PIC 9(05)V9(02):** IPPS national labor share.
    *   **H-IPPS-NAT-NONLABOR-SHR PIC 9(05)V9(02):** IPPS national non-labor share.
    *   **H-IPPS-PR-LABOR-SHR PIC 9(05)V9(02):** IPPS Puerto Rico labor share.
    *   **H-IPPS-PR-NONLABOR-SHR PIC 9(05)V9(02):** IPPS Puerto Rico non-labor share.
    *   **H-IPPS-DRG-WGT PIC 9(02)V9(04):** IPPS DRG weight.
    *   **H-IPPS-DRG-ALOS PIC 9(02)V9(01):** IPPS DRG Average Length of Stay.
    *   **H-IPPS-DAYS-CUTOFF PIC 9(02):** IPPS days cutoff.
    *   **H-IPPS-ARITH-ALOS PIC 9(02)V9(01):** IPPS arithmetic ALOS.
    *   **H-IPPS-CAPI-STD-FED-RATE PIC 9(03)V9(02):** IPPS capital standard federal rate.
    *   **H-IPPS-CAPI-STD-PR-RATE PIC 9(03)V9(02):** IPPS capital standard Puerto Rico rate.
    *   **H-NAT-IPPS-PMT-PCT PIC 9(01)V9(02):** National IPPS payment percentage.
    *   **H-PR-IPPS-PMT-PCT PIC 9(01)V9(02):** Puerto Rico IPPS payment percentage.
    *   **H-COUNTER PIC 9(02):** A counter variable.
*   **H-PPS-DRG-UNADJ-PAY-AMT PIC 9(07)V9(02):** Unadjusted DRG payment amount for PC Pricer.
*   **H-SS-COST-IND PIC X:** Indicator for Short Stay Cost.
*   **H-SS-PERDIEM-IND PIC X:** Indicator for Short Stay Per Diem.
*   **H-SS-BLEND-IND PIC X:** Indicator for Short Stay Blend.
*   **H-SS-IPPSCOMP-IND PIC X:** Indicator for Short Stay IPPS Comparable.
    *   **PC-PRICER (2999):** Condition flag for PC Pricer.
*   **PPS-DATA-ALL:**
    *   **Description:** A comprehensive structure to hold all PPS-related calculated data.
    *   **PPS-RTC PIC 9(02):** PPS Return Code.
    *   **PPS-CHRG-THRESHOLD PIC 9(07)V9(02):** Charge threshold for outliers.
    *   **PPS-DATA:**
        *   **Description:** Contains various PPS calculation results.
        *   **PPS-MSA PIC X(04):** Metropolitan Statistical Area code.
        *   **PPS-WAGE-INDEX PIC 9(02)V9(04):** Wage index.
        *   **PPS-AVG-LOS PIC 9(02)V9(01):** Average Length of Stay.
        *   **PPS-RELATIVE-WGT PIC 9(01)V9(04):** Relative weight.
        *   **PPS-OUTLIER-PAY-AMT PIC 9(07)V9(02):** Outlier payment amount.
        *   **PPS-LOS PIC 9(03):** Length of Stay.
        *   **PPS-DRG-ADJ-PAY-AMT PIC 9(07)V9(02):** DRG adjusted payment amount.
        *   **PPS-FED-PAY-AMT PIC 9(07)V9(02):** Federal payment amount.
        *   **PPS-FINAL-PAY-AMT PIC 9(07)V9(02):** Final payment amount.
        *   **PPS-FAC-COSTS PIC 9(07)V9(02):** Facility costs.
        *   **PPS-NEW-FAC-SPEC-RATE PIC 9(07)V9(02):** New facility specific rate.
        *   **PPS-OUTLIER-THRESHOLD PIC 9(07)V9(02):** Outlier threshold.
        *   **PPS-SUBM-DRG-CODE PIC X(03):** Submitted DRG code.
        *   **PPS-CALC-VERS-CD PIC X(05):** Calculation version code.
        *   **PPS-REG-DAYS-USED PIC 9(03):** Regular days used.
        *   **PPS-LTR-DAYS-USED PIC 9(03):** Lifetime reserve days used.
        *   **PPS-BLEND-YEAR PIC 9(01):** Blend year.
        *   **PPS-COLA PIC 9(01)V9(03):** Cost of Living Adjustment.
        *   **FILLER PIC X(04):** Unused characters.
    *   **PPS-OTHER-DATA:**
        *   **Description:** Additional PPS data.
        *   **PPS-NAT-LABOR-PCT PIC 9(01)V9(05):** National labor percentage.
        *   **PPS-NAT-NONLABOR-PCT PIC 9(01)V9(05):** National non-labor percentage.
        *   **PPS-STD-FED-RATE PIC 9(05)V9(02):** Standard federal rate.
        *   **PPS-BDGT-NEUT-RATE PIC 9(01)V9(03):** Budget neutrality rate.
        *   **PPS-IPTHRESH PIC 9(03)V9(01):** IPPS threshold.
        *   **FILLER PIC X(16):** Unused characters.
    *   **PPS-PC-DATA:**
        *   **Description:** Data specific to PC (Physician's Case) Pricer.
        *   **PPS-COT-IND PIC X(01):** Cost Outlier Indicator.
        *   **H-PC-IND PIC X(02):** Placeholder for PC indicator.
        *   **FILLER PIC X(18):** Unused characters.
*   **PPS-CBSA PIC X(05):** CBSA (Core-Based Statistical Area) code.
*   **PRICER-OPT-VERS-SW:**
    *   **Description:** Switches and version information for the pricer.
    *   **PRICER-OPTION-SW PIC X(01):** Pricer option switch.
        *   **ALL-TABLES-PASSED (313):** Condition flag for all tables passed.
        *   **PROV-RECORD-PASSED (314):** Condition flag for provider record passed.
    *   **PPS-VERSIONS:**
        *   **Description:** Contains version information for PPS.
        *   **PPDRV-VERSION PIC X(05):** PPDRV program version.
*   **PROV-NEW-HOLD:**
    *   **Description:** A structure to hold provider record data passed from the calling program. It's broken into three parts (`HOLD1`, `HOLD2`, `HOLD3`) for organization.
    *   **PROV-NEWREC-HOLD1:**
        *   **P-NEW-NPI10:** NPI (National Provider Identifier) data.
        *   **P-NEW-PROVIDER-NO:** Provider number, including state.
        *   **P-NEW-DATE-DATA:** Various date fields (effective, FY begin, report, termination).
        *   **P-NEW-WAIVER-CODE:** Waiver code indicator.
            *   **P-NEW-WAIVER-STATE (353):** Condition flag for waiver state.
        *   **P-NEW-INTERN-NO:** Intern number.
        *   **P-NEW-PROVIDER-TYPE:** Provider type.
        *   **P-NEW-CURRENT-CENSUS-DIV:** Current census division.
        *   **P-NEW-CURRENT-DIV (358):** Redefines `P-NEW-CURRENT-CENSUS-DIV`.
        *   **P-NEW-MSA-DATA:** MSA related data (charge code index, MSA location, wage index location, standard amount location).
        *   **P-NEW-STAND-AMT-LOC-MSA9 (366):** Redefines `P-NEW-STAND-AMT-LOC-MSA` for numeric access.
        *   **P-NEW-RURAL-1ST:** First part of rural indicator.
        *   **P-NEW-STD-RURAL-CHECK (370):** Condition flag for standard rural check.
        *   **P-NEW-RURAL-2ND:** Second part of rural indicator.
        *   **P-NEW-SOL-COM-DEP-HOSP-YR:** Sole community dependent hospital year.
        *   **P-NEW-LUGAR:** Large urban area indicator.
        *   **P-NEW-TEMP-RELIEF-IND:** Temporary relief indicator.
        *   **P-NEW-FED-PPS-BLEND-IND:** Federal PPS blend indicator.
        *   **FILLER PIC X(05):** Unused characters.
    *   **PROV-NEWREC-HOLD2:**
        *   **P-NEW-VARIABLES:** Various provider-specific calculation variables.
            *   **P-NEW-FAC-SPEC-RATE:** Facility specific rate.
            *   **P-NEW-COLA:** COLA.
            *   **P-NEW-INTERN-RATIO:** Intern ratio.
            *   **P-NEW-BED-SIZE:** Bed size.
            *   **P-NEW-OPER-CSTCHG-RATIO:** Operating cost-to-charge ratio.
            *   **P-NEW-CMI:** Case Mix Index.
            *   **P-NEW-SSI-RATIO:** SSI ratio.
            *   **P-NEW-MEDICAID-RATIO:** Medicaid ratio.
            *   **P-NEW-PPS-BLEND-YR-IND:** PPS blend year indicator.
            *   **P-NEW-PRUF-UPDTE-FACTOR:** Proof update factor.
            *   **P-NEW-DSH-PERCENT:** DSH percentage.
            *   **P-NEW-FYE-DATE:** Fiscal Year End Date.
        *   **P-NEW-SPECIAL-PAY-IND:** Special payment indicator.
        *   **FILLER PIC X(01):** Unused character.
        *   **P-NEW-GEO-LOC-CBSAX:** CBSA location (alphanumeric).
        *   **P-NEW-GEO-LOC-CBSA9 (394):** Redefines `P-NEW-GEO-LOC-CBSAX` for numeric access.
        *   **P-NEW-GEO-LOC-CBSA-AST (396):** Redefines `P-NEW-GEO-LOC-CBSA9` to break down CBSA.
            *   **P-NEW-GEO-LOC-CBSA-1ST to P-NEW-GEO-LOC-CBSA-5TH:** Individual CBSA characters.
        *   **FILLER PIC X(10):** Unused characters.
        *   **P-NEW-SPECIAL-WAGE-INDEX:** Special wage index.
    *   **PROV-NEWREC-HOLD3:**
        *   **P-NEW-PASS-AMT-DATA:** Pass-through amounts.
        *   **P-NEW-CAPI-DATA:** Capital data fields (payment codes, rates, ratios, IME, exceptions).
        *   **FILLER PIC X(22):** Unused characters.
*   **WAGE-NEW-INDEX-RECORD:**
    *   **Description:** Structure to hold wage index data for LTCH.
    *   **W-CBSA PIC X(5):** CBSA code.
    *   **W-EFF-DATE PIC X(8):** Effective date.
    *   **W-WAGE-INDEX1, W-WAGE-INDEX2, W-WAGE-INDEX3 PIC S9(02)V9(04):** Wage indices for different periods.
*   **WAGE-NEW-IPPS-INDEX-RECORD:**
    *   **Description:** Structure to hold wage index data for IPPS.
    *   **W-CBSA-IPPS:** CBSA code for IPPS.
        *   **CBSA-IPPS-123, CBSA-IPPS-45:** Parts of the CBSA code.
    *   **W-CBSA-IPPS-SIZE PIC X:** Size indicator for CBSA.
        *   **LARGE-URBAN (445):** Condition flag for large urban.
        *   **OTHER-URBAN (446):** Condition flag for other urban.
        *   **ALL-RURAL (447):** Condition flag for all rural.
    *   **W-CBSA-IPPS-EFF-DATE PIC X(8):** Effective date for IPPS CBSA.
    *   **FILLER PIC X:** Unused character.
    *   **W-IPPS-WAGE-INDEX PIC S9(02)V9(04):** IPPS wage index.
    *   **W-IPPS-PR-WAGE-INDEX PIC S9(02)V9(04):** Puerto Rico IPPS wage index.

**3. Data Structures in LINKAGE SECTION:**

*   **BILL-NEW-DATA:**
    *   **Description:** Represents the bill record passed from the calling program (LTDRV___).
    *   **B-NPI10:** NPI data.
        *   **B-NPI8 PIC X(08):** National Provider Identifier (first 8 characters).
        *   **B-NPI-FILLER PIC X(02):** Filler for NPI.
    *   **B-PROVIDER-NO PIC X(06):** Provider number.
    *   **B-PATIENT-STATUS PIC X(02):** Patient status.
    *   **B-DRG-CODE PIC 9(03):** DRG code.
    *   **B-LOS PIC 9(03):** Length of Stay.
    *   **B-COV-DAYS PIC 9(03):** Covered days.
    *   **B-LTR-DAYS PIC 9(02):** Lifetime reserve days.
    *   **B-DISCHARGE-DATE:** Discharge date.
        *   **B-DISCHG-CC, B-DISCHG-YY, B-DISCHG-MM, B-DISCHG-DD:** Components of the discharge date.
    *   **B-COV-CHARGES PIC 9(07)V9(02):** Covered charges.
    *   **B-SPEC-PAY-IND PIC X(01):** Special payment indicator.
    *   **FILLER PIC X(13):** Unused characters.
*   **PPS-DATA-ALL:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).
*   **PPS-CBSA:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).
*   **PRICER-OPT-VERS-SW:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).
*   **PROV-NEW-HOLD:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).
*   **WAGE-NEW-INDEX-RECORD:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).
*   **WAGE-NEW-IPPS-INDEX-RECORD:** (Already described in WORKING-STORAGE SECTION, but passed as a linkage item).

---