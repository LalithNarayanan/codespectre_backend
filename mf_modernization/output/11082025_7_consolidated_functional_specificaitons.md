## Program Overview

This document consolidates information from multiple functional specifications regarding the Long-Term Care Prospective Payment System (LTCH PPS) pricer modules. It outlines the overview, business functions, and called programs/data structures for each identified component.

---

### Core Driver and Pricing Modules

These programs form the main execution flow for LTCH PPS pricing calculations.

**1. Program: LTMGR212**

*   **Overview:** This program acts as a driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and directs the results to a printer file named `PRTOPER`. The program's extensive change log indicates numerous revisions, reflecting updates to pricing methodologies and data structures over time.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls a pricing subroutine (`LTOPN212`) to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Manages file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains bill information including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Contains pre-calculated PPS data such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

**2. Program: LTOPN212**

*   **Overview:** This subroutine is a critical component of the LTCH PPS pricer. Its primary function is to load necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then delegate the actual pricing calculations to the `LTDRV212` module. It serves as an intermediary, managing data flow and table loading before transferring control to the calculation module.
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

**3. Program: LTDRV212**

*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves the relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then invokes the appropriate `LTCALxxx` module (determined by the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes for error and exception management.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Numerous calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number, e.g., 032, 080, 111, 212). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially uses `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` arises from its management of numerous `LTCAL` module versions, each tailored for a specific fiscal year. While data structures passed are largely consistent, minor variations may exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the correct `LTCAL` module and managing transitions between different rate years and data structures.

---

### Year-Specific Calculation Modules and Data Tables

These programs and data tables are responsible for applying specific fiscal year rules and providing necessary data for calculations.

**1. Programs: LTCALxxxx (e.g., LTCAL162, LTCAL170, LTCAL183, LTCAL190, LTCAL202, LTCAL212)**

*   **Overview:** These COBOL programs are designed to calculate Medicare payments for LTCH claims based on the specific rules of a given fiscal year's Inpatient Prospective Payment System (IPPS). They rely on corresponding year-specific DRG tables.
*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
    *   Handles year-specific adjustments (e.g., budget neutrality, short-stay outlier changes, Subclause II removal, COVID-19 adjustments, supplemental wage index adjustments).
*   **Called Programs and Data Structures:**
    *   These programs likely call other programs to read claim data (e.g., `LTDRV...`) and provider-specific data (e.g., `LTWIX...`).
    *   They pass data structures such as `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, and `WAGE-NEW-IPPS-INDEX-RECORD` to themselves or related modules for processing.
    *   Specific examples of data structures passed to or used by these programs include:
        *   **LTCAL162:** Uses `LTDRG160` and `IPDRG160` tables.
        *   **LTCAL170:** Uses `LTDRG170` and `IPDRG170` tables, handles budget neutrality for site-neutral payments.
        *   **LTCAL183:** Uses `LTDRG181` and `IPDRG181` tables, incorporates changes to short-stay outlier and Subclause II handling.
        *   **LTCAL190:** Uses `LTDRG190` and `IPDRG190` tables, reflects 2019 IPPS rules.
        *   **LTCAL202:** Uses `LTDRG200` and `IPDRG200` tables, incorporates 2020 IPPS rules and COVID-19 related logic. Also uses internal functions `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.
        *   **LTCAL212:** Uses `LTDRG210` and `IPDRG211` tables, incorporates 2021 IPPS rules and logic for a 5% cap on wage index decreases.
*   **Important Note:** The ellipses ("...") in program names suggest these are part of larger program names, and the exact names of data files and other called programs would require consultation of the full application context. `COPY` statements indicate the inclusion of external code modules, which are vital for a complete understanding.

**2. Programs: IPDRGxxxx (e.g., IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG200, IPDRG211)**

*   **Overview:** These programs define data tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for specific years.
*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for a given year.
    *   Provides a lookup mechanism for DRG codes and associated information (weights, average lengths of stay (ALOS), descriptions).
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like the `LTCAL...` modules) to retrieve DRG information.
*   **Data Structures:**
    *   The data structure passed *to* these tables would typically be a DRG code (likely a 3-digit numeric or alphanumeric code).
    *   The data structure passed *from* these tables is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

**3. Programs: LTDRGxxxx (e.g., LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210)**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for various years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions Addressed:** These tables store LTCH DRG data for lookup purposes.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs.
*   **Data Structures:**
    *   The data structure passed *to* these tables would be a DRG code.
    *   The data structure passed *from* these tables is `WWM-ENTRY`, which contains the DRG code, relative weight, and ALOS.

---

### Data Definitions/Copybooks

**1. Program: RUFL200**

*   **Overview:** This copybook contains the Rural Floor Factor Table, specifically for Fiscal Year 2020. It is utilized by `LTDRV212` for IPPS calculations. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

---

This consolidated overview provides a structured understanding of the LTCH PPS pricing system, highlighting the interdependencies between the driver programs, year-specific calculators, and the data tables they utilize.