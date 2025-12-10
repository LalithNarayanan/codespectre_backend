## Data Definition and File Handling

This section consolidates the data definition and file handling information extracted from multiple functional specification documents, providing a comprehensive overview of the COBOL programs involved in prospective payment system (PPS) calculations.

### Program Analysis Overview

The analyzed programs are primarily concerned with calculating prospective payments for healthcare services, likely for Long-Term Care (LTCH) and Inpatient Prospective Payment System (IPPS) facilities. They process billing data, utilize various lookup tables (DRG, wage index, rural factors), and perform complex calculations based on fiscal year, provider-specific data, and regulatory requirements.

The programs generally follow a pattern of:
1.  **Data Input:** Receiving billing data and provider information, often passed via linkage sections.
2.  **Table Loading/Access:** Loading or accessing various data tables, including DRG tables, wage index tables (CBSA, MSA, IPPS), and rural floor adjustment tables. These tables are often included via `COPY` statements, implying they are stored in separate files or copybooks.
3.  **Calculation:** Performing payment calculations based on the input data and the loaded tables. This involves determining rates, weights, adjustments, and ultimately the final payment amount.
4.  **Output:** Returning calculated PPS data, including payment amounts and return codes, to the calling program. Some programs also generate output reports.

The extensive versioning (e.g., LTCAL032, LTCAL042, LTCAL162, LTCAL212) indicates a long history of updates and modifications to the payment methodologies and data structures over many years.

### Program-Specific Details

---

#### Program: LTMGR212

*   **Purpose:** Reads billing records, prepares data, calls `LTOPN212` for payment calculation, and formats/writes results to an output report.
*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format: `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format: `PRTOPER-LINE` (133 bytes).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal (51 characters), likely a comment.
    *   `PPMGR-VERSION`: Program version (5 characters), 'M21.2'.
    *   `LTOPN212`: Literal (8 characters), name of the called program.
    *   `EOF-SW`: End-of-file switch (1-digit numeric).
    *   `OPERLINE-CTR`: Line counter for `PRTOPER` file (2-digit numeric), initialized to 65.
    *   `UT1-STAT`, `UT1-STAT1`, `UT1-STAT2`: File status for `BILLFILE` (2 characters total).
    *   `OPR-STAT`, `OPR-STAT1`, `OPR-STAT2`: File status for `PRTOPER` (2 characters total).
    *   `BILL-WORK`: Structure for input bill record from `BILLFILE` (includes NPI, patient status, DRG, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis/procedure code tables).
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212` (payment calculation results, wage indices).
    *   `PPS-CBSA`: Core Based Statistical Area (CBSA) code (5 characters).
    *   `PPS-PAYMENT-DATA`: Structure for calculated payment amounts (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212`:
        *   `PRICER-OPTION-SW`: Pricing option indicator (1 character).
        *   `PPS-VERSIONS`: Version number structure.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) for CBSA/MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.
*   **Linkage Section:** Not present.

---

#### Program: LTOPN212

*   **Purpose:** Loads provider and wage index tables, determines which tables to use, and calls `LTDRV212` for payment calculations.
*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout: `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout: `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout: `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout: `MSAX-REC`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal (48 characters), likely a comment.
    *   `OPN-VERSION`: Program version (5 characters), '021.2'.
    *   `LTDRV212`: Literal (8 characters), name of the called program.
    *   `TABLES-LOADED-SW`: Table loaded indicator (1-digit numeric).
    *   `EOF-SW`: End-of-file switch (1-digit numeric).
    *   `W-PROV-NEW-HOLD`: Structure to hold provider record (passed or from `PROV-FILE`), mirrors `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: File status for input files (2 characters each).
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data (up to 10000 entries), indexed by `CU1`, `CU2`.
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data (up to 10000 entries), indexed by `MA1`, `MA2`, `MA3`.
    *   `MSA-WI-TABLE`: Table for MSA wage index data (up to 4000 entries), indexed by `MU1`, `MU2`.
    *   `WORK-COUNTERS`: Structure for record counts from each file.
    *   `PROV-TABLE`: Table for provider data from `PROV-FILE` (up to 2400 entries), divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`, indexed by `PX1`, `PD2`, `PD3`.
    *   `PROV-NEW-HOLD`: Structure to hold provider record for `LTDRV212`, mirrors `PROV-RECORD-FROM-USER` from LTMGR212.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirrors `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: PPS data passed/returned to `LTMGR212`, mirrors `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: CBSA code passed from `LTMGR212` (5 characters).
    *   `PPS-PAYMENT-DATA`: Payment data passed/returned to `LTMGR212`, mirrors `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Pricer option/version info passed from `LTMGR212`, mirrors `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Provider-specific info passed from `LTMGR212`, mirrors `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212 for wage index tables.

---

#### Program: LTDRV212

*   **Purpose:** Selects the appropriate wage index and calls the correct `LTCAL` module for payment calculation based on fiscal year and provider information.
*   **Files Accessed:** Does not access any files directly.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal (48 characters), likely a comment.
    *   `DRV-VERSION`: Program version (5 characters), 'D21.2'.
    *   `LTCAL032` ... `LTCAL212`: Literals (8 characters each), names of called programs.
    *   `WS-9S`: Numeric literal (8 characters) with all 9s, used for date comparison.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table (from COPY RUFL200) containing rural floor adjustment factors for CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures for fiscal year begin/end dates.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA/CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from LTOPN212 tables.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider record passed from `LTOPN212`, mirrors `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure for billing data for fiscal years before Jan 2015.
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015+, mirrors `BILL-NEW-DATA` in LTMGR212/LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212/LTOPN212.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed/returned to `LTOPN212`.
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PPS-PAYMENT-DATA`: Payment data passed/returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option/version info passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific info passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212 for wage index tables and record counts.

---

#### COPY Member: RUFL200

*   **Purpose:** Defines data structures for rural floor adjustment factors.
*   **Files Accessed:** Not a program; does not access files directly.
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Main structure containing `RUFL-TAB` table of rural floor adjustment factors. Each entry includes:
        *   `RUFL-CBSA`: CBSA code.
        *   `RUFL-EFF-DATE`: Effective date.
        *   `RUFL-WI3`: Wage index.
    *   The table has 459 entries.

---

#### Program: IPDRG160

*   **Purpose:** Likely accesses a DRG table file for processing.
*   **Files Accessed:** Implied DRG table file (read-only). No explicit file names mentioned.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE`: Effective date for DRG table (20151001).
    *   `PPS-DRG-TABLE`: Group item for DRG table data.
        *   `WK-DRG-DATA`: Temporary holding area for DRG data.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Structured table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG records.
                *   `DRG-DATA-TAB`: Single DRG record structure including:
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code.
                    *   `FILLER1` (PIC X(01)): Filler.
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)): Filler.
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean of average length of stay.
                    *   `FILLER3` (PIC X(05)): Filler.
                    *   `DRG-LOW` (PIC X(01)): Indicator ('Y'/'N').
                    *   `FILLER5` (PIC X(01)): Filler.
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic mean of average length of stay.
                    *   `FILLER6` (PIC X(02)): Filler.
                    *   `DRG-PAC` (PIC X(01)): Post-acute care indicator.
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Special post-acute care indicator.
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG170

*   **Purpose:** Likely accesses a DRG table file for 2016.
*   **Files Accessed:** Implied DRG table file (read-only) for 2016.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`. DRG data is specific to 2016.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG181

*   **Purpose:** Likely accesses a DRG table file for 2017.
*   **Files Accessed:** Implied DRG table file (read-only) for 2017.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20171001' and `DRG-TAB` having `OCCURS 754`. DRG data is specific to 2017.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG190

*   **Purpose:** Likely accesses a DRG table file for 2018.
*   **Files Accessed:** Implied DRG table file (read-only) for 2018.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20181001' and `DRG-TAB` having `OCCURS 761`. DRG data is specific to 2018.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG200

*   **Purpose:** Likely accesses a DRG table file for 2019.
*   **Files Accessed:** Implied DRG table file (read-only) for 2019.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20191001' and `DRG-TAB` having `OCCURS 761`. DRG data is specific to 2019, noting additions for DRG 319 and 320.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG211

*   **Purpose:** Likely accesses a DRG table file for 2020.
*   **Files Accessed:** Implied DRG table file (read-only) for 2020.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20201001' and `DRG-TAB` having `OCCURS 767`. DRG data is specific to 2020, noting changes in some descriptions.
*   **Linkage Section:** Not present.

---

#### Program: LTCAL162

*   **Purpose:** Performs PPS calculations, likely for FY16.
*   **Files Accessed:**
    *   Implied Provider-Specific File (PSF).
    *   Implied CBSA wage index file.
    *   Implied LTCH DRG table file (`LTDRG160` via COPY).
    *   Implied IPPS DRG table file (`IPDRG160` via COPY).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive filler.
    *   `CAL-VERSION`: Program version ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in the program.
    *   `PROGRAM-FLAGS`: Flags for program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for payment.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data copied from DRG tables.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Input bill data from `LTDRV`.
    *   `PPS-DATA-ALL`: Output PPS calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches for pricer option and driver program versions.
    *   `PROV-NEW-HOLD`: Input provider-specific data from `LTDRV`.
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

#### Program: LTCAL170

*   **Purpose:** Performs PPS calculations, likely for FY17.
*   **Files Accessed:** Similar to LTCAL162, implies PSF, CBSA wage index file, `LTDRG170` (COPY), and `IPDRG170` (COPY).
*   **Working-Storage Section:** Similar to LTCAL162, but with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.
*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

#### Program: LTCAL183

*   **Purpose:** Performs PPS calculations, likely for FY18.
*   **Files Accessed:** Implies PSF, CBSA wage index file, `LTDRG181` (COPY), and `IPDRG181` (COPY).
*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3'. Updated for FY18. Variables related to Subclause II removed.
*   **Linkage Section:** Similar to LTCAL170, with fields related to Subclause II removed.

---

#### Program: LTCAL190

*   **Purpose:** Performs PPS calculations, likely for FY19.
*   **Files Accessed:** Implies PSF, CBSA wage index file, `LTDRG190` (COPY), and `IPDRG190` (COPY).
*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0'. Updated for FY19.
*   **Linkage Section:** Similar to LTCAL183.

---

#### Program: LTCAL202

*   **Purpose:** Performs PPS calculations, likely for FY20.
*   **Files Accessed:** Implies PSF, CBSA wage index file, `LTDRG200` (COPY), and `IPDRG200` (COPY).
*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2'. Updated for FY20. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` for Disproportionate Patient Percentage (DPP) adjustment.

---

#### Program: LTCAL212

*   **Purpose:** Performs PPS calculations, likely for FY21.
*   **Files Accessed:** Implies PSF, CBSA wage index file, `LTDRG210` (COPY), and `IPDRG211` (COPY).
*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2'. Updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

---

#### Program: LTDRG160

*   **Purpose:** Copybook defining LTCH DRG table data for FY15.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **Linkage Section:** Not present.

---

#### Program: LTDRG170

*   **Purpose:** Copybook defining LTCH DRG table data for FY16.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.
*   **Linkage Section:** Not present.

---

#### Program: LTDRG181

*   **Purpose:** Copybook defining LTCH DRG table data for FY18.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** Not present.

---

#### Program: LTDRG190

*   **Purpose:** Copybook defining LTCH DRG table data for FY19.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** Not present.

---

#### Program: LTDRG210

*   **Purpose:** Copybook defining LTCH DRG table data for FY21.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** Not present.

---

#### Program: IPDRG104

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG104` statement.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds DRG data in packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG110

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG110` statement.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

---

#### Program: IPDRG123

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG123` statement.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

---

#### Program: IRFBN102

*   **Purpose:** Defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs) for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IRFBN102` statement.
*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Other code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
    *   Message area fields (`MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`).
    *   `MES-TOT-PAY`: Total payment amount (PIC 9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record, structurally identical to `WK-SSRFBN-REASON-ALL`.
*   **Linkage Section:** None.

---

#### Program: IRFBN105

*   **Purpose:** Defines a table of updated state-specific RFBNs for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IRFBN105` statement.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** None.

---

#### Program: LTCAL103

*   **Purpose:** Performs PPS calculations, likely for FY03-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: Likely LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN102`: IPPS state-specific RFBNs.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive comment (46 characters).
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds calculated PPS components (LOS, days, rates, adjustments, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW`: 'A' or 'P'.
        *   `PPS-VERSIONS`: `PPDRV-VERSION`.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, codes, indices, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, patient status, DRG, LOS, covered days, LTR days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.

---

#### Program: LTCAL105

*   **Purpose:** Performs PPS calculations, likely for FY05-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **Working-Storage Section:** Very similar to `LTCAL103`, differences in version number (`CAL-VERSION` = 'V10.5') and copybooks used (`IRFBN105`). Minor numeric constant adjustments.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL111

*   **Purpose:** Performs PPS calculations, likely for FY11, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG110`: LTC DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   `IRFBN102` (commented out): No state-specific RFBN table included.
*   **Working-Storage Section:** Similar to `LTCAL103`, with version `V11.1` and adjusted copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL123

*   **Purpose:** Performs PPS calculations, likely for FY12-FY13, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG123`: LTC DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL103

*   **Purpose:** Performs PPS calculations, likely for FY03-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: Likely LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN102`: IPPS state-specific RFBNs.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive comment (46 characters).
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds calculated PPS components (LOS, days, rates, adjustments, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW`: 'A' or 'P'.
        *   `PPS-VERSIONS`: `PPDRV-VERSION`.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, codes, indices, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, patient status, DRG, LOS, covered days, LTR days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.

---

#### Program: LTCAL105

*   **Purpose:** Performs PPS calculations, likely for FY05-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **Working-Storage Section:** Very similar to `LTCAL103`, differences in version number (`CAL-VERSION` = 'V10.5') and copybooks used (`IRFBN105`). Minor numeric constant adjustments.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL111

*   **Purpose:** Performs PPS calculations, likely for FY11, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG110`: LTC DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   `IRFBN102` (commented out): No state-specific RFBN table included.
*   **Working-Storage Section:** Similar to `LTCAL103`, with version `V11.1` and adjusted copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL123

*   **Purpose:** Performs PPS calculations, likely for FY12-FY13, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG123`: LTC DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTDRG100

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None explicitly accessed. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG110

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None explicitly accessed. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG123

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None explicitly accessed. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG080

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as packed strings.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (likely year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date ('20071001').
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

---

#### Program: IPDRG090

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

---

#### Program: IRFBN091

*   **Purpose:** Defines message and state-specific RFBN data structures in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   Message area fields (`MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`).
    *   `MES-TOT-PAY`: Total payment amount (PIC 9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record (State Code, Filler, State Specific Rate, Filler, Code2, Filler, State Name, Remaining Data).
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state (State Code, Filler, Rate, Filler, Code2, Filler, State Name, Remaining Data).
*   **Linkage Section:** None.

---

#### Program: LTCAL087

*   **Purpose:** Performs PPS calculations, likely for FY07.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG086` and `COPY IPDRG080`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment (46 characters).
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates (FY03-FY07).
    *   `COPY LTDRG086`: Includes LTCH DRG table (`WWM-ENTRY`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, days, rates, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned (Return Code, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay, LOS, DRG Adjusted Pay, Federal Pay, Final Pay, Facility Costs, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Pricer options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, codes, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Index 1, 2, 3).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data (CBSA, size, effective date, IPPS wage index, PR IPPS wage index).

---

#### Program: LTCAL091

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Similar to LTCAL087, uses `COPY LTDRG086` and `COPY IPDRG080`.
*   **Working-Storage Section:** Similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data reflects year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL094

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Uses `COPY LTDRG093`, `COPY IPDRG090`, `COPY IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL087/091, with `CAL-VERSION` as 'V09.4'. Copied data reflects year's changes. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL095

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Uses `COPY LTDRG095`, `COPY IPDRG090`, `COPY IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL094, with `CAL-VERSION` as 'V09.5'. Copied data reflects year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTDRG080

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

---

#### Program: LTDRG086

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.
*   **Linkage Section:** None.

---

#### Program: LTDRG093

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

---

#### Program: LTDRG095

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

---

#### Program: IPDRG063

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG071

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Similar structure to IPDRG063, a table of DRG data.
        *   `05 D-TAB`: Raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 580 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTCAL064

*   **Purpose:** Performs PPS calculations, likely for FY06.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, implying use of DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes `LTDRG062` copybook (LTCH DRG table).
    *   `HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Various numeric/alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `PROV-NEW-HOLD`: Structure for provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Structure for wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (provider info, DRG, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results returned (return codes, payment amounts).
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

#### Program: LTCAL072

*   **Purpose:** Performs PPS calculations, likely for FY07.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062` and `COPY IPDRG063`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `HOLD-PPS-COMPONENTS`: Intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (updated to numeric DRG-CODE).
    *   `PPS-DATA-ALL`: PPS calculation results returned.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

#### Program: LTCAL075 and LTCAL080

*   **Purpose:** Perform PPS calculations for respective fiscal years.
*   **Files Accessed:** Similar to LTCAL072, using relevant DRG copybooks.
*   **Working-Storage Section:** Similar structure to LTCAL072, with incremental changes in constants, rates, and potentially new variables.
*   **Linkage Section:** Similar structure to LTCAL072.

---

#### Program: LTDRG062

*   **Purpose:** Defines a LTCH DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains raw data for LTCH DRG table as packed strings.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG075 and LTDRG080

*   **Purpose:** Define LTCH DRG table data structures.
*   **Files Accessed:** None. Data defined within the programs.
*   **Working-Storage Section:** Similar structure to LTDRG062, with updated DRG codes, weights, average lengths of stay, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may vary.
*   **Linkage Section:** None.

---

#### Program: LTCAL043

*   **Purpose:** Performs PPS calculations, likely for FY04.
*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment (46 characters).
    *   `CAL-VERSION`: Version ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure:
        *   `WWM-ENTRY` (OCCURS 510): DRG data (DRG code, Relative Weight, Average Length of Stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Days, SSOT, Blend amounts, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results (Return Code, Thresholds, MSA, Wage Index, Average LOS, Relative Weight, Outlier payments, Final payment, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Index 1, 2).

---

#### Program: LTCAL058

*   **Purpose:** Performs PPS calculations, likely for FY05.
*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version ('V05.8').
    *   `PROGRAM-CONSTANTS`: Fiscal year dates.
    *   `LTDRG041`: Copy of DRG table structure (same as LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results (same as LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

---

#### Program: LTCAL059

*   **Purpose:** Performs PPS calculations, likely for FY05.
*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version ('V05.9').
    *   `PROGRAM-CONSTANTS`: Fiscal year dates.
    *   `LTDRG057`: Copy of DRG table structure:
        *   `WWM-ENTRY` (OCCURS 512): DRG data (DRG code, Relative Weight, Average Length of Stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results (same as LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

---

#### Program: LTCAL063

*   **Purpose:** Performs PPS calculations, likely for FY06.
*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version ('V06.3').
    *   `PROGRAM-CONSTANTS`: Fiscal year dates.
    *   `LTDRG057`: Copy of DRG table structure (same as LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA`: CBSA code (5 characters).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data (adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`).
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data (uses CBSA instead of MSA).

---

#### Program: LTDRG041

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG057

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTCAL032

*   **Purpose:** Performs PPS calculations, likely for FY03.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version ('C03.2').
    *   `LTDRG031` (COPY): Includes `W-DRG-TABLE` (DRG codes, weights, ALoS).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Days, SSOT, Blend amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing switches.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, codes, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Index 1, 2, 3).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay, LOS, DRG Adjusted Pay, Federal Pay, Final Pay, Facility Costs, etc.).

---

#### Program: LTCAL042

*   **Purpose:** Performs PPS calculations, likely for FY04.
*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:** Almost identical to LTCAL032, with key differences:
    *   `CAL-VERSION` is 'C04.2'.
    *   `PPS-STD-FED-RATE` value differs.
    *   `H-FIXED-LOSS-AMT` value differs.
    *   `PPS-BDGT-NEUT-RATE` value differs.
    *   Adds `H-LOS-RATIO` to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

---

#### Program: LTDRG031

*   **Purpose:** Copybook defining DRG table data structure.
*   **Files Accessed:** Not a program; data definitions used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Table structure (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG104

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG104` statement.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds DRG data in packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG110

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG110` statement.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

---

#### Program: IPDRG123

*   **Purpose:** Defines a DRG table for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IPDRG123` statement.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

---

#### Program: IRFBN102

*   **Purpose:** Defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs) for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IRFBN102` statement.
*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Other code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
    *   Message area fields (`MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`).
    *   `MES-TOT-PAY`: Total payment amount (PIC 9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record, structurally identical to `WK-SSRFBN-REASON-ALL`.
*   **Linkage Section:** None.

---

#### Program: IRFBN105

*   **Purpose:** Defines a table of updated state-specific RFBNs for inclusion via `COPY`.
*   **Files Accessed:** Implied by `COPY IRFBN105` statement.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** None.

---

#### Program: LTCAL103

*   **Purpose:** Performs PPS calculations, likely for FY03-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: Likely LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN102`: IPPS state-specific RFBNs.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive comment (46 characters).
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds calculated PPS components (LOS, days, rates, adjustments, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW`: 'A' or 'P'.
        *   `PPS-VERSIONS`: `PPDRV-VERSION`.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, codes, indices, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, patient status, DRG, LOS, covered days, LTR days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.

---

#### Program: LTCAL105

*   **Purpose:** Performs PPS calculations, likely for FY05-FY07, using specific DRG and RFBN tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG100`: LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **Working-Storage Section:** Very similar to `LTCAL103`, differences in version number (`CAL-VERSION` = 'V10.5') and copybooks used (`IRFBN105`). Minor numeric constant adjustments.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL111

*   **Purpose:** Performs PPS calculations, likely for FY11, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG110`: LTC DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   `IRFBN102` (commented out): No state-specific RFBN table included.
*   **Working-Storage Section:** Similar to `LTCAL103`, with version `V11.1` and adjusted copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTCAL123

*   **Purpose:** Performs PPS calculations, likely for FY12-FY13, using specific DRG tables.
*   **Files Accessed:** Implied via `COPY` statements:
    *   `LTDRG123`: LTC DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

#### Program: LTDRG100

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG110

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG123

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG080

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as packed strings.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (likely year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date ('20071001').
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

---

#### Program: IPDRG090

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

---

#### Program: IRFBN091

*   **Purpose:** Defines message and state-specific RFBN data structures in WORKING-STORAGE.
*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   Message area fields (`MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`).
    *   `MES-TOT-PAY`: Total payment amount (PIC 9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record (State Code, Filler, State Specific Rate, Filler, Code2, Filler, State Name, Remaining Data).
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state (State Code, Filler, Rate, Filler, Code2, Filler, State Name, Remaining Data).
*   **Linkage Section:** None.

---

#### Program: LTCAL087

*   **Purpose:** Performs PPS calculations, likely for FY07.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG086` and `COPY IPDRG080`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment (46 characters).
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates (FY03-FY07).
    *   `COPY LTDRG086`: Includes LTCH DRG table (`WWM-ENTRY`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, days, rates, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned (Return Code, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay, LOS, DRG Adjusted Pay, Federal Pay, Final Pay, Facility Costs, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Pricer options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, codes, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Index 1, 2, 3).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data (CBSA, size, effective date, IPPS wage index, PR IPPS wage index).

---

#### Program: LTCAL091

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Similar to LTCAL087, uses `COPY LTDRG086` and `COPY IPDRG080`.
*   **Working-Storage Section:** Similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data reflects year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL094

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Uses `COPY LTDRG093`, `COPY IPDRG090`, `COPY IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL087/091, with `CAL-VERSION` as 'V09.4'. Copied data reflects year's changes. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL095

*   **Purpose:** Performs PPS calculations, likely for FY09.
*   **Files Accessed:** Uses `COPY LTDRG095`, `COPY IPDRG090`, `COPY IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL094, with `CAL-VERSION` as 'V09.5'. Copied data reflects year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTDRG080

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

---

#### Program: LTDRG086

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.
*   **Linkage Section:** None.

---

#### Program: LTDRG093

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

---

#### Program: LTDRG095

*   **Purpose:** Defines a LTC DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

---

#### Program: IPDRG063

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: IPDRG071

*   **Purpose:** Defines a DRG table data structure in WORKING-STORAGE.
*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Similar structure to IPDRG063, a table of DRG data.
        *   `05 D-TAB`: Raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 580 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTCAL064

*   **Purpose:** Performs PPS calculations, likely for FY06.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, implying use of DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes `LTDRG062` copybook (LTCH DRG table).
    *   `HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Various numeric/alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `PROV-NEW-HOLD`: Structure for provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Structure for wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (provider info, DRG, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results returned (return codes, payment amounts).
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

#### Program: LTCAL072

*   **Purpose:** Performs PPS calculations, likely for FY07.
*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062` and `COPY IPDRG063`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `HOLD-PPS-COMPONENTS`: Intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (updated to numeric DRG-CODE).
    *   `PPS-DATA-ALL`: PPS calculation results returned.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

#### Program: LTCAL075 and LTCAL080

*   **Purpose:** Perform PPS calculations for respective fiscal years.
*   **Files Accessed:** Similar to LTCAL072, using relevant DRG copybooks.
*   **Working-Storage Section:** Similar structure to LTCAL072, with incremental changes in constants, rates, and potentially new variables.
*   **Linkage Section:** Similar structure to LTCAL072.

---

#### Program: LTDRG062

*   **Purpose:** Defines a LTCH DRG table data structure.
*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains raw data for LTCH DRG table as packed strings.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

#### Program: LTDRG075 and LTDRG080

*   **Purpose:** Define LTCH DRG table data structures.
*   **Files Accessed:** None. Data defined within the programs.
*   **Working-Storage Section:** Similar structure to LTDRG062, with updated DRG codes, weights, average lengths of stay, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may vary.
*   **Linkage Section:** None.

---

**Overall Program Flow Summary:**

The programs `LTMGR212`, `LTOPN212`, and `LTDRV212` form a primary processing chain. `LTMGR212` initiates the process by reading billing data. It then calls `LTOPN212`, which is responsible for loading necessary tables (provider, wage index) from various files and then calling `LTDRV212`. `LTDRV212` selects the correct calculation logic based on fiscal year and provider data, potentially calling different `LTCAL` modules (e.g., `LTCAL032`, `LTCAL162`, etc.) which contain the core payment calculation algorithms. These `LTCAL` programs, in turn, utilize DRG tables (defined in `LTDRG` copybooks) and potentially other lookup data defined in `IPDRG` and `IRFBN` copybooks. The results are passed back through the chain, with `LTMGR212` ultimately producing the output report.

**Note on Data Structures:**

The analysis of programs like `IPDRG080` and `IPDRG090` highlights long strings of `FILLER` data within the `D-TAB` structure. These are highly likely to be packed representations of DRG table data. Similarly, `W-DRG-FILLS` in `LTDRG` programs contains packed data. A more in-depth analysis would involve decoding these packed fields to fully understand the structure of the DRG data itself. The presence of `COPY` statements throughout indicates a modular design, where data structures and potentially logic are reused across different programs and versions.