## Data Definition and File Handling

This document consolidates the data definition and file handling information extracted from multiple functional specification documents (L1, L2, L4, L5, L6, L7, L8). It details the files accessed, working-storage sections, and linkage sections for various COBOL programs involved in processing healthcare claims, likely related to Prospective Payment Systems (PPS).

---

### Program: LTMGR212 (from L1_FunctionalSpecification.md)

This program acts as a manager, reading billing records and calling other programs for payment calculations, then formatting the output.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format: `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for printing prospective payment reports. Record format: `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal (comment).
    *   `PPMGR-VERSION`: A 5-character field storing the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of the called program.
    *   `EOF-SW`: A 1-digit numeric field (end-of-file switch: 0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field counting lines written to `PRTOPER`, initialized to 65.
    *   `UT1-STAT`: A 2-character field for `BILLFILE` status (`UT1-STAT1`, `UT1-STAT2`).
    *   `OPR-STAT`: A 2-character field for `PRTOPER` status (`OPR-STAT1`, `OPR-STAT2`).
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (provider NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis/procedure code tables).
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212` (payment calculation results, wage indices).
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure holding payment amounts from `LTOPN212` (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, likely for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Single character indicating pricing option.
        *   `PPS-VERSIONS`: Structure containing version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (arrays) for CBSA/MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

---

### Program: LTOPN212 (from L1_FunctionalSpecification.md)

This program loads tables and performs initial payment calculations, calling another program for detailed processing.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout: `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout: `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout: `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout: `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `OPN-VERSION`: A 5-character field storing the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of the called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field (tables loaded: 0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field (end-of-file switch).
    *   `W-PROV-NEW-HOLD`: Structure to hold provider records from `PROV-FILE` or passed in, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status of input files.
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data (up to 10000 entries), indexed by `CU1`, `CU2`.
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data (up to 10000 entries), indexed by `MA1`, `MA2`, `MA3`.
    *   `MSA-WI-TABLE`: Table for MSA wage index data (up to 4000 entries), indexed by `MU1`, `MU2`.
    *   `WORK-COUNTERS`: Structure with counters for records read from each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) to hold provider data from `PROV-FILE`, divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`, indexed by `PX1`, `PD2`, `PD3`.
    *   `PROV-NEW-HOLD`: Structure to hold provider record passed to `LTDRV212`, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirroring `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTMGR212`, mirroring `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: 5-character CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTMGR212`, mirroring `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Pricer option/version information passed from `LTMGR212`, mirroring `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Provider-specific information passed from `LTMGR212`, mirroring `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, for wage index tables.

---

### Program: LTDRV212 (from L1_FunctionalSpecification.md)

This program performs the core logic of wage index selection and calls specific calculation modules.

*   **Files Accessed:** LTDRV212 does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `DRV-VERSION`: A 5-character field storing the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of called programs (likely `LTCAL` module versions).
    *   `WS-9S`: An 8-character numeric literal with all 9s, used for date comparisons.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields holding wage index related constants for FY2020.
    *   `RUFL-ADJ-TABLE`: Table (defined in COPY `RUFL200`) containing rural floor adjustment factors for various CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: An index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold fiscal year begin/end dates calculated from the bill's discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from tables in LTOPN212.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field to hold the Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field to hold the supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding the provider record passed from `LTOPN212`, mirroring `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure to hold billing data for older fiscal years (pre-Jan 2015).
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015 and later, mirroring `BILL-NEW-DATA` in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option/version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

---

### COPY Member: RUFL200 (from L1_FunctionalSpecification.md)

This is a COPY member, not an executable program, defining data structures.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: The main structure. Contains a table `RUFL-TAB` of rural floor adjustment factors. Each entry includes:
        *   `RUFL-CBSA`: CBSA code.
        *   `RUFL-EFF-DATE`: Effective date.
        *   `RUFL-WI3`: Wage index.
    *   The table has 459 entries.

---

### Program: IPDRG160 (from L2_FunctionalSpecification.md)

This program likely accesses a DRG table file for a specific year.

*   **Files Accessed:** Likely accesses a DRG table file, read-only. No file names explicitly mentioned.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item containing DRG table data.
        *   `WK-DRG-DATA`: Group item holding DRG data in a literal, record-like format.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Redefined structure for table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Single DRG record structure.
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code.
                    *   `FILLER1` (PIC X(01)): Filler.
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)): Filler.
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean average length of stay.
                    *   `FILLER3` (PIC X(05)): Filler.
                    *   `DRG-LOW` (PIC X(01)): Indicator ('Y'/'N').
                    *   `FILLER5` (PIC X(01)): Filler.
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic average length of stay.
                    *   `FILLER6` (PIC X(02)): Filler.
                    *   `DRG-PAC` (PIC X(01)): Post-acute care indicator.
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Special post-acute care indicator.
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.
*   **Linkage Section:** Not present.

---

### Program: IPDRG170 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for the year 2016.

*   **Files Accessed:** Likely accesses a DRG table file, read-only, for 2016.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`.
*   **Linkage Section:** Not present.

---

### Program: IPDRG181 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for the year 2017.

*   **Files Accessed:** Likely accesses a DRG table file, read-only, for 2017.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20171001' and `DRG-TAB` having `OCCURS 754`.
*   **Linkage Section:** Not present.

---

### Program: IPDRG190 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for the year 2018.

*   **Files Accessed:** Likely accesses a DRG table file, read-only, for 2018.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20181001' and `DRG-TAB` having `OCCURS 761`.
*   **Linkage Section:** Not present.

---

### Program: IPDRG200 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for the year 2019.

*   **Files Accessed:** Likely accesses a DRG table file, read-only, for 2019.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20191001' and `DRG-TAB` having `OCCURS 761`.
*   **Linkage Section:** Not present.

---

### Program: IPDRG211 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for the year 2020.

*   **Files Accessed:** Likely accesses a DRG table file, read-only, for 2020.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20201001' and `DRG-TAB` having `OCCURS 767`.
*   **Linkage Section:** Not present.

---

### Program: LTCAL162 (from L2_FunctionalSpecification.md)

This program performs payment calculations using DRG and wage index data.

*   **Files Accessed:** Likely accesses:
    *   Provider-specific file (PSF) with wage indices, cost-to-charge ratios, etc.
    *   CBSA wage index file.
    *   LTCH DRG table (`LTDRG160`) and IPPS DRG table (`IPDRG160`) via COPY statements. These are read-only.
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
    *   `PRICER-OPT-VERS-SW`: Switches indicating pricer option and driver program versions.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

### Program: LTCAL170 (from L2_FunctionalSpecification.md)

Similar to LTCAL162, but for FY17.

*   **Files Accessed:** Similar to LTCAL162, likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG170`, `IPDRG170`).
*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.
*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

### Program: LTCAL183 (from L2_FunctionalSpecification.md)

Similar to LTCAL170, but for FY18.

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG181`, `IPDRG181`).
*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Some variables related to Subclause II removed.
*   **Linkage Section:** Similar to LTCAL170, with removal of Subclause II fields.

---

### Program: LTCAL190 (from L2_FunctionalSpecification.md)

Similar to LTCAL183, but for FY19.

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and DRG tables (`LTDRG190`, `IPDRG190`).
*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **Linkage Section:** Similar to LTCAL183.

---

### Program: LTCAL202 (from L2_FunctionalSpecification.md)

Similar to LTCAL190, but for FY20, including COVID-19 processing.

*   **Files Accessed:** Similar to previous LTCAL programs, accesses PSF, CBSA wage index file, and DRG tables (`LTDRG200`, `IPDRG200`).
*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` for Disproportionate Patient Percentage (DPP) adjustment.

---

### Program: LTCAL212 (from L2_FunctionalSpecification.md)

Similar to LTCAL202, but for FY21.

*   **Files Accessed:** Similar to LTCAL202, accesses PSF, CBSA wage index file, and DRG tables (`LTDRG210`, `IPDRG211`).
*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Adds `P-SUPP-WI-IND` and `P-SUPP-WI` in `PROV-NEW-HOLD`.
*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

---

### COPY Member: LTDRG160 (from L2_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for FY15.

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

---

### COPY Member: LTDRG170 (from L2_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for FY16.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG181 (from L2_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for FY18.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG190 (from L2_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for FY19.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG210 (from L2_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for FY21.

*   **Files Accessed:** Not applicable (COPY member).
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** Not applicable.

---

### Program: IPDRG104 (from L4_FunctionalSpecification.md)

This program defines a DRG table, likely for a specific year.

*   **Files Accessed:** Uses `COPY IPDRG104`, implying inclusion from another file containing a DRG table.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

### Program: IPDRG110 (from L4_FunctionalSpecification.md)

Similar to IPDRG104, but for a different year/dataset.

*   **Files Accessed:** Uses `COPY IPDRG110`, referencing a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`, with `DRG-DATA OCCURS 1000`.
*   **Linkage Section:** None.

---

### Program: IPDRG123 (from L4_FunctionalSpecification.md)

Similar to IPDRG104, but for a different year/dataset.

*   **Files Accessed:** Uses `COPY IPDRG123`, indicating inclusion of DRG data from another file.
*   **Working-Storage Section:** Structurally similar to `IPDRG104`, with `DRG-DATA OCCURS 1000`.
*   **Linkage Section:** None.

---

### Program: IRFBN102 (from L4_FunctionalSpecification.md)

This program deals with state-specific Rural Floor Budget Neutrality Factors (RFBNS).

*   **Files Accessed:** Uses `COPY IRFBN102`, suggesting data from a file containing state-specific RFBNS.
*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for table access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details per state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Another code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`, `MES-TOT-PAY`: Message and holding fields.
    *   `MES-SSRFBN`: Holds a single RFBN record, structured like `WK-SSRFBN-REASON-ALL`.
*   **Linkage Section:** None.

---

### Program: IRFBN105 (from L4_FunctionalSpecification.md)

Similar to IRFBN102, likely for updated RFBN data.

*   **Files Accessed:** Uses `COPY IRFBN105`, referencing a file with updated RFBN data.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** None.

---

### Program: LTCAL103 (from L4_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG and RFBN data.

*   **Files Accessed:** Includes data via `COPY` statements from:
    *   `LTDRG100`: Likely contains a LTC DRG table.
    *   `IPDRG104`: Contains IPPS DRG data.
    *   `IRFBN102`: Contains IPPS state-specific RFBNs.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive comment.
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for PPS. Contains numerous numeric variables for LOS, days, rates, shares, adjustments, etc.
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (return code, charge threshold, numerous other data elements).
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `PRICER-OPTION-SW`: 'A' for all tables passed, 'P' for provider record passed.
        *   `PPS-VERSIONS`: Contains `PPDRV-VERSION`.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, type, MSA data, various rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size indicator, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in a packed format (redefined below).
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from the calling program (NPI, provider number, patient status, DRG, LOS, covered days, LTR days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105 (from L4_FunctionalSpecification.md)

Similar to LTCAL103, but uses `IRFBN105` and updated constants.

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG100`, `IPDRG104`, and `IRFBN105`.
*   **Working-Storage Section:** Very similar to `LTCAL103`, main differences are `CAL-VERSION` ('V10.5') and use of `IRFBN105`.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL111 (from L4_FunctionalSpecification.md)

Similar to LTCAL103, but uses `LTDRG110` and `IPDRG110`, and does not include RFBNs.

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG110`, `IPDRG110`. `IRFBN***` is commented out.
*   **Working-Storage Section:** Similar to `LTCAL103`, updated to version `V11.1`, adjusted copybooks, and absence of RFBN table.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL123 (from L4_FunctionalSpecification.md)

Similar to LTCAL111, but uses `LTDRG123` and `IPDRG123`.

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG123`, `IPDRG123`. RFBN copybook is commented out.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3`, relevant copybooks adjusted. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTDRG100 (from L4_FunctionalSpecification.md)

This copybook defines the LTC DRG table data.

*   **Files Accessed:** None directly. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTDRG110 (from L4_FunctionalSpecification.md)

This copybook defines the LTC DRG table data for a different year.

*   **Files Accessed:** None directly. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTDRG123 (from L4_FunctionalSpecification.md)

This copybook defines the LTC DRG table data for yet another year.

*   **Files Accessed:** None directly. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: IPDRG080 (from L5_FunctionalSpecification.md)

This program defines a DRG table for the year 2007.

*   **Files Accessed:** None. Defines a table in WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds the DRG data as packed strings.
            *   `10 FILLER PIC X(08) VALUE '20071001'`: Effective date.
            *   `10 FILLER PIC X(56) VALUE ...`: Repeated lines of DRG data.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for table access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective Date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

---

### Program: IPDRG090 (from L5_FunctionalSpecification.md)

This program defines a DRG table for the year 2008.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, but with `DRGX-EFF-DATE` as '20081001' and different DRG data.
*   **Linkage Section:** None.

---

### Program: IRFBN091 (from L5_FunctionalSpecification.md)

This program defines message areas and a table for State Specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `MES-ADD-PROV`, `MES-CHG-PROV`, `MES-PPS-STATE`, `MES-INTRO`, `MES-TOT-PAY`: Message and holding fields.
    *   `MES-SSRFBN`: Holds a single RFBN record.
        *   `MES-SSRFBN-STATE PIC 99`: State Code.
        *   `FILLER PIC XX`.
        *   `MES-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
        *   `FILLER PIC XX`.
        *   `MES-SSRFBN-CODE2 PIC 99`.
        *   `FILLER PIC X`.
        *   `MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `MES-SSRFBN-REST PIC X(22)`.
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for table access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state (State Code, Filler, Rate, Filler, Code2, Filler, State Name, Remaining data).
*   **Linkage Section:** None.

---

### Program: LTCAL087 (from L5_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG and RFBN data.

*   **Files Accessed:** None explicitly defined. Uses `COPY` statements for `LTDRG086` and `IPDRG080`, implying use of data from these sources.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates (`FED-FY-BEGIN-03` to `FED-FY-BEGIN-07`).
    *   (Includes substantial data structures from `LTDRG086` and `IPDRG080`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results (LOS, Regular Days, Total Days, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS data returned to calling program (Return Code, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version switch.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, provider number, dates, waiver code, type, MSA data, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (MSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, wage indices).

---

### Program: LTCAL091 (from L5_FunctionalSpecification.md)

Similar to LTCAL087, but for version 09.1.

*   **Files Accessed:** Similar to LTCAL087, uses `COPY` statements for `LTDRG086` and `IPDRG080`.
*   **Working-Storage Section:** Very similar to LTCAL087; main difference is `CAL-VERSION` ('V09.1'). Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL094 (from L5_FunctionalSpecification.md)

Similar to LTCAL091, but for version 09.4, with additional fields.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG093`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL091; `CAL-VERSION` is 'V09.4'. Copied data structures reflect year's changes. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL095 (from L5_FunctionalSpecification.md)

Similar to LTCAL094, but for version 09.5.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG095`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTDRG080 (from L5_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

---

### Program: LTDRG086 (from L5_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for a different year.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of WWM-ENTRY.
*   **Linkage Section:** None.

---

### Program: LTDRG093 (from L5_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for a different year.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

---

### Program: LTDRG095 (from L5_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for a different year.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

---

### Program: IPDRG063 (from L6_FunctionalSpecification.md)

This program defines a DRG table for a specific year (likely 2006).

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Table containing DRG data.
        *   `05 D-TAB`: Holds the raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for table access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

### Program: IPDRG071 (from L6_FunctionalSpecification.md)

This program defines a DRG table for a specific year (likely 2007).

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

### Program: LTCAL064 (from L6_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG data.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, suggesting use of data from that copybook.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (containing `WWM-ENTRY` DRG table).
    *   `HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Various numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, payment amounts).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `PROV-NEW-HOLD`: Structure for provider data (NPI, provider number, dates, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: Structure for wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from a calling program (provider info, DRG code, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results returned to the calling program (return codes, payment amounts, etc.).
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

### Program: LTCAL072 (from L6_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG data and short-stay outlier logic.

*   **Files Accessed:** None explicitly defined. Uses `COPY` statements for `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `HOLD-PPS-COMPONENTS`: Intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data from calling program (updated to numeric DRG-CODE).
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PROV-NEW-HOLD`: Provider data.
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

### Programs: LTCAL075, LTCAL080 (from L6_FunctionalSpecification.md)

These programs perform PPS calculations, similar to LTCAL072, with incremental changes.

*   **Files Accessed:** Similar to LTCAL072, using copybooks for DRG data.
*   **Working-Storage Section:** Similar structure to LTCAL072. Differences lie in constants, rates, and potentially added variables reflecting evolving methodologies.
*   **Linkage Section:** Similar structure to LTCAL072.

---

### Program: LTDRG062 (from L6_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data.

*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains raw data for the LTCH DRG table as packed strings.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for table access.
        *   `WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Programs: LTDRG075, LTDRG080 (from L6_FunctionalSpecification.md)

These copybooks define LTCH DRG table data for different years.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG062, but with updated DRG codes, weights, ALOS, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.
*   **Linkage Section:** None.

---

### Program: LTCAL043 (from L7_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG data.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure:
        *   `WWM-ENTRY` (OCCURS 510): DRG data (DRG code, relative weight, average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payment amounts, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results structure (Return Code, threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and version structure.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, provider number, dates, waiver code, various provider variables).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, Effective Date, wage index values).

---

### Program: LTCAL058 (from L7_FunctionalSpecification.md)

Similar to LTCAL043, but for version 05.8.

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('V05.8').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table structure (same as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

---

### Program: LTCAL059 (from L7_FunctionalSpecification.md)

Similar to LTCAL058, but for version 05.9, using `LTDRG057`.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure:
        *   `WWM-ENTRY` (OCCURS 512): DRG data (DRG code, relative weight, average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in previous programs).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in previous programs).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in previous programs).

---

### Program: LTCAL063 (from L7_FunctionalSpecification.md)

Similar to LTCAL059, but for version 06.3, with CBSA-specific wage index.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure (same as in LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA`: 5-character CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure.
    *   `PPS-DATA-ALL`: PPS calculation results structure.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data (uses CBSA instead of MSA).

---

### Program: LTDRG041 (from L7_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTDRG057 (from L7_FunctionalSpecification.md)

This copybook defines the LTCH DRG table data for a different year.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing data.
        *   `WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `WWM-DRG PIC X(3)`: DRG code.
            *   `WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTCAL032 (from L8_FunctionalSpecification.md)

This program performs PPS calculations, incorporating DRG data.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031`, likely defining DRG table structures.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string for working storage identification.
    *   `CAL-VERSION`: Program version ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, weights, ALOS).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blend amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Version information and pricing option switches.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, waiver code, type, MSA data, rates, ratios, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, wage indices).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).

---

### Program: LTCAL042 (from L8_FunctionalSpecification.md)

Similar to LTCAL032, but for version 04.2, with updated constants and fields.

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   Almost identical to LTCAL032.
    *   Key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` has a different value (35726.18 vs 34956.15).
        *   `H-FIXED-LOSS-AMT` has a different value (19590 vs 24450).
        *   `PPS-BDGT-NEUT-RATE` has a different value (0.940 vs 0.934).
        *   Adds `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

---

### Program: LTDRG031 (from L8_FunctionalSpecification.md)

This copybook defines the DRG table data used by LTCAL032 and LTCAL042.

*   **Files Accessed:** This is a copybook; it doesn't directly access files but defines structures used to access DRG data.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Series of literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure as a table (`WWM-ENTRY`).
        *   `WWM-ENTRY` (OCCURS 737): DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

---

### Overall Program Flow and Observations:

The analyzed programs form a suite for processing healthcare claims, likely within a Prospective Payment System (PPS) framework. The core functionality appears to involve:

1.  **Data Input and Preparation:** Programs like `LTMGR212` read billing data from files.
2.  **Table Loading:** Programs like `LTOPN212` load various data tables, including provider information, CBSA/MSA wage indices, and DRG tables (often through `COPY` statements, implying these tables are managed externally).
3.  **Payment Calculation:** Programs like `LTCALxxx` perform complex payment calculations based on bill data, provider specifics, and various rate/index tables. Different `LTCAL` versions correspond to different fiscal years, reflecting evolving payment methodologies.
4.  **Driver/Manager Programs:** Programs like `LTDRV212` orchestrate the calls to calculation modules (`LTCALxxx`) based on fiscal year and other criteria. `LTMGR212` serves as a higher-level manager.
5.  **Data Structures:** Extensive use of group items, tables (`OCCURS`), and `REDEFINES` clauses is evident, typical of COBOL for handling structured data and table lookups.
6.  **Versioning:** The presence of multiple `IPDRGxxx`, `LTDRGxxx`, and `LTCALxxx` programs with incremental version numbers (e.g., 160, 170, 181, 190, 200, 211 for IPDRG; 031, 032, 041, 042, 043, 057, 058, 059, 062, 063, 064, 071, 072, 075, 080, 086, 087, 090, 091, 093, 094, 095, 100, 103, 104, 105, 110, 111, 123, 160, 162, 170, 181, 183, 190, 200, 202, 210, 211, 212 for others) indicates a long history of updates and maintenance to adapt to changes in payment rules and regulations.
7.  **Extensive Comments:** The presence of `W-STORAGE-REF` and other descriptive literals suggests a strong emphasis on code documentation, likely due to the program's age and complexity.

The detailed analysis of WORKING-STORAGE and LINKAGE SECTIONS reveals the data elements passed between programs and used internally for calculations, providing a clear picture of the data flow and transformations within the system. The analysis of `COPY` statements highlights the modularity and reliance on external data definitions.