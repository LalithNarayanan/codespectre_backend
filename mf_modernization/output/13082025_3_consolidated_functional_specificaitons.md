# Program Overview

This document consolidates information from multiple functional specifications to provide a comprehensive overview of the COBOL programs involved in the Long-Term Care Hospital (LTCH) Prospective Payment System (PPS) pricer modules.

## Core Pricing Logic and Driver Programs

The following programs form the core of the LTCH PPS pricing calculation and the overall processing flow:

### Program: LTMGR212

*   **Overview:** This program acts as a driver for testing the Long-Term Care PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes the results to a printer file (`PRTOPER`). Its extensive change log indicates numerous revisions to pricing methodologies and data structures over time.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   `BILL-NEW-DATA`: Contains bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   `PPS-DATA-ALL`: Contains pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   `PPS-CBSA`: Contains the Core Based Statistical Area code.
        *   `PPS-PAYMENT-DATA`: Contains calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   `PRICER-OPT-VERS-SW`: Contains pricing option and version information (option switch, PPDRV version).

### Program: LTOPN212

*   **Overview:** This subroutine is a key component of the Long-Term Care PPS pricer. Its primary function is to load necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then call the `LTDRV212` module to perform the actual pricing calculations. It acts as an intermediary, managing data flow and table loading before passing control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines which wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   `BILL-NEW-DATA`: (same as in LTMGR212)
        *   `PPS-DATA-ALL`: (same as in LTMGR212)
        *   `PPS-CBSA`: (same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (same as in LTMGR212)
        *   `PROV-RECORD-FROM-USER`: (same as in LTMGR212)
        *   `CBSAX-TABLE-FROM-USER`: Contains the CBSA wage index table.
        *   `IPPS-CBSAX-TABLE-FROM-USER`: Contains the IPPS CBSA wage index table.
        *   `MSAX-TABLE-FROM-USER`: Contains the MSA wage index table.
        *   `WORK-COUNTERS`: Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

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
    *   Numerous calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   `BILL-NEW-DATA`: (same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   `PPS-DATA-ALL`: (same as in LTMGR212)
        *   `PPS-CBSA`: (same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (same as in LTMGR212)
        *   `PROV-NEW-HOLD`: Contains the provider record.
        *   `WAGE-NEW-INDEX-RECORD-CBSA`: Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   `WAGE-IPPS-INDEX-RECORD-CBSA`: Contains the IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` stems from its handling of numerous versions of the `LTCAL` modules, each designed for a specific fiscal year. The data structures passed remain largely consistent, though some minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing the transition between different rate years and data structures.

## Fiscal Year Specific Calculation Modules (`LTCALxxx`)

These programs perform the actual payment calculations based on specific fiscal year IPPS rules. They are called by `LTDRV212`.

### Program: LTCAL162

*   **Overview:** This COBOL program calculates the Medicare payment for Long-Term Care Hospital (LTCH) claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables for data lookups.
*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:**
    *   Likely calls other programs to read claim data (e.g., `LTDRV...`) and provider-specific data (e.g., `LTWIX...`).
    *   Passes `BILL-NEW-DATA` (containing claim details) to itself (implicitly for processing).
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### Program: LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. It passes data structures analogous to those in `LTCAL162`.

### Program: LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. It notes significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

### Program: LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

### Program: LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.
*   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### Program: LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.
*   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Table Programs (DRG and Wage Index Data)

These programs define and store data tables used by the calculation modules. They are not executable programs in the traditional sense but are called by other programs to retrieve specific data.

### Program: RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not a program itself but a data definition that is included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

### IPPS DRG Table Programs (2015-2020)

These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for specific years.

*   **Program: IPDRG160**
    *   **Overview:** Defines a table (`PPS-DRG-TABLE`) with IPPS DRG data for 2015, including DRG codes, weights, average lengths of stay (ALOS), and descriptions.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2015; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is *called* by other programs (like `LTCAL162`) to retrieve DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

*   **Program: IPDRG170**
    *   **Overview:** Defines an IPPS DRG table for 2016.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2016; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2016 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

*   **Program: IPDRG181**
    *   **Overview:** Defines an IPPS DRG table for 2017.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2017; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2017 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

*   **Program: IPDRG190**
    *   **Overview:** Defines an IPPS DRG table for 2018.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2018; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2018 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

*   **Program: IPDRG200**
    *   **Overview:** Defines an IPPS DRG table for 2019.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2019; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2019 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

*   **Program: IPDRG211**
    *   **Overview:** Defines an IPPS DRG table for 2020.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2020; provides a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2020 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

### LTCH DRG Table Programs (2016-2021)

These programs define tables containing Long-Term Care Hospital (LTCH) DRG data for different years.

*   **Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**
    *   **Overview:** These are data tables containing LTCH DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
    *   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

**General Important Notes:**

*   The ellipses ("...") in program names suggest that these are parts of larger program names, and the exact names and functionalities of related data files and other called programs would require consulting the full context of the application.
*   The use of `COPY` statements indicates the inclusion of external code modules, and their contents are crucial for a complete understanding of the system's logic.
*   The programs described are primarily COBOL-based, indicating a legacy system architecture. The evolution of these programs over different fiscal years reflects changes in Medicare payment rules and policies.