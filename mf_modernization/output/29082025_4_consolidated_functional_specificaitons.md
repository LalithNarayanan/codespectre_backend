## Data Definition and File Handling

This document consolidates and analyzes the "Data Definition and File Handling" sections extracted from multiple functional specification documents (L1, L2, L4, L5, L6, L7, and L8). It provides a detailed overview of the COBOL programs, their accessed files (where explicitly mentioned or implied), working-storage data structures, and linkage sections.

The analysis reveals a suite of COBOL programs designed to process healthcare claims, likely related to Prospective Payment Systems (PPS), with a particular focus on Long-Term Care (LTCH) and Inpatient Prospective Payment Systems (IPPS). The programs demonstrate a history of updates and versioning over several years, indicating a complex and evolving system.

---

### Program: LTMGR212

This program acts as a manager, preparing billing data and orchestrating the payment calculation process by calling other programs.

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format is defined by `BILL-REC` (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for printing prospective payment reports. Record format is defined by `PRTOPER-LINE` (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal, likely a comment.
    *   `PPMGR-VERSION`: A 5-character field storing the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of the called program.
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field counting lines written to the `PRTOPER` file, initialized to 65.
    *   `UT1-STAT`: A 2-character field storing the file status of `BILLFILE`.
        *   `UT1-STAT1`: First character of the file status.
        *   `UT1-STAT2`: Second character of the file status.
    *   `OPR-STAT`: A 2-character field storing the file status of `PRTOPER`.
        *   `OPR-STAT1`: First character of the file status.
        *   `OPR-STAT2`: Second character of the file status.
    *   `BILL-WORK`: A structure holding the input bill record from `BILLFILE`. Includes fields like provider NPI, patient status, DRG code, length of stay (LOS), coverage days, cost report days, discharge date, charges, special pay indicator, review code, and tables for diagnosis and procedure codes.
    *   `PPS-DATA-ALL`: A structure containing data returned from the `LTOPN212` program, including payment calculation results, wage indices, and other relevant data.
    *   `PPS-CBSA`: A 5-character field for CBSA code (Core Based Statistical Area).
    *   `PPS-PAYMENT-DATA`: A structure holding payment amounts calculated by `LTOPN212`, including site-neutral cost and IPPS payments, and standard full and short stay payments.
    *   `BILL-NEW-DATA`: A structure mirroring `BILL-WORK`, used for passing data to the called program.
    *   `PRICER-OPT-VERS-SW`: A structure to hold the pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: A single character indicating the pricing option.
        *   `PPS-VERSIONS`: A structure containing the version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: A large structure (holding provider information) that can be passed to `LTOPN212`. It includes NPI, provider number, various dates, codes, indices, and other provider-specific data.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) to hold CBSA and MSA wage index tables that can be passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`, containing formatted data for header and detail lines.

*   **Linkage Section:** LTMGR212 does not have a Linkage Section.

---

### Program: LTOPN212

This program loads and processes various tables required for payment calculations, then calls another program for detailed calculations.

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout defined as `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout defined as `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout defined as `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout defined as `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `OPN-VERSION`: A 5-character field storing the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of the called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating whether tables have been loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch.
    *   `W-PROV-NEW-HOLD`: A structure to hold the provider record, either passed in or retrieved from `PROV-FILE`. Mirrors `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields storing file status information for each input file.
    *   `CBSA-WI-TABLE`: A table to hold CBSA wage index data, loaded from `CBSAX-FILE`. It has up to 10000 entries, indexed by `CU1` and `CU2`.
    *   `IPPS-CBSA-WI-TABLE`: A table to hold IPPS CBSA wage index data, loaded from `IPPS-CBSAX-FILE`. It has up to 10000 entries, indexed by `MA1`, `MA2`, and `MA3`.
    *   `MSA-WI-TABLE`: A table to hold MSA wage index data, loaded from `MSAX-FILE`. It has up to 4000 entries, indexed by `MU1` and `MU2`.
    *   `WORK-COUNTERS`: A structure containing counters for the number of records read from each file.
    *   `PROV-TABLE`: A table (up to 2400 entries) to hold provider data read from `PROV-FILE`. Divided into three parts (`PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`), indexed by `PX1`, `PD2`, and `PD3`.
    *   `PROV-NEW-HOLD`: A structure to hold the provider record to be passed to `LTDRV212`. Mirrors `PROV-RECORD-FROM-USER` from LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTMGR212`, mirroring the `BILL-NEW-DATA` structure in LTMGR212.
    *   `PPS-DATA-ALL`: Structure to hold PPS data passed from and returned to `LTMGR212`, mirroring the `PPS-DATA-ALL` structure in LTMGR212.
    *   `PPS-CBSA`: A 5-character field for the CBSA code, passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: Structure to hold payment data passed from and returned to `LTMGR212`, mirroring the `PPS-PAYMENT-DATA` structure in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: Structure holding the pricer option and version information passed from `LTMGR212`, mirroring the `PRICER-OPT-VERS-SW` structure in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: Structure containing provider-specific information passed from `LTMGR212`, mirroring the `PROV-RECORD-FROM-USER` structure in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, to hold wage index tables.

---

### Program: LTDRV212

This program acts as a driver, selecting the correct wage index and calling the appropriate calculation module based on fiscal year and provider data.

*   **Files Accessed:** LTDRV212 does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, likely a comment.
    *   `DRV-VERSION`: A 5-character field storing the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of various called programs (likely different versions of the same pricing module).
    *   `WS-9S`: An 8-character numeric literal with all 9s, used for date comparisons.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields holding wage index related constants for FY2020.
    *   `RUFL-ADJ-TABLE`: A table (defined in COPY RUFL200) containing rural floor factors for various CBSAs.
    *   `HOLD-RUFL-DATA`: A structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: An index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold the fiscal year begin and end dates calculated from the bill's discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from the tables in LTOPN212.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: A field to hold the Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: A field to hold the supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: A structure holding the provider record passed from `LTOPN212`. Mirrors the `PROV-NEW-HOLD` structure in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: A structure to hold billing data for older fiscal years (before Jan 2015).
    *   `BILL-NEW-DATA`: A structure holding billing data for FY2015 and later, mirroring the `BILL-NEW-DATA` structure in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: Structure to hold PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: Structure for payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: Structure holding the pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: Structure containing provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

---

### COPY Member: RUFL200

This is a COPY member, not an executable program, defining data structures for rural floor adjustment factors.

*   **Files Accessed:** Not applicable, as it's a data definition.
*   **Working-Storage Section:** Not applicable.
*   **Linkage Section:** Not applicable.
*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: The main structure, containing a table `RUFL-TAB` of rural floor adjustment factors. Each entry includes:
        *   `RUFL-CBSA`: CBSA code.
        *   `RUFL-EFF-DATE`: Effective date.
        *   `RUFL-WI3`: Wage index.
        *   The table has 459 entries.

---

### Program: IPDRG160

This program likely accesses a DRG table file for a specific fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only). No explicit file name mentioned.
*   **WORKING-STORAGE SECTION:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table (e.g., '20151001').
    *   `PPS-DRG-TABLE`: A group item containing the DRG table data.
        *   `WK-DRG-DATA`: A group item for temporary holding of DRG data.
        *   `WK-DRG-DATA2` (REDEFINES WK-DRG-DATA): A redefinition allowing structured table access.
            *   `DRG-TAB` (OCCURS 758): A table of DRG data records.
                *   `DRG-DATA-TAB`: A group item representing a single DRG record with fields:
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
*   **LINKAGE SECTION:** Not present in the provided code.

---

### Program: IPDRG170

Similar to IPDRG160, but for the 2016 fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only) for 2016.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20161001' and `DRG-TAB` has `OCCURS 757`. DRG data is specific to 2016.
*   **LINKAGE SECTION:** Not present.

---

### Program: IPDRG181

Similar to IPDRG160, but for the 2017 fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only) for 2017.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20171001' and `DRG-TAB` has `OCCURS 754`. DRG data is specific to 2017.
*   **LINKAGE SECTION:** Not present.

---

### Program: IPDRG190

Similar to IPDRG160, but for the 2018 fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only) for 2018.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20181001' and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2018.
*   **LINKAGE SECTION:** Not present.

---

### Program: IPDRG200

Similar to IPDRG160, but for the 2019 fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only) for 2019.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20191001' and `DRG-TAB` has `OCCURS 761`. DRG data is specific to 2019, noting the addition of DRG 319 and 320.
*   **LINKAGE SECTION:** Not present.

---

### Program: IPDRG211

Similar to IPDRG160, but for the 2020 fiscal year.

*   **Files Accessed:** Likely accesses a DRG table file (read-only) for 2020.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but `WK-DRGX-EFF-DATE` is '20201001' and `DRG-TAB` has `OCCURS 767`. DRG data is specific to 2020, noting changes in some DRG descriptions.
*   **LINKAGE SECTION:** Not present.

---

### Program: LTCAL162

This program performs payment calculations, likely using DRG and wage index data.

*   **Files Accessed:** Likely accesses a provider-specific file (PSF), a CBSA wage index file, and LTCH DRG (`LTDRG160`) and IPPS DRG (`IPDRG160`) tables via COPY statements. These are read-only.
*   **WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF`: A descriptive filler.
    *   `CAL-VERSION`: Program version number ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in the program.
    *   `PROGRAM-FLAGS`: Flags to control program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for payment.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold data copied from DRG tables.
*   **LINKAGE SECTION:**
    *   `BILL-NEW-DATA`: Input bill data from a calling program (likely `LTDRV`).
    *   `PPS-DATA-ALL`: Output PPS (Prospective Payment System) calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches indicating the versions of the pricer option and other driver programs.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

---

### Program: LTCAL170

This program performs payment calculations, similar to LTCAL162, but for the FY17.

*   **Files Accessed:** Likely accesses a PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG170` and `IPDRG170`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL162, with `CAL-VERSION` set to 'V17.0'. Constants and rates are updated for FY17.
*   **LINKAGE SECTION:** Identical to LTCAL162's Linkage Section, except for the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

---

### Program: LTCAL183

This program performs payment calculations, similar to LTCAL170, but for the FY18.

*   **Files Accessed:** Likely accesses a PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG181` and `IPDRG181`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Note that some variables related to Subclause II have been removed.
*   **LINKAGE SECTION:** The linkage section is similar to LTCAL170, with the removal of fields related to Subclause II.

---

### Program: LTCAL190

This program performs payment calculations, similar to LTCAL183, but for the FY19.

*   **Files Accessed:** Likely accesses a PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG190` and `IPDRG190`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **LINKAGE SECTION:** The linkage section is similar to LTCAL183.

---

### Program: LTCAL202

This program performs payment calculations, similar to LTCAL190, but for the FY20, including COVID-19 processing.

*   **Files Accessed:** Similar to previous LTCAL programs, accessing a PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG200` and `IPDRG200`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.
*   **LINKAGE SECTION:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` to handle the Disproportionate Patient Percentage (DPP) adjustment.

---

### Program: LTCAL212

This program performs payment calculations, similar to LTCAL202, but for the FY21.

*   **Files Accessed:** Similar to LTCAL202, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (`LTDRG210` and `IPDRG211`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **LINKAGE SECTION:** Similar to LTCAL202, with no additional fields.

---

### COPY Member: LTDRG160

This COPY member defines the structure for the LTCH DRG table for FY15.

*   **Files Accessed:** Not applicable; it's a data definition.
*   **WORKING-STORAGE SECTION:** Defines the structure of the LTCH DRG table.
    *   `W-DRG-FILLS`: Contains the DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES W-DRG-FILLS): A table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): A table entry containing:
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **LINKAGE SECTION:** Not applicable.

---

### COPY Member: LTDRG170

This COPY member defines the structure for the LTCH DRG table for FY16.

*   **Files Accessed:** Not applicable.
*   **WORKING-STORAGE SECTION:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747` times.
*   **LINKAGE SECTION:** Not applicable.

---

### COPY Member: LTDRG181

This COPY member defines the structure for the LTCH DRG table for FY18.

*   **Files Accessed:** Not applicable.
*   **WORKING-STORAGE SECTION:** Structurally similar to LTDRG160 and LTDRG170, with `WWM-ENTRY` having `OCCURS 744` times.
*   **LINKAGE SECTION:** Not applicable.

---

### COPY Member: LTDRG190

This COPY member defines the structure for the LTCH DRG table for FY19.

*   **Files Accessed:** Not applicable.
*   **WORKING-STORAGE SECTION:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751` times.
*   **LINKAGE SECTION:** Not applicable.

---

### COPY Member: LTDRG210

This COPY member defines the structure for the LTCH DRG table for FY21.

*   **Files Accessed:** Not applicable.
*   **WORKING-STORAGE SECTION:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754` times.
*   **LINKAGE SECTION:** Not applicable.

---

### Program: IPDRG104

This program appears to define a DRG table within WORKING-STORAGE.

*   **Files Accessed:** Uses a `COPY IPDRG104` statement, implying data from a file named `IPDRG104` containing a DRG table. No explicit file access statements.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: A table containing DRG data.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: A single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the DRG data.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed (for outlier calculations).
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG110

Similar to IPDRG104, defining a DRG table for a different fiscal year.

*   **Files Accessed:** Uses a `COPY IPDRG110` statement, referencing a file containing DRG data.
*   **WORKING-STORAGE SECTION:** Structurally identical to `IPDRG104`, with `DRG-DATA OCCURS 1000`.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG123

Similar to IPDRG104, defining a DRG table for a different fiscal year.

*   **Files Accessed:** Uses a `COPY IPDRG123` statement, indicating inclusion of DRG data from another file.
*   **WORKING-STORAGE SECTION:** Structurally similar to `IPDRG104` and `IPDRG110`, with `DRG-DATA OCCURS 1000`.
*   **LINKAGE SECTION:** None.

---

### Program: IRFBN102

This program likely defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** The `COPY IRFBN102` statement suggests data from a file containing RFBNs.
*   **WORKING-STORAGE SECTION:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries, sorted by state code).
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
*   **LINKAGE SECTION:** None.

---

### Program: IRFBN105

Similar to IRFBN102, but likely for an updated RFBN data set.

*   **Files Accessed:** Uses a `COPY IRFBN105` statement, referencing a file presumably containing updated RFBN data.
*   **WORKING-STORAGE SECTION:** Structurally identical to `IRFBN102`.
*   **LINKAGE SECTION:** None.

---

### Program: LTCAL103

This program performs payment calculations, incorporating DRG and RFBN data via COPY statements.

*   **Files Accessed:** Uses `COPY` statements to include data from:
    *   `LTDRG100`: Likely contains an LTC DRG table.
    *   `IPDRG104`: Contains IPPS DRG data.
    *   `IRFBN102`: Contains IPPS state-specific RFBNs.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103      - W O R K I N G   S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components. Contains numerous numeric variables for various aspects of payment calculation (LOS, days, rates, shares, adjustments, etc.).
    *   `01 PPS-DATA-ALL`: Holds the final PPS calculation results. Includes `PPS-RTC` (return code), `PPS-CHRG-THRESHOLD` (charge threshold), and many other numeric fields for PPS data elements.
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data. Contains nested groups for NPI, provider number, dates, waiver code, intern number, provider type, census division, MSA data, and various other parameters.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record.
        *   `05 W-CBSA PIC X(5)`: CBSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective date.
        *   `05 W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record. Contains CBSA code, size indicator, effective date, and wage indices.
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format (redefined below).
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program. Contains provider NPI, provider number, patient status, DRG code, LOS, covered days, lifetime reserve days, discharge date, covered charges, special pay indicator, and filler.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

---

### Program: LTCAL105

This program performs payment calculations, similar to LTCAL103, but uses updated copybooks.

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG100`: LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **WORKING-STORAGE SECTION:** Very similar to `LTCAL103`, with the main differences being the version number (`CAL-VERSION` as 'V10.5') and the use of `IRFBN105` instead of `IRFBN102`. Minor numeric constant adjustments are also present.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

---

### Program: LTCAL111

This program performs payment calculations, similar to LTCAL105, but without state-specific RFBNs.

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG110`: LTC DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   `IRFBN091` (commented out): Indicates no state-specific RFBN table is used in this version.
*   **WORKING-STORAGE SECTION:** Similar to `LTCAL103` and `LTCAL105`, with the version number updated to `V11.1` and copybooks adjusted.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

---

### Program: LTCAL123

This program performs payment calculations, similar to LTCAL111, but using different DRG tables.

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG123`: LTC DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs, similar to LTCAL111.
*   **WORKING-STORAGE SECTION:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table is used.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

---

### Program: LTDRG100

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None explicitly accessed. Data is defined internally.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed, less structured format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG110

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None explicitly accessed.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG123

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None explicitly accessed.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG080

This program defines a DRG table within WORKING-STORAGE, likely for the 2007 fiscal year.

*   **Files Accessed:** None. This program defines a table in WORKING-STORAGE.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: A table containing DRG data.
        *   `05 D-TAB`: Holds DRG data as a packed string, starting with '20071001'.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective Date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG Weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average Length of Stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days Trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic ALoS.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG090

Similar to IPDRG080, defining a DRG table for the 2008 fiscal year.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **LINKAGE SECTION:** None.

---

### Program: IRFBN091

This program defines a table of state-specific Rural Floor Budget Neutrality Factors (RFBNs).

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:**
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
        *   `05 MES-SSRFBN-REST PIC X(22)`: Remaining data.
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs (72 entries).
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State Code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: State Specific Rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Code (unclear purpose).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State Name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data.
*   **LINKAGE SECTION:** None.

---

### Program: LTCAL087

This program performs payment calculations, incorporating DRG data via a COPY statement.

*   **Files Accessed:** None explicitly defined in `FILE-CONTROL`. Uses `COPY LTDRG086` and `COPY IPDRG080`, implying use of data from these sources (likely DRG tables).
*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL087      - W O R K I N G   S T O R A G E'`: Comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V08.7'`: Version Number.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `COPY LTDRG086`: Includes the `LTDRG086` copybook, containing `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `COPY IPDRG080`: Includes the `IPDRG080` copybook, containing `DRG-TABLE` (DRG codes, weights, ALoS, days trimmed, arithmetic ALoS).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for PPS calculations. Includes fields for LOS, Regular Days, Total Days, SSOT, and blended payment amounts.
*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA`: Bill Data passed from the calling program.
        *   `10 B-NPI10`: National Provider Identifier (NPI).
        *   `10 B-PROVIDER-NO`: Provider Number.
        *   `10 B-PATIENT-STATUS`: Patient Status.
        *   `10 B-DRG-CODE`: DRG Code.
        *   `10 B-LOS`: Length of Stay.
        *   `10 B-COV-DAYS`: Covered Days.
        *   `10 B-LTR-DAYS`: Lifetime Reserve Days.
        *   `10 B-DISCHARGE-DATE`: Discharge Date (CCYYMMDD).
        *   `10 B-COV-CHARGES`: Covered Charges.
        *   `10 B-SPEC-PAY-IND`: Special Pay Indicator.
        *   `10 FILLER`: Filler.
    *   `01 PPS-DATA-ALL`: PPS data returned to the calling program. Includes return code, threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, facility costs, new facility specific rate, etc.
    *   `01 PPS-CBSA`: A 5-character field for CBSA Code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: Indicates if all tables were passed.
        *   `05 PPS-VERSIONS`: Contains version numbers.
            *   `10 PPDRV-VERSION PIC X(05)`: Version of PPDRV program.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data. Contains NPI, provider number, state, various dates (effective, FY begin, report, termination), waiver code, intermediary number, provider type, census division, MSA data, facility specific rate, COLA, intern ratio, bed size, operating cost-to-charge ratio, CMI, SSI ratio, Medicaid ratio, PPS blend year indicator, PRUF update factor, DSH percent, and FYE date. Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, and `PROV-NEWREC-HOLD3`.
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record.
        *   `05 W-MSA PIC X(4)`: MSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective date.
        *   `05 W-WAGE-INDEX1`, `W-WAGE-INDEX2`: Wage index values.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record.
        *   `05 W-CBSA-IPPS`: CBSA code for IPPS.
        *   `05 W-CBSA-IPPS-SIZE`: Size indicator for CBSA.
        *   `05 W-CBSA-IPPS-EFF-DATE`: Effective date for IPPS CBSA.
        *   `05 FILLER`: Filler.
        *   `05 W-IPPS-WAGE-INDEX`: IPPS Wage Index.
        *   `05 W-IPPS-PR-WAGE-INDEX`: PR IPPS Wage Index.

---

### Program: LTCAL091

This program performs payment calculations, similar to LTCAL087, but for a different fiscal year.

*   **Files Accessed:** Similar to LTCAL087, uses data from copybooks `LTDRG086` and `IPDRG080`.
*   **WORKING-STORAGE SECTION:** Very similar to LTCAL087, with the main difference being the `CAL-VERSION` which is 'V09.1'. The copied data structures will also reflect the year's changes.
*   **LINKAGE SECTION:** Identical to LTCAL087.

---

### Program: LTCAL094

This program performs payment calculations, incorporating updated DRG and RFBN data.

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG093`, `IPDRG090`, `IRFBN091`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL087 and LTCAL091, but with `CAL-VERSION` as 'V09.4'. The copied data structures reflect changes for the year. Note the addition of `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **LINKAGE SECTION:** Identical to LTCAL087.

---

### Program: LTCAL095

This program performs payment calculations, similar to LTCAL094, but for a different fiscal year.

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG095`, `IPDRG090`, `IRFBN091`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. The copied data structures reflect changes for the year.
*   **LINKAGE SECTION:** Identical to LTCAL087.

---

### Program: LTDRG080

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None. This is a data definition file.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds the DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
            *   `05 WWM-IPTHRESH PIC 9(3)V9(1)`: IPPS threshold.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG086

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG080, but with different data and 735 occurrences of WWM-ENTRY.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG093

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG086, but with different data.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG095

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG093, but with different data.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG063

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: A table containing DRG data.
        *   `05 D-TAB`: Holds the raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Structured DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the period.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: Weight of the DRG.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: IPDRG071

This program defines a DRG table within WORKING-STORAGE.

*   **Files Accessed:** None explicitly defined.
*   **WORKING-STORAGE SECTION:**
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
*   **LINKAGE SECTION:** None.

---

### Program: LTCAL064

This program performs payment calculations, using DRG data via a COPY statement.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG062.`, suggesting data from that copybook.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF`: A comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook, containing a DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results.
    *   Several numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `01 PROV-NEW-HOLD`: Structure to hold provider data. Contains numerous fields related to provider information.
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA`: Bill data passed from a calling program. Includes fields for provider information, DRG code, length of stay, discharge date, and charges.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program. Contains return codes, payment amounts, and other calculated values.
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program (same as in Working-Storage).

---

### Program: LTCAL072

This program performs payment calculations, similar to LTCAL064, but for a later fiscal year and with more complex calculations.

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (LTCH DRG table).
    *   `COPY IPDRG063`: Includes the `IPDRG063` copybook (IPPS DRG table).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded to include many more variables for short-stay outlier calculations.
    *   Numerous variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices, and other factors.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data for LTCH.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data for IPPS.
*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE in this version).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data (same as in Working-Storage).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data (same as in Working-Storage).

---

### Program: LTCAL075 and LTCAL080

These programs perform payment calculations similar to LTCAL072, with incremental changes in constants, rates, and potentially new variables.

*   **Files Accessed:** Similar to LTCAL064, uses data from copybooks like `LTDRG075` and `LTDRG080`.
*   **WORKING-STORAGE SECTION:** Similar to LTCAL072, with `CAL-VERSION` updated for the respective years. The basic structure and copybook inclusions remain consistent.
*   **LINKAGE SECTION:** Similar to LTCAL072, maintaining consistent data structures.

---

### Program: LTDRG062

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Contains the raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefines `W-DRG-FILLS` to structure the data.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: The LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** None.

---

### Program: LTDRG075 and LTDRG080

These programs define DRG tables within WORKING-STORAGE, with updated data and structures compared to LTDRG062.

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG062. LTDRG075 and LTDRG080 will contain updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (like `WWM-IPTHRESH` in LTDRG080). The number of `WWM-ENTRY` occurrences may also change.
*   **LINKAGE SECTION:** None.

---

### Program: LTCAL043

This program performs payment calculations, using DRG data via a COPY statement.

*   **Files Accessed:** None explicitly defined. Uses `COPY LTDRG041`, implying access to data defined within that copied file (likely a DRG table).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 46-character text string used for identifying the working storage section (comment).
    *   `CAL-VERSION`: A 5-character string holding the version number 'C04.3'.
    *   `LTDRG041`: A copy of another COBOL program or data structure.
       *   `WWM-ENTRY`: An array (occurs 510 times) containing DRG-related data: `WWM-DRG` (3-char DRG code), `WWM-RELWT` (relative weight), `WWM-ALOS` (average length of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for PPS calculations, including LOS, Regular Days, Total Days, SSOT, and blended payment amounts.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Passed to and from the calling program, containing bill information (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, LTR Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Contains PPS calculation results (return code, threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, etc.).
    *   `PRICER-OPT-VERS-SW`: Structure indicating pricing tables and versions used (`PRICER-OPTION-SW`, `PPS-VERSIONS` including `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Structure holding provider-specific data (NPI, provider number, dates, waiver code, and various provider-specific variables).
    *   `WAGE-NEW-INDEX-RECORD`: Structure containing wage index data (MSA, Effective Date, and three wage index values).

---

### Program: LTCAL058

This program performs payment calculations, similar to LTCAL043, but for a different fiscal year.

*   **Files Accessed:** Similar to LTCAL043, uses `COPY LTDRG041`.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.8').
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

### Program: LTCAL059

This program performs payment calculations, using a different DRG table copybook.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table; structure is defined as:
       *   `WWM-ENTRY`: An array (occurs 512 times) containing DRG-related data (`WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `HOLD-PPS-COMPONENTS`: Structure for holding intermediate PPS calculation results (same as in LTCAL043 and LTCAL058).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in LTCAL043 and LTCAL058).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in LTCAL043 and LTCAL058).
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in LTCAL043 and LTCAL058).
    *   `PROV-NEW-HOLD`: Provider-specific data (same as in LTCAL043 and LTCAL058).
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data (same as in LTCAL043 and LTCAL058).

---

### Program: LTCAL063

This program performs payment calculations, using DRG data and including CBSA code.

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table (same structure as in LTCAL059).
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

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: A table of DRG codes and related information, implemented as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
       *   `WWM-ENTRY`: An array (occurs 510 times) of records, each containing:
          *   `WWM-DRG`: 3-character DRG code.
          *   `WWM-RELWT`: Relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
*   **Linkage Section:** None.

---

### Program: LTDRG057

This program defines a DRG table directly within WORKING-STORAGE.

*   **Files Accessed:** None. This is a data definition file.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Table of DRG codes and related data as 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
       *   `WWM-ENTRY`: An array (occurs 512 times) of records, each containing:
          *   `WWM-DRG`: 3-character DRG code.
          *   `WWM-RELWT`: Relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
*   **Linkage Section:** None.

---

### Program: LTCAL032

This program performs payment calculations, utilizing DRG data via a COPY statement.

*   **Files Accessed:** None explicitly defined in `FILE-CONTROL`. Uses `COPY LTDRG031`, likely defining DRG table structures.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Literal string indicating working storage.
    *   `CAL-VERSION`: Program version number ('C03.2').
    *   `LTDRG031` (from COPY): Contains `W-DRG-TABLE` (DRG codes, relative weights, average lengths of stay).
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, Regular Days, Total Days, SSOT, Blend RTC, Blend Facility Rate, Blend PPS Rate, Social Security Pay Amount, Social Security Cost, Labor and Non-labor Portions, Fixed Loss Amount, New Facility Specific Rate).
    *   `PRICER-OPT-VERS-SW`: Version information and switches (`PRICER-OPTION-SW`, `PPDRV-VERSION`).
    *   `PROV-NEW-HOLD`: Holds provider-specific data (NPI, Provider Number, State, dates, waiver code, intermediary number, provider type, census division, MSA data, facility rates, COLA, etc.). Structured into `PROV-NEWREC-HOLD1`, `PROV-NEWREC-HOLD2`, `PROV-NEWREC-HOLD3`.
    *   `WAGE-NEW-INDEX-RECORD`: Holds wage index data (MSA, Effective Date, wage index values).
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Contains bill data passed to the subroutine (NPI, Provider Number, Patient Status, DRG Code, Length of Stay, Covered Days, Lifetime Reserve Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Contains calculated PPS data returned by the subroutine (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, LOS, DRG Adjusted Pay Amount, Federal Pay Amount, Final Pay Amount, Facility Costs, New Facility Specific Rate, Outlier Threshold, Submitted DRG Code, Calculation Version Code, Regular Days Used, Lifetime Reserve Days Used, Blend Year, COLA, etc.). Structured into `PPS-DATA` and `PPS-OTHER-DATA`.

---

### Program: LTCAL042

This program performs payment calculations, similar to LTCAL032, but with updated version and specific calculation values.

*   **Files Accessed:** Same as LTCAL032; none explicitly defined, relies on `COPY LTDRG031`.
*   **Working-Storage Section:**
    *   Almost identical to LTCAL032, with key differences:
        *   `CAL-VERSION` is 'C04.2'.
        *   `PPS-STD-FED-RATE` has a different value (35726.18 vs 34956.15).
        *   `H-FIXED-LOSS-AMT` has a different value (19590 vs 24450).
        *   `PPS-BDGT-NEUT-RATE` has a different value (0.940 vs 0.934).
        *   An additional field `H-LOS-RATIO` (PIC 9(01)V9(05)) is added to `HOLD-PPS-COMPONENTS`.
*   **Linkage Section:** Identical to LTCAL032.

---

### Program: LTDRG031

This is a copybook defining DRG table data structures, used by other programs.

*   **Files Accessed:** This is a copybook; it doesn't directly access files. It defines data structures used by programs like LTCAL032 and LTCAL042.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None (as it's a copybook).

---

### Overall Program Flow and Observations:

The programs analyzed are part of a system that calculates healthcare payments based on various factors including Diagnosis Related Groups (DRGs), provider-specific data, and wage indices.

1.  **LTMGR212:** Initiates the process by reading billing records and calling `LTOPN212` for payment calculations. It then formats output to `PRTOPER`.
2.  **LTOPN212:** Loads necessary tables (provider, wage index) and calls `LTDRV212` to perform the core payment logic.
3.  **LTDRV212:** Acts as a driver, selecting the appropriate `LTCAL` module based on the bill's discharge date and provider information to perform the final payment calculations.
4.  **LTCALxx programs:** These modules execute the detailed payment calculations, referencing DRG tables (via `LTDRGxx` and `IPDRGxx` copybooks) and potentially wage index and RFBN tables. They receive bill and provider data via the linkage section and return calculated payment information.
5.  **IPDRGxx programs:** Primarily define IPPS DRG table structures.
6.  **LTDRGxx programs:** Primarily define LTCH DRG table structures.
7.  **IRFBNxx programs:** Define state-specific Rural Floor Budget Neutrality Factor tables.

The extensive versioning (e.g., LTCAL162, LTCAL170, LTCAL183, etc.) and the introduction of new logic (like COVID-19 processing in LTCAL202) indicate a system that has undergone significant evolution to adapt to changing healthcare regulations and methodologies. The use of COPY statements is prevalent, suggesting a modular design where common data structures and logic are reused across different program versions and modules. The presence of numerous filler fields and complex nested structures points to a legacy system with a long development history.