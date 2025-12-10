## Program Overview

This document consolidates and details the functionality of several COBOL programs involved in the Long-Term Care Hospital (LTCH) Prospective Payment System (PPS) pricer. The programs work together to process LTCH claims, calculate Medicare payments, and manage various data tables and pricing methodologies across different fiscal years.

---

### Core Pricing Driver and Subroutines

**Program: LTMGR212**

*   **Overview:** This program acts as the primary driver for testing the Long-Term Care PPS pricer modules. It reads bill records from `BILLFILE`, calls the `LTOPN212` subroutine to perform pricing calculations, and writes the results to the `PRTOPER` printer file. Its extensive change log indicates frequent updates to pricing methodologies and data structures.
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

**Program: LTOPN212**

*   **Overview:** This subroutine is a crucial component of the LTCH PPS pricer. It is responsible for loading essential tables, including provider, MSA, CBSA, and IPPS CBSA wage index tables, before calling the `LTDRV212` module for the actual pricing calculations. It manages data flow and table loading as an intermediary.
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

**Program: LTDRV212**

*   **Overview:** This module is the core of the LTCH PPS pricing calculation. It retrieves the appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (based on the bill's fiscal year) to perform the final payment calculations. Its extensive change log reflects its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   **BILL-NEW-DATA:** (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   **PPS-DATA-ALL:** (Same as in LTMGR212)
        *   **PPS-CBSA:** (Same as in LTMGR212)
        *   **PPS-PAYMENT-DATA:** (Same as in LTMGR212)
        *   **PRICER-OPT-VERS-SW:** (Same as in LTMGR212)
        *   **PROV-NEW-HOLD:** Contains the provider record.
        *   **WAGE-NEW-INDEX-RECORD-CBSA:** Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   **WAGE-IPPS-INDEX-RECORD-CBSA:** Contains the IPPS CBSA wage index data.
*   **Important Note:** The complexity of `LTDRV212` stems from its handling of numerous versions of the `LTCAL` modules, each designed for a specific fiscal year. The data structures passed remain largely consistent, though minor variations might exist across different `LTCAL` versions. The extensive conditional logic within `LTDRV212` is crucial for selecting the appropriate `LTCAL` module and managing transitions between different rate years and data structures.

**Copybook: RUFL200**

*   **Overview:** This copybook contains the Rural Floor Factor Table, specifically used by `LTDRV212` for IPPS calculations for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a data definition included by other programs.

---

### Fiscal Year Specific Payment Calculation Modules (`LTCAL` series)

These programs are responsible for calculating Medicare payments for LTCH claims based on specific fiscal year IPPS rules. They leverage various DRG and wage index tables.

**Program: LTCAL162**

*   **Overview:** Calculates the Medicare payment for LTCH claims based on the 2016 IPPS rules, utilizing the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Called Programs and Data Structures:**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (containing claim details) to itself (implicitly for processing).
    *   Passes `PROV-NEW-HOLD` (provider information) to itself.
    *   Passes `WAGE-NEW-INDEX-RECORD` (LTCH wage index data) to itself.
    *   Passes `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself.

**Program: LTCAL170**

*   **Overview:** Calculates Medicare payments for LTCH claims using the 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to `LTCAL162`, passing analogous data structures.

**Program: LTCAL183**

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. Features significant changes in short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, analogous to previous `LTCAL` programs.

**Program: LTCAL190**

*   **Overview:** Calculates Medicare payments for LTCH claims according to the 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data, similar to previous `LTCAL` programs.

**Program: LTCAL202**

*   **Overview:** Calculates Medicare payments for LTCH claims based on the 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, but incorporates 2020 IPPS rules and adds logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Called Programs and Data Structures:** Likely calls programs to read claim and provider data. The program also uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

**Program: LTCAL212**

*   **Overview:** Calculates Medicare payments for LTCH claims under the 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, but incorporates 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Called Programs and Data Structures:** Likely calls programs for claim and provider data input. It uses internal functions, similar to `LTCAL202`.

---

### Data Tables for Diagnosis Related Groups (DRG)

These programs define data tables containing Diagnosis Related Group (DRG) information for various years, used by the `LTCAL` series programs for payment calculations. They are not executable programs in the traditional sense but are called by other programs.

**Program: IPDRG160**

*   **Overview:** Defines a table (`PPS-DRG-TABLE`) containing data for Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs) for the year 2015. Data includes DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2015.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs (like `LTCAL162`) to retrieve DRG information.
    *   The data structure passed *to* it would be a DRG code (likely a 3-digit numeric or alphanumeric code).
    *   The data structure passed *from* it is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

**Program: IPDRG170**

*   **Overview:** Defines an IPPS DRG table for the year 2016, similar to `IPDRG160`.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2016.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2016 DRG information.
    *   The data structure passed *to* it would be a DRG code.
    *   The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**Program: IPDRG181**

*   **Overview:** Defines an IPPS DRG table for the year 2017.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2017.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2017 DRG information.
    *   The data structure passed *to* it would be a DRG code.
    *   The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**Program: IPDRG190**

*   **Overview:** Defines an IPPS DRG table for the year 2018.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2018.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2018 DRG information.
    *   The data structure passed *to* it would be a DRG code.
    *   The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**Program: IPDRG200**

*   **Overview:** Defines an IPPS DRG table for the year 2019.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2019.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2019 DRG information.
    *   The data structure passed *to* it would be a DRG code.
    *   The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**Program: IPDRG211**

*   **Overview:** Defines an IPPS DRG table for the year 2020.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2020.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Called Programs and Data Structures:**
    *   This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2020 DRG information.
    *   The data structure passed *to* it would be a DRG code.
    *   The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

**Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing Long-Term Care Hospital (LTCH) DRG data for different years (2016, 2017, 2018, 2019, 2020 respectively). The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions:** These tables store LTCH DRG data for lookups.
*   **Called Programs and Data Structures:**
    *   These are data tables; they don't call other programs. They are called by the `LTCAL...` programs.
    *   The data structure passed *to* them would be a DRG code.
    *   The data structure passed *from* them is `WWM-ENTRY`, containing the DRG code, relative weight, and ALOS.

---

**General Notes:**

*   The ellipses ("...") in some program names suggest they are part of a naming convention for programs specific to certain versions or fiscal years.
*   The mention of `COPY` statements indicates the use of external code modules, the contents of which are crucial for a complete understanding of the system.
*   The consistency in data structures passed between programs (`BILL-NEW-DATA`, `PPS-DATA-ALL`, etc.) highlights a standardized interface for claim processing, despite variations in fiscal year logic.