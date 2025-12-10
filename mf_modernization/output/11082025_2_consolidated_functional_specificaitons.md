# Program Overview

This document consolidates the program overview information extracted from multiple functional specification files, detailing the Long-Term Care Prospective Payment System (LTCH PPS) pricing modules and related data components.

## Core Processing Programs

The central flow of the LTCH PPS pricing process is driven by a series of interconnected COBOL programs.

### LTMGR212: The Driver Program

*   **Overview:** `LTMGR212` acts as the primary driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and outputs the results to a printer file, `PRTOPER`. The program's extensive change log indicates frequent updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information, including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

### LTOPN212: The Subroutine for Table Loading and Calculation Initiation

*   **Overview:** `LTOPN212` is a key subroutine responsible for loading essential tables required for LTCH PPS pricing. These tables include provider data, MSA, CBSA, and IPPS CBSA wage index tables. It then calls the `LTDRV212` module to perform the actual pricing calculations, acting as an intermediary to manage data flow and control before passing execution to the calculation engine.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill's discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   **BILL-NEW-DATA:** (Same as in `LTMGR212`)
        *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
        *   **PPS-CBSA:** (Same as in `LTMGR212`)
        *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
        *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
        *   **PROV-RECORD-FROM-USER:** (Same as in `LTMGR212`)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

### LTDRV212: The Core Pricing Calculation Engine

*   **Overview:** `LTDRV212` is the central module for LTCH PPS payment calculations. It retrieves relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. Subsequently, it calls the appropriate `LTCALxxx` module, selected based on the bill's fiscal year, to execute the final payment computations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number, e.g., 032, 080, 111, 212). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in `LTMGR212`, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
        *   **PPS-CBSA:** (Same as in `LTMGR212`)
        *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
        *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data, including CBSA, effective date, and wage index values.
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

**Important Note on `LTDRV212` Complexity:** The complexity of `LTDRV212` is significantly driven by its need to manage calls to numerous versions of the `LTCAL` modules, each tailored for specific fiscal years. While the data structures passed remain largely consistent, minor variations may exist across different `LTCAL` versions. The program's extensive conditional logic is crucial for selecting the correct `LTCAL` module and managing transitions between different rate years and associated data structures.

## Fiscal Year Specific Calculation Modules (`LTCALxxx`)

These modules perform the actual payment calculations based on the rules for a specific fiscal year.

*   **LTCAL162:** Calculates Medicare payments for LTCH claims under the 2016 IPPS rules, utilizing `LTDRG160` and `IPDRG160` tables.
    *   **Business Functions:** Reads LTCH claim data, validates claim data, calculates LTCH payments (standard, short-stay outlier, site-neutral, blended), calculates high-cost outliers, determines appropriate return codes, and writes results to output data structures.
    *   **Other Programs Called:** Likely calls programs for claim data (`LTDRV...`) and provider-specific data (`LTWIX...`). Passes `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD` to itself (implicitly for processing).

*   **LTCAL170:** Calculates Medicare payments for LTCH claims using the 2017 IPPS rules and `LTDRG170`, `IPDRG170` tables.
    *   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling budget neutrality adjustments for site-neutral payments.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input, passing analogous data structures to `LTCAL162`.

*   **LTCAL183:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables.
    *   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2018 rules, including significant changes to short-stay outlier calculations and the removal of Subclause II processing.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input, analogous to previous `LTCAL` programs.

*   **LTCAL190:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
    *   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input, similar to previous `LTCAL` programs.

*   **LTCAL202:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables.
    *   **Business Functions:** Similar to previous versions, incorporating 2020 IPPS rules and adding logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
    *   **Other Programs Called:** Likely calls programs for claim and provider data input. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

*   **LTCAL212:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables.
    *   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

**Important Note on `LTCAL` Program Naming:** The ellipses ("...") in some program names (e.g., `LTCALxxxx`) suggest that these represent a family of programs, with specific versions identified by the trailing numbers. The exact names and functionalities of any other data files or programs called would require examination of the complete application context. `COPY` statements indicate the inclusion of external code modules, which are critical for a full understanding.

## Data Table Programs

These programs define data tables used by the calculation modules, primarily for lookups.

*   **IPDRG160:** Defines an Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) table for 2015.
    *   **Business Functions:** Stores IPPS DRG data for 2015, providing a lookup mechanism for DRG codes and associated information.
    *   **Other Programs Called:** This is a data table and does not call other programs. It is called by other programs (e.g., `LTCAL162`) to retrieve DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing the DRG code, weight, ALOS, and description.

*   **IPDRG170:** Defines an IPPS DRG table for 2016.
    *   **Business Functions:** Stores IPPS DRG data for 2016, providing a lookup mechanism.
    *   **Other Programs Called:** Data table; called by other programs for 2016 DRG information. Passes `DRG-DATA-TAB` containing DRG code, weight, ALOS, and description.

*   **IPDRG181:** Defines an IPPS DRG table for 2017.
    *   **Business Functions:** Stores IPPS DRG data for 2017, providing a lookup mechanism.
    *   **Other Programs Called:** Data table; called by other programs for 2017 DRG information. Passes `DRG-DATA-TAB` containing DRG code, weight, ALOS, and description.

*   **IPDRG190:** Defines an IPPS DRG table for 2018.
    *   **Business Functions:** Stores IPPS DRG data for 2018, providing a lookup mechanism.
    *   **Other Programs Called:** Data table; called by other programs for 2018 DRG information. Passes `DRG-DATA-TAB` containing DRG code, weight, ALOS, and description.

*   **IPDRG200:** Defines an IPPS DRG table for 2019.
    *   **Business Functions:** Stores IPPS DRG data for 2019, providing a lookup mechanism.
    *   **Other Programs Called:** Data table; called by other programs for 2019 DRG information. Passes `DRG-DATA-TAB` containing DRG code, weight, ALOS, and description.

*   **IPDRG211:** Defines an IPPS DRG table for 2020.
    *   **Business Functions:** Stores IPPS DRG data for 2020, providing a lookup mechanism.
    *   **Other Programs Called:** Data table; called by other programs for 2020 DRG information. Passes `DRG-DATA-TAB` containing DRG code, weight, ALOS, and description.

*   **LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210:** These are all data tables containing Long-Term Care Hospital (LTCH) DRG data for different years.
    *   **Overview:** These tables store LTCH DRG data, including DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Business Functions:** Provide LTCH DRG data for lookups.
    *   **Other Programs Called:** These are data tables and do not call other programs. They are called by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

## Supporting Data Definitions

### RUFL200: Rural Floor Factor Table

*   **Overview:** `RUFL200` is a copybook that defines the Rural Floor Factor Table. This table is used by `LTDRV212` specifically for IPPS calculations pertaining to Fiscal Year 2020. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it is a copybook.

**General Note on Data Structures:** The data structures like `BILL-NEW-DATA`, `PPS-DATA-ALL`, `PPS-CBSA`, `PPS-PAYMENT-DATA`, `PRICER-OPT-VERS-SW`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD-CBSA`, and `WAGE-IPPS-INDEX-RECORD-CBSA` are consistently passed across multiple programs, indicating a standardized data exchange mechanism for the LTCH PPS pricing calculations. Minor variations in `BILL-NEW-DATA` (e.g., `BILL-DATA-FY03-FY15`) exist for compatibility with older fiscal years.