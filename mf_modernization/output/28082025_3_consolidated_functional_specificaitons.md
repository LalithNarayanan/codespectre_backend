## Business Logic

This document consolidates the business logic extracted from multiple functional specification files, detailing the execution flow, business rules, and data validation/error handling of various COBOL programs involved in calculating Medicare payments for Long-Term Care Hospitals (LTCHs) and Inpatient Prospective Payment Systems (IPPS).

The analysis highlights the progressive evolution of these programs, reflecting changes in regulations, payment methodologies, and data requirements over time.

---

### Program: LTMGR212

This program is responsible for calculating long-term care (LTC) payments using a Prospective Payment System (PPS).

**1. Paragraph Execution Order and Description:**

1.  **0000-MAINLINE:** Opens input `BILLFILE` and output `PRTOPER`. Initializes `PPS-VERSIONS` to zeros and starts the main processing loop.
2.  **0100-PROCESS-RECORDS:** Reads a record from `BILLFILE` into `BILL-WORK`. Sets `EOF-SW` to 1 to terminate the loop upon end-of-file.
3.  **1000-CALC-PAYMENT:** Calls the `LTOPN212` subroutine to perform PPS calculations using option 1 (' '). Options 2 and 3 are commented out.
4.  **1100-WRITE-SYSUT2:** Formats and writes calculated payment data to `PRTOPER`. Includes error handling for write operations to `PRTOPER`.
5.  **1200-PPS-HEADINGS:** Writes header information to `PRTOPER` if the line counter (`OPERLINE-CTR`) exceeds 54 lines. Includes error handling for write operations.
6.  **0100-EXIT:** Exits the `0100-PROCESS-RECORDS` paragraph.
7.  **0100-PROCESS-RECORDS (repeated):** The loop continues until `EOF-SW` is 1.
8.  **0000-MAINLINE (continued):** Closes `BILLFILE` and `PRTOPER` and ends program execution.

**2. Business Rules:**

*   Calculates payments for LTC using a PPS.
*   Supports different pricing options, though only option 1 is active.
*   Payment calculations consider factors like length of stay (LOS), covered days, Diagnosis Related Groups (DRGs), wage indices (MSA or CBSA), and provider-specific data.
*   Uses a line counter to control header printing on the output report.

**3. Data Validation and Error Handling:**

*   **File I/O Errors:** Uses file status variables (`UT1-STAT`, `OPR-STAT`) to check for errors during file operations. Displays error messages for write errors. This is considered rudimentary error handling; more robust methods would involve logging and retry mechanisms.
*   **Data Validation:** No explicit data validation within `LTMGR212`; validation is assumed to occur in called subroutines (`LTOPN212`, `LTCAL`).
*   **Record Processing:** Checks `EOF-SW` to ensure it is 0 before processing a record.

---

### Program: LTOPN212

This subroutine loads wage index tables and provider-specific data, preparing for further processing by `LTDRV212`.

**1. Paragraph Execution Order and Description:**

1.  **0000-TEST-PRICER-OPTION-SW:** Determines processing path based on `PRICER-OPTION-SW` (A, P, or blank).
2.  **1200-GET-THIS-PROVIDER:** Searches `PROV-TABLE` for a provider record matching the bill's provider number. Sets `PPS-RTC` to 59 if not found. Updates `PROV-NEW-HOLD` with provider data if found. Includes error handling for provider not found.
3.  **1300-GET-CURR-PROV:** Refines provider record selection based on the bill's discharge date.
4.  **1500-LOAD-ALL-TABLES:** Loads provider, MSA, CBSA, and IPPS CBSA wage index tables from their files. This occurs only on the first call. Includes error handling for reading the provider file.
5.  **1600-READ-PROV-FILE:** Reads records from `PROV-FILE` and loads them into `PROV-TABLE`.
6.  **1700-LOAD-MSAX-FILE, 1750-LOAD-CBSAX-FILE, 1775-LOAD-IPPS-CBSAX-FILE:** Read and load MSA, CBSA, and IPPS CBSA wage index tables into arrays.
7.  **1800-READ-MSAX-FILE, 1850-READ-CBSAX-FILE, 1875-READ-IPPS-CBSAX-FILE:** Read individual records from MSAX-FILE, CBSAX-FILE, and IPPS-CBSAX-FILE and populate corresponding tables.
8.  **1900-OPTION-SW-A, 2000-OPTION-SW-P, 2100-OPTION-SW:** Handle different options based on `PRICER-OPTION-SW`. Option A loads tables from user data, Option P loads MSA/CBSA/IPPS CBSA wage index tables, and Option Blank loads all tables from files.
9.  **0000-TEST-PRICER-OPTION-SW (continued):** Executes the selected option's paragraph.
10. **9650-CALL-LTDRV212:** Calls the `LTDRV212` subroutine, passing processed bill and provider data.
11. **GOBACK:** Returns control to the calling program.

**2. Business Rules:**

*   Loads wage index tables (MSA and CBSA) and provider-specific data.
*   Selects the wage index file (MSA or CBSA) based on the bill's discharge date.
*   Handles different options for passing data to the next pricing module (`LTDRV212`), with only one option active.
*   Provider data is loaded into a table for efficient batch processing lookup.

**3. Data Validation and Error Handling:**

*   **File I/O Errors:** Uses file status variables (`PROV-STAT`, `MSAX-STAT`, `CBSAX-STAT`, `IPPS-CBSAX-STAT`) for error checking.
*   **Provider Not Found:** Checks for a provider record; if not found, `PPS-RTC` is set to 59.
*   **General Validation:** Basic data validation is implied by program structure; more robust checks would enhance reliability.

---

### Program: LTDRV212

This program is a complex module that retrieves wage index records and calls the appropriate `LTCAL` module.

**1. Paragraph Execution Order and Description:**

This program is very lengthy and complex. The general flow is:

1.  **MAIN PARAGRAPH:** Initializes variables and moves data from `PROV-RECORD` to `PROV-NEW-HOLD`.
2.  **DATE AND FISCAL YEAR PROCESSING:** Determines the fiscal year based on the bill's discharge date.
3.  **WAGE INDEX LOOKUP:** A significant section that uses different logic based on the fiscal year to determine appropriate wage indices (MSA or CBSA, and IPPS CBSA). This involves searching wage index tables (`MSA-WI-TABLE`, `CBSA-WI-TABLE`, `IPPS-CBSA-WI-TABLE`) and handling special wage indices.
4.  **RURAL FLOOR LOGIC:** Implements complex logic to determine rural floor wage indices based on various criteria and specific state codes, involving extensive conditional logic.
5.  **LTCAL MODULE CALL:** Calls the appropriate `LTCAL` module (e.g., `LTCAL212`, `LTCAL202`) based on fiscal year and other conditions.
6.  **GOBACK:** Returns control to the calling program.

**2. Business Rules:**

*   Retrieves wage index records for the bill.
*   Calls the correct `LTCAL` module based on the bill's discharge date and fiscal year.
*   Includes complex logic for handling rural floor wage indices, which vary by fiscal year and state.
*   The selection of the correct wage index and determination of rural floors are highly dependent on the fiscal year and potentially other parameters.

**3. Data Validation and Error Handling:**

*   **Return Codes:** Error handling is primarily through return codes (`PPS-RTC`). Specific return codes indicate problems like wage index not found or invalid data.
*   **Implicit Validation:** Data validation is implicit in the program's structure and logic; more rigorous checks (e.g., range checks, data type validation) would improve robustness.

---

### Copybook: RUFL200

This is a copybook, not an executable program.

*   **Content:** Defines a table (`RUFL-ADJ-TABLE`) containing rural floor factors for different CBSAs.
*   **Business Rules:** The data within the copybook represents business rules, specifically the rural floor factors used in IPPS calculations.
*   **Executable Code:** Contains no executable code.

---

### Overall Observations (from L1_FunctionalSpecification.md):

*   The programs are complex and heavily reliant on external data files and numerous subroutines.
*   Error handling is primarily through return codes, making debugging and maintenance challenging.
*   The code relies heavily on conditional logic, making it difficult to understand and modify without extensive documentation.
*   Data validation is largely missing; adding more checks would be beneficial.
*   The extensive use of copybooks suggests a large, well-established system.
*   Change logs indicate a long history of maintenance and updates, reflecting the evolving nature of PPS regulations.
*   Access to `LTCAL` modules and detailed documentation is necessary for a complete understanding of business logic and error handling. Modernizing the code would significantly improve readability, maintainability, and error handling.

---

### Programs: IPDRG160, IPDRG170, IPDRG181, IPDRG190, IPDRG211

These programs are data definition modules (tables of DRG data).

*   **Paragraphs:** None (data definitions only).
*   **Business Rules:** Contain business rules encoded in DRG tables. Each record represents a DRG with associated weights, average lengths of stay (ALOS), and other payment-influencing factors. `DRG-LOW`, `DRG-PAC`, and `DRG-SPPAC` likely indicate flags for specific conditions or payment adjustments.
*   **Data Validation and Error Handling:** No explicit validation or error handling within these modules; it resides in programs that utilize these tables.

---

### Programs: LTCAL162, LTCAL170, LTCAL183, LTCAL190, LTCAL202, LTCAL212

These are the main processing programs that read bill and provider data, perform calculations, and return payment information.

**1. Paragraphs (General Execution Order):** The flow is similar across versions:

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables, sets constants and flags, and reads provider data (`PROV-NEW-HOLD`).
3.  `1000-EDIT-INPUT-DATA`: Validates bill data (`BILL-NEW-DATA`). Sets error return codes if validation fails.
4.  `1700-EDIT-DRG-CODE`: Looks up the LTCH DRG code in the `LTDRGxxx` table. Sets error codes if not found.
5.  `1800-EDIT-IPPS-DRG-CODE`: Looks up the IPPS DRG code in the `IPDRGxxx` table. Sets error codes if not found.
6.  `2000-ASSEMBLE-PPS-VARIABLES`: Assembles necessary components for payment calculation (wage index, COLA, blend percentages, etc.). Handles logic for supplemental wage indexes (in later versions).
7.  `3000-CALC-PAYMENT`: Calculates the payment amount based on the determined payment type (standard, site-neutral, blended). Includes logic for short-stay outliers and COVID-19 adjustments (in later versions). Calls several subroutines.
8.  `6000-CALC-HIGH-COST-OUTLIER`: Calculates high-cost outlier payments if applicable.
9.  `7000-SET-FINAL-RETURN-CODES`: Sets final return codes based on calculation results. Calls several subroutines.
10. `8000-CALC-FINAL-PMT`: Calculates the final payment amount, considering all adjustments.
11. `9000-MOVE-RESULTS`: Moves results to the output data structure (`PPS-DATA-ALL`). Handles errors.
12. `GOBACK`: Returns control to the calling program.

**2. Business Rules:**

*   **Data Tables:** COPYed data tables (`LTDRGxxx`, `IPDRGxxx`) define DRG-specific weights, ALOS, and other factors.
*   **Constants:** `PROGRAM-CONSTANTS` section defines fixed values (e.g., Federal fiscal year start date, ICD-10 code for ventilator use).
*   **Conditional Logic:** Complex conditional logic determines payment type, outlier adjustments, and return codes, incorporating changes from various correction notices and legislation (e.g., ACCESS Act, COVID-19).
*   **Formulas:** Specific formulas are used for calculating payments, outlier thresholds, and blended payments, embedded in `COMPUTE` statements.

**3. Data Validation and Error Handling:**

*   **Extensive Validation:** Implemented in `1000-EDIT-INPUT-DATA` and other sections. Checks for numeric values, valid ranges, and data consistency.
*   **Return Codes:** Invalid data triggers setting of appropriate return codes (`PPS-RTC`) in the 50-99 range, signaling errors to the calling program. Error codes are version-specific.
*   **Version Changes:** Different program versions reflect changes in business rules, leading to modifications in error codes and calculation logic.

---

### Programs: LTDRG160, LTDRG170, LTDRG181, LTDRG190, LTDRG210

These are data definition modules (tables of LTCH DRG data).

*   **Paragraphs:** None (data definitions only).
*   **Business Rules:** Encoded in the LTCH DRG tables. Each record represents an LTCH DRG with its relative weight, average length of stay (ALOS), and IPPS threshold.
*   **Data Validation and Error Handling:** No explicit validation or error handling present.

---

### Programs: IPDRG104, IPDRG110, IPDRG123

These programs are data definition modules, defining DRG tables.

*   **Paragraph Execution Order and Description:** These programs are solely data definitions with no procedural code. No paragraphs are executed. They define `DRG-TABLE` structures, likely for different years or versions.
*   **Business Rules:** Not explicitly defined; business rules are embedded in programs that use these tables.
*   **Data Validation and Error Handling:** No validation or error handling present; data is simply defined.

---

### Program: IRFBN102 and IRFBN105

These programs define state-specific tables for Rural Floor Budget Neutrality factors.

*   **Paragraph Execution Order and Description:** Primarily data definition programs with no `PROCEDURE DIVISION`. They define `PPS-SSRFBN-TABLE`, which is restructured using `REDEFINES` for easier access. No paragraphs are executed.
*   **Business Rules:** Implicit in the data itself, with each entry representing a state and its associated `SSRFBN` values.
*   **Data Validation and Error Handling:** No explicit validation or error handling is done in these data definition programs.

---

### Program: LTCAL103

This program calculates LTCH Medicare payments, utilizing DRG tables and applying various rules.

**1. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables, reads relevant data from tables (assumed from `COPY` statements), applies state-specific Rural Floor Budget Neutrality factors, and sets initial rates for LTCH and IPPS calculations.
3.  `1000-EDIT-THE-BILL-INFO`: Validates input `BILL-NEW-DATA`. Sets `PPS-RTC` to a non-zero value if errors are found.
4.  `1700-EDIT-DRG-CODE`: (Conditional) If `PPS-RTC` is 00, searches the LTCH DRG table (assumed from `COPY LTDRG100`) for the DRG weight and average length of stay.
5.  `1800-EDIT-IPPS-DRG-CODE`: (Conditional) If `PPS-RTC` is 00, searches the IPPS DRG table (assumed from `COPY IPDRG104`) for the DRG weight and average length of stay. This is performed for each period in the `DRGX-TAB`.
6.  `2000-ASSEMBLE-PPS-VARIABLES`: Assembles various pricing components including wage index adjustments.
7.  `3000-CALC-PAYMENT`: Calculates the standard payment amount, short-stay outlier amount, and short-stay blended payment. Includes logic for short-stay outliers and COVID-19 adjustments. Calls several subroutines.
8.  `7000-CALC-OUTLIER`: Calculates outlier payments if applicable. Adjusts `PPS-RTC` based on outlier calculations.
9.  `8000-BLEND`: Blends facility-specific and DRG payment amounts if applicable. Sets the final return code based on the blending.
10. `9000-MOVE-RESULTS`: Moves calculated results to the output `PPS-DATA-ALL`.
11. `GOBACK`: Returns control to the calling program.

**2. Business Rules:**

*   Payment calculations are based on length of stay, DRG codes, facility costs, wage indices, and other factors.
*   Rules are embedded in `COPY`ed data tables (`LTDRGxxx`, `IPDRGxxx`), `PROGRAM-CONSTANTS`, and conditional logic.
*   Formulas for payments, outlier thresholds, and blended payments are embedded in `COMPUTE` statements.

**3. Data Validation and Error Handling:**

*   Extensive data validation in `1000-EDIT-THE-BILL-INFO` and other edit routines.
*   Checks for numeric values, valid ranges, and consistency between input fields.
*   Invalid data triggers setting of appropriate return codes (`PPS-RTC`) in the 50-99 range.

---

### Program: LTCAL105

This program is very similar to `LTCAL103`, with key differences being the use of `COPY IRFBN105` and potentially updated rate constants.

*   **Business Rules:** Similar to `LTCAL103`, but potentially with updated payment calculation rules reflected in constants and copied data.
*   **Data Validation and Error Handling:** Similar to `LTCAL103`.

---

### Program: LTCAL111

This program is also very similar to `LTCAL103`, with key differences being the use of `COPY LTDRG110` and `COPY IPDRG110` (indicating updated DRG tables) and the absence of a state-specific RFBN table (`COPY IRFBN***`).

*   **Business Rules:** Similar to previous `LTCAL` programs, but likely with adjustments based on updated tables and potentially different rate constants.
*   **Data Validation and Error Handling:** Similar to `LTCAL103`.

---

### Program: LTCAL123

This program is very similar to `LTCAL111`, using the latest versions of the DRG tables (`COPY LTDRG123`, `COPY IPDRG123`) and lacking an RFBN table.

*   **Business Rules:** Similar payment calculation rules, but updated based on newer tables and constants.
*   **Data Validation and Error Handling:** Error handling remains consistent with previous `LTCAL` programs.

---

### Programs: LTDRG100, LTDRG110, LTDRG123

These are data definition modules defining LTCH DRG tables.

*   **Paragraphs:** None (data definitions only).
*   **Business Rules:** Encoded in the LTCH DRG tables, containing DRG codes, relative weights, and average lengths of stay (ALOS). `LTDRG123` also includes an IPPS threshold field.
*   **Data Validation and Error Handling:** No explicit validation or error handling present.

---

### Program: IPDRG080 and IPDRG090

These programs are data tables, not executable programs.

*   **Content:** Define `DRG-TABLE` containing DRG weight, Average Length of Stay (ALOS), days trim, and arithmetic ALOS data for different periods.
*   **Paragraphs:** None.
*   **Business Rules:** None explicitly defined; rules are in programs using these tables.
*   **Data Validation and Error Handling:** Implicit in PIC clauses. Invalid data could cause runtime errors.

---

### Program: IRFBN091

This program is a data table defining `PPS-SSRFBN-TABLE`, containing state-specific rural floor budget neutrality factors.

*   **Paragraphs:** None.
*   **Business Rules:** Implicit in the data, representing state-specific `SSRFBN` values.
*   **Data Validation and Error Handling:** Implicit in PIC clauses.

---

### Program: LTCAL087

This program calculates LTCH Medicare payments, incorporating various rules and provisions.

**1. Paragraph Execution Order (Simplified):**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables, loads rate constants (pre/post April 1, 2008), and loads IPPS-related constants.
3.  `1000-EDIT-THE-BILL-INFO`: Validates bill information (`B-LOS`, `B-COV-CHARGES`, `B-LTR-DAYS`, `B-COV-DAYS`, dates, provider termination status). Sets `PPS-RTC` on error.
4.  `1700-EDIT-DRG-CODE`: Searches `LTDRG086` for the LTCH DRG code. Sets `PPS-RTC` to 54 if not found.
5.  `1750-FIND-VALUE`: Retrieves relative weight and average LOS from `LTDRG086`.
6.  `1800-EDIT-IPPS-DRG-CODE`: Searches `IPDRG080` for the IPPS DRG code across table periods. Sets `PPS-RTC` to 54 if not found.
7.  `2000-ASSEMBLE-PPS-VARIABLES`: Assembles PPS variables, determines wage index based on provider fiscal year and blend year, and validates cost-to-charge ratio.
8.  `3000-CALC-PAYMENT`: Calculates standard payment amount. Forces COLA to 1.000 except for Alaska and Hawaii.
9.  `3400-SHORT-STAY`: (Called if `H-LOS <= H-SSOT`) Calculates short-stay payment based on cost, per diem, blended payment, or IPPS comparable. Includes special handling for provider '332006'.
10. `3600-SS-BLENDED-PMT`: Calculates blended short-stay payment.
11. `3650-SS-IPPS-COMP-PMT`: Calculates IPPS comparable payment components. Includes DSH adjustment logic.
12. `3675-SS-IPPS-COMP-PR-PMT`: Calculates Puerto Rico IPPS comparable payment.
13. `7000-CALC-OUTLIER`: Calculates outlier payment if applicable. Sets appropriate return codes.
14. `8000-BLEND`: Performs the blend calculation for the final payment. Adjusts `PPS-RTC` for blend year.
15. `9000-MOVE-RESULTS`: Moves calculated results to output parameters.
16. `GOBACK`: Returns control to the calling program.

**2. Business Rules:**

*   Payment calculation is based on LOS, DRG code, covered charges, and provider-specific data.
*   Short-stay outlier provisions apply if LOS is less than or equal to 5/6 of the average LOS, with multiple methodologies. Special rules for provider '332006'.
*   Cost outlier provisions apply if facility costs exceed a threshold.
*   A blend of facility-specific and standard DRG payments is used depending on the blend year.
*   Different rates and calculations apply to Puerto Rico hospitals.

**3. Data Validation and Error Handling:**

*   Extensive validation of input data.
*   Error handling through `PPS-RTC` return codes for invalid data, missing records, etc.
*   Uses `IF` and `EVALUATE` statements for checks on numeric values, ranges, and data consistency.

---

### Programs: LTCAL091, LTCAL094, LTCAL095

These programs are very similar to `LTCAL087`, differing primarily in the versions of COPY members they include and minor adjustments to constants and calculations.

*   **Business Rules:** Follow a similar pattern to `LTCAL087`, with updated constants, tables, and potentially minor algorithmic changes reflecting later effective dates.
*   **Data Validation and Error Handling:** Similar to `LTCAL087`.

---

### Program: IPDRG063

This program defines a lookup table for Inpatient Prospective Payment System (IPPS) Diagnosis Related Groups (DRGs).

*   **Content:** Contains a single data structure, `DRG-TABLE`.
*   **Paragraphs:** None (no executable code).
*   **Business Rules:** None explicitly defined; data represents DRG information.
*   **Data Validation and Error Handling:** None.

---

### Program: IPDRG071

Similar to IPDRG063, this program defines a `DRG-TABLE` for IPPS DRGs with an effective date ('20061001').

*   **Content:** Defines a `DRG-TABLE` data structure.
*   **Paragraphs:** None (no executable code).
*   **Business Rules:** None explicitly defined; data represents DRG information.
*   **Data Validation and Error Handling:** None.

---

### Program: LTCAL064

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**1. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables and sets program constants (labor/non-labor percentages, standard federal rate, fixed loss amount).
3.  `1000-EDIT-THE-BILL-INFO`: Validates bill data (LOS, discharge date, covered charges, LTR days, covered days). Sets `PPS-RTC` error codes if validation fails.
4.  `1200-DAYS-USED`: Determines regular and lifetime reserve days used based on total days and LOS.
5.  `1700-EDIT-DRG-CODE`: Searches `W-DRG-TABLE` for the submitted DRG code. Sets `PPS-RTC` to 54 if not found.
6.  `1750-FIND-VALUE`: Retrieves relative weight and average LOS from `W-DRG-TABLE`.
7.  `2000-ASSEMBLE-PPS-VARIABLES`: Selects wage index based on provider FY begin date and bill discharge date. Determines blend year and blend percentages. Validates provider's operating cost-to-charge ratio.
8.  `3000-CALC-PAYMENT`: Calculates standard payment amount and handles short-stay calculations (`3400-SHORT-STAY`).
9.  `3400-SHORT-STAY`: Calculates short-stay cost and payment, applying multipliers based on discharge date and provider.
10. `4000-SPECIAL-PROVIDER`: Contains special processing for provider '332006', applying different short-stay multipliers.
11. `7000-CALC-OUTLIER`: Calculates outlier threshold and payment if facility costs exceed the threshold. Sets appropriate return codes.
12. `8000-BLEND`: Calculates final payment considering blend year and short-stay/outlier adjustments. Sets final `PPS-RTC`.
13. `9000-MOVE-RESULTS`: Moves calculated PPS data to output parameters.

**2. Business Rules:**

*   Payment calculations are based on LOS, covered days, lifetime reserve days, and DRG code.
*   Short-stay payments are calculated differently depending on LOS and provider. Special rules apply to provider '332006'.
*   Outlier payments are triggered when facility costs exceed a calculated threshold.
*   Wage index blending is applied based on the provider's fiscal year begin date and the bill's discharge date, using a 4-year blend period.
*   Return codes (`PPS-RTC`) indicate payment method or reason for non-payment.

**3. Data Validation and Error Handling:**

*   `1000-EDIT-THE-BILL-INFO`: Validates numeric values and ranges for LOS, discharge date, covered charges, LTR days, and covered days. Error codes (50-74) indicate invalid data.
*   `1700-EDIT-DRG-CODE`: Checks for DRG code existence (error code 54).
*   `2000-ASSEMBLE-PPS-VARIABLES`: Validates wage index and cost-to-charge ratio.
*   `7000-CALC-OUTLIER`: Checks for cost outlier conditions.

---

### Program: LTCAL072

This program is an update to LTCAL064, with updated constants, rates, and additional logic for IPPS calculations.

*   **Paragraph Execution Order and Description:** Similar to LTCAL064, with the addition of `1800-EDIT-IPPS-DRG-CODE` for IPPS DRG processing.
*   **Business Rules:** Similar to LTCAL064 but includes IPPS calculation rules, separate wage indices for IPPS and LTCH, and blended payments. Short-stay outlier calculation includes a blend of LTCH and IPPS comparable amounts.
*   **Data Validation and Error Handling:** Similar to LTCAL064, with additional validation for IPPS-related data.

---

### Program: LTCAL075

This program is an update to LTCAL072, with different constants and slight modifications to the short-stay logic.

*   **Paragraph Execution Order and Description:** Overall structure is the same as LTCAL072.
*   **Business Rules:** Similar to LTCAL072, but with updated rates and constants. Modified short-stay logic introduces new return codes (20, 21, 22, 24, 25) for short-stay payment types.
*   **Data Validation and Error Handling:** Similar to LTCAL072.

---

### Program: LTCAL080

This program shares a similar structure with LTCAL075, but with updated constants, rates, and a new short-stay provision (#5) based on the IPPS comparable threshold.

*   **Paragraph Execution Order and Description:** Mainline control flow is largely the same as LTCAL075. The `3400-SHORT-STAY` paragraph is expanded to incorporate the new short-stay provision.
*   **Business Rules:** Updates to rates and constants. A new short-stay provision calculates payment based on the IPPS comparable threshold.
*   **Data Validation and Error Handling:** Similar to previous versions, with additional checks related to the new IPPS threshold. Short stay payment return codes 20, 21, 22, 24, 25, 26, and 27 are used.

---

### Program: LTDRG062, LTDRG075, LTDRG080

These are data definition programs that define lookup tables for DRG data.

*   **Content:** Define tables (`WWM-ENTRY`) containing DRG codes, relative weights, and average lengths of stay. `LTDRG080` also includes an IPPS threshold field.
*   **Paragraphs:** None (no executable code).
*   **Business Rules:** Implicit within the table data.
*   **Data Validation and Error Handling:** None.

---

### Program: LTCAL043

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL042

This program is very similar to LTCAL032, with additions to `4000-SPECIAL-PROVIDER` and modifications in wage index assembly and blending.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`
2.  `0100-INITIAL-ROUTINE` (updated values for federal rate, fixed loss amount, budget neutrality rate)
3.  `1000-EDIT-THE-BILL-INFO` (additional check for numeric `P-NEW-COLA`)
4.  `1200-DAYS-USED`
5.  `1700-EDIT-DRG-CODE`
6.  `1750-FIND-VALUE`
7.  `2000-ASSEMBLE-PPS-VARIABLES` (updated logic for wage index selection based on FY begin date and discharge date)
8.  `3000-CALC-PAYMENT`
9.  `3400-SHORT-STAY` (conditional call to `4000-SPECIAL-PROVIDER` based on provider number)
10. `4000-SPECIAL-PROVIDER` (handles special short-stay calculation for provider '332006' based on discharge date)
11. `7000-CALC-OUTLIER`
12. `8000-BLEND` (added calculation of `H-LOS-RATIO` and its use in final payment calculation)
13. `9000-MOVE-RESULTS` (updated version number in `PPS-CALC-VERS-CD`)
14. `GOBACK`

**B. Business Rules:**

*   Same as LTCAL032, with these additions:
    *   Special calculation for short-stay costs/payments for provider '332006', dependent on discharge date.
    *   `H-LOS-RATIO` is calculated and used to adjust the facility-specific rate in the blend calculation.

**C. Data Validation and Error Handling:**

*   Similar to LTCAL032, with these additions:
    *   Additional numeric check for `P-NEW-COLA`.
    *   Error code 50 used for non-numeric provider-specific rates or COLA values.

---

### Program: LTDRG031

This is a copybook that defines a DRG table.

*   **Content:** Defines a data structure containing DRG codes, relative weights, and average lengths of stay.
*   **Paragraphs:** None (data structure definition).
*   **Business Rules:** Contains business rules related to DRG codes, relative weights, and average lengths of stay, used in payment calculations within LTCAL032 and LTCAL042.
*   **Data Validation and Error Handling:** No validation or error handling within the copybook itself; it occurs in the programs that access this data.

---

### Program: LTCAL032

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate).
3.  `1000-EDIT-THE-BILL-INFO`: Validates bill information (`BILL-NEW-DATA`), including LOS, discharge date validity, provider termination status, covered charges, lifetime reserve days, and covered days. Sets `PPS-RTC` error codes if validation fails.
4.  `1200-DAYS-USED`: Calculates `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.
5.  `1700-EDIT-DRG-CODE`: Searches the `W-DRG-TABLE` (`LTDRG031`) for the DRG code. Sets `PPS-RTC` if not found.
6.  `1750-FIND-VALUE`: Retrieves relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the `W-DRG-TABLE`.
7.  `2000-ASSEMBLE-PPS-VARIABLES`: Retrieves wage index (`PPS-WAGE-INDEX`) from `WAGE-NEW-INDEX-RECORD`. Selects provider-specific variables based on blend year. Sets `PPS-RTC` error codes for invalid wage index or blend year.
8.  `3000-CALC-PAYMENT`: Calculates the standard payment amount, including facility costs, labor/non-labor portions, and federal payment amounts.
9.  `3400-SHORT-STAY`: Calculates short-stay cost and payment amounts if LOS is less than or equal to 5/6 of the average LOS. Selects the minimum of short-stay cost, short-stay payment amount, and DRG-adjusted payment amount.
10. `7000-CALC-OUTLIER`: Calculates the outlier threshold and payment amount if facility costs exceed the threshold. Sets `PPS-RTC` to indicate outlier payment. Handles special payment indicators and performs consistency checks.
11. `8000-BLEND`: Calculates the final payment amount based on the blend year and its rates/ratios. Updates `PPS-RTC` with the blend return code.
12. `9000-MOVE-RESULTS`: Moves calculated results to output parameters. Initializes certain output fields if `PPS-RTC` indicates an error.
13. `GOBACK`: Returns control to the calling program.

**B. Business Rules:**

*   Payment calculations are based on LOS, DRG code, covered charges, and provider-specific data.
*   Short-stay payments are calculated if LOS is <= 5/6 of the average LOS.
*   Outlier payments are calculated if facility costs exceed a predefined threshold.
*   Blend year affects payment calculations, using weighted averages of facility and DRG-based payments.
*   Specific return codes (`PPS-RTC`) indicate success, short-stay payment, outlier payment, or various error conditions.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** Performed on LOS, covered charges, wage index, etc.
*   **Date Checks:** Ensure discharge date is valid relative to provider effective, MSA effective dates, and termination dates.
*   **DRG Code Validation:** Checks for valid DRG codes in the lookup table.
*   **Consistency Checks:** Verify lifetime reserve days (<= 60) and covered days validity.
*   **Error Handling:** Uses `PPS-RTC` to store return codes (00 for success, 50-99 for errors). Error codes prevent further processing of invalid claims.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL103 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH Medicare payments, utilizing DRG tables and applying various rules.

**1. Paragraphs (General Execution Order):** The flow is similar across versions:

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables, sets constants and flags, and reads provider data (`PROV-NEW-HOLD`).
3.  `1000-EDIT-INPUT-DATA`: Validates bill data (`BILL-NEW-DATA`). Sets error return codes if validation fails.
4.  `1700-EDIT-DRG-CODE`: Looks up the LTCH DRG code in the `LTDRGxxx` table. Sets error codes if not found.
5.  `1800-EDIT-IPPS-DRG-CODE`: Looks up the IPPS DRG code in the `IPDRGxxx` table. Sets error codes if not found.
6.  `2000-ASSEMBLE-PPS-VARIABLES`: Assembles necessary components for payment calculation (wage index, COLA, blend percentages, etc.). Handles logic for supplemental wage indexes (in later versions).
7.  `3000-CALC-PAYMENT`: Calculates the payment amount based on the determined payment type (standard, site-neutral, blended). Includes logic for short-stay outliers and COVID-19 adjustments (in later versions). Calls several subroutines.
8.  `6000-CALC-HIGH-COST-OUTLIER`: Calculates high-cost outlier payments if applicable.
9.  `7000-SET-FINAL-RETURN-CODES`: Sets final return codes based on calculation results. Calls several subroutines.
10. `8000-CALC-FINAL-PMT`: Calculates the final payment amount, considering all adjustments.
11. `9000-MOVE-RESULTS`: Moves results to the output data structure (`PPS-DATA-ALL`). Handles errors.
12. `GOBACK`: Returns control to the calling program.

**2. Business Rules:**

*   **Data Tables:** COPYed data tables (`LTDRGxxx`, `IPDRGxxx`) define DRG-specific weights, ALOS, and other factors.
*   **Constants:** `PROGRAM-CONSTANTS` section defines fixed values (e.g., Federal fiscal year start date, ICD-10 code for ventilator use).
*   **Conditional Logic:** Complex conditional logic determines payment type, outlier adjustments, and return codes, incorporating changes from various correction notices and legislation (e.g., ACCESS Act, COVID-19).
*   **Formulas:** Specific formulas are used for calculating payments, outlier thresholds, and blended payments, embedded in `COMPUTE` statements.

**3. Data Validation and Error Handling:**

*   **Extensive Validation:** Implemented in `1000-EDIT-INPUT-DATA` and other sections. Checks for numeric values, valid ranges, and data consistency.
*   **Return Codes:** Invalid data triggers setting of appropriate return codes (`PPS-RTC`) in the 50-99 range, signaling errors to the calling program. Error codes are version-specific.
*   **Version Changes:** Different program versions reflect changes in business rules, leading to modifications in error codes and calculation logic.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL042 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL032, with additions to `4000-SPECIAL-PROVIDER` and modifications in wage index assembly and blending.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`
2.  `0100-INITIAL-ROUTINE` (updated values for federal rate, fixed loss amount, budget neutrality rate)
3.  `1000-EDIT-THE-BILL-INFO` (additional check for numeric `P-NEW-COLA`)
4.  `1200-DAYS-USED`
5.  `1700-EDIT-DRG-CODE`
6.  `1750-FIND-VALUE`
7.  `2000-ASSEMBLE-PPS-VARIABLES` (updated logic for wage index selection based on FY begin date and discharge date)
8.  `3000-CALC-PAYMENT`
9.  `3400-SHORT-STAY` (conditional call to `4000-SPECIAL-PROVIDER` based on provider number)
10. `4000-SPECIAL-PROVIDER` (handles special short-stay calculation for provider '332006' based on discharge date)
11. `7000-CALC-OUTLIER`
12. `8000-BLEND` (added calculation of `H-LOS-RATIO` and its use in final payment calculation)
13. `9000-MOVE-RESULTS` (updated version number in `PPS-CALC-VERS-CD`)
14. `GOBACK`

**B. Business Rules:**

*   Same as LTCAL032, with these additions:
    *   Special calculation for short-stay costs/payments for provider '332006', dependent on discharge date.
    *   `H-LOS-RATIO` is calculated and used to adjust the facility-specific rate in the blend calculation.

**C. Data Validation and Error Handling:**

*   Similar to LTCAL032, with these additions:
    *   Additional numeric check for `P-NEW-COLA`.
    *   Error code 50 used for non-numeric provider-specific rates or COLA values.

---

### Program: LTDRG031 (Duplicate from above, retained for completeness of the merged content)

This is a copybook that defines a DRG table.

*   **Content:** Defines a data structure containing DRG codes, relative weights, and average lengths of stay.
*   **Paragraphs:** None (data structure definition).
*   **Business Rules:** Contains business rules related to DRG codes, relative weights, and average lengths of stay, used in payment calculations within LTCAL032 and LTCAL042.
*   **Data Validation and Error Handling:** No validation or error handling within the copybook itself; it occurs in the programs that access this data.

---

### Program: LTCAL032 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate).
3.  `1000-EDIT-THE-BILL-INFO`: Validates bill information (`BILL-NEW-DATA`), including LOS, discharge date validity, provider termination status, covered charges, lifetime reserve days, and covered days. Sets `PPS-RTC` error codes if validation fails.
4.  `1200-DAYS-USED`: Calculates `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.
5.  `1700-EDIT-DRG-CODE`: Searches the `W-DRG-TABLE` (`LTDRG031`) for the DRG code. Sets `PPS-RTC` if not found.
6.  `1750-FIND-VALUE`: Retrieves relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the `W-DRG-TABLE`.
7.  `2000-ASSEMBLE-PPS-VARIABLES`: Retrieves wage index (`PPS-WAGE-INDEX`) from `WAGE-NEW-INDEX-RECORD`. Selects provider-specific variables based on blend year. Sets `PPS-RTC` error codes for invalid wage index or blend year.
8.  `3000-CALC-PAYMENT`: Calculates the standard payment amount, including facility costs, labor/non-labor portions, and federal payment amounts.
9.  `3400-SHORT-STAY`: Calculates short-stay cost and payment amounts if LOS is less than or equal to 5/6 of the average LOS. Selects the minimum of short-stay cost, short-stay payment amount, and DRG-adjusted payment amount.
10. `7000-CALC-OUTLIER`: Calculates the outlier threshold and payment amount if facility costs exceed the threshold. Sets `PPS-RTC` to indicate outlier payment. Handles special payment indicators and performs consistency checks.
11. `8000-BLEND`: Calculates the final payment amount based on the blend year and its rates/ratios. Updates `PPS-RTC` with the blend return code.
12. `9000-MOVE-RESULTS`: Moves calculated results to output parameters. Initializes certain output fields if `PPS-RTC` indicates an error.
13. `GOBACK`: Returns control to the calling program.

**B. Business Rules:**

*   Payment calculations are based on LOS, DRG code, covered charges, and provider-specific data.
*   Short-stay payments are calculated if LOS is <= 5/6 of the average LOS.
*   Outlier payments are calculated if facility costs exceed a predefined threshold.
*   Blend year affects payment calculations, using weighted averages of facility and DRG-based payments.
*   Specific return codes (`PPS-RTC`) indicate success, short-stay payment, outlier payment, or various error conditions.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** Performed on LOS, covered charges, wage index, etc.
*   **Date Checks:** Ensure discharge date is valid relative to provider effective, MSA effective dates, and termination dates.
*   **DRG Code Validation:** Checks for valid DRG codes in the lookup table.
*   **Consistency Checks:** Verify lifetime reserve days (<= 60) and covered days validity.
*   **Error Handling:** Uses `PPS-RTC` to store return codes (00 for success, 50-99 for errors). Error codes prevent further processing of invalid claims.

---

### Program: LTCAL042 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL032, with additions to `4000-SPECIAL-PROVIDER` and modifications in wage index assembly and blending.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`
2.  `0100-INITIAL-ROUTINE` (updated values for federal rate, fixed loss amount, budget neutrality rate)
3.  `1000-EDIT-THE-BILL-INFO` (additional check for numeric `P-NEW-COLA`)
4.  `1200-DAYS-USED`
5.  `1700-EDIT-DRG-CODE`
6.  `1750-FIND-VALUE`
7.  `2000-ASSEMBLE-PPS-VARIABLES` (updated logic for wage index selection based on FY begin date and discharge date)
8.  `3000-CALC-PAYMENT`
9.  `3400-SHORT-STAY` (conditional call to `4000-SPECIAL-PROVIDER` based on provider number)
10. `4000-SPECIAL-PROVIDER` (handles special short-stay calculation for provider '332006' based on discharge date)
11. `7000-CALC-OUTLIER`
12. `8000-BLEND` (added calculation of `H-LOS-RATIO` and its use in final payment calculation)
13. `9000-MOVE-RESULTS` (updated version number in `PPS-CALC-VERS-CD`)
14. `GOBACK`

**B. Business Rules:**

*   Same as LTCAL032, with these additions:
    *   Special calculation for short-stay costs/payments for provider '332006', dependent on discharge date.
    *   `H-LOS-RATIO` is calculated and used to adjust the facility-specific rate in the blend calculation.

**C. Data Validation and Error Handling:**

*   Similar to LTCAL032, with these additions:
    *   Additional numeric check for `P-NEW-COLA`.
    *   Error code 50 used for non-numeric provider-specific rates or COLA values.

---

### Program: LTDRG031 (Duplicate from above, retained for completeness of the merged content)

This is a copybook that defines a DRG table.

*   **Content:** Defines a data structure containing DRG codes, relative weights, and average lengths of stay.
*   **Paragraphs:** None (data structure definition).
*   **Business Rules:** Contains business rules related to DRG codes, relative weights, and average lengths of stay, used in payment calculations within LTCAL032 and LTCAL042.
*   **Data Validation and Error Handling:** No validation or error handling within the copybook itself; it occurs in the programs that access this data.

---

### Program: LTCAL032 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Execution Flow (Paragraphs and Description):**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate).
3.  `1000-EDIT-THE-BILL-INFO`: Validates bill information (`BILL-NEW-DATA`), including LOS, discharge date validity, provider termination status, covered charges, lifetime reserve days, and covered days. Sets `PPS-RTC` error codes if validation fails.
4.  `1200-DAYS-USED`: Calculates `PPS-REG-DAYS-USED` and `PPS-LTR-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.
5.  `1700-EDIT-DRG-CODE`: Searches the `W-DRG-TABLE` (`LTDRG031`) for the DRG code. Sets `PPS-RTC` if not found.
6.  `1750-FIND-VALUE`: Retrieves relative weight (`WWM-RELWT`) and average length of stay (`WWM-ALOS`) from the `W-DRG-TABLE`.
7.  `2000-ASSEMBLE-PPS-VARIABLES`: Retrieves wage index (`PPS-WAGE-INDEX`) from `WAGE-NEW-INDEX-RECORD`. Selects provider-specific variables based on blend year. Sets `PPS-RTC` error codes for invalid wage index or blend year.
8.  `3000-CALC-PAYMENT`: Calculates the standard payment amount, including facility costs, labor/non-labor portions, and federal payment amounts.
9.  `3400-SHORT-STAY`: Calculates short-stay cost and payment amounts if LOS is less than or equal to 5/6 of the average LOS. Selects the minimum of short-stay cost, short-stay payment amount, and DRG-adjusted payment amount.
10. `7000-CALC-OUTLIER`: Calculates the outlier threshold and payment amount if facility costs exceed the threshold. Sets `PPS-RTC` to indicate outlier payment. Handles special payment indicators and performs consistency checks.
11. `8000-BLEND`: Calculates the final payment amount based on the blend year and its rates/ratios. Updates `PPS-RTC` with the blend return code.
12. `9000-MOVE-RESULTS`: Moves calculated results to output parameters. Initializes certain output fields if `PPS-RTC` indicates an error.
13. `GOBACK`: Returns control to the calling program.

**B. Business Rules:**

*   Payment calculations are based on LOS, DRG code, covered charges, and provider-specific data.
*   Short-stay payments are calculated if LOS is <= 5/6 of the average LOS.
*   Outlier payments are calculated if facility costs exceed a predefined threshold.
*   Blend year affects payment calculations, using weighted averages of facility and DRG-based payments.
*   Specific return codes (`PPS-RTC`) indicate success, short-stay payment, outlier payment, or various error conditions.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** Performed on LOS, covered charges, wage index, etc.
*   **Date Checks:** Ensure discharge date is valid relative to provider effective, MSA effective dates, and termination dates.
*   **DRG Code Validation:** Checks for valid DRG codes in the lookup table.
*   **Consistency Checks:** Verify lifetime reserve days (<= 60) and covered days validity.
*   **Error Handling:** Uses `PPS-RTC` to store return codes (00 for success, 50-99 for errors). Error codes prevent further processing of invalid claims.

---

### Program: LTCAL072 (Duplicate from above, retained for completeness of the merged content)

This program is an update to LTCAL064, with updated constants, rates, and additional logic for IPPS calculations.

*   **Paragraph Execution Order and Description:** Similar to LTCAL064, with the addition of `1800-EDIT-IPPS-DRG-CODE` for IPPS DRG processing.
*   **Business Rules:** Similar to LTCAL064 but includes IPPS calculation rules, separate wage indices for IPPS and LTCH, and blended payments. Short-stay outlier calculation includes a blend of LTCH and IPPS comparable amounts.
*   **Data Validation and Error Handling:** Similar to LTCAL064, with additional validation for IPPS-related data.

---

### Program: LTCAL075 (Duplicate from above, retained for completeness of the merged content)

This program is an update to LTCAL072, with different constants and slight modifications to the short-stay logic.

*   **Paragraph Execution Order and Description:** Overall structure is the same as LTCAL072.
*   **Business Rules:** Similar to LTCAL072, but with updated rates and constants. Modified short-stay logic introduces new return codes (20, 21, 22, 24, 25) for short-stay payment types.
*   **Data Validation and Error Handling:** Similar to LTCAL072.

---

### Program: LTCAL080 (Duplicate from above, retained for completeness of the merged content)

This program shares a similar structure with LTCAL075, but with updated constants, rates, and a new short-stay provision (#5) based on the IPPS comparable threshold.

*   **Paragraph Execution Order and Description:** Mainline control flow is largely the same as LTCAL075. The `3400-SHORT-STAY` paragraph is expanded to incorporate the new short-stay provision.
*   **Business Rules:** Updates to rates and constants. A new short-stay provision calculates payment based on the IPPS comparable threshold.
*   **Data Validation and Error Handling:** Similar to previous versions, with additional checks related to the new IPPS threshold. Short stay payment return codes 20, 21, 22, 24, 25, 26, and 27 are used.

---

### Program: LTDRG062, LTDRG075, LTDRG080 (Duplicate from above, retained for completeness of the merged content)

These are data definition programs that define lookup tables for DRG data.

*   **Content:** Define tables (`WWM-ENTRY`) containing DRG codes, relative weights, and average lengths of stay. `LTDRG080` also includes an IPPS threshold field.
*   **Paragraphs:** None (no executable code).
*   **Business Rules:** Implicit within the table data.
*   **Data Validation and Error Handling:** None.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate from above, retained for completeness of the merged content)

This program shares structure with LTCAL058 and LTCAL059 but includes additional enhancements related to CBSA wage index and special pay indicators.

*   **CBSA Wage Index:** Uses a CBSA wage index instead of an MSA index. Input structures (`WAGE-NEW-INDEX-RECORD-CBSA`, `PPS-CBSA`) are updated. Error codes are adjusted (e.g., 60 for CBSA WAGE INDEX RECORD NOT FOUND).
*   **Special Pay Indicator:** Adds `P-NEW-SPECIAL-PAY-IND` and `P-NEW-SPECIAL-WAGE-INDEX` to `PROV-NEW-HOLD` for special wage index handling.
*   **Date Validation:** Discharge date comparison is against the CBSA effective date (`W-EFF-DATE`).
*   **Default Values:** Further updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, `PPS-BDGT-NEUT-RATE`.
*   **Special Provider Logic:** The `4000-SPECIAL-PROVIDER` paragraph includes additional logic for short-stay cost/payment calculations for different calendar years (2003-2007).
*   **Version Number:** `CAL-VERSION` is updated to 'V06.3'.
*   **Return Code:** Added return code 74 for provider FY begin date before 10/01/2002, and 98 for bill discharge date before 10/01/2002.

---

### Program: LTCAL043 (Duplicate from above, retained for completeness of the merged content)

This program calculates LTCH PPS payments, incorporating various rules and provisions.

**A. Paragraph Execution Order and Description:**

1.  `0000-MAINLINE-CONTROL`: Main control paragraph.
2.  `0100-INITIAL-ROUTINE` through `0100-EXIT`: Initializes variables with default values (national labor/non-labor percentages, standard federal rate, fixed loss amount, budget neutrality rate, PPS return code to 0).
3.  `1000-EDIT-THE-BILL-INFO` through `1000-EXIT`: Validates bill data (LOS, COLA, waiver status, discharge date, covered charges, lifetime reserve days, covered days). Sets `PPS-RTC` if errors are found. Calls `1200-DAYS-USED`.
4.  `1200-DAYS-USED` through `1200-DAYS-USED-EXIT`: Determines regular and lifetime reserve days used, considering LOS and available days.
5.  `1700-EDIT-DRG-CODE` through `1700-EXIT`: Looks up the DRG code from the `LTDRG041` table. Sets `PPS-RTC` to 54 if not found. Calls `1750-FIND-VALUE` if found.
6.  `1750-FIND-VALUE` through `1750-EXIT`: Retrieves relative weight and average length of stay from `LTDRG041`.
7.  `2000-ASSEMBLE-PPS-VARIABLES` through `2000-EXIT`: Selects wage index based on provider fiscal year begin date and bill discharge date. Performs validation on wage index and operating cost-to-charge ratio. Determines blend factors and return codes (`H-BLEND-RTC`) based on `PPS-BLEND-YEAR`.
8.  `3000-CALC-PAYMENT` through `3000-EXIT`: Calculates standard payment amount. If LOS is short stay (<= 5/6 of average LOS), calls `3400-SHORT-STAY`.
9.  `3400-SHORT-STAY` through `3400-SHORT-STAY-EXIT`: Calculates short-stay cost and payment, potentially using special logic for provider '332006'.
10. `7000-CALC-OUTLIER` through `7000-EXIT`: Calculates outlier threshold and payment if facility costs exceed the threshold. Adjusts `PPS-RTC` for outlier payment. Includes logic for Cost Outlier situations.
11. `8000-BLEND` through `8000-EXIT`: Calculates the final payment amount considering the blend year.
12. `9000-MOVE-RESULTS` through `9000-EXIT`: Moves calculated results to the output data structure.

**B. Business Rules:**

*   Payment calculation is based on LOS, DRG code, wage index, COLA, and provider-specific factors.
*   Short-stay payments are calculated differently, with a minimum payment determined.
*   Outlier payments are calculated if facility costs exceed a threshold.
*   Blend payments are applied based on the blend year indicator.
*   Specific rules apply to provider '332006'.

**C. Data Validation and Error Handling:**

*   **Numeric Checks:** LOS, COLA, covered charges, lifetime reserve days, covered days, wage indices, operating cost-to-charge ratio.
*   **Range Checks:** Lifetime reserve days (<= 60), covered days (consistency with LOS and LTR days).
*   **Date Checks:** Discharge date vs. provider effective and MSA effective dates.
*   **DRG Code Lookup:** Checks for DRG code existence in `LTDRG041`.
*   **Termination Date Check:** Verifies provider termination status before discharge date.
*   **Blend Year Validation:** Checks for valid blend year indicator values.
*   **Error Handling:** Uses `PPS-RTC` to store error codes (50-99), indicating processing failures.

---

### Program: LTCAL058 (Duplicate from above, retained for completeness of the merged content)

This program is very similar to LTCAL043, with key differences in wage index calculation and constants.

*   **Wage Index Calculation:** Revised to use an `EVALUATE` statement based on provider fiscal year begin date and discharge date, incorporating different blend percentages for different fiscal years. A new return code (98) is added for provider effective date before 10/01/2002.
*   **Constants:** Includes `PROGRAM-CONSTANTS` defining federal fiscal year begin dates.
*   **Default Values:** Updated default values for `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.8'.

---

### Program: LTCAL059 (Duplicate from above, retained for completeness of the merged content)

This program is almost identical to LTCAL058, with the primary difference being the use of `LTDRG057` instead of `LTDRG041`.

*   **DRG Table:** Uses `LTDRG057`, implying a different DRG table for this version.
*   **Version Number:** `CAL-VERSION` is updated to 'V05.9'.

---

### Program: LTCAL063 (Duplicate