## Data Definition and File Handling

This document consolidates the data definition and file handling information extracted from multiple functional specification documents (L1 through L8). It provides a detailed analysis of the COBOL programs, outlining the files they access (or are implied to access via COPY statements), their WORKING-STORAGE SECTION data structures, and their LINKAGE SECTION data structures.

The programs analyzed are primarily involved in calculating prospective payment system (PPS) amounts, likely for healthcare claims, with a focus on Long-Term Care (LTCH) and Inpatient Prospective Payment System (IPPS) methodologies. The analysis reveals a lineage of programs that have evolved over time, with different versions handling specific fiscal years and incorporating changes in payment rules.

### Program: LTMGR212

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records (record format `BILL-REC`, 422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports (record format `PRTOPER-LINE`, 133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 51-character literal (comment).
    *   `PPMGR-VERSION`: 5-character field storing the program version ('M21.2').
    *   `LTOPN212`: 8-character literal (name of the called program).
    *   `EOF-SW`: 1-digit numeric field (end-of-file switch: 0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: 2-digit numeric field counting lines written to `PRTOPER` (initialized to 65).
    *   `UT1-STAT`: 2-character field for `BILLFILE` status (`UT1-STAT1`, `UT1-STAT2`).
    *   `OPR-STAT`: 2-character field for `PRTOPER` status (`OPR-STAT1`, `OPR-STAT2`).
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (includes NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis and procedure code tables).
    *   `PPS-DATA-ALL`: Structure containing data returned from `LTOPN212` (payment calculation results, wage indices).
    *   `PPS-CBSA`: 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure holding payment amounts calculated by `LTOPN212` (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure holding pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Single character indicating pricing option.
        *   `PPS-VERSIONS`: Structure containing version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (arrays) for CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

### Program: LTOPN212

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records (record layout `PROV-REC`, 240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data (record layout `CBSAX-REC`).
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data (record layout `F-IPPS-CBSA-REC`).
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data (record layout `MSAX-REC`).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 48-character literal (comment).
    *   `OPN-VERSION`: 5-character field storing the program version ('021.2').
    *   `LTDRV212`: 8-character literal (name of the called program).
    *   `TABLES-LOADED-SW`: 1-digit numeric field (tables loaded: 0 = not loaded, 1 = loaded).
    *   `EOF-SW`: 1-digit numeric field (end-of-file switch).
    *   `W-PROV-NEW-HOLD`: Structure to hold provider record (passed or from `PROV-FILE`), mirrors `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status of input files.
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data (up to 10000 entries, indexed by `CU1`, `CU2`).
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data (up to 10000 entries, indexed by `MA1`, `MA2`, `MA3`).
    *   `MSA-WI-TABLE`: Table for MSA wage index data (up to 4000 entries, indexed by `MU1`, `MU2`).
    *   `WORK-COUNTERS`: Structure containing counters for records read from each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) to hold provider data from `PROV-FILE` (divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`, indexed by `PX1`, `PD2`, `PD3`).
    *   `PROV-NEW-HOLD`: Structure to hold provider record to be passed to `LTDRV212`, mirrors `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirrors `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: Structure for PPS data passed from and returned to `LTMGR212`, mirrors `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: 5-character CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Structure for payment data passed from and returned to `LTMGR212`, mirrors `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Structure holding pricer option and version information passed from `LTMGR212`, mirrors `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Structure containing provider-specific information passed from `LTMGR212`, mirrors `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, holding wage index tables.

### Program: LTDRV212

*   **Files Accessed:** Does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 48-character literal (comment).
    *   `DRV-VERSION`: 5-character field storing the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of called programs (likely different `LTCAL` versions).
    *   `WS-9S`: 8-character numeric literal with all 9s (for date comparison).
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table (defined in COPY `RUFL200`) containing rural floor adjustment factors for various CBSAs.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold fiscal year begin and end dates calculated from the bill's discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from tables in LTOPN212.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field to hold the Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field to hold the supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding the provider record passed from `LTOPN212`, mirrors `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure to hold billing data for older fiscal years (pre-Jan 2015).
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015 and later, mirrors `BILL-NEW-DATA` in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: Structure for PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure for payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Structure holding pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Structure containing provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

### COPY Member: RUFL200

*   **Files Accessed:** None (as it's a COPY member, not a program).
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Contains a table `RUFL-TAB` of rural floor adjustment factors. Each entry includes `RUFL-CBSA` (CBSA code), `RUFL-EFF-DATE` (effective date), and `RUFL-WI3` (wage index). The table has 459 entries.

### Overall Program Flow (L1 Analysis)

1.  **LTMGR212:** Reads `BILLFILE`, prepares data, calls `LTOPN212` for payment calculation, formats and writes results to `PRTOPER`.
2.  **LTOPN212:** Loads provider and wage index tables from various files, determines table usage based on discharge date and pricer option, then calls `LTDRV212` for payment calculations.
3.  **LTDRV212:** Selects the appropriate wage index based on discharge date and provider information, then calls the correct `LTCAL` module (not shown) for final payment calculations, chosen by the bill's fiscal year.

The extensive comments suggest a long history of updates. The programs are designed to handle complex long-term care prospective payment systems.

---

### Program: IPDRG160

*   **Files Accessed:** Likely accesses a read-only DRG (Diagnosis Related Group) table file containing DRG codes, weights, and descriptions. No file names are explicitly mentioned.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item for DRG table data.
        *   `WK-DRG-DATA`: Group item holding DRG data in a literal, record-like format (temporary holding).
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
                    *   `DRG-PAC` (PIC X(01)): Post-acute care indicator.
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Special post-acute care indicator.
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.
*   **Linkage Section:** Not present.

### Program: IPDRG170

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2016.
*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`. DRG data is specific to 2016.
*   **Linkage Section:** Not present.

### Program: IPDRG181

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2017.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20171001', and `DRG-TAB` has `OCCURS 754`. DRG data is specific to 2017.
*   **Linkage Section:** Not present.

### Program: IPDRG190

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2018.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20181001', and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2018.
*   **Linkage Section:** Not present.

### Program: IPDRG200

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2019.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20191001', and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2019.
*   **Linkage Section:** Not present.

### Program: IPDRG211

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2020.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20201001', and `DRG-TAB` has `OCCURS 767`. DRG data is specific to 2020.
*   **Linkage Section:** Not present.

### Program: LTCAL162

*   **Files Accessed:** Likely accesses a Provider-Specific File (PSF), a CBSA wage index file, and LTCH/IPPS DRG table files (`LTDRG160`, `IPDRG160`) via COPY statements. These are read-only.
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

### Program: LTCAL170

*   **Files Accessed:** Similar to LTCAL162, likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG170`, `IPDRG170`).
*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.
*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

### Program: LTCAL183

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG181`, `IPDRG181`).
*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Variables related to Subclause II have been removed.
*   **Linkage Section:** Similar to LTCAL170, with the removal of fields related to Subclause II.

### Program: LTCAL190

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG190`, `IPDRG190`).
*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **Linkage Section:** Similar to LTCAL183.

### Program: LTCAL202

*   **Files Accessed:** Similar to previous LTCAL programs, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG200`, `IPDRG200`).
*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` to handle the Disproportionate Patient Percentage (DPP) adjustment.

### Program: LTCAL212

*   **Files Accessed:** Similar to LTCAL202, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG210`, `IPDRG211`).
*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

### COPY Member: LTDRG160

*   **Files Accessed:** None (as it's a COPY member). Likely contains LTCH DRG table data for FY15.
*   **Working-Storage Section:** Defines the structure of the LTCH DRG table.
    *   `W-DRG-FILLS`: Contains DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **Linkage Section:** None.

### COPY Member: LTDRG170

*   **Files Accessed:** None. Similar to LTDRG160, but for FY16.
*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747` times.
*   **Linkage Section:** None.

### COPY Member: LTDRG181

*   **Files Accessed:** None. Contains LTCH DRG data for FY18.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** None.

### COPY Member: LTDRG190

*   **Files Accessed:** None. Contains LTCH DRG data for FY19.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** None.

### COPY Member: LTDRG210

*   **Files Accessed:** None. Contains LTCH DRG data for FY21.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** None.

---

### Program: IPDRG104

*   **Files Accessed:** The program uses a `COPY IPDRG104` statement, implying data inclusion from a file named `IPDRG104`, likely a DRG table.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for DRG data access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

### Program: IPDRG110

*   **Files Accessed:** Uses a `COPY IPDRG110` statement, referencing a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

### Program: IPDRG123

*   **Files Accessed:** Uses a `COPY IPDRG123` statement, indicating inclusion of DRG data from another file.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`.
*   **Linkage Section:** None.

### Program: IRFBN102

*   **Files Accessed:** The `COPY IRFBN102` statement suggests data from a file containing state-specific Rural Floor Budget Neutrality Factors (RFBNS).
*   **Working-Storage Section:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNS.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for RFBN data access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries, sorted by state code).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Unclear purpose code.
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: State code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record (structurally identical to `WK-SSRFBN-REASON-ALL`).
*   **Linkage Section:** None.

### Program: IRFBN105

*   **Files Accessed:** Uses a `COPY IRFBN105` statement, referencing a file presumably containing updated RFBN data.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`.
*   **Linkage Section:** None.

### Program: LTCAL103

*   **Files Accessed:** Uses `COPY` statements to include data from `LTDRG100` (LTC DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN102` (IPPS state-specific RFBNs).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103      - W O R K I N G   S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components (numerous numeric variables for payment calculation aspects).
    *   `01 PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, codes, indices, rates, ratios, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record.
        *   `05 W-CBSA PIC X(5)`: CBSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective date.
        *   `05 W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA code, size indicator, effective date, wage indices).
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format (redefined below).
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for DRG data access.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program (NPI, provider number, patient status, DRG code, LOS, covered days, discharge date, charges, etc.).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

### Program: LTCAL105

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG100`, `IPDRG104`, and `IRFBN105`.
*   **Working-Storage Section:** Very similar to `LTCAL103`, with differences in `CAL-VERSION`, copybooks used (`IRFBN105`), and minor numeric constant adjustments.
*   **Linkage Section:** Identical to `LTCAL103`.

### Program: LTCAL111

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG110`, `IPDRG110`. A commented-out `COPY IRFBN***` suggests no state-specific RFBN table is used.
*   **Working-Storage Section:** Similar to `LTCAL103`, with `CAL-VERSION` updated to `V11.1` and copybooks adjusted.
*   **Linkage Section:** Identical to `LTCAL103`.

### Program: LTCAL123

*   **Files Accessed:** Includes data via `COPY` statements from `LTDRG123`, `IPDRG123`. Commented-out copybook for RFBNs, similar to LTCAL111.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table is used.
*   **Linkage Section:** Identical to `LTCAL103`.

### COPY Member: LTDRG100

*   **Files Accessed:** None. Data is defined directly within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### COPY Member: LTDRG110

*   **Files Accessed:** None. Data is defined directly within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### COPY Member: LTDRG123

*   **Files Accessed:** None. Data is defined directly within the program.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

**Note on COPY statements:** The `COPY` statements indicate reliance on external data files (tables) for DRG and RFBN information. Analyzing these copied files would be necessary for a complete understanding.

---

### Program: IPDRG080

*   **Files Accessed:** None. Defines a table in WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds DRG data in a packed string. Includes `FILLER PIC X(08) VALUE '20071001'` for the effective date.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for DRG data access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective Date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

### Program: IPDRG090

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

### Program: IRFBN091

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
        *   `05 MES-SSRFBN-CODE2 PIC 99`: Code (unclear purpose).
        *   `05 FILLER PIC X`: Filler.
        *   `05 MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `05 MES-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNS.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for RFBN data access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries, sorted by state code).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Code (unclear purpose).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
*   **Linkage Section:** None.

### Program: LTCAL087

*   **Files Accessed:** No explicit `FILE-CONTROL` entries. `COPY` statements imply use of data from `LTDRG086` and `IPDRG080`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL087      - W O R K I N G   S T O R A G E'`: Comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V08.7'`: Version Number.
    *   `01 PROGRAM-CONSTANTS`: Federal Fiscal Year Begin Dates.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `COPY LTDRG086`: Includes `LTDRG086` copybook (DRG table `WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for PPS. Includes `H-LOS`, `H-REG-DAYS`, `H-TOTAL-DAYS`, etc.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill Data passed from calling program.
        *   `10 B-NPI10`: National Provider Identifier (NPI).
        *   `10 B-PROVIDER-NO`: Provider Number.
        *   `10 B-PATIENT-STATUS`: Patient Status.
        *   `10 B-DRG-CODE`: DRG Code.
        *   `10 B-LOS`: Length of Stay.
        *   `10 B-COV-DAYS`: Covered Days.
        *   `10 B-LTR-DAYS`: Lifetime Reserve Days.
        *   `10 B-DISCHARGE-DATE`: Discharge date (CCYYMMDD).
        *   `10 B-COV-CHARGES`: Covered Charges.
        *   `10 B-SPEC-PAY-IND`: Special Pay Indicator.
        *   `10 FILLER`: Filler.
    *   `01 PPS-DATA-ALL`: PPS data returned to calling program. Includes `PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.
    *   `01 PPS-CBSA`: CBSA Code.
    *   `01 PRICER-OPT-VERS-SW`: Pricer Option and Version Switch.
        *   `05 PRICER-OPTION-SW`: Indicates table passing method.
        *   `05 PPS-VERSIONS`: Contains `PPDRV-VERSION`.
    *   `01 PROV-NEW-HOLD`: Provider Data passed from calling program. Includes NPI, provider number, dates, waiver code, various variables, and cost data.
        *   `02 PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`: Subdivisions of provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH Wage Index Record (CBSA, Effective Date, Wage Indices).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS Wage Index Record (CBSA, Size, Effective Date, IPPS Wage Index, PR IPPS Wage Index).

### Program: LTCAL091

*   **Files Accessed:** Similar to LTCAL087, relies on `COPY LTDRG086` and `IPDRG080`.
*   **Working-Storage Section:** Similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

### Program: LTCAL094

*   **Files Accessed:** Uses `COPY` statements for `LTDRG093`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL087/091, with `CAL-VERSION` as 'V09.4'. Copied data structures reflect year's changes. Note the addition of `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

### Program: LTCAL095

*   **Files Accessed:** Uses `COPY` statements for `LTDRG095`, `IPDRG090`, `IRFBN091`.
*   **Working-Storage Section:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

### COPY Member: LTDRG080

*   **Files Accessed:** None. Defines a table within WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `03 WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `05 WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

### COPY Member: LTDRG086

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.
*   **Linkage Section:** None.

### COPY Member: LTDRG093

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

### COPY Member: LTDRG095

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

**Note on Packed Data:** The long strings of numeric data within `FILLER` fields in `IPDRGxxx` programs and `W-DRG-FILLS` fields in `LTDRGxxx` programs likely represent packed DRG table data. Unpacking would be required for a full understanding.

---

### Program: IPDRG063

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

### Program: IPDRG071

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:** Similar structure to IPDRG063, with `DRG-DATA` having `OCCURS 580` entries.
*   **Linkage Section:** None.

### Program: LTCAL064

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, suggesting data from that copybook.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes `LTDRG062` copybook (LTCH DRG table `WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `01 PROV-NEW-HOLD`: Structure for provider data (NPI, provider number, dates, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure for wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from calling program (provider info, DRG code, LOS, discharge date, charges).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to calling program (return codes, payment amounts).
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

### Program: LTCAL072

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded for short-stay outlier calculations.
    *   Variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data for LTCH.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data for IPPS.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from calling program (updated to numeric DRG-CODE).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to calling program.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data.

### Programs: LTCAL075 and LTCAL080

*   **Files Accessed:** Similar to LTCAL072, using copybooks like `LTDRG075` and `LTDRG080`.
*   **Working-Storage Section:** Similar structure to LTCAL072, with incremental changes in constants, rates, and potentially additional variables for new calculations.
*   **Linkage Section:** Similar structure to LTCAL072.

### COPY Member: LTDRG062

*   **Files Accessed:** None. Defines DRG table data.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for data access.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### COPY Members: LTDRG075 and LTDRG080

*   **Files Accessed:** None. Define DRG tables.
*   **Working-Storage Section:** Similar structure to LTDRG062, but with updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (`WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.
*   **Linkage Section:** None.

---

### Program: LTCAL043

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 46-character comment string.
    *   `CAL-VERSION`: 5-character version number ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 510 times) with `WWM-DRG` (3-char DRG code), `WWM-RELWT` (1V9(4) relative weight), `WWM-ALOS` (2V9(1) average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Structure passed to/from calling program (bill info: NPI, provider number, patient status, DRG code, LOS, covered days, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: Structure containing PPS calculation results (return code, threshold values, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Structure indicating pricing tables and versions used (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Structure holding provider-specific data (NPI, provider number, dates, waiver code, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Structure containing wage index data (MSA, Effective Date, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`).

### Program: LTCAL058

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.8').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table (same structure as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

### Program: LTCAL059

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 512 times) with `WWM-DRG` (3-char DRG code), `WWM-RELWT` (1V9(4) relative weight), `WWM-ALOS` (2V9(1) average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in LTCAL043 and LTCAL058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in LTCAL043 and LTCAL058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in LTCAL043 and LTCAL058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in LTCAL043 and LTCAL058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in LTCAL043 and LTCAL058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in LTCAL043 and LTCAL058).

### Program: LTCAL063

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table (same structure as in LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: 5-character field for CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

### COPY Member: LTDRG041

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:** Defines a DRG table.
    *   `W-DRG-FILLS`: Table of DRG codes and related info as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY`: Array (occurs 510 times) with `WWM-DRG` (3-char DRG code), `WWM-RELWT` (1V9(4) relative weight), `WWM-ALOS` (2V9(1) average length of stay).
*   **Linkage Section:** None.

### COPY Member: LTDRG057

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:** Defines a DRG table.
    *   `W-DRG-FILLS`: Table of DRG codes and related data as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY`: Array (occurs 512 times) with `WWM-DRG` (3-char DRG code), `WWM-RELWT` (1V9(4) relative weight), `WWM-ALOS` (2V9(1) average length of stay).
*   **Linkage Section:** None.

**Note on Packed Data:** The `W-DRG-FILLS` fields in `LTDRGxxx` programs are likely packed data representations of DRG tables requiring unpacking for full understanding.

---

### Program: LTCAL032

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031` for DRG table data structures.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string (comment).
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor/Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing option switches (`PRICER-OPTION-SW` (A=All Tables Passed, P=Provider Record Passed), `PPS-VERSIONS` (`PPDRV-VERSION`)).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Subdivided into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Lifetime Reserve Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Subdivided into `PPS-DATA` and `PPS-OTHER-DATA`.

### Program: LTCAL042

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   Almost identical to LTCAL032, with key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` value: 35726.18 (vs. 34956.15).
        *   `H-FIXED-LOSS-AMT` value: 19590 (vs. 24450).
        *   `PPS-BDGT-NEUT-RATE` value: 0.940 (vs. 0.934).
        *   Added field `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

### COPY Member: LTDRG031

*   **Files Accessed:** None. Defines DRG table data structures used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 chars each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

**Summary of Commonalities and Differences (L8 Analysis):**
LTCAL032 and LTCAL042 perform similar PPS calculations. Differences include version numbers and hardcoded values (`PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`). LTCAL042 also includes `H-LOS-RATIO` and logic for a special provider. Both heavily utilize the DRG table from `LTDRG031`.

---

### Program: LTCAL043 (Detailed Linkage)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041` for DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 46-character comment.
    *   `CAL-VERSION`: Version 'C04.3'.
    *   `LTDRG041` (COPY): Contains `W-DRG-TABLE` (510 `WWM-ENTRY` records: `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill info structure (NPI, provider number, patient status, DRG code, LOS, covered days, discharge date, charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS results structure (return code, thresholds, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (`PRICER-OPTION-SW`, `PPS-VERSIONS` with `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`).

### Program: LTCAL058

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.8'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table (same structure as LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as LTCAL043).

### Program: LTCAL059

*   **Files Accessed:** Uses `COPY LTDRG057` for DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.9'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043/058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as LTCAL043/058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as LTCAL043/058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as LTCAL043/058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as LTCAL043/058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as LTCAL043/058).

### Program: LTCAL063

*   **Files Accessed:** Uses `COPY LTDRG057`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V06.3'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table (same structure as LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as previous).
    *   `PPS-CBSA`: 5-character CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as previous).
    *   `PPS-DATA-ALL`: PPS calculation results (same as previous).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as previous).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

### COPY Member: LTDRG041

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 510 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

### COPY Member: LTDRG057

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

**Note on COPY statements:** These programs rely on external data definitions (`LTDRG041`, `LTDRG057`).

---

### Program: LTCAL032 (Detailed Analysis)

*   **Files Accessed:** None explicitly defined. Relies on `COPY LTDRG031` for DRG table data structures.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string comment.
    *   `CAL-VERSION`: Version 'C03.2'.
    *   `LTDRG031` (COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor/Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing option switches (`PRICER-OPTION-SW` (A=All Tables Passed, P=Provider Record Passed), `PPS-VERSIONS` (`PPDRV-VERSION`)).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Subdivided into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Lifetime Reserve Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Subdivided into `PPS-DATA` and `PPS-OTHER-DATA`.

### Program: LTCAL042

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   Almost identical to LTCAL032, with key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` value: 35726.18 (vs. 34956.15).
        *   `H-FIXED-LOSS-AMT` value: 19590 (vs. 24450).
        *   `PPS-BDGT-NEUT-RATE` value: 0.940 (vs. 0.934).
        *   Added field `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

### COPY Member: LTDRG031

*   **Files Accessed:** None. Defines DRG table data structures used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 chars each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

**Summary of Commonalities and Differences (L8 Analysis):**
LTCAL032 and LTCAL042 perform similar PPS calculations. Differences include version numbers and hardcoded values (`PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`). LTCAL042 also includes `H-LOS-RATIO` and logic for a special provider. Both heavily utilize the DRG table from `LTDRG031`. The exact files used to populate this table are not defined in the provided code.

---

### Program: LTCAL043 (Detailed Linkage)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 46-character comment.
    *   `CAL-VERSION`: Version 'C04.3'.
    *   `LTDRG041` (COPY): Contains `W-DRG-TABLE` (510 `WWM-ENTRY` records: `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill info structure (NPI, provider number, patient status, DRG code, LOS, covered days, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS results structure (return code, thresholds, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (`PRICER-OPTION-SW`, `PPS-VERSIONS` with `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`).

### Program: LTCAL058

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.8'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table (same structure as LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as LTCAL043).

### Program: LTCAL059

*   **Files Accessed:** Uses `COPY LTDRG057` for DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.9'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043/058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as LTCAL043/058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as LTCAL043/058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as LTCAL043/058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as LTCAL043/058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as LTCAL043/058).

### Program: LTCAL063

*   **Files Accessed:** Uses `COPY LTDRG057`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V06.3'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table (same structure as LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as previous).
    *   `PPS-CBSA`: 5-character CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as previous).
    *   `PPS-DATA-ALL`: PPS calculation results (same as previous).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as previous).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

### COPY Member: LTDRG041

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 510 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

### COPY Member: LTDRG057

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

**Note on COPY statements:** These programs rely on external data definitions (`LTDRG041`, `LTDRG057`).

---

### Program: LTCAL032 (Detailed Analysis)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031` for DRG table data structures.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string comment.
    *   `CAL-VERSION`: Version 'C03.2'.
    *   `LTDRG031` (COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor/Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing option switches (`PRICER-OPTION-SW` (A=All Tables Passed, P=Provider Record Passed), `PPS-VERSIONS` (`PPDRV-VERSION`)).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Operating Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Subdivided into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Lifetime Reserve Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA). Subdivided into `PPS-DATA` and `PPS-OTHER-DATA`.

### Program: LTCAL042

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   Almost identical to LTCAL032, with key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` value: 35726.18 (vs. 34956.15).
        *   `H-FIXED-LOSS-AMT` value: 19590 (vs. 24450).
        *   `PPS-BDGT-NEUT-RATE` value: 0.940 (vs. 0.934).
        *   Added field `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

### COPY Member: LTDRG031

*   **Files Accessed:** None. Defines DRG table data structures used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 chars each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

**Summary of Commonalities and Differences (L8 Analysis):**
LTCAL032 and LTCAL042 perform similar PPS calculations. Differences include version numbers and hardcoded values (`PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`). LTCAL042 also includes `H-LOS-RATIO` and logic for a special provider. Both heavily utilize the DRG table from `LTDRG031`. The exact files used to populate this table are not defined in the provided code.

---

### Program: LTCAL043 (Detailed Linkage)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 46-character comment.
    *   `CAL-VERSION`: Version 'C04.3'.
    *   `LTDRG041` (COPY): Contains `W-DRG-TABLE` (510 `WWM-ENTRY` records: `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payments, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill info structure (NPI, provider number, patient status, DRG code, LOS, covered days, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS results structure (return code, thresholds, MSA, Wage Index, Avg LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (`PRICER-OPTION-SW`, `PPS-VERSIONS` with `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, `W-WAGE-INDEX1`, `W-WAGE-INDEX2`).

### Program: LTCAL058

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.8'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table (same structure as LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as LTCAL043).

### Program: LTCAL059

*   **Files Accessed:** Uses `COPY LTDRG057` for DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V05.9'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table structure.
        *   `WWM-ENTRY`: Array (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as LTCAL043/058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as LTCAL043/058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as LTCAL043/058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as LTCAL043/058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as LTCAL043/058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as LTCAL043/058).

### Program: LTCAL063

*   **Files Accessed:** Uses `COPY LTDRG057`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version 'V06.3'.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057` (COPY): DRG table (same structure as LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as previous).
    *   `PPS-CBSA`: 5-character CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as previous).
    *   `PPS-DATA-ALL`: PPS calculation results (same as previous).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as previous).
    *   `PROV-NEW-HOLD`: Provider-specific data; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; uses CBSA instead of MSA.

### COPY Member: LTDRG041

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 510 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

### COPY Member: LTDRG057

*   **Files Accessed:** None. Data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: DRG table data as packed strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as `WWM-ENTRY` table (occurs 512 times) with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`.
*   **Linkage Section:** None.

**Note on COPY statements:** These programs rely on external data definitions (`LTDRG041`, `LTDRG057`).