## Data Definition and File Handling

This document consolidates and analyzes the "Data Definition and File Handling" sections extracted from multiple functional specification documents (L1 through L8). It provides a comprehensive overview of the COBOL programs, detailing the files they access (or are implied to access via COPY statements), their WORKING-STORAGE sections, and their LINKAGE SECTIONS.

The programs analyzed are primarily involved in calculating prospective payment system (PPS) rates, likely for healthcare claims, and involve intricate data structures for Diagnosis Related Groups (DRGs), wage indices, provider information, and various payment components.

---

### Program: LTMGR212

This program acts as a primary driver, processing billing records and orchestrating calls to other modules for payment calculations.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format is defined by `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format is defined by `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal, likely a comment.
    *   `PPMGR-VERSION`: A 5-character field for the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of a called program.
    *   `EOF-SW`: A 1-digit numeric field, an end-of-file switch (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field, counter for lines written to `PRTOPER`, initialized to 65.
    *   `UT1-STAT`, `UT1-STAT1`, `UT1-STAT2`: 2-character field for `BILLFILE` status and its components.
    *   `OPR-STAT`, `OPR-STAT1`, `OPR-STAT2`: 2-character field for `PRTOPER` status and its components.
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE`, including NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, and diagnosis/procedure code tables.
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212`, including payment calculation results, wage indices, and other relevant data.
    *   `PPS-CBSA`: A 5-character field for the Core Based Statistical Area (CBSA) code.
    *   `PPS-PAYMENT-DATA`: Structure holding calculated payment amounts from `LTOPN212`, including site-neutral cost, IPPS payments, standard full, and short stay payments.
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for passing pricer option and version information to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Single character indicating pricing option.
        *   `PPS-VERSIONS`: Structure containing the version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: A large structure for provider information passed to `LTOPN212`, including NPI, provider number, dates, codes, indices, and other provider-specific data.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) to hold CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** LTMGR212 does not have a Linkage Section.

---

### Program: LTOPN212

This program loads various tables and performs initial processing before calling a calculation module.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout defined as `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout defined as `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout defined as `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout defined as `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `OPN-VERSION`: A 5-character field for the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of a called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating if tables are loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field, an end-of-file switch.
    *   `W-PROV-NEW-HOLD`: Structure to hold provider records from `PROV-FILE` or passed in, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status of input files.
    *   `CBSA-WI-TABLE`: Table holding CBSA wage index data from `CBSAX-FILE` (up to 10000 entries).
    *   `IPPS-CBSA-WI-TABLE`: Table holding IPPS CBSA wage index data from `IPPS-CBSAX-FILE` (up to 10000 entries).
    *   `MSA-WI-TABLE`: Table holding MSA wage index data from `MSAX-FILE` (up to 4000 entries).
    *   `WORK-COUNTERS`: Structure containing record counters for each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) holding provider data from `PROV-FILE`, divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`.
    *   `PROV-NEW-HOLD`: Structure to hold provider records passed to `LTDRV212`, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirroring `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: Structure for PPS data passed to and returned from `LTMGR212`, mirroring `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: A 5-character field for the CBSA code, passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Structure for payment data passed to and returned from `LTMGR212`, mirroring `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed from `LTMGR212`, mirroring `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Structure containing provider-specific information passed from `LTMGR212`, mirroring `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, holding wage index tables.

---

### Program: LTDRV212

This module performs the core wage index selection and calls calculation modules.

*   **Files Accessed:** LTDRV212 does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `DRV-VERSION`: A 5-character field for the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of called programs (likely different `LTCAL` versions).
    *   `WS-9S`: An 8-character numeric literal with all 9s, for date comparisons.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table (defined in COPY RUFL200) containing rural floor adjustment factors for CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: An index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold fiscal year begin/end dates calculated from the bill's discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from tables in LTOPN212.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for the Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for the supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider records passed from `LTOPN212`, mirroring `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure holding billing data for older fiscal years (pre-Jan 2015).
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015 and later, mirroring `BILL-NEW-DATA` in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed to and returned from `LTOPN212`.
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed to and returned from `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

---

### COPY Member: RUFL200

This is a COPY member, not a program, defining data structures for rural floor adjustment factors.

*   **Files Accessed:** Not applicable, as it's a data definition.
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Contains a table `RUFL-TAB` with rural floor adjustment factors. Each entry includes `RUFL-CBSA` (CBSA code), `RUFL-EFF-DATE` (effective date), and `RUFL-WI3` (wage index). The table has 459 entries.

---

### Program: IPDRG160

This program likely accesses a DRG table file for a specific year.

*   **Files Accessed:** Likely a DRG table file (read-only). No explicit file names mentioned.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item containing DRG table data.
        *   `WK-DRG-DATA`: Temporary holding area for DRG data.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Structured access to DRG data.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Group item for a single DRG record.
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

### Program: IPDRG170

Similar to IPDRG160, but for the year 2016.

*   **Files Accessed:** Likely a DRG table file (read-only) for 2016.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`.
*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG181

Similar to IPDRG160, but for the year 2017.

*   **Files Accessed:** Likely a DRG table file (read-only) for 2017.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20171001' and `DRG-TAB` having `OCCURS 754`.
*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG190

Similar to IPDRG160, but for the year 2018.

*   **Files Accessed:** Likely a DRG table file (read-only) for 2018.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20181001' and `DRG-TAB` having `OCCURS 761`.
*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG200

Similar to IPDRG160, but for the year 2019.

*   **Files Accessed:** Likely a DRG table file (read-only) for 2019.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20191001' and `DRG-TAB` having `OCCURS 761`. Notes addition of DRG 319 and 320.
*   **Linkage Section:** Not present in the provided code.

---

### Program: IPDRG211

Similar to IPDRG160, but for the year 2020.

*   **Files Accessed:** Likely a DRG table file (read-only) for 2020.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20201001' and `DRG-TAB` having `OCCURS 767`. Notes changes in some DRG descriptions.
*   **Linkage Section:** Not present in the provided code.

---

### Program: LTCAL162

This program likely performs calculation logic using DRG and wage index data.

*   **Files Accessed:** Likely a provider-specific file (PSF), a CBSA wage index file, and DRG table files (`LTDRG160`, `IPDRG160`) via COPY statements.
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

### Program: LTCAL170

Similar to LTCAL162, updated for FY17.

*   **Files Accessed:** Likely a PSF, CBSA wage index file, and DRG table files (`LTDRG170`, `IPDRG170`).
*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated.
*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

### Program: LTCAL183

Similar to LTCAL170, updated for FY18.

*   **Files Accessed:** Likely a PSF, CBSA wage index file, and DRG table files (`LTDRG181`, `IPDRG181`).
*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3'. Some variables related to Subclause II removed.
*   **Linkage Section:** Similar to LTCAL170, with the removal of fields related to Subclause II.

---

### Program: LTCAL190

Similar to LTCAL183, updated for FY19.

*   **Files Accessed:** Likely a PSF, CBSA wage index file, and DRG table files (`LTDRG190`, `IPDRG190`).
*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0'.
*   **Linkage Section:** Similar to LTCAL183.

---

### Program: LTCAL202

Similar to LTCAL190, updated for FY20, including COVID-19 processing.

*   **Files Accessed:** Likely a PSF, CBSA wage index file, and DRG table files (`LTDRG200`, `IPDRG200`).
*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2'. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` for Disproportionate Patient Percentage (DPP) adjustment.

---

### Program: LTCAL212

Similar to LTCAL202, updated for FY21.

*   **Files Accessed:** Likely a PSF, CBSA wage index file, and DRG table files (`LTDRG210`, `IPDRG211`).
*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2'. Includes changes for CR11707 and CR11879. Notes addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in `PROV-NEW-HOLD`.
*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

---

### COPY Member: LTDRG160

This COPY member defines the structure for LTCH DRG table data for FY15.

*   **Files Accessed:** Not applicable.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry containing:
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG170

This COPY member defines the structure for LTCH DRG table data for FY16.

*   **Files Accessed:** Not applicable.
*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG181

This COPY member defines the structure for LTCH DRG table data for FY18.

*   **Files Accessed:** Not applicable.
*   **Working-Storage Section:** Structurally similar to LTDRG160 and LTDRG170, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG190

This COPY member defines the structure for LTCH DRG table data for FY19.

*   **Files Accessed:** Not applicable.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** Not applicable.

---

### COPY Member: LTDRG210

This COPY member defines the structure for LTCH DRG table data for FY21.

*   **Files Accessed:** Not applicable.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** Not applicable.

---

### Program: IPDRG104

This program uses a COPY statement to include DRG table data.

*   **Files Accessed:** Uses `COPY IPDRG104`, implying inclusion of DRG data from another file.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access to DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: IPDRG110

Similar to IPDRG104, uses COPY IPDRG110 for DRG data.

*   **Files Accessed:** Uses `COPY IPDRG110`, referencing a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`, with `DRG-DATA OCCURS 1000`.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: IPDRG123

Similar to IPDRG104, uses COPY IPDRG123 for DRG data.

*   **Files Accessed:** Uses `COPY IPDRG123`, indicating inclusion of DRG data from another file.
*   **Working-Storage Section:** Structurally similar to `IPDRG104` and `IPDRG110`, with `DRG-DATA OCCURS 1000`.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: IRFBN102

This program defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** Uses `COPY IRFBN102`, suggesting data from a file containing RFBNs.
*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access to RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Another code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: PPS state code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record, structurally identical to `WK-SSRFBN-REASON-ALL`.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: IRFBN105

Similar to IRFBN102, but likely for updated RFBN data.

*   **Files Accessed:** Uses `COPY IRFBN105`, referencing a file for updated RFBN data.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: LTCAL103

This program incorporates DRG and RFBN data for calculations.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100` (LTC DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN102` (IPPS state-specific RFBNs).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103 - W O R K I N G S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (FY 2003-2007).
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components, with numerous numeric variables for various payment calculation aspects.
    *   `01 PPS-DATA-ALL`: Holds final PPS calculation results, including return code, charge threshold, and many other data elements.
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data, including NPI, provider number, dates, waiver code, codes, indices, and various other parameters.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record, including CBSA code, effective date, and wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record, including CBSA code, size indicator, effective date, and wage indices (federal and Puerto Rico).
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program, containing provider NPI, provider number, patient status, DRG code, LOS, covered days, LTR days, discharge date, covered charges, and special pay indicator.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105

Similar to LTCAL103, but uses `IRFBN105` for RFBNs and has minor constant adjustments.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100`, `IPDRG104`, and `IRFBN105`.
*   **Working-Storage Section:** Very similar to `LTCAL103`, with `CAL-VERSION` as 'V10.5' and use of `IRFBN105`.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL111

Similar to LTCAL103, but without state-specific RFBNs and using `LTDRG110`, `IPDRG110`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG110`, `IPDRG110`. `IRFBN***` copybook is commented out.
*   **Working-Storage Section:** Similar to `LTCAL103`, with version `V11.1` and adjusted copybooks. No state-specific RFBN table is used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL123

Similar to LTCAL111, but uses `LTDRG123`, `IPDRG123`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG123`, `IPDRG123`. RFBN copybook is commented out.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table is used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### COPY Member: LTDRG100

This COPY member defines the structure for a LTC DRG table.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** No LINKAGE SECTION.

---

### COPY Member: LTDRG110

This COPY member defines the structure for a LTC DRG table.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** No LINKAGE SECTION.

---

### COPY Member: LTDRG123

This COPY member defines the structure for a LTC DRG table.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** No LINKAGE SECTION.

---

### Program: IPDRG080

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None explicitly. Defines a table in WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective Date ('20071001').
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

---

### Program: IPDRG090

Similar to IPDRG080, but for a different year's DRG data.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

---

### Program: IRFBN091

Defines a table of state-specific RFBNs.

*   **Files Accessed:** None.
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
        *   `05 MES-SSRFBN-CODE2 PIC 99`: Code.
        *   `05 FILLER PIC X`: Filler.
        *   `05 MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `05 MES-SSRFBN-REST PIC X(22)`: Remaining data.
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access to RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
*   **Linkage Section:** None.

---

### Program: LTCAL103

This program incorporates DRG and RFBN data for calculations.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100` (LTC DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN102` (IPPS state-specific RFBNs).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103 - W O R K I N G S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (FY 2003-2007).
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components, with numerous numeric variables for various payment calculation aspects.
    *   `01 PPS-DATA-ALL`: Holds final PPS calculation results, including return code, charge threshold, and many other data elements.
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data, including NPI, provider number, dates, waiver code, codes, indices, and various other parameters.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record, including CBSA code, effective date, and wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record, including CBSA code, size indicator, effective date, and wage indices (federal and Puerto Rico).
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program, containing provider NPI, provider number, patient status, DRG code, LOS, covered days, LTR days, discharge date, covered charges, and special pay indicator.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105

Similar to LTCAL103, but uses `IRFBN105` for RFBNs and has minor constant adjustments.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100`, `IPDRG104`, and `IRFBN105`.
*   **Working-Storage Section:** Very similar to `LTCAL103`, with `CAL-VERSION` as 'V10.5' and use of `IRFBN105`.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL111

Similar to LTCAL103, but without state-specific RFBNs and using `LTDRG110`, `IPDRG110`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG110`, `IPDRG110`. `IRFBN***` copybook is commented out.
*   **Working-Storage Section:** Similar to `LTCAL103`, with version `V11.1` and adjusted copybooks. No state-specific RFBN table is used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL123

Similar to LTCAL111, but uses `LTDRG123`, `IPDRG123`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG123`, `IPDRG123`. RFBN copybook is commented out.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table is used.
*   **Linkage Section:** Identical to `LTCAL103`.

---

### Program: LTCAL087

This program incorporates DRG data for calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG086`, implying use of data from that copybook.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL087 - W O R K I N G S T O R A G E'`: Comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V08.7'`: Version Number.
    *   `01 PROGRAM-CONSTANTS`: Federal Fiscal Year Begin Dates.
    *   `COPY LTDRG086`: Includes `LTDRG086` copybook with `WWM-ENTRY` (DRG table).
    *   `01 HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `01 PROV-NEW-HOLD`: Structure to hold provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill Data passed from calling program. Includes NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator.
    *   `01 PPS-DATA-ALL`: PPS data returned to calling program.
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

### Program: LTCAL091

Similar to LTCAL087, updated version.

*   **Files Accessed:** Similar to LTCAL087, uses `COPY LTDRG086`.
*   **Working-Storage Section:** Very similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL094

Similar to LTCAL091, uses `LTDRG093`, `IPDRG090`, `IRFBN091`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG093`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL091; `CAL-VERSION` is 'V09.4'. Copied data structures reflect year's changes. Notes addition of `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTCAL095

Similar to LTCAL094, uses `LTDRG095`, `IPDRG090`, `IRFBN091`.

*   **Files Accessed:** Uses `COPY` statements for `LTDRG095`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

---

### Program: LTDRG080

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None. Defines a table within WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `05 WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

---

### Program: LTDRG086

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of WWM-ENTRY.
*   **Linkage Section:** None.

---

### Program: LTDRG093

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

---

### Program: LTDRG095

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

---

### Program: IPDRG063

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the period.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: Weight of the DRG.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

### Program: IPDRG071

Similar to IPDRG063, but for a different year's DRG data.

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

### Program: LTCAL064

This program incorporates DRG data for calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, implying use of data from that copybook.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook, which contains a DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results.
    *   Several numeric and alphanumeric variables for PPS calculations and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `01 PROV-NEW-HOLD`: Structure to hold provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from a calling program, including provider information, DRG code, length of stay, discharge date, and charges.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

### Program: LTCAL072

Similar to LTCAL064, updated for a new fiscal year, with more complex calculations.

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (LTCH DRG table).
    *   `COPY IPDRG063`: Includes the `IPDRG063` copybook (IPPS DRG table).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices, and other factors.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

### Programs: LTCAL075, LTCAL080

These programs are expected to follow the structure of LTCAL072 with incremental changes in constants, rates, and potentially additional variables for new features.

---

### COPY Member: LTDRG062

This COPY member defines the structure for a LTCH DRG table.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains the raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefines `W-DRG-FILLS` to structure the data.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: The LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### COPY Members: LTDRG075, LTDRG080

These COPY members define DRG tables with updated data.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG062, but with updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (like `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.
*   **Linkage Section:** None.

---

### Program: LTCAL043

This program incorporates DRG data for calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Version number ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 510 times) with DRG code, relative weight, and average length of stay.
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure passed to/from the calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results structure (Return Code, Thresholds, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payments, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
        *   `PRICER-OPTION-SW`: Indicates if all tables were passed.
        *   `PPS-VERSIONS`: Contains version numbers (`PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, Provider Number, Dates, Waiver Code, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, Effective Date, Wage Index values).

---

### Program: LTCAL058

Similar to LTCAL043, updated version.

*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.8').
    *   `PROGRAM-CONSTANTS`: Holds dates for federal fiscal years.
    *   `LTDRG041`: Copy of DRG table structure (same as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Structure for holding intermediate PPS calculation results (same as in LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

---

### Program: LTCAL059

Similar to LTCAL058, uses `LTDRG057` for DRG data.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table; structure includes `WWM-ENTRY` (occurs 512 times) with DRG code, relative weight, and average length of stay.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in previous programs).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in previous programs).

---

### Program: LTCAL063

Similar to LTCAL059, uses `LTDRG057` and adds CBSA code.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V06.3').
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

### Program: LTDRG041

This is a data definition file, not a program, defining a DRG table.

*   **Files Accessed:** None. Data defined within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Table of DRG codes and related information as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTDRG057

This is a data definition file, not a program, defining a DRG table.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar to `LTDRG041`, defines a DRG table.
    *   `01 W-DRG-FILLS`: Table of DRG codes and related data as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### Program: LTCAL032

This program performs PPS calculations, utilizing DRG data.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031` which likely defines data structures for a table used in the program's logic.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string indicating working storage.
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor and Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version information and switches for pricing options (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, Provider Number, State, Dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Contains bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Contains calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Structured into `PPS-DATA` and `PPS-OTHER-DATA`.

---

### Program: LTCAL042

Similar to LTCAL032, with updated version and calculation constants.

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:** Almost identical to LTCAL032, with key differences:
    *   `CAL-VERSION` is 'C04.2'.
    *   `PPS-STD-FED-RATE` value differs (35726.18 vs 34956.15).
    *   `H-FIXED-LOSS-AMT` value differs (19590 vs 24450).
    *   `PPS-BDGT-NEUT-RATE` value differs (0.940 vs 0.934).
    *   `H-LOS-RATIO` (PIC 9(01)V9(05)) is added to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

---

### Program: LTDRG031

This is a copybook defining DRG table data structures.

*   **Files Accessed:** This is a copybook; it doesn't directly access files. It defines data structures used by other programs (LTCAL032, LTCAL042).
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None. Copybooks do not have linkage sections.

---

### Program: IPDRG063

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the period.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: Weight of the DRG.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

---

### Program: IPDRG071

Similar to IPDRG063, but for a different year's DRG data.

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

### Program: LTCAL064

This program incorporates DRG data for calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, implying use of data from that copybook.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook, which contains a DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results.
    *   Several numeric and alphanumeric variables for PPS calculations and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `01 PROV-NEW-HOLD`: Structure to hold provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from a calling program, including provider information, DRG code, length of stay, discharge date, and charges.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

### Program: LTCAL072

Similar to LTCAL064, updated for a new fiscal year, with more complex calculations.

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (LTCH DRG table).
    *   `COPY IPDRG063`: Includes the `IPDRG063` copybook (IPPS DRG table).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices, and other factors.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

---

### Programs: LTCAL075, LTCAL080

These programs are expected to follow the structure of LTCAL072 with incremental changes in constants, rates, and potentially additional variables for new features.

---

### Program: LTDRG062

This COPY member defines the structure for a LTCH DRG table.

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains the raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefines `W-DRG-FILLS` to structure the data.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: The LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

---

### COPY Members: LTDRG075, LTDRG080

These COPY members define DRG tables with updated data.

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG062, but with updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (like `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.
*   **Linkage Section:** None.

---

### Program: LTCAL043

This program incorporates DRG data for calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Version number ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 510 times) with DRG code, relative weight, and average length of stay.
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure passed to/from the calling program (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: PPS calculation results structure (Return Code, Thresholds, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payments, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
        *   `PRICER-OPTION-SW`: Indicates if all tables were passed.
        *   `PPS-VERSIONS`: Contains version numbers (`PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, Provider Number, Dates, Waiver Code, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, Effective Date, Wage Index values).

---

### Program: LTCAL058

Similar to LTCAL043, updated version.

*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.8').
    *   `PROGRAM-CONSTANTS`: Holds dates for federal fiscal years.
    *   `LTDRG041`: Copy of DRG table structure (same as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Structure for holding intermediate PPS calculation results (same as in LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

---

### Program: LTCAL059

Similar to LTCAL058, uses `LTDRG057` for DRG data.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table; structure includes `WWM-ENTRY` (occurs 512 times) with DRG code, relative weight, and average length of stay.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in previous programs).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in previous programs).

---

### Program: LTCAL063

Similar to LTCAL059, uses `LTDRG057` and adds CBSA code.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V06.3').
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

### Program: LTCAL032

This program performs PPS calculations, utilizing DRG data.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031` which likely defines data structures for a table used in the program's logic.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string indicating working storage.
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor and Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version information and switches for pricing options (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, Provider Number, State, Dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Contains bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Contains calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Structured into `PPS-DATA` and `PPS-OTHER-DATA`.

---

### Program: LTCAL042

Similar to LTCAL032, with updated version and calculation constants.

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:** Almost identical to LTCAL032, with key differences:
    *   `CAL-VERSION` is 'C04.2'.
    *   `PPS-STD-FED-RATE` value differs (35726.18 vs 34956.15).
    *   `H-FIXED-LOSS-AMT` value differs (19590 vs 24450).
    *   `PPS-BDGT-NEUT-RATE` value differs (0.940 vs 0.934).
    *   `H-LOS-RATIO` (PIC 9(01)V9(05)) is added to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

---

### Program: LTDRG031

This is a copybook defining DRG table data structures.

*   **Files Accessed:** This is a copybook; it doesn't directly access files. It defines data structures used by other programs (LTCAL032, LTCAL042).
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None. Copybooks do not have linkage sections.

---

### Overall Program Flow Summary:

The programs appear to function within a hierarchical structure for processing healthcare claims and calculating prospective payments:

1.  **LTMGR212:** Acts as a high-level driver. It reads billing records from `BILLFILE`, prepares data, calls `LTOPN212` for payment calculations, and formats results for `PRTOPER`.
2.  **LTOPN212:** Loads necessary data tables (provider, wage indices) from various input files. It then calls `LTDRV212` to perform the detailed payment calculations.
3.  **LTDRV212:** Selects the appropriate wage index based on discharge date and provider information. It then calls specific `LTCAL` modules (e.g., `LTCAL032`, `LTCAL162`, etc., depending on the fiscal year) to perform the actual payment calculations.
4.  **LTCALxx:** These modules contain the core payment calculation logic. They utilize DRG tables (often via COPY statements from `LTDRGxx` members) and other data to compute payment amounts, considering factors like LOS, DRG weights, wage indices, and various adjustments.
5.  **IPDRGxx:** These programs appear to define or load IPPS (Inpatient Prospective Payment System) DRG tables for different fiscal years. They are likely used by the `LTCAL` modules.
6.  **IRFBNxx:** These programs define or load state-specific Rural Floor Budget Neutrality Factors, used in specific calculation scenarios.
7.  **COPY Members (RUFL200, LTDRGxx, IPDRGxx):** These members provide data structure definitions, primarily for tables (DRG data, rural floor factors), which are incorporated into the main programs via `COPY` statements. They do not perform file I/O themselves but define the structure of data that would be read from files or embedded within programs.

The extensive versioning (e.g., `LTCAL032` vs. `LTCAL212`, `IPDRG160` vs. `IPDRG211`) indicates a long history of updates and modifications to accommodate changes in healthcare payment methodologies over the years. The numerous comments within the code suggest a focus on maintainability and tracking of changes.