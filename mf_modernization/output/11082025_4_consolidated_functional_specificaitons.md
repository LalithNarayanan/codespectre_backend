# Program Overview

This document consolidates information from multiple functional specifications regarding COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricer. It outlines the purpose, business functions, and interdependencies of these programs.

## Core Pricing Driver and Subroutines

The primary driver for the LTCH PPS pricer is `LTMGR212`, which orchestrates the pricing calculations. It interacts with several subroutines and data tables to achieve its objectives.

### Program: LTMGR212

*   **Overview:** This program acts as the driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes the results to a printer file (`PRTOPER`). Its extensive change log indicates numerous revisions, reflecting updates to pricing methodologies and data structures over time.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

### Program: LTOPN212

*   **Overview:** This subroutine is a core component of the LTCH PPS pricer. Its primary function is to load necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then call the `LTDRV212` module to perform the actual pricing calculations. It serves as an intermediary, managing data flow and table loading before passing control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines which wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in `LTMGR212`)
        *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
        *   **PPS-CBSA:** (Same as in `LTMGR212`)
        *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
        *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
        *   **PROV-RECORD-FROM-USER:** (Same as in `LTMGR212` - likely refers to provider data)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

### Program: LTDRV212

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves the appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (depending on the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in `LTMGR212`, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
        *   **PPS-CBSA:** (Same as in `LTMGR212`)
        *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
        *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

### Copybook: RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

**Important Note on `LTDRV212` Complexity:** The complexity of `LTDRV212` arises from its handling of numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While the data structures passed are largely consistent, minor variations may exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the correct `LTCAL` module and managing transitions between different rate years and data structures.

## Year-Specific DRG and Calculation Modules

The system utilizes specific programs to manage Diagnosis Related Group (DRG) data for various years and to perform the actual payment calculations based on those DRGs and the corresponding fiscal year rules.

### Data Tables for IPPS DRG Information

These programs define tables that store Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for different years. They do not call other programs but are called by the `LTCAL` programs to retrieve DRG information.

*   **Program: IPDRG160**
    *   **Overview:** Defines an IPPS DRG table for the year 2015, containing DRG codes, weights, average lengths of stay (ALOS), and descriptions.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2015 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB` (contains DRG code, weight, ALOS, and description).
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG170**
    *   **Overview:** Defines an IPPS DRG table for the year 2016.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2016 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG181**
    *   **Overview:** Defines an IPPS DRG table for the year 2017.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2017 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG190**
    *   **Overview:** Defines an IPPS DRG table for the year 2018.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2018 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG200**
    *   **Overview:** Defines an IPPS DRG table for the year 2019.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2019 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG211**
    *   **Overview:** Defines an IPPS DRG table for the year 2020.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2020 and provides a lookup mechanism.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

### LTCH Payment Calculation Programs (`LTCALxxx`)

These programs perform the actual Medicare payment calculations for LTCH claims, adhering to the IPPS rules for specific fiscal years. They leverage the year-specific DRG tables and other relevant data.

*   **Program: LTCAL162**
    *   **Overview:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
    *   **Business Functions Addressed:** Reads LTCH claim data, validates claim data, calculates LTCH payments (standard, short-stay outlier, site-neutral, blended), calculates high-cost outliers, determines appropriate return codes, and writes results to output data structures.
    *   **Other Programs Called:** Likely calls programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   **Data Structures Passed:** `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, `WAGE-NEW-IPPS-INDEX-RECORD`.

*   **Program: LTCAL170**
    *   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
    *   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017, including handling budget neutrality adjustments for site-neutral payments.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, passing analogous data structures to `LTCAL162`.

*   **Program: LTCAL183**
    *   **Overview:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. Significant changes in short-stay outlier and Subclause II handling are noted.
    *   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

*   **Program: LTCAL190**
    *   **Overview:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
    *   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

*   **Program: LTCAL202**
    *   **Overview:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
    *   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
    *   **Other Programs Called:** Likely calls programs to read claim and provider data. Also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

*   **Program: LTCAL212**
    *   **Overview:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
    *   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

### Data Tables for LTCH DRG Information

These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years. They are called by the `LTCAL` programs to retrieve LTCH DRG-specific information.

*   **Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**
    *   **Overview:** These tables store LTCH DRG data for various years, including DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Business Functions Addressed:** Store LTCH DRG data for lookups.
    *   **Data Structure Passed From:** `WWM-ENTRY` (contains DRG code, relative weight, and ALOS).
    *   **Data Structure Passed To:** A DRG code.

**Important General Notes:**

*   The ellipses ("...") in program names like `LTCALxxxx` and `LTDRGxxxx` indicate that these are part of a naming convention representing different versions or fiscal years.
*   The `COPY` statements mentioned in the original text signify the inclusion of external code modules. The full functionality of these programs relies on the content of these copied modules.
*   The exact names and functionalities of specific data files and other programs called would require examination of the complete application context.