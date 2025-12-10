# Program Overview

This document consolidates information from multiple functional specifications to provide a comprehensive overview of the COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) pricer.

## Core Processing Programs

These programs form the backbone of the LTCH PPS pricing calculation, handling the workflow from input to final payment determination.

### LTMGR212

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care PPS pricer modules. It orchestrates the process by reading bill records from the `BILLFILE`, invoking the `LTOPN212` subroutine for pricing calculations, and then outputting the results to the `PRTOPER` printer file. Its extensive change log indicates a history of revisions to accommodate evolving pricing methodologies and data structures.

*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file (`BILLFILE`).
    *   Initiates pricing calculations by calling the `LTOPN212` subroutine.
    *   Generates a prospective payment test data report.
    *   Manages all file input/output operations (opening, reading, writing, and closing).

*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   **BILL-NEW-DATA:** Contains essential bill information, including NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, and the LTCH DPP indicator.
        *   **PPS-DATA-ALL:** Holds pre-calculated Prospective Payment System (PPS) data, such as RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, and COLA.
        *   **PPS-CBSA:** Contains the Core Based Statistical Area (CBSA) code.
        *   **PPS-PAYMENT-DATA:** Stores calculated payment data, including site-neutral cost payment, site-neutral IPPS payment, standard full payment, and standard short-stay outlier payment.
        *   **PRICER-OPT-VERS-SW:** Carries pricing option and version information, such as the option switch and PPDRV version.

### LTOPN212

*   **Overview:** This subroutine functions as a crucial intermediary within the LTCH PPS pricer. Its primary role is to load necessary data tables—specifically, provider, MSA, CBSA, and IPPS CBSA wage index tables—before delegating the actual pricing calculations to the `LTDRV212` module. It manages data flow and table loading, acting as a gateway to the core calculation engine.

*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill's discharge date.
    *   Calls the main pricing calculation module, `LTDRV212`.
    *   Returns status codes indicating the success or failure of the pricing process.

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
        *   **WORK-COUNTERS:** Holds record counts for CBSA, MSA, provider, and IPPS CBSA.

### LTDRV212

*   **Overview:** This module is the core engine for performing LTCH PPS payment calculations. It retrieves the relevant wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the appropriate `LTCALxxx` module, selected based on the bill's fiscal year, to finalize the payment calculations. The program's extensive change log highlights its continuous evolution to support various rate years and policy changes.

*   **Business Functions:**
    *   Retrieves wage index records from loaded tables, using the bill's discharge date and provider information.
    *   Determines the specific `LTCALxxx` module to execute based on the bill's fiscal year.
    *   Calls the selected `LTCALxxx` module to perform the payment calculations.
    *   Manages various return codes to handle errors and exceptions.
    *   Executes rural floor wage index calculations.
    *   Applies supplemental wage index adjustments, where applicable.

*   **Called Programs and Data Structures:**
    *   **Numerous calls to programs of the form `LTCALxxxx`** (where `xxxx` represents a fiscal year version, e.g., 032, 080, 111, 212). Each call utilizes the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, with potential use of `BILL-DATA-FY03-FY15` for older fiscal years).
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains CBSA wage index data, including CBSA, effective date, and wage index values.
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains IPPS CBSA wage index data.

    *   **Important Note:** The complexity of `LTDRV212` is significantly attributed to its handling of numerous `LTCAL` modules, each tailored to a specific fiscal year. While the core data structures passed remain largely consistent, minor variations may exist across different `LTCAL` versions. The program's extensive conditional logic is critical for selecting the correct `LTCAL` module and managing transitions between different rate years and data structures.

## Fiscal Year Specific Calculation Modules (LTCALxxx)

These programs perform the actual payment calculations based on the specific IPPS rules for a given fiscal year. They rely on various data tables for DRG and wage index information.

### LTCAL162

*   **Overview:** This COBOL program calculates the Medicare payment for Long-Term Care Hospital (LTCH) claims according to the 2016 IPPS rules. It utilizes the `LTDRG160` and `IPDRG160` tables for its calculations.

*   **Business Functions Addressed:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments, including standard, short-stay outlier, site-neutral, and blended amounts.
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes for processing outcomes.
    *   Writes results to output data structures.

*   **Other Programs Called:**
    *   Likely calls other programs for reading claim data (e.g., `LTDRV...`) and provider-specific data (e.g., `LTWIX...`).
    *   Passes `BILL-NEW-DATA` (containing claim details) to itself for processing.
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

### LTCAL170

*   **Overview:** This program calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.

*   **Business Functions Addressed:** Similar to `LTCAL162`, but incorporates updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to `LTCAL162`. It passes data structures similar to those used in `LTCAL162`.

### LTCAL183

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2018 IPPS rules, utilizing the `LTDRG181` and `IPDRG181` tables. Notably, it incorporates significant changes in short-stay outlier and Subclause II handling.

*   **Business Functions Addressed:** Similar to previous LTCAL programs, but adapted for 2018 rules, including modifications to short-stay outlier calculations and the removal of Subclause II processing.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, analogous to previous LTCAL programs.

### LTCAL190

*   **Overview:** This program calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and uses the `LTDRG190` and `IPDRG190` tables.

*   **Business Functions Addressed:** Similar to previous versions, reflecting the specific 2019 IPPS rules.

*   **Other Programs Called:** Likely calls programs to read claim and provider data, similar to previous LTCAL programs.

### LTCAL202

*   **Overview:** This program calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. It includes special logic related to COVID-19 adjustments.

*   **Business Functions Addressed:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments. This includes re-routing site-neutral claims to standard payment under specific conditions.

*   **Other Programs Called:** Likely calls programs to read claim and provider data. The program also utilizes internal functions such as `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

### LTCAL212

*   **Overview:** This program calculates Medicare payments for LTCH claims under the 2021 IPPS rules, using the `LTDRG210` and `IPDRG211` tables. It incorporates new logic for supplemental wage index adjustments.

*   **Business Functions Addressed:** Similar to previous LTCAL programs, but incorporates 2021 IPPS rules. This includes logic to apply a 5% cap to wage index decreases from the prior year, utilizing supplemental wage index data from the provider-specific file.

*   **Other Programs Called:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

## Data Table Programs

These programs define and store data tables that are essential for the LTCH PPS calculations, particularly for Diagnosis Related Groups (DRGs) and wage index information across different fiscal years. These are not executable programs in the traditional sense but are data structures accessed by other programs.

### IPPS DRG Data Tables

These programs define tables containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRG) data for various years. They provide a lookup mechanism for DRG codes and associated information.

*   **IPDRG160:** Defines the `PPS-DRG-TABLE` for IPPS DRGs for the year 2015. Contains DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **IPDRG170:** Defines an IPPS DRG table for the year 2016. Contains DRG codes, weights, ALOS, and descriptions.
*   **IPDRG181:** Defines an IPPS DRG table for the year 2017. Contains DRG codes, weights, ALOS, and descriptions.
*   **IPDRG190:** Defines an IPPS DRG table for the year 2018. Contains DRG codes, weights, ALOS, and descriptions.
*   **IPDRG200:** Defines an IPPS DRG table for the year 2019. Contains DRG codes, weights, ALOS, and descriptions.
*   **IPDRG211:** Defines an IPPS DRG table for the year 2020. Contains DRG codes, weights, ALOS, and descriptions.

*   **Business Functions Addressed:**
    *   Store IPPS DRG data for specific years.
    *   Provide a lookup mechanism for DRG codes and associated information.

*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by other programs (like `LTCALxxx` modules) to retrieve DRG information. The data structure passed *to* them is typically a DRG code. The data structure passed *from* them is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

### LTCH DRG Data Tables

These programs define tables containing Long-Term Care Hospital (LTCH) DRG data for different years.

*   **LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210:** These are all data tables containing LTCH DRG data for their respective years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.

*   **Business Functions Addressed:** These tables store LTCH DRG data for lookups.

*   **Other Programs Called:** These are data tables; they do not call other programs. They are *called* by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY`, containing the DRG code, relative weight, and ALOS.

## Supporting Data Definitions

### RUFL200

*   **Overview:** This is a copybook that contains the Rural Floor Factor Table. It is used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is not an executable program but a data definition included in other programs.

*   **Business Functions:** Provides data necessary for determining rural floor wage indices.

*   **Called Programs and Data Structures:** None; it is a copybook.

## General Notes

*   The ellipses ("...") in program names suggest these are parts of larger, potentially versioned, program names. The exact and complete names and functionalities of associated data files and other called programs would require access to the full context of the application.
*   The use of `COPY` statements indicates the inclusion of external code modules. The content of these copied modules is crucial for a complete understanding of the system's functionality.