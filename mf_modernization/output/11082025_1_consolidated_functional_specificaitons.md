# Program Overview

This document consolidates information about various COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricing calculations. The programs described here handle data input, pricing logic, and the application of specific fiscal year rules and adjustments.

## Core Pricing Driver and Subroutines

The central flow of the LTCH PPS pricing process is orchestrated by a driver program that calls various subroutines to perform specific calculations.

### LTMGR212

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from a file named `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and subsequently writes the results to an output printer file named `PRTOPER`. The program's extensive change log indicates numerous revisions, reflecting updates to pricing methodologies and data structures over time.

*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file Input/Output operations (opening, reading, writing, and closing files).

*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information, including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, such as the option switch and PPDRV version.

### LTOPN212

*   **Overview:** This subroutine is a fundamental component of the Long-Term Care PPS pricer. Its main responsibility is to load essential tables, including provider, MSA, CBSA, and IPPS CBSA wage index tables, before calling the `LTDRV212` module to execute the actual pricing calculations. It functions as an intermediary, managing data flow and table loading before transferring control to the calculation module.

*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill's discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes to indicate the success or failure of the pricing process.

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

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves the relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module, contingent on the bill's fiscal year, to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.

*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Manages various return codes for error and exception handling.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments as applicable.

*   **Called Programs and Data Structures:**
    *   Numerous calls are made to programs of the form `LTCALxxxx`, where `xxxx` represents a version number (e.g., 032, 080, 111, 212). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

*   **Important Note:** The complexity of `LTDRV212` arises from its management of numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While the data structures passed remain largely consistent, minor variations might exist across different `LTCAL` versions (not detailed here). The extensive conditional logic within `LTDRV212` is critical for selecting the correct `LTCAL` module and handling transitions between different rate years and data structures.

### RUFL200

*   **Overview:** This is a copybook, not an executable program. It contains the Rural Floor Factor Table, which is utilized by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It serves as a data definition that is incorporated into other programs.

*   **Business Functions:** Provides data for determining rural floor wage indices.

*   **Called Programs and Data Structures:** None, as it is a copybook.

## Fiscal Year Specific Calculation Modules (`LTCALxxx`)

These programs implement the specific LTCH PPS payment calculation logic for different fiscal years, leveraging DRG and IPPS data tables.

### LTCAL162

*   **Overview:** This COBOL program calculates the Medicare payment for Long-Term Care Hospital (LTCH) claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.

*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.

*   **Other Programs Called:**
    *   Likely calls other programs for reading claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (containing claim details) to itself for processing.
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.

*   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017. Includes handling of budget neutrality adjustments for site-neutral payments.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. It passes data structures analogous to those in `LTCAL162`.

### LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. It incorporates significant changes in short-stay outlier and Subclause II handling.

*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

### LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.

*   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

### LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.

*   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).

*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.

*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.

*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Tables for DRG and Wage Index Information

These programs define and store data critical for the pricing calculations, typically used by the `LTCALxxx` modules.

### IPPS DRG Tables (2015-2020)

*   **Programs:** `IPDRG160` (2015), `IPDRG170` (2016), `IPDRG181` (2017), `IPDRG190` (2018), `IPDRG200` (2019), `IPDRG211` (2020).
*   **Overview:** These programs define data tables containing information related to Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for specific years. The data typically includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for the respective years.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them would be a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

### LTCH DRG Tables (Various Years)

*   **Programs:** `LTDRG160`, `LTDRG170`, `LTDRG181`, `LTDRG190`, `LTDRG200`, `LTDRG210`.
*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

*   **Important Note:** The ellipses ("...") in program names suggest that these are parts of larger program names, and the exact names and functionalities of associated data files and other called programs would require examination of the full system context. Additionally, `COPY` statements indicate the inclusion of external code modules, the content of which is crucial for a comprehensive understanding.