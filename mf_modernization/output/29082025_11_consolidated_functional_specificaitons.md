## Data Definition and File Handling

This document consolidates the data definition and file handling information extracted from multiple functional specification documents (L1 through L8). It provides a detailed analysis of COBOL programs, outlining the files they access, their working-storage sections, and their linkage sections.

### Program Analysis

The following programs have been analyzed. Note that where `COPY` statements are mentioned, the analysis focuses on the data structures defined within those copied files, as the actual external files are not explicitly accessed within the provided snippets.

---

### Program: LTMGR212 (from L1_FunctionalSpecification.md)

This program reads billing records, prepares data, and calls `LTOPN212` to calculate payments, then formats and writes results to an output file.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records (422 bytes per record, defined by `BILL-REC`).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports (133 bytes per record, defined by `PRTOPER-LINE`).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal, likely a comment.
    *   `PPMGR-VERSION`: A 5-character field storing the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of the called program.
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field counting lines written to `PRTOPER`, initialized to 65.
    *   `UT1-STAT`, `UT1-STAT1`, `UT1-STAT2`: 2-character field for `BILLFILE` status.
    *   `OPR-STAT`, `OPR-STAT1`, `OPR-STAT2`: 2-character field for `PRTOPER` status.
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (provider NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis/procedure code tables).
    *   `PPS-DATA-ALL`: Structure containing data returned from `LTOPN212` (payment calculation results, wage indices).
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure holding calculated payment amounts (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212` (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (arrays) for CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

---

### Program: LTOPN212 (from L1_FunctionalSpecification.md)

This program loads provider and wage index tables, determines table usage based on discharge date and pricer option, and calls `LTDRV212` for payment calculations.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records (`PROV-REC`, 240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data (`CBSAX-REC`).
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data (`F-IPPS-CBSA-REC`).
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data (`MSAX-REC`).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `OPN-VERSION`: A 5-character field storing the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of the called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating if tables have been loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch.
    *   `W-PROV-NEW-HOLD`: Structure to hold provider records (mirrors `PROV-RECORD-FROM-USER` from LTMGR212).
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status information.
    *   `CBSA-WI-TABLE`: Table to hold CBSA wage index data (up to 10000 entries).
    *   `IPPS-CBSA-WI-TABLE`: Table to hold IPPS CBSA wage index data (up to 10000 entries).
    *   `MSA-WI-TABLE`: Table to hold MSA wage index data (up to 4000 entries).
    *   `WORK-COUNTERS`: Structure containing counters for records read from each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) to hold provider data (divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`).
    *   `PROV-NEW-HOLD`: Structure to hold the provider record passed to `LTDRV212` (mirrors `PROV-RECORD-FROM-USER` from LTMGR212).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTMGR212`.
    *   `PPS-CBSA`: CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTMGR212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTMGR212`.
    *   `PROV-RECORD-FROM-USER`: Provider-specific information passed from `LTMGR212`.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212 for wage index tables.

---

### Program: LTDRV212 (from L1_FunctionalSpecification.md)

This module selects the appropriate wage index, calls the correct `LTCAL` module for payment calculations, and handles the fiscal year logic. It does not directly access files.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `DRV-VERSION`: A 5-character field storing the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of called programs.
    *   `WS-9S`: An 8-character numeric literal with all 9s, used for date comparisons.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields holding wage index related constants for FY2020.
    *   `RUFL-ADJ-TABLE`: Table (defined in COPY `RUFL200`) containing rural floor adjustment factors.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: An index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold fiscal year begin/end dates.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from LTOPN212's tables.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider record passed from `LTOPN212` (mirrors `PROV-NEW-HOLD` in LTOPN212).
    *   `BILL-DATA-FY03-FY15`: Structure for billing data from older fiscal years.
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015 and later (mirrors `BILL-NEW-DATA` in LTMGR212 and LTOPN212).
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

---

### Program: RUFL200 (COPY member) (from L1_FunctionalSpecification.md)

This is a COPY member defining data structures, not a program that directly accesses files or has procedural logic.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Not applicable (as it's a COPY member defining data structures).

*   **Linkage Section:** Not applicable (as it's a COPY member defining data structures).

*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: The main structure containing a table `RUFL-TAB` of rural floor adjustment factors. Each entry includes:
        *   `RUFL-CBSA`: CBSA code.
        *   `RUFL-EFF-DATE`: Effective date.
        *   `RUFL-WI3`: Wage index.
        *   The table has 459 entries.

---

### Program: IPDRG160 (from L2_FunctionalSpecification.md)

This program likely accesses a DRG (Diagnosis Related Group) table file, which is read-only.

*   **Files Accessed:** Likely a DRG table file (no explicit file name provided).

*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item containing DRG table data.
        *   `WK-DRG-DATA`: Group item for temporary holding of file data.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Structured table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Single DRG record structure.
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code.
                    *   `FILLER1` (PIC X(01)): Filler.
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)): Filler.
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean of average length of stay.
                    *   `FILLER3` (PIC X(05)): Filler.
                    *   `DRG-LOW` (PIC X(01)): Indicator ('Y' or 'N').
                    *   `FILLER5` (PIC X(01)): Filler.
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic mean of average length of stay.
                    *   `FILLER6` (PIC X(02)): Filler.
                    *   `DRG-PAC` (PIC X(01)): Post-acute care indicator.
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Special post-acute care indicator.
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.

*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG170 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, likely accesses a read-only DRG table file for 2016.

*   **Files Accessed:** Likely a DRG table file for 2016 (no explicit file name provided).

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`. DRG data is specific to 2016.

*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG181 (from L2_FunctionalSpecification.md)

Likely accesses a read-only DRG table file for 2017.

*   **Files Accessed:** Likely a DRG table file for 2017 (no explicit file name provided).

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20171001' and `DRG-TAB` having `OCCURS 754`. DRG data is specific to 2017.

*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG190 (from L2_FunctionalSpecification.md)

Likely accesses a read-only DRG table file for 2018.

*   **Files Accessed:** Likely a DRG table file for 2018 (no explicit file name provided).

*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20181001' and `DRG-TAB` having `OCCURS 761`. Data reflects 2018 DRGs.

*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG200 (from L2_FunctionalSpecification.md)

Likely accesses a read-only DRG table file for 2019.

*   **Files Accessed:** Likely a DRG table file for 2019 (no explicit file name provided).

*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20191001' and `DRG-TAB` having `OCCURS 761`. Data is for 2019 DRGs, noting the addition of DRG 319 and 320.

*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG211 (from L2_FunctionalSpecification.md)

Likely accesses a read-only DRG table file for 2020.

*   **Files Accessed:** Likely a DRG table file for 2020 (no explicit file name provided).

*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20201001' and `DRG-TAB` having `OCCURS 767`. Data is for 2020 DRGs, noting changes in some DRG descriptions.

*   **Linkage Section:** Not present in the provided code.

---

### Program: LTCAL162 (from L2_FunctionalSpecification.md)

This program likely accesses a Provider-Specific File (PSF), a CBSA wage index file, and DRG table files (via COPY statements).

*   **Files Accessed:**
    *   Provider-Specific File (PSF) containing wage indices, cost-to-charge ratios, etc.
    *   CBSA wage index file.
    *   LTCH DRG table file (`LTDRG160`) and IPPS DRG table file (`IPDRG160`) via COPY statements.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive filler.
    *   `CAL-VERSION`: Program version number ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in the program.
    *   `PROGRAM-FLAGS`: Flags to control program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for payment.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data copied from DRG tables.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Input bill data from a calling program (likely `LTDRV`).
    *   `PPS-DATA-ALL`: Output PPS calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches indicating the versions of the pricer option and other driver programs.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

### Program: LTCAL170 (from L2_FunctionalSpecification.md)

Similar to LTCAL162, likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG170`, `IPDRG170`).

*   **Files Accessed:** PSF, CBSA wage index file, LTCH/IPPS DRG tables (`LTDRG170`, `IPDRG170`) via COPY statements.

*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.

*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

### Program: LTCAL183 (from L2_FunctionalSpecification.md)

Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG181`, `IPDRG181`).

*   **Files Accessed:** PSF, CBSA wage index file, LTCH/IPPS DRG tables (`LTDRG181`, `IPDRG181`) via COPY statements.

*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Variables related to Subclause II have been removed.

*   **Linkage Section:** Similar to LTCAL170, with the removal of fields related to Subclause II.

---

### Program: LTCAL190 (from L2_FunctionalSpecification.md)

Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG190`, `IPDRG190`).

*   **Files Accessed:** PSF, CBSA wage index file, LTCH/IPPS DRG tables (`LTDRG190`, `IPDRG190`) via COPY statements.

*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.

*   **Linkage Section:** Similar to LTCAL183.

---

### Program: LTCAL202 (from L2_FunctionalSpecification.md)

Similar to previous LTCAL programs, accessing PSF, CBSA wage index file, and DRG tables (`LTDRG200`, `IPDRG200`).

*   **Files Accessed:** PSF, CBSA wage index file, LTCH/IPPS DRG tables (`LTDRG200`, `IPDRG200`) via COPY statements.

*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.

*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` to handle the Disproportionate Patient Percentage (DPP) adjustment.

---

### Program: LTCAL212 (from L2_FunctionalSpecification.md)

Similar to LTCAL202, accessing PSF, CBSA wage index file, and DRG tables (`LTDRG210`, `IPDRG211`).

*   **Files Accessed:** PSF, CBSA wage index file, LTCH/IPPS DRG tables (`LTDRG210`, `IPDRG211`) via COPY statements.

*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Adds `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.

*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

---

### Program: LTDRG160 (from L2_FunctionalSpecification.md)

This is a copybook likely containing LTCH DRG table data for FY15.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Defines the structure of the LTCH DRG table.
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.

*   **Linkage Section:** None.

---

### Program: LTDRG170 (from L2_FunctionalSpecification.md)

This is a copybook similar to LTDRG160, containing LTCH DRG data for FY16.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.

*   **Linkage Section:** None.

---

### Program: LTDRG181 (from L2_FunctionalSpecification.md)

This is a copybook containing LTCH DRG data for FY18.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Structurally similar to LTDRG160 and LTDRG170, with `WWM-ENTRY` having `OCCURS 744`.

*   **Linkage Section:** None.

---

### Program: LTDRG190 (from L2_FunctionalSpecification.md)

This is a copybook containing LTCH DRG data for FY19.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.

*   **Linkage Section:** None.

---

### Program: LTDRG210 (from L2_FunctionalSpecification.md)

This is a copybook containing LTCH DRG data for FY21.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.

*   **Linkage Section:** None.

---

### Program: IPDRG104 (from L4_FunctionalSpecification.md)

This program uses a `COPY IPDRG104` statement, implying it includes data from a file containing a DRG table.

*   **Files Accessed:** None explicitly listed. Relies on data from `COPY IPDRG104`.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: A table containing DRG data.
        *   `D-TAB`: Holds DRG data in a packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single year.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

### Program: IPDRG110 (from L4_FunctionalSpecification.md)

Similar to `IPDRG104`, uses a `COPY IPDRG110` statement referencing a DRG data file.

*   **Files Accessed:** None explicitly listed. Relies on data from `COPY IPDRG110`.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table, structurally identical to `IPDRG104`, but `DRG-DATA OCCURS 1000`.

*   **Linkage Section:** None.

---

### Program: IPDRG123 (from L4_FunctionalSpecification.md)

Uses a `COPY IPDRG123` statement, indicating inclusion of DRG data from another file.

*   **Files Accessed:** None explicitly listed. Relies on data from `COPY IPDRG123`.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table, structurally similar to `IPDRG104`, but `DRG-DATA OCCURS 1000`.

*   **Linkage Section:** None.

---

### Program: IRFBN102 (from L4_FunctionalSpecification.md)

The `COPY IRFBN102` statement suggests data from a file containing state-specific Rural Floor Budget Neutrality Factors (RFBNS).

*   **Files Accessed:** None explicitly listed. Relies on data from `COPY IRFBN102`.

*   **Working-Storage Section:**
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `WK-SSRFBN-STATE PIC 99`: State code.
                    *   `FILLER PIC XX`: Filler.
                    *   `WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `FILLER PIC XX`: Filler.
                    *   `WK-SSRFBN-CODE2 PIC 99`: Unclear code.
                    *   `FILLER PIC X`: Filler.
                    *   `WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`, `MES-TOT-PAY`: Message and data holding fields.
    *   `MES-SSRFBN`: Holds a single RFBN record, structurally identical to `WK-SSRFBN-REASON-ALL`.

*   **Linkage Section:** None.

---

### Program: IRFBN105 (from L4_FunctionalSpecification.md)

Uses a `COPY IRFBN105` statement, referencing a file presumably containing updated RFBN data.

*   **Files Accessed:** None explicitly listed. Relies on data from `COPY IRFBN105`.

*   **Working-Storage Section:**
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs, structurally identical to `IRFBN102`.
    *   Message and data holding fields (`MES-ADD-PROV`, etc.).
    *   `MES-SSRFBN`: Holds a single RFBN record.

*   **Linkage Section:** None.

---

### Program: LTCAL103 (from L4_FunctionalSpecification.md)

This program uses `COPY` statements to include data from `LTDRG100`, `IPDRG104`, and `IRFBN102`.

*   **Files Accessed:** Relies on data from `COPY LTDRG100`, `COPY IPDRG104`, `COPY IRFBN102`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive comment.
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds calculated PPS components, with numerous numeric variables for payment calculation aspects.
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, codes, indices, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, Effective Date, Wage Indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size indicator, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from the calling program (NPI, provider number, DRG code, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105 (from L4_FunctionalSpecification.md)

Includes data through `COPY` statements from `LTDRG100`, `IPDRG104`, and `IRFBN105`.

*   **Files Accessed:** Relies on data from `COPY LTDRG100`, `COPY IPDRG104`, `COPY IRFBN105`.

*   **Working-Storage Section:** Very similar to `LTCAL103`, with differences in `CAL-VERSION` ('V10.5'), copybooks used (`IRFBN105`), and minor constant adjustments.

*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL111 (from L4_FunctionalSpecification.md)

Includes data through `COPY` statements from `LTDRG110`, `IPDRG110`, and a commented-out `COPY IRFBN***`.

*   **Files Accessed:** Relies on data from `COPY LTDRG110`, `COPY IPDRG110`. No state-specific RFBN table is used in this version.

*   **Working-Storage Section:** Similar to `LTCAL103`, with `CAL-VERSION` updated to 'V11.1' and copybooks adjusted. Absence of a state-specific RFBN table.

*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL123 (from L4_FunctionalSpecification.md)

Includes data through `COPY` statements from `LTDRG123`, `IPDRG123`, and commented-out RFBN copybooks.

*   **Files Accessed:** Relies on data from `COPY LTDRG123`, `COPY IPDRG123`. No state-specific RFBN table is used.

*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version 'V12.3' and relevant copybooks.

*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTDRG100 (from L4_FunctionalSpecification.md)

This program defines a DRG table within `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Program: LTDRG110 (from L4_FunctionalSpecification.md)

This program defines a DRG table within `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Program: LTDRG123 (from L4_FunctionalSpecification.md)

This program defines a DRG table within `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Program: IPDRG080 (from L5_FunctionalSpecification.md)

This program defines a DRG table in `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: A table containing DRG data.
        *   `D-TAB`: Holds DRG data in a packed format. Includes `FILLER PIC X(08) VALUE '20071001'` and subsequent `FILLER` fields containing alphanumeric data likely representing DRG records.
        *   `DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `DRGX-EFF-DATE PIC X(08)`: Effective Date.
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.

*   **Linkage Section:** None.

---

### Program: IPDRG090 (from L5_FunctionalSpecification.md)

Similar to IPDRG080, defines a DRG table in `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.

*   **Linkage Section:** None.

---

### Program: IRFBN091 (from L5_FunctionalSpecification.md)

Defines message areas and a table of state-specific RFBNs in `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`, `MES-TOT-PAY`: Message and data holding fields.
    *   `MES-SSRFBN`: Holds a single RFBN record.
        *   `MES-SSRFBN-STATE PIC 99`: State Code.
        *   `FILLER PIC XX`.
        *   `MES-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
        *   `FILLER PIC XX`.
        *   `MES-SSRFBN-CODE2 PIC 99`.
        *   `FILLER PIC X`.
        *   `MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `MES-SSRFBN-REST PIC X(22)`.
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `FILLER PIC XX`.
                    *   `WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `FILLER PIC XX`.
                    *   `WK-SSRFBN-CODE2 PIC 99`.
                    *   `FILLER PIC X`.
                    *   `WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `WK-SSRFBN-REST PIC X(22)`.

*   **Linkage Section:** None.

---

### Program: LTCAL087 (from L5_FunctionalSpecification.md)

This program uses `COPY` statements to include data from `LTDRG086` and `IPDRG080`.

*   **Files Accessed:** None explicitly defined. Relies on data from `COPY LTDRG086` and `COPY IPDRG080`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `COPY LTDRG086`: Includes the `LTDRG086` copybook, containing `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payment amounts, etc.).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program.
        *   `B-NPI10` (NPI), `B-PROVIDER-NO`, `B-PATIENT-STATUS`, `B-DRG-CODE`, `B-LOS`, `B-COV-DAYS`, `B-LTR-DAYS`, `B-DISCHARGE-DATE`, `B-COV-CHARGES`, `B-SPEC-PAY-IND`, `FILLER`.
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program (RTC, charge threshold, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure. Includes NPI, provider number, dates, waiver code, cost data, etc.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index record (MSA, Effective Date, Wage Indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record.

---

### Program: LTCAL091 (from L5_FunctionalSpecification.md)

Similar to LTCAL087, uses files implied by `COPY` statements (`LTDRG086`, `IPDRG080`).

*   **Files Accessed:** Relies on data from `COPY LTDRG086` and `COPY IPDRG080`.

*   **Working-Storage Section:** Very similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data structures reflect year's changes.

*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL094 (from L5_FunctionalSpecification.md)

Uses files implied by `COPY` statements (`LTDRG093`, `IPDRG090`, `IRFBN091`).

*   **Files Accessed:** Relies on data from `COPY LTDRG093`, `COPY IPDRG090`, `COPY IRFBN091`.

*   **Working-Storage Section:** Similar to LTCAL087 and LTCAL091, with `CAL-VERSION` as 'V09.4'. Copied data structures reflect year's changes. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.

*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL095 (from L5_FunctionalSpecification.md)

Uses files implied by `COPY` statements (`LTDRG095`, `IPDRG090`, `IRFBN091`).

*   **Files Accessed:** Relies on data from `COPY LTDRG095`, `COPY IPDRG090`, `COPY IRFBN091`.

*   **Working-Storage Section:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. Copied data structures reflect year's changes.

*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTDRG080 (from L5_FunctionalSpecification.md)

This program defines a DRG table within `WORKING-STORAGE`.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds the LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.

*   **Linkage Section:** None.

---

### Program: LTDRG086 (from L5_FunctionalSpecification.md)

Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.

*   **Linkage Section:** None.

---

### Program: LTDRG093 (from L5_FunctionalSpecification.md)

Similar structure to LTDRG086, but with different data.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.

*   **Linkage Section:** None.

---

### Program: LTDRG095 (from L5_FunctionalSpecification.md)

Similar structure to LTDRG093, but with different data.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.

*   **Linkage Section:** None.

---

### Program: IPDRG063 (from L6_FunctionalSpecification.md)

This program defines a DRG table in `WORKING-STORAGE`.

*   **Files Accessed:** None explicitly defined.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: A table containing DRG data.
        *   `D-TAB`: Holds raw DRG data as a packed string.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

### Program: IPDRG071 (from L6_FunctionalSpecification.md)

Similar to IPDRG063, defines a DRG table in `WORKING-STORAGE`.

*   **Files Accessed:** None explicitly defined.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: Similar structure to IPDRG063, a table of DRG data.
        *   `D-TAB`: Raw DRG data as a packed string.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 580 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

### Program: LTCAL064 (from L6_FunctionalSpecification.md)

Uses `COPY LTDRG062.` which suggests data from a file defined in that copybook.

*   **Files Accessed:** None explicitly defined. Uses data from `COPY LTDRG062`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook, which contains a DRG table (`WWM-ENTRY`).
    *   `HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results.
    *   Various numeric and alphanumeric variables for PPS calculations and payment amounts.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `PROV-NEW-HOLD`: Structure to hold provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from a calling program. Includes provider info, DRG code, LOS, discharge date, and charges.
    *   `PPS-DATA-ALL`: PPS calculation results returned to the calling program. Includes return codes, payment amounts, and other calculated values.
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

### Program: LTCAL072 (from L6_FunctionalSpecification.md)

Uses data from copybooks `LTDRG062` and `IPDRG063`.

*   **Files Accessed:** None explicitly defined. Uses data from `COPY LTDRG062` and `COPY IPDRG063`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (LTCH DRG table).
    *   `COPY IPDRG063`: Includes the `IPDRG063` copybook (IPPS DRG table).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices, etc.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data for LTCH.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data for IPPS.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE).
    *   `PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

### Programs: LTCAL075, LTCAL080 (from L6_FunctionalSpecification.md)

These programs are expected to be similar to LTCAL072, with incremental changes in constants, rates, and potentially additional variables reflecting evolving methodologies.

*   **Files Accessed:** Similar to LTCAL072, using data from copybooks like `LTDRG075`, `LTDRG080`, and IPDRG tables.

*   **Working-Storage Section:** Expected to maintain the basic structure of LTCAL072, with updated constants, rates, and potentially new variables for version-specific calculations.

*   **Linkage Section:** Expected to maintain the basic structure of LTCAL072.

---

### Program: LTDRG062 (from L6_FunctionalSpecification.md)

This copybook defines DRG table data.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains raw data for the LTCH DRG table as packed strings.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefines `W-DRG-FILLS` to structure the data.
        *   `WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: The LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Programs: LTDRG075, LTDRG080 (from L6_FunctionalSpecification.md)

These copybooks define DRG tables with updated data.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to LTDRG062, but containing updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.

*   **Linkage Section:** None.

---

### Program: LTCAL043 (from L7_FunctionalSpecification.md)

No files explicitly defined in `FILE-CONTROL`. Uses `COPY LTDRG041` for DRG table data.

*   **Files Accessed:** Relies on data from `COPY LTDRG041`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('C04.3').
    *   `LTDRG041`: Copy of DRG table data.
        *   `WWM-ENTRY`: Array (occurs 510 times) with DRG data: `WWM-DRG` (3-char code), `WWM-RELWT` (relative weight), `WWM-ALOS` (average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payment amounts, etc.).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to/from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results (RTC, threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, provider number, dates, waiver code, various provider variables and cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, Effective Date, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`).

---

### Program: LTCAL058 (from L7_FunctionalSpecification.md)

Similar to LTCAL043, uses `COPY LTDRG041` for DRG table data.

*   **Files Accessed:** Relies on data from `COPY LTDRG041`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V05.8').
    *   `PROGRAM-CONSTANTS`: Holds dates for federal fiscal years.
    *   `LTDRG041`: Copy of DRG table (same structure as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Structure for holding intermediate PPS calculation results (same as in LTCAL043).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

---

### Program: LTCAL059 (from L7_FunctionalSpecification.md)

Uses `COPY LTDRG057` for DRG table data.

*   **Files Accessed:** Relies on data from `COPY LTDRG057`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table.
        *   `WWM-ENTRY`: Array (occurs 512 times) with DRG data: `WWM-DRG` (3-char code), `WWM-RELWT` (relative weight), `WWM-ALOS` (average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in previous programs).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in previous programs).

---

### Program: LTCAL063 (from L7_FunctionalSpecification.md)

Uses `COPY LTDRG057` for DRG table data.

*   **Files Accessed:** Relies on data from `COPY LTDRG057`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table (same structure as in LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA`: A 5-character field for CBSA code.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

---

### Program: LTDRG041 (from L7_FunctionalSpecification.md)

This is a data definition file, not a program.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Defines a DRG table structure.
    *   `W-DRG-FILLS`: Table of DRG codes and related information as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Program: LTDRG057 (from L7_FunctionalSpecification.md)

This is a data definition file.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Defines a DRG table structure.
    *   `W-DRG-FILLS`: Table of DRG codes and related data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:** None.

---

### Program: LTCAL032 (from L8_FunctionalSpecification.md)

No explicit files in `FILE-CONTROL`. Uses `COPY LTDRG031` for DRG table data.

*   **Files Accessed:** Relies on data from `COPY LTDRG031`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string indicating working storage.
    *   `CAL-VERSION`: Program version ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blend amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Version information and pricing option switches (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, Provider Number, State, dates, waiver code, intermediary number, provider type, census division, MSA data, facility specific rate, COLA, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data (MSA, Effective Date, three wage index values).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Contains bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Contains calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA, etc.).

---

### Program: LTCAL042 (from L8_FunctionalSpecification.md)

Same file dependencies as LTCAL032 (`COPY LTDRG031`).

*   **Files Accessed:** Relies on data from `COPY LTDRG031`.

*   **Working-Storage Section:** Similar to LTCAL032, with key differences:
    *   `CAL-VERSION`: 'C04.2'.
    *   `PPS-STD-FED-RATE`: Different value (35726.18 vs 34956.15).
    *   `H-FIXED-LOSS-AMT`: Different value (19590 vs 24450).
    *   `PPS-BDGT-NEUT-RATE`: Different value (0.940 vs 0.934).
    *   Adds `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.

*   **Linkage Section:** Identical to LTCAL032.

---

### Program: LTDRG031 (from L8_FunctionalSpecification.md)

This is a copybook defining DRG table data structures used by other programs.

*   **Files Accessed:** None (as it's a COPY member).

*   **Working-Storage Section:** Defines DRG table data.
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.

*   **Linkage Section:** None.

---

### Overall Program Flow and Data Usage Summary

The analyzed programs primarily focus on calculating prospective payments based on billing and provider data. They extensively use DRG (Diagnosis Related Group) tables and wage index data, often incorporated via `COPY` statements, indicating a reliance on external data files that are managed separately.

*   **LTMGR212** acts as a driver, reading billing files, calling `LTOPN212` for calculations, and producing reports.
*   **LTOPN212** is responsible for loading various lookup tables (provider, wage indices) and then calling `LTDRV212`.
*   **LTDRV212** performs the core logic of selecting the appropriate wage index and calling specific calculation modules (`LTCAL` programs) based on fiscal year and other criteria.
*   **LTCAL** programs (e.g., `LTCAL162`, `LTCAL043`, `LTCAL032`) contain the detailed payment calculation logic, incorporating DRG weights, wage indices, and provider-specific rates. These programs often use multiple `COPY` statements to bring in DRG data and other necessary tables.
*   **IPDRGxxxx** and **LTDRGxxxx** programs (or copybooks) primarily define the structure and content of DRG tables for different fiscal years.
*   **IRFBNxxxx** programs/copybooks define structures for state-specific Rural Floor Budget Neutrality Factors.

The extensive use of version numbers (e.g., `CAL-VERSION`, `PPMGR-VERSION`, `OPN-VERSION`) and the evolution of data structures across different versions (e.g., addition of COVID-19 related fields, changes in DRG counts) highlight a long maintenance history and adaptation to regulatory changes in healthcare payment systems. The programs are designed to be modular, with specific calculation logic encapsulated in different `LTCAL` versions.