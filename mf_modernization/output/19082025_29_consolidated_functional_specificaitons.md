## Program Overview

This document consolidates and organizes information about various COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) and Inpatient Prospective Payment System (IPPS) calculations. The programs, extracted from multiple functional specification files, detail their functionalities, business processes, and the data structures they utilize or interact with.

The system appears to be structured around a core driver program (`LTMGR212`) that initiates the processing, followed by subroutines that perform specific calculations (`LTOPN212`, `LTDRV212`), and then specialized modules for different fiscal years (`LTCALxxxx` programs). Data tables (`IPDRGxxxx`, `LTDRGxxxx`) are used to store rate and weight information for various years.

---

### Program: LTMGR212

*   **Overview:** This program acts as a driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes the results to `PRTOPER`. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   **PPS-CBSA:** Contains the Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information (option switch, PPDRV version).

---

### Program: LTOPN212

*   **Overview:** This subroutine is a core component of the Long-Term Care PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module for pricing calculations. It manages data flow and table loading before handing off control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in LTMGR212)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212, likely referring to provider data)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

---

### Program: LTDRV212

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (based on the bill's fiscal year) for final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212 etc.) are made. Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` stems from its handling of numerous versions of the `LTCAL` modules, each designed for a specific fiscal year. The data structures passed remain largely consistent, though minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing transitions between different rate years and data structures.

---

### Program: RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

---

### Programs: IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211

*   **Overview:** These programs define Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) tables for specific years (2015, 2016, 2017, 2018, 2019, and 2020 respectively). They contain data such as DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:**
    *   Store IPPS DRG data for specific years.
    *   Provide a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables and do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them is typically a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, containing the DRG code, weight, ALOS, and description.

---

### Program: LTCAL162

*   **Overview:** This COBOL program calculates Medicare payment for Long-Term Care Hospital (LTCH) claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (claim details), `PROV-NEW-HOLD` (provider information), `WAGE-NEW-INDEX-RECORD` (LTCH wage index data), and `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) implicitly for processing.

---

### Program: LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`, passing analogous data structures.

---

### Program: LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. It notes significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporating 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

---

### Program: LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

---

### Program: LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.
*   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

---

### Program: LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.
*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

---

### Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.
*   **Important Note:** The ellipses ("...") in the program names suggest that these are parts of larger program names. The exact names and functionalities of the data files and other programs called would need to be determined from the full context of the application. Also, `COPY` statements indicate the inclusion of external code modules; their contents are crucial for a complete understanding.

---

### Programs: IPDRG104, IPDRG110, IPDRG123

*   **Overview:** These programs define IPPS DRG data tables (`DRG-TABLE`) for different effective dates ('20101001', '20111001'). They contain effective dates and multiple sets of weight, average length of stay (ALOS), trimmed days, and arithmetic ALOS values for a large number of DRGs. `IPDRG104` appears to be an earlier version.
*   **Business Functions Addressed:**
    *   Data storage and retrieval of IPPS DRG data.
    *   Potentially used in calculating reimbursement amounts based on DRG codes.
*   **Other Programs Called:** None directly called. These are data definition programs intended to be *called* by other programs.

---

### Programs: IRFBN102, IRFBN105

*   **Overview:** These programs define tables (`PPS-SSRFBN-TABLE`) containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs). This data likely adjusts payments based on geographic location. `IRFBN105` is a revised version of `IRFBN102` with updated rates. The tables include state codes, rates, and descriptive information.
*   **Business Functions Addressed:**
    *   Storage and retrieval of state-specific payment adjustment factors.
    *   Used to adjust IPPS payments based on state and potentially rural location.
*   **Other Programs Called:** None directly called. These are data definition programs.

---

### Program: LTCAL103

*   **Overview:** This COBOL subroutine (or program) calculates PPS payments for LTCH claims. It uses data tables defined in copied programs to determine payment amounts based on length of stay, DRG, facility costs, wage indices, and other factors. It handles outlier payments and blended payments.
*   **Business Functions Addressed:**
    *   LTCH PPS Payment Calculation: Calculates payment amounts for LTCH claims.
    *   Data Validation: Performs edits and validations on input bill data.
    *   Outlier Payment Calculation: Calculates outlier payments.
    *   Blended Payment Calculation: Handles blended payments based on blend years and percentages.
*   **Other Programs Called:** This program calls no other programs directly but uses data from:
    *   `LTDRG100`: LTCH DRG table (`WWM-ENTRY` with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `IPDRG104`: IPPS DRG table (`DRGX-TAB` with `DRGX-EFF-DATE`, `DRG-WT`, `DRG-ALOS`, `DRG-DAYS-TRIM`, `DRG-ARITH-ALOS`).
    *   `IRFBN102`: IPPS State-Specific Rural Floor Budget Neutrality Factors (`SSRFBN-TAB` with `WK-SSRFBN-STATE`, `WK-SSRFBN-RATE`, `WK-SSRFBN-CODE2`, `WK-SSRFBN-STNAM`, `WK-SSRFBN-REST`).
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` data structures.

---

### Program: LTCAL105

*   **Overview:** A revised version of `LTCAL103`, likely reflecting updates to payment rates and calculation logic. The overall structure is very similar.
*   **Business Functions Addressed:** Similar to `LTCAL103` but with updated constants and potentially updated logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG100`: LTCH DRG table.
    *   `IPDRG104`: IPPS DRG table.
    *   `IRFBN105`: Updated IPPS State-Specific Rural Floor Budget Neutrality Factors.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

---

### Program: LTCAL111

*   **Overview:** Another revision of the LTCH PPS payment calculation program, with an effective date of October 1, 2010. The structure is similar to `LTCAL103` and `LTCAL105`. It does not appear to use a state-specific RFBN table (`IRFBN`).
*   **Business Functions Addressed:** Similar to `LTCAL103` and `LTCAL105`, but with potentially different rate constants and calculation logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG110`: LTCH DRG table.
    *   `IPDRG110`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

---

### Program: LTCAL123

*   **Overview:** The latest version (as of the provided snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. The structure is very similar to previous `LTCAL` programs. Like `LTCAL111`, this version does not appear to use a state-specific RFBN table.
*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, with updated constants and potentially refined logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG123`: LTCH DRG table.
    *   `IPDRG123`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

---

### Program: LTDRG100

*   **Overview:** This program defines a table (`W-DRG-TABLE`) containing LTCH DRG data. The data is encoded in `W-DRG-FILLS` and redefined.
*   **Business Functions Addressed:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
*   **Other Programs Called:** None; this is a data definition program.

---

### Program: LTDRG110

*   **Overview:** A revised LTCH DRG table, likely reflecting changes in DRG definitions or weights.
*   **Business Functions Addressed:** Data storage and retrieval of LTCH DRG data.
*   **Other Programs Called:** None; this is a data definition program.

---

### Program: LTDRG123

*   **Overview:** Another updated LTCH DRG table.
*   **Business Functions Addressed:** Data storage and retrieval of LTCH DRG data.
*   **Other Programs Called:** None; this is a data definition program.

---

### Program: LTCAL032

*   **Overview:** This program calculates PPS payments for LTC claims based on Length of Stay (LOS). It uses input parameters from claim and provider records to determine payment amounts, considering DRG code, covered days, and outlier thresholds. It handles short-stay and outlier payments, and incorporates blend year calculations. The version is C03.2.
*   **Business Functions:**
    *   LTC Claim Processing: Processes individual LTC claims for payment determination.
    *   PPS Calculation: Core functionality for calculating PPS payments.
    *   Short-Stay Payment Calculation: Calculates payments for short hospital stays.
    *   Outlier Payment Calculation: Determines and calculates outlier payments based on cost thresholds.
    *   Blend Year Calculation: Adjusts payments based on blend year parameters.
    *   Data Validation and Error Handling: Performs data edits and assigns return codes.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Included via a COPY statement. Data structures defined in `LTDRG031` (`WWM-ENTRY`, containing `WWM-DRG`, `WWM-RELWT`, and `WWM-ALOS`) are used directly within `LTCAL032` for DRG lookups.

---

### Program: LTCAL042

*   **Overview:** Similar to `LTCAL032`, this program calculates PPS payments for LTC claims. It's a later version (C04.2) likely incorporating updates to payment methodologies, rules, or data structures. It includes special handling for provider '332006'.
*   **Business Functions:**
    *   LTC Claim Processing: Processes individual LTC claims for payment determination.
    *   PPS Calculation: Core functionality for calculating PPS payments.
    *   Short-Stay Payment Calculation: Calculates payments for short stays, with special logic for provider '332006'.
    *   Outlier Payment Calculation: Determines and calculates outlier payments.
    *   Blend Year Calculation: Adjusts payments according to blend year parameters.
    *   Data Validation and Error Handling: Edits data and assigns return codes.
    *   Special Provider Handling: Contains specific logic for provider '332006', adjusting short-stay calculations based on discharge date.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Copied into `LTCAL042`. Data structures within `LTDRG031` (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) are used for DRG code lookups.

---

### Program: LTDRG031

*   **Overview:** This program defines a DRG lookup table. It defines a table (`WWM-ENTRY`) that maps DRG codes (`WWM-DRG`) to relative weights (`WWM-RELWT`) and average lengths of stay (`WWM-ALOS`). This table is used by other programs (`LTCAL032` and `LTCAL042`) via COPY statements.
*   **Business Functions:** DRG Lookup Table Definition: Provides a central repository for DRG-related data.
*   **Called Programs & Data Structures:** Does not call other programs. Defines the `WWM-ENTRY` data structure containing DRG code, relative weight, and average length of stay.

---

### **General Important Considerations:**

*   **COPY Statements:** Many programs rely on external data definitions through `COPY` statements. The content of these copied files is critical for a complete understanding.
*   **Procedural Logic:** The provided snippets primarily focus on data structures. The `PROCEDURE DIVISION` logic is essential for understanding the flow of control and dynamic calls. `PERFORM` statements suggest many internal subroutines.
*   **Data Structures:** The data structures are well-defined, utilizing `OCCURS`, `INDEXED BY`, and `REDEFINES` for efficient table handling and alternate data views.
*   **Program Evolution:** The presence of multiple versions of `LTCAL` and `IPDRG`/`LTDRG` programs highlights the system's evolution to accommodate changes in Medicare payment rules and data year over year.
*   **Interdependencies:** The system exhibits clear interdependencies, with driver programs calling subroutines, and calculation modules utilizing data tables and other modules based on fiscal year.