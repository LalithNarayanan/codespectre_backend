## Program Overview

This document consolidates information from multiple functional specification files, detailing the programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricing and calculation. The programs can be broadly categorized into driver programs, calculation subroutines, and data definition modules.

---

### Core Driver and Calculation Programs

These programs form the backbone of the LTCH PPS processing, orchestrating the calculations and interacting with various data sources.

**1. LTMGR212**

*   **Overview:** This program acts as a driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to `PRTOPER`. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   **PPS-DATA-ALL:** Pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   **PPS-CBSA:** Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   **PRICER-OPT-VERS-SW:** Pricing option and version information (option switch, PPDRV version).

**2. LTOPN212**

*   **Overview:** This subroutine is a key component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module to perform the actual pricing calculations. It manages data flow and table loading before handing off control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines which wage index table to use based on the bill discharge date.
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

*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (based on the bill's fiscal year) for final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Multiple calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` arises from its handling of numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While data structures passed are largely consistent, minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is critical for selecting the appropriate `LTCAL` module and managing transitions between rate years and data structures.

---

### Year-Specific LTCH Payment Calculation Programs (`LTCALxxx`)

These programs are responsible for calculating LTCH PPS payments for specific fiscal years, incorporating the prevailing rules and data for that period.

**1. LTCAL032 (Version C03.2)**

*   **Overview:** Calculates PPS payments for LTC claims based on Length of Stay (LOS). It uses input parameters from claim and provider records, considering DRG code, covered days, and outlier thresholds. It handles short-stay and outlier payments, and incorporates blend year calculations.
*   **Business Functions:**
    *   LTC Claim Processing: Determines payment amounts for individual LTC claims.
    *   PPS Calculation: Core function of calculating PPS payments.
    *   Short-Stay Payment Calculation: Calculates payments for short hospital stays.
    *   Outlier Payment Calculation: Determines and calculates outlier payments based on costs exceeding thresholds.
    *   Blend Year Calculation: Adjusts payments based on blend year parameters (percentage of facility rate vs. DRG payment).
    *   Data Validation and Error Handling: Performs data edits and assigns return codes.
*   **Called Programs & Data Structures:**
    *   **LTDRG031 (via COPY):** Data structures within `LTDRG031` (specifically `WWM-ENTRY` containing `WWM-DRG`, `WWM-RELWT`, and `WWM-ALOS`) are used for DRG lookups.

**2. LTCAL042 (Version C04.2)**

*   **Overview:** Similar to `LTCAL032`, this program calculates PPS payments for LTC claims but is a later version (C04.2), likely incorporating updates to payment methodologies, rules, or data structures. It includes special handling for provider '332006'.
*   **Business Functions:**
    *   LTC Claim Processing: Determines payment amounts for individual LTC claims.
    *   PPS Calculation: Core function of calculating PPS payments.
    *   Short-Stay Payment Calculation: Calculates payments for short stays, with special logic for provider '332006'.
    *   Outlier Payment Calculation: Determines and calculates outlier payments.
    *   Blend Year Calculation: Adjusts payments according to blend year parameters.
    *   Data Validation and Error Handling: Edits data and assigns return codes.
    *   Special Provider Handling: Contains specific logic for provider '332006', adjusting short-stay calculations based on discharge date.
*   **Called Programs & Data Structures:**
    *   **LTDRG031 (via COPY):** Data structures within `LTDRG031` (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) are used for DRG code lookups.

**3. LTCAL103**

*   **Overview:** A COBOL subroutine (or program) that calculates LTCH PPS payments. It uses data tables from copied programs.
*   **Business Functions:**
    *   LTCH PPS Payment Calculation: Calculates payment amounts based on LOS, DRG, facility costs, wage indices, and other factors.
    *   Data Validation: Performs edits and validations on input bill data.
    *   Outlier Payment Calculation: Calculates outlier payments if applicable.
    *   Blended Payment Calculation: Handles blended payments based on blend years and percentages.
*   **Called Programs & Data Structures (via COPY):**
    *   `LTDRG100`: LTCH DRG table (`WWM-ENTRY` with fields `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `IPDRG104`: IPPS DRG table (`DRGX-TAB` with fields `DRGX-EFF-DATE`, `DRG-WT`, `DRG-ALOS`, `DRG-DAYS-TRIM`, `DRG-ARITH-ALOS`).
    *   `IRFBN102`: IPPS State-Specific Rural Floor Budget Neutrality Factors (`SSRFBN-TAB` with `WK-SSRFBN-STATE`, `WK-SSRFBN-RATE`, `WK-SSRFBN-CODE2`, `WK-SSRFBN-STNAM`, `WK-SSRFBN-REST`).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**4. LTCAL105**

*   **Overview:** A revised version of `LTCAL103`, likely reflecting updates to payment rates and calculation logic.
*   **Business Functions:** Similar to `LTCAL103`, but with updated constants and potentially updated logic.
*   **Called Programs & Data Structures (via COPY):**
    *   `LTDRG100`: LTCH DRG table.
    *   `IPDRG104`: IPPS DRG table.
    *   `IRFBN105`: Updated IPPS State-Specific Rural Floor Budget Neutrality Factors.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**5. LTCAL111**

*   **Overview:** Another revision of the LTCH PPS payment calculation program, effective October 1, 2010. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to `LTCAL103` and `LTCAL105`, but with potentially different rate constants and calculation logic.
*   **Called Programs & Data Structures (via COPY):**
    *   `LTDRG110`: LTCH DRG table.
    *   `IPDRG110`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**6. LTCAL123**

*   **Overview:** The latest version (as of the provided snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. Does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to previous `LTCAL` programs, with updated constants and potentially refined logic.
*   **Called Programs & Data Structures (via COPY):**
    *   `LTDRG123`: LTCH DRG table.
    *   `IPDRG123`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

**7. LTCAL162**

*   **Overview:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called (Implicitly via COPY or expected runtime calls):**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD` to itself (implicitly for processing).

**8. LTCAL170**

*   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170` and `IPDRG170` tables. Handles budget neutrality adjustments for site-neutral payments.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, passing analogous data structures to `LTCAL162`.

**9. LTCAL183**

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables. Includes significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, analogous to previous `LTCAL` programs.

**10. LTCAL190**

*   **Overview:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, similar to previous `LTCAL` programs.

**11. LTCAL202**

*   **Overview:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs for claim and provider data input. Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

**12. LTCAL212**

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

---

### Data Definition Modules and Tables

These programs primarily define data structures and tables used by the calculation programs. They do not execute logic in the traditional sense but serve as data repositories.

**1. RUFL200**

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

**2. IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211**

*   **Overview:** These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for specific years (2015, 2016, 2017, 2018, 2019, and 2020 respectively). The data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions:**
    *   Store IPPS DRG data for specified years.
    *   Provide a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them would be a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, containing the DRG code, weight, ALOS, and description.

**3. LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions:** Store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

**4. IPDRG104, IPDRG110, IPDRG123**

*   **Overview:** These programs define IPPS DRG data tables (`DRG-TABLE`) with effective dates of '20101001' (IPDRG110), '20111001' (IPDRG123), and an earlier date for IPDRG104. They represent versions or updates of DRG data.
*   **Business Functions:**
    *   Data storage and retrieval of IPPS DRG data.
    *   Potentially used in calculating reimbursement amounts based on DRG codes.
*   **Other Programs Called:** None directly called. These are data definition programs meant to be called by other programs.

**5. LTDRG100, LTDRG110, LTDRG123**

*   **Overview:** These programs define LTCH DRG tables (`W-DRG-TABLE` or similar), likely reflecting changes in DRG definitions or weights.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
*   **Other Programs Called:** None; these are data definition programs.

**6. IRFBN102, IRFBN105**

*   **Overview:** These programs define tables (`PPS-SSRFBN-TABLE`) containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs), likely used to adjust payments based on geographic location. `IRFBN105` appears to be a revised version of `IRFBN102` with updated rates.
*   **Business Functions:**
    *   Storage and retrieval of state-specific payment adjustment factors.
    *   Used to adjust IPPS payments based on state and potentially rural location.
*   **Other Programs Called:** None directly called. These are data definition programs.

**7. LTDRG031**

*   **Overview:** This program defines a DRG lookup table (`WWM-ENTRY`) that maps DRG codes (`WWM-DRG`) to relative weights (`WWM-RELWT`) and average lengths of stay (`WWM-ALOS`). It is used by `LTCAL032` and `LTCAL042`. The table is initialized using literal values.
*   **Business Functions:** DRG Lookup Table Definition: Provides a central repository for DRG-related data.
*   **Called Programs & Data Structures:** Does not call other programs. Defines the `WWM-ENTRY` data structure.

---

### Supporting Programs and Copybooks

**1. LTMGR212** (also listed above as a driver)

*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator)
        *   **PPS-DATA-ALL:** (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA)
        *   **PPS-CBSA:** (Core Based Statistical Area code)
        *   **PPS-PAYMENT-DATA:** (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment)
        *   **PRICER-OPT-VERS-SW:** (option switch, PPDRV version)

**2. LTOPN212** (also listed above)

*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in LTMGR212)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212)
        *   **CBSAX-TABLE-FROM-USER:** (CBSA wage index table)
        *   **IPPS-CBSAX-TABLE-FROM-USER:** (IPPS CBSA wage index table)
        *   **MSAX-TABLE-FROM-USER:** (MSA wage index table)
        *   **WORK-COUNTERS:** (record counts for CBSA, MSA, provider, and IPPS CBSA)

**3. LTDRV212** (also listed above)

*   **Called Programs and Data Structures:**
    *   Calls `LTCALxxxx` modules (e.g., 032, 080, 111, 212). Each call uses:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, or `BILL-DATA-FY03-FY15` for older fiscal years)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** (Provider record)
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** (CBSA wage index data)
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** (IPPS CBSA wage index data)

**4. LTCAL162** (also listed above)

*   **Other Programs Called (Implicitly via COPY or expected runtime calls):**
    *   Likely calls other programs for claim data (`LTDRV...`) and provider data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD` to itself (implicitly for processing).

---

**Important Considerations:**

*   **COPY Statements:** The frequent use of `COPY` statements indicates a reliance on external data definitions. The actual content of these copied files is crucial for a complete understanding.
*   **Procedural Logic:** Snippets primarily show data structures. The `PROCEDURE DIVISION` is essential for understanding program flow, conditional logic, and dynamic calls.
*   **Data Structures:** Well-defined data structures are used, including `OCCURS` and `INDEXED BY` for efficient table handling, and `REDEFINES` for alternate data views.
*   **Program Naming Conventions:** Ellipses ("...") in program names suggest they are part of larger naming schemes, implying a family of related programs.
*   **Version Control:** The evolution of programs like `LTCALxxx` and `IPDRGxxx` across different years highlights the dynamic nature of healthcare reimbursement regulations.

**Overall, the programs described form a comprehensive system for calculating LTCH PPS payments, handling various fiscal years, policy changes, and data inputs from different sources.**