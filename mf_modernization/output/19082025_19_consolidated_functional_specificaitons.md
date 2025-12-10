## Control Flow and Module Execution Order

This document consolidates the analysis of COBOL programs responsible for calculating Medicare Prospective Payment System (PPS) payments for Long-Term Care Hospitals (LTCHs) and Inpatient Prospective Payment Systems (IPPS). The analysis is derived from multiple functional specification documents, providing insights into program functionalities, execution sequences, and the use cases they address.

---

### Overall System Functionality:

The primary purpose of this suite of COBOL programs is to calculate Medicare prospective payments for LTCH claims. This process involves complex logic that considers various factors, including:

*   **Diagnosis Related Groups (DRGs):** Payments are fundamentally based on the DRG assigned to a patient's bill.
*   **Length of Stay (LOS):** The duration of a patient's stay influences payment calculations, particularly for short stays.
*   **Wage Index:** Geographic variations in labor costs are accounted for through wage index adjustments.
*   **Fiscal Year (FY) and Versioning:** The system is designed to handle annual updates and changes in payment rules and data tables, with programs and data structures often versioned by year or effective date.
*   **Provider-Specific Data:** Variations in payment based on individual hospital characteristics and specific provider rules are accommodated.
*   **Outlier Payments:** Additional payments are made for unusually high-cost or long-stay cases.
*   **Transitional Payment Methodologies:** The system supports blended payment calculations during periods of transition between different payment systems.

---

### Program Categorization and Execution Flow Inference:

While exact calling sequences are not always explicitly defined, the program names, COPY statements, and linkage sections allow for the inference of a general execution flow. The programs can be broadly categorized as follows:

1.  **Data Initialization/Table Loading Programs:** These programs (often named `LTDRGxxx` and `IPDRGxxx`) primarily define and load data tables, such as DRG weights, average lengths of stay (ALOS), and other rate-setting information. They are typically called once during initialization or before the main calculation programs.

2.  **Main Calculation Programs:** These programs (primarily named `LTCALxxx`) perform the core payment calculations. They utilize the data loaded by the initialization programs and process individual claim data.

3.  **Supporting Data/Utility Programs:** Programs like `RUFL200` (a copybook) or `IRFBNxxx` provide specific data or functionality used by the main calculation programs.

The general execution flow for processing a claim typically involves:

*   **Selection of the appropriate `LTCAL` program:** This is usually determined by the claim's discharge date, as different `LTCAL` programs are effective for specific periods.
*   **Loading of relevant data tables:** The selected `LTCAL` program will internally include or access data from `LTDRGxxx` and `IPDRGxxx` programs/copybooks relevant to the claim's discharge date.
*   **Processing of claim data:** The `LTCAL` program reads claim details, provider information, and wage index data.
*   **Performing calculations:** This includes DRG-based calculations, LOS adjustments, outlier calculations, wage index adjustments, and any applicable provider-specific or transitional adjustments.
*   **Returning results:** The program returns the calculated payment information and a return code indicating the outcome of the processing (success, specific calculation method used, or reason for failure).

---

### Detailed Program Analysis and Execution Sequence:

The following sections detail the programs analyzed from each functional specification, outlining their roles and inferred execution sequences:

#### From 'L1_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `LTMGR212`
*   `LTOPN212`
*   `LTDRV212`
*   `RUFL200` (Copybook)

**Sequence in which these programs are called, along with a description:**

1.  **`LTMGR212` (Main Program):** Acts as the primary driver. It reads billing records from `BILLFILE` (SYSUT1). For each record, it initiates the pricing calculation by calling `LTOPN212` and then writes the results to `PRTOPER` (a print file).
2.  **`LTOPN212` (Subroutine):** Called by `LTMGR212`. It handles file operations for `PROV-FILE`, `CBSAX-FILE`, `IPPS-CBSAX-FILE`, and `MSAX-FILE`. Based on `PRICER-OPTION-SW`, it loads wage index tables either from input data or files. It reads provider records and calls `LTDRV212` for pricing calculations.
3.  **`LTDRV212` (Subroutine):** Called by `LTOPN212`. It determines the appropriate wage index (MSA or CBSA, LTCH or IPPS) based on discharge date and provider information, using tables loaded by `LTOPN212`. It then calls version-specific `LTCALxxx` modules (implied) for the actual pricing calculations and returns the payment information.
4.  **`RUFL200` (Copybook):** Contains the `RUFL-ADJ-TABLE` for rural floor factors, used by `LTDRV212` for wage index calculations, particularly for fiscal year 2020 and later.

**List of Use Cases Addressed by All Programs Together:**
*   Prospective Payment Calculation for LTCHs.
*   Versioning and Updates for payment rules.
*   Handling Provider-Specific Data.
*   Efficient Data Table Management (wage indices, provider data).
*   Facilitating Testing and Development.
*   Report Generation (`PRTOPER`).

---

#### From 'L2_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `IPDRG160`, `IPDRG170`, `IPDRG181`, `IPDRG190`, `IPDRG211`
*   `LTCAL162`, `LTCAL170`, `LTCAL183`, `LTCAL190`, `LTCAL202`, `LTCAL212`
*   `LTDRG160`, `LTDRG170`, `LTDRG181`, `LTDRG190`, `LTDRG210`, `LTDRG211`

**Sequence in which these programs are called, along with a description:**

*   **`LTDRV` (Inferred Main Driver):** Reads bill and provider data, then calls appropriate `IPDRG` and `LTDRG` programs before `LTCAL` programs.
*   **`IPDRGXXX`:** Contain IPPS DRG tables for different years. Called by `LTDRV` based on discharge date for data lookup.
*   **`LTDRGXXX`:** Contain LTCH DRG tables for different years. Called by `LTDRV` based on discharge date for data lookup.
*   **`LTCALXXX`:** Core LTCH payment calculation modules. Called by `LTDRV`, receiving bill data, provider data, and DRG tables. They perform complex payment calculations.

**List of Use Cases Addressed by All Programs Together:**
*   LTCH Payment Calculation (DRG, LOS, wage index, cost report days, covered days, CCR, outliers, blend percentages, provider adjustments, fiscal year, policy changes).
*   Data Management for DRG tables.
*   Error Handling and Return Codes.
*   Reporting (populating `PPS-DATA-ALL`).

---

#### From 'L4_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `IPDRG104`, `IPDRG110`, `IPDRG123`
*   `IRFBN102`, `IRFBN105`
*   `LTCAL103`, `LTCAL105`, `LTCAL111`, `LTCAL123`
*   `LTDRG100`, `LTDRG110`, `LTDRG123`

**Sequence in which these programs are called, along with the description:**

*   **`LTDRGxxx`:** Table-defining programs for LTCH DRG data. Likely called once during initialization to load DRG tables (`WWM-ENTRY`).
*   **`IRFBNxxx`:** Programs defining State-Specific Rural Floor Budget Neutrality Factors (RFBNS) tables (`SSRFBN-TAB`). Likely loaded once during initialization.
*   **`IPDRGxxx`:** Programs defining IPPS DRG tables (`DRG-TABLE`). Likely initialized once.
*   **`LTCALxxx`:** Main calculation programs. Use data from loaded tables (`LTDRGxxx`, `IRFBNxxx`, `IPDRGxxx`) to calculate payments. They receive bill data, provider data, wage index data, and control information.

**Probable call sequence within a single claim processing cycle:**
`LTDRGxxx` -> `IRFBNxxx` -> `IPDRGxxx` -> `LTCALxxx`
(This sequence would be repeated for each relevant version of `LTCALxxx`).

**List of Use Cases Addressed by all the programs together:**
*   DRG-based Payment Calculation.
*   Length of Stay (LOS) Considerations (short stay vs. normal stay).
*   Outlier Payments.
*   Wage Index Adjustment.
*   State-Specific Adjustments (RFBNS).
*   Blended Payments.
*   Versioning and Updates.

---

#### From 'L5_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `IPDRG080`, `IPDRG090`
*   `IRFBN091`
*   `LTCAL087`, `LTCAL091`, `LTCAL094`, `LTCAL095`
*   `LTDRG080`, `LTDRG086`, `LTDRG093`, `LTDRG095`

**Sequence in which these programs are called, along with the description:**

1.  **Data Initialization:** `LTDRGXXX` and `IPDRGXXX` programs populate `DRG-TABLE` and `PPS-SSRFBN-TABLE`. Called before calculation programs. Order between `LTDRG` and `IPDRG` within a version is not determinable.
2.  **Main Calculation Program:** `LTCALXXX` programs perform payment calculations using initialized tables. Called sequentially based on claim date.
3.  **`LTCALXXX` Internal Calls:** Each `LTCALXXX` calls internal subroutines (e.g., `0100-INITIAL-ROUTINE`, `1000-EDIT-THE-BILL-INFO`, `3000-CALC-PAYMENT`, `7000-CALC-OUTLIER`, `8000-BLEND`, `9000-MOVE-RESULTS`) in a specified `PERFORM` order.
4.  **`IRFBN091` Usage:** Called by `LTCAL094` and `LTCAL095` to adjust the IPPS wage index, acting as a lookup table for state-specific data.

**List of Use Cases Addressed by all the programs together:**
*   DRG-based Payment Calculation (using versioned DRG tables).
*   Short-Stay Outlier Provision (blending methodologies).
*   IPPS Comparable Payment (alternative for short stays).
*   Wage Index Adjustment (state-specific using `IRFBN091`, blended across FYs).
*   Cost Outlier Calculation.
*   Provider-Specific Rates and COLAs.
*   Return Codes (`PPS-RTC`) for processing outcomes.

---

#### From 'L6_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `IPDRG063`, `IPDRG071` (IPPS DRG tables)
*   `LTCAL064`, `LTCAL072`, `LTCAL075`, `LTCAL080` (LTCH PPS calculation programs)
*   `LTDRG062`, `LTDRG075`, `LTDRG080` (LTCH DRG tables)

**Sequence in which these programs are called, along with a description:**

1.  A main driver program (not shown) reads LTCH claims.
2.  The driver calls the appropriate `LTCAL` program based on the claim's discharge date and effective pricing logic.
3.  The selected `LTCAL` program internally uses appropriate `LTDRG` and `IPDRG` COPY files (tables) for DRG information lookup.
4.  The `LTCAL` program performs calculations using claim data, provider data, and wage index data.
5.  The `LTCAL` program returns `PPS-DATA-ALL` and a return code (`PPS-RTC`) to the driver.

**List of Use Cases Addressed by all the programs together:**
*   DRG-based payment calculation (weights, ALOS).
*   Short-stay outlier payments (evolving logic and return codes).
*   Outlier payment calculation.
*   Wage index adjustment (CBSA).
*   Blend year adjustment.
*   Provider-specific adjustments (COLAs).
*   Error handling and return codes.
*   Data maintenance for DRG tables.

---

#### From 'L7_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `LTCAL043`, `LTCAL058`, `LTCAL059`, `LTCAL063` (PPS calculation programs)
*   `LTDRG041`, `LTDRG057` (Copybooks for DRG data)

**Sequence in which these programs are called, along with a description:**

*   **`LTDRG041` and `LTDRG057`:** Copybooks containing DRG table data definitions. Not independently executable; included in `LTCAL` programs. `LTDRG041` likely used by `LTCAL043`, and `LTDRG057` by `LTCAL058`, `LTCAL059`, `LTCAL063`.
*   **`LTCAL` programs:** Called by a higher-level program based on claim discharge date. Each performs a specific version of PPS calculations.
*   **Likely chronological order of `LTCAL` programs:** `LTCAL043`, `LTCAL058`, `LTCAL059`, `LTCAL063`, reflecting versioning and updates.

**List of Use Cases Addressed by all the programs together:**
*   DRG-based Payment Calculation.
*   Length of Stay (LOS) Adjustments.
*   Short-Stay Outlier Payments.
*   Cost Outlier Payments.
*   Wage Index Adjustments (MSA/CBSA).
*   Blend Year Calculations.
*   Versioning and Updates.
*   Data Validation and Error Handling (Return Codes).

---

#### From 'L8_FunctionalSpecification.md':

**List of COBOL Programs Analyzed:**
*   `LTCAL032`, `LTCAL042` (PPS calculator programs)
*   `LTDRG031` (COPY member for DRG data)

**Sequence in which these programs are called, along with the description:**

1.  **`LTDRG031`:** COPY member containing DRG data (codes, weights, ALOS). Used by both `LTCAL032` and `LTCAL042`.
2.  **`LTCAL032`:** PPS calculator effective January 1, 2003. Takes bill, provider, and wage index data as input. Performs edits and calculations. Returns results and a return code (`PPS-RTC`).
3.  **`LTCAL042`:** PPS calculator effective July 1, 2003. Uses `LTDRG031`. Similar structure to `LTCAL032` but with updated logic, including special provider handling (`P-NEW-PROVIDER-NO = '332006'`) and specific blend calculations. Returns results and a return code.

**Inferred Calling Sequence:** A main program (not shown) would call either `LTCAL032` or `LTCAL042` based on the bill's discharge date to select the appropriate PPS calculation rules.

**List of Use Cases Addressed by all programs together:**
*   Prospective Payment System (PPS) Calculation.
*   Data Validation and Error Handling (Return Codes).
*   Version Control (`CAL-VERSION`, `PPS-CALC-VERS-CD`).
*   DRG Lookup (`LTDRG031`).
*   Short-Stay and Outlier Calculations.
*   Blend Year Calculations.
*   Special Provider Handling (e.g., `LTCAL042`).

---

### Consolidated List of Use Cases Addressed by All Programs Together:

Across all analyzed documents, the programs collectively address the following comprehensive set of use cases related to Medicare PPS for LTCHs:

*   **DRG-based Payment Calculation:** The fundamental use case, determining payment amounts based on assigned Diagnosis Related Groups (DRGs), including their relative weights and average lengths of stay.
*   **Length of Stay (LOS) Considerations:** Processing claims with varying lengths of stay, including specific logic for short stays.
*   **Short-Stay Outlier Payments:** Calculating additional payments when a patient's stay is significantly shorter than the average for their DRG, often involving blended payment methodologies.
*   **Cost Outlier Payments:** Adjusting payments for claims where the facility costs exceed predetermined thresholds.
*   **Wage Index Adjustments:** Applying adjustments to payments based on the geographic location's wage index (initially MSA, later CBSA), accounting for regional cost differences.
*   **State-Specific Adjustments:** Incorporating state-specific factors, such as Rural Floor Budget Neutrality Factors (RFBNS), to further refine wage index calculations.
*   **Blend Year Calculations:** Managing transitional periods where payment methodologies are phased in, often involving a blend of facility-specific rates and standard DRG-based payments.
*   **Versioning and Updates:** The system is designed to accommodate frequent updates to payment rules, rates, and data tables across numerous fiscal years and effective dates, as evidenced by the version numbers in program names (`LTCALxxx`, `LTDRGxxx`, `IPDRGxxx`).
*   **Provider-Specific Data and Rules:** Handling variations in payment based on individual provider characteristics, including special provider rules and Cost of Living Adjustments (COLAs).
*   **Data Management:** Efficiently managing large data tables, such as DRG definitions and wage index data, often through COPY members or separate data programs.
*   **Data Validation and Error Handling:** Implementing extensive data edits and checks to ensure input accuracy, with return codes (`PPS-RTC`) providing detailed feedback on processing outcomes, including success, the specific calculation method used, or reasons for failure.
*   **IPPS Comparable Payment:** In some versions, calculating payments based on Inpatient Prospective Payment System (IPPS) comparable amounts as an alternative for specific scenarios (e.g., short stays).
*   **Report Generation:** Producing output reports (e.g., `PRTOPER`) summarizing the processed claim data and payment calculations.
*   **Testing and Development Support:** Comments within the code suggest considerations for different testing scenarios and data passing options.