## Data Definition and File Handling

This document consolidates and analyzes the "Data Definition and File Handling" sections from multiple functional specification documents (L1, L2, L4, L5, L6, L7, L8). It details the files accessed, WORKING-STORAGE data structures, and LINKAGE SECTION data structures for various COBOL programs involved in healthcare payment processing.

### Program: LTMGR212

*   **Files Accessed:**
    *   `BILLFILE` (UT-S-SYSUT1): Input file containing billing records. Record format is described in the `BILL-REC` record (422 bytes).
    *   `PRTOPER` (UT-S-PRTOPER): Output file for printing prospective payment reports. Record format is described in `PRTOPER-LINE` record (133 bytes).

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 51-character literal, seemingly a comment.
    *   `PPMGR-VERSION`: A 5-character field storing the program version ('M21.2').
    *   `LTOPN212`: An 8-character literal, the name of the called program.
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch (0 = not EOF, 1 = EOF).
    *   `OPERLINE-CTR`: A 2-digit numeric field counting lines written to the `PRTOPER` file. Initialized to 65.
    *   `UT1-STAT`: A 2-character field storing the file status of `BILLFILE`.
        *   `UT1-STAT1`: First character of the file status.
        *   `UT1-STAT2`: Second character of the file status.
    *   `OPR-STAT`: A 2-character field storing the file status of `PRTOPER`.
        *   `OPR-STAT1`: First character of the file status.
        *   `OPR-STAT2`: Second character of the file status.
    *   `BILL-WORK`: A structure holding the input bill record from `BILLFILE`. Contains various fields like provider NPI, patient status, DRG code, length of stay (LOS), coverage days, cost report days, discharge date, charges, special pay indicator, review code, and tables for diagnosis and procedure codes.
    *   `PPS-DATA-ALL`: A structure containing data returned from the `LTOPN212` program. Includes various payment calculation results, wage indices, and other relevant data.
    *   `PPS-CBSA`: A 5-character field for CBSA code (Core Based Statistical Area).
    *   `PPS-PAYMENT-DATA`: A structure holding payment amounts calculated by `LTOPN212`. Contains site-neutral cost and IPPS payments and standard full and short stay payments.
    *   `BILL-NEW-DATA`: A structure mirroring `BILL-WORK`, but presumably used for passing data to the called program. It includes similar data elements.
    *   `PRICER-OPT-VERS-SW`: A structure to hold the pricer option and version information passed to `LTOPN212`.
        *   `PRICER-OPTION-SW`: A single character indicating the pricing option.
        *   `PPS-VERSIONS`: A structure containing the version number passed to `LTOPN212`.
    *   `PROV-RECORD-FROM-USER`: A large structure (holding provider information) that can be passed to `LTOPN212`. It includes NPI, provider number, various dates, codes, indices, and other provider-specific data.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Large structures (likely arrays) to hold CBSA (Core Based Statistical Area) and MSA (Metropolitan Statistical Area) wage index tables that can be passed to `LTOPN212`.
    *   `PPS-DETAIL-LINE-OPER`, `PPS-HEAD2-OPER`, `PPS-HEAD3-OPER`, `PPS-HEAD4-OPER`: Structures defining the format of lines in the output report `PRTOPER`. These structures contain formatted data to create a header and detail lines for the report.

*   **Linkage Section:** LTMGR212 does not have a Linkage Section.

### Program: LTOPN212

*   **Files Accessed:**
    *   `PROV-FILE` (UT-S-PPSPROV): Input file containing provider records. Record layout is defined as `PROV-REC` (240 bytes).
    *   `CBSAX-FILE` (UT-S-PPSCBSAX): Input file containing CBSA wage index data. Record layout defined as `CBSAX-REC`.
    *   `IPPS-CBSAX-FILE` (UT-S-IPCBSAX): Input file containing IPPS CBSA wage index data. Record layout defined as `F-IPPS-CBSA-REC`.
    *   `MSAX-FILE` (UT-S-PPSMSAX): Input file containing MSA wage index data. Record layout defined as `MSAX-REC`.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, seemingly a comment.
    *   `OPN-VERSION`: A 5-character field storing the program version ('021.2').
    *   `LTDRV212`: An 8-character literal, the name of the called program.
    *   `TABLES-LOADED-SW`: A 1-digit numeric field indicating whether tables have been loaded (0 = not loaded, 1 = loaded).
    *   `EOF-SW`: A 1-digit numeric field acting as an end-of-file switch.
    *   `W-PROV-NEW-HOLD`: A structure to hold the provider record either passed in or retrieved from `PROV-FILE`. It mirrors the structure `PROV-RECORD-FROM-USER` from LTMGR212.
    *   `PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`: 2-character fields storing file status information for each of the input files.
    *   `CBSA-WI-TABLE`: A table to hold CBSA wage index data, loaded from `CBSAX-FILE`. It's a table with varying number of entries (up to 10000), indexed by `CU1` and `CU2`.
    *   `IPPS-CBSA-WI-TABLE`: A table to hold IPPS CBSA wage index data, loaded from `IPPS-CBSAX-FILE`. It's a table with varying number of entries (up to 10000), indexed by `MA1`, `MA2`, and `MA3`.
    *   `MSA-WI-TABLE`: A table to hold MSA wage index data, loaded from `MSAX-FILE`. It's a table with varying number of entries (up to 4000), indexed by `MU1` and `MU2`.
    *   `WORK-COUNTERS`: A structure containing counters for the number of records read from each file.
    *   `PROV-TABLE`: A table (up to 2400 entries) to hold provider data read from `PROV-FILE`. It's divided into three parts (`PROV-DATA1`, `PROV-DATA2`, `PROV-DATA3`). Indexed by `PX1`, `PD2`, and `PD3`.
    *   `PROV-NEW-HOLD`: A structure to hold the provider record to be passed to `LTDRV212`. It mirrors the `PROV-NEW-HOLD` structure in LTMGR212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: A structure containing the billing data passed from `LTMGR212`. It mirrors the `BILL-NEW-DATA` structure in LTMGR212.
    *   `PPS-DATA-ALL`: A structure to hold the PPS data passed from and returned to `LTMGR212`. It mirrors the `PPS-DATA-ALL` structure in LTMGR212.
    *   `PPS-CBSA`: A 5-character field for the CBSA code, passed from `LTMGR212`.
    *   `PPS-PAYMENT-DATA`: A structure to hold payment data passed from and returned to `LTMGR212`. It mirrors the `PPS-PAYMENT-DATA` structure in LTMGR212.
    *   `PRICER-OPT-VERS-SW`: A structure holding the pricer option and version information passed from `LTMGR212`. It mirrors the `PRICER-OPT-VERS-SW` structure in LTMGR212.
    *   `PROV-RECORD-FROM-USER`: A structure containing provider-specific information passed from `LTMGR212`. It mirrors the `PROV-RECORD-FROM-USER` structure in LTMGR212.
    *   `CBSAX-TABLE-FROM-USER`, `IPPS-CBSAX-TABLE-FROM-USER`, `MSAX-TABLE-FROM-USER`: Structures mirroring those in LTMGR212, to hold wage index tables.

### Program: LTDRV212

*   **Files Accessed:** LTDRV212 does not access any files directly.

*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 48-character literal, seemingly a comment.
    *   `DRV-VERSION`: A 5-character field storing the program version ('D21.2').
    *   `LTCAL032` ... `LTCAL212`: 8-character literals representing names of various called programs (likely different versions of the same pricing module).
    *   `WS-9S`: An 8-character numeric literal with all 9s, used for comparing dates.
    *   `WI_QUARTILE_FY2020`, `WI_PCT_REDUC_FY2020`, `WI_PCT_ADJ_FY2020`: Numeric fields holding wage index related constants for FY2020.
    *   `RUFL-ADJ-TABLE`: A table (defined in the COPY RUFL200) containing rural floor factors for various CBSAs.
    *   `HOLD-RUFL-DATA`: A structure to hold data from `RUFL-ADJ-TABLE`.
    *   `RUFL-IDX2`: An index for `RUFL-TAB` table.
    *   `W-FY-BEGIN-DATE`, `W-FY-END-DATE`: Structures to hold the fiscal year begin and end dates calculated from the bill's discharge date.
    *   `HOLD-PROV-MSA`, `HOLD-PROV-CBSA`, `HOLD-PROV-IPPS-CBSA`, `HOLD-PROV-IPPS-CBSA-RURAL`: Structures to hold MSA and CBSA codes for wage index lookups.
    *   `WAGE-NEW-INDEX-RECORD-MSA`, `WAGE-NEW-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RECORD-CBSA`, `WAGE-IPPS-INDEX-RURAL-CBSA`: Structures to hold wage index records retrieved from the tables in LTOPN212.
    *   `W-IPPS-PR-WAGE-INDEX-RUR`: A field to hold the Puerto Rico-specific IPPS wage index.
    *   `H-LTCH-SUPP-WI-RATIO`: A field to hold the supplemental wage index ratio.
    *   `PROV-NEW-HOLD`: A structure holding the provider record passed from `LTOPN212`. It mirrors the `PROV-NEW-HOLD` structure in LTOPN212.
    *   `BILL-DATA-FY03-FY15`: A structure to hold billing data for older fiscal years (before Jan 2015).
    *   `BILL-NEW-DATA`: A structure holding billing data for FY2015 and later, mirroring the `BILL-NEW-DATA` structure in LTMGR212 and LTOPN212.
    *   `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-RECORD`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTMGR212 and LTOPN212.

*   **Linkage Section:**
    *   `BILL-NEW-DATA`: A structure containing the billing data passed from `LTOPN212`.
    *   `PPS-DATA-ALL`: A structure to hold PPS data passed from and returned to `LTOPN212`.
    *   `PPS-CBSA`: A 5-character field for CBSA code.
    *   `PPS-PAYMENT-DATA`: A structure for payment data passed from and returned to `LTOPN212`.
    *   `PRICER-OPT-VERS-SW`: A structure holding the pricer option and version information passed from `LTOPN212`.
    *   `PROV-RECORD`: A structure containing provider-specific information passed from `LTOPN212`.
    *   `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`, `MSA-WI-TABLE`, `WORK-COUNTERS`: Structures mirroring those in LTOPN212, holding wage index tables and record counts.

### Program: RUFL200 (COPY member)

*   **Files Accessed:** This is a COPY member, not a program; it doesn't directly access files. It defines a data structure.

*   **Working-Storage Section:** This COPY member only defines data structures, no working-storage section is needed.

*   **Linkage Section:** This COPY member only defines data structures, no linkage section is needed.

*   **Data Structures:**
    *   `RUFL-ADJ-TABLE`: The main structure. Contains a table `RUFL-TAB` of rural floor adjustment factors. Each entry contains a CBSA code (`RUFL-CBSA`), an effective date (`RUFL-EFF-DATE`), and a wage index (`RUFL-WI3`). The table has 459 entries.

### Program: IPDRG160

*   **Files Accessed:** This program likely accesses a DRG (Diagnosis Related Group) table file. The data suggests it's a master file containing DRG codes, weights, and descriptions. The file is read-only. No file names are explicitly mentioned in the code.
*   **WORKING-STORAGE SECTION:**
    *   `WK-DRGX-EFF-DATE` (PIC X(08)): Effective date for the DRG table (20151001).
    *   `PPS-DRG-TABLE`: A group item containing the DRG table data.
        *   `WK-DRG-DATA`: A group item containing DRG data in a literal, record-like format. This is likely a temporary holding area for the data read from the file.
        *   `WK-DRG-DATA2` (REDEFINES WK-DRG-DATA): A redefinition of `WK-DRG-DATA` to allow access to the DRG data in a more structured table format.
            *   `DRG-TAB` (OCCURS 758): A table of DRG data records.
                *   `DRG-DATA-TAB`: A group item representing a single DRG record.
                    *   `WK-DRG-DRGX` (PIC X(03)): DRG code (e.g., '001').
                    *   `FILLER1` (PIC X(01)): Filler.
                    *   `DRG-WEIGHT` (PIC 9(02)V9(04)): DRG weight.
                    *   `FILLER2` (PIC X(01)): Filler.
                    *   `DRG-GMALOS` (PIC 9(02)V9(01)): Geometric mean of average length of stay.
                    *   `FILLER3` (PIC X(05)): Filler.
                    *   `DRG-LOW` (PIC X(01)): Indicator (likely 'Y' or 'N').
                    *   `FILLER5` (PIC X(01)): Filler.
                    *   `DRG-ARITH-ALOS` (PIC 9(02)V9(01)): Arithmetic mean of average length of stay.
                    *   `FILLER6` (PIC X(02)): Filler.
                    *   `DRG-PAC` (PIC X(01)): Indicator (possible for post-acute care).
                    *   `FILLER7` (PIC X(01)): Filler.
                    *   `DRG-SPPAC` (PIC X(01)): Indicator (possible for special post-acute care).
                    *   `FILLER8` (PIC X(02)): Filler.
                    *   `DRG-DESC` (PIC X(26)): DRG description.

*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG170

*   **Files Accessed:** Similar to IPDRG160, this program likely accesses a DRG table file, read-only, for the year 2016.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160, but with `WK-DRGX-EFF-DATE` set to '20161001' and `DRG-TAB` having `OCCURS 757` instead of 758. The DRG data itself is different, reflecting the 2016 data.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG181

*   **Files Accessed:** Likely a read-only DRG table file for the year 2017.
*   **WORKING-STORAGE SECTION:** Structurally identical to IPDRG160 and IPDRG170, `WK-DRGX-EFF-DATE` is '20171001', and `DRG-TAB` has `OCCURS 754`. The DRG data is specific to 2017.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG190

*   **Files Accessed:** Likely a read-only DRG table file for the year 2018.
*   **WORKING-STORAGE SECTION:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20181001' and `DRG-TAB` having `OCCURS 761`. Data reflects 2018 DRGs.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG200

*   **Files Accessed:** Likely a read-only DRG table file for the year 2019.
*   **WORKING-STORAGE SECTION:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20191001' and `DRG-TAB` having `OCCURS 761`. Data is for 2019 DRGs. Note the addition of DRG 319 and 320.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG211

*   **Files Accessed:** Likely a read-only DRG table file for the year 2020.
*   **WORKING-STORAGE SECTION:** Structurally identical to previous IPDRG programs, with `WK-DRGX-EFF-DATE` as '20201001' and `DRG-TAB` having `OCCURS 767`. Data is for 2020 DRGs. Note the change in some DRG descriptions.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: LTCAL162

*   **Files Accessed:** This program likely accesses at least three files:
    *   A provider-specific file (PSF) containing provider information, including wage indices, cost-to-charge ratios, and other parameters.
    *   A CBSA (Core Based Statistical Area) wage index file containing wage index data for different geographic areas.
    *   An LTCH DRG table file (LTDRG160) and an IPPS DRG table file (IPDRG160) which are included via COPY statements. These are read-only.
*   **WORKING-STORAGE SECTION:**
    *   `W-STORAGE-REF`: A descriptive filler.
    *   `CAL-VERSION`: Program version number ('V16.2').
    *   `PROGRAM-CONSTANTS`: Constants used in the program.
    *   `PROGRAM-FLAGS`: Flags to control program flow and payment type selection.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate calculation results for payment.
    *   `WK-HLDDRG-DATA`, `WK-HLDDRG-DATA2`: Structures to hold the data copied from the DRG tables.
*   **LINKAGE SECTION:**
    *   `BILL-NEW-DATA`: Input bill data from a calling program (likely `LTDRV`).
    *   `PPS-DATA-ALL`: Output PPS (Prospective Payment System) calculation results.
    *   `PPS-CBSA`: Output CBSA code.
    *   `PPS-PAYMENT-DATA`: Output payment data for different payment types.
    *   `PRICER-OPT-VERS-SW`: Switches indicating the versions of the pricer option and other driver programs.
    *   `PROV-NEW-HOLD`: Input provider-specific data from a calling program (likely `LTDRV`).
    *   `WAGE-NEW-INDEX-RECORD`: Input LTCH wage index record.
    *   `WAGE-NEW-IPPS-INDEX-RECORD`: Input IPPS wage index record.

### Program: LTCAL170

*   **Files Accessed:** Similar to LTCAL162, this likely accesses a PSF, CBSA wage index file, and the LTCH/IPPS DRG tables (LTDRG170 and IPDRG170).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL162, but with `CAL-VERSION` set to 'V17.0'. The constants and rates are updated for FY17.
*   **LINKAGE SECTION:** Identical to LTCAL162's Linkage Section, except for the addition of `P-NEW-STATE-CODE` within `PROV-NEW-HOLD`.

### Program: LTCAL183

*   **Files Accessed:** Likely accesses a PSF, CBSA wage index file, and the LTCH/IPPS DRG tables (LTDRG181 and IPDRG181).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL170, with `CAL-VERSION` as 'V18.3', updated for FY18. Note that some variables related to Subclause II have been removed.
*   **LINKAGE SECTION:** The linkage section is similar to LTCAL170, with the removal of fields related to Subclause II.

### Program: LTCAL190

*   **Files Accessed:** Likely accesses a PSF, CBSA wage index file, and the LTCH/IPPS DRG tables (LTDRG190 and IPDRG190).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL183, with `CAL-VERSION` set to 'V19.0' and updated for FY19.
*   **LINKAGE SECTION:** The linkage section is similar to LTCAL183.

### Program: LTCAL202

*   **Files Accessed:** Similar to previous LTCAL programs, accessing a PSF, CBSA wage index file, and the LTCH/IPPS DRG tables (LTDRG200 and IPDRG200).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL190, with `CAL-VERSION` as 'V20.2', updated for FY20. Includes additions related to COVID-19 processing.
*   **LINKAGE SECTION:** Similar to previous LTCAL programs, with the addition of `B-LTCH-DPP-INDICATOR-SW` within `BILL-NEW-DATA` to handle the Disproportionate Patient Percentage (DPP) adjustment.

### Program: LTCAL212

*   **Files Accessed:** Similar to LTCAL202, accessing PSF, CBSA wage index file, and LTCH/IPPS DRG tables (LTDRG210 and IPDRG211).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL202, with `CAL-VERSION` as 'V21.2', updated for FY21. Includes changes for CR11707 and CR11879. Note the addition of `P-SUPP-WI-IND` and `P-SUPP-WI` in the `PROV-NEW-HOLD` structure.
*   **LINKAGE SECTION:** Similar to LTCAL202, with no additional fields.

### Program: LTDRG160

*   **Files Accessed:** This is a copybook likely containing the LTCH DRG table data for FY15. It's not a program itself but data definitions used by other programs.
*   **WORKING-STORAGE SECTION:** The `W-DRG-FILLS` and `W-DRG-TABLE` items define the structure of the LTCH DRG table.
    *   `W-DRG-FILLS`: Contains the DRG data in a packed format.
    *   `W-DRG-TABLE` (REDEFINES W-DRG-FILLS): A table of DRG records.
        *   `WWM-ENTRY` (OCCURS 748): A table entry containing the following:
            *   `WWM-DRG` (PIC X(3)): LTCH DRG code.
            *   `WWM-RELWT` (PIC 9(1)V9(4)): Relative weight.
            *   `WWM-ALOS` (PIC 9(2)V9(1)): Average length of stay.
            *   `WWM-IPTHRESH` (PIC 9(3)V9(1)): IPPS threshold.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: LTDRG170

*   **Files Accessed:** This is a copybook, similar to LTDRG160, but containing LTCH DRG data for FY16.
*   **WORKING-STORAGE SECTION:** Structurally similar to LTDRG160, but `WWM-ENTRY` has `OCCURS 747` times.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: LTDRG181

*   **Files Accessed:** This is a copybook containing LTCH DRG data for FY18.
*   **WORKING-STORAGE SECTION:** Structurally similar to LTDRG160 and LTDRG170, with `WWM-ENTRY` having `OCCURS 744`.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: LTDRG190

*   **Files Accessed:** This is a copybook containing LTCH DRG data for FY19.
*   **WORKING-STORAGE SECTION:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 751`.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: LTDRG210

*   **Files Accessed:** This is a copybook containing LTCH DRG data for FY21.
*   **WORKING-STORAGE SECTION:** Structurally similar to previous LTDRG copybooks, with `WWM-ENTRY` having `OCCURS 754`.
*   **LINKAGE SECTION:** This program section is not present in the provided code.

### Program: IPDRG104

*   **Files Accessed:** The program doesn't explicitly list any files. It uses a `COPY IPDRG104` statement, implying that the data is being included from another file named `IPDRG104`. This file likely contains a DRG table.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: A table containing DRG data.
        *   `05 D-TAB`: A level 05 item that is redefined. It appears to hold the DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: A redefinition of `D-TAB` to provide a more structured access to the DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: A single period (presumably a year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the DRG data.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed (possibly for outlier calculations).
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: IPDRG110

*   **Files Accessed:** Similar to `IPDRG104`, this program uses a `COPY IPDRG110` statement, referencing a file containing DRG data.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: A table containing DRG data. Structurally identical to `IPDRG104`.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing the DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: A single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: IPDRG123

*   **Files Accessed:** Uses a `COPY IPDRG123` statement, indicating inclusion of DRG data from another file.
*   **WORKING-STORAGE SECTION:**
    *   `01 DRG-TABLE`: DRG data table, structurally similar to `IPDRG104` and `IPDRG110`.
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing the DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: IRFBN102

*   **Files Accessed:** The `COPY IRFBN102` statement suggests the data is from a file containing state-specific Rural Floor Budget Neutrality Factors (RFBNS).
*   **WORKING-STORAGE SECTION:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNS.
        *   `02 WK-SSRFBN-DATA`: Holds the RFBN data in a less structured format (likely for easier readability/initialization).
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing the RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs. 72 entries, sorted by state code.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Another code (unclear purpose).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   `01 MES-ADD-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-CHG-PROV PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-PPS-STATE PIC X(02)`: State code.
    *   `01 MES-INTRO PIC X(53) VALUE SPACES`: Message area.
    *   `01 MES-TOT-PAY PIC 9(07)V9(02) VALUE 0`: Total payment amount.
    *   `01 MES-SSRFBN`: Holds a single RFBN record. Structurally identical to `WK-SSRFBN-REASON-ALL`.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: IRFBN105

*   **Files Accessed:** Uses a `COPY IRFBN105` statement, referencing a file presumably containing updated RFBN data.
*   **WORKING-STORAGE SECTION:**
    *   `01 PPS-SSRFBN-TABLE`: Table of state-specific RFBNs. Structurally identical to `IRFBN102`.
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing the RFBN data.
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
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: LTCAL103

*   **Files Accessed:** This program uses `COPY` statements to include data from:
    *   `LTDRG100`: Likely contains a LTC DRG table.
    *   `IPDRG104`: Contains IPPS DRG data.
    *   `IRFBN102`: Contains IPPS state-specific RFBNs.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-STORAGE-REF PIC X(46) VALUE 'LTCAL103      - W O R K I N G   S T O R A G E'`: Descriptive comment.
    *   `01 CAL-VERSION PIC X(05) VALUE 'V10.3'`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
        *   `05 FED-FY-BEGIN-03 THRU FED-FY-BEGIN-07 PIC 9(08)`: Fiscal year start dates.
    *   `01 HOLD-PPS-COMPONENTS`: Holds calculated PPS components. Contains numerous numeric variables for various aspects of payment calculation (LOS, days, rates, shares, adjustments, etc.). See the code for individual variable descriptions.
    *   `01 PPS-DATA-ALL`: Holds the final PPS calculation results. Includes `PPS-RTC` (return code), `PPS-CHRG-THRESHOLD` (charge threshold), and many other numeric fields for various PPS data elements.
    *   `01 PPS-CBSA PIC X(05)`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Switch for pricer options and versions.
        *   `05 PRICER-OPTION-SW PIC X(01)`: 'A' for all tables passed, 'P' for provider record passed.
        *   `05 PPS-VERSIONS`: Versions of related programs.
            *   `10 PPDRV-VERSION PIC X(05)`: Version number.
    *   `01 PROV-NEW-HOLD`: Holds provider-specific data. Contains nested groups for NPI, provider number, dates (effective, fiscal year begin, report, termination), waiver code, intern number, provider type, census division, MSA data, and various other parameters (rates, ratios, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index record.
        *   `05 W-CBSA PIC X(5)`: CBSA code.
        *   `05 W-EFF-DATE PIC X(8)`: Effective date.
        *   `05 W-WAGE-INDEX1`, `W-WAGE-INDEX2`, `W-WAGE-INDEX3 PIC S9(02)V9(04)`: Wage indices.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index record. Contains CBSA code, size indicator (large urban, other urban, all rural), effective date, and wage indices (federal and Puerto Rico).
    *   `01 W-DRG-FILLS`: Holds DRG data in a packed format (redefined below).
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing DRG data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:**
    *   `01 BILL-NEW-DATA`: Bill data passed from the calling program. Contains provider NPI, provider number, patient status, DRG code, length of stay (LOS), covered days, lifetime reserve days, discharge date, covered charges, special pay indicator, and filler.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.

### Program: LTCAL105

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG100`: LTC DRG table.
    *   `IPDRG104`: IPPS DRG data.
    *   `IRFBN105`: IPPS state-specific RFBNs.
*   **WORKING-STORAGE SECTION:** Very similar to `LTCAL103`, the main differences are in the version number (`CAL-VERSION`), the copybooks used (`IRFBN105` instead of `IRFBN102`), and some minor numeric constant adjustments within the program's logic.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

### Program: LTCAL111

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG110`: LTC DRG table.
    *   `IPDRG110`: IPPS DRG data.
    *   `IRFBN102` (commented out): There is a commented out `COPY IRFBN***` statement. This likely indicates that for this version, there's no state-specific RFBN table to be included.
*   **WORKING-STORAGE SECTION:** Similar to `LTCAL103` and `LTCAL105`, with the version number updated to `V11.1` and copybooks adjusted. Note the absence of a state-specific RFBN table.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

### Program: LTCAL123

*   **Files Accessed:** Includes data through `COPY` statements from:
    *   `LTDRG123`: LTC DRG table.
    *   `IPDRG123`: IPPS DRG data.
    *   Commented out copybook for RFBNs, similar to LTCAL111.
*   **WORKING-STORAGE SECTION:** Similar to previous LTCAL programs, updated to version `V12.3` and relevant copybooks. No state-specific RFBN table is used.
*   **LINKAGE SECTION:** Identical to `LTCAL103`.

### Program: LTDRG100

*   **Files Accessed:** No files are explicitly accessed. The data is defined directly within the program.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds the LTC DRG data in a packed format (redefined below).
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 736 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: LTDRG110

*   **Files Accessed:** No files are explicitly accessed. The data is defined directly within the program.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 737 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: LTDRG123

*   **Files Accessed:** No files are explicitly accessed. The data is defined directly within the program.
*   **WORKING-STORAGE SECTION:**
    *   `01 W-DRG-FILLS`: Holds LTC DRG data in a packed format.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefined structure for accessing the data.
        *   `03 WWM-ENTRY OCCURS 742 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: LTC DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **LINKAGE SECTION:** The program has no LINKAGE SECTION.

### Program: IPDRG080

*   **Files Accessed:** None. This program appears to define a table in WORKING-STORAGE, not to access external files.
*   **WORKING-STORAGE SECTION:**
    ```cobol
    01  DRG-TABLE.
        05  D-TAB.
            10  FILLER                  PIC X(08) VALUE '20071001'.  (Date: October 1, 2007)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
            10  FILLER                  PIC X(56) VALUE ... (Long string of alphanumeric data - likely DRG data)
        05  DRGX-TAB REDEFINES D-TAB.
            10  DRGX-PERIOD               OCCURS 1 INDEXED BY DX5.
                15  DRGX-EFF-DATE         PIC X(08). (Effective Date)
                15  DRG-DATA              OCCURS 1000 INDEXED BY DX6.
                    20  DRG-WT            PIC 9(02)V9(04). (DRG Weight)
                    20  DRG-ALOS          PIC 9(02)V9(01). (Average Length of Stay)
                    20  DRG-DAYS-TRIM     PIC 9(02). (Days Trimmed)
                    20  DRG-ARITH-ALOS    PIC 9(02)V9(01). (Arithmetic ALoS)
    ```
*   **LINKAGE SECTION:** None.

### Program: IPDRG090

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to IPDRG080, but with a different effective date ('20081001') and DRG data.
*   **LINKAGE SECTION:** None.

### Program: IRFBN091

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:**
    ```cobol
    01  MES-ADD-PROV                   PIC X(53) VALUE SPACES. (Message Area for Adding Provider)
    01  MES-CHG-PROV                   PIC X(53) VALUE SPACES. (Message Area for Changing Provider)
    01  MES-PPS-STATE                  PIC X(02). (PPS State Code)
    01  MES-INTRO                      PIC X(53) VALUE SPACES. (Introductory Message Area)
    01  MES-TOT-PAY                    PIC 9(07)V9(02) VALUE 0. (Total Payment Amount)
    01  MES-SSRFBN.
        05 MES-SSRFBN-STATE PIC 99. (State Code)
        05 FILLER           PIC XX.
        05 MES-SSRFBN-RATE  PIC 9(1)V9(5). (State Specific Rate)
        05 FILLER           PIC XX.
        05 MES-SSRFBN-CODE2 PIC 99.
        05 FILLER           PIC X.
        05 MES-SSRFBN-STNAM PIC X(20). (State Name)
        05 MES-SSRFBN-REST  PIC X(22).
    01  PPS-SSRFBN-TABLE.
        02  WK-SSRFBN-DATA.
            05  FILLER   PIC X(57)  VALUE ... (Repeated lines defining State data)
        02  WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA.
            05  SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX.
                10  WK-SSRFBN-REASON-ALL.
                    15 WK-SSRFBN-STATE  PIC 99. (State Code)
                    15 FILLER           PIC XX.
                    15 WK-SSRFBN-RATE   PIC 9(1)V9(5). (State Specific Rate)
                    15 FILLER           PIC XX.
                    15 WK-SSRFBN-CODE2  PIC 99.
                    15 FILLER           PIC X.
                    15 WK-SSRFBN-STNAM  PIC X(20). (State Name)
                    15 WK-SSRFBN-REST   PIC X(22).
    ```
*   **LINKAGE SECTION:** None.

### Program: LTCAL087

*   **Files Accessed:** None explicitly defined in the `FILE-CONTROL`. However, the `COPY` statements imply the use of external files containing the data for `LTDRG086` and `IPDRG080`.
*   **WORKING-STORAGE SECTION:**
    ```cobol
    01  W-STORAGE-REF                  PIC X(46)  VALUE 'LTCAL087      - W O R K I N G   S T O R A G E'. (Comment)
    01  CAL-VERSION                    PIC X(05)  VALUE 'V08.7'. (Version Number)
    01  PROGRAM-CONSTANTS.              (Federal Fiscal Year Begin Dates)
        05  FED-FY-BEGIN-03            PIC 9(08) VALUE 20021001.
        05  FED-FY-BEGIN-04            PIC 9(08) VALUE 20031001.
        05  FED-FY-BEGIN-05            PIC 9(08) VALUE 20041001.
        05  FED-FY-BEGIN-06            PIC 9(08) VALUE 20051001.
        05  FED-FY-BEGIN-07            PIC 9(08) VALUE 20061001.
    ```
    (The `COPY` statements bring in substantial additional data structures from `LTDRG086` and `IPDRG080`.)
    ```cobol
    01  HOLD-PPS-COMPONENTS. (Holds intermediate calculation results)
        05  H-LOS                        PIC 9(03). (Length of Stay)
        05  H-REG-DAYS                   PIC 9(03). (Regular Days)
        05  H-TOTAL-DAYS                 PIC 9(05). (Total Days)
        ... many more numeric fields for calculations ...
    ```
*   **LINKAGE SECTION:**
    ```cobol
    01  BILL-NEW-DATA. (Bill Data passed from calling program)
        10  B-NPI10.
            15  B-NPI8             PIC X(08). (Provider NPI)
            15  B-NPI-FILLER       PIC X(02).
        10  B-PROVIDER-NO          PIC X(06). (Provider Number)
        10  B-PATIENT-STATUS       PIC X(02). (Patient Status)
        10  B-DRG-CODE             PIC 9(03). (DRG Code)
        10  B-LOS                  PIC 9(03). (Length of Stay)
        10  B-COV-DAYS             PIC 9(03). (Covered Days)
        10  B-LTR-DAYS             PIC 9(02). (Lifetime Reserve Days)
        10  B-DISCHARGE-DATE.
            15  B-DISCHG-CC        PIC 9(02). (Discharge Date Components)
            15  B-DISCHG-YY        PIC 9(02).
            15  B-DISCHG-MM        PIC 9(02).
            15  B-DISCHG-DD        PIC 9(02).
        10  B-COV-CHARGES          PIC 9(07)V9(02). (Covered Charges)
        10  B-SPEC-PAY-IND         PIC X(01). (Special Pay Indicator)
        10  FILLER                 PIC X(13).
    01  PPS-DATA-ALL. (PPS data returned to calling program)
        05  PPS-RTC                       PIC 9(02). (Return Code)
        05  PPS-CHRG-THRESHOLD            PIC 9(07)V9(02). (Charge Threshold)
        ... many more numeric fields for results ...
    01  PPS-CBSA                           PIC X(05). (CBSA Code)
    01  PRICER-OPT-VERS-SW. (Pricer Option and Version Switch)
        05  PRICER-OPTION-SW          PIC X(01).
            88  ALL-TABLES-PASSED          VALUE 'A'.
            88  PROV-RECORD-PASSED         VALUE 'P'.
        05  PPS-VERSIONS.
            10  PPDRV-VERSION         PIC X(05). (Version of PPDRV program)
    01  PROV-NEW-HOLD. (Provider Data passed from calling program)
        02  PROV-NEWREC-HOLD1.
            05  P-NEW-NPI10.
                10  P-NEW-NPI8             PIC X(08). (Provider NPI)
                10  P-NEW-NPI-FILLER       PIC X(02).
            05  P-NEW-PROVIDER-NO.
                10  P-NEW-STATE            PIC 9(02). (Provider State)
                10  FILLER                 PIC X(04).
            05  P-NEW-DATE-DATA.
                10  P-NEW-EFF-DATE. (Effective Date)
                    15  P-NEW-EFF-DT-CC    PIC 9(02).
                    15  P-NEW-EFF-DT-YY    PIC 9(02).
                    15  P-NEW-EFF-DT-MM    PIC 9(02).
                    15  P-NEW-EFF-DT-DD    PIC 9(02).
                10  P-NEW-FY-BEGIN-DATE. (Fiscal Year Begin Date)
                    15  P-NEW-FY-BEG-DT-CC PIC 9(02).
                    15  P-NEW-FY-BEG-DT-YY PIC 9(02).
                    15  P-NEW-FY-BEG-DT-MM PIC 9(02).
                    15  P-NEW-FY-BEG-DT-DD PIC 9(02).
                10  P-NEW-REPORT-DATE. (Report Date)
                    15  P-NEW-REPORT-DT-CC PIC 9(02).
                    15  P-NEW-REPORT-DT-YY PIC 9(02).
                    15  P-NEW-REPORT-DT-MM PIC 9(02).
                    15  P-NEW-REPORT-DT-DD PIC 9(02).
                10  P-NEW-TERMINATION-DATE. (Termination Date)
                    15  P-NEW-TERM-DT-CC   PIC 9(02).
                    15  P-NEW-TERM-DT-YY   PIC 9(02).
                    15  P-NEW-TERM-DT-MM   PIC 9(02).
                    15  P-NEW-TERM-DT-DD   PIC 9(02).
            05  P-NEW-WAIVER-CODE          PIC X(01). (Waiver Code)
                88  P-NEW-WAIVER-STATE       VALUE 'Y'.
            05  P-NEW-INTER-NO             PIC 9(05). (Internship Number)
            05  P-NEW-PROVIDER-TYPE        PIC X(02). (Provider Type)
            05  P-NEW-CURRENT-CENSUS-DIV   PIC 9(01).
            05  P-NEW-CURRENT-DIV REDEFINES P-NEW-CURRENT-CENSUS-DIV PIC 9(01).
            05  P-NEW-MSA-DATA.
                10  P-NEW-CHG-CODE-INDEX       PIC X.
                10  P-NEW-GEO-LOC-MSAX         PIC X(04) JUST RIGHT.
                10  P-NEW-GEO-LOC-MSA9 REDEFINES P-NEW-GEO-LOC-MSAX PIC 9(04).
                10  P-NEW-WAGE-INDEX-LOC-MSA   PIC X(04) JUST RIGHT.
                10  P-NEW-STAND-AMT-LOC-MSA    PIC X(04) JUST RIGHT.
                10  P-NEW-STAND-AMT-LOC-MSA9 REDEFINES P-NEW-STAND-AMT-LOC-MSA.
                    15  P-NEW-RURAL-1ST.
                        20  P-NEW-STAND-RURAL  PIC XX.
                            88  P-NEW-STD-RURAL-CHECK VALUE '  '.
                    15  P-NEW-RURAL-2ND        PIC XX.
            05  P-NEW-SOL-COM-DEP-HOSP-YR PIC XX.
            05  P-NEW-LUGAR                    PIC X.
            05  P-NEW-TEMP-RELIEF-IND          PIC X.
            05  P-NEW-FED-PPS-BLEND-IND        PIC X.
            05  FILLER                         PIC X(05).
        02  PROV-NEWREC-HOLD2.
            05  P-NEW-VARIABLES.
                10  P-NEW-FAC-SPEC-RATE     PIC  9(05)V9(02). (Facility Specific Rate)
                10  P-NEW-COLA              PIC  9(01)V9(03). (COLA)
                10  P-NEW-INTERN-RATIO      PIC  9(01)V9(04). (Internship Ratio)
                10  P-NEW-BED-SIZE          PIC  9(05). (Bed Size)
                10  P-NEW-OPER-CSTCHG-RATIO PIC  9(01)V9(03). (Operating Cost-to-Charge Ratio)
                10  P-NEW-CMI               PIC  9(01)V9(04).
                10  P-NEW-SSI-RATIO         PIC  V9(04). (SSI Ratio)
                10  P-NEW-MEDICAID-RATIO    PIC  V9(04). (Medicaid Ratio)
                10  P-NEW-PPS-BLEND-YR-IND  PIC  9(01). (PPS Blend Year Indicator)
                10  P-NEW-PRUF-UPDTE-FACTOR PIC  9(01)V9(05).
                10  P-NEW-DSH-PERCENT       PIC  V9(04). (DSH Percent)
                10  P-NEW-FYE-DATE          PIC  X(08). (Fiscal Year End Date)
            05  P-NEW-SPECIAL-PAY-IND         PIC X(01). (Special Pay Indicator)
            05  FILLER                        PIC X(01).
            05  P-NEW-GEO-LOC-CBSAX           PIC X(05) JUST RIGHT.
            05  P-NEW-GEO-LOC-CBSA9 REDEFINES P-NEW-GEO-LOC-CBSAX PIC 9(05).
            05  P-NEW-GEO-LOC-CBSA-AST REDEFINES P-NEW-GEO-LOC-CBSA9.
                10 P-NEW-GEO-LOC-CBSA-1ST     PIC X.
                10 P-NEW-GEO-LOC-CBSA-2ND     PIC X.
                10 P-NEW-GEO-LOC-CBSA-3RD     PIC X.
                10 P-NEW-GEO-LOC-CBSA-4TH     PIC X.
                10 P-NEW-GEO-LOC-CBSA-5TH     PIC X.
            05  FILLER                        PIC X(10).
            05  P-NEW-SPECIAL-WAGE-INDEX      PIC 9(02)V9(04). (Special Wage Index)
        02  PROV-NEWREC-HOLD3.
            05  P-NEW-PASS-AMT-DATA.
                10  P-NEW-PASS-AMT-CAPITAL    PIC 9(04)V99.
                10  P-NEW-PASS-AMT-DIR-MED-ED PIC 9(04)V99.
                10  P-NEW-PASS-AMT-ORGAN-ACQ  PIC 9(04)V99.
                10  P-NEW-PASS-AMT-PLUS-MISC  PIC 9(04)V99.
            05  P-NEW-CAPI-DATA.
                15  P-NEW-CAPI-PPS-PAY-CODE   PIC X.
                15  P-NEW-CAPI-HOSP-SPEC-RATE PIC 9(04)V99.
                15  P-NEW-CAPI-OLD-HARM-RATE  PIC 9(04)V99.
                15  P-NEW-CAPI-NEW-HARM-RATIO PIC 9(01)V9999.
                15  P-NEW-CAPI-CSTCHG-RATIO   PIC 9V999.
                15  P-NEW-CAPI-NEW-HOSP       PIC X.
                15  P-NEW-CAPI-IME            PIC 9V9999.
                15  P-NEW-CAPI-EXCEPTIONS     PIC 9(04)V99.
            05  FILLER                        PIC X(22).
    01  WAGE-NEW-INDEX-RECORD. (Wage Index Record)
        05  W-CBSA                        PIC X(5). (CBSA Code)
        05  W-EFF-DATE                    PIC X(8). (Effective Date)
        05  W-WAGE-INDEX1                 PIC S9(02)V9(04). (Wage Index 1)
        05  W-WAGE-INDEX2                 PIC S9(02)V9(04). (Wage Index 2)
        05  W-WAGE-INDEX3                 PIC S9(02)V9(04). (Wage Index 3)
    01  WAGE-NEW-IPPS-INDEX-RECORD. (IPPS Wage Index Record)
        05  W-CBSA-IPPS.
            10 CBSA-IPPS-123              PIC X(3).
            10 CBSA-IPPS-45               PIC X(2).
        05  W-CBSA-IPPS-SIZE              PIC X.
            88  LARGE-URBAN       VALUE 'L'.
            88  OTHER-URBAN       VALUE 'O'.
            88  ALL-RURAL         VALUE 'R'.
        05  W-CBSA-IPPS-EFF-DATE          PIC X(8). (Effective Date)
        05  FILLER                        PIC X.
        05  W-IPPS-WAGE-INDEX             PIC S9(02)V9(04). (IPPS Wage Index)
        05  W-IPPS-PR-WAGE-INDEX          PIC S9(02)V9(04). (PR IPPS Wage Index)

### Program: LTCAL091

*   **Files Accessed:** Similar to LTCAL087, uses files implied by `COPY` statements (`LTDRG086`, `IPDRG080`).
*   **WORKING-STORAGE SECTION:** Very similar to LTCAL087, the main difference is the `CAL-VERSION` which is 'V09.1'. The copied data structures will also reflect the year's changes.
*   **LINKAGE SECTION:** Identical to LTCAL087.

### Program: LTCAL094

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG093`, `IPDRG090`, `IRFBN091`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL087 and LTCAL091 but with `CAL-VERSION` as 'V09.4'. The copied data structures will reflect changes for the year. Note the addition of `P-VAL-BASED-PURCH-SCORE` in `PROV-NEWREC-HOLD3`.
*   **LINKAGE SECTION:** Identical to LTCAL087.

### Program: LTCAL095

*   **Files Accessed:** Uses files implied by `COPY` statements (`LTDRG095`, `IPDRG090`, `IRFBN091`).
*   **WORKING-STORAGE SECTION:** Similar to LTCAL094; `CAL-VERSION` is 'V09.5'. The copied data structures will reflect changes for the year.
*   **LINKAGE SECTION:** Identical to LTCAL087.

### Program: LTDRG080

*   **Files Accessed:** None. This program defines a table within WORKING-STORAGE.
*   **WORKING-STORAGE SECTION:**
    ```cobol
    01  W-DRG-FILLS. (Filler for DRG data)
        03  PIC X(45) VALUE ... (Repeated lines containing DRG data)
    01  W-DRG-TABLE REDEFINES W-DRG-FILLS. (Redefines the filler as a table)
        03  WWM-ENTRY OCCURS 530 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX.
            05  WWM-DRG             PIC X(3). (DRG Code)
            05  WWM-RELWT           PIC 9(1)V9(4). (Relative Weight)
            05  WWM-ALOS            PIC 9(2)V9(1). (Average Length of Stay)
            05  WWM-IPTHRESH        PIC 9(3)V9(1). (IPPS Threshold)
    ```
*   **LINKAGE SECTION:** None.

### Program: LTDRG086

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG080, but with different data and 735 occurrences of WWM-ENTRY.
*   **LINKAGE SECTION:** None.

### Program: LTDRG093

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG086, but with different data.
*   **LINKAGE SECTION:** None.

### Program: LTDRG095

*   **Files Accessed:** None.
*   **WORKING-STORAGE SECTION:** Similar structure to LTDRG093, but with different data.
*   **LINKAGE SECTION:** None.

### Program: IPDRG063

*   **Files Accessed:** None explicitly defined in the provided code.
*   **Working-Storage Section:**
    *   `01 DRG-TABLE`: A table containing DRG data.
        *   `05 D-TAB`: A level 05 item that holds the raw DRG data as a packed string.
        *   `05 DRGX-TAB REDEFINES D-TAB`: A redefinition of `D-TAB` to structure the data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (likely a year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date for the period.
                *   `15 DRG-DATA OCCURS 560 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: Weight of the DRG.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed (likely for outlier calculations).
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **Linkage Section:** None.

### Program: IPDRG071

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

### Program: LTCAL064

*   **Files Accessed:** None explicitly defined. The `COPY LTDRG062.` statement suggests it uses data from a file or table defined in the `LTDRG062` copybook.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: A comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Constants for federal fiscal year beginnings.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook, which contains a DRG table (`WWM-ENTRY`).
    *   `01 HOLD-PPS-COMPONENTS`: Variables to hold intermediate PPS calculation results.
    *   Several numeric and alphanumeric variables for PPS calculations (H-LOS, H-REG-DAYS, H-TOTAL-DAYS, etc.) and payment amounts.
    *   `01 PPS-CBSA`: CBSA code (Census Bureau Area).
    *   `01 PRICER-OPT-VERS-SW`: Flags indicating which tables were passed.
    *   `01 PROV-NEW-HOLD`: Structure to hold provider data. Contains numerous fields related to provider information (NPI, provider number, effective dates, etc.).
    *   `01 WAGE-NEW-INDEX-RECORD`: Structure to hold wage index data.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data passed from a calling program. Includes fields for provider information, DRG code, length of stay, discharge date, and charges.
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program. Contains return codes, payment amounts, and other calculated values.
    *   `01 PROV-NEW-HOLD`: Provider data passed to the program (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data passed to the program (same as in Working-Storage).

### Program: LTCAL072

*   **Files Accessed:** None explicitly defined. Uses data from copybooks `LTDRG062` and `IPDRG063`.
*   **Working-Storage Section:**
    *   `01 W-STORAGE-REF`: Comment field.
    *   `01 CAL-VERSION`: Program version.
    *   `01 PROGRAM-CONSTANTS`: Federal fiscal year beginning dates.
    *   `COPY LTDRG062`: Includes the `LTDRG062` copybook (LTCH DRG table).
    *   `COPY IPDRG063`: Includes the `IPDRG063` copybook (IPPS DRG table).
    *   `01 HOLD-PPS-COMPONENTS`: Holds intermediate calculation results, expanded to include many more variables for short-stay outlier calculations.
    *   Numerous variables for PPS calculations (H-LOS, H-REG-DAYS, etc.), payment amounts, COLA, wage indices, and other factors involved in the more complex calculations in this version.
    *   `01 PPS-CBSA`: CBSA code.
    *   `01 PRICER-OPT-VERS-SW`: Flags for passed tables.
    *   `01 PROV-NEW-HOLD`: Provider data.
    *   `01 WAGE-NEW-INDEX-RECORD`: Wage index data for LTCH.
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data for IPPS.
*   **Linkage Section:**
    *   `01 BILL-NEW-DATA`: Bill data from a calling program (updated to numeric DRG-CODE in this version).
    *   `01 PPS-DATA-ALL`: PPS calculation results returned to the calling program.
    *   `01 PROV-NEW-HOLD`: Provider data (same as in Working-Storage).
    *   `01 WAGE-NEW-INDEX-RECORD`: LTCH wage index data (same as in Working-Storage).
    *   `01 WAGE-NEW-IPPS-INDEX-RECORD`: IPPS wage index data (same as in Working-Storage).

### Programs: LTCAL075 and LTCAL080

The analysis for LTCAL075 and LTCAL080 would be very similar to LTCAL072, with incremental changes in constants, rates, and potentially some additional variables or calculations reflecting the evolving payment methodologies and data structures across the versions. The main differences will lie in the values of constants and rates used within the calculations, and potentially a few new variables added to handle the specifics of the newer versions. The basic structure of the Working-Storage and Linkage Sections will remain consistent, maintaining the same data structures and copybook inclusions. The comments in the code itself will provide a clear indication of those differences.

### Program: LTDRG062

*   **Files Accessed:** None explicitly defined.
*   **Working-Storage Section:**
    *   `01 W-DRG-FILLS`: Contains the raw data for the LTCH DRG table as packed strings.
    *   `01 W-DRG-TABLE REDEFINES W-DRG-FILLS`: Redefines `W-DRG-FILLS` to structure the data.
        *   `03 WWM-ENTRY OCCURS 518 TIMES ASCENDING KEY IS WWM-DRG INDEXED BY WWM-INDX`: The LTCH DRG table.
            *   `05 WWM-DRG PIC X(3)`: DRG code.
            *   `05 WWM-RELWT PIC 9(1)V9(4)`: Relative weight.
            *   `05 WWM-ALOS PIC 9(2)V9(1)`: Average length of stay.
*   **Linkage Section:** None.

### Programs: LTDRG075 and LTDRG080

Similar to LTDRG062, these copybooks define DRG tables. LTDRG075 and LTDRG080 will have a similar structure, but they will contain updated DRG codes, relative weights, average lengths of stay, and potentially additional fields (as seen in LTDRG080 adding `WWM-IPTHRESH`). The number of `WWM-ENTRY` occurrences may also change to reflect updates in the DRG tables.

### Program: LTCAL043

*   **Files Accessed:** None explicitly defined in the `FILE-CONTROL` section. The program uses a COPY statement to include `LTDRG041`, which implies access to data defined within that copied file (likely a DRG table).
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: A 46-character text string used for identifying the working storage section. It's a comment field.
    *   `CAL-VERSION`: A 5-character string holding the version number 'C04.3'.
    *   `LTDRG041`: This is a copy of another COBOL program or data structure. The structure is defined below.
       *   `WWM-ENTRY`: An array (occurs 510 times) containing DRG-related data. Each entry has:
          *   `WWM-DRG`: A 3-character DRG code.
          *   `WWM-RELWT`: A relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
    *   `HOLD-PPS-COMPONENTS`: A structure holding intermediate calculation results for Prospective Payment System (PPS) calculations. Contains various numeric fields representing Length of Stay (LOS), Regular Days, Total Days, Short Stay Outlier Threshold (SSOT), and blended payment amounts, etc.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: A structure passed to and from the calling program, containing bill information.
       *   `B-NPI10`: National Provider Identifier (NPI), including filler.
          *   `B-NPI8`: NPI (8 characters).
          *   `B-NPI-FILLER`: Filler (2 characters).
       *   `B-PROVIDER-NO`: Provider number (6 characters).
       *   `B-PATIENT-STATUS`: Patient status (2 characters).
       *   `B-DRG-CODE`: DRG code (3 characters).
       *   `B-LOS`: Length of stay (3 numeric digits).
       *   `B-COV-DAYS`: Covered days (3 numeric digits).
       *   `B-LTR-DAYS`: Lifetime reserve days (2 numeric digits).
       *   `B-DISCHARGE-DATE`: Discharge date (CCYYMMDD).
          *   `B-DISCHG-CC`: Century.
          *   `B-DISCHG-YY`: Year.
          *   `B-DISCHG-MM`: Month.
          *   `B-DISCHG-DD`: Day.
       *   `B-COV-CHARGES`: Covered charges (7 numeric digits with 2 decimals).
       *   `B-SPEC-PAY-IND`: Special payment indicator (1 character).
       *   `FILLER`: Filler (13 characters).
    *   `PPS-DATA-ALL`: A structure containing PPS calculation results. Includes return code (`PPS-RTC`), threshold values, MSA, Wage Index, Average LOS, Relative Weight, outlier payments, final payment amounts, and other data.
    *   `PRICER-OPT-VERS-SW`: Structure indicating which pricing tables and versions were used.
       *   `PRICER-OPTION-SW`: Indicates if all tables were passed.
       *   `PPS-VERSIONS`: Contains version numbers.
          *   `PPDRV-VERSION`: Version number.
    *   `PROV-NEW-HOLD`: A structure holding provider-specific data. Contains NPI, provider number, various dates (effective, FY begin, report, termination), waiver code, other codes, and various provider-specific variables and cost data.
    *   `WAGE-NEW-INDEX-RECORD`: Structure containing wage index data.
       *   `W-MSA`: MSA code (4 characters).
       *   `W-EFF-DATE`: Effective date (8 characters).
       *   `W-WAGE-INDEX1`, `W-WAGE-INDEX2`: Wage index values (numeric with 2 digits before and 4 after the decimal).

### Program: LTCAL058

*   **Files Accessed:** Similar to LTCAL043, no files are explicitly defined; it uses `COPY LTDRG041`, implying access to the DRG table data.
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

### Program: LTCAL059

*   **Files Accessed:** Uses `COPY LTDRG057`, implying access to a DRG table defined in that copy.
*   **Working-Storage Section:**
    *   `W-STORAGE-REF`: Working storage identification comment.
    *   `CAL-VERSION`: Version number ('V05.9').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRG057`: Copy of DRG table; structure is defined below.
       *   `WWM-ENTRY`: An array (occurs 512 times) containing DRG-related data. Each entry has:
          *   `WWM-DRG`: A 3-character DRG code.
          *   `WWM-RELWT`: A relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
    *   `HOLD-PPS-COMPONENTS`: Structure for holding intermediate PPS calculation results (same as in LTCAL043 and LTCAL058).
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
    *   `PPS-CBSA`: A 5-character field for CBSA (Core Based Statistical Area) code.
*   **Linkage Section:**
    *   `BILL-NEW-DATA`: Bill information (same as in previous programs).
    *   `PPS-DATA-ALL`: PPS calculation results (same as in previous programs).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricing options and versions (same as in previous programs).
    *   `PROV-NEW-HOLD`: Provider-specific data; this program adds a `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX`.
    *   `WAGE-NEW-INDEX-RECORD-CBSA`: Wage index data; this program uses CBSA instead of MSA.

### Program: LTDRG041

*   **Files Accessed:** None. This is a data definition file, not a program.
*   **Working-Storage Section:** This program only contains a data structure.
    *   `W-DRG-FILLS`: This is a table of DRG codes and related information. It's implemented as a series of 44-character strings that are then redefined as a table.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
       *   `WWM-ENTRY`: An array (occurs 510 times) containing DRG-related data. Each entry has:
          *   `WWM-DRG`: A 3-character DRG code.
          *   `WWM-RELWT`: A relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
*   **Linkage Section:** None.

### Program: LTDRG057

*   **Files Accessed:** None. This is also a data definition file.
*   **Working-Storage Section:** Similar to `LTDRG041`, this defines a DRG table.
    *   `W-DRG-FILLS`: Table of DRG codes and related data as a series of 44-character strings.
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table of `WWM-ENTRY` records.
       *   `WWM-ENTRY`: An array (occurs 512 times) of records, each containing:
          *   `WWM-DRG`: 3-character DRG code.
          *   `WWM-RELWT`: Relative weight (numeric with 1 digit before and 4 after the decimal).
          *   `WWM-ALOS`: Average length of stay (numeric with 2 digits before and 1 after the decimal).
*   **Linkage Section:** None.

### Program: IPDRG104, IPDRG110, IPDRG123

*   **Files Accessed:** These programs use `COPY` statements (e.g., `COPY IPDRG104`) implying they include data from external files named `IPDRG104`, `IPDRG110`, and `IPDRG123` respectively. These files likely contain DRG tables.
*   **WORKING-STORAGE SECTION:** Each program defines a `DRG-TABLE` with a structure similar to the following:
    *   `01 DRG-TABLE`:
        *   `05 D-TAB`: Holds DRG data in a packed format.
        *   `05 DRGX-TAB REDEFINES D-TAB`: Redefined structure for accessing the DRG data.
            *   `10 DRGX-PERIOD OCCURS 1 INDEXED BY DX5`: Represents a single period (year).
                *   `15 DRGX-EFF-DATE PIC X(08)`: Effective date.
                *   `15 DRG-DATA OCCURS 1000 INDEXED BY DX6`: DRG data for the period.
                    *   `20 DRG-WT PIC 9(02)V9(04)`: DRG weight.
                    *   `20 DRG-ALOS PIC 9(02)V9(01)`: Average length of stay.
                    *   `20 DRG-DAYS-TRIM PIC 9(02)`: Days trimmed.
                    *   `20 DRG-ARITH-ALOS PIC 9(02)V9(01)`: Arithmetic average length of stay.
*   **LINKAGE SECTION:** None present in the provided code for these programs.

### Program: IRFBN102, IRFBN105

*   **Files Accessed:** These programs use `COPY` statements (`COPY IRFBN102`, `COPY IRFBN105`) indicating they include data from external files containing state-specific Rural Floor Budget Neutrality Factors (RFBNs).
*   **WORKING-STORAGE SECTION:** Both programs define a `PPS-SSRFBN-TABLE` with a similar structure:
    *   `01 PPS-SSRFBN-TABLE`:
        *   `02 WK-SSRFBN-DATA`: Holds RFBN data in a less structured format.
        *   `02 WK-SSRFBN-DATA2 REDEFINES WK-SSRFBN-DATA`: Redefined structure for accessing RFBN data.
            *   `05 SSRFBN-TAB OCCURS 72 ASCENDING KEY IS WK-SSRFBN-STATE INDEXED BY SSRFBN-IDX`: Table of RFBNs, sorted by state code.
                *   `10 WK-SSRFBN-REASON-ALL`: Details for each state.
                    *   `15 WK-SSRFBN-STATE PIC 99`: State code.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-RATE PIC 9(1)V9(5)`: RFBN rate.
                    *   `15 FILLER PIC XX`: Filler.
                    *   `15 WK-SSRFBN-CODE2 PIC 99`: Another code (unclear purpose).
                    *   `15 FILLER PIC X`: Filler.
                    *   `15 WK-SSRFBN-STNAM PIC X(20)`: State name.
                    *   `15 WK-SSRFBN-REST PIC X(22)`: Remaining data (unclear purpose).
    *   Additional message and payment-related fields are also present.
*   **LINKAGE SECTION:** None present in the provided code.

### Program: LTCAL103, LTCAL105, LTCAL111, LTCAL123

*   **Files Accessed:** These programs use `COPY` statements to include data from DRG tables (`LTDRG100`, `LTDRG110`, `LTDRG123`) and IPPS DRG data (`IPDRG104`, `IPDRG110`, `IPDRG123`). LTCAL103 also copies `IRFBN102` for RFBN data. LTCAL111 and LTCAL123 have commented-out RFBN copy statements, suggesting they might not use RFBN data.
*   **WORKING-STORAGE SECTION:** These programs share a common structure with variations in version numbers and copybook inclusions:
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version (e.g., 'V10.3', 'V11.1').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRGxxx` / `IPDRGxxx` (from COPY statements): DRG table data.
    *   `IRFBNxxx` (from COPY statement, if applicable): RFBN data.
    *   `HOLD-PPS-COMPONENTS`: Holds intermediate PPS calculation results (LOS, days, rates, etc.).
    *   `PPS-DATA-ALL`: Holds final PPS calculation results (return code, thresholds, etc.).
    *   `PPS-CBSA`: CBSA code.
    *   `PRICER-OPT-VERS-SW`: Pricer option and version switches.
    *   `PROV-NEW-HOLD`: Provider-specific data (NPI, provider number, dates, waiver code, rates, etc.).
    *   `WAGE-NEW-INDEX-RECORD` / `WAGE-NEW-IPPS-INDEX-RECORD`: Wage index data.
*   **LINKAGE SECTION:** The linkage sections are largely consistent, primarily passing bill data and receiving PPS results:
    *   `BILL-NEW-DATA`: Bill data (NPI, provider number, DRG, LOS, discharge date, charges, etc.).
    *   `PPS-DATA-ALL`: PPS calculation results.

### Program: LTDRG100, LTDRG110, LTDRG123

*   **Files Accessed:** None explicitly. These are copybooks defining DRG tables.
*   **WORKING-STORAGE SECTION:** Each defines a DRG table structure:
    *   `W-DRG-FILLS`: Packed DRG data.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS n TIMES`: DRG code (`WWM-DRG`), relative weight (`WWM-RELWT`), average length of stay (`WWM-ALOS`). The number of occurrences (`n`) varies (736, 737, 742 respectively).
*   **LINKAGE SECTION:** None.

### Program: LTCAL043, LTCAL058, LTCAL059, LTCAL063

*   **Files Accessed:** These programs use `COPY` statements to include DRG table data from `LTDRG041` and `LTDRG057`. LTCAL063 also includes `PPS-CBSA` in its working storage.
*   **WORKING-STORAGE SECTION:** Common structures include:
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version number (e.g., 'C04.3', 'V05.8', 'V05.9', 'V06.3').
    *   `PROGRAM-CONSTANTS`: Federal fiscal year begin dates.
    *   `LTDRGxxx` (from COPY statements): DRG table data.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results.
    *   `PPS-CBSA` (in LTCAL063): CBSA code.
*   **LINKAGE SECTION:** Consistent across these programs:
    *   `BILL-NEW-DATA`: Bill data (NPI, provider number, DRG, LOS, discharge date, charges).
    *   `PPS-DATA-ALL`: PPS calculation results.
    *   `PRICER-OPT-VERS-SW`: Pricer options and versions.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD` (or `WAGE-NEW-INDEX-RECORD-CBSA` in LTCAL063): Wage index data.

### Program: LTDRG041, LTDRG057

*   **Files Accessed:** None explicitly. These are data definition files (copybooks).
*   **WORKING-STORAGE SECTION:** Both define DRG tables:
    *   `W-DRG-FILLS`: Packed DRG data.
    *   `W-DRG-TABLE REDEFINES W-DRG-FILLS`: Table of `WWM-ENTRY` records.
        *   `WWM-ENTRY OCCURS n TIMES`: DRG code (`WWM-DRG`), relative weight (`WWM-RELWT`), average length of stay (`WWM-ALOS`). Occurrences vary (510 for LTDRG041, 512 for LTDRG057).
*   **LINKAGE SECTION:** None.

### Program: LTCAL032, LTCAL042

*   **Files Accessed:** None explicitly defined. Both rely on `COPY LTDRG031` for DRG table data.
*   **Working-Storage Section:** Similar structures for both, with differences in version numbers and specific hardcoded calculation values:
    *   `W-STORAGE-REF`: Comment field.
    *   `CAL-VERSION`: Program version ('C03.2' for LTCAL032, 'C04.2' for LTCAL042).
    *   `LTDRG031` (from COPY): DRG table data.
    *   `HOLD-PPS-COMPONENTS`: Intermediate PPS calculation results (LOS, days, SSOT, etc.). LTCAL042 adds `H-LOS-RATIO`.
    *   `PRICER-OPT-VERS-SW`: Version and pricing option switches.
    *   `PROV-NEW-HOLD`: Provider-specific data.
    *   `WAGE-NEW-INDEX-RECORD`: Wage index data.
    *   Specific constants differ (e.g., `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`).
*   **Linkage Section:** Identical for both programs:
    *   `BILL-NEW-DATA`: Bill data (NPI, Provider Number, Patient Status, DRG Code, LOS, Covered Days, Lifetime Reserve Days, Discharge Date, Covered Charges, Special Pay Indicator).
    *   `PPS-DATA-ALL`: Calculated PPS data (RTC, Charge Threshold, MSA, Wage Index, Average LOS, Relative Weight, Outlier Pay Amount, etc.).

### Program: LTDRG031

*   **Files Accessed:** This is a copybook; it doesn't directly access any files. It defines a data structure used by other programs to access DRG data.
*   **Working-Storage Section:**
    *   `W-DRG-FILLS`: Literals representing DRG table data (44 characters each).
    *   `W-DRG-TABLE`: Redefines `W-DRG-FILLS` as a table (`WWM-ENTRY`) of DRG codes, relative weights, and average lengths of stay.
*   **Linkage Section:** None.

### Overall Program Flow Summary:

The analyzed programs form a processing chain for healthcare claims, primarily focusing on Prospective Payment System (PPS) calculations.

1.  **LTMGR212:** Acts as a driver program. It reads billing records from `BILLFILE`, prepares data, calls `LTOPN212` for payment calculations, and formats results for the `PRTOPER` output file.
2.  **LTOPN212:** Manages the loading of various lookup tables, including provider and wage index data from multiple input files (`PROV-FILE`, `CBSAX-FILE`, `IPPS-CBSAX-FILE`, `MSAX-FILE`). It then calls `LTDRV212` to perform the core payment calculations.
3.  **LTDRV212:** Orchestrates the payment calculation logic. It determines the appropriate wage index based on discharge date and provider information and then calls version-specific `LTCAL` modules (e.g., `LTCAL032`, `LTCAL162`, etc.) to perform the actual payment computations based on the fiscal year.
4.  **LTCALxxx Programs:** These modules perform the detailed PPS calculations. They utilize DRG tables (e.g., `LTDRGxxx`, `IPDRGxxx`) and potentially other rate/factor tables (e.g., `IRFBNxxx`) loaded via COPY statements or passed as parameters. They receive bill and provider data via the linkage section and return calculated payment data.
5.  **DRG Copybooks (e.g., LTDRG041, IPDRG160):** These are data definition files that contain DRG codes, relative weights, and average lengths of stay, often as hardcoded tables within the copybook. They are included in other programs via `COPY` statements.
6.  **Other Data Copybooks (e.g., RUFL200):** Define specific data structures, such as rural floor adjustment tables, used in calculations.

The extensive use of versioned `LTCAL` programs and the variety of DRG table copybooks (e.g., `IPDRG160`, `IPDRG170`, etc.) indicate a system that has been updated and maintained over many years to accommodate changes in healthcare payment regulations and methodologies. The presence of `COPY` statements highlights a modular design, where data structures and potentially some logic are shared across programs.

**Important Note on Data:** The long strings of numeric data within `FILLER` fields in programs like `IPDRG080` and `IPDRG090`, and the `W-DRG-FILLS` fields in `LTDRG` programs, strongly suggest these are encoded or packed tables. A more detailed analysis would be required to decode and fully understand the specific data points within these fields. The absence of explicit `FILE SECTION` entries in most snippets means file I/O details are handled by calling programs or through dynamic means not shown here.