# Program Overview

This document consolidates and organizes information about a suite of COBOL programs involved in the Long-Term Care Hospital (LTCH) Prospective Payment System (PPS) pricer. The programs are analyzed for their overview, business functions, and called programs/data structures.

## Core Pricing and Driver Programs

### LTMGR212

*   **Overview:** This program acts as a driver for testing the Long-Term Care Prospective Payment System (PPS) pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine for pricing calculations, and writes results to the printer file `PRTOPER`. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
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
        *   **PPS-PAYMENT-DATA:** Contains calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Contains pricing option and version information, specifically the option switch and PPDRV version.

### LTOPN212

*   **Overview:** This subroutine is a fundamental part of the Long-Term Care PPS pricer. It is responsible for loading necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then invoking the `LTDRV212` module to execute the actual pricing calculations. It serves as an intermediary, managing data flow and table loading before delegating to the calculation module.
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

### LTDRV212

*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves the relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module (determined by the bill's fiscal year) to perform the final payment calculations. The program's extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Manages errors and exceptions through various return codes.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments as applicable.
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number such as 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.

## Year-Specific LTCAL Calculation Modules

These programs calculate Medicare payments for LTCH claims based on specific fiscal year IPPS rules and associated DRG tables.

### LTCAL162

*   **Overview:** This COBOL program calculates Medicare payment for Long-Term Care Hospital (LTCH) claims based on the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Called Programs and Data Structures:**
    *   This program likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   It passes `BILL-NEW-DATA` (containing claim details) to itself (implicitly for processing).
    *   It passes `PROV-NEW-HOLD` (provider information) to itself.
    *   It passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   It passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to `LTCAL162`. It passes data structures analogous to those in `LTCAL162`.

### LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. It incorporates significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous LTCAL programs, but with 2018 rules, including changes to short-stay outlier calculations and the removal of Subclause II processing.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, analogous to previous LTCAL programs.

### LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to previous LTCAL programs.

### LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. It includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous LTCAL programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Called Programs and Data Structures:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Tables (DRG and Rural Floor)

These are not executable programs in the traditional sense but are data definitions or tables that are utilized by other programs.

### IPPS DRG Data Tables

These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for various years. They provide a lookup mechanism for DRG codes and associated information.

*   **IPDRG160:** Defines the `PPS-DRG-TABLE` for IPPS DRGs for 2015.
*   **IPDRG170:** Defines the IPPS DRG table for 2016.
*   **IPDRG181:** Defines the IPPS DRG table for 2017.
*   **IPDRG190:** Defines the IPPS DRG table for 2018.
*   **IPDRG200:** Defines the IPPS DRG table for 2019.
*   **IPDRG211:** Defines the IPPS DRG table for 2020.

*   **Business Functions Addressed:**
    *   Stores IPPS DRG data for specific years.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them is a DRG code. The data structure passed *from* them is `DRG-DATA-TAB` (containing DRG code, weight, ALOS, and description).

### LTCH DRG Data Tables

These tables contain Long-Term Care Hospital (LTCH) DRG data for different years, including DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.

*   **LTDRG160:** Contains LTCH DRG data for 2016.
*   **LTDRG170:** Contains LTCH DRG data for 2017.
*   **LTDRG181:** Contains LTCH DRG data for 2018.
*   **LTDRG190:** Contains LTCH DRG data for 2019.
*   **LTDRG200:** Contains LTCH DRG data for 2020.
*   **LTDRG210:** Contains LTCH DRG data for 2021.

*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

### RUFL200

*   **Overview:** This copybook contains the Rural Floor Factor Table specifically for IPPS calculations in Fiscal Year 2020. It is a data definition included in other programs, not an executable program itself.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

## Important Notes:

*   The ellipses ("...") in program names like `LTCALxxxx` and `LTDRGxxxx` indicate that these are part of a series of programs that vary by year or version.
*   The complexity of `LTDRV212` is notably high due to its role in managing calls to numerous `LTCAL` modules, each tailored to specific fiscal years and policy changes.
*   While data structures are generally consistent across programs, minor variations may exist between different `LTCAL` versions, particularly for older fiscal years.
*   The use of `COPY` statements signifies the inclusion of external code modules, the contents of which are critical for a complete understanding of program functionality.
*   The exact names and functionalities of data files and other called programs would require examination of the full context of the application.