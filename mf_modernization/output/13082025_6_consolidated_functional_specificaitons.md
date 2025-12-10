# Program Overview

This document consolidates information about various COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricer. The programs are categorized by their primary functions, ranging from high-level drivers to specific calculation modules and data tables.

## Core Pricing and Driving Programs

These programs form the backbone of the LTCH PPS pricing process, orchestrating calls to subroutines and handling data flow.

### LTMGR212
*   **Overview:** This program acts as a driver for testing the Long-Term Care PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and outputs results to a printer file (`PRTOPER`). Its extensive change log indicates frequent updates to pricing methodologies and data structures.
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

### LTOPN212
*   **Overview:** This subroutine is a crucial component of the LTCH PPS pricer. It is responsible for loading necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) before calling the `LTDRV212` module to perform the actual pricing calculations. It serves as an intermediary, managing data flow and table loading.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in LTMGR212)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212, referring to provider data)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

### LTDRV212
*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (based on the bill's fiscal year) to execute the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Manages various return codes for error and exception handling.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Numerous calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` arises from its handling of numerous `LTCAL` module versions, each tailored for a specific fiscal year. While data structures passed are largely consistent, minor variations may exist across different `LTCAL` versions. The extensive conditional logic is vital for selecting the correct `LTCAL` module and managing transitions between rate years and data structures.

## Fiscal Year Specific Calculation Modules (LTCALxxx)

These programs are responsible for performing the actual payment calculations for LTCH claims, adhering to the specific IPPS rules for a given fiscal year.

### LTCAL162
*   **Overview:** This COBOL program calculates Medicare payments for LTCH claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:**
    *   Likely calls programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (claim details) to itself.
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### LTCAL170
*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. Passes analogous data structures.

### LTCAL183
*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, utilizing the `LTDRG181` and `IPDRG181` tables. It incorporates significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

### LTCAL190
*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

### LTCAL202
*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, incorporating 2020 IPPS rules and adding logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212
*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, incorporating 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Definition Programs (Tables)

These programs define data structures that are used as tables for lookups within the pricing modules. They do not execute logic but provide essential data.

### IPPS DRG Data Tables
*   **Overview:** These programs define tables containing data related to Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for specific years. The data typically includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:**
    *   Store IPPS DRG data for specific years, providing a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (e.g., `LTCALxxx` modules) to retrieve DRG information.
    *   **IPDRG160:** Stores IPPS DRG data for 2015. Data structure passed *from* it: `DRG-DATA-TAB` (DRG code, weight, ALOS, description).
    *   **IPDRG170:** Stores IPPS DRG data for 2016. Data structure passed *from* it: `DRG-DATA-TAB`.
    *   **IPDRG181:** Stores IPPS DRG data for 2017. Data structure passed *from* it: `DRG-DATA-TAB`.
    *   **IPDRG190:** Stores IPPS DRG data for 2018. Data structure passed *from* it: `DRG-DATA-TAB`.
    *   **IPDRG200:** Stores IPPS DRG data for 2019. Data structure passed *from* it: `DRG-DATA-TAB`.
    *   **IPDRG211:** Stores IPPS DRG data for 2020. Data structure passed *from* it: `DRG-DATA-TAB`.

### LTCH DRG Data Tables
*   **Overview:** These programs define data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code.
    *   **LTDRG160:** Contains LTCH DRG data for 2016. Data structure passed *from* it: `WWM-ENTRY` (DRG code, relative weight, ALOS).
    *   **LTDRG170:** Contains LTCH DRG data for 2017. Data structure passed *from* it: `WWM-ENTRY`.
    *   **LTDRG181:** Contains LTCH DRG data for 2018. Data structure passed *from* it: `WWM-ENTRY`.
    *   **LTDRG190:** Contains LTCH DRG data for 2019. Data structure passed *from* it: `WWM-ENTRY`.
    *   **LTDRG200:** Contains LTCH DRG data for 2020. Data structure passed *from* it: `WWM-ENTRY`.
    *   **LTDRG210:** Contains LTCH DRG data for 2021. Data structure passed *from* it: `WWM-ENTRY`.

## Supporting Data Definitions

### RUFL200
*   **Overview:** This is a copybook containing the Rural Floor Factor Table, used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

**General Notes:**
*   The ellipses ("...") in program names suggest they are part of larger, more specific program names.
*   The exact details of data files and other called programs would require examination of the full application context.
*   `COPY` statements indicate the inclusion of external code modules, the contents of which are critical for a complete understanding.