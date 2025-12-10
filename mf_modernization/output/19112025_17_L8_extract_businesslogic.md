# Step 1: LTCAL032 Analysis

## LTCAL032

### Overview
- This COBOL program, LTCAL032, calculates Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) system.
- It receives bill data and provider information as input, performs edits, looks up DRG information, calculates payment amounts, and returns the results.
- The program uses a copybook `LTDRG031` for DRG-related data.
- It also uses the provider and wage index records to calculate the payment.

### Definitions
- `W-STORAGE-REF`:  A working storage field containing a descriptive string.
- `CAL-VERSION`: Stores the version of the calculation logic.
- `HOLD-PPS-COMPONENTS`: A group of working storage fields used to hold intermediate calculation results and input values, such as:
  - `H-LOS`: Length of Stay.
  - `H-REG-DAYS`: Regular Days.
  - `H-TOTAL-DAYS`: Total Days.
  - `H-SSOT`: Short Stay Outlier Threshold.
  - `H-BLEND-RTC`: Blend Return Code.
  - `H-BLEND-FAC`: Blend Facility Rate.
  - `H-BLEND-PPS`: Blend PPS Rate.
  - `H-SS-PAY-AMT`: Short Stay Payment Amount.
  - `H-SS-COST`: Short Stay Cost.
  - `H-LABOR-PORTION`: Labor Portion of the payment.
  - `H-NONLABOR-PORTION`: Non-Labor Portion of the payment.
  - `H-FIXED-LOSS-AMT`: Fixed Loss Amount.
  - `H-NEW-FAC-SPEC-RATE`: New Facility Specific Rate.
- `BILL-NEW-DATA`: A data structure passed to the program containing the bill information:
  - `B-NPI10`: National Provider Identifier.
    - `B-NPI8`: NPI (8 characters).
    - `B-NPI-FILLER`: NPI Filler (2 characters).
  - `B-PROVIDER-NO`: Provider Number.
  - `B-PATIENT-STATUS`: Patient Status.
  - `B-DRG-CODE`: DRG Code.
  - `B-LOS`: Length of Stay.
  - `B-COV-DAYS`: Covered Days.
  - `B-LTR-DAYS`: Lifetime Reserve Days.
  - `B-DISCHARGE-DATE`: Discharge Date (CCYYMMDD).
    - `B-DISCHG-CC`: Century.
    - `B-DISCHG-YY`: Year.
    - `B-DISCHG-MM`: Month.
    - `B-DISCHG-DD`: Day.
  - `B-COV-CHARGES`: Covered Charges.
  - `B-SPEC-PAY-IND`: Special Payment Indicator.
- `PPS-DATA-ALL`: A data structure passed back from the program containing the calculated PPS data:
  - `PPS-RTC`: Return Code (00-99).
  - `PPS-CHRG-THRESHOLD`: Charge Threshold.
  - `PPS-DATA`: PPS Data.
    - `PPS-MSA`: MSA.
    - `PPS-WAGE-INDEX`: Wage Index.
    - `PPS-AVG-LOS`: Average Length of Stay.
    - `PPS-RELATIVE-WGT`: Relative Weight.
    - `PPS-OUTLIER-PAY-AMT`: Outlier Payment Amount.
    - `PPS-LOS`: Length of Stay.
    - `PPS-DRG-ADJ-PAY-AMT`: DRG Adjusted Payment Amount.
    - `PPS-FED-PAY-AMT`: Federal Payment Amount.
    - `PPS-FINAL-PAY-AMT`: Final Payment Amount.
    - `PPS-FAC-COSTS`: Facility Costs.
    - `PPS-NEW-FAC-SPEC-RATE`: New Facility Specific Rate.
    - `PPS-OUTLIER-THRESHOLD`: Outlier Threshold.
    - `PPS-SUBM-DRG-CODE`: Submitted DRG Code.
    - `PPS-CALC-VERS-CD`: Calculation Version Code.
    - `PPS-REG-DAYS-USED`: Regular Days Used.
    - `PPS-LTR-DAYS-USED`: Lifetime Reserve Days Used.
    - `PPS-BLEND-YEAR`: Blend Year.
    - `PPS-COLA`: COLA.
  - `PPS-OTHER-DATA`: Other PPS Data.
    - `PPS-NAT-LABOR-PCT`: National Labor Percentage.
    - `PPS-NAT-NONLABOR-PCT`: National Non-Labor Percentage.
    - `PPS-STD-FED-RATE`: Standard Federal Rate.
    - `PPS-BDGT-NEUT-RATE`: Budget Neutrality Rate.
  - `PPS-PC-DATA`: PPS PC Data.
    - `PPS-COT-IND`: COT Indicator.
- `PRICER-OPT-VERS-SW`: Pricer Option Version Switch:
  - `PRICER-OPTION-SW`: Option Switch.
  - `ALL-TABLES-PASSED`: Value 'A'.
  - `PROV-RECORD-PASSED`: Value 'P'.
  - `PPS-VERSIONS`: PPS Versions.
    - `PPDRV-VERSION`: PPDRV Version.
- `PROV-NEW-HOLD`: Provider Record.
  - `PROV-NEWREC-HOLD1`: Provider Record Hold 1.
    - `P-NEW-NPI10`: NPI.
      - `P-NEW-NPI8`: NPI (8 characters).
      - `P-NEW-NPI-FILLER`: NPI Filler (2 characters).
    - `P-NEW-PROVIDER-NO`: Provider Number.
    - `P-NEW-DATE-DATA`: Date Data.
      - `P-NEW-EFF-DATE`: Effective Date.
        - `P-NEW-EFF-DT-CC`: Century.
        - `P-NEW-EFF-DT-YY`: Year.
        - `P-NEW-EFF-DT-MM`: Month.
        - `P-NEW-EFF-DT-DD`: Day.
      - `P-NEW-FY-BEGIN-DATE`: Fiscal Year Begin Date.
        - `P-NEW-FY-BEG-DT-CC`: Century.
        - `P-NEW-FY-BEG-DT-YY`: Year.
        - `P-NEW-FY-BEG-DT-MM`: Month.
        - `P-NEW-FY-BEG-DT-DD`: Day.
      - `P-NEW-REPORT-DATE`: Report Date.
        - `P-NEW-REPORT-DT-CC`: Century.
        - `P-NEW-REPORT-DT-YY`: Year.
        - `P-NEW-REPORT-DT-MM`: Month.
        - `P-NEW-REPORT-DT-DD`: Day.
      - `P-NEW-TERMINATION-DATE`: Termination Date.
        - `P-NEW-TERM-DT-CC`: Century.
        - `P-NEW-TERM-DT-YY`: Year.
        - `P-NEW-TERM-DT-MM`: Month.
        - `P-NEW-TERM-DT-DD`: Day.
    - `P-NEW-WAIVER-CODE`: Waiver Code.
      - `P-NEW-WAIVER-STATE`: Value 'Y'.
    - `P-NEW-INTER-NO`: Intern Number.
    - `P-NEW-PROVIDER-TYPE`: Provider Type.
    - `P-NEW-CURRENT-CENSUS-DIV`: Current Census Division.
    - `P-NEW-MSA-DATA`: MSA Data.
      - `P-NEW-CHG-CODE-INDEX`: Charge Code Index.
      - `P-NEW-GEO-LOC-MSAX`: Geo Location MSA.
      - `P-NEW-GEO-LOC-MSA9`: Geo Location MSA (numeric).
      - `P-NEW-WAGE-INDEX-LOC-MSA`: Wage Index Location MSA.
      - `P-NEW-STAND-AMT-LOC-MSA`: Standard Amount Location MSA.
      - `P-NEW-STAND-AMT-LOC-MSA9`: Standard Amount Location MSA (numeric).
        - `P-NEW-RURAL-1ST`: Rural 1st.
          - `P-NEW-STAND-RURAL`: Standard Rural.
            - `P-NEW-STD-RURAL-CHECK`: Value '  '.
          - `P-NEW-RURAL-2ND`: Rural 2nd.
    - `P-NEW-SOL-COM-DEP-HOSP-YR`: SOL COM DEP HOSP YR.
    - `P-NEW-LUGAR`: Lugar.
    - `P-NEW-TEMP-RELIEF-IND`: Temporary Relief Indicator.
    - `P-NEW-FED-PPS-BLEND-IND`: Federal PPS Blend Indicator.
  - `PROV-NEWREC-HOLD2`: Provider Record Hold 2.
    - `P-NEW-VARIABLES`: Variables.
      - `P-NEW-FAC-SPEC-RATE`: Facility Specific Rate.
      - `P-NEW-COLA`: COLA.
      - `P-NEW-INTERN-RATIO`: Intern Ratio.
      - `P-NEW-BED-SIZE`: Bed Size.
      - `P-NEW-OPER-CSTCHG-RATIO`: Operating Cost to Charge Ratio.
      - `P-NEW-CMI`: CMI.
      - `P-NEW-SSI-RATIO`: SSI Ratio.
      - `P-NEW-MEDICAID-RATIO`: Medicaid Ratio.
      - `P-NEW-PPS-BLEND-YR-IND`: PPS Blend Year Indicator.
      - `P-NEW-PRUF-UPDTE-FACTOR`: PRUF Update Factor.
      - `P-NEW-DSH-PERCENT`: DSH Percent.
      - `P-NEW-FYE-DATE`: FYE Date.
  - `PROV-NEWREC-HOLD3`: Provider Record Hold 3.
    - `P-NEW-PASS-AMT-DATA`: Pass Amount Data.
      - `P-NEW-PASS-AMT-CAPITAL`: Pass Amount Capital.
      - `P-NEW-PASS-AMT-DIR-MED-ED`: Pass Amount Direct Medical Education.
      - `P-NEW-PASS-AMT-ORGAN-ACQ`: Pass Amount Organ Acquisition.
      - `P-NEW-PASS-AMT-PLUS-MISC`: Pass Amount Plus Misc.
    - `P-NEW-CAPI-DATA`: Capital Data.
      - `P-NEW-CAPI-PPS-PAY-CODE`: Capital PPS Pay Code.
      - `P-NEW-CAPI-HOSP-SPEC-RATE`: Capital Hospital Specific Rate.
      - `P-NEW-CAPI-OLD-HARM-RATE`: Capital Old Harm Rate.
      - `P-NEW-CAPI-NEW-HARM-RATIO`: Capital New Harm Ratio.
      - `P-NEW-CAPI-CSTCHG-RATIO`: Capital Cost to Charge Ratio.
      - `P-NEW-CAPI-NEW-HOSP`: Capital New Hospital.
      - `P-NEW-CAPI-IME`: Capital IME.
      - `P-NEW-CAPI-EXCEPTIONS`: Capital Exceptions.
- `WAGE-NEW-INDEX-RECORD`: Wage Index Record.
  - `W-MSA`: MSA.
  - `W-EFF-DATE`: Effective Date.
  - `W-WAGE-INDEX1`: Wage Index 1.
  - `W-WAGE-INDEX2`: Wage Index 2.
  - `W-WAGE-INDEX3`: Wage Index 3.

### Business Rules
- The program calculates payments based on the DRG system and considers factors like length of stay, covered charges, and provider-specific information.
- The program uses a Return Code (`PPS-RTC`) to indicate the payment method and any errors encountered during processing.
- The program incorporates blend payment methodologies based on the `PPS-BLEND-YEAR` and applies outlier payments if applicable.
- Data validation is performed to ensure the integrity of the input data.

### Data validation and error handling logic

- **0100-INITIAL-ROUTINE:**
  - Initializes `PPS-RTC` to zero.
  - Initializes several working storage areas: `PPS-DATA`, `PPS-OTHER-DATA`, and `HOLD-PPS-COMPONENTS`.
  - Sets initial values for constants: `PPS-NAT-LABOR-PCT`, `PPS-NAT-NONLABOR-PCT`, `PPS-STD-FED-RATE`, `H-FIXED-LOSS-AMT`, and `PPS-BDGT-NEUT-RATE`.
- **1000-EDIT-THE-BILL-INFO:**
  - Validates `B-LOS`:
    - If `B-LOS` is not numeric or is less than or equal to zero, sets `PPS-RTC` to 56.
  - Checks for `P-NEW-WAIVER-STATE`:
    - If `P-NEW-WAIVER-STATE` is true, sets `PPS-RTC` to 53.
  - Validates `B-DISCHARGE-DATE` against `P-NEW-EFF-DATE` and `W-EFF-DATE`:
    - If `B-DISCHARGE-DATE` is earlier than either effective date, sets `PPS-RTC` to 55.
  - Checks for `P-NEW-TERMINATION-DATE`:
    - If a termination date exists and `B-DISCHARGE-DATE` is on or after the termination date, sets `PPS-RTC` to 51.
  - Validates `B-COV-CHARGES`:
    - If `B-COV-CHARGES` is not numeric, sets `PPS-RTC` to 58.
  - Validates `B-LTR-DAYS`:
    - If `B-LTR-DAYS` is not numeric or greater than 60, sets `PPS-RTC` to 61.
  - Validates `B-COV-DAYS`:
    - If `B-COV-DAYS` is not numeric, or if `B-COV-DAYS` is zero and `H-LOS` is greater than zero, sets `PPS-RTC` to 62.
  - Validates `B-LTR-DAYS` against `B-COV-DAYS`:
    - If `B-LTR-DAYS` is greater than `B-COV-DAYS`, sets `PPS-RTC` to 62.
  - Calculates intermediate values: `H-REG-DAYS` and `H-TOTAL-DAYS`.
  - Calls `1200-DAYS-USED`.
- **1200-DAYS-USED:**
  - Calculates `PPS-LTR-DAYS-USED` and `PPS-REG-DAYS-USED` based on `B-LTR-DAYS`, `H-REG-DAYS`, and `H-LOS`.
- **1700-EDIT-DRG-CODE:**
  - Moves `B-DRG-CODE` to `PPS-SUBM-DRG-CODE`.
  - Searches the `WWM-ENTRY` table (from the `LTDRG031` copybook) for a matching `WWM-DRG` code.
    - If no match is found, sets `PPS-RTC` to 54.
    - If a match is found, calls `1750-FIND-VALUE`.
- **1750-FIND-VALUE:**
  - Moves `WWM-RELWT` and `WWM-ALOS` (from the `LTDRG031` copybook) to `PPS-RELATIVE-WGT` and `PPS-AVG-LOS` respectively.
- **2000-ASSEMBLE-PPS-VARIABLES:**
  - Validates `W-WAGE-INDEX1`:
    - If `W-WAGE-INDEX1` is numeric and greater than 0, move it to `PPS-WAGE-INDEX`.
    - Otherwise, sets `PPS-RTC` to 52.
  - Validates `P-NEW-OPER-CSTCHG-RATIO`:
    - If `P-NEW-OPER-CSTCHG-RATIO` is not numeric, sets `PPS-RTC` to 65.
  - Validates `PPS-BLEND-YEAR`:
    - If `PPS-BLEND-YEAR` is not between 1 and 5 (inclusive), sets `PPS-RTC` to 72.
  - Calculates blend percentages based on `PPS-BLEND-YEAR`.
- **3000-CALC-PAYMENT:**
  - Moves `P-NEW-COLA` to `PPS-COLA`.
  - Computes `PPS-FAC-COSTS`.
  - Computes `H-LABOR-PORTION`.
  - Computes `H-NONLABOR-PORTION`.
  - Computes `PPS-FED-PAY-AMT`.
  - Computes `PPS-DRG-ADJ-PAY-AMT`.
  - Computes `H-SSOT`.
  - Calls `3400-SHORT-STAY` if `H-LOS` is less than or equal to `H-SSOT`.
- **3400-SHORT-STAY:**
  - Computes `H-SS-COST`.
  - Computes `H-SS-PAY-AMT`.
  - Compares `H-SS-COST`, `H-SS-PAY-AMT`, and `PPS-DRG-ADJ-PAY-AMT` to determine the short stay payment amount and sets `PPS-RTC` to 02 if a short stay payment is applicable.
- **7000-CALC-OUTLIER:**
  - Computes `PPS-OUTLIER-THRESHOLD`.
  - Computes `PPS-OUTLIER-PAY-AMT` if `PPS-FAC-COSTS` is greater than `PPS-OUTLIER-THRESHOLD`.
  - If `B-SPEC-PAY-IND` is '1', sets `PPS-OUTLIER-PAY-AMT` to 0.
  - Adjusts `PPS-RTC` to indicate outlier payment.
  - If `PPS-RTC` is 00 or 02 and `PPS-REG-DAYS-USED` is greater than `H-SSOT`, sets `PPS-LTR-DAYS-USED` to 0.
  - If `PPS-RTC` is 01 or 03 and certain conditions are met, sets `PPS-RTC` to 67.
- **8000-BLEND:**
  - Computes `PPS-DRG-ADJ-PAY-AMT`.
  - Computes `PPS-NEW-FAC-SPEC-RATE`.
  - Computes `PPS-FINAL-PAY-AMT`.
  - Adds `H-BLEND-RTC` to `PPS-RTC`.
- **9000-MOVE-RESULTS:**
  - If `PPS-RTC` is less than 50, moves `H-LOS` to `PPS-LOS` and sets `PPS-CALC-VERS-CD` to 'V03.2'.
  - If `PPS-RTC` is greater than or equal to 50, initializes `PPS-DATA` and `PPS-OTHER-DATA` and sets `PPS-CALC-VERS-CD` to 'V03.2'.

### Execution Flow
- **0000-MAINLINE-CONTROL:**
  - Calls `0100-INITIAL-ROUTINE`.
  - Calls `1000-EDIT-THE-BILL-INFO`.
  - If `PPS-RTC` is 00, calls `1700-EDIT-DRG-CODE`.
  - If `PPS-RTC` is 00, calls `2000-ASSEMBLE-PPS-VARIABLES`.
  - If `PPS-RTC` is 00, calls `3000-CALC-PAYMENT` and `7000-CALC-OUTLIER`.
  - If `PPS-RTC` is less than 50, calls `8000-BLEND`.
  - Calls `9000-MOVE-RESULTS`.
  - `GOBACK`.

## LTDRG031 (COPY)

### Overview
- This is a copybook containing DRG-related data for the year 2003, effective January 1, 2003.
- It defines the structure and data for DRG codes, relative weights, and average lengths of stay.
- It is used by LTCAL032 to look up DRG information.

### Definitions
- `WWM-ENTRY`: A table containing DRG information.
  - `WWM-INDX`: Index for the table.
  - `WWM-DRG`: DRG Code.
  - `WWM-RELWT`: Relative Weight.
  - `WWM-ALOS`: Average Length of Stay.

### Business Rules
- Contains the DRG codes and associated data used for payment calculations.

### Data validation and error handling logic
- None within the copybook itself. The data is assumed to be validated when it is created or updated.

# Step 2: LTCAL042 Analysis

## LTCAL042

### Overview
- This COBOL program, LTCAL042, is a modified version of LTCAL032.
- It calculates Long-Term Care (LTC) payments based on the Diagnosis Related Group (DRG) system.
- It receives bill data and provider information as input, performs edits, looks up DRG information, calculates payment amounts, and returns the results.
- The program uses a copybook `LTDRG031` for DRG-related data.
- It also uses the provider and wage index records to calculate the payment.
- This version has an additional provider-specific logic for short stay calculations for provider number 332006.

### Definitions
- The definitions are the same as in LTCAL032, with the following additions/changes:
  - `CAL-VERSION`: Value is 'C04.2'.
  - `H-LOS-RATIO`: Length of Stay Ratio.
  - The logic in `2000-ASSEMBLE-PPS-VARIABLES` to determine the wage index has been updated to check for fiscal year begin date and discharge date.
  - An additional paragraph `4000-SPECIAL-PROVIDER` is used to calculate the short stay payment for provider number 332006.

### Business Rules
- The business rules are the same as in LTCAL032, with the following addition:
  - Provider-specific logic is applied for provider number 332006, modifying the short stay calculations based on the discharge date.

### Data validation and error handling logic

- The data validation and error handling logic are the same as in LTCAL032, with the following changes:
  - In `1000-EDIT-THE-BILL-INFO`:
    - Added a check for `P-NEW-COLA` (COLA) to ensure it is numeric, setting `PPS-RTC` to 50 if not.
  - In `2000-ASSEMBLE-PPS-VARIABLES`:
    - The wage index is determined based on the fiscal year begin date and discharge date. If the discharge date is on or after 2003-10-01 and the fiscal year begin date is also on or after 2003-10-01, it uses `W-WAGE-INDEX2`, otherwise, it uses `W-WAGE-INDEX1`.
  - In `3400-SHORT-STAY`:
    - Added logic to call `4000-SPECIAL-PROVIDER` if `P-NEW-PROVIDER-NO` equals '332006'.
  - **4000-SPECIAL-PROVIDER:**
    - This new paragraph calculates short-stay costs and payment amounts based on the `B-DISCHARGE-DATE`.
      - If `B-DISCHARGE-DATE` is between 20030701 and 20040101, it uses a factor of 1.95.
      - If `B-DISCHARGE-DATE` is between 20040101 and 20050101, it uses a factor of 1.93.
  - In `8000-BLEND`:
    - Calculates `H-LOS-RATIO` (Length of Stay Ratio) and limits it to a maximum of 1.
    - Uses `H-LOS-RATIO` in the calculation of `PPS-NEW-FAC-SPEC-RATE`.

### Execution Flow
- **0000-MAINLINE-CONTROL:**
  - Calls `0100-INITIAL-ROUTINE`.
  - Calls `1000-EDIT-THE-BILL-INFO`.
  - If `PPS-RTC` is 00, calls `1700-EDIT-DRG-CODE`.
  - If `PPS-RTC` is 00, calls `2000-ASSEMBLE-PPS-VARIABLES`.
  - If `PPS-RTC` is 00, calls `3000-CALC-PAYMENT` and `7000-CALC-OUTLIER`.
  - If `PPS-RTC` is less than 50, calls `8000-BLEND`.
  - Calls `9000-MOVE-RESULTS`.
  - `GOBACK`.

## LTDRG031 (COPY)

### Overview, Definitions, Business Rules, Data validation and error handling logic
- Same as in LTCAL032.
