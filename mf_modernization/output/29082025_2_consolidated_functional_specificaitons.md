## Data Definition and File Handling

This document consolidates the data definition and file handling information extracted from multiple functional specification documents (L1 through L8). It provides a detailed analysis of COBOL programs, outlining the files they access, their working-storage sections, and their linkage sections.

The programs analyzed are primarily related to prospective payment system (PPS) calculations, likely for healthcare claims, with a focus on Long-Term Care (LTCH) and Inpatient Prospective Payment System (IPPS) methodologies. The analysis reveals a consistent pattern of programs interacting with various DRG (Diagnosis Related Group) tables, wage index data, and provider-specific information.

### Program Analysis: LTMGR212

**Purpose:** This program reads billing records, prepares data, calls `LTOPN212` for payment calculations, and formats results for output.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format defined by `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format defined by `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string (51 characters), likely a comment.
    *   `PPMGR-VERSION`: Program version ('M21.2', 5 characters).
    *   `LTOPN212`: Literal string (8 characters), name of the called program.
    *   `EOF-SW`: End-of-file switch (1-digit numeric; 0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: Line counter for `PRTOPER` (2-digit numeric), initialized to 65.
    *   `UT1-STAT`: File status for `BILLFILE` (2 characters).
        *   `UT1-STAT1`: First character of file status.
        *   `UT1-STAT2`: Second character of file status.
    *   `OPR-STAT`: File status for `PRTOPER` (2 characters).
        *   `OPR-STAT1`: First character of file status.
        *   `OPR-STAT2`: Second character of file status.
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (includes NPI, patient status, DRG, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis and procedure code tables).
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212` (payment calculation results, wage indices, etc.).
    *   `PPS-CBSA`: Core Based Statistical Area (CBSA) code (5 characters).
    *   `PPS-PAYMENT-DATA`: Structure holding payment amounts calculated by `LTOPN212` (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, likely for passing data to called programs.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Pricing option indicator (single character).
        *   `PPS-VERSIONS`: Versions passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, provider-specific data).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) for CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

### Program Analysis: LTOPN212

**Purpose:** Loads provider and wage index tables, determines table usage based on discharge date and pricer option, and calls `LTDRV212` for payment calculations.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file with provider records. Record layout defined as `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file with CBSA wage index data. Record layout defined as `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file with IPPS CBSA wage index data. Record layout defined as `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file with MSA wage index data. Record layout defined as `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string (48 characters), likely a comment.
    *   `OPN-VERSION`: Program version ('021.2', 5 characters).
    *   `LTDRV212`: Literal string (8 characters), name of the called program.
    *   `TABLES-LOADED-SW`: Table loaded switch (1-digit numeric; 0 = not loaded, 1 = loaded).
    *   `EOF-SW`: End-of-file switch (1-digit numeric).
    *   `W-PROV-NEW-HOLD`: Structure to hold provider record (passed in or from `PROV-FILE`), mirrors `PROV-RECORD-FROM-USER` from `LTMGR212`.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: File status for input files (2 characters each).
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data from `CBSAX-FILE` (up to 10000 entries, indexed by `CU1`, `CU2`).
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data from `IPPS-CBSAX-FILE` (up to 10000 entries, indexed by `MA1`, `MA2`, `MA3`).
    *   `MSA-WI-TABLE`: Table for MSA wage index data from `MSAX-FILE` (up to 4000 entries, indexed by `MU1`, `MU2`).
    *   `WORK-COUNTERS`: Structure containing record counters for each file.
    *   `PROV-TABLE`: Table to hold provider data from `PROV-FILE` (up to 2400 entries, divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`, indexed by `PX1`, `PD2`, `PD3`).
    *   `PROV-NEW-HOLD`: Structure to hold provider record for passing to `LTDRV212`, mirrors `PROV-RECORD-FROM-USER` from `LTMGR212`.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirrors `BILL-NEW-DATA` in `LTMGR212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTMGR212`, mirrors `PPS-DATA-ALL` in `LTMGR212`.
    *   `PPS-CBSA`: CBSA code passed from `LTMGR212` (5 characters).
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTMGR212`, mirrors `PPS-PAYMENT-DATA` in `LTMGR212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTMGR212`, mirrors `PRICER-OPT-VERS-SW` in `LTMGR212`.
    *   `PROV-RECORD-FROM-USER`: Provider-specific information passed from `LTMGR212`, mirrors `PROV-RECORD-FROM-USER` in `LTMGR212`.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in `LTMGR212` for wage index tables.

### Program Analysis: LTDRV212

**Purpose:** Selects the appropriate wage index, calls the correct `LTCAL` module for payment calculation based on fiscal year.

*   **Files Accessed:** Does not directly access any files.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string (48 characters), likely a comment.
    *   `DRV-VERSION`: Program version ('D21.2', 5 characters).
    *   `LTCAL032` ... `LTCAL212`: Literal strings (8 characters each), names of called programs (various `LTCAL` versions).
    *   `WS-9S`: Numeric literal (8 characters) with all 9s, used for date comparison.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields holding wage index constants for FY2020.
    *   `RUFL-ADJ-TABLE`: Table (defined in COPY `RUFL200`) containing rural floor adjustment factors for CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold fiscal year begin/end dates calculated from discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from tables in `LTOPN212`.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider record passed from `LTOPN212`, mirrors `PROV-NEW-HOLD` in `LTOPN212`.
    *   `BILL-DATA-FY03-FY15`: Structure for billing data for older fiscal years (pre-Jan 2015).
    *   `BILL-NEW-DATA`: Structure for billing data for FY2015 and later, mirrors `BILL-NEW-DATA` in `LTMGR212` and `LTOPN212`.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in `LTMGR212` and `LTOPN212`.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in `LTOPN212`, holding wage index tables and record counts.

### COPY Member: RUFL200

**Purpose:** Defines data structures for rural floor adjustment factors.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Not applicable (COPY member).
*   **Linkage Section:** Not applicable (COPY member).
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Main structure containing `RUFL-TAB` (a table of rural floor adjustment factors). Each entry includes:
        *   `RUFL-CBSA`: CBSA code.
        *   `RUFL-EFF-DATE`: Effective date.
        *   `RUFL-WI3`: Wage index.
        *   The table has 459 entries.

### Program Analysis: IPDRG160

**Purpose:** Likely accesses a DRG table file for the year 2015.

*   **Files Accessed:** Likely accesses a DRG table file (read-only). No explicit file names mentioned.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE`: Effective date for DRG table ('20151001', 8 characters).
    *   `PPS-DRG-TABLE`: Group item containing DRG table data.
        *   `WK-DRG-DATA`: Temporary holding area for file data.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Structured table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Single DRG record group.
                    *   `WK-DRG-DRGX`: DRG code ('001', 3 characters).
                    *   `FILLER1`: Filler (1 character).
                    *   `DRG-WEIGHT`: DRG weight (9(02)V9(04)).
                    *   `FILLER2`: Filler (1 character).
                    *   `DRG-GMALOS`: Geometric mean of average length of stay (9(02)V9(01)).
                    *   `FILLER3`: Filler (5 characters).
                    *   `DRG-LOW`: Indicator ('Y'/'N', 1 character).
                    *   `FILLER5`: Filler (1 character).
                    *   `DRG-ARITH-ALOS`: Arithmetic mean of average length of stay (9(02)V9(01)).
                    *   `FILLER6`: Filler (2 characters).
                    *   `DRG-PAC`: Post-acute care indicator (1 character).
                    *   `FILLER7`: Filler (1 character).
                    *   `DRG-SPPAC`: Special post-acute care indicator (1 character).
                    *   `FILLER8`: Filler (2 characters).
                    *   `DRG-DESC`: DRG description (26 characters).
*   **Linkage Section:** Not present.

### Program Analysis: IPDRG170

**Purpose:** Likely accesses a DRG table file for the year 2016.

*   **Files Accessed:** Likely accesses a DRG table file (read-only).
*   **Working-Storage Section:** Structurally identical to `IPDRG160`, but with:
    *   `WK-DRGX-EFF-DATE`: '20161001'.
    *   `DRG-TAB` (OCCURS 757).
    *   DRG data specific to 2016.
*   **Linkage Section:** Not present.

### Program Analysis: IPDRG181

**Purpose:** Likely accesses a DRG table file for the year 2017.

*   **Files Accessed:** Likely accesses a DRG table file (read-only).
*   **Working-Storage Section:** Structurally identical to `IPDRG160`, but with:
    *   `WK-DRGX-EFF-DATE`: '20171001'.
    *   `DRG-TAB` (OCCURS 754).
    *   DRG data specific to 2017.
*   **Linkage Section:** Not present.

### Program Analysis: IPDRG190

**Purpose:** Likely accesses a DRG table file for the year 2018.

*   **Files Accessed:** Likely accesses a DRG table file (read-only).
*   **Working-Storage Section:** Structurally identical to `IPDRG160`, but with:
    *   `WK-DRGX-EFF-DATE`: '20181001'.
    *   `DRG-TAB` (OCCURS 761).
    *   DRG data specific to 2018.
*   **Linkage Section:** Not present.

### Program Analysis: IPDRG200

**Purpose:** Likely accesses a DRG table file for the year 2019.

*   **Files Accessed:** Likely accesses a DRG table file (read-only).
*   **Working-Storage Section:** Structurally identical to `IPDRG160`, but with:
    *   `WK-DRGX-EFF-DATE`: '20191001'.
    *   `DRG-TAB` (OCCURS 761).
    *   DRG data specific to 2019 (includes DRG 319 and 320).
*   **Linkage Section:** Not present.

### Program Analysis: IPDRG211

**Purpose:** Likely accesses a DRG table file for the year 2020.

*   **Files Accessed:** Likely accesses a DRG table file (read-only).
*   **Working-Storage Section:** Structurally identical to `IPDRG160`, but with:
    *   `WK-DRGX-EFF-DATE`: '20201001'.
    *   `DRG-TAB` (OCCURS 767).
    *   DRG data specific to 2020 (includes changes in descriptions).
*   **Linkage Section:** Not present.

### Program Analysis: LTCAL162

**Purpose:** Performs PPS calculations, likely accessing provider, CBSA, and DRG tables.

*   **Files Accessed:** Likely accesses:
    *   Provider-specific file (PSF) for wage indices, cost-to-charge ratios, etc.
    *   CBSA wage index file.
    *   LTCH DRG table (`LTDRG160`) and IPPS DRG table (`IPDRG160`) via COPY statements (read-only).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive filler.
    *   `CAL-VERSION`: Program version ('V16.2').
    *   `PROGRAM-CONSTANTS`: Program constants.
    *   `PROGRAM-FLAGS`: Flags for program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data copied from DRG tables.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Input bill data from a calling program (likely `LTDRV`).
    *   `PPS-DATA-ALL`: Output PPS calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches for pricer option and driver program versions.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

### Program Analysis: LTCAL170

**Purpose:** Performs PPS calculations for FY17.

*   **Files Accessed:** Similar to `LTCAL162`, likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG170`, `IPDRG170`).
*   **Working-Storage Section:** Similar to `LTCAL162`, with `CAL-VERSION` set to 'V17.0' and updated constants/rates for FY17.
*   **Linkage Section:** Identical to `LTCAL162`'s Linkage Section, except for the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

### Program Analysis: LTCAL183

**Purpose:** Performs PPS calculations for FY18.

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG181`, `IPDRG181`).
*   **Working-Storage Section:** Similar to `LTCAL170`, with `CAL-VERSION` as 'V18.3' and updated for FY18. Variables related to Subclause II have been removed.
*   **Linkage Section:** Similar to `LTCAL170`, with fields related to Subclause II removed.

### Program Analysis: LTCAL190

**Purpose:** Performs PPS calculations for FY19.

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG190`, `IPDRG190`).
*   **Working-Storage Section:** Similar to `LTCAL183`, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **Linkage Section:** Similar to `LTCAL183`.

### Program Analysis: LTCAL202

**Purpose:** Performs PPS calculations for FY20, including COVID-19 processing.

*   **Files Accessed:** Similar to previous `LTCAL` programs, accessing PSF, CBSA wage index file, and DRG tables (`LTDRG200`, `IPDRG200`).
*   **Working-Storage Section:** Similar to `LTCAL190`, with `CAL-VERSION` as 'V20.2' and updated for FY20. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous `LTCAL` programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` for Disproportionate Patient Percentage (DPP) adjustment.

### Program Analysis: LTCAL212

**Purpose:** Performs PPS calculations for FY21.

*   **Files Accessed:** Similar to `LTCAL202`, accessing PSF, CBSA wage index file, and DRG tables (`LTDRG210`, `IPDRG211`).
*   **Working-Storage Section:** Similar to `LTCAL202`, with `CAL-VERSION` as 'V21.2' and updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **Linkage Section:** Similar to `LTCAL202`, with no additional fields.

### COPY Member: LTDRG160

**Purpose:** Defines the data structure for the LTCH DRG table for FY15.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Defines the structure of the LTCH DRG table.
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **Linkage Section:** Not applicable.

### COPY Member: LTDRG170

**Purpose:** Defines the data structure for the LTCH DRG table for FY16.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to `LTDRG160`, but `WWM-ENTRY` has `OCCURS 747`.
*   **Linkage Section:** Not applicable.

### COPY Member: LTDRG181

**Purpose:** Defines the data structure for the LTCH DRG table for FY18.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to `LTDRG160`, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** Not applicable.

### COPY Member: LTDRG190

**Purpose:** Defines the data structure for the LTCH DRG table for FY19.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to previous `LTDRG` copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** Not applicable.

### COPY Member: LTDRG210

**Purpose:** Defines the data structure for the LTCH DRG table for FY21.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to previous `LTDRG` copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** Not applicable.

### Program Analysis: IPDRG104

**Purpose:** Uses a COPY statement to include DRG data.

*   **Files Accessed:** None explicitly listed. Uses `COPY IPDRG104`, implying inclusion from a file containing a DRG table.
*   **Working-Storage Section:**
    *   `DRG-TABLE`: Table containing DRG data.
        *   `D-TAB`: Holds DRG data in a packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

### Program Analysis: IPDRG110

**Purpose:** Uses a COPY statement to include DRG data.

*   **Files Accessed:** Uses `COPY IPDRG110`, referencing a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

### Program Analysis: IPDRG123

**Purpose:** Uses a COPY statement to include DRG data.

*   **Files Accessed:** Uses `COPY IPDRG123`, referencing a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

### Program Analysis: IRFBN102

**Purpose:** Defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** Uses `COPY IRFBN102`, suggesting data from a file containing RFBNs.
*   **Working-Storage Section:**
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-INTRO`: Message areas (53 characters each).
    *   `MES-PPS-STATE`: PPS State code (2 characters).
    *   `MES-TOT-PAY`: Total payment amount (9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record (similar structure to `WK-SSRFBN-REASON-ALL`).
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Holds RFBN data.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `WK-SSRFBN-STATE PIC 99`: State code.
                    *   `FILLER PIC XX`: Filler.
                    *   `WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `FILLER PIC XX`: Filler.
                    *   `WK-SSRFBN-CODE2 PIC 99`: Code (unclear purpose).
                    *   `FILLER PIC X`: Filler.
                    *   `WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
*   **Linkage Section:** None.

### Program Analysis: IRFBN105

**Purpose:** Defines a table of updated state-specific RFBNs.

*   **Files Accessed:** Uses `COPY IRFBN105`, referencing a file with updated RFBN data.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** None.

### Program Analysis: LTCAL103

**Purpose:** Performs PPS calculations, utilizing DRG and RFBN data.

*   **Files Accessed:** Uses `COPY` statements to include data from:
    *   `LTDRG100`: Likely contains an LTCH DRG table.
    *   `IPDRG104`: Contains IPPS DRG data.
    *   `IRFBN102`: Contains IPPS state-specific RFBNs.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string comment.
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (`FED-FY-BEGIN-03` to `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Structure holding calculated PPS components (LOS, days, rates, adjustments, etc.).
    *   `PPS-DATA-ALL`: Structure for final PPS calculation results (return code, charge threshold, various PPS data elements).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW`: 'A' for all tables passed, 'P' for provider record passed.
        *   `PPS-VERSIONS`: Related program versions (`PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Structure holding provider-specific data (NPI, provider number, dates, waiver code, type, census division, MSA data, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size indicator, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG access.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, patient status, DRG, LOS, covered days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.

### Program Analysis: LTCAL105

**Purpose:** Performs PPS calculations, utilizing updated copybooks.

*   **Files Accessed:** Uses `COPY` statements from:
    *   `LTDRG100`: LTCH DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **Working-Storage Section:** Very similar to `LTCAL103`, with differences in `CAL-VERSION` ('V10.5') and the use of `IRFBN105`. Minor numeric constant adjustments may exist.
*   **Linkage Section:** Identical to `LTCAL103`.

### Program Analysis: LTCAL111

**Purpose:** Performs PPS calculations, without state-specific RFBNs.

*   **Files Accessed:** Uses `COPY` statements from:
    *   `LTDRG110`: LTCH DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   Commented out `COPY IRFBN***`: Indicates no state-specific RFBN table included.
*   **Working-Storage Section:** Similar to `LTCAL103`, with `CAL-VERSION` ('V11.1') and adjusted copybooks.
*   **Linkage Section:** Identical to `LTCAL103`.

### Program Analysis: LTCAL123

**Purpose:** Performs PPS calculations, without state-specific RFBNs.

*   **Files Accessed:** Uses `COPY` statements from:
    *   `LTDRG123`: LTCH DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs.
*   **Working-Storage Section:** Similar to previous `LTCAL` programs, updated to version 'V12.3' and relevant copybooks.
*   **Linkage Section:** Identical to `LTCAL103`.

### COPY Member: LTDRG100

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None explicitly accessed. Data is defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### COPY Member: LTDRG110

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None explicitly accessed.
*   **Working-Storage Section:** Similar structure to `LTDRG100`, but `WWM-ENTRY` has `OCCURS 737`.
*   **Linkage Section:** None.

### COPY Member: LTDRG123

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None explicitly accessed.
*   **Working-Storage Section:** Similar structure to `LTDRG110`, but `WWM-ENTRY` has `OCCURS 742`.
*   **Linkage Section:** None.

### Program Analysis: IPDRG080

**Purpose:** Defines a DRG table in WORKING-STORAGE for the year 2007.

*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds DRG data in a packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date ('20071001').
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
    *   The `FILLER` fields contain long strings of alphanumeric data, likely encoded DRG data.
*   **Linkage Section:** None.

### Program Analysis: IPDRG090

**Purpose:** Defines a DRG table in WORKING-STORAGE for the year 2008.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to `IPDRG080`, but with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

### Program Analysis: IRFBN091

**Purpose:** Defines a table of state-specific RFBNs.

*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-INTRO`: Message areas (53 characters each).
    *   `MES-PPS-STATE`: PPS State code (2 characters).
    *   `MES-TOT-PAY`: Total payment amount (9(07)V9(02)).
    *   `MES-SSRFBN`: Holds a single RFBN record (State Code, Filler, State Specific Rate, Filler, Code2, Filler, State Name, Remaining Data).
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Holds RFBN data.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `WK-SSRFBN-REASON-ALL`: Details for each state (State Code, Filler, Rate, Filler, Code2, Filler, State Name, Remaining Data).
*   **Linkage Section:** None.

### Program Analysis: LTCAL087

**Purpose:** Performs PPS calculations, utilizing DRG and RFBN data.

*   **Files Accessed:** None explicitly defined. Uses `COPY` statements to include data from `LTDRG086` and `IPDRG080`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment string.
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates (`FED-FY-BEGIN-03` to `FED-FY-BEGIN-07`).
    *   `COPY LTDRG086`: Includes `LTDRG086` copybook defining `W-DRG-TABLE`.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results (LOS, days, SSOT, blended payment amounts, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS data returned to calling program (Return Code, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PPS-CBSA`: CBSA code (5 characters).
    *   `PRICER-OPT-VERS-SW`: Pricer option and version switch (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, type, MSA data, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (MSA, Effective Date, Wage Indices 1-3).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, IPPS Wage Index, PR IPPS Wage Index).

### Program Analysis: LTCAL091

**Purpose:** Performs PPS calculations for FY09.

*   **Files Accessed:** Relies on data from `COPY` statements (`LTDRG086`, `IPDRG080`).
*   **Working-Storage Section:** Similar to `LTCAL087`, with `CAL-VERSION` as 'V09.1'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to `LTCAL087`.

### Program Analysis: LTCAL094

**Purpose:** Performs PPS calculations for FY09.

*   **Files Accessed:** Relies on data from `COPY` statements (`LTDRG093`, `IPDRG090`, `IRFBN091`).
*   **Working-Storage Section:** Similar to `LTCAL087`, with `CAL-VERSION` as 'V09.4'. Copied data structures reflect year's changes. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to `LTCAL087`.

### Program Analysis: LTCAL095

**Purpose:** Performs PPS calculations for FY09.

*   **Files Accessed:** Relies on data from `COPY` statements (`LTDRG095`, `IPDRG090`, `IRFBN091`).
*   **Working-Storage Section:** Similar to `LTCAL094`, with `CAL-VERSION` as 'V09.5'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to `LTCAL087`.

### COPY Member: LTDRG080

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

### COPY Member: LTDRG086

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to `LTDRG080`, but with different data and 735 occurrences of `WWM-ENTRY`.
*   **Linkage Section:** None.

### COPY Member: LTDRG093

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to `LTDRG086`, but with different data.
*   **Linkage Section:** None.

### COPY Member: LTDRG095

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to `LTDRG093`, but with different data.
*   **Linkage Section:** None.

### Program Analysis: IPDRG063

**Purpose:** Defines a DRG table in WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds raw DRG data as a packed string.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

### Program Analysis: IPDRG071

**Purpose:** Defines a DRG table in WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:** Similar structure to `IPDRG063`, but with `DRG-DATA` occurring 580 times.
*   **Linkage Section:** None.

### Program Analysis: LTCAL064

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, suggesting use of data from that copybook.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes `LTDRG062` copybook (LTCH DRG table).
    *   `HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Various numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `PROV-NEW-HOLD`: Structure to hold provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from a calling program (provider info, DRG, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program (return codes, payment amounts, etc.).
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

### Program Analysis: LTCAL072

**Purpose:** Performs PPS calculations, incorporating short-stay outlier logic.

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (updated to numeric DRG-CODE).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

### Program Analysis: LTCAL075 and LTCAL080

**Purpose:** Perform incremental PPS calculations for subsequent fiscal years.

*   **Files Accessed:** Similar to `LTCAL072`, using `LTDRG075`/`LTDRG080` and `IPDRG063`/`IPDRG071` respectively.
*   **Working-Storage Section:** Similar structure to `LTCAL072`, with differences in constants, rates, and potentially new variables for specific calculations. `CAL-VERSION` will reflect the respective version (e.g., 'V07.5', 'V08.0').
*   **Linkage Section:** Likely similar to `LTCAL072`, maintaining the same core data structures.

### COPY Member: LTDRG075 and LTDRG080

**Purpose:** Define LTCH DRG table data structures for respective fiscal years.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to `LTDRG062`, containing updated DRG codes, weights, ALOS, and potentially additional fields (e.g., `WWM-IPTHRESH` in `LTDRG080`). The number of `WWM-ENTRY` occurrences may vary.
*   **Linkage Section:** None.

### Program Analysis: LTCAL063

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment string.
    *   `CAL-VERSION`: Program version ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `LTDRG057`: Copy of DRG table (same structure as in `LTCAL059`).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA`: CBSA code (5 characters).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data using CBSA (instead of MSA).

### Program Analysis: LTCAL058

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment string.
    *   `CAL-VERSION`: Program version ('V05.8').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG041`: Copy of DRG table (same structure as in `LTCAL043`).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

### Program Analysis: LTCAL059

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment string.
    *   `CAL-VERSION`: Program version ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `LTDRG057`: Copy of DRG table (occurs 512 times).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

### Program Analysis: LTCAL043

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment string.
    *   `CAL-VERSION`: Program version ('C04.3').
    *   `LTDRG041`: Copy of DRG table (occurs 510 times).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, days, SSOT, blended payments).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data (NPI, Provider Number, Patient Status, DRG Code, LOS, Discharge Date, Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results (Return Code, Thresholds, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Indices).

### Program Analysis: LTCAL042

**Purpose:** Performs PPS calculations with updated values.

*   **Files Accessed:** Relies on `COPY LTDRG031`.
*   **Working-Storage Section:** Similar to `LTCAL032`, with differences in:
    *   `CAL-VERSION` ('C04.2').
    *   `PPS-STD-FED-RATE` (35726.18 vs 34956.15).
    *   `H-FIXED-LOSS-AMT` (19590 vs 24450).
    *   `PPS-BDGT-NEUT-RATE` (0.940 vs 0.934).
    *   Adds `H-LOS-RATIO` to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to `LTCAL032`.

### Program Analysis: LTCAL032

**Purpose:** Performs PPS calculations.

*   **Files Accessed:** Relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment literal.
    *   `CAL-VERSION`: Program version ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, days, SSOT, blend codes, rates, Social Security amounts, labor/non-labor portions, fixed loss, facility rate).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing option switches (`PRICER-OPTION-SW`, `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, type, MSA data, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, Wage Indices).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay, LOS, DRG Adjusted Pay, Federal Pay, Final Pay, Facility Costs, New Facility Rate, Outlier Threshold, Submitted DRG, Calc Version, Regular Days Used, LTR Days Used, Blend Year, COLA).

### COPY Member: LTDRG031

**Purpose:** Defines the data structure for the DRG table used by `LTCAL032` and `LTCAL042`.

*   **Files Accessed:** None. Defines data structures.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

### Program Analysis: LTDRG041

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Table of DRG codes and related information as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### Program Analysis: LTDRG057

**Purpose:** Defines the data structure for the LTCH DRG table.

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Table of DRG codes and related data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### Overall Program Flow Summary:

1.  **LTMGR212:** Initiates by reading billing records from `BILLFILE`. It prepares the data and calls `LTOPN212` to perform payment calculations. The results are then formatted and written to `PRTOPER`.
2.  **LTOPN212:** Responsible for loading provider and wage index tables from various input files (`PROV-FILE`, `CBSAX-FILE`, `IPPS-CBSAX-FILE`, `MSAX-FILE`). It determines which tables to use based on the bill's discharge date and pricer option. Subsequently, it calls `LTDRV212` to execute the payment calculations.
3.  **LTDRV212:** This module selects the correct wage index based on discharge date and provider information. It then invokes the appropriate `LTCAL` module (e.g., `LTCAL032`, `LTCAL162`, etc.) to compute the final payment amounts, choosing the specific `LTCAL` module based on the bill's fiscal year.

**Note on Data Structures:** The extensive use of `COPY` statements across various programs indicates a modular design where data structures (like DRG tables) are defined in separate copybook files. This promotes reusability and maintainability. The long strings of numeric data within `FILLER` fields in some `IPDRG` programs are likely encoded DRG data requiring unpacking for full interpretation. Similarly, `W-DRG-FILLS` fields in `LTDRG` programs represent packed data that needs unpacking.

The comments within the code highlight a long history of updates and modifications, suggesting the programs are designed to handle the evolving complexities of prospective payment systems over many years.