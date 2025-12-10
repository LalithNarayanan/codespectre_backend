## Program Overview

This document consolidates and analyzes the program descriptions extracted from multiple functional specification files. It provides a comprehensive overview of the Long-Term Care Prospective Payment System (LTCH PPS) pricing modules, detailing their purpose, business functions, and interactions with other programs and data structures.

---

### Core Pricing Driver and Subroutines

The central components of the LTCH PPS pricer are `LTMGR212`, `LTOPN212`, and `LTDRV212`, which work in conjunction to process bill records and calculate payments.

#### Program: LTMGR212

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from a file named `BILLFILE`, invokes the `LTOPN212` subroutine to execute pricing calculations, and subsequently writes the results to an output printer file named `PRTOPER`. The program's extensive change log indicates numerous revisions, reflecting ongoing updates to pricing methodologies and data structures.

*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file (`BILLFILE`).
    *   Calls the `LTOPN212` subroutine to perform payment calculations based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file input/output operations, including opening, reading, writing, and closing files.

*   **Called Programs and Data Structures:**
    *   **LTOPN212:** This subroutine is called to perform the pricing calculations.
        *   **Data Structures Passed:**
            *   **BILL-NEW-DATA:** Contains comprehensive bill information, including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
            *   **PPS-DATA-ALL:** Holds pre-calculated PPS data, such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
            *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
            *   **PPS-PAYMENT-DATA:** Stores calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
            *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

#### Program: LTOPN212

*   **Overview:** This subroutine is a fundamental part of the Long-Term Care PPS pricer. Its primary role is to load essential tables, including provider, MSA, CBSA, and IPPS CBSA wage index tables. It then delegates the actual pricing calculations to the `LTDRV212` module. `LTOPN212` serves as an intermediary, managing data flow and table loading before transferring control to the calculation module.

*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill's discharge date.
    *   Calls the main pricing calculation module, `LTDRV212`.
    *   Returns return codes to indicate the success or failure of the pricing process.

*   **Called Programs and Data Structures:**
    *   **LTDRV212:** The core pricing calculation module.
        *   **Data Structures Passed:**
            *   **BILL-NEW-DATA:** (Same as in `LTMGR212`)
            *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
            *   **PPS-CBSA:** (Same as in `LTMGR212`)
            *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
            *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
            *   **PROV-RECORD-FROM-USER:** (Same as in `LTMGR212`'s `PROV-NEW-HOLD` which contains provider information)
            *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
            *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
            *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
            *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

#### Program: LTDRV212

*   **Overview:** This module is the computational core of the LTCH PPS pricing calculation. It retrieves the relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. Subsequently, it invokes the appropriate `LTCALxxx` module (selected based on the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.

*   **Business Functions:**
    *   Retrieves wage index records from tables using the bill's discharge date.
    *   Determines the correct `LTCALxxx` module to call based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to execute payment calculations.
    *   Manages various return codes to handle errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments, where applicable.

*   **Called Programs and Data Structures:**
    *   **Many calls to programs of the form `LTCALxxxx`:** Where `xxxx` represents a specific version number (e.g., 032, 080, 111, 212). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in `LTMGR212`, but may use `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in `LTMGR212`)
        *   **PPS-CBSA:** (Same as in `LTMGR212`)
        *   **PPS-PAYMENT-DATA:** (Same as in `LTMGR212`)
        *   **PRICER-OPT-VERS-SW:** (Same as in `LTMGR212`)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data, including CBSA, effective date, and wage index values.
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

*   **Important Note:** The complexity of `LTDRV212` arises from its need to support numerous versions of the `LTCAL` modules, each tailored for specific fiscal years. While the data structures passed are largely consistent, minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing transitions between different rate years and data structures.

---

### Data Tables and Specific Year Calculations

Several programs function as data tables, providing crucial information for the `LTCAL` modules, which perform the actual payment calculations for specific fiscal years.

#### Data Tables (IPPS DRG and LTCH DRG)

The following programs are identified as data tables, storing Diagnosis Related Group (DRG) information for different fiscal years. They are not executable programs in the traditional sense but are called by other programs to retrieve data.

*   **Program: IPDRG160**
    *   **Overview:** Defines an Inpatient Prospective Payment System (IPPS) DRG table for the year 2015.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2015 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs (like `LTCAL162`) to retrieve DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB` (containing DRG code, weight, ALOS, and description).
    *   **Data Structure Passed To:** A DRG code (likely 3-digit numeric or alphanumeric).

*   **Program: IPDRG170**
    *   **Overview:** Defines an IPPS DRG table for the year 2016.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2016 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs to retrieve 2016 DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG181**
    *   **Overview:** Defines an IPPS DRG table for the year 2017.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2017 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs to retrieve 2017 DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG190**
    *   **Overview:** Defines an IPPS DRG table for the year 2018.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2018 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs to retrieve 2018 DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG200**
    *   **Overview:** Defines an IPPS DRG table for the year 2019.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2019 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs to retrieve 2019 DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Program: IPDRG211**
    *   **Overview:** Defines an IPPS DRG table for the year 2020.
    *   **Business Functions Addressed:** Stores IPPS DRG data for 2020 and provides a lookup mechanism for DRG codes and associated information.
    *   **Called by:** Other programs to retrieve 2020 DRG information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.
    *   **Data Structure Passed To:** A DRG code.

*   **Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**
    *   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for various years. They include DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Business Functions Addressed:** Store LTCH DRG data for lookup purposes.
    *   **Called by:** The `LTCAL...` programs.
    *   **Data Structure Passed From:** `WWM-ENTRY` (containing DRG code, relative weight, and ALOS).
    *   **Data Structure Passed To:** A DRG code.

#### Fiscal Year Specific Calculation Modules (`LTCALxxx`)

These programs perform the detailed payment calculations for LTCH claims, incorporating the specific rules and data for each fiscal year.

*   **Program: LTCAL162**
    *   **Overview:** Calculates Medicare payment for LTCH claims based on the 2016 IPPS rules, utilizing the `LTDRG160` and `IPDRG160` tables.
    *   **Business Functions Addressed:**
        *   Reads LTCH claim data.
        *   Validates claim data.
        *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
        *   Calculates high-cost outliers.
        *   Determines appropriate return codes.
        *   Writes results to output data structures.
    *   **Other Programs Called:** Likely calls programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   **Data Structures Passed:** `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, `WAGE-NEW-IPPS-INDEX-RECORD`.

*   **Program: LTCAL170**
    *   **Overview:** Calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
    *   **Business Functions Addressed:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, passing analogous data structures to `LTCAL162`.

*   **Program: LTCAL183**
    *   **Overview:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, utilizing the `LTDRG181` and `IPDRG181` tables. This version includes significant changes in short-stay outlier and Subclause II handling.
    *   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

*   **Program: LTCAL190**
    *   **Overview:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
    *   **Business Functions Addressed:** Similar to previous versions, reflecting the 2019 IPPS rules.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

*   **Program: LTCAL202**
    *   **Overview:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.
    *   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
    *   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

*   **Program: LTCAL212**
    *   **Overview:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.
    *   **Business Functions Addressed:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

---

### Utility Copybook

#### Program: RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table, specifically used by `LTDRV212` for IPPS calculations related to Fiscal Year 2020. It is a data definition included in other programs rather than an executable program itself.
*   **Business Functions:** Provides data essential for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it is a copybook and does not call other programs.

---

**Important Notes:**

*   The ellipses ("...") in program names suggest these might be parts of longer, more specific program names.
*   The exact details of data files and other programs called would require access to the full context of the application.
*   `COPY` statements indicate the inclusion of external code modules, the contents of which are critical for a complete understanding of program functionality.