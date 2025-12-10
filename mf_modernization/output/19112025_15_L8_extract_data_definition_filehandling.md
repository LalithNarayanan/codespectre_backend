# Step 1: Program Overview

## Program: LTCAL032

### Overview
- This program calculates Long-Term Care (LTC) payments based on the DRG (Diagnosis Related Group) code and other patient and provider data. It is a subroutine called by another program to determine the appropriate payment amount.

### Business Functions
- Calculates PPS (Prospective Payment System) payments for LTC facilities.
- Edits input data for validity.
- Determines if a short-stay or outlier payment applies.
- Applies blending rules based on the facility's blend year.

### Data Structures
- `BILL-NEW-DATA` (LINKAGE SECTION): Contains input data passed from the calling program, including patient and billing information.
- `PPS-DATA-ALL` (LINKAGE SECTION): Contains output data, including the calculated payment amounts, return codes, and other PPS related information, and versions of the calling programs.
- `PROV-NEW-HOLD` (LINKAGE SECTION): Contains provider-specific data.
- `WAGE-NEW-INDEX-RECORD` (LINKAGE SECTION): Contains wage index data.
- `HOLD-PPS-COMPONENTS` (WORKING-STORAGE SECTION):  Intermediate variables used for calculations.
- `W-STORAGE-REF` (WORKING-STORAGE SECTION): A reference string for identifying the working storage area.
- `CAL-VERSION` (WORKING-STORAGE SECTION): Program version.
- `LTDRG031` (COPY):  Contains DRG-related data (relative weights, average length of stay), included via a COPY statement.

### Execution Order
- 0100-INITIAL-ROUTINE: Initializes variables and sets constants.
- 1000-EDIT-THE-BILL-INFO: Edits the input bill data.
- 1700-EDIT-DRG-CODE: Finds the DRG code in the DRG table.
- 2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables based on provider and wage index data.
- 3000-CALC-PAYMENT: Calculates the standard payment amount. Calls 3400-SHORT-STAY if applicable.
- 7000-CALC-OUTLIER: Calculates outlier payments.
- 8000-BLEND: Applies blending rules.
- 9000-MOVE-RESULTS: Moves the final results to the output area.

### Rules
- `PPS-RTC`:  Return Code values that indicate the outcome of the calculation (success, type of payment, or error).
- Edits are performed to ensure the data is valid before calculations.
- Short-stay and outlier payments are calculated based on specific conditions.
- Blending rules are applied based on the facility's blend year.

### External System Interactions
- None. This program is a subroutine.

## Program: LTCAL042

### Overview
- This program calculates Long-Term Care (LTC) payments based on the DRG (Diagnosis Related Group) code and other patient and provider data. It is a subroutine called by another program to determine the appropriate payment amount. This is a modified version of LTCAL032.

### Business Functions
- Calculates PPS (Prospective Payment System) payments for LTC facilities.
- Edits input data for validity.
- Determines if a short-stay or outlier payment applies.
- Applies blending rules based on the facility's blend year.
- Includes special logic for a specific provider.

### Data Structures
- `BILL-NEW-DATA` (LINKAGE SECTION): Contains input data passed from the calling program, including patient and billing information.
- `PPS-DATA-ALL` (LINKAGE SECTION): Contains output data, including the calculated payment amounts, return codes, and other PPS related information, and versions of the calling programs.
- `PROV-NEW-HOLD` (LINKAGE SECTION): Contains provider-specific data.
- `WAGE-NEW-INDEX-RECORD` (LINKAGE SECTION): Contains wage index data.
- `HOLD-PPS-COMPONENTS` (WORKING-STORAGE SECTION):  Intermediate variables used for calculations.
- `W-STORAGE-REF` (WORKING-STORAGE SECTION): A reference string for identifying the working storage area.
- `CAL-VERSION` (WORKING-STORAGE SECTION): Program version.
- `LTDRG031` (COPY):  Contains DRG-related data (relative weights, average length of stay), included via a COPY statement.
- `H-LOS-RATIO` (WORKING-STORAGE SECTION): Ratio of length of stay to average length of stay.

### Execution Order
- 0100-INITIAL-ROUTINE: Initializes variables and sets constants.
- 1000-EDIT-THE-BILL-INFO: Edits the input bill data.
- 1700-EDIT-DRG-CODE: Finds the DRG code in the DRG table.
- 2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables based on provider and wage index data.
- 3000-CALC-PAYMENT: Calculates the standard payment amount. Calls 3400-SHORT-STAY if applicable.
- 3400-SHORT-STAY: Calculates short stay payment. Calls 4000-SPECIAL-PROVIDER if provider is 332006.
- 4000-SPECIAL-PROVIDER: Special logic for provider 332006
- 7000-CALC-OUTLIER: Calculates outlier payments.
- 8000-BLEND: Applies blending rules.
- 9000-MOVE-RESULTS: Moves the final results to the output area.

### Rules
- `PPS-RTC`:  Return Code values that indicate the outcome of the calculation (success, type of payment, or error).
- Edits are performed to ensure the data is valid before calculations.
- Short-stay and outlier payments are calculated based on specific conditions.
- Blending rules are applied based on the facility's blend year.
- Special logic is applied for provider 332006.

### External System Interactions
- None. This program is a subroutine.

## Program: LTDRG031

### Overview
- This is a copybook (included via `COPY` statements in other programs) that contains DRG (Diagnosis Related Group) data used for calculating payments. It essentially acts as a lookup table.

### Business Functions
- Provides DRG-specific information for payment calculations.

### Data Structures
- `W-DRG-FILLS` (WORKING-STORAGE SECTION): Contains a series of strings, each holding data for multiple DRG entries.
- `W-DRG-TABLE` (WORKING-STORAGE SECTION):  A redefined structure that parses the data in `W-DRG-FILLS` into individual DRG entries.
   - `WWM-ENTRY` (OCCURS 502 TIMES):  An array of DRG entries.
      - `WWM-DRG`:  The DRG code (3 characters).
      - `WWM-RELWT`: The relative weight for the DRG (PIC 9(1)V9(4)).
      - `WWM-ALOS`: The average length of stay for the DRG (PIC 9(2)V9(1)).

### Execution Order
- Data is accessed via the `SEARCH ALL` statement in the calling programs.

### Rules
- The data is structured to be easily searched by DRG code.

### External System Interactions
- None. This is a data definition.

# Step 2: Data Definition and File Handling

## Program: LTCAL032

### Files Accessed
- None. This program is a subroutine and does not directly access any files. It uses a `COPY` statement to include `LTDRG031`, which contains DRG data.

### Data Structures in WORKING-STORAGE SECTION
- `W-STORAGE-REF`
  - Description: A 46-character string used to identify the working storage area.
  - Attributes: `PIC X(46)`
  - Value: `'LTCAL032      - W O R K I N G   S T O R A G E'`
- `CAL-VERSION`
  - Description: Stores the version of the calculation program.
  - Attributes: `PIC X(05)`
  - Value: `'C03.2'`
- `HOLD-PPS-COMPONENTS`
  - Description: Contains intermediate values used during the PPS calculation.
  - Attributes: Group item.
    - `H-LOS`: Length of Stay (3 digits)
      - Attributes: `PIC 9(03)`
    - `H-REG-DAYS`: Regular Days (3 digits)
      - Attributes: `PIC 9(03)`
    - `H-TOTAL-DAYS`: Total Days (5 digits)
      - Attributes: `PIC 9(05)`
    - `H-SSOT`:  Short Stay Outlier Threshold (2 digits)
      - Attributes: `PIC 9(02)`
    - `H-BLEND-RTC`: Blend Return Code (2 digits)
      - Attributes: `PIC 9(02)`
    - `H-BLEND-FAC`: Blend Facility Factor (1 digit, 1 decimal)
      - Attributes: `PIC 9(01)V9(01)`
    - `H-BLEND-PPS`: Blend PPS Factor (1 digit, 1 decimal)
      - Attributes: `PIC 9(01)V9(01)`
    - `H-SS-PAY-AMT`: Short Stay Payment Amount (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-SS-COST`: Short Stay Cost (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-LABOR-PORTION`: Labor Portion (7 digits, 6 decimals)
      - Attributes: `PIC 9(07)V9(06)`
    - `H-NONLABOR-PORTION`: Non-Labor Portion (7 digits, 6 decimals)
      - Attributes: `PIC 9(07)V9(06)`
    - `H-FIXED-LOSS-AMT`: Fixed Loss Amount (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-NEW-FAC-SPEC-RATE`: New Facility Specific Rate (5 digits, 2 decimals)
      - Attributes: `PIC 9(05)V9(02)`

### Data Structures in LINKAGE SECTION
- `BILL-NEW-DATA`
  - Description:  Contains the input bill data passed from the calling program.
  - Attributes:  Group item.
    - `B-NPI10`
      - Description:  NPI (National Provider Identifier)
      - Attributes: Group item.
        - `B-NPI8`: NPI (8 characters)
          - Attributes: `PIC X(08)`
        - `B-NPI-FILLER`: NPI Filler (2 characters)
          - Attributes: `PIC X(02)`
    - `B-PROVIDER-NO`: Provider Number (6 characters)
      - Attributes: `PIC X(06)`
    - `B-PATIENT-STATUS`: Patient Status (2 characters)
      - Attributes: `PIC X(02)`
    - `B-DRG-CODE`: DRG Code (3 characters)
      - Attributes: `PIC X(03)`
    - `B-LOS`: Length of Stay (3 digits)
      - Attributes: `PIC 9(03)`
    - `B-COV-DAYS`: Covered Days (3 digits)
      - Attributes: `PIC 9(03)`
    - `B-LTR-DAYS`: Lifetime Reserve Days (2 digits)
      - Attributes: `PIC 9(02)`
    - `B-DISCHARGE-DATE`
      - Description: Discharge Date
      - Attributes: Group item.
        - `B-DISCHG-CC`: Century code for discharge date (2 digits)
          - Attributes: `PIC 9(02)`
        - `B-DISCHG-YY`: Year of discharge date (2 digits)
          - Attributes: `PIC 9(02)`
        - `B-DISCHG-MM`: Month of discharge date (2 digits)
          - Attributes: `PIC 9(02)`
        - `B-DISCHG-DD`: Day of discharge date (2 digits)
          - Attributes: `PIC 9(02)`
    - `B-COV-CHARGES`: Covered Charges (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `B-SPEC-PAY-IND`: Special Payment Indicator (1 character)
      - Attributes: `PIC X(01)`
    - `FILLER`: Filler (13 characters)
      - Attributes: `PIC X(13)`
- `PPS-DATA-ALL`
  - Description: Contains the calculated PPS data to be returned to the calling program.
  - Attributes: Group item.
    - `PPS-RTC`: Return Code (2 digits)
      - Attributes: `PIC 9(02)`
    - `PPS-CHRG-THRESHOLD`: Charge Threshold (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `PPS-DATA`
      - Description: PPS Data
      - Attributes: Group item.
        - `PPS-MSA`: MSA (Metropolitan Statistical Area) Code (4 characters)
          - Attributes: `PIC X(04)`
        - `PPS-WAGE-INDEX`: Wage Index (2 digits, 4 decimals)
          - Attributes: `PIC 9(02)V9(04)`
        - `PPS-AVG-LOS`: Average Length of Stay (2 digits, 1 decimal)
          - Attributes: `PIC 9(02)V9(01)`
        - `PPS-RELATIVE-WGT`: Relative Weight (1 digit, 4 decimals)
          - Attributes: `PIC 9(01)V9(04)`
        - `PPS-OUTLIER-PAY-AMT`: Outlier Payment Amount (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-LOS`: Length of Stay (3 digits)
          - Attributes: `PIC 9(03)`
        - `PPS-DRG-ADJ-PAY-AMT`: DRG Adjusted Payment Amount (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-FED-PAY-AMT`: Federal Payment Amount (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-FINAL-PAY-AMT`: Final Payment Amount (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-FAC-COSTS`: Facility Costs (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-NEW-FAC-SPEC-RATE`: New Facility Specific Rate (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-OUTLIER-THRESHOLD`: Outlier Threshold (7 digits, 2 decimals)
          - Attributes: `PIC 9(07)V9(02)`
        - `PPS-SUBM-DRG-CODE`: Submitted DRG Code (3 characters)
          - Attributes: `PIC X(03)`
        - `PPS-CALC-VERS-CD`: Calculation Version Code (5 characters)
          - Attributes: `PIC X(05)`
        - `PPS-REG-DAYS-USED`: Regular Days Used (3 digits)
          - Attributes: `PIC 9(03)`
        - `PPS-LTR-DAYS-USED`: Lifetime Reserve Days Used (3 digits)
          - Attributes: `PIC 9(03)`
        - `PPS-BLEND-YEAR`: Blend Year (1 digit)
          - Attributes: `PIC 9(01)`
        - `PPS-COLA`: COLA (Cost of Living Adjustment) (1 digit, 3 decimals)
          - Attributes: `PIC 9(01)V9(03)`
        - `FILLER`: Filler (4 characters)
          - Attributes: `PIC X(04)`
    - `PPS-OTHER-DATA`
      - Description: Other PPS Data
      - Attributes: Group item.
        - `PPS-NAT-LABOR-PCT`: National Labor Percentage (1 digit, 5 decimals)
          - Attributes: `PIC 9(01)V9(05)`
        - `PPS-NAT-NONLABOR-PCT`: National Non-Labor Percentage (1 digit, 5 decimals)
          - Attributes: `PIC 9(01)V9(05)`
        - `PPS-STD-FED-RATE`: Standard Federal Rate (5 digits, 2 decimals)
          - Attributes: `PIC 9(05)V9(02)`
        - `PPS-BDGT-NEUT-RATE`: Budget Neutrality Rate (1 digit, 3 decimals)
          - Attributes: `PIC 9(01)V9(03)`
        - `FILLER`: Filler (20 characters)
          - Attributes: `PIC X(20)`
    - `PPS-PC-DATA`
      - Description: PPS PC Data
      - Attributes: Group item.
        - `PPS-COT-IND`: COT (Cost of Therapy) Indicator (1 character)
          - Attributes: `PIC X(01)`
        - `FILLER`: Filler (20 characters)
          - Attributes: `PIC X(20)`
- `PRICER-OPT-VERS-SW`
  - Description: Pricer Option and Version Switch
  - Attributes: Group item.
    - `PRICER-OPTION-SW`: Pricer Option Switch (1 character)
      - Attributes: `PIC X(01)`
      - `ALL-TABLES-PASSED`: Value 'A'
        - Attributes: `VALUE 'A'`
      - `PROV-RECORD-PASSED`: Value 'P'
        - Attributes: `VALUE 'P'`
    - `PPS-VERSIONS`
      - Description: PPS Versions
      - Attributes: Group item.
        - `PPDRV-VERSION`:  PPDRV Version (5 characters)
          - Attributes: `PIC X(05)`
- `PROV-NEW-HOLD`
  - Description:  Contains provider-specific information.
  - Attributes:  Group item.
    - `PROV-NEWREC-HOLD1`
      - Description: Provider record hold area 1
      - Attributes: Group item
        - `P-NEW-NPI10`
          - Description: NPI
          - Attributes: Group item
            - `P-NEW-NPI8`: NPI (8 characters)
              - Attributes: `PIC X(08)`
            - `P-NEW-NPI-FILLER`: NPI Filler (2 characters)
              - Attributes: `PIC X(02)`
        - `P-NEW-PROVIDER-NO`
          - Description: Provider Number
          - Attributes: Group item
            - `P-NEW-STATE`: State code
              - Attributes: `PIC 9(02)`
            - `FILLER`: Filler (4 characters)
              - Attributes: `PIC X(04)`
        - `P-NEW-DATE-DATA`
          - Description: Date Data
          - Attributes: Group item
            - `P-NEW-EFF-DATE`
              - Description: Effective Date
              - Attributes: Group item
                - `P-NEW-EFF-DT-CC`: Century of effective date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-EFF-DT-YY`: Year of effective date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-EFF-DT-MM`: Month of effective date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-EFF-DT-DD`: Day of effective date
                  - Attributes: `PIC 9(02)`
            - `P-NEW-FY-BEGIN-DATE`
              - Description: Fiscal Year Begin Date
              - Attributes: Group item
                - `P-NEW-FY-BEG-DT-CC`: Century of FY begin date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-FY-BEG-DT-YY`: Year of FY begin date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-FY-BEG-DT-MM`: Month of FY begin date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-FY-BEG-DT-DD`: Day of FY begin date
                  - Attributes: `PIC 9(02)`
            - `P-NEW-REPORT-DATE`
              - Description: Report Date
              - Attributes: Group item
                - `P-NEW-REPORT-DT-CC`: Century of report date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-REPORT-DT-YY`: Year of report date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-REPORT-DT-MM`: Month of report date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-REPORT-DT-DD`: Day of report date
                  - Attributes: `PIC 9(02)`
            - `P-NEW-TERMINATION-DATE`
              - Description: Termination Date
              - Attributes: Group item
                - `P-NEW-TERM-DT-CC`: Century of Termination Date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-TERM-DT-YY`: Year of Termination Date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-TERM-DT-MM`: Month of Termination Date
                  - Attributes: `PIC 9(02)`
                - `P-NEW-TERM-DT-DD`: Day of Termination Date
                  - Attributes: `PIC 9(02)`
        - `P-NEW-WAIVER-CODE`: Waiver Code (1 character)
          - Attributes: `PIC X(01)`
          - `P-NEW-WAIVER-STATE`: Value 'Y'
            - Attributes: `VALUE 'Y'`
        - `P-NEW-INTER-NO`: Intern Number (5 digits)
          - Attributes: `PIC 9(05)`
        - `P-NEW-PROVIDER-TYPE`: Provider Type (2 characters)
          - Attributes: `PIC X(02)`
        - `P-NEW-CURRENT-CENSUS-DIV`: Current Census Division (1 digit)
          - Attributes: `PIC 9(01)`
        - `P-NEW-CURRENT-DIV` REDEFINES P-NEW-CURRENT-CENSUS-DIV: (1 digit)
          - Attributes: `PIC 9(01)`
        - `P-NEW-MSA-DATA`
          - Description: MSA Data
          - Attributes: Group item
            - `P-NEW-CHG-CODE-INDEX`: Charge Code Index (1 character)
              - Attributes: `PIC X`
            - `P-NEW-GEO-LOC-MSAX`: Geo Location MSA X (4 characters)
              - Attributes: `PIC X(04) JUST RIGHT`
            - `P-NEW-GEO-LOC-MSA9` REDEFINES P-NEW-GEO-LOC-MSAX: Geo Location MSA9 (4 digits)
              - Attributes: `PIC 9(04)`
            - `P-NEW-WAGE-INDEX-LOC-MSA`: Wage Index Location MSA (4 characters)
              - Attributes: `PIC X(04) JUST RIGHT`
            - `P-NEW-STAND-AMT-LOC-MSA`: Standard Amount Location MSA (4 characters)
              - Attributes: `PIC X(04) JUST RIGHT`
            - `P-NEW-STAND-AMT-LOC-MSA9` REDEFINES P-NEW-STAND-AMT-LOC-MSA
              - Description: Standard Amount Location MSA9
              - Attributes: Group item
                - `P-NEW-RURAL-1ST`
                  - Description: Rural 1st
                  - Attributes: Group item
                    - `P-NEW-STAND-RURAL`: Stand Rural (2 characters)
                      - Attributes: `PIC XX`
                      - `P-NEW-STD-RURAL-CHECK`: Value '  '
                        - Attributes: `VALUE '  '`
                    - `P-NEW-RURAL-2ND`: Rural 2nd (2 characters)
                      - Attributes: `PIC XX`
        - `P-NEW-SOL-COM-DEP-HOSP-YR`: SOL COM DEP HOSP YR (2 characters)
          - Attributes: `PIC XX`
        - `P-NEW-LUGAR`: Lugar (1 character)
          - Attributes: `PIC X`
        - `P-NEW-TEMP-RELIEF-IND`: Temporary Relief Indicator (1 character)
          - Attributes: `PIC X`
        - `P-NEW-FED-PPS-BLEND-IND`: Federal PPS Blend Indicator (1 character)
          - Attributes: `PIC X`
        - `FILLER`: Filler (5 characters)
          - Attributes: `PIC X(05)`
    - `PROV-NEWREC-HOLD2`
      - Description: Provider record hold area 2
      - Attributes: Group item
        - `P-NEW-VARIABLES`
          - Description: Variables
          - Attributes: Group item
            - `P-NEW-FAC-SPEC-RATE`: Facility Specific Rate (5 digits, 2 decimals)
              - Attributes: `PIC  9(05)V9(02)`
            - `P-NEW-COLA`: COLA (1 digit, 3 decimals)
              - Attributes: `PIC  9(01)V9(03)`
            - `P-NEW-INTERN-RATIO`: Intern Ratio (1 digit, 4 decimals)
              - Attributes: `PIC  9(01)V9(04)`
            - `P-NEW-BED-SIZE`: Bed Size (5 digits)
              - Attributes: `PIC  9(05)`
            - `P-NEW-OPER-CSTCHG-RATIO`: Operating Cost to Charge Ratio (1 digit, 3 decimals)
              - Attributes: `PIC  9(01)V9(03)`
            - `P-NEW-CMI`: CMI (Case Mix Index) (1 digit, 4 decimals)
              - Attributes: `PIC  9(01)V9(04)`
            - `P-NEW-SSI-RATIO`: SSI Ratio (4 decimals)
              - Attributes: `PIC  V9(04)`
            - `P-NEW-MEDICAID-RATIO`: Medicaid Ratio (4 decimals)
              - Attributes: `PIC  V9(04)`
            - `P-NEW-PPS-BLEND-YR-IND`: PPS Blend Year Indicator (1 digit)
              - Attributes: `PIC  9(01)`
            - `P-NEW-PRUF-UPDTE-FACTOR`: PRUF Update Factor (1 digit, 5 decimals)
              - Attributes: `PIC  9(01)V9(05)`
            - `P-NEW-DSH-PERCENT`: DSH Percent (4 decimals)
              - Attributes: `PIC  V9(04)`
            - `P-NEW-FYE-DATE`: FYE Date (8 characters)
              - Attributes: `PIC  X(08)`
        - `FILLER`: Filler (23 characters)
          - Attributes: `PIC  X(23)`
    - `PROV-NEWREC-HOLD3`
      - Description: Provider record hold area 3
      - Attributes: Group item
        - `P-NEW-PASS-AMT-DATA`
          - Description: Pass Amount Data
          - Attributes: Group item
            - `P-NEW-PASS-AMT-CAPITAL`: Capital Pass Amount (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
            - `P-NEW-PASS-AMT-DIR-MED-ED`: Direct Medical Education Pass Amount (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
            - `P-NEW-PASS-AMT-ORGAN-ACQ`: Organ Acquisition Pass Amount (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
            - `P-NEW-PASS-AMT-PLUS-MISC`: Plus Misc Pass Amount (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
        - `P-NEW-CAPI-DATA`
          - Description: Capital Data
          - Attributes: Group item
            - `P-NEW-CAPI-PPS-PAY-CODE`: Capi PPS Pay Code (1 character)
              - Attributes: `PIC X`
            - `P-NEW-CAPI-HOSP-SPEC-RATE`: Capi Hospital Specific Rate (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
            - `P-NEW-CAPI-OLD-HARM-RATE`: Capi Old Harm Rate (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
            - `P-NEW-CAPI-NEW-HARM-RATIO`: Capi New Harm Ratio (1 digit, 4 decimals)
              - Attributes: `PIC 9(01)V9999`
            - `P-NEW-CAPI-CSTCHG-RATIO`: Capi Cost to Charge Ratio (3 decimals)
              - Attributes: `PIC 9V999`
            - `P-NEW-CAPI-NEW-HOSP`: Capi New Hosp (1 character)
              - Attributes: `PIC X`
            - `P-NEW-CAPI-IME`: Capi IME (Indirect Medical Education) (4 decimals)
              - Attributes: `PIC 9V9999`
            - `P-NEW-CAPI-EXCEPTIONS`: Capi Exceptions (4 digits, 2 decimals)
              - Attributes: `PIC 9(04)V99`
        - `FILLER`: Filler (22 characters)
          - Attributes: `PIC X(22)`
- `WAGE-NEW-INDEX-RECORD`
  - Description: Contains wage index data.
  - Attributes: Group item.
    - `W-MSA`: MSA (Metropolitan Statistical Area) Code (4 characters)
      - Attributes: `PIC X(4)`
    - `W-EFF-DATE`: Effective Date (8 characters)
      - Attributes: `PIC X(8)`
    - `W-WAGE-INDEX1`: Wage Index 1 (2 digits, 4 decimals)
      - Attributes: `PIC S9(02)V9(04)`
    - `W-WAGE-INDEX2`: Wage Index 2 (2 digits, 4 decimals)
      - Attributes: `PIC S9(02)V9(04)`
    - `W-WAGE-INDEX3`: Wage Index 3 (2 digits, 4 decimals)
      - Attributes: `PIC S9(02)V9(04)`

## Program: LTCAL042

### Files Accessed
- None. This program is a subroutine and does not directly access any files. It uses a `COPY` statement to include `LTDRG031`, which contains DRG data.

### Data Structures in WORKING-STORAGE SECTION
- `W-STORAGE-REF`
  - Description: A 46-character string used to identify the working storage area.
  - Attributes: `PIC X(46)`
  - Value: `'LTCAL042      - W O R K I N G   S T O R A G E'`
- `CAL-VERSION`
  - Description: Stores the version of the calculation program.
  - Attributes: `PIC X(05)`
  - Value: `'C04.2'`
- `HOLD-PPS-COMPONENTS`
  - Description: Contains intermediate values used during the PPS calculation.
  - Attributes: Group item.
    - `H-LOS`: Length of Stay (3 digits)
      - Attributes: `PIC 9(03)`
    - `H-REG-DAYS`: Regular Days (3 digits)
      - Attributes: `PIC 9(03)`
    - `H-TOTAL-DAYS`: Total Days (5 digits)
      - Attributes: `PIC 9(05)`
    - `H-SSOT`:  Short Stay Outlier Threshold (2 digits)
      - Attributes: `PIC 9(02)`
    - `H-BLEND-RTC`: Blend Return Code (2 digits)
      - Attributes: `PIC 9(02)`
    - `H-BLEND-FAC`: Blend Facility Factor (1 digit, 1 decimal)
      - Attributes: `PIC 9(01)V9(01)`
    - `H-BLEND-PPS`: Blend PPS Factor (1 digit, 1 decimal)
      - Attributes: `PIC 9(01)V9(01)`
    - `H-SS-PAY-AMT`: Short Stay Payment Amount (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-SS-COST`: Short Stay Cost (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-LABOR-PORTION`: Labor Portion (7 digits, 6 decimals)
      - Attributes: `PIC 9(07)V9(06)`
    - `H-NONLABOR-PORTION`: Non-Labor Portion (7 digits, 6 decimals)
      - Attributes: `PIC 9(07)V9(06)`
    - `H-FIXED-LOSS-AMT`: Fixed Loss Amount (7 digits, 2 decimals)
      - Attributes: `PIC 9(07)V9(02)`
    - `H-NEW-FAC-SPEC-RATE`: New Facility Specific Rate (5 digits, 2 decimals)
      - Attributes: `PIC 9(05)V9(02)`
    - `H-LOS-RATIO`: Length of stay ratio (1 digit, 5 decimals)
      - Attributes: `PIC 9(01)V9(05)`

### Data Structures in LINKAGE SECTION
- `BILL-NEW-DATA`
  - Description:  Contains the input bill data passed from the calling program.
  - Attributes:  Group item.
    - `B-NPI10`
      - Description:  NPI (National Provider Identifier)
      - Attributes: Group item.
        - `B-NPI8`: NPI (8 characters)
          - Attributes: `PIC X(08)`
        - `B-NPI-FILLER`: NPI Filler (2 characters)
          - Attributes: `PIC X(02)`
    - `B-PROVIDER-NO`: Provider Number (6 characters)
      - Attributes: `PIC X(06)`
    - `B-PATIENT-STATUS`: Patient Status (2 characters)
      - Attributes: `PIC X