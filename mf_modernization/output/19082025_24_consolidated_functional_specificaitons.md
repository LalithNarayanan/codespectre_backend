## Program Overview

This document consolidates the program overview information extracted from multiple functional specification files, providing a comprehensive understanding of the COBOL programs involved in the Long-Term Care Prospective Payment System (LTCH PPS) processing.

The programs can be broadly categorized into two main types:
1.  **Driver/Processing Programs:** These programs are responsible for orchestrating the payment calculation process, reading input data, calling subroutines, and generating output. Examples include `LTMGR212`, `LTOPN212`, and `LTDRV212`.
2.  **Data Table Definitions:** These programs define and store various lookup tables, such as Diagnosis Related Group (DRG) data, wage index information, and state-specific factors, which are utilized by the processing programs. Examples include `IPDRGxxx`, `LTDRGxxx`, and `IRFBNxxx`.

### 1. Driver and Processing Programs

These programs are the engines of the LTCH PPS calculation.

#### **Program: LTMGR212**

*   **Overview:** This program acts as a driver for testing the LTCH PPS pricer modules. It reads bill records from `BILLFILE`, invokes the `LTOPN212` subroutine for pricing calculations, and writes results to the `PRTOPER` printer file. Its extensive change log reflects numerous updates to pricing methodologies and data structures over time.
*   **Business Functions:**
    *   Reads long-term care hospital bill data from an input file.
    *   Calls the `LTOPN212` subroutine to calculate payments based on various pricing options.
    *   Generates a prospective payment test data report.
    *   Handles file I/O operations (opening, reading, writing, and closing files).
*   **Called Programs and Data Structures:**
    *   **LTOPN212:**
        *   `BILL-NEW-DATA`: Contains bill information (NPI, provider number, patient status, DRG code, length of stay, covered days, cost report days, discharge date, covered charges, special pay indicator, review code, diagnosis codes, procedure codes, LTCH DPP indicator).
        *   `PPS-DATA-ALL`: Contains pre-calculated PPS data (RTC, charge threshold, MSA, wage index, average LOS, relative weight, outlier payment amount, LOS, DRG adjusted payment amount, federal payment amount, final payment amount, facility costs, new facility-specific rate, outlier threshold, submitted DRG code, calculation version code, regular days used, LTR days used, blend year, COLA).
        *   `PPS-CBSA`: Contains the Core Based Statistical Area code.
        *   `PPS-PAYMENT-DATA`: Contains calculated payment data (site-neutral cost payment, site-neutral IPPS payment, standard full payment, standard short-stay outlier payment).
        *   `PRICER-OPT-VERS-SW`: Contains pricing option and version information (option switch, PPDRV version).

#### **Program: LTOPN212**

*   **Overview:** This subroutine is a key component of the LTCH PPS pricer. It loads necessary tables (provider, MSA, CBSA, and IPPS CBSA wage index tables) and then calls the `LTDRV212` module to perform the actual pricing calculations. It manages data flow and table loading before passing control to the calculation module.
*   **Business Functions:**
    *   Loads provider-specific data.
    *   Loads MSA, CBSA, and IPPS CBSA wage index tables.
    *   Determines the appropriate wage index table to use based on the bill discharge date.
    *   Calls the main pricing calculation module (`LTDRV212`).
    *   Returns return codes indicating the success or failure of the pricing process.
*   **Called Programs and Data Structures:**
    *   **LTDRV212:**
        *   `BILL-NEW-DATA`: (Same as in LTMGR212)
        *   `PPS-DATA-ALL`: (Same as in LTMGR212)
        *   `PPS-CBSA`: (Same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212)
        *   `PROV-RECORD-FROM-USER`: (Same as in LTMGR212)
        *   `CBSAX-TABLE-FROM-USER`: Contains the CBSA wage index table.
        *   `IPPS-CBSAX-TABLE-FROM-USER`: Contains the IPPS CBSA wage index table.
        *   `MSAX-TABLE-FROM-USER`: Contains the MSA wage index table.
        *   `WORK-COUNTERS`: Contains record counts for CBSA, MSA, provider, and IPPS CBSA.

#### **Program: LTDRV212**

*   **Overview:** This module is central to the LTCH PPS pricing calculation. It retrieves appropriate wage index records (MSA or CBSA, and potentially IPPS CBSA) based on the bill's discharge date and provider information. It then calls the relevant `LTCALxxx` module (based on the bill's fiscal year) for final payment calculations. Its extensive change log highlights its evolution to accommodate various rate years and policy changes.
*   **Business Functions:**
    *   Retrieves wage index records from tables based on the bill's discharge date.
    *   Determines the appropriate `LTCALxxx` module to call based on the fiscal year of the bill.
    *   Calls the selected `LTCALxxx` module to calculate payments.
    *   Handles various return codes to manage errors and exceptions.
    *   Performs rural floor wage index calculations.
    *   Applies supplemental wage index adjustments (as applicable).
*   **Called Programs and Data Structures:**
    *   Many calls are made to programs of the form `LTCALxxxx` (where `xxxx` represents a version number like 032, 080, 111, 212, etc.). Each call uses the following data structures:
        *   `BILL-NEW-DATA`: (Same as in LTMGR212, but potentially using `BILL-DATA-FY03-FY15` for older fiscal years.)
        *   `PPS-DATA-ALL`: (Same as in LTMGR212)
        *   `PPS-CBSA`: (Same as in LTMGR212)
        *   `PPS-PAYMENT-DATA`: (Same as in LTMGR212)
        *   `PRICER-OPT-VERS-SW`: (Same as in LTMGR212)
        *   `PROV-NEW-HOLD`: Contains the provider record.
        *   `WAGE-NEW-INDEX-RECORD-CBSA`: Contains the CBSA wage index data (CBSA, effective date, wage index values).
        *   `WAGE-IPPS-INDEX-RECORD-CBSA`: Contains the IPPS CBSA wage index data.
*   **Note:** The complexity of `LTDRV212` arises from its handling of numerous versions of the `LTCAL` modules, each tailored for a specific fiscal year. While data structures passed are largely consistent, minor variations may exist across different `LTCAL` versions. The extensive conditional logic is crucial for selecting the correct `LTCAL` module and managing rate year transitions.

#### **Program: RUFL200**

*   **Overview:** This is a copybook containing the Rural Floor Factor Table used by `LTDRV212` for IPPS calculations, specifically for Fiscal Year 2020. It is a data definition, not an executable program.
*   **Business Functions:** Provides data for determining rural floor wage indices.
*   **Called Programs and Data Structures:** None; it's a copybook.

#### **Program: LTCAL162**

*   **Overview:** This COBOL program calculates Medicare payments for LTCH claims based on 2016 IPPS rules, utilizing the `LTDRG160` and `IPDRG160` tables.
*   **Business Functions:**
    *   Reads LTCH claim data.
    *   Validates claim data.
    *   Calculates LTCH payments (standard, short-stay outlier, site-neutral, blended).
    *   Calculates high-cost outliers.
    *   Determines appropriate return codes.
    *   Writes results to output data structures.
*   **Other Programs Called:**
    *   Likely calls other programs to read claim data (`LTDRV...`) and provider-specific data (`LTWIX...`).
    *   Passes `BILL-NEW-DATA` (claim details), `PROV-NEW-HOLD` (provider information), `WAGE-NEW-INDEX-RECORD` (LTCH wage index data), and `WAGE-NEW-IPPS-INDEX-RECORD` (IPPS wage index data) to itself (implicitly for processing).

#### **Program: LTCAL170**

*   **Overview:** Calculates Medicare payments for LTCH claims using 2017 IPPS rules and the `LTDRG170` and `IPDRG170` tables.
*   **Business Functions:** Similar to `LTCAL162`, but with updated rules for 2017, including handling of budget neutrality adjustments for site-neutral payments.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, passing analogous data structures to `LTCAL162`.

#### **Program: LTCAL183**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2018 IPPS rules, using the `LTDRG181` and `IPDRG181` tables. Notable changes include short-stay outlier and Subclause II handling.
*   **Business Functions:** Similar to previous `LTCAL` programs, but with 2018 rules, including changes to short-stay outlier calculations and removal of Subclause II processing.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, analogous to previous `LTCAL` programs.

#### **Program: LTCAL190**

*   **Overview:** Calculates Medicare payments for LTCH claims according to 2019 IPPS rules and the `LTDRG190` and `IPDRG190` tables.
*   **Business Functions:** Similar to previous versions, reflecting the 2019 IPPS rules.
*   **Other Programs Called:** Likely calls programs for claim and provider data input, similar to previous `LTCAL` programs.

#### **Program: LTCAL202**

*   **Overview:** Calculates Medicare payments for LTCH claims based on 2020 IPPS rules and the `LTDRG200` and `IPDRG200` tables. Includes special COVID-19 related logic.
*   **Business Functions:** Similar to previous versions, incorporating 2020 IPPS rules and adding logic to handle COVID-19 adjustments to claim payments (re-routing site-neutral claims to standard payment under certain conditions).
*   **Other Programs Called:** Likely calls programs for claim and provider data input. Uses internal functions like `FUNCTION INTEGER-OF-DATE` and `FUNCTION DATE-OF-INTEGER`.

#### **Program: LTCAL212**

*   **Overview:** Calculates Medicare payments for LTCH claims under 2021 IPPS rules and the `LTDRG210` and `IPDRG211` tables. Includes new logic for supplemental wage index adjustments.
*   **Business Functions:** Similar to previous `LTCAL` programs, incorporating 2021 IPPS rules and logic to apply a 5% cap to wage index decreases from the prior year, using supplemental wage index data from the provider-specific file.
*   **Other Programs Called:** Likely calls programs for claim and provider data input. Uses internal functions, similar to `LTCAL202`.

#### **Program: LTCAL032**

*   **Overview:** Calculates Prospective Payment System (PPS) payments for long-term care (LTC) claims based on Length of Stay (LOS). It uses various input parameters from claim and provider records to determine payment, considering DRG code, covered days, and outlier thresholds. The program handles different payment scenarios, including short-stay and outlier payments, and incorporates blend year calculations. Version C03.2 indicates a specific release.
*   **Business Functions:**
    *   LTC Claim Processing: Processes individual LTC claims to determine payment amounts.
    *   PPS Calculation: Core function is calculating PPS payments according to specified rules and parameters.
    *   Short-Stay Payment Calculation: Calculates payments for short hospital stays.
    *   Outlier Payment Calculation: Determines and calculates outlier payments based on facility costs exceeding thresholds.
    *   Blend Year Calculation: Adjusts payments based on blend year parameters (percentage of facility rate versus DRG payment).
    *   Data Validation and Error Handling: Performs data edits and assigns return codes indicating success or specific error conditions.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Included via a COPY statement. Data structures defined in `LTDRG031` (specifically `WWM-ENTRY`, containing `WWM-DRG`, `WWM-RELWT`, and `WWM-ALOS`) are used directly within `LTCAL032` for DRG lookups. Data is accessed implicitly through the copy.

#### **Program: LTCAL042**

*   **Overview:** Similar to `LTCAL032`, this program calculates PPS payments for LTC claims. It's a later version (C04.2) and likely incorporates updates to payment methodologies, rules, or data structures. It includes special handling for provider '332006'.
*   **Business Functions:**
    *   LTC Claim Processing: Processes individual LTC claims to determine payment amounts.
    *   PPS Calculation: Core function is calculating PPS payments.
    *   Short-Stay Payment Calculation: Calculates payments for short stays, with special logic for provider '332006'.
    *   Outlier Payment Calculation: Determines and calculates outlier payments.
    *   Blend Year Calculation: Adjusts payments according to blend year parameters.
    *   Data Validation and Error Handling: Edits data and assigns return codes.
    *   Special Provider Handling: Contains specific logic for provider '332006', adjusting short-stay calculations based on discharge date.
*   **Called Programs & Data Structures:**
    *   **LTDRG031:** Copied into `LTCAL042`. Data structures within `LTDRG031` (`WWM-ENTRY`, `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`) are used for DRG code lookups.

#### **Program: LTCAL103**

*   **Overview:** A COBOL subroutine (or full program) that calculates PPS payments for LTCH claims. It uses data tables defined in copied programs.
*   **Business Functions:**
    *   LTCH PPS Payment Calculation: Core function is calculating payment amounts based on length of stay, DRG, facility costs, wage indices, and other factors.
    *   Data Validation: Performs edits and validations on input bill data.
    *   Outlier Payment Calculation: Calculates outlier payments if applicable.
    *   Blended Payment Calculation: Handles blended payments based on blend years and percentages.
*   **Other Programs Called:** Calls no other programs directly but uses data from:
    *   `LTDRG100`: LTCH DRG table (`WWM-ENTRY` with `WWM-DRG`, `WWM-RELWT`, `WWM-ALOS`).
    *   `IPDRG104`: IPPS DRG table (`DRGX-TAB` with `DRGX-EFF-DATE`, `DRG-WT`, `DRG-ALOS`, `DRG-DAYS-TRIM`, `DRG-ARITH-ALOS`).
    *   `IRFBN102`: IPPS State-Specific Rural Floor Budget Neutrality Factors (`SSRFBN-TAB` with `WK-SSRFBN-STATE`, `WK-SSRFBN-RATE`, `WK-SSRFBN-CODE2`, `WK-SSRFBN-STNAM`, `WK-SSRFBN-REST`).
    *   Uses data from `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures passed as parameters.

#### **Program: LTCAL105**

*   **Overview:** A revised version of `LTCAL103`, likely reflecting updates to payment rates and calculation logic. The structure is very similar to `LTCAL103`.
*   **Business Functions:** Similar to `LTCAL103` but with updated constants and potentially updated logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG100`: LTCH DRG table.
    *   `IPDRG104`: IPPS DRG table.
    *   `IRFBN105`: Updated IPPS State-Specific Rural Floor Budget Neutrality Factors.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

#### **Program: LTCAL111**

*   **Overview:** Another revision of the LTCH PPS payment calculation program, effective October 1, 2010. The structure is similar to `LTCAL103` and `LTCAL105`. It does not appear to use a state-specific RFBN table (`IRFBN`).
*   **Business Functions:** Similar to `LTCAL103` and `LTCAL105`, but with potentially different rate constants and calculation logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG110`: LTCH DRG table.
    *   `IPDRG110`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

#### **Program: LTCAL123**

*   **Overview:** The latest version (as of the provided snippets) of the LTCH PPS payment calculation program, effective October 1, 2011. The structure is similar to previous `LTCAL` programs. Like `LTCAL111`, it does not appear to use a state-specific RFBN table.
*   **Business Functions:** Similar to previous `LTCAL` programs, with updated constants and potentially refined logic.
*   **Other Programs Called:** Uses data from:
    *   `LTDRG123`: LTCH DRG table.
    *   `IPDRG123`: IPPS DRG table.
    *   Uses `BILL-NEW-DATA` and `PROV-NEW-HOLD` structures.

### 2. Data Table Definition Programs

These programs define and store lookup tables used by the processing programs. They do not call other programs but are called by them.

#### **Program: IPDRG160**

*   **Overview:** Defines a table (`PPS-DRG-TABLE`) containing Inpatient Prospective Payment System (IPPS) Diagnosis Related Group (DRG) data for 2015, including DRG codes, weights, average lengths of stay (ALOS), and descriptions.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2015.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs (like `LTCAL162`) to retrieve DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, which contains the DRG code, weight, ALOS, and description.

#### **Program: IPDRG170**

*   **Overview:** Defines an IPPS DRG table for 2016.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2016.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2016 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

#### **Program: IPDRG181**

*   **Overview:** Defines an IPPS DRG table for 2017.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2017.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2017 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

#### **Program: IPDRG190**

*   **Overview:** Defines an IPPS DRG table for 2018.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2018.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2018 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

#### **Program: IPDRG200**

*   **Overview:** Defines an IPPS DRG table for 2019.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2019.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2019 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

#### **Program: IPDRG211**

*   **Overview:** Defines an IPPS DRG table for 2020.
*   **Business Functions:**
    *   Stores IPPS DRG data for 2020.
    *   Provides a lookup mechanism for DRG codes and associated information.
*   **Other Programs Called:** This is a data table; it doesn't call other programs. It is called by other programs to retrieve 2020 DRG information. The data structure passed *to* it would be a DRG code. The data structure passed *from* it is `DRG-DATA-TAB`, containing DRG code, weight, ALOS, and description.

#### **Program: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG200, LTDRG210**

*   **Overview:** These are data tables containing LTCH DRG data for different years. The data includes DRG codes, relative weights, average lengths of stay (ALOS), and IPPS thresholds.
*   **Business Functions:** Store LTCH DRG data for lookups.
*   **Other Programs Called:** These are data tables; they don't call other programs. They are called by the `LTCAL...` programs. The data structure passed *to* them would be a DRG code; the data structure passed *from* them is `WWM-ENTRY` containing the DRG code, relative weight, and ALOS.

#### **Program: LTDRG100**

*   **Overview:** Defines a table (`W-DRG-TABLE`) containing LTCH DRG data, encoded in `W-DRG-FILLS` and redefined.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data (relative weights and average lengths of stay).
*   **Other Programs Called:** None; this is a data definition program.

#### **Program: LTDRG110**

*   **Overview:** A revised LTCH DRG table, likely reflecting changes in DRG definitions or weights.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data.
*   **Other Programs Called:** None; this is a data definition program.

#### **Program: LTDRG123**

*   **Overview:** Another updated LTCH DRG table.
*   **Business Functions:** Data storage and retrieval of LTCH DRG data.
*   **Other Programs Called:** None; this is a data definition program.

#### **Program: LTDRG031**

*   **Overview:** A data definition module containing a DRG lookup table. It defines a table (`WWM-ENTRY`) that maps DRG codes (`WWM-DRG`) to relative weights (`WWM-RELWT`) and average lengths of stay (`WWM-ALOS`). This table is used by other programs (e.g., `LTCAL032`, `LTCAL042`) via COPY statements. The table is initialized using literal values.
*   **Business Functions:** DRG Lookup Table Definition: Provides a central repository for DRG-related data.
*   **Called Programs & Data Structures:** This program does not call any other programs. It defines the `WWM-ENTRY` data structure.

#### **Program: IPDRG104**

*   **Overview:** Defines a table (`DRG-TABLE`) containing IPPS DRG data, including an effective date and multiple sets of weight, ALOS, trimmed days, and arithmetic ALOS values for numerous DRGs.
*   **Business Functions:**
    *   Data storage and retrieval of IPPS DRG data.
    *   Potentially used in calculating reimbursement amounts based on DRG codes.
*   **Other Programs Called:** None directly called within this code snippet. This is a data definition program; its purpose is to be called by other programs.

#### **Program: IPDRG110**

*   **Overview:** Similar to `IPDRG104`, defines an IPPS DRG table (`DRG-TABLE`) with an effective date of '20101001'. It appears to be a subsequent version or update.
*   **Business Functions:** Identical to `IPDRG104`.
*   **Other Programs Called:** None directly called within this code snippet. This is a data definition program.

#### **Program: IPDRG123**

*   **Overview:** Another IPPS DRG data table (`DRG-TABLE`), with an effective date of '20111001'. This represents a further update of the DRG data.
*   **Business Functions:** Identical to `IPDRG104`.
*   **Other Programs Called:** None directly called within this code snippet. This is a data definition program.

#### **Program: IRFBN102**

*   **Overview:** Defines a table (`PPS-SSRFBN-TABLE`) containing State-Specific Rural Floor Budget Neutrality Factors (SSRFBNs), likely used to adjust payments based on geographic location. The table includes state codes, rates, and descriptive information.
*   **Business Functions:**
    *   Storage and retrieval of state-specific payment adjustment factors.
    *   Used to adjust IPPS payments based on state and potentially rural location.
*   **Other Programs Called:** None directly called within this code snippet. This is a data definition program.

#### **Program: IRFBN105**

*   **Overview:** Appears to be a revised version of `IRFBN102`, containing updated SSRFBN data with identical structure but different values, implying an update to the rates for different states.
*   **Business Functions:** Identical to `IRFBN102`.
*   **Other Programs Called:** None directly called within this code snippet. This is a data definition program.

### Cross-Program Considerations:

*   **COPY Statements:** The use of `COPY` statements (e.g., in `LTCAL032`, `LTCAL042`, `LTDRV212`, `LTOPN212`) indicates that these programs rely on external data definitions. The actual content of these copied files is crucial for a complete understanding of the programs' functionality. If a copied file is modified, all programs using it need to be recompiled.
*   **Implicit Data Structure Usage:** For programs that `COPY` data definitions (like `LTDRG031` and `LTDRG100`), the data structures are not passed as explicit parameters but are used directly within the program's logic.
*   **Program Naming Conventions:** The ellipses ("...") in some program names suggest they are part of larger, more specific program names, implying a family of similar programs.
*   **Procedural Logic:** The provided snippets primarily focus on data structures. The `PROCEDURE DIVISION` sections, which contain the actual executable logic, are essential for a complete understanding of control flow and dynamic calls. `PERFORM` statements indicate internal subroutines.
*   **Data Structures:** The programs demonstrate well-defined data structures, utilizing COBOL features like `OCCURS`, `INDEXED BY`, and `REDEFINES` for efficient data handling and alternate views of data.