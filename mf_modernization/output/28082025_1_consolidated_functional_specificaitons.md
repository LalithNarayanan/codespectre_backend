## Program Overview

This document consolidates and organizes the program overview information extracted from multiple functional specification files (`L1_FunctionalSpecification.md`, `L2_FunctionalSpecification.md`, `L4_FunctionalSpecification.md`, and `L8_FunctionalSpecification.md`). The aim is to provide a comprehensive understanding of the COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricing, their business functions, and the data structures they utilize or are associated with.

---

### Core Pricing and Driver Programs

These programs form the backbone of the LTCH PPS pricing logic, handling claim processing, table lookups, and calculation execution.

**1. LTMGR212**

*   **Overview:** This program acts as a driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to `PRTOPER`. Its extensive change log reflects frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:** (See below)
    *   **Data Structures Passed to LTOPN212:**
        *   `BILL-NEW-DATA`: Contains bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   `PPS-DATA-ALL`: Contains pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   `PPS-CBSA`: Contains the Core Based Statistical Area code.
        *   `PPS-PAYMENT-DATA`: Contains calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   `PRICER-OPT-VERS-SW`: Contains pricing option and version information (option switch, PPDRV version).

**2. LTOPN212**

*   **Overview:** This subroutine is a core component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module for actual pricing calculations. It manages data flow and table loading before passing control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines which wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:** (See below)
    *   **Data Structures Passed to LTDRV212:**
        *   `BILL-NEW-DATA`: (Same as in LTMGR212)
        *   `PPS-DATA-ALL`: (Same as in LTMGR212)
        *   `PPS-CBSA`: (Same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212)
        *   `PROV-RECORD-FROM-USER`: (Same as in LTMGR212)
        *   `CBSAX-TABLE-FROM-USER`: Contains the CBSA wage index table.
        *   `IPPS-CBSAX-TABLE-FROM-USER`: Contains the IPPS CBSA wage index table.
        *   `MSAX-TABLE-FROM-USER`: Contains the MSA wage index table.
        *   `WORK-COUNTERS`: Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

**3. LTDRV212**

*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (depending on the bill's fiscal year) to perform final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   **Many `LTCALxxxx` programs:** (See specific `LTCAL` programs below, e.g., `LTCAL162`, `LTCAL032`, etc.). The specific `LTCAL` module called depends on the fiscal year of the bill.
    *   **Data Structures Passed to `LTCALxxxx` programs:**
        *   `BILL-NEW-DATA`: (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   `PPS-DATA-ALL`: (Same as in LTMGR212)
        *   `PPS-CBSA`: (Same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212)
        *   `PROV-NEW-HOLD`: Contains the provider record.
        *   `WAGE-NEW-INDEX-RECORD-CBSA`: Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   `WAGE-IPPS-INDEX-RECORD-CBSA`: Contains the IPPS CBSA wage index data.
        *   `BILL-DATA-FY03-FY15`: (Potentially for older fiscal years).

**4. RUFL200**

*   **Overview:** This is a copybook (data definition) containing the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not an executable program but a data structure definition.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook used by other programs.

---

### Year-Specific Calculation Modules (`LTCALxxxx`)

These programs perform the core LTCH PPS payment calculations, adapting to specific fiscal year rules and data tables. The `LTCAL` programs generally utilize data structures passed down from `LTDRV212`.

**5. LTCAL032 (Version C03.2)**

*   **Overview:** Calculates PPS payments for LTC claims based on Length of Stay (LOS), DRG code, covered days, and outlier thresholds. It handles short-stay and outlier payments and incorporates blend year calculations.
*   **Business Functions:**
    *   LTC Claim Processing.
    *   PPS Calculation.
    *   Short-Stay Payment Calculation.
    *   Outlier Payment Calculation.
    *   Blend Year Calculation.
    *   Data Validation and Error Handling.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Included via COPY; data structures (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) used for DRG lookups.
    *   Implicitly uses data structures passed from `LTDRV212` (e.g., `BILL-NEW-DATA`, `PROV-NEW-HOLD`).

**6. LTCAL042 (Version C04.2)**

*   **Overview:** Similar to LTCAL032 but a later version (C04.2), likely incorporating updates to payment methodologies, rules, or data structures. Includes special handling for provider '332006'.
*   **Business Functions:**
    *   LTC Claim Processing.
    *   PPS Calculation.
    *   Short-Stay Payment Calculation (with special logic for provider '332006').
    *   Outlier Payment Calculation.
    *   Blend Year Calculation.
    *   Data Validation and Error Handling.
    *   Special Provider Handling.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Included via COPY; data structures (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) used for DRG lookups.
    *   Implicitly uses data structures passed from `LTDRV212`.

**7. LTCAL103**

*   **Overview:** A COBOL subroutine calculating LTCH PPS payments. Uses data tables defined in COPY statements. Effective October 1, 2010. Does not appear to use a state-specific RFBN table.
*   **Business Functions:**
    *   LTCH PPS Payment Calculation.
    *   Data Validation.
    *   Outlier Payment Calculation.
    *   Blended Payment Calculation.
*   **Called Programs & Data Structures:**
    *   **Data Structures via COPY:**
        *   `LTDRG100`: LTCH DRG table (`WWM-ENTRY` with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
        *   `IPDRG104`: IPPS DRG table (`DRGX-TAB` with `DRGX-EFF-DATE`, `DRG-WT`, `DRG-ALOS`, `DRG-DAYS-TRIM`, `DRG-ARITH-ALOS`).
        *   `IRFBN102`: IPPS State-Specific Rural Floor Budget Neutrality Factors (`SSRFBN-TAB` with `WK-SSRFBN-STATE`, `WK-SSRFBN-RATE`, `WK-SSRFBN-CODE2`, `WK-SSRFBN-STNAM`, `WK-SSRFBN-REST`).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**8. LTCAL105**

*   **Overview:** A revised version of `LTCAL103`, likely reflecting updates to payment rates and calculation logic. Very similar structure to LTCAL103.
*   **Business Functions:** Similar to LTCAL103 but with updated constants and potentially updated logic.
*   **Called Programs & Data Structures:**
    *   **Data Structures via COPY:**
        *   `LTDRG100`: LTCH DRG table.
        *   `IPDRG104`: IPPS DRG table.
        *   `IRFBN105`: Updated IPPS State-Specific Rural Floor Budget Neutrality Factors.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

**9. LTCAL111**

*   **Overview:** Another revision of the LTCH PPS payment calculation program, effective October 1, 2010. Similar structure to LTCAL103 and LTCAL105. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to LTCAL103 and LTCAL105, but with potentially different rate constants and calculation logic.
*   **Called Programs & Data Structures:**
    *   **Data Structures via COPY:**
        *   `LTDRG110`: LTCH DRG table.
        *   `IPDRG110`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

**10. LTCAL123**

*   **Overview:** The latest version (as of the provided snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. Similar structure to previous LTCAL programs. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to previous LTCAL programs, with updated constants and potentially refined logic.
*   **Called Programs & Data Structures:**
    *   **Data Structures via COPY:**
        *   `LTDRG123`: LTCH DRG table.
        *   `IPDRG123`: IPPS DRG table.
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
*   **Called Programs & Data Structures:**
    *   Implicitly calls programs to read claim data (`LTDRV...`) and provider data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD` (LTCH wage index data), and `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data).

**12. LTCAL170**

*   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170`, `IPDRG170` tables. Includes handling of budget neutrality adjustments for site-neutral payments.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017.
*   **Called Programs & Data Structures:** Likely calls programs for claim and provider data input, passing analogous data structures to `LTCAL162`.

**13. LTCAL183**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables. Significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous LTCAL programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Called Programs & Data Structures:** Likely calls programs for claim and provider data input, analogous to previous LTCAL programs.

**14. LTCAL190**

*   **Overview:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and `LTDRG190`, `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Called Programs & Data Structures:** Likely calls programs for claim and provider data input, similar to previous LTCAL programs.

**15. LTCAL202**

*   **Overview:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and `LTDRG200`, `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Called Programs & Data Structures:**
    *   Likely calls programs for claim and provider data input.
    *   Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

**16. LTCAL212**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and `LTDRG210`, `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous LTCAL programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Called Programs & Data Structures:**
    *   Likely calls programs for claim and provider data input.
    *   Uses internal functions, similar to `LTCAL202`.

---

### Data Definition Programs (DRG and RFBN Tables)

These programs define data tables used by the calculation modules. They are not executable in themselves but are "called" (included via COPY or used as lookup files) by other programs.

**17. IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211**

*   **Overview:** These programs define Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) tables for specific years (2015, 2016, 2017, 2018, 2019, and 2020 respectively). They contain DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions:**
    *   Stores IPPS DRG data for lookup.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by other programs (like `LTCAL162`, `LTCAL170`, etc.). The data structure passed *to* them would be a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**18. LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions:** Store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

**19. IPDRG104, IPDRG110, IPDRG123**

*   **Overview:** These programs define IPPS DRG tables with effective dates of '20101001' (IPDRG110, IPDRG123) and an unspecified effective date for IPDRG104, but implying earlier versions (e.g., 2010/2011). They contain DRG data including effective date, weights, ALOS, trimmed days, and arithmetic ALOS.
*   **Business Functions:** Data storage and retrieval of IPPS DRG data, potentially used for calculating reimbursement amounts.
*   **Other Programs Called:** None directly. These are data definition programs called by other programs.

**20. LTDRG100, LTDRG110, LTDRG123**

*   **Overview:** These programs define LTCH DRG tables. `LTDRG100` has an encoded structure within `W-DRG-FILLS` redefined as `WWM-ENTRY`. `LTDRG110` and `LTDRG123` are revised versions, likely reflecting changes in DRG definitions or weights.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
*   **Other Programs Called:** None; these are data definition programs.

**21. IRFBN102, IRFBN105**

*   **Overview:** These programs define tables (`PPS-SSRFBN-TABLE`) containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs). This data is likely used to adjust payments based on geographic location. `IRFBN105` is a revised version of `IRFBN102` with updated rates.
*   **Business Functions:**
    *   Storage and retrieval of state-specific payment adjustment factors.
    *   Used to adjust IPPS payments based on state and potentially rural location.
*   **Other Programs Called:** None directly. These are data definition programs.

**22. IPDRG104**

*   **Overview:** Defines a table (`DRG-TABLE`) containing IPPS DRG data with an effective date and multiple sets of weight, ALOS, trimmed days, and arithmetic ALOS values.
*   **Business Functions:** Data storage and retrieval of IPPS DRG data.
*   **Other Programs Called:** None directly. This is a data definition program.

---

### Supporting Modules and Utilities

**23. LTDRG031**

*   **Overview:** A data definition module containing a DRG lookup table (`WWM-ENTRY`) that maps DRG codes (`WWM-DRG`) to relative weights (`WWM-RELWT`) and average lengths of stay (`WWM-ALOS`). Initialized with literal values.
*   **Business Functions:** Provides a central repository for DRG-related data for lookup.
*   **Called Programs & Data Structures:** Does not call other programs. Used via COPY statements by `LTCAL032` and `LTCAL042`. The `WWM-ENTRY` data structure is crucial.

---

**Important Considerations:**

*   **COPY Statements:** The extensive use of `COPY` statements indicates that many programs rely on shared data definitions and potentially reusable code modules. The actual content of these copied files is critical for a complete understanding.
*   **Implicit Calls/Data Usage:** Programs like `LTCALxxxx` often don't explicitly "call" the DRG or RFBN tables. Instead, the data structures defined in these table programs are included via `COPY` statements, making the data directly accessible within the calling program's Working-Storage or Linkage Section.
*   **Version Control:** The naming conventions (e.g., `LTCAL162`, `IPDRG200`) clearly indicate that these programs are updated annually to reflect changes in Medicare payment rules and data.
*   **Data Structures:** The detailed definitions of data structures like `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PROV-NEW-HOLD`, and various DRG/Wage Index entries highlight the structured approach to data management in these COBOL programs.
*   **Procedural Logic:** The provided snippets primarily focus on data structures. The actual procedural logic (`PROCEDURE DIVISION`) within these programs would detail the execution flow, conditional logic, and specific calculations performed.
*   **Program Evolution:** The presence of multiple versions of `LTCAL` and `IPDRG` programs, along with notes about extensive change logs (e.g., for `LTMGR212` and `LTDRV212`), signifies a long history of development and adaptation to evolving healthcare policies.