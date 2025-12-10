## Data Definition and File Handling

This document consolidates and analyzes the "Data Definition and File Handling" sections extracted from multiple functional specification files (L1 through L8). It provides a detailed overview of the COBOL programs, their accessed files, working-storage data structures, and linkage sections.

The programs analyzed are primarily related to healthcare prospective payment systems (PPS), handling billing data, provider information, and various tables such as Diagnosis Related Groups (DRGs) and wage indices.

---

### Program: LTMGR212

This program reads billing records, prepares data, calls `LTOPN212` for payment calculations, and formats output for a prospective payment report.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format defined by `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format defined by `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal (comment).
    *   `PPMGR-VERSION`: A 5-character field for program version ('M21.2').
    *   `LTOPN212`: An 8-character literal for the called program name.
    *   `EOF-SW`: A 1-digit numeric field for end-of-file status (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field for counting output lines, initialized to 65.
    *   `UT1-STAT`: A 2-character field for `BILLFILE` status (`UT1-STAT1`, `UT1-STAT2`).
    *   `OPR-STAT`: A 2-character field for `PRTOPER` status (`OPR-STAT1`, `OPR-STAT2`).
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (provider NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis/procedure code tables).
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212` (payment calculation results, wage indices).
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure for payment amounts calculated by `LTOPN212` (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Single character indicating pricing option.
        *   `PPS-VERSIONS`: Structure for version numbers passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (arrays) for CBSA/MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:**
    *   LTMGR212 does not have a Linkage Section.

---

### Program: LTOPN212

This program loads provider and wage index tables, determines table usage based on discharge date and pricer option, and calls `LTDRV212` for payment calculations.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file for provider records. Record layout defined as `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file for CBSA wage index data. Record layout defined as `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file for IPPS CBSA wage index data. Record layout defined as `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file for MSA wage index data. Record layout defined as `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `OPN-VERSION`: A 5-character field for program version ('021.2').
    *   `LTDRV212`: An 8-character literal for the called program name.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating if tables are loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field for end-of-file status.
    *   `W-PROV-NEW-HOLD`: Structure to hold provider records from file or passed in, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status of input files.
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data from `CBSAX-FILE` (up to 10000 entries, indexed by `CU1`, `CU2`).
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data from `IPPS-CBSAX-FILE` (up to 10000 entries, indexed by `MA1`, `MA2`, `MA3`).
    *   `MSA-WI-TABLE`: Table for MSA wage index data from `MSAX-FILE` (up to 4000 entries, indexed by `MU1`, `MU2`).
    *   `WORK-COUNTERS`: Structure containing counters for records read from each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) for provider data from `PROV-FILE`, divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3` (indexed by `PX1`, `PD2`, `PD3`).
    *   `PROV-NEW-HOLD`: Structure to hold the provider record for `LTDRV212`, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirroring `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTMGR212`, mirroring `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: 5-character CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTMGR212`, mirroring `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTMGR212`, mirroring `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Provider-specific information passed from `LTMGR212`, mirroring `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, for wage index tables.

---

### Program: LTDRV212

This module selects the appropriate wage index, calls the correct `LTCAL` module for payment calculation based on fiscal year, and does not directly access files.

*   **Files Accessed:**
    *   LTDRV212 does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `DRV-VERSION`: A 5-character field for program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals for names of called programs.
    *   `WS-9S`: An 8-character numeric literal of all 9s for date comparisons.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table (from COPY RUFL200) containing rural floor adjustment factors for CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures for calculated fiscal year begin/end dates.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA/CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from LTOPN212 tables.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider record passed from `LTOPN212`, mirroring `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure for billing data from older fiscal years.
    *   `BILL-NEW-DATA`: Structure for billing data from FY2015 onwards, mirroring `BILL-NEW-DATA` in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, for wage index tables and record counts.

---

### COPY Member: RUFL200

This is a COPY member, not a program. It defines data structures for rural floor adjustment factors.

*   **Files Accessed:**
    *   This is a COPY member; it does not directly access files. It defines data structures.

*   **Working-Storage Section:**
    *   Not applicable as it's a data definition member.

*   **Linkage Section:**
    *   Not applicable as it's a data definition member.

*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: The main structure containing `RUFL-TAB`.
        *   `RUFL-TAB`: Table of rural floor adjustment factors, each entry containing:
            *   `RUFL-CBSA`: CBSA code.
            *   `RUFL-EFF-DATE`: Effective date.
            *   `RUFL-WI3`: Wage index.
        *   The table has 459 entries.

---

### Program: IPDRG160

This program likely accesses a DRG table file for the year 2015.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only). No explicit file names mentioned.

*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item for DRG table data.
        *   `WK-DRG-DATA`: Group item for DRG data in a literal, record-like format (temporary holding).
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Redefined structure for table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Group item for a single DRG record.
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
                    *   `DRG-PAC` (PIC X(01)): Indicator (post-acute care).
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Indicator (special post-acute care).
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: IPDRG170

This program likely accesses a DRG table file for the year 2016.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only) for 2016.

*   **Working-Storage Section:**
    *   Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20161001' and `DRG-TAB` has `OCCURS 757`. DRG data is specific to 2016.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: IPDRG181

This program likely accesses a DRG table file for the year 2017.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only) for 2017.

*   **Working-Storage Section:**
    *   Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20171001' and `DRG-TAB` has `OCCURS 754`. DRG data is specific to 2017.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: IPDRG190

This program likely accesses a DRG table file for the year 2018.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only) for 2018.

*   **Working-Storage Section:**
    *   Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20181001' and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2018.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: IPDRG200

This program likely accesses a DRG table file for the year 2019.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only) for 2019.

*   **Working-Storage Section:**
    *   Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20191001' and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2019. Note the addition of DRG 319 and 320.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: IPDRG211

This program likely accesses a DRG table file for the year 2020.

*   **Files Accessed:**
    *   Likely accesses a DRG table file (read-only) for 2020.

*   **Working-Storage Section:**
    *   Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20201001' and `DRG-TAB` has `OCCURS 767`. DRG data is specific to 2020. Note the change in some DRG descriptions.

*   **Linkage Section:**
    *   Not present in the provided code.

---

### Program: LTCAL162

This program likely accesses a Provider-Specific File (PSF), a CBSA wage index file, and DRG table files.

*   **Files Accessed:**
    *   Provider-specific file (PSF) containing wage indices, cost-to-charge ratios, etc.
    *   CBSA wage index file.
    *   LTCH DRG table file (`LTDRG160`) and IPPS DRG table file (`IPDRG160`) included via COPY statements (read-only).

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
    *   `PRICER-OPT-VERS-SW`: Switches indicating versions of the pricer option and driver programs.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

### Program: LTCAL170

This program likely accesses a PSF, CBSA wage index file, and DRG table files for FY17.

*   **Files Accessed:**
    *   Similar to LTCAL162, likely PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG170`, `IPDRG170`).

*   **Working-Storage Section:**
    *   Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.

*   **Linkage Section:**
    *   Identical to LTCAL162's Linkage Section, except for the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

### Program: LTCAL183

This program likely accesses a PSF, CBSA wage index file, and DRG table files for FY18.

*   **Files Accessed:**
    *   Likely PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG181`, `IPDRG181`).

*   **Working-Storage Section:**
    *   Similar to LTCAL170, with `CAL-VERSION` as 'V18.3'. Updated for FY18. Variables related to Subclause II have been removed.

*   **Linkage Section:**
    *   Similar to LTCAL170, with the removal of fields related to Subclause II.

---

### Program: LTCAL190

This program likely accesses a PSF, CBSA wage index file, and DRG table files for FY19.

*   **Files Accessed:**
    *   Likely PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG190`, `IPDRG190`).

*   **Working-Storage Section:**
    *   Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0'. Updated for FY19.

*   **Linkage Section:**
    *   Similar to LTCAL183.

---

### Program: LTCAL202

This program likely accesses a PSF, CBSA wage index file, and DRG table files for FY20.

*   **Files Accessed:**
    *   Similar to previous LTCAL programs, likely PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG200`, `IPDRG200`).

*   **Working-Storage Section:**
    *   Similar to LTCAL190, with `CAL-VERSION` as 'V20.2'. Updated for FY20. Includes additions related to COVID-19 processing.

*   **Linkage Section:**
    *   Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` to handle the Disproportionate Patient Percentage (DPP) adjustment.

---

### Program: LTCAL212

This program likely accesses a PSF, CBSA wage index file, and DRG table files for FY21.

*   **Files Accessed:**
    *   Similar to LTCAL202, likely PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG210`, `IPDRG211`).

*   **Working-Storage Section:**
    *   Similar to LTCAL202, with `CAL-VERSION` as 'V21.2'. Updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.

*   **Linkage Section:**
    *   Similar to LTCAL202, with no additional fields.

---

### COPY Member: LTDRG160

This copybook likely contains the LTCH DRG table data for FY15.

*   **Files Accessed:**
    *   This is a copybook containing data definitions, not a program accessing files.

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.

*   **Linkage Section:**
    *   Not applicable.

---

### COPY Member: LTDRG170

This copybook contains LTCH DRG data for FY16.

*   **Files Accessed:**
    *   This is a copybook containing data definitions.

*   **Working-Storage Section:**
    *   Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.

*   **Linkage Section:**
    *   Not applicable.

---

### COPY Member: LTDRG181

This copybook contains LTCH DRG data for FY18.

*   **Files Accessed:**
    *   This is a copybook containing data definitions.

*   **Working-Storage Section:**
    *   Structurally similar to LTDRG160 and LTDRG170, with `WWM-ENTRY` having `OCCURS 744`.

*   **Linkage Section:**
    *   Not applicable.

---

### COPY Member: LTDRG190

This copybook contains LTCH DRG data for FY19.

*   **Files Accessed:**
    *   This is a copybook containing data definitions.

*   **Working-Storage Section:**
    *   Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.

*   **Linkage Section:**
    *   Not applicable.

---

### COPY Member: LTDRG210

This copybook contains LTCH DRG data for FY21.

*   **Files Accessed:**
    *   This is a copybook containing data definitions.

*   **Working-Storage Section:**
    *   Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.

*   **Linkage Section:**
    *   Not applicable.

---

### Program: IPDRG104

This program uses `COPY IPDRG104`, implying it includes DRG data from another file.

*   **Files Accessed:**
    *   Uses a `COPY IPDRG104` statement, referencing a file containing a DRG table.

*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single year.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the DRG data.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG110

This program uses `COPY IPDRG110`, implying it includes DRG data from another file.

*   **Files Accessed:**
    *   Uses a `COPY IPDRG110` statement, referencing a file containing DRG data.

*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data, structurally identical to IPDRG104.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG123

This program uses `COPY IPDRG123`, implying it includes DRG data from another file.

*   **Files Accessed:**
    *   Uses a `COPY IPDRG123` statement, indicating inclusion of DRG data from another file.

*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table, structurally similar to IPDRG104.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IRFBN102

This program uses `COPY IRFBN102`, referencing a file containing state-specific Rural Floor Budget Neutrality Factors (RFBNS).

*   **Files Accessed:**
    *   `COPY IRFBN102` statement suggests data from a file containing RFBNS.

*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNS.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Another code (purpose unclear).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (purpose unclear).
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: State code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record, structurally identical to `WK-SSRFBN-REASON-ALL`.

*   **Linkage Section:**
    *   None.

---

### Program: IRFBN105

This program uses `COPY IRFBN105`, referencing a file presumably containing updated RFBN data.

*   **Files Accessed:**
    *   Uses a `COPY IRFBN105` statement, referencing a file with RFBN data.

*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNS, structurally identical to IRFBN102.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Code (unclear purpose).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: State code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record.

*   **Linkage Section:**
    *   None.

---

### Program: LTCAL103

This program uses COPY statements to include data from `LTDRG100`, `IPDRG104`, and `IRFBN102`.

*   **Files Accessed:**
    *   Uses `COPY` statements to include data from `LTDRG100` (LTC DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN102` (IPPS state-specific RFBNs).

*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103 - W O R K I N G S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components. Contains numerous numeric variables for payment calculation aspects.
    *   `01 PPS-DATA-ALL`: Holds final PPS calculation results (return code, charge threshold, etc.).
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, intermediary number, provider type, census division, MSA data, various parameters).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record.
        *   `05 W-CBSA PIC X(5)`: CBSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective date.
        *   `05 W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA code, size indicator, effective date, wage indices).
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program (NPI, provider number, patient status, DRG code, LOS, covered days, LTR days, discharge date, covered charges, special pay indicator).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105

This program uses COPY statements to include data from `LTDRG100`, `IPDRG104`, and `IRFBN105`.

*   **Files Accessed:**
    *   Includes data through `COPY` statements from `LTDRG100` (LTC DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN105` (IPPS state-specific RFBNs).

*   **Working-Storage Section:**
    *   Very similar to `LTCAL103`. Main differences: `CAL-VERSION` is 'V10.5', uses `IRFBN105`, and minor numeric constant adjustments.

*   **Linkage Section:**
    *   Identical to `LTCAL103`.

---

### Program: LTCAL111

This program uses COPY statements to include data from `LTDRG110` and `IPDRG110`. `IRFBN***` is commented out.

*   **Files Accessed:**
    *   Includes data through `COPY` statements from `LTDRG110` (LTC DRG table) and `IPDRG110` (IPPS DRG data). A `COPY IRFBN***` statement is commented out, indicating no state-specific RFBN table is included.

*   **Working-Storage Section:**
    *   Similar to `LTCAL103`, with `CAL-VERSION` updated to 'V11.1' and copybooks adjusted. No state-specific RFBN table is used.

*   **Linkage Section:**
    *   Identical to `LTCAL103`.

---

### Program: LTCAL123

This program uses COPY statements to include data from `LTDRG123` and `IPDRG123`. RFBN copybook is commented out.

*   **Files Accessed:**
    *   Includes data through `COPY` statements from `LTDRG123` (LTC DRG table) and `IPDRG123` (IPPS DRG data). RFBN copybook is commented out.

*   **Working-Storage Section:**
    *   Similar to previous LTCAL programs, updated to version 'V12.3' and relevant copybooks. No state-specific RFBN table is used.

*   **Linkage Section:**
    *   Identical to `LTCAL103`.

---

### Program: LTCAL103 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `01 LTDRG100`: Copy of LTC DRG table data.
        *   `01 W-DRG-FILLS`: Holds DRG data in packed format.
        *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG data access.
            *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
                *   `05 WWM-DRG PIC X(3)`: DRG code.
                *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
                *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section (continued):**
    *   `01 PROV-NEW-HOLD`: Provider data structure includes nested groups:
        *   `PROV-NEWREC-HOLD1`:
            *   `P-NEW-NPI10`: NPI (8 chars + filler).
            *   `P-NEW-PROVIDER-NO`: Provider number (6 chars, includes state code).
            *   `P-NEW-DATE-DATA`: Effective, FY Begin, Report, Termination dates.
            *   `P-NEW-WAIVER-CODE`: Waiver code ('Y' = waiver state).
            *   `P-NEW-INTER-NO`: Internship number.
            *   `P-NEW-PROVIDER-TYPE`: Provider type.
            *   `P-NEW-CURRENT-CENSUS-DIV`: Census division.
            *   `P-NEW-MSA-DATA`: MSA data (Charge Code Index, Geo Location MSA, Wage Index Location MSA, Standard Amount Location MSA).
            *   `P-NEW-SOL-COM-DEP-HOSP-YR`: Filler.
            *   `P-NEW-LUGAR`, `P-NEW-TEMP-RELIEF-IND`, `P-NEW-FED-PPS-BLEND-IND`: Fillers/Indicators.
        *   `PROV-NEWREC-HOLD2`:
            *   `P-NEW-VARIABLES`: Facility specific rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date.
            *   `P-NEW-SPECIAL-PAY-IND`: Special Pay Indicator.
            *   `FILLER`: Filler.
            *   `P-NEW-GEO-LOC-CBSAX`: CBSA location data (5 chars).
            *   `FILLER`: Filler.
            *   `P-NEW-SPECIAL-WAGE-INDEX`: Special Wage Index.
        *   `PROV-NEWREC-HOLD3`:
            *   `P-NEW-PASS-AMT-DATA`: Pass amount data (Capital, Direct Medical Education, Organ Acquisition, Plus Misc).
            *   `P-NEW-CAPI-DATA`: Capital payment data (PPS Pay Code, Hospital Specific Rate, Old Harm Rate, New Harm Ratio, Cost-to-Charge Ratio, Exceptions).
            *   `FILLER`: Filler.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record.
        *   `05 W-CBSA-IPPS`: CBSA code (3+2 chars).
        *   `05 W-CBSA-IPPS-SIZE`: Size indicator ('L', 'O', 'R').
        *   `05 W-CBSA-IPPS-EFF-DATE`: Effective date.
        *   `05 FILLER`: Filler.
        *   `05 W-IPPS-WAGE-INDEX`: IPPS Wage Index.
        *   `05 W-IPPS-PR-WAGE-INDEX`: PR IPPS Wage Index.

---

### Program: LTDRG100

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   No files explicitly accessed. Data is defined directly.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: LTDRG110

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   No files explicitly accessed. Data is defined directly.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: LTDRG123

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   No files explicitly accessed. Data is defined directly.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG080

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:**
    *   None. This program defines a table in WORKING-STORAGE.

*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds the DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date ('20071001').
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
        *   The `FILLER` fields in `D-TAB` contain long strings of alphanumeric data, likely encoded DRG data.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG090

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:**
    *   None.

*   **Working-Storage Section:**
    *   Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.

*   **Linkage Section:**
    *   None.

---

### Program: IRFBN091

This program defines tables for message areas and RFBN data within WORKING-STORAGE.

*   **Files Accessed:**
    *   None.

*   **Working-Storage Section:**
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message Area for Adding Provider.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message Area for Changing Provider.
    *   `01 MES-PPS-STATE PIC X(02)`: PPS State Code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Introductory Message Area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total Payment Amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record.
        *   `05 MES-SSRFBN-STATE PIC 99`: State Code.
        *   `05 FILLER PIC XX`: Filler.
        *   `05 MES-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
        *   `05 FILLER PIC XX`: Filler.
        *   `05 MES-SSRFBN-CODE2 PIC 99`: Unspecified code.
        *   `05 FILLER PIC X`: Filler.
        *   `05 MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `05 MES-SSRFBN-REST PIC X(22)`: Unspecified data.
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Unspecified code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Unspecified data.

*   **Linkage Section:**
    *   None.

---

### Program: LTCAL043

This program uses `COPY LTDRG041`, implying access to DRG table data.

*   **Files Accessed:**
    *   No files explicitly defined in `FILE-CONTROL`. Uses `COPY LTDRG041` for DRG table data.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 46-character comment string.
    *   `CAL-VERSION`: Program version ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (510 occurrences) with DRG code (`WWM-DRG`), relative weight (`WWM-RELWT`), and average length of stay (`WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payment amounts).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to/from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results (Return Code, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts).
    *   `PRICER-OPT-VERS-SW`: Pricing tables and versions used.
        *   `PRICER-OPTION-SW`: Indicates if all tables passed.
        *   `PPS-VERSIONS`: Contains version numbers (`PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, provider number, dates, waiver code, other codes, provider variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, Effective Date, Wage index values).

---

### Program: LTCAL058

This program uses `COPY LTDRG041`, implying access to DRG table data.

*   **Files Accessed:**
    *   No files explicitly defined. Uses `COPY LTDRG041` for DRG table data.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.8').
    *   `PROGRAM-CONSTANTS`: Holds federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table structure (same as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (same as in LTCAL043).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

---

### Program: LTCAL059

This program uses `COPY LTDRG057`, implying access to DRG table data.

*   **Files Accessed:**
    *   Uses `COPY LTDRG057` for DRG table data.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (512 occurrences) with DRG code (`WWM-DRG`), relative weight (`WWM-RELWT`), and average length of stay (`WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (same as in LTCAL043 and LTCAL058).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in LTCAL043 and LTCAL058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in LTCAL043 and LTCAL058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in LTCAL043 and LTCAL058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in LTCAL043 and LTCAL058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in LTCAL043 and LTCAL058).

---

### Program: LTCAL063

This program uses `COPY LTDRG057`, implying access to DRG table data.

*   **Files Accessed:**
    *   Uses `COPY LTDRG057` for DRG table data.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure (same as in LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: A 5-character field for CBSA code.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

---

### Program: LTDRG041

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   None. This is a data definition file.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: LTDRG057

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   None. This is a data definition file.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG063

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:**
    *   None explicitly defined in the provided code.

*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds the raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG071

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:**
    *   None explicitly defined.

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

*   **Linkage Section:**
    *   None.

---

### Program: LTCAL064

This program uses `COPY LTDRG062`, implying use of data from that copybook.

*   **Files Accessed:**
    *   None explicitly defined. Uses `COPY LTDRG062`, suggesting data from `LTDRG062` copybook.

*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes `LTDRG062` copybook containing DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `01 PROV-NEW-HOLD`: Structure for provider data (NPI, provider number, effective dates, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure for wage index data.

*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from a calling program (provider info, DRG code, LOS, discharge date, charges).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program (return codes, payment amounts).
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program (same as in Working-Storage).

---

### Program: LTCAL072

This program uses `COPY LTDRG062` and `COPY IPDRG063`.

*   **Files Accessed:**
    *   None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.

*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `01 HOLD-PPS-COMPONENTS`: Intermediate calculation results, expanded for short-stay outlier calculations.
    *   Variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data for LTCH.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data for IPPS.

*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data (same as in Working-Storage).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data (same as in Working-Storage).

---

### Programs: LTCAL075 and LTCAL080

These programs are expected to have similar structures to LTCAL072, with incremental changes in constants, rates, and potentially additional variables for newer versions.

*   **Files Accessed:**
    *   Likely similar to LTCAL072, using LTCH and IPPS DRG copybooks.

*   **Working-Storage Section:**
    *   Consistent basic structure, but with updated `CAL-VERSION` and specific constants/rates for the respective years.

*   **Linkage Section:**
    *   Consistent structure, mirroring LTCAL072, with potential minor field additions for new functionalities.

---

### Program: LTDRG062

This copybook defines a DRG table.

*   **Files Accessed:**
    *   None explicitly defined.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for the data.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.

*   **Linkage Section:**
    *   None.

---

### Programs: LTDRG075 and LTDRG080

These copybooks define DRG tables with updated data.

*   **Files Accessed:**
    *   None explicitly defined.

*   **Working-Storage Section:**
    *   Similar structure to LTDRG062, but with updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also vary.

*   **Linkage Section:**
    *   None.

---

### Program: LTCAL042

This program shares a similar structure and performs similar calculations to LTCAL032 but with updated version numbers and hardcoded values.

*   **Files Accessed:**
    *   Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.

*   **Working-Storage Section:**
    *   Almost identical to LTCAL032, with key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` has a different value (35726.18 vs 34956.15).
        *   `H-FIXED-LOSS-AMT` has a different value (19590 vs 24450).
        *   `PPS-BDGT-NEUT-RATE` has a different value (0.940 vs 0.934).
        *   Adds `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.

*   **Linkage Section:**
    *   Identical to LTCAL032.

---

### Program: LTDRG031

This copybook defines data structures for a DRG table, likely used by other programs.

*   **Files Accessed:**
    *   This is a copybook; it doesn't directly access files. It defines data structures used by other programs (LTCAL032, LTCAL042).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: A series of literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`).
        *   `WWM-ENTRY`: Table of DRG codes, relative weights, and average lengths of stay.

*   **Linkage Section:**
    *   None. Copybooks do not have linkage sections.

---

### Program: LTCAL032

This program performs PPS calculations and uses the DRG table from `LTDRG031`.

*   **Files Accessed:**
    *   None explicitly defined in `FILE-CONTROL`. Uses `COPY LTDRG031` for DRG table data.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string for working storage identification.
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, weights, average LOS).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay, Social Security Cost, Labor/Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version information and pricing option switches (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, various dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, three wage index values).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Structured into `PPS-DATA` and `PPS-OTHER-DATA`.

---

### Program: LTCAL043 (Detailed Data Structures)

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD` structure details:
        *   `PROV-NEWREC-HOLD1`: `P-NEW-NPI10` (NPI), `P-NEW-PROVIDER-NO` (Provider Number), `P-NEW-DATE-DATA` (dates), `P-NEW-WAIVER-CODE`, `P-NEW-INTER-NO`, `P-NEW-PROVIDER-TYPE`, `P-NEW-CURRENT-CENSUS-DIV`, `P-NEW-MSA-DATA` (MSA info), `P-NEW-SOL-COM-DEP-HOSP-YR`, `P-NEW-LUGAR`, `P-NEW-TEMP-RELIEF-IND`, `P-NEW-FED-PPS-BLEND-IND`.
        *   `PROV-NEWREC-HOLD2`: `P-NEW-VARIABLES` (rates, ratios, bed size, CMI, etc.), `P-NEW-SPECIAL-PAY-IND`, `FILLER`, `P-NEW-GEO-LOC-CBSAX` (CBSA location), `FILLER`, `P-NEW-SPECIAL-WAGE-INDEX`.
        *   `PROV-NEWREC-HOLD3`: `P-NEW-PASS-AMT-DATA` (payment amounts), `P-NEW-CAPI-DATA` (capital payment data), `FILLER`.
    *   `WAGE-NEW-INDEX-RECORD` details:
        *   `W-MSA`: MSA code (4 chars).
        *   `W-EFF-DATE`: Effective date (8 chars).
        *   `W-WAGE-INDEX1`, `W-WAGE-INDEX2`: Wage index values (S9(02)V9(04)).

---

### Program: LTCAL059 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG057` copybook details:
        *   `WWM-ENTRY` (512 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTCAL063 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PPS-CBSA`: A 5-character field for CBSA code.

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD`: Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Uses CBSA instead of MSA for wage index data.

---

### Program: LTCAL043 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG041` copybook details:
        *   `WWM-ENTRY` (510 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTCAL058 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG041` copybook details:
        *   `WWM-ENTRY` (510 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTCAL059 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG057` copybook details:
        *   `WWM-ENTRY` (512 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTCAL063 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG057` copybook details:
        *   `WWM-ENTRY` (512 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTDRG041 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (510 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTDRG057 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (512 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: IPDRG080 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `D-TAB` contains `FILLER PIC X(56)` repeated multiple times, representing encoded DRG data.
    *   `DRG-DATA` (1000 occurrences):
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG Weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average Length of Stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days Trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic ALoS.

---

### Program: IRFBN091 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `WK-SSRFBN-DATA` contains `FILLER PIC X(57)` repeated lines.
    *   `WK-SSRFBN-REASON-ALL` details:
        *   `WK-SSRFBN-STATE` (PIC 99): State Code.
        *   `WK-SSRFBN-RATE` (PIC 9(1)V9(5)): State Specific Rate.
        *   `WK-SSRFBN-STNAM` (PIC X(20)): State Name.

---

### Program: LTCAL042 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `H-LOS-RATIO` (PIC 9(01)V9(05)) added to `HOLD-PPS-COMPONENTS`.

---

### Program: LTCAL032 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure details:
        *   `PROV-NEWREC-HOLD1`: `P-NEW-NPI10`, `P-NEW-PROVIDER-NO`, `P-NEW-DATE-DATA`, `P-NEW-WAIVER-CODE`, `P-NEW-INTER-NO`, `P-NEW-PROVIDER-TYPE`, `P-NEW-CURRENT-CENSUS-DIV`, `P-NEW-MSA-DATA`, etc.
        *   `PROV-NEWREC-HOLD2`: `P-NEW-VARIABLES` (rates, ratios, etc.), `P-NEW-SPECIAL-PAY-IND`, `P-NEW-GEO-LOC-CBSAX`, `P-NEW-SPECIAL-WAGE-INDEX`.
        *   `PROV-NEWREC-HOLD3`: `P-NEW-PASS-AMT-DATA`, `P-NEW-CAPI-DATA`.
    *   `WAGE-NEW-INDEX-RECORD` details:
        *   `W-MSA` (PIC X(5)).
        *   `W-EFF-DATE` (PIC X(8)).
        *   `W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3` (S9(02)V9(04)).

*   **Linkage Section (continued):**
    *   `BILL-NEW-DATA` details: `B-NPI10`, `B-PROVIDER-NO`, `B-PATIENT-STATUS`, `B-DRG-CODE`, `B-LOS`, `B-COV-DAYS`, `B-LTR-DAYS`, `B-DISCHARGE-DATE`, `B-COV-CHARGES`, `B-SPEC-PAY-IND`.
    *   `PPS-DATA-ALL` details: `PPS-RTC`, `PPS-CHRG-THRESHOLD`, `PPS-CBSA`, `PPS-WAGE-INDEX`, `PPS-AVG-LOS`, `PPS-REL-WT`, `PPS-OUTLIER-PAY-AMT`, `PPS-LOS`, `PPS-DRG-ADJ-PAY-AMT`, `PPS-FED-PAY-AMT`, `PPS-FINAL-PAY-AMT`, `PPS-FACILITY-COSTS`, `PPS-NEW-FAC-SPEC-RATE`, `PPS-OUTLIER-THRESHOLD`, `PPS-SUBMITTED-DRG-CODE`, `PPS-CALC-VERSION-CODE`, `PPS-REG-DAYS-USED`, `PPS-LTR-DAYS-USED`, `PPS-BLEND-YEAR`, `PPS-COLA`.

---

### Program: LTCAL032 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `HOLD-PPS-COMPONENTS` includes: `H-LOS`, `H-REG-DAYS`, `H-TOTAL-DAYS`, `H-SSOT`, `H-BLEND-RTC`, `H-BLEND-FAC-RATE`, `H-BLEND-PPS-RATE`, `H-SOC-SEC-PAY`, `H-SOC-SEC-COST`, `H-LABOR-PORTION`, `H-NONLABOR-PORTION`, `H-FIXED-LOSS-AMT`, `H-NEW-FAC-SPEC-RATE`.
    *   `PROV-NEW-HOLD` details:
        *   `PROV-NEWREC-HOLD1`: `P-NEW-NPI10`, `P-NEW-PROVIDER-NO`, `P-NEW-DATE-DATA`, `P-NEW-WAIVER-CODE`, `P-NEW-INTER-NO`, `P-NEW-PROVIDER-TYPE`, `P-NEW-CURRENT-CENSUS-DIV`, `P-NEW-MSA-DATA`, etc.
        *   `PROV-NEWREC-HOLD2`: `P-NEW-VARIABLES` (rates, ratios, etc.), `P-NEW-SPECIAL-PAY-IND`, `P-NEW-GEO-LOC-CBSAX`, `P-NEW-SPECIAL-WAGE-INDEX`.
        *   `PROV-NEWREC-HOLD3`: `P-NEW-PASS-AMT-DATA`, `P-NEW-CAPI-DATA`.
    *   `WAGE-NEW-INDEX-RECORD` details:
        *   `W-MSA` (PIC X(5)).
        *   `W-EFF-DATE` (PIC X(8)).
        *   `W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3` (S9(02)V9(04)).

*   **Linkage Section (continued):**
    *   `BILL-NEW-DATA` details: `B-NPI10`, `B-PROVIDER-NO`, `B-PATIENT-STATUS`, `B-DRG-CODE`, `B-LOS`, `B-COV-DAYS`, `B-LTR-DAYS`, `B-DISCHARGE-DATE`, `B-COV-CHARGES`, `B-SPEC-PAY-IND`.
    *   `PPS-DATA-ALL` details: `PPS-RTC`, `PPS-CHRG-THRESHOLD`, `PPS-CBSA`, `PPS-WAGE-INDEX`, `PPS-AVG-LOS`, `PPS-REL-WT`, `PPS-OUTLIER-PAY-AMT`, `PPS-LOS`, `PPS-DRG-ADJ-PAY-AMT`, `PPS-FED-PAY-AMT`, `PPS-FINAL-PAY-AMT`, `PPS-FACILITY-COSTS`, `PPS-NEW-FAC-SPEC-RATE`, `PPS-OUTLIER-THRESHOLD`, `PPS-SUBMITTED-DRG-CODE`, `PPS-CALC-VERSION-CODE`, `PPS-REG-DAYS-USED`, `PPS-LTR-DAYS-USED`, `PPS-BLEND-YEAR`, `PPS-COLA`.

---

### Program: LTDRG062 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (518 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTDRG075 and LTDRG080 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `LTDRG080` includes `WWM-IPTHRESH` (PIC 9(3)V9(1)).

---

### Program: LTDRG080

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   None. This is a data definition file.

*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `05 WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.

*   **Linkage Section:**
    *   None.

---

### Program: LTDRG093

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   None.

*   **Working-Storage Section:**
    *   Similar structure to LTDRG080, but with different data.

*   **Linkage Section:**
    *   None.

---

### Program: LTDRG095

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:**
    *   None.

*   **Working-Storage Section:**
    *   Similar structure to LTDRG093, but with different data.

*   **Linkage Section:**
    *   None.

---

### Program: IPDRG104 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `DRG-DATA` OCCURS 1000:
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average length of stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.

---

### Program: IPDRG110 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `DRG-DATA` OCCURS 1000:
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average length of stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.

---

### Program: IPDRG123 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `DRG-DATA` OCCURS 1000:
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average length of stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.

---

### Program: IRFBN102 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `WK-SSRFBN-DATA` contains `FILLER PIC X(57)` repeated lines.
    *   `WK-SSRFBN-REASON-ALL` details:
        *   `WK-SSRFBN-STATE` (PIC 99): State Code.
        *   `WK-SSRFBN-RATE` (PIC 9(1)V9(5)): State Specific Rate.
        *   `WK-SSRFBN-STNAM` (PIC X(20)): State Name.

---

### Program: IRFBN105 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `WK-SSRFBN-DATA` contains `FILLER PIC X(57)` repeated lines.
    *   `WK-SSRFBN-REASON-ALL` details:
        *   `WK-SSRFBN-STATE` (PIC 99): State Code.
        *   `WK-SSRFBN-RATE` (PIC 9(1)V9(5)): State Specific Rate.
        *   `WK-SSRFBN-STNAM` (PIC X(20)): State Name.

---

### Program: LTCAL103 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure details:
        *   `PROV-NEWREC-HOLD1`: `P-NEW-NPI10`, `P-NEW-PROVIDER-NO`, `P-NEW-DATE-DATA`, `P-NEW-WAIVER-CODE`, `P-NEW-INTER-NO`, `P-NEW-PROVIDER-TYPE`, `P-NEW-CURRENT-CENSUS-DIV`, `P-NEW-MSA-DATA`, etc.
        *   `PROV-NEWREC-HOLD2`: `P-NEW-VARIABLES` (rates, ratios, etc.), `P-NEW-SPECIAL-PAY-IND`, `P-NEW-GEO-LOC-CBSAX`, `P-NEW-SPECIAL-WAGE-INDEX`.
        *   `PROV-NEWREC-HOLD3`: `P-NEW-PASS-AMT-DATA`, `P-NEW-CAPI-DATA`.
    *   `WAGE-NEW-IPPS-INDEX-RECORD` details:
        *   `W-CBSA-IPPS` (3+2 chars).
        *   `W-CBSA-IPPS-SIZE` (PIC X).
        *   `W-CBSA-IPPS-EFF-DATE` (PIC X(8)).
        *   `W-IPPS-WAGE-INDEX` (S9(02)V9(04)).
        *   `W-IPPS-PR-WAGE-INDEX` (S9(02)V9(04)).

---

### Program: LTCAL105 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure details are the same as LTCAL103.

---

### Program: LTCAL111 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure details are the same as LTCAL103.

---

### Program: LTCAL123 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure details are the same as LTCAL103.

---

### Program: LTCAL043 (Detailed Data Structures)

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD` structure details:
        *   `PROV-NEWREC-HOLD1`: `P-NEW-NPI10`, `P-NEW-PROVIDER-NO`, `P-NEW-DATE-DATA`, `P-NEW-WAIVER-CODE`, `P-NEW-INTER-NO`, `P-NEW-PROVIDER-TYPE`, `P-NEW-CURRENT-CENSUS-DIV`, `P-NEW-MSA-DATA`.
        *   `PROV-NEWREC-HOLD2`: `P-NEW-VARIABLES`, `P-NEW-SPECIAL-PAY-IND`, `P-NEW-GEO-LOC-CBSAX`, `P-NEW-SPECIAL-WAGE-INDEX`.
        *   `PROV-NEWREC-HOLD3`: `P-NEW-PASS-AMT-DATA`, `P-NEW-CAPI-DATA`.
    *   `WAGE-NEW-INDEX-RECORD` details:
        *   `W-MSA` (PIC X(4)).
        *   `W-EFF-DATE` (PIC X(8)).
        *   `W-WAGE-INDEX1`, `W-WAGE-INDEX2` (S9(02)V9(04)).

---

### Program: LTCAL058 (Detailed Data Structures)

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD` structure details are the same as LTCAL043.
    *   `WAGE-NEW-INDEX-RECORD` structure details are the same as LTCAL043.

---

### Program: LTCAL059 (Detailed Data Structures)

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD` structure details are the same as LTCAL043.
    *   `WAGE-NEW-INDEX-RECORD` structure details are the same as LTCAL043.

---

### Program: LTCAL063 (Detailed Data Structures)

*   **Linkage Section (continued):**
    *   `PROV-NEW-HOLD`: Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Uses CBSA instead of MSA for wage index data.

---

### Program: LTDRG041 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (510 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: LTDRG057 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (512 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.

---

### Program: IPDRG063 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `D-TAB` contains `FILLER PIC X(56)` repeated.
    *   `DRG-DATA` (560 occurrences):
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average length of stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.

---

### Program: IPDRG071 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `D-TAB` contains `FILLER PIC X(56)` repeated.
    *   `DRG-DATA` (580 occurrences):
        *   `DRG-WT` (PIC 9(02)V9(04)): DRG weight.
        *   `DRG-ALOS` (PIC 9(02)V9(01)): Average length of stay.
        *   `DRG-DAYS-TRIM` (PIC 9(02)): Days trimmed.
        *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.

---

### Program: LTCAL064 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `PROV-NEW-HOLD` structure includes NPI, provider number, dates, waiver code, etc.
    *   `WAGE-NEW-INDEX-RECORD` includes MSA, Effective Date, and wage index values.

---

### Program: LTCAL072 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `HOLD-PPS-COMPONENTS` expanded for short-stay outlier calculations.
    *   `PROV-NEW-HOLD` structure includes NPI, provider number, dates, waiver code, etc.
    *   `WAGE-NEW-INDEX-RECORD` includes MSA, Effective Date, and wage index values.
    *   `WAGE-NEW-IPPS-INDEX-RECORD` includes IPPS wage index data.

*   **Linkage Section (continued):**
    *   `BILL-NEW-DATA` updated to numeric `DRG-CODE`.

---

### Program: LTDRG080 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   `W-DRG-FILLS` contains packed data.
    *   `W-DRG-TABLE` redefines `W-DRG-FILLS`.
        *   `WWM-ENTRY` (530 occurrences):
            *   `WWM-DRG` (PIC X(3)): DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.

---

### Program: LTDRG093 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   Similar structure to LTDRG080, but with different data.

---

### Program: LTDRG095 (Detailed Data Structures)

*   **Working-Storage Section (continued):**
    *   Similar structure to LTDRG093, but with different data.

---

### Overall Program Flow Summary:

1.  **LTMGR212:** Reads billing records from `BILLFILE`, prepares data, calls `LTOPN212` for payment calculations, and writes formatted results to `PRTOPER`.
2.  **LTOPN212:** Loads provider and wage index tables from various files. Determines table usage based on discharge date and pricer option, then calls `LTDRV212` for payment calculations.
3.  **LTDRV212:** Selects the appropriate wage index based on discharge date and provider information. Calls the correct `LTCAL` module (not shown) for payment calculations, with the choice dependent on the bill's fiscal year.

The extensive comments suggest a long history of updates and modifications. The programs are designed to handle the complexities of long-term care prospective payment systems.

**Important Note:** The `COPY` statements in many programs indicate reliance on external data definitions and potentially other COBOL programs. Without the contents of those copied files, the analysis is based on context. The absence of `FILE SECTION` entries means file I/O details are not in these excerpts. The long strings of numeric data in some `IPDRG` programs and `W-DRG-FILLS` fields in `LTDRG` programs likely represent encoded or packed DRG table data requiring unpacking for full understanding.