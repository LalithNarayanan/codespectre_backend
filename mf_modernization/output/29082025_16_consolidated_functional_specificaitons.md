## Data Definition and File Handling

This section consolidates the data definitions and file handling information from multiple functional specification documents (L1 through L8), providing a comprehensive view of the COBOL programs involved in prospective payment system (PPS) calculations.

### Program Analysis Overview

The analyzed COBOL programs are primarily involved in calculating prospective payments for healthcare claims, likely within a Long-Term Care (LTCH) or similar facility setting. They process billing data, utilize various lookup tables (DRG, wage index, rural factors), and perform complex calculations based on fiscal year, provider-specific information, and regulatory rules. The programs often call sub-modules to perform specific calculation steps.

A common pattern observed is the extensive use of `COPY` statements, indicating that data structures and potentially logic are shared across programs, promoting modularity and maintainability. However, this also means that a complete understanding of file dependencies requires analyzing these copybooks.

### Program Details

Here's a detailed breakdown of each program, including files accessed, working-storage data structures, and linkage section data structures:

---

#### Program: LTMGR212 (from L1_FunctionalSpecification.md)

This program acts as a primary driver, reading billing records, preparing data, calling calculation modules, and formatting output reports.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format described by `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for prospective payment reports. Record format described by `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal (comment).
    *   `PPMGR-VERSION`: A 5-character field for the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of the called program.
    *   `EOF-SW`: A 1-digit numeric field for end-of-file indication (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field counting lines written to `PRTOPER`, initialized to 65.
    *   `UT1-STAT`: A 2-character field for `BILLFILE` status (`UT1-STAT1`, `UT1-STAT2`).
    *   `OPR-STAT`: A 2-character field for `PRTOPER` status (`OPR-STAT1`, `OPR-STAT2`).
    *   `BILL-WORK`: Structure holding input bill record from `BILLFILE` (provider NPI, patient status, DRG code, LOS, coverage days, cost report days, discharge date, charges, special pay indicator, review code, diagnosis/procedure code tables).
    *   `PPS-DATA-ALL`: Structure containing payment calculation results from `LTOPN212` (payment amounts, wage indices, etc.).
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure holding calculated payment amounts (site-neutral cost, IPPS payments, standard full and short stay payments).
    *   `BILL-NEW-DATA`: Structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: Structure for pricer option and version information passed to `LTOPN212` (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-RECORD-FROM-USER`: Large structure holding provider information passed to `LTOPN212` (NPI, provider number, dates, codes, indices, etc.).
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) for CBSA and MSA wage index tables passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`.

*   **Linkage Section:** None.

---

#### Program: LTOPN212 (from L1_FunctionalSpecification.md)

This program loads various tables and calls the payment calculation driver.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file with provider records (`PROV-REC`, 240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file with CBSA wage index data (`CBSAX-REC`).
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file with IPPS CBSA wage index data (`F-IPPS-CBSA-REC`).
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file with MSA wage index data (`MSAX-REC`).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `OPN-VERSION`: A 5-character field for the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of the called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating if tables are loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field for end-of-file indication.
    *   `W-PROV-NEW-HOLD`: Structure to hold provider records (mirrors `PROV-RECORD-FROM-USER` from LTMGR212).
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields for file status.
    *   `CBSA-WI-TABLE`: Table to hold CBSA wage index data (up to 10000 entries).
    *   `IPPS-CBSA-WI-TABLE`: Table to hold IPPS CBSA wage index data (up to 10000 entries).
    *   `MSA-WI-TABLE`: Table to hold MSA wage index data (up to 4000 entries).
    *   `WORK-COUNTERS`: Structure for record counts from each file.
    *   `PROV-TABLE`: Table to hold provider data (up to 2400 entries), divided into `PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`.
    *   `PROV-NEW-HOLD`: Structure to hold provider records passed to `LTDRV212` (mirrors `PROV-RECORD-FROM-USER` from LTMGR212).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`.
    *   `PPS-DATA-ALL`: PPS data passed to and returned from `LTMGR212`.
    *   `PPS-CBSA`: CBSA code passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Payment data passed to and returned from `LTMGR212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTMGR212`.
    *   `PROV-RECORD-FROM-USER`: Provider-specific information passed from `LTMGR212`.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212 for wage index tables.

---

#### Program: LTDRV212 (from L1_FunctionalSpecification.md)

This program selects the appropriate wage index and calls the calculation modules.

*   **Files Accessed:** None directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal (comment).
    *   `DRV-VERSION`: A 5-character field for the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals for names of called programs.
    *   `WS-9S`: An 8-character numeric literal of all 9s, for date comparison.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields for FY2020 wage index constants.
    *   `RUFL-ADJ-TABLE`: Table of rural floor adjustment factors (from COPY RUFL200).
    *   `HOLD-RUFL-DATA`: Structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: Index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold calculated fiscal year dates.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from LTOPN212 tables.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: Field for Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: Field for supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: Structure holding provider records passed from `LTOPN212` (mirrors `PROV-NEW-HOLD` in LTOPN212).
    *   `BILL-DATA-FY03-FY15`: Structure for billing data for older fiscal years.
    *   `BILL-NEW-DATA`: Structure holding billing data for FY2015 and later (mirrors `BILL-NEW-DATA` in LTMGR212 and LTOPN212).
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: PPS data passed to and returned from `LTOPN212`.
    *   `PPS-CBSA`: CBSA code.
    *   `PPS-PAYMENT-DATA`: Payment data passed to and returned from `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212.

---

#### COPY Member: RUFL200 (from L1_FunctionalSpecification.md)

This is a copybook, not a program, defining data structures.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Not applicable.

*   **Linkage Section:** Not applicable.

*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: Main structure containing `RUFL-TAB` (rural floor adjustment factors table). Each entry includes `RUFL-CBSA`, `RUFL-EFF-DATE`, and `RUFL-WI3`. The table has 459 entries.

---

#### Program: IPDRG160 (from L2_FunctionalSpecification.md)

Likely accesses a DRG table file.

*   **Files Accessed:** Inferred: DRG table file (read-only).

*   **Working-Storage Section:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for DRG table ('20151001').
    *   `PPS-DRG-TABLE`: Group item for DRG table data.
        *   `WK-DRG-DATA`: Temporary holding area for DRG data.
        *   `WK-DRG-DATA2 REDEFINES WK-DRG-DATA`: Structured access to DRG data.
            *   `DRG-TAB` (OCCURS 758): Table of DRG data records.
                *   `DRG-DATA-TAB`: Single DRG record structure including:
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code.
                    *   `FILLER1` (PIC X(01)).
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)).
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean of average length of stay.
                    *   `FILLER3` (PIC X(05)).
                    *   `DRG-LOW` (PIC X(01)): Indicator.
                    *   `FILLER5` (PIC X(01)).
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic mean of average length of stay.
                    *   `FILLER6` (PIC X(02)).
                    *   `DRG-PAC` (PIC X(01)): Indicator.
                    *   `FILLER7` (PIC X(01)).
                    *   `DRG-SPPAC` (PIC X(01)): Indicator.
                    *   `FILLER8` (PIC X(02)).
                    *   `DRG-DESC` (PIC X(26)): DRG description.

*   **Linkage Section:** None.

---

#### Program: IPDRG170 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for 2016 data.

*   **Files Accessed:** Inferred: DRG table file (read-only) for 2016.

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757`. DRG data specific to 2016.

*   **Linkage Section:** None.

---

#### Program: IPDRG181 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for 2017 data.

*   **Files Accessed:** Inferred: DRG table file (read-only) for 2017.

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20171001' and `DRG-TAB` having `OCCURS 754`. DRG data specific to 2017.

*   **Linkage Section:** None.

---

#### Program: IPDRG190 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for 2018 data.

*   **Files Accessed:** Inferred: DRG table file (read-only) for 2018.

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20181001' and `DRG-TAB` having `OCCURS 761`. DRG data specific to 2018.

*   **Linkage Section:** None.

---

#### Program: IPDRG200 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for 2019 data.

*   **Files Accessed:** Inferred: DRG table file (read-only) for 2019.

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20191001' and `DRG-TAB` having `OCCURS 761`. DRG data specific to 2019.

*   **Linkage Section:** None.

---

#### Program: IPDRG211 (from L2_FunctionalSpecification.md)

Similar to IPDRG160, but for 2020 data.

*   **Files Accessed:** Inferred: DRG table file (read-only) for 2020.

*   **Working-Storage Section:** Structurally identical to IPDRG160, with `WK-DRGX-EFF-DATE` set to '20201001' and `DRG-TAB` having `OCCURS 767`. DRG data specific to 2020.

*   **Linkage Section:** None.

---

#### Program: LTCAL162 (from L2_FunctionalSpecification.md)

Performs payment calculations based on DRG and wage index data.

*   **Files Accessed:**
    *   Provider-specific file (PSF): Contains provider info (wage indices, cost-to-charge ratios).
    *   CBSA wage index file.
    *   LTCH DRG table file (via `LTDRG160` COPY).
    *   IPPS DRG table file (via `IPDRG160` COPY).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Descriptive filler.
    *   `CAL-VERSION`: Program version number ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in calculations.
    *   `PROGRAM-FLAGS`: Flags controlling program flow.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate payment calculation results.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data from DRG tables.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Input bill data from `LTDRV`.
    *   `PPS-DATA-ALL`: Output PPS calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches indicating pricer option and driver program versions.
    *   `PROV-NEW-HOLD`: Input provider-specific data from `LTDRV`.
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

#### Program: LTCAL170 (from L2_FunctionalSpecification.md)

Similar to LTCAL162, but for FY17.

*   **Files Accessed:** PSF, CBSA wage index file, `LTDRG170`, `IPDRG170`.

*   **Working-Storage Section:** Similar to LTCAL162, with `CAL-VERSION` as 'V17.0'. Constants and rates updated for FY17.

*   **Linkage Section:** Identical to LTCAL162, with the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

#### Program: LTCAL183 (from L2_FunctionalSpecification.md)

Similar to LTCAL170, but for FY18.

*   **Files Accessed:** PSF, CBSA wage index file, `LTDRG181`, `IPDRG181`.

*   **Working-Storage Section:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3'. Variables related to Subclause II removed.

*   **Linkage Section:** Similar to LTCAL170, with removal of Subclause II fields.

---

#### Program: LTCAL190 (from L2_FunctionalSpecification.md)

Similar to LTCAL183, but for FY19.

*   **Files Accessed:** PSF, CBSA wage index file, `LTDRG190`, `IPDRG190`.

*   **Working-Storage Section:** Similar to LTCAL183, with `CAL-VERSION` as 'V19.0'.

*   **Linkage Section:** Similar to LTCAL183.

---

#### Program: LTCAL202 (from L2_FunctionalSpecification.md)

Similar to LTCAL190, but for FY20, including COVID-19 processing.

*   **Files Accessed:** PSF, CBSA wage index file, `LTDRG200`, `IPDRG200`.

*   **Working-Storage Section:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2'. Includes additions for COVID-19.

*   **Linkage Section:** Similar to previous LTCAL programs, with addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA`.

---

#### Program: LTCAL212 (from L2_FunctionalSpecification.md)

Similar to LTCAL202, but for FY21.

*   **Files Accessed:** PSF, CBSA wage index file, `LTDRG210`, `IPDRG211`.

*   **Working-Storage Section:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2'. Includes changes for CR11707 and CR11879. Adds `P-SUPP-WI-IND` and `P-SUPP-WI` in `PROV-NEW-HOLD`.

*   **Linkage Section:** Similar to LTCAL202.

---

#### COPY Member: LTDRG160 (from L2_FunctionalSpecification.md)

Defines the LTCH DRG table for FY15.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748):
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG170 (from L2_FunctionalSpecification.md)

Defines the LTCH DRG table for FY16.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 747`.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG181 (from L2_FunctionalSpecification.md)

Defines the LTCH DRG table for FY18.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 744`.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG190 (from L2_FunctionalSpecification.md)

Defines the LTCH DRG table for FY19.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 751`.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG210 (from L2_FunctionalSpecification.md)

Defines the LTCH DRG table for FY21.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Structurally similar to LTDRG160, with `WWM-ENTRY` having `OCCURS 754`.

*   **Linkage Section:** None.

---

#### Program: IPDRG104 (from L4_FunctionalSpecification.md)

Defines an IPPS DRG table.

*   **Files Accessed:** Implicitly via `COPY IPDRG104`.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds DRG data in packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

#### Program: IPDRG110 (from L4_FunctionalSpecification.md)

Defines an IPPS DRG table, similar to IPDRG104.

*   **Files Accessed:** Implicitly via `COPY IPDRG110`.

*   **Working-Storage Section:** Structurally identical to IPDRG104.

*   **Linkage Section:** None.

---

#### Program: IPDRG123 (from L4_FunctionalSpecification.md)

Defines an IPPS DRG table, similar to IPDRG104.

*   **Files Accessed:** Implicitly via `COPY IPDRG123`.

*   **Working-Storage Section:** Structurally identical to IPDRG104.

*   **Linkage Section:** None.

---

#### Program: IRFBN102 (from L4_FunctionalSpecification.md)

Defines a table for state-specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** Implicitly via `COPY IRFBN102`.

*   **Working-Storage Section:**
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Less structured RFBN data.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `WK-SSRFBN-REASON-ALL`: Details per state.
                    *   `WK-SSRFBN-STATE PIC 99`: State code.
                    *   `FILLER PIC XX`.
                    *   `WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `FILLER PIC XX`.
                    *   `WK-SSRFBN-CODE2 PIC 99`.
                    *   `FILLER PIC X`.
                    *   `WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `WK-SSRFBN-REST PIC X(22)`: Remaining data.
    *   `MES-ADD-PROV`...`MES-TOT-PAY`: Message and payment holding areas.
    *   `MES-SSRFBN`: Holds a single RFBN record.

*   **Linkage Section:** None.

---

#### Program: IRFBN105 (from L4_FunctionalSpecification.md)

Defines a table for updated state-specific RFBNs.

*   **Files Accessed:** Implicitly via `COPY IRFBN105`.

*   **Working-Storage Section:** Structurally identical to IRFBN102.

*   **Linkage Section:** None.

---

#### Program: LTCAL103 (from L4_FunctionalSpecification.md)

Performs PPS calculations using DRG and RFBN data.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG100`, `IPDRG104`, `IRFBN102`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V10.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates (`FED-FY-BEGIN-03` to `FED-FY-BEGIN-07`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results (LOS, days, rates, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (`PPS-RTC`, `PPS-CHRG-THRESHOLD`, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version switch (`PRICER-OPTION-SW`, `PPS-VERSIONS`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, MSA data, rates, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (CBSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record (CBSA, size, effective date, wage indices).
    *   `W-DRG-FILLS`: Holds DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, DRG, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.

---

#### Program: LTCAL105 (from L4_FunctionalSpecification.md)

Similar to LTCAL103, but uses `IRFBN105`.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG100`, `IPDRG104`, `IRFBN105`.

*   **Working-Storage Section:** Similar to LTCAL103, with `CAL-VERSION` as 'V10.5' and use of `IRFBN105`.

*   **Linkage Section:** Identical to LTCAL103.

---

#### Program: LTCAL111 (from L4_FunctionalSpecification.md)

Similar to LTCAL103, but uses `LTDRG110` and `IPDRG110`, and does not include RFBNs.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG110`, `IPDRG110`. `IRFBN***` copybook is commented out.

*   **Working-Storage Section:** Similar to LTCAL103, with `CAL-VERSION` as 'V11.1' and adjusted copybooks.

*   **Linkage Section:** Identical to LTCAL103.

---

#### Program: LTCAL123 (from L4_FunctionalSpecification.md)

Similar to LTCAL111, but uses `LTDRG123` and `IPDRG123`.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG123`, `IPDRG123`. RFBN copybook is commented out.

*   **Working-Storage Section:** Similar to LTCAL111, with `CAL-VERSION` as 'V12.3' and adjusted copybooks.

*   **Linkage Section:** Identical to LTCAL103.

---

#### COPY Member: LTDRG100 (from L4_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG110 (from L4_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG123 (from L4_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.

*   **Linkage Section:** None.

---

#### Program: IPDRG080 (from L5_FunctionalSpecification.md)

Defines a DRG table for 2007 data.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds DRG data in packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date ('20071001').
                *   `DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

#### Program: IPDRG090 (from L5_FunctionalSpecification.md)

Defines a DRG table for 2008 data.

*   **Files Accessed:** None.

*   **Working-Storage Section:** Similar structure to IPDRG080, with `DRGX-EFF-DATE` as '20081001'.

*   **Linkage Section:** None.

---

#### Program: IRFBN091 (from L5_FunctionalSpecification.md)

Defines a table for state-specific RFBNs.

*   **Files Accessed:** None.

*   **Working-Storage Section:**
    *   `MES-ADD-PROV`...`MES-TOT-PAY`: Message and payment holding areas.
    *   `MES-SSRFBN`: Holds a single RFBN record.
    *   `PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `WK-SSRFBN-DATA`: Less structured RFBN data.
        *   `WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Structured access.
            *   `SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs.
                *   `WK-SSRFBN-REASON-ALL`: Details per state (State Code, Rate, State Name, etc.).

*   **Linkage Section:** None.

---

#### Program: LTCAL087 (from L5_FunctionalSpecification.md)

Performs PPS calculations using DRG data.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG086` and `IPDRG080`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V08.7').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `COPY LTDRG086`: Includes LTCH DRG table data.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results (LOS, days, rates, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version switch.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, MSA data, rates, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: LTCH wage index record (MSA, effective date, wage indices).
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (NPI, provider number, DRG, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

---

#### Program: LTCAL091 (from L5_FunctionalSpecification.md)

Similar to LTCAL087, but for FY09.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG086` and `IPDRG080`.

*   **Working-Storage Section:** Similar to LTCAL087, with `CAL-VERSION` as 'V09.1'.

*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL094 (from L5_FunctionalSpecification.md)

Similar to LTCAL091, but for FY09, updated data.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG093` and `IPDRG090`.

*   **Working-Storage Section:** Similar to LTCAL091, with `CAL-VERSION` as 'V09.4'. Adds `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.

*   **Linkage Section:** Identical to LTCAL087.

---

#### Program: LTCAL095 (from L5_FunctionalSpecification.md)

Similar to LTCAL094, but for FY09, updated data.

*   **Files Accessed:** Implicitly via `COPY` statements for `LTDRG095` and `IPDRG090`.

*   **Working-Storage Section:** Similar to LTCAL094, with `CAL-VERSION` as 'V09.5'.

*   **Linkage Section:** Identical to LTCAL087.

---

#### COPY Member: LTDRG080 (from L5_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS, IPPS threshold).

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG086 (from L5_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Similar structure to LTDRG080, but with 735 occurrences of `WWM-ENTRY`.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG093 (from L5_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Similar structure to LTDRG086, with different data.

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG095 (from L5_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:** Similar structure to LTDRG093, with different data.

*   **Linkage Section:** None.

---

#### Program: IPDRG063 (from L6_FunctionalSpecification.md)

Defines an IPPS DRG table.

*   **Files Accessed:** None explicitly defined. Relies on data defined in `IPDRG063` copybook.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds DRG data in packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

#### Program: IPDRG071 (from L6_FunctionalSpecification.md)

Defines an IPPS DRG table.

*   **Files Accessed:** None explicitly defined. Relies on data defined in `IPDRG071` copybook.

*   **Working-Storage Section:**
    *   `DRG-TABLE`: DRG data table.
        *   `D-TAB`: Holds DRG data in packed format.
        *   `DRGX-TAB REDEFINES D-TAB`: Structured access.
            *   `DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period.
                *   `DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `DRG-DATA OCCURS 580 INDEXED BY DX6`: DRG data for the period.
                    *   `DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.

*   **Linkage Section:** None.

---

#### Program: LTCAL064 (from L6_FunctionalSpecification.md)

Performs PPS calculations.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table (`WWM-ENTRY`).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results.
    *   Various numeric and alphanumeric variables for PPS calculations (LOS, days, rates, payments, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Flags indicating passed tables.
    *   `PROV-NEW-HOLD`: Holds provider data.
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed from calling program (provider info, DRG, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results returned to calling program (return codes, payment amounts, etc.).
    *   `PROV-NEW-HOLD`: Provider data passed to the program.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program.

---

#### Program: LTCAL072 (from L6_FunctionalSpecification.md)

Performs PPS calculations, including short-stay outlier logic.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062` and `COPY IPDRG063`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version.
    *   `PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes LTCH DRG table.
    *   `COPY IPDRG063`: Includes IPPS DRG table.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results (expanded for short-stay outlier calculations).
    *   Numerous variables for PPS calculations, payment amounts, COLA, wage indices, etc.
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

---

#### Program: LTCAL075 & LTCAL080 (from L6_FunctionalSpecification.md)

These programs are similar to LTCAL072, with incremental changes in constants, rates, and potentially additional variables for newer versions. The basic structure and copybook inclusions remain consistent.

---

#### COPY Member: LTDRG062 (from L6_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG075 & LTDRG080 (from L6_FunctionalSpecification.md)

These copybooks define DRG tables with updated data, potentially including additional fields like `WWM-IPTHRESH` in LTDRG080. The number of `WWM-ENTRY` occurrences may also vary.

---

#### Program: LTCAL043 (from L7_FunctionalSpecification.md)

Performs PPS calculations.

*   **Files Accessed:** Implicitly via `COPY LTDRG041`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('C04.3').
    *   `LTDRG041`: Includes `W-DRG-TABLE` (DRG code, relative weight, average LOS).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, days, SSOT, blend amounts, etc.).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to/from calling program (NPI, provider number, DRG, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS calculation results (return code, thresholds, MSA, Wage Index, payments, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (MSA, effective date, wage indices).

---

#### Program: LTCAL058 (from L7_FunctionalSpecification.md)

Similar to LTCAL043, but for FY05.

*   **Files Accessed:** Implicitly via `COPY LTDRG041`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V05.8').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year dates.
    *   `LTDRG041`: Includes LTCH DRG table.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

---

#### Program: LTCAL059 (from L7_FunctionalSpecification.md)

Similar to LTCAL058, but for FY05, using `LTDRG057`.

*   **Files Accessed:** Implicitly via `COPY LTDRG057`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Includes LTCH DRG table (`WWM-ENTRY` occurs 512 times).
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.

---

#### Program: LTCAL063 (from L7_FunctionalSpecification.md)

Similar to LTCAL059, but for FY06, using `LTDRG057`.

*   **Files Accessed:** Implicitly via `COPY LTDRG057`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Includes LTCH DRG table.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA`: CBSA code.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information.
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data (adds `P-NEW-SPECIAL-PAY-IND`, `P-NEW-SPECIAL-WAGE-INDEX`).
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data (uses CBSA instead of MSA).

---

#### COPY Member: LTDRG041 (from L7_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 510 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:** None.

---

#### COPY Member: LTDRG057 (from L7_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 512 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:** None.

---

#### Program: LTCAL032 (from L8_FunctionalSpecification.md)

Performs PPS calculations.

*   **Files Accessed:** None explicitly defined. Relies on `COPY LTDRG031`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Comment.
    *   `CAL-VERSION`: Program version ('C03.2').
    *   `LTDRG031`: Includes `W-DRG-TABLE` (DRG code, relative weight, average LOS).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, days, SSOT, blend amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Pricer option and version information.
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, provider number, dates, waiver code, MSA data, rates, etc.).
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data (MSA, effective date, wage indices).

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill data passed to/from subroutine (NPI, provider number, DRG, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: Calculated PPS data returned by subroutine (RTC, thresholds, MSA, Wage Index, payments, etc.).

---

#### Program: LTCAL042 (from L8_FunctionalSpecification.md)

Similar to LTCAL032, but for FY04, with updated values.

*   **Files Accessed:** None explicitly defined. Relies on `COPY LTDRG031`.

*   **Working-Storage Section:**
    *   Similar to LTCAL032, with `CAL-VERSION` as 'C04.2'.
    *   Updated values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
    *   Adds `H-LOS-RATIO` to `HOLD-PPS-COMPONENTS`.

*   **Linkage Section:** Identical to LTCAL032.

---

#### COPY Member: LTDRG031 (from L8_FunctionalSpecification.md)

Defines the LTCH DRG table.

*   **Files Accessed:** None (as it's a copybook).

*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Contains LTCH DRG data in packed format.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Structured access.
        *   `WWM-ENTRY OCCURS 44 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table (DRG code, relative weight, average LOS).

*   **Linkage Section:** None.

---

### Overall Program Flow Summary

The programs generally operate in the following sequence:

1.  **LTMGR212:** Initiates the process by reading billing records from `BILLFILE`. It prepares the data and calls `LTOPN212` for payment calculations. The results are then formatted and written to `PRTOPER`.
2.  **LTOPN212:** Loads necessary tables (provider, wage index) from various input files based on the bill's discharge date and pricing options. It then calls `LTDRV212` to perform the core payment calculations.
3.  **LTDRV212:** Selects the appropriate wage index based on discharge date and provider information. It then calls specific `LTCAL` modules (e.g., `LTCAL032`, `LTCAL162`, etc.) based on the fiscal year to perform the actual payment calculations.
4.  **LTCALxxx Modules:** These modules perform the detailed PPS calculations. They utilize DRG tables (from `LTDRGxxx` or `IPDRGxxx` copybooks), wage index data, provider-specific data, and other regulatory parameters to determine payment amounts. Some `LTCAL` modules might further call other calculation sub-modules (e.g., `LTCAL032` calls `LTCALxxx` modules).

The extensive use of version numbers (e.g., `PPMGR-VERSION`, `OPN-VERSION`, `DRV-VERSION`, `CAL-VERSION`) and dated copybooks (`IPDRG160`, `LTDRG062`, etc.) clearly indicates a system that has evolved significantly over many fiscal years to accommodate changes in payment methodologies and data requirements. The presence of numerous filler fields and literal values suggests a long development history with potential for optimization.