# Program Overview

This document consolidates information from multiple functional specifications to provide a comprehensive overview of the Long-Term Care Prospective Payment System (LTCH PPS) pricer modules and related data programs. The system is designed to calculate Medicare payments for LTCH claims based on various fiscal year-specific rules and data.

## Core Pricing Driver and Subroutines

The core of the LTCH PPS pricing calculation is driven by a set of interconnected COBOL programs.

### LTMGR212

*   **Overview:** This program acts as the primary driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and outputs the results to a printer file named `PRTOPER`. The program's extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file Input/Output operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

### LTOPN212

*   **Overview:** This subroutine is a crucial component of the LTCH PPS pricer. It is responsible for loading necessary data tables, including provider, MSA, CBSA, and IPPS CBSA wage index tables. After loading these tables, it calls the `LTDRV212` module to perform the actual pricing calculations, acting as an intermediary to manage data flow and table loading before passing control.
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
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212, referring to provider data)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

### LTDRV212

*   **Overview:** This module is the central component for LTCH PPS pricing calculations. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module, determined by the bill's fiscal year, to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes for error and exception management.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments as applicable.
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a fiscal year or version number, e.g., 032, 080, 111, 212). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years).
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data, including CBSA, effective date, and wage index values.
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

    *   **Important Note:** The complexity of `LTDRV212` arises from its handling of numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While the data structures passed are largely consistent, minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is critical for selecting the correct `LTCAL` module and managing transitions between different rate years and data structures.

## Fiscal Year-Specific Calculation Modules (`LTCALxxx`)

These programs perform the actual payment calculations based on the IPPS rules for specific fiscal years.

### LTCAL162

*   **Overview:** This COBOL program calculates Medicare payments for LTCH claims, adhering to the 2016 IPPS rules. It utilizes data from the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments, including standard, short-stay outlier, site-neutral, and blended payments.
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:** This program likely calls other programs to read claim data (e.g., `LTDRV...`) and provider-specific data (e.g., `LTWIX...`).
    *   It passes `BILL-NEW-DATA` (containing claim details) for processing.
    *   It passes `PROV-NEW-HOLD` (provider information).
    *   It passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data).
    *   It passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data).

### LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but incorporates updated rules for 2017, including handling budget neutrality adjustments for site-neutral payments.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. It passes analogous data structures.

### LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, utilizing the `LTDRG181` and `IPDRG181` tables. It reflects significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but adapted for 2018 rules, including modifications to short-stay outlier calculations and the removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

### LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

### LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special logic related to COVID-19.
*   **Business Functions:** Similar to previous versions, incorporating 2020 IPPS rules and adding logic to handle COVID-19 adjustments to claim payments (e.g., re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules, using the `LTDRG210` and `IPDRG211` tables. It incorporates new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, utilizing supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Tables and Copybooks

These components provide the necessary data for the pricing calculations.

### IPPS DRG Data Tables (2015-2020)

*   **Programs:** `IPDRG160` (2015), `IPDRG170` (2016), `IPDRG181` (2017), `IPDRG190` (2018), `IPDRG200` (2019), `IPDRG211` (2020).
*   **Overview:** These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for specific years. The data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:** Store IPPS DRG data for lookup purposes. Provide a mechanism for retrieving DRG codes and associated information.
*   **Other Programs Called:** These are data tables and do not call other programs. They are called by other programs (like the `LTCALxxx` modules) to retrieve DRG information.
    *   The data structure passed *to* them is typically a DRG code (numeric or alphanumeric).
    *   The data structure passed *from* them is `DRG-DATA-TAB`, containing the DRG code, weight, ALOS, and description.

### LTCH DRG Data Tables (Fiscal Year Specific)

*   **Programs:** `LTDRG160`, `LTDRG170`, `LTDRG181`, `LTDRG190`, `LTDRG200`, `LTDRG210`.
*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different fiscal years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups by the `LTCALxxx` programs.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs.
    *   The data structure passed *to* them would be a DRG code.
    *   The data structure passed *from* them is `WWM-ENTRY`, containing the DRG code, relative weight, and ALOS.

### RUFL200 (Copybook)

*   **Overview:** This copybook contains the Rural Floor Factor Table, specifically used by `LTDRV212` for IPPS calculations for Fiscal Year 2020. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

**General Notes:**

*   The ellipses ("...") in some program names suggest these are part of a larger naming convention.
*   The exact functionality of data files and other called programs would require access to the complete application context.
*   `COPY` statements indicate the inclusion of external code modules, which are essential for a full understanding of program logic.