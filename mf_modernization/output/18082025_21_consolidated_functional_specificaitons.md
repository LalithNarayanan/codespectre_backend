## Program Overview

This document consolidates information regarding the Long-Term Care Prospective Payment System (LTCH PPS) pricing modules, derived from multiple functional specifications. It details the core programs involved in processing LTCH claims, their business functions, and the data structures they interact with.

### Core Pricing Driver and Subroutines

The central flow of the LTCH PPS pricing calculation is orchestrated by a series of programs, starting with a driver program that initiates the process and calling subsequent subroutines and modules responsible for specific calculation steps.

**1. LTMGR212: LTCH PPS Pricer Driver**

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from an input file (`BILLFILE`), invokes the `LTOPN212` subroutine to execute pricing calculations, and then writes the results to a printer output file (`PRTOPER`). The program's extensive change log indicates numerous revisions, reflecting ongoing updates to pricing methodologies and data structures.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file input/output operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information, including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, such as option switch and PPDRV version.

**2. LTOPN212: LTCH PPS Pricer Subroutine**

*   **Overview:** This subroutine is a crucial component of the LTCH PPS pricer. Its main responsibility is to load necessary tables, including provider, MSA, CBSA, and IPPS CBSA wage index tables, and then delegate the actual pricing calculations to the `LTDRV212` module. It serves as an intermediary, managing data flow and table loading before transferring control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill's discharge date.
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

**3. LTDRV212: LTCH PPS Pricing Calculation Logic**

*   **Overview:** This module is the core engine for LTCH PPS payment calculations. It retrieves the correct wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module, selected based on the bill's fiscal year, to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

*   **Important Note on LTDRV212:** The complexity of `LTDRV212` arises from its responsibility to manage calls to numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While the data structures passed remain largely consistent, minor variations may exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is critical for selecting the correct `LTCAL` module and managing transitions between different rate years and data structures.

**4. RUFL200: Rural Floor Factor Table Copybook**

*   **Overview:** This is not an executable program but a copybook that defines the Rural Floor Factor Table. It is utilized by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020.
*   **Business Functions:** Provides data necessary for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None directly; it is a data definition included in other programs.

### Year-Specific LTCH Payment Calculation Modules (`LTCALxxxx`)

These programs are responsible for calculating Medicare payments for LTCH claims based on specific fiscal year IPPS rules. They rely on various data tables for DRG and wage index information.

**General Information for `LTCALxxxx` Programs:**

*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:** These programs likely call other programs to read claim data (e.g., `LTDRV...`) and provider-specific data (e.g., `LTWIX...`).
*   **Data Structures Passed:** They typically pass and receive data structures such as `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD`. They also utilize internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER` in some versions.

**Specific `LTCALxxxx` Programs:**

*   **LTCAL162:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
*   **LTCAL170:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170` and `IPDRG170` tables. Includes handling of budget neutrality adjustments for site-neutral payments.
*   **LTCAL183:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables. Notes significant changes in short-stay outlier and Subclause II handling.
*   **LTCAL190:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and `LTDRG190` and `IPDRG190` tables.
*   **LTCAL202:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
*   **LTCAL212:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments (e.g., a 5% cap on wage index decreases from the prior year).

### Year-Specific Inpatient DRG Data Tables (`IPDRGxxxx`)

These programs define tables containing data related to Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for various years. They serve as data repositories for DRG information used by the `LTCALxxxx` programs.

**General Information for `IPDRGxxxx` Programs:**

*   **Overview:** These programs define tables containing IPPS DRG data for specific years. The data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for specific years.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables and do not call other programs. They are *called* by other programs (like `LTCALxxxx`) to retrieve DRG information.
*   **Data Structures:** The data structure passed *to* them would typically be a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, containing the DRG code, weight, ALOS, and description.

**Specific `IPDRGxxxx` Programs:**

*   **IPDRG160:** Defines the IPPS DRG table for 2015.
*   **IPDRG170:** Defines the IPPS DRG table for 2016.
*   **IPDRG181:** Defines the IPPS DRG table for 2017.
*   **IPDRG190:** Defines the IPPS DRG table for 2018.
*   **IPDRG200:** Defines the IPPS DRG table for 2019.
*   **IPDRG211:** Defines the IPPS DRG table for 2020.

### Year-Specific LTCH DRG Data Tables (`LTDRGxxxx`)

These programs define tables containing Long-Term Care Hospital (LTCH) DRG data for different years. They are also used by the `LTCALxxxx` programs.

**General Information for `LTDRGxxxx` Programs:**

*   **Overview:** These are data tables containing LTCH DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCALxxxx` programs.
*   **Data Structures:** The data structure passed *to* them would be a DRG code. The data structure passed *from* them is `WWM-ENTRY`, containing the DRG code, relative weight, and ALOS.

**Specific `LTDRGxxxx` Programs:**

*   **LTDRG160:** Defines LTCH DRG data for 2016.
*   **LTDRG170:** Defines LTCH DRG data for 2017.
*   **LTDRG181:** Defines LTCH DRG data for 2018.
*   **LTDRG190:** Defines LTCH DRG data for 2019.
*   **LTDRG200:** Defines LTCH DRG data for 2020.
*   **LTDRG210:** Defines LTCH DRG data for 2021.

**Important Note on Program Naming:** The ellipses ("...") in some program names suggest they are part of a larger naming convention. The precise details of data files and other programs called would require examination of the full application context. Additionally, `COPY` statements indicate the inclusion of external code modules, the contents of which are essential for a complete understanding of program functionality.