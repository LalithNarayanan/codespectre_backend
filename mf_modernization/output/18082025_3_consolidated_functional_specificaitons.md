## Program Overview

This document consolidates and organizes program information extracted from multiple functional specification files, providing a comprehensive view of the Long-Term Care Prospective Payment System (LTCH PPS) pricer modules and related data tables.

---

### Core Pricing Driver and Subroutines

The primary execution flow for processing LTCH claims involves a driver program that initiates calls to various subroutines responsible for data loading, wage index determination, and payment calculations.

#### **Program: LTMGR212**

*   **Overview:** This program acts as the driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes the results to the printer file `PRTOPER`. The program's extensive change log indicates numerous revisions, reflecting updates to pricing methodologies and data structures over time.

*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).

*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

#### **Program: LTOPN212**

*   **Overview:** This subroutine is a critical component of the LTCH PPS pricer. Its primary role is to load necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then invoke the `LTDRV212` module to perform the actual pricing calculations. It serves as an intermediary, managing data flow and table loading before delegating the calculation to the subsequent module.

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
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212, referring to provider information)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

#### **Program: LTDRV212**

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves the appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (determined by the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.

*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments, as applicable.

*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data, including CBSA, effective date, and wage index values.
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

*   **Important Note:** The complexity of `LTDRV212` stems from its handling of numerous versions of the `LTCAL` modules, each designed for a specific fiscal year. The data structures passed remain largely consistent, though minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing transitions between different rate years and data structures.

---

### Fiscal Year Specific Calculation Modules (`LTCALxxx`)

These programs are responsible for the actual payment calculations, tailored to the specific IPPS rules of a given fiscal year. They leverage various data tables for DRG weights, ALOS, and wage index information.

#### **Program: LTCAL162**

*   **Overview:** This COBOL program calculates Medicare payments for Long-Term Care Hospital (LTCH) claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.

*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.

*   **Other Programs Called:**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   It passes `BILL-NEW-DATA` (containing claim details) to itself for processing.
    *   It passes `PROV-NEW-HOLD` (provider information) to itself.
    *   It passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   It passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

#### **Program: LTCAL170**

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.

*   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017. This includes handling of budget neutrality adjustments for site-neutral payments.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. It passes data structures analogous to those in `LTCAL162`.

#### **Program: LTCAL183**

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. It incorporates significant changes in short-stay outlier and Subclause II handling.

*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but reflecting 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

#### **Program: LTCAL190**

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.

*   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

#### **Program: LTCAL202**

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.

*   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).

*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

#### **Program: LTCAL212**

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.

*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.

*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

---

### Data Tables for DRG Information

These programs define data tables that store Diagnosis Related Group (DRG) information specific to Inpatient Prospective Payment System (IPPS) and Long-Term Care Hospital (LTCH) PPS for various years. They serve as lookup mechanisms for DRG codes, weights, and average lengths of stay (ALOS).

#### **Programs: IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211**

*   **Overview:** These programs define tables containing data related to Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for the years 2015, 2016, 2017, 2018, 2019, and 2020, respectively. The data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.

*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for specific years.
    *   Provides a lookup mechanism for DRG codes and associated information.

*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them would be a DRG code (likely a 3-digit numeric or alphanumeric code). The data structure passed *from* them is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

#### **Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years (2016, 2017, 2018, 2019, 2020, and 2021 respectively, based on the `LTCAL` program usage). The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.

*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.

*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

---

### Utility Data Structures

#### **Program: RUFL200**

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not an executable program but a data definition included in other programs.

*   **Business Functions:** Provides data for determining rural floor wage indices.

*   **Called Programs and Data Structures:** None; it's a copybook.

---

**Important Notes:**

*   The ellipses ("...") in some program names suggest they are part of a larger naming convention, indicating potential variations or specific versions.
*   The exact names and functionalities of associated data files and other programs called would require examination of the full context of the application.
*   `COPY` statements indicate the inclusion of external code modules; understanding the content of these copied modules is crucial for a complete analysis.
*   The interplay between `LTDRV212` and the various `LTCALxxx` modules highlights a design pattern where core logic is maintained in a central driver, while year-specific calculations are handled by modularized programs.