## Program Overview

This document consolidates and analyzes the program descriptions extracted from multiple functional specification files, providing a comprehensive overview of the Long-Term Care Prospective Payment System (LTCH PPS) and Inpatient Prospective Payment System (IPPS) related COBOL programs. The programs are primarily involved in calculating Medicare payments for LTCH claims, utilizing various data tables for DRG information, wage indices, and other payment factors.

### Core Processing Programs

These programs perform the primary calculation and processing of LTCH claims.

**1. LTMGR212**

*   **Overview:** This program acts as a driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to `PRTOPER`. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   `BILL-NEW-DATA`: Bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   `PPS-DATA-ALL`: Pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   `PPS-CBSA`: Core Based Statistical Area code.
        *   `PPS-PAYMENT-DATA`: Calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   `PRICER-OPT-VERS-SW`: Pricing option and version information (option switch, PPDRV version).

**2. LTOPN212**

*   **Overview:** This subroutine is a key component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module for pricing calculations. It manages data flow and table loading before passing control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   `BILL-NEW-DATA`: (Same as in LTMGR212).
        *   `PPS-DATA-ALL`: (Same as in LTMGR212).
        *   `PPS-CBSA`: (Same as in LTMGR212).
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212).
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212).
        *   `PROV-RECORD-FROM-USER`: (Same as in LTMGR212).
        *   `CBSAX-TABLE-FROM-USER`: CBSA wage index table.
        *   `IPPS-CBSAX-TABLE-FROM-USER`: IPPS CBSA wage index table.
        *   `MSAX-TABLE-FROM-USER`: MSA wage index table.
        *   `WORK-COUNTERS`: Record counts for CBSA, MSA, provider, and IPPS CBSA.

**3. LTDRV212**

*   **Overview:** This module is central to LTCH PPS payment calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (based on the bill's fiscal year) for final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes for error and exception management.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Numerous calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   `BILL-NEW-DATA`: (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years).
        *   `PPS-DATA-ALL`: (Same as in LTMGR212).
        *   `PPS-CBSA`: (Same as in LTMGR212).
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212).
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212).
        *   `PROV-NEW-HOLD`: Provider record.
        *   `WAGE-NEW-INDEX-RECORD-CBSA`: CBSA wage index data (CBSA, effective date, wage index values).
        *   `WAGE-IPPS-INDEX-RECORD-CBSA`: IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` is due to its handling of numerous versions of the `LTCAL` modules, each for a specific fiscal year. Data structures passed remain largely consistent, with minor variations across `LTCAL` versions. Extensive conditional logic is crucial for selecting the correct `LTCAL` module and managing rate year transitions.

**4. LTCALxxx (Various Versions)**

These programs perform the core LTCH PPS payment calculations for specific fiscal years, utilizing various data tables.

*   **LTCAL032 (Version C03.2)**
    *   **Overview:** Calculates PPS payments for LTC claims based on Length of Stay (LOS), DRG code, covered days, and outlier thresholds. It handles short-stay and outlier payments, and incorporates blend year calculations.
    *   **Business Functions:** LTC Claim Processing, PPS Calculation, Short-Stay Payment Calculation, Outlier Payment Calculation, Blend Year Calculation, Data Validation and Error Handling.
    *   **Called Programs & Data Structures:**
        *   `LTDRG031` (included via COPY): Uses `WWM-ENTRY` (containing `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) for DRG lookups.

*   **LTCAL042 (Version C04.2)**
    *   **Overview:** Similar to LTCAL032, but a later version (C04.2) with updates to payment methodologies, rules, or data structures. Includes special handling for provider '332006'.
    *   **Business Functions:** LTC Claim Processing, PPS Calculation, Short-Stay Payment Calculation (with special logic for provider '332006'), Outlier Payment Calculation, Blend Year Calculation, Data Validation and Error Handling, Special Provider Handling.
    *   **Called Programs & Data Structures:**
        *   `LTDRG031` (included via COPY): Uses `WWM-ENTRY` (containing `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) for DRG lookups.

*   **LTCAL103**
    *   **Overview:** Calculates LTCH PPS payments using various data tables. Performs edits and validations, outlier and blended payment calculations.
    *   **Business Functions:** LTCH PPS Payment Calculation, Data Validation, Outlier Payment Calculation, Blended Payment Calculation.
    *   **Called Programs & Data Structures:** Uses data from:
        *   `LTDRG100` (via COPY): LTCH DRG table (`WWM-ENTRY` with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
        *   `IPDRG104` (via COPY): IPPS DRG table (`DRGX-TAB` with `DRGX-EFF-DATE`, `DRG-WT`, `DRG-ALOS`, `DRG-DAYS-TRIM`, `DRG-ARITH-ALOS`).
        *   `IRFBN102` (via COPY): IPPS State-Specific Rural Floor Budget Neutrality Factors (SSRFBN-TAB with WK-SSRFBN-STATE, WK-SSRFBN-RATE, WK-SSRFBN-CODE2, WK-SSRFBN-STNAM, WK-SSRFBN-REST).
        *   `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures are used.

*   **LTCAL105**
    *   **Overview:** A revised version of LTCAL103, likely with updated payment rates and calculation logic.
    *   **Business Functions:** Similar to LTCAL103, but with updated constants and potentially updated logic.
    *   **Called Programs & Data Structures:** Uses data from:
        *   `LTDRG100` (via COPY): LTCH DRG table.
        *   `IPDRG104` (via COPY): IPPS DRG table.
        *   `IRFBN105` (via COPY): Updated IPPS State-Specific Rural Floor Budget Neutrality Factors.
        *   `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures are used.

*   **LTCAL111**
    *   **Overview:** A revision of the LTCH PPS payment calculation program, effective October 1, 2010. Does not appear to use a state-specific RFBN table.
    *   **Business Functions:** Similar to LTCAL103 and LTCAL105, but with potentially different rate constants and calculation logic.
    *   **Called Programs & Data Structures:** Uses data from:
        *   `LTDRG110` (via COPY): LTCH DRG table.
        *   `IPDRG110` (via COPY): IPPS DRG table.
        *   `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures are used.

*   **LTCAL123**
    *   **Overview:** The latest version (as of snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. Does not appear to use a state-specific RFBN table.
    *   **Business Functions:** Similar to previous LTCAL programs, with updated constants and potentially refined logic.
    *   **Called Programs & Data Structures:** Uses data from:
        *   `LTDRG123` (via COPY): LTCH DRG table.
        *   `IPDRG123` (via COPY): IPPS DRG table.
        *   `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures are used.

*   **LTCAL162**
    *   **Overview:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
    *   **Business Functions:** Reads LTCH claim data, Validates claim data, Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended), Calculates high-cost outliers, Determines appropriate return codes, Writes results to output data structures.
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data (`LTDRV...`, `LTWIX...`). Passes `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD` to itself (implicitly for processing).

*   **LTCAL170**
    *   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170` and `IPDRG170` tables. Handles budget neutrality adjustments for site-neutral payments.
    *   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including budget neutrality adjustments for site-neutral payments.
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data. Passes analogous data structures to `LTCAL162`.

*   **LTCAL183**
    *   **Overview:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables. Notes significant changes in short-stay outlier and Subclause II handling.
    *   **Business Functions:** Similar to previous LTCAL programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data. Passes analogous data structures to previous LTCAL programs.

*   **LTCAL190**
    *   **Overview:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and `LTDRG190` and `IPDRG190` tables.
    *   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data. Passes analogous data structures to previous LTCAL programs.

*   **LTCAL202**
    *   **Overview:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
    *   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data. Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

*   **LTCAL212**
    *   **Overview:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
    *   **Business Functions:** Similar to previous LTCAL programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
    *   **Called Programs & Data Structures:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

### Data Definition Programs (Copybooks/Tables)

These programs define data structures and tables that are used by the core processing programs. They do not execute independently but are included in other programs via COPY statements.

**1. RUFL200**

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

**2. IPDRGxxx (Various Versions)**

These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for different years. They are called by `LTCAL` programs to retrieve DRG information.

*   **IPDRG160 (2015 IPPS DRG Table)**
    *   **Overview:** Defines a table (`PPS-DRG-TABLE`) with IPPS DRG data for 2015, including DRG codes, weights, average lengths of stay (ALOS), and descriptions.
    *   **Business Functions:** Stores IPPS DRG data for 2015, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is *called* by other programs (like `LTCAL162`) to retrieve DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG170 (2016 IPPS DRG Table)**
    *   **Overview:** Defines an IPPS DRG table for 2016.
    *   **Business Functions:** Stores IPPS DRG data for 2016, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** Called by other programs to retrieve 2016 DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG181 (2017 IPPS DRG Table)**
    *   **Overview:** Defines an IPPS DRG table for 2017.
    *   **Business Functions:** Stores IPPS DRG data for 2017, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** Called by other programs to retrieve 2017 DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG190 (2018 IPPS DRG Table)**
    *   **Overview:** Defines an IPPS DRG table for 2018.
    *   **Business Functions:** Stores IPPS DRG data for 2018, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** Called by other programs to retrieve 2018 DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG200 (2019 IPPS DRG Table)**
    *   **Overview:** Defines an IPPS DRG table for 2019.
    *   **Business Functions:** Stores IPPS DRG data for 2019, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** Called by other programs to retrieve 2019 DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG211 (2020 IPPS DRG Table)**
    *   **Overview:** Defines an IPPS DRG table for 2020.
    *   **Business Functions:** Stores IPPS DRG data for 2020, Provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** Called by other programs to retrieve 2020 DRG information. Data structure passed *from* it is `DRG-DATA-TAB`.

*   **IPDRG104 (IPPS DRG Data Table)**
    *   **Overview:** Defines a table (`DRG-TABLE`) with IPPS DRG data, including an effective date and multiple sets of weight, ALOS, trimmed days, and arithmetic ALOS values.
    *   **Business Functions:** Data storage and retrieval of IPPS DRG data, potentially used in calculating reimbursement amounts.
    *   **Other Programs Called:** None directly called; it's a data definition program meant to be called by others.

*   **IPDRG110 (IPPS DRG Data Table)**
    *   **Overview:** Defines a table (`DRG-TABLE`) containing IPPS DRG data with an effective date of '20101001'. A subsequent version or update of the DRG table.
    *   **Business Functions:** Identical to IPDRG104.
    *   **Other Programs Called:** None directly called; it's a data definition program.

*   **IPDRG123 (IPPS DRG Data Table)**
    *   **Overview:** Defines a table (`DRG-TABLE`) containing IPPS DRG data with an effective date of '20111001'. A further update of the DRG data.
    *   **Business Functions:** Identical to IPDRG104.
    *   **Other Programs Called:** None directly called; it's a data definition program.

**3. LTDRGxxx (Various Versions)**

These programs define tables containing Long-Term Care Hospital (LTCH) DRG data for different years. They are used by the `LTCAL` programs.

*   **LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**
    *   **Overview:** These are data tables containing LTCH DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Business Functions:** These tables store LTCH DRG data for lookups.
    *   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. Data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

*   **LTDRG031**
    *   **Overview:** Defines a DRG lookup table (`WWM-ENTRY`) mapping DRG codes (`WWM-DRG`) to relative weights (`WWM-RELWT`) and average lengths of stay (`WWM-ALOS`). Initialized using literal values.
    *   **Business Functions:** DRG Lookup Table Definition.
    *   **Called Programs & Data Structures:** This program does not call any other programs. It defines data structures used by other programs via COPY statements.

*   **LTDRG100**
    *   **Overview:** Defines a table (`W-DRG-TABLE`) containing LTCH DRG data, encoded in `W-DRG-FILLS` and redefined.
    *   **Business Functions:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
    *   **Other Programs Called:** None; this is a data definition program.

*   **LTDRG110**
    *   **Overview:** A revised LTCH DRG table, likely reflecting changes in DRG definitions or weights.
    *   **Business Functions:** Data storage and retrieval of LTCH DRG data.
    *   **Other Programs Called:** None; this is a data definition program.

*   **LTDRG123**
    *   **Overview:** Another updated LTCH DRG table.
    *   **Business Functions:** Data storage and retrieval of LTCH DRG data.
    *   **Other Programs Called:** None; this is a data definition program.

**4. IRFBNxxx (Various Versions)**

These programs define tables containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs), likely used to adjust payments based on geographic location.

*   **IRFBN102**
    *   **Overview:** Defines a table (`PPS-SSRFBN-TABLE`) containing SSRFBNs, including state codes, rates, and descriptive information.
    *   **Business Functions:** Storage and retrieval of state-specific payment adjustment factors, used to adjust IPPS payments based on state and potentially rural location.
    *   **Other Programs Called:** None directly called; it's a data definition program.

*   **IRFBN105**
    *   **Overview:** A revised version of `IRFBN102`, containing updated SSRFBN data with identical structure but different values, implying an update to rates.
    *   **Business Functions:** Identical to IRFBN102.
    *   **Other Programs Called:** None directly called; it's a data definition program.

### Important Considerations:

*   **COPY Statements:** The extensive use of `COPY` statements indicates that these programs rely heavily on external data definitions. The actual content of these copied files is crucial for a complete understanding of the programs' functionality. Modifications to copied files require recompilation of the calling programs.
*   **Missing Procedural Logic:** The provided snippets primarily focus on data structures. The `PROCEDURE DIVISION` sections are essential for understanding the precise flow of control, conditional logic, and any dynamic calls made during execution. `PERFORM` statements suggest many internal subroutines.
*   **Data Structures:** The data structures are generally well-defined, utilizing `OCCURS`, `INDEXED BY`, and `REDEFINES` for efficient table handling and alternate data views, common in COBOL.
*   **Program Naming Conventions:** The ellipses ("...") in some program names suggest they are part of larger, more descriptive names or that only a portion of the name was captured.
*   **Evolution of Programs:** The presence of multiple versions of `LTCAL` and `IPDRG` programs highlights the continuous evolution of Medicare payment rules and the need for system updates to reflect these changes over different fiscal years.