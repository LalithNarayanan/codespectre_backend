## Program Overview

This document consolidates the program overview information extracted from multiple functional specification files (`L1_FunctionalSpecification.md`, `L2_FunctionalSpecification.md`, `L4_FunctionalSpecification.md`, and `L8_FunctionalSpecification.md`). It provides a comprehensive view of the COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricing calculations, their business functions, and the data structures they utilize or interact with.

---

### Core Pricing Logic and Drivers

The central components of the LTCH PPS pricing system are the `LTDRV212`, `LTOPN212`, and various `LTCALxxx` programs, orchestrated by the driver program `LTMGR212`.

**1. LTMGR212**

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and directs results to the `PRTOPER` output printer file. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   **PPS-CBSA:** Contains the Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information (option switch, PPDRV version).

**2. LTOPN212**

*   **Overview:** This subroutine is a key part of the LTCH PPS pricer. It's responsible for loading essential tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) before calling the `LTDRV212` module to perform the actual pricing calculations. It acts as an intermediary, managing data flow and table loading.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the correct wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in LTMGR212)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

**3. LTDRV212**

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves the appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (based on the bill's fiscal year) to perform the final payment calculations. Its extensive change log reflects its evolution to support various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Manages errors and exceptions through various return codes.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Note:** The complexity of `LTDRV212` arises from its handling of numerous `LTCAL` module versions, each tailored for specific fiscal years. Data structures passed are generally consistent, with minor variations across `LTCAL` versions. Extensive conditional logic is critical for selecting the correct `LTCAL` module and managing rate year transitions.

**4. RUFL200**

*   **Overview:** This is a copybook containing the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

---

### Year-Specific LTCH PPS Calculation Modules (`LTCALxxx`)

These programs are responsible for the detailed calculation of Medicare payments for LTCH claims, adhering to specific fiscal year IPPS rules. They often rely on year-specific DRG tables and may incorporate various adjustments.

**5. LTCAL032**

*   **Overview:** Calculates PPS payments for LTC claims based on Length of Stay (LOS). It uses claim and provider record parameters to determine payment amounts, considering DRG code, covered days, and outlier thresholds. It handles short-stay and outlier payments and incorporates blend year calculations. Version is C03.2.
*   **Business Functions:**
    *   LTC Claim Processing.
    *   PPS Calculation.
    *   Short-Stay Payment Calculation.
    *   Outlier Payment Calculation.
    *   Blend Year Calculation.
    *   Data Validation and Error Handling.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Included via COPY. Data structures (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) from `LTDRG031` are used for DRG lookups.

**6. LTCAL042**

*   **Overview:** Similar to `LTCAL032`, this program calculates PPS payments for LTC claims but is a later version (C04.2), likely incorporating updated payment methodologies or data structures. It includes special handling for provider '332006'.
*   **Business Functions:**
    *   LTC Claim Processing.
    *   PPS Calculation.
    *   Short-Stay Payment Calculation (with special logic for provider '332006').
    *   Outlier Payment Calculation.
    *   Blend Year Calculation.
    *   Data Validation and Error Handling.
    *   Special Provider Handling.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Copied into `LTCAL042`. Data structures (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) from `LTDRG031` are used for DRG code lookups.

**7. LTCAL103**

*   **Overview:** A COBOL subroutine for LTCH PPS payment calculation. It uses data tables from copied programs for various factors.
*   **Business Functions:**
    *   LTCH PPS Payment Calculation.
    *   Data Validation.
    *   Outlier Payment Calculation.
    *   Blended Payment Calculation.
*   **Called Programs:** Calls no other programs directly but uses data from `COPY` statements:
    *   `LTDRG100` (LTCH DRG table - `WWM-ENTRY`).
    *   `IPDRG104` (IPPS DRG table - `DRGX-TAB`).
    *   `IRFBN102` (IPPS State-Specific Rural Floor Budget Neutrality Factors - `SSRFBN-TAB`).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**8. LTCAL105**

*   **Overview:** A revised version of `LTCAL103`, likely with updated payment rates and calculation logic.
*   **Business Functions:** Similar to `LTCAL103`, but with updated constants and potentially updated logic.
*   **Called Programs:** Uses data from:
    *   `LTDRG100` (LTCH DRG table).
    *   `IPDRG104` (IPPS DRG table).
    *   `IRFBN105` (Updated IPPS State-Specific Rural Floor Budget Neutrality Factors).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

**9. LTCAL111**

*   **Overview:** An LTCH PPS payment calculation program with an effective date of October 1, 2010. Structure is similar to `LTCAL103`/`LTCAL105`. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to `LTCAL103`/`LTCAL105`, but with potentially different rate constants and calculation logic.
*   **Called Programs:** Uses data from:
    *   `LTDRG110` (LTCH DRG table).
    *   `IPDRG110` (IPPS DRG table).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

**10. LTCAL123**

*   **Overview:** The latest version (as of snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. Structure is similar to previous `LTCAL` programs. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to previous `LTCAL` programs, with updated constants and potentially refined logic.
*   **Called Programs:** Uses data from:
    *   `LTDRG123` (LTCH DRG table).
    *   `IPDRG123` (IPPS DRG table).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

**11. LTCAL162**

*   **Overview:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Called Programs:** Likely calls programs for claim and provider data (`LTDRV...`, `LTWIX...`). Passes:
    *   `BILL-NEW-DATA`.
    *   `PROV-NEW-HOLD`.
    *   `WAGE-NEW-INDEX-RECORD` (LTCH wage index data).
    *   `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data).

**12. LTCAL170**

*   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170`, `IPDRG170` tables. Handles budget neutrality adjustments for site-neutral payments.
*   **Business Functions:** Similar to `LTCAL162`, but with updated 2017 rules.
*   **Called Programs:** Likely calls programs for claim and provider data, passing analogous data structures to `LTCAL162`.

**13. LTCAL183**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using `LTDRG181`, `IPDRG181` tables. Features significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Called Programs:** Likely calls programs for claim and provider data, analogous to previous `LTCAL` programs.

**14. LTCAL190**

*   **Overview:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and `LTDRG190`, `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Called Programs:** Likely calls programs for claim and provider data, similar to previous `LTCAL` programs.

**15. LTCAL202**

*   **Overview:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and `LTDRG200`, `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Called Programs:** Likely calls programs for claim and provider data. Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

**16. LTCAL212**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and `LTDRG210`, `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Called Programs:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

---

### Data Definition Modules (Tables)

These programs define data structures that are used as lookup tables by the `LTCAL` and other processing programs. They do not call other programs but are called by them.

**17. IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211**

*   **Overview:** These programs define Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) tables for specific years (2015, 2016, 2017, 2018, 2019, 2020 respectively).
*   **Business Functions:**
    *   Store IPPS DRG data for each year.
    *   Provide a lookup mechanism for DRG codes and associated information (DRG code, weight, ALOS, description).
*   **Called Programs:** None directly. They are *called* by other programs to retrieve DRG information. The data structure passed *to* them is typically a DRG code. The data structure passed *from* them is `DRG-DATA-TAB` (containing DRG code, weight, ALOS, description).

**18. LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions:** Store LTCH DRG data for lookups.
*   **Called Programs:** None. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

**19. IPDRG104, IPDRG110, IPDRG123**

*   **Overview:** These programs define IPPS DRG tables with effective dates of '20091001' (implied by `IPDRG104` structure), '20101001' (`IPDRG110`), and '20111001' (`IPDRG123`). They represent updates to the DRG data.
*   **Business Functions:**
    *   Data storage and retrieval of IPPS DRG data.
    *   Potentially used in calculating reimbursement amounts based on DRG codes.
*   **Called Programs:** None directly. They are data definition programs.

**20. LTDRG100, LTDRG110, LTDRG123**

*   **Overview:** These programs define LTCH DRG tables, likely reflecting changes in DRG definitions or weights over time. `LTDRG100`'s data is encoded in `W-DRG-FILLS` and redefined.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
*   **Called Programs:** None. They are data definition programs.

**21. IRFBN102, IRFBN105**

*   **Overview:** These programs define tables (`PPS-SSRFBN-TABLE`) containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs). `IRFBN105` is a revised version of `IRFBN102` with updated rates.
*   **Business Functions:**
    *   Storage and retrieval of state-specific payment adjustment factors.
    *   Used to adjust IPPS payments based on state and potentially rural location.
*   **Called Programs:** None. They are data definition programs.

---

### Important Considerations:

*   **COPY Statements:** The frequent use of `COPY` statements indicates that many programs rely on external data definitions and shared code modules. The content of these copied files is critical for a complete understanding of the programs' behavior and data handling.
*   **Implicit Calls:** Programs like `LTDRG031` and various `LTDRGxxx` tables are not explicitly called at runtime but are included via `COPY` statements. Their data structures are directly accessible within the calling programs.
*   **Program Naming Conventions:** The ellipses ("...") in program names suggest they are part of larger naming conventions, potentially indicating versioning or functional grouping (e.g., `LTCALxxxx`).
*   **Data Structures:** The data structures are generally well-defined, utilizing COBOL features like `OCCURS`, `INDEXED BY`, and `REDEFINES` for efficient data handling.
*   **Procedural Logic:** The provided snippets primarily focus on data definitions. The actual calculation logic resides in the `PROCEDURE DIVISION` of the programs, which is essential for understanding the full functionality. The `PERFORM` statements suggest the use of numerous internal subroutines.