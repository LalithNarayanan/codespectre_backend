# Program Overview

This document consolidates information from multiple functional specification files to provide a comprehensive overview of the Long-Term Care Prospective Payment System (LTCH PPS) pricing modules and related data components.

---

## Core Pricing and Driver Programs

The following programs form the core of the LTCH PPS pricing engine, orchestrating data flow and calculations.

### LTMGR212

*   **Overview:** This program acts as a driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to a printer file (`PRTOPER`). Its extensive change log indicates numerous revisions to pricing methodologies and data structures over time.
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
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, including option switch and PPDRV version.

### LTOPN212

*   **Overview:** This subroutine is a key component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module to perform the actual pricing calculations. It serves as an intermediary, managing data flow and table loading before delegating to the calculation module.
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
        *   **PROV-RECORD-FROM-USER:** (Same as in LTMGR212)
        *   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table.
        *   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table.
        *   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table.
        *   **WORK-COUNTERS:** Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

### LTDRV212

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (depending on the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.) are made. Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
    *   **Important Note:** The complexity of `LTDRV212` stems from its handling of numerous versions of the `LTCAL` modules, each designed for a specific fiscal year. The data structures passed remain largely consistent, though some minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing the transition between different rate years and data structures.

---

## Fiscal Year Specific Calculation Modules (`LTCALxxx`) and Data Tables

These programs and associated data tables provide the specific logic and data required for calculating LTCH PPS payments for different fiscal years.

### LTCAL Calculation Programs (Fiscal Year Specific)

These programs are called by `LTDRV212` to perform the actual payment calculations based on the fiscal year of the bill. The ellipses ("...") in the program names suggest that these are parts of larger program names, and the exact names and functionalities of the data files and other programs called would need to be determined from the full context of the application.

*   **LTCAL162:** Calculates Medicare payment for LTCH claims based on 2016 IPPS rules, using `LTDRG160` and `IPDRG160` tables.
    *   **Business Functions:** Reads LTCH claim data, validates claim data, calculates LTCH payments (standard, short-stay outlier, site-neutral, blended), calculates high-cost outliers, determines appropriate return codes, and writes results to output data structures.
    *   **Other Programs Called:** Likely calls programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   **Data Structures Passed:** `BILL-NEW-DATA`, `PROV-NEW-HOLD`, `WAGE-NEW-INDEX-RECORD`, `WAGE-NEW-IPPS-INDEX-RECORD`.

*   **LTCAL170:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and `LTDRG170` and `IPDRG170` tables.
    *   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to `LTCAL162`.
    *   **Data Structures Passed:** Analogous to those in `LTCAL162`.

*   **LTCAL183:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using `LTDRG181` and `IPDRG181` tables.
    *   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

*   **LTCAL190:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and `LTDRG190` and `IPDRG190` tables.
    *   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
    *   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

*   **LTCAL202:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and `LTDRG200` and `IPDRG200` tables.
    *   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
    *   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

*   **LTCAL212:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables.
    *   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
    *   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

### DRG Data Tables (Fiscal Year Specific)

These programs define data tables containing Diagnosis Related Group (DRG) information for specific fiscal years. They do not call other programs but are called by the `LTCALxxx` programs to retrieve DRG-specific data.

*   **IPDRG160:** Defines an IPPS DRG table for the year 2015.
    *   **Business Functions:** Stores IPPS DRG data for 2015, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB` (contains DRG code, weight, ALOS, and description).

*   **IPDRG170:** Defines an IPPS DRG table for the year 2016.
    *   **Business Functions:** Stores IPPS DRG data for 2016, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.

*   **IPDRG181:** Defines an IPPS DRG table for the year 2017.
    *   **Business Functions:** Stores IPPS DRG data for 2017, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.

*   **IPDRG190:** Defines an IPPS DRG table for the year 2018.
    *   **Business Functions:** Stores IPPS DRG data for 2018, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.

*   **IPDRG200:** Defines an IPPS DRG table for the year 2019.
    *   **Business Functions:** Stores IPPS DRG data for 2019, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.

*   **IPDRG211:** Defines an IPPS DRG table for the year 2020.
    *   **Business Functions:** Stores IPPS DRG data for 2020, provides a lookup mechanism for DRG codes and associated information.
    *   **Data Structure Passed From:** `DRG-DATA-TAB`.

*   **LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years.
    *   **Business Functions:** Store LTCH DRG data for lookups, including DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
    *   **Data Structure Passed From:** `WWM-ENTRY` (contains DRG code, relative weight, and ALOS).
    *   **Important Note:** The `COPY` statements indicate the inclusion of external code modules; the contents of these copied modules are crucial for a complete understanding.

---

## Supporting Data Structures and Components

These items are either data definitions or specific data structures used within the LTCH PPS pricing process.

### RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table, specifically for Fiscal Year 2020, used by `LTDRV212` for IPPS calculations. It is not an executable program but a data definition included in other programs.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

---

## General Data Structures Used Across Programs

The following data structures are frequently passed between the core pricing programs (`LTMGR212`, `LTOPN212`, `LTDRV212`) and the fiscal year-specific `LTCALxxx` modules, indicating a consistent data model for claim processing.

*   **BILL-NEW-DATA:** Contains detailed information about a patient's bill or claim, including:
    *   NPI (National Provider Identifier)
    *   Provider Number
    *   Patient Status
    *   DRG Code
    *   Length of Stay (LOS)
    *   Covered Days
    *   Cost Report Days
    *   Discharge Date
    *   Covered Charges
    *   Special Pay Indicator
    *   Review Code
    *   Diagnosis Codes
    *   Procedure Codes
    *   LTCH DPP Indicator
    *   *(Note: Older fiscal years might use variations like `BILL-DATA-FY03-FY15`)*

*   **PPS-DATA-ALL:** Holds comprehensive pre-calculated Prospective Payment System data:
    *   RTC (Reason for Transfer to/from LTCH)
    *   Charge Threshold
    *   MSA (Metropolitan Statistical Area)
    *   Wage Index
    *   Average LOS
    *   Relative Weight
    *   Outlier Payment Amount
    *   LOS (Length of Stay)
    *   DRG Adjusted Payment Amount
    *   Federal Payment Amount
    *   Final Payment Amount
    *   Facility Costs
    *   New Facility-Specific Rate
    *   Outlier Threshold
    *   Submitted DRG Code
    *   Calculation Version Code
    *   Regular Days Used
    *   LTR Days Used (Long-Term Readmission days)
    *   Blend Year
    *   COLA (Cost of Living Adjustment)

*   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code, used for wage index adjustments.

*   **PPS-PAYMENT-DATA:** Stores the results of payment calculations:
    *   Site-Neutral Cost Payment
    *   Site-Neutral IPPS Payment
    *   Standard Full Payment
    *   Standard Short-Stay Outlier Payment

*   **PRICER-OPT-VERS-SW:** Contains configuration and versioning information for the pricer:
    *   Option Switch
    *   PPDRV Version

*   **PROV-RECORD-FROM-USER / PROV-NEW-HOLD:** Contains provider-specific information.

*   **CBSAX-TABLE-FROM-USER:** Contains the CBSA wage index table data.

*   **IPPS-CBSAX-TABLE-FROM-USER:** Contains the IPPS CBSA wage index table data.

*   **MSAX-TABLE-FROM-USER:** Contains the MSA wage index table data.

*   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains CBSA wage index data including CBSA, effective date, and wage index values.

*   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains IPPS CBSA wage index data.

*   **WORK-COUNTERS:** Used to store record counts for various tables (e.g., CBSA, MSA, provider, IPPS CBSA).