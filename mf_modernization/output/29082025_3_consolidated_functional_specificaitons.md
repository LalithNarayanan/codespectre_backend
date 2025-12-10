## Data Definition and File Handling

This document consolidates the data definition and file handling information extracted from multiple functional specification documents (L1 through L8). It provides a detailed analysis of the COBOL programs, outlining the files they access (or are implied to access via COPY statements), their WORKING-STORAGE sections, and their LINKAGE sections.

The programs analyzed are primarily related to healthcare prospective payment systems (PPS), handling billing data, provider information, and various rate and index tables. The analysis reveals a series of programs that have evolved over time, with different versions handling specific fiscal years and incorporating changes in payment methodologies.

### Program Analysis

#### Program: LTMGR212 (from L1_FunctionalSpecification.md)

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format: `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format: `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal (comment).
    *   `PPMGR-VERSION`: 5-character field for program version ('M21.2').
    *   `LTOPN212`: 8-character literal (called program name).
    *   `EOF-SW`: 1-digit numeric field (End-of-File switch: 0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: 2-digit numeric field (line counter for `PRTOPER`), initialized to 65.
    *   `UT1-STAT`: 2-character field for `BILLFILE` status (`UT1-STAT1`, `UT1-STAT2`).
    *   `OPR-STAT`: 2-character field for `PRTOPER` status (`OPR-STAT1`, `OPR-STAT2`).
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (includes NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis and procedure code tables).
    *   `PPS-DATA-ALL`: Structure for data returned from `LTOPN212` (payment calculation results, wage indices, etc.).
    *   `PPS-CBSA`: 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure for calculated payment amounts from `LTOPN212` (site-neutral cost, IPPS payments, standard full/short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: Single character indicating pricing option.
        *   `PPS-VERSIONS`: Structure containing version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: Large structure for provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) for CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

#### Program: LTOPN212 (from L1_FunctionalSpecification.md)

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout: `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout: `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout: `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout: `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `OPN-VERSION`: 5-character field for program version ('021.2').
    *   `LTDRV212`: 8-character literal (called program name).
    *   `TABLES-LOADED-SW`: 1-digit numeric field (tables loaded indicator: 0 = not loaded, 1 = loaded).
    *   `EOF-SW`: 1-digit numeric field (End-of-File switch).
    *   `W-PROV-NEW-HOLD`: Structure to hold provider record (passed in or from `PROV-FILE`), mirroring `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status of input files.
    *   `CBSA-WI-TABLE`: Table for CBSA wage index data loaded from `CBSAX-FILE` (up to 10000 entries, indexed by `CU1`, `CU2`).
    *   `IPPS-CBSA-WI-TABLE`: Table for IPPS CBSA wage index data loaded from `IPPS-CBSAX-FILE` (up to 10000 entries, indexed by `MA1`, `MA2`, `MA3`).
    *   `MSA-WI-TABLE`: Table for MSA wage index data loaded from `MSAX-FILE` (up to 4000 entries, indexed by `MU1`, `MU2`).
    *   `WORK-COUNTERS`: Structure containing record counters for each file.
    *   `PROV-TABLE`: Table (up to 2400 entries) to hold provider data from `PROV-FILE` (`PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`, indexed by `PX1`, `PD2`, `PD3`).
    *   `PROV-NEW-HOLD`: Structure to hold provider record passed to `LTDRV212`, mirroring `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirroring `BILL-NEW-DATA` in LTMGR212.
    *   `PPS-DATA-ALL`: PPS data passed from/to `LTMGR212`, mirroring `PPS-DATA-ALL` in LTMGR212.
    *   `PPS-CBSA`: 5-character CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Payment data passed from/to `LTMGR212`, mirroring `PPS-PAYMENT-DATA` in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version info passed from `LTMGR212`, mirroring `PRICER-OPT-VERS-SW` in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Provider-specific info passed from `LTMGR212`, mirroring `PROV-RECORD-FROM-USER` in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, for wage index tables.

#### Program: LTDRV212 (from L1_FunctionalSpecification.md)

*   **Files Accessed:** Does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `DRV-VERSION`: 5-character field for program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals (names of called programs).
    *   `WS-9S`: 8-character numeric literal (all 9s, for date comparison).
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table (from COPY RUFL200) for rural floor adjustment factors.
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures for calculated fiscal year begin/end dates.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA/CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from LTOPN212 tables.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider record passed from LTOPN212, mirroring `PROV-NEW-HOLD` in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: Structure for billing data for older fiscal years.
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015+, mirroring `BILL-NEW-DATA` in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from LTOPN212.
    *   `PPS-DATA-ALL`: PPS data passed from/to LTOPN212.
    *   `PPS-CBSA`: 5-character CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed from/to LTOPN212.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version info passed from LTOPN212.
    *   `PROV-RECORD`: Provider-specific info passed from LTOPN212.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

#### COPY member: RUFL200 (from L1_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; defines a data structure.
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Contains `RUFL-TAB` (table of rural floor adjustment factors). Each entry has `RUFL-CBSA` (CBSA code), `RUFL-EFF-DATE` (effective date), and `RUFL-WI3` (wage index). Table has 459 entries.

#### Program: IPDRG160 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file.
*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item for DRG table data.
        *   `WK-DRG-DATA`: Group item for literal DRG data.
        *   `WK-DRG-DATA2` (REDEFINES `WK-DRG-DATA`): Structured table access.
            *   `DRG-TAB` (OCCURS 758): Table of DRG records.
                *   `DRG-DATA-TAB`: Single DRG record.
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code.
                    *   `FILLER1` (PIC X(01)): Filler.
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)): Filler.
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean of average length of stay.
                    *   `FILLER3` (PIC X(05)): Filler.
                    *   `DRG-LOW` (PIC X(01)): Indicator.
                    *   `FILLER5` (PIC X(01)): Filler.
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic mean of average length of stay.
                    *   `FILLER6` (PIC X(02)): Filler.
                    *   `DRG-PAC` (PIC X(01)): Indicator.
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Indicator.
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.
*   **Linkage Section:** Not present.

#### Program: IPDRG170 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2016.
*   **Working-Storage Section:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20161001', and `DRG-TAB` has `OCCURS 757`.
*   **Linkage Section:** Not present.

#### Program: IPDRG181 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2017.
*   **Working-Storage Section:** Structurally identical to IPDRG160/170, `WK-DRGX-EFF-DATE` is '20171001', and `DRG-TAB` has `OCCURS 754`.
*   **Linkage Section:** Not present.

#### Program: IPDRG190 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2018.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20181001', and `DRG-TAB` has `OCCURS 761`.
*   **Linkage Section:** Not present.

#### Program: IPDRG200 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2019.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20191001', and `DRG-TAB` has `OCCURS 761`.
*   **Linkage Section:** Not present.

#### Program: IPDRG211 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a read-only DRG table file for 2020.
*   **Working-Storage Section:** Structurally identical to previous IPDRG programs, `WK-DRGX-EFF-DATE` is '20201001', and `DRG-TAB` has `OCCURS 767`.
*   **Linkage Section:** Not present.

#### Program: LTCAL162 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses a Provider-Specific File (PSF), a CBSA wage index file, and LTCH/IPPS DRG table files (via COPY statements: `LTDRG160`, `IPDRG160`).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive filler.
    *   `CAL-VERSION`: Program version number ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in the program.
    *   `PROGRAM-FLAGS`: Flags for program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for payment.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data copied from DRG tables.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Input bill data from a calling program (likely `LTDRV`).
    *   `PPS-DATA-ALL`: Output PPS calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches indicating versions of pricer option and driver programs.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

#### Program: LTCAL170 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Similar to LTCAL162, likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG170`, `IPDRG170`).
*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'; constants and rates updated for FY17.
*   **Linkage Section:** Identical to LTCAL162's Linkage Section, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

#### Program: LTCAL183 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG181`, `IPDRG181`).
*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Variables related to Subclause II removed.
*   **Linkage Section:** Similar to LTCAL170, with fields related to Subclause II removed.

#### Program: LTCAL190 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Likely accesses PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG190`, `IPDRG190`).
*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **Linkage Section:** Similar to LTCAL183.

#### Program: LTCAL202 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Similar to previous LTCAL programs, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG200`, `IPDRG200`).
*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.
*   **Linkage Section:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` for Disproportionate Patient Percentage (DPP) adjustment.

#### Program: LTCAL212 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Similar to LTCAL202, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG210`, `IPDRG211`).
*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **Linkage Section:** Similar to LTCAL202, with no additional fields.

#### COPY member: LTDRG160 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; likely contains LTCH DRG table data for FY15.
*   **Working-Storage Section:** Defines structure of LTCH DRG table.
    *   `W-DRG-FILLS`: Contains DRG data in packed format.
    *   `W-DRG-TABLE` (REDEFINES `W-DRG-FILLS`): Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): Table entry.
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **Linkage Section:** Not present.

#### COPY member: LTDRG170 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; likely contains LTCH DRG table data for FY16.
*   **Working-Storage Section:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747`.
*   **Linkage Section:** Not present.

#### COPY member: LTDRG181 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; likely contains LTCH DRG table data for FY18.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 744`.
*   **Linkage Section:** Not present.

#### COPY member: LTDRG190 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; likely contains LTCH DRG table data for FY19.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **Linkage Section:** Not present.

#### COPY member: LTDRG210 (from L2_FunctionalSpecification.md)

*   **Files Accessed:** Not a program; likely contains LTCH DRG table data for FY21.
*   **Working-Storage Section:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **Linkage Section:** Not present.

#### Program: IPDRG104 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY IPDRG104`, implying inclusion from a file containing a DRG table.
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

#### Program: IPDRG110 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY IPDRG110`, implying inclusion from a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`'s `DRG-TABLE`.
*   **Linkage Section:** None.

#### Program: IPDRG123 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY IPDRG123`, implying inclusion from a file containing DRG data.
*   **Working-Storage Section:** Structurally identical to `IPDRG104`'s `DRG-TABLE`.
*   **Linkage Section:** None.

#### Program: IRFBN102 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY IRFBN102`, suggesting data from a file of state-specific Rural Floor Budget Neutrality Factors (RFBNs).
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
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: PPS state code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record (structurally identical to `WK-SSRFBN-REASON-ALL`).
*   **Linkage Section:** None.

#### Program: IRFBN105 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY IRFBN105`, implying inclusion from a file with updated RFBN data.
*   **Working-Storage Section:** Structurally identical to `IRFBN102`'s `PPS-SSRFBN-TABLE` and related message/holding fields.
*   **Linkage Section:** None.

#### Program: LTCAL103 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100` (LTCH DRG table), `IPDRG104` (IPPS DRG data), and `IRFBN102` (IPPS state-specific RFBNs).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46)`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05)`: Program version ('V10.3').
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings (`FED-FY-BEGIN-03` through `FED-FY-BEGIN-07`).
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components (numerous numeric variables for LOS, days, rates, adjustments, etc.).
    *   `01 PPS-DATA-ALL`: Holds final PPS calculation results (return code, threshold, and many other numeric fields).
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs (`PPDRV-VERSION`).
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, codes, indices, rates, ratios, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size indicator, effective date, federal and PR wage indices).
    *   `01 W-DRG-FILLS`: Holds DRG data in packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, DRG code, LOS, discharge date, charges, etc.).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to calling program.

#### Program: LTCAL105 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY` statements for `LTDRG100`, `IPDRG104`, and `IRFBN105` (IPPS state-specific RFBNs).
*   **Working-Storage Section:** Very similar to `LTCAL103`, differences are `CAL-VERSION` ('V10.5') and use of `IRFBN105`. Minor numeric constant adjustments.
*   **Linkage Section:** Identical to `LTCAL103`.

#### Program: LTCAL111 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY` statements for `LTDRG110` (LTCH DRG table), `IPDRG110` (IPPS DRG data). `IRFBN***` copybook is commented out.
*   **Working-Storage Section:** Similar to `LTCAL103`, with `CAL-VERSION` updated to `V11.1` and copybooks adjusted. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

#### Program: LTCAL123 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY` statements for `LTDRG123` (LTCH DRG table), `IPDRG123` (IPPS DRG data). RFBN copybook commented out.
*   **Working-Storage Section:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table used.
*   **Linkage Section:** Identical to `LTCAL103`.

#### COPY member: LTDRG100 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly accessed. Defines data directly.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

#### COPY member: LTDRG110 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly accessed. Defines data directly.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

#### COPY member: LTDRG123 (from L4_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly accessed. Defines data directly.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

#### Program: IPDRG080 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines a table in WORKING-STORAGE.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: DRG data table.
        *   `05 D-TAB`: Holds raw DRG data as packed strings, starting with '20071001'.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective Date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **Linkage Section:** None.

#### Program: IPDRG090 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None.
*   **Working-Storage Section:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **Linkage Section:** None.

#### Program: IRFBN091 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None.
*   **Working-Storage Section:**
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: PPS State Code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total Payment Amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record.
        *   `05 MES-SSRFBN-STATE PIC 99`: State Code.
        *   `05 FILLER PIC XX`.
        *   `05 MES-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
        *   `05 FILLER PIC XX`.
        *   `05 MES-SSRFBN-CODE2 PIC 99`.
        *   `05 FILLER PIC X`.
        *   `05 MES-SSRFBN-STNAM PIC X(20)`: State Name.
        *   `05 MES-SSRFBN-REST PIC X(22)`.
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `15 FILLER PIC XX`.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `15 FILLER PIC XX`.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`.
                    *   `15 FILLER PIC X`.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`.
*   **Linkage Section:** None.

#### Program: LTCAL087 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined. Uses `COPY` statements for `LTDRG086` and `IPDRG080`, implying use of data from these sources (likely DRG tables).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF PIC X(46)`: Comment.
    *   `01 CAL-VERSION PIC X(05)`: Program version ('V08.7').
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year begin dates (`FED-FY-BEGIN-03` to `FED-FY-BEGIN-07`).
    *   *(COPY statements bring in data structures from `LTDRG086` and `IPDRG080`, including DRG tables like `WWM-ENTRY`)*.
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for PPS. Includes fields like `H-LOS`, `H-REG-DAYS`, `H-TOTAL-DAYS`, `SSOT`, blended payment amounts, etc.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from calling program. Includes NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator.
    *   `01 PPS-DATA-ALL`: PPS data returned to calling program. Includes Return Code (`PPS-RTC`), Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Payments, Final Payment Amounts, Facility Costs, etc.
    *   `01 PPS-CBSA PIC X(05)`: CBSA Code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `88 ALL-TABLES-PASSED VALUE 'A'`.
        *   `88 PROV-RECORD-PASSED VALUE 'P'`.
        *   `05 PPS-VERSIONS`: Version of PPDRV program (`PPDRV-VERSION`).
    *   `01 PROV-NEW-HOLD`: Provider-specific data. Includes nested groups for NPI, provider number, dates (effective, FY begin, report, termination), waiver code, internship number, provider type, census division, MSA data (charge code index, geo location, wage index location, standard amount location), and other variables (facility specific rate, COLA, intern ratio, bed size, cost-to-charge ratio, CMI, SSI ratio, Medicaid ratio, PPS blend year indicator, PRUF update factor, DSH percent, FYE date).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices `W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3`).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size indicator, effective date, IPPS wage index, PR IPPS wage index).

#### Program: LTCAL091 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** Similar to LTCAL087, uses files implied by `COPY` statements (`LTDRG086`, `IPDRG080`).
*   **Working-Storage Section:** Similar to LTCAL087, with `CAL-VERSION` as 'V09.1'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

#### Program: LTCAL094 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG093`, `IPDRG090`, `IRFBN091`).
*   **Working-Storage Section:** Similar to LTCAL087/091, with `CAL-VERSION` as 'V09.4'. Copied data structures reflect year's changes. Note addition of `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **Linkage Section:** Identical to LTCAL087.

#### Program: LTCAL095 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG095`, `IPDRG090`, `IRFBN091`).
*   **Working-Storage Section:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. Copied data structures reflect year's changes.
*   **Linkage Section:** Identical to LTCAL087.

#### COPY member: LTDRG080 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines data directly.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Holds LTCH DRG data in packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `03 WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `05 WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **Linkage Section:** None.

#### COPY member: LTDRG086 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines data directly.
*   **Working-Storage Section:** Similar structure to LTDRG080, but with different data and 735 occurrences of `WWM-ENTRY`.
*   **Linkage Section:** None.

#### COPY member: LTDRG093 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines data directly.
*   **Working-Storage Section:** Similar structure to LTDRG086, but with different data.
*   **Linkage Section:** None.

#### COPY member: LTDRG095 (from L5_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines data directly.
*   **Working-Storage Section:** Similar structure to LTDRG093, but with different data.
*   **Linkage Section:** None.

#### Program: IPDRG063 (from L6_FunctionalSpecification.md)

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

#### Program: IPDRG071 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: Similar structure to IPDRG063.
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

#### Program: LTCAL064 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`, suggesting use of data from `LTDRG062` copybook (LTCH DRG table).
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables for intermediate PPS calculation results.
    *   Various numeric/alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `01 PROV-NEW-HOLD`: Structure for provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure for wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from calling program (provider info, DRG code, LOS, discharge date, charges).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to calling program (return codes, payment amounts, etc.).
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

#### Program: LTCAL072 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `01 HOLD-PPS-COMPONENTS`: Intermediate calculation results, expanded for short-stay outlier calculations.
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices, etc.
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

#### Programs: LTCAL075 and LTCAL080 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** Similar to LTCAL072, using `LTDRG075`/`LTDRG080` and `IPDRG063`/`IPDRG071` copybooks respectively.
*   **Working-Storage Section:** Similar structure to LTCAL072, with incremental changes in constants, rates, and potentially variables for version-specific calculations.
*   **Linkage Section:** Similar structure to LTCAL072, maintaining the same data structures.

#### COPY member: LTDRG062 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines data directly.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains raw data for LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

#### COPY members: LTDRG075 and LTDRG080 (from L6_FunctionalSpecification.md)

*   **Files Accessed:** None. Define data directly.
*   **Working-Storage Section:** Similar structure to LTDRG062, but with updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (e.g., `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may vary.
*   **Linkage Section:** None.

#### Program: LTCAL043 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: 46-character comment string.
    *   `CAL-VERSION`: 5-character version number ('C04.3').
    *   `LTDRG041`: Copy of DRG table structure.
        *   `WWM-ENTRY` (OCCURS 510): DRG data array (DRG code, relative weight, average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Structure for intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, blended payment amounts, etc.).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data structure passed to/from calling program (NPI, provider number, patient status, DRG code, LOS, covered days, LTR days, discharge date, covered charges, special pay indicator).
    *   `PPS-DATA-ALL`: PPS calculation results structure (return code, threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions structure.
        *   `PRICER-OPTION-SW`: Indicates if all tables were passed.
        *   `PPS-VERSIONS`: Contains version numbers (`PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (NPI, provider number, dates, waiver code, codes, variables, cost data).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (MSA, effective date, wage index values).

#### Program: LTCAL058 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY LTDRG041`, implying access to DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version number ('V05.8').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Copy of DRG table structure (same as in LTCAL043).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results structure (same as in LTCAL043).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043).

#### Program: LTCAL059 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure.
        *   `WWM-ENTRY` (OCCURS 512): DRG data array (DRG code, relative weight, average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results structure (same as in LTCAL043/058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as in LTCAL043/058).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as in LTCAL043/058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in LTCAL043/058).
    *   `PROV-NEW-HOLD`: Provider-specific data structure (same as in LTCAL043/058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data structure (same as in LTCAL043/058).

#### Program: LTCAL063 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Version number ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table structure (same as in LTCAL059).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (same as previous programs).
    *   `PPS-CBSA`: 5-character field for CBSA code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information structure (same as previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results structure (same as previous programs).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data structure; adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data structure; uses CBSA instead of MSA.

#### COPY member: LTDRG041 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:** Defines a DRG table.
    *   `W-DRG-FILLS`: Table of DRG codes and related information as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY` (OCCURS 510): DRG data array (DRG code, relative weight, average length of stay).
*   **Linkage Section:** None.

#### COPY member: LTDRG057 (from L7_FunctionalSpecification.md)

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:** Defines a DRG table.
    *   `W-DRG-FILLS`: Table of DRG codes and related data as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
        *   `WWM-ENTRY` (OCCURS 512): DRG data array (DRG code, relative weight, average length of stay).
*   **Linkage Section:** None.

#### Program: LTCAL032 (from L8_FunctionalSpecification.md)

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG031` for DRG table data.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string for working storage identification.
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay, Social Security Cost, Labor/Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version info and pricing option switches (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, Provider Number, State, dates, Waiver Code, Intermediary Number, Provider Type, Census Division, MSA data, Facility Specific Rate, COLA, Intern Ratio, Bed Size, Cost-to-Charge Ratio, CMI, SSI Ratio, Medicaid Ratio, PPS Blend Year Indicator, PRUF Update Factor, DSH Percent, FYE Date). Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, Effective Date, three wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to subroutine (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay, LOS, DRG Adjusted Pay, Federal Pay, Final Pay, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, LTR Days Used, Blend Year, COLA, etc.). Structured into `PPS-DATA` and `PPS-OTHER-DATA`.

#### Program: LTCAL042 (from L8_FunctionalSpecification.md)

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:** Almost identical to LTCAL032, with key differences:
    *   `CAL-VERSION`: 'C04.2'.
    *   `PPS-STD-FED-RATE`: 35726.18 (vs 34956.15 in LTCAL032).
    *   `H-FIXED-LOSS-AMT`: 19590 (vs 24450 in LTCAL032).
    *   `PPS-BDGT-NEUT-RATE`: 0.940 (vs 0.934 in LTCAL032).
    *   Added `H-LOS-RATIO` (PIC 9(01)V9(05)) to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

#### COPY member: LTDRG031 (from L8_FunctionalSpecification.md)

*   **Files Accessed:** None. Defines a data structure used by other programs.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

### Overall Program Flow and Data Handling Summary

The analyzed programs form a complex system for calculating prospective payments in healthcare. The flow generally involves:

1.  **LTMGR212:** Acts as a driver program, reading billing data from `BILLFILE`, preparing it, and calling `LTOPN212` for payment calculations. It then formats and outputs results to `PRTOPER`.
2.  **LTOPN212:** Loads various lookup tables (provider, CBSA, MSA wage indices) from files. It then calls `LTDRV212` to perform the core payment calculation logic.
3.  **LTDRV212:** Utilizes the loaded tables and provider information to select the correct wage index and then calls specific `LTCAL` modules (e.g., `LTCAL032`, `LTCAL162`) based on the fiscal year or other criteria to perform the detailed payment calculations.
4.  **LTCALxxx Programs:** These modules contain the core payment calculation logic, often relying on data from DRG tables (via `LTDRGxxx` copybooks) and potentially other tables like RFBNs (via `IRFBNxxx` copybooks). They receive bill and provider data via the linkage section and return calculated PPS data.
5.  **IPDRGxxx Programs:** These appear to be data definition files or programs that load IPPS (Inpatient Prospective Payment System) DRG data, often structured as tables with effective dates, DRG codes, weights, and average lengths of stay.
6.  **LTDRGxxx Programs:** These are copybooks that define the structure and data for LTCH (Long-Term Care Hospital) DRG tables, including DRG codes, relative weights, and average lengths of stay.

The extensive use of `COPY` statements indicates a modular design, where data structures and potentially common logic are shared across multiple programs. The versioning (e.g., `LTCAL162`, `LTCAL170`, `LTCAL032`, `LTCAL042`) clearly shows an evolution of the payment system logic over different fiscal years, with updates to rates, calculation methods, and data requirements. The presence of specific fields related to wage indices, CBSA/MSA codes, and various payment components highlights the complexity of the PPS calculations.

It is important to note that the absence of `FILE SECTION` entries in most snippets implies that file access is handled either by calling programs or through dynamic file handling not detailed here. The "Files Accessed" descriptions often infer file usage based on the presence of `COPY` statements or the context of the data structures.