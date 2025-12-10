# Program Overview

This document consolidates information from multiple functional specification files, providing a comprehensive overview of the Long-Term Care Prospective Payment System (LTCH PPS) pricing modules. It details the purpose, business functions, and interdependencies of various COBOL programs and data structures involved in calculating Medicare payments for LTCH claims.

## Core Pricing Driver and Subroutines

The central component of this system is a driver program that orchestrates the pricing calculations. This driver, along with its key subroutines, manages input data, calls specific calculation modules based on fiscal year, and handles data retrieval and table loading.

### LTMGR212

*   **Overview:** This program acts as a driver for testing the Long-Term Care PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to `PRTOPER`. Its extensive change log indicates numerous revisions to pricing methodologies and data structures.
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

### LTOPN212

*   **Overview:** This subroutine is a core component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module to perform the actual pricing calculations. It acts as an intermediary, managing data flow and table loading before passing control to the calculation module.
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

### LTDRV212

*   **Overview:** This module is the heart of the LTCH PPS pricing calculation. It retrieves the appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (depending on the bill's fiscal year) to perform the final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes. The complexity arises from handling numerous versions of the `LTCAL` modules, each designed for a specific fiscal year.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212 etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Note:** The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing the transition between different rate years and data structures.

## Fiscal Year Specific Calculation Modules (LTCALxxx)

These programs are responsible for the actual payment calculations, adapting to the specific rules and data tables of each fiscal year.

### LTCAL162

*   **Overview:** This COBOL program calculates the Medicare payment for LTCH claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Called Programs and Data Structures:**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (containing claim details) to itself (implicitly for processing).
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### LTCAL170

*   **Overview:** Calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to `LTCAL162`, passing analogous data structures.

### LTCAL183

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. Features significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

### LTCAL190

*   **Overview:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

### LTCAL202

*   **Overview:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data. Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Called Programs and Data Structures:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

## Data Tables for DRG and Wage Index Information

These programs define data tables used by the calculation modules. They are not executable programs in themselves but are called by other programs to retrieve specific data.

### IPPS DRG Tables (2015-2020)

*   **Programs:** `IPDRG160` (2015), `IPDRG170` (2016), `IPDRG181` (2017), `IPDRG190` (2018), `IPDRG200` (2019), `IPDRG211` (2020).
*   **Overview:** These programs define data tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for specific years. The data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for specified years.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:** These are data tables; they don't call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them is typically a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

### LTCH DRG Tables (Various Years)

*   **Programs:** `LTDRG160`, `LTDRG170`, `LTDRG181`, `LTDRG190`, `LTDRG200`, `LTDRG210`.
*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Called Programs and Data Structures:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them is a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

### RUFL200 (Rural Floor Factor Table)

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition included in other programs, not an executable program itself.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

## Data Structures Summary

The following data structures are consistently passed between programs involved in the LTCH PPS pricing process:

*   **BILL-NEW-DATA:** Contains detailed information about the LTCH bill.
*   **PPS-DATA-ALL:** Holds comprehensive pre-calculated PPS data.
*   **PPS-CBSA:** Stores the Core Based Statistical Area code.
*   **PPS-PAYMENT-DATA:** Contains the results of payment calculations.
*   **PRICER-OPT-VERS-SW:** Manages pricing option and version control.
*   **PROV-NEW-HOLD / PROV-RECORD-FROM-USER:** Contains provider-specific information.
*   **WAGE-NEW-INDEX-RECORD-CBSA / WAGE-NEW-INDEX-RECORD:** Holds CBSA wage index data.
*   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains IPPS CBSA wage index data.
*   **CBSAX-TABLE-FROM-USER:** The CBSA wage index table.
*   **IPPS-CBSAX-TABLE-FROM-USER:** The IPPS CBSA wage index table.
*   **MSAX-TABLE-FROM-USER:** The MSA wage index table.
*   **WORK-COUNTERS:** Tracks various record counts.
*   **DRG-DATA-TAB:** Returned by IPPS DRG tables, containing DRG details.
*   **WWM-ENTRY:** Returned by LTCH DRG tables, containing LTCH DRG details.

**Important Note:** The use of ellipses ("...") in program names suggests these are parts of larger program names, and the exact names and functionalities of associated data files and other called programs would require consulting the full context of the application. `COPY` statements indicate the inclusion of external code modules, the contents of which are crucial for a complete understanding.