# Step 1: Program Overview

## Program: LTCAL032

### Overview
This COBOL program, LTCAL032, is a subroutine designed to calculate the Long-Term Care (LTC) payment for a given bill. It receives bill data, provider information, and wage index data as input. It performs edits, assembles pricing components, calculates the payment amount, and determines if any outliers apply. It then returns the calculated payment information and a return code (PPS-RTC) indicating the payment method and any reasons for non-payment. The program utilizes a copybook `LTDRG031` which appears to contain DRG-related data. The program is effective for bills starting January 1, 2003.

### Business Functions
-   Calculates LTC payments based on DRG and other relevant data.
-   Applies payment methodologies, including normal DRG, short stay, and blend payments.
-   Calculates outlier payments.
-   Performs data validation and error handling.

### Programs Called and Data Structures Passed

-   **COPY LTDRG031**: Includes DRG information in a table.
    -   Data structure used: `W-DRG-TABLE` (defined within `LTDRG031`) containing `WWM-ENTRY` records.

-   **Called from**: The program is designed to be called by another program. The data structures are passed through the `LINKAGE SECTION`.

    -   `BILL-NEW-DATA`: Input bill data.
        -   `B-NPI10`
            -   `B-NPI8`
            -   `B-NPI-FILLER`
        -   `B-PROVIDER-NO`
        -   `B-PATIENT-STATUS`
        -   `B-DRG-CODE`
        -   `B-LOS`
        -   `B-COV-DAYS`
        -   `B-LTR-DAYS`
        -   `B-DISCHARGE-DATE`
            -   `B-DISCHG-CC`
            -   `B-DISCHG-YY`
            -   `B-DISCHG-MM`
            -   `B-DISCHG-DD`
        -   `B-COV-CHARGES`
        -   `B-SPEC-PAY-IND`
        -   `FILLER`
    -   `PPS-DATA-ALL`: Output payment data and related information.
        -   `PPS-RTC`
        -   `PPS-CHRG-THRESHOLD`
        -   `PPS-DATA`
            -   `PPS-MSA`
            -   `PPS-WAGE-INDEX`
            -   `PPS-AVG-LOS`
            -   `PPS-RELATIVE-WGT`
            -   `PPS-OUTLIER-PAY-AMT`
            -   `PPS-LOS`
            -   `PPS-DRG-ADJ-PAY-AMT`
            -   `PPS-FED-PAY-AMT`
            -   `PPS-FINAL-PAY-AMT`
            -   `PPS-FAC-COSTS`
            -   `PPS-NEW-FAC-SPEC-RATE`
            -   `PPS-OUTLIER-THRESHOLD`
            -   `PPS-SUBM-DRG-CODE`
            -   `PPS-CALC-VERS-CD`
            -   `PPS-REG-DAYS-USED`
            -   `PPS-LTR-DAYS-USED`
            -   `PPS-BLEND-YEAR`
            -   `PPS-COLA`
            -   `FILLER`
        -   `PPS-OTHER-DATA`
            -   `PPS-NAT-LABOR-PCT`
            -   `PPS-NAT-NONLABOR-PCT`
            -   `PPS-STD-FED-RATE`
            -   `PPS-BDGT-NEUT-RATE`
            -   `FILLER`
        -   `PPS-PC-DATA`
            -   `PPS-COT-IND`
            -   `FILLER`
    -   `PRICER-OPT-VERS-SW`: Option and version flags.
        -   `PRICER-OPTION-SW`
            -   `ALL-TABLES-PASSED`
            -   `PROV-RECORD-PASSED`
        -   `PPS-VERSIONS`
            -   `PPDRV-VERSION`
    -   `PROV-NEW-HOLD`: Provider-specific data.
        -   `PROV-NEWREC-HOLD1`
            -   `P-NEW-NPI10`
                -   `P-NEW-NPI8`
                -   `P-NEW-NPI-FILLER`
            -   `P-NEW-PROVIDER-NO`
                -   `P-NEW-STATE`
                -   `FILLER`
            -   `P-NEW-DATE-DATA`
                -   `P-NEW-EFF-DATE`
                    -   `P-NEW-EFF-DT-CC`
                    -   `P-NEW-EFF-DT-YY`
                    -   `P-NEW-EFF-DT-MM`
                    -   `P-NEW-EFF-DT-DD`
                -   `P-NEW-FY-BEGIN-DATE`
                    -   `P-NEW-FY-BEG-DT-CC`
                    -   `P-NEW-FY-BEG-DT-YY`
                    -   `P-NEW-FY-BEG-DT-MM`
                    -   `P-NEW-FY-BEG-DT-DD`
                -   `P-NEW-REPORT-DATE`
                    -   `P-NEW-REPORT-DT-CC`
                    -   `P-NEW-REPORT-DT-YY`
                    -   `P-NEW-REPORT-DT-MM`
                    -   `P-NEW-REPORT-DT-DD`
                -   `P-NEW-TERMINATION-DATE`
                    -   `P-NEW-TERM-DT-CC`
                    -   `P-NEW-TERM-DT-YY`
                    -   `P-NEW-TERM-DT-MM`
                    -   `P-NEW-TERM-DT-DD`
            -   `P-NEW-WAIVER-CODE`
                -   `P-NEW-WAIVER-STATE`
            -   `P-NEW-INTER-NO`
            -   `P-NEW-PROVIDER-TYPE`
            -   `P-NEW-CURRENT-CENSUS-DIV`
            -   `P-NEW-MSA-DATA`
                -   `P-NEW-CHG-CODE-INDEX`
                -   `P-NEW-GEO-LOC-MSAX`
                -   `P-NEW-GEO-LOC-MSA9`
                -   `P-NEW-WAGE-INDEX-LOC-MSA`
                -   `P-NEW-STAND-AMT-LOC-MSA`
                -   `P-NEW-STAND-AMT-LOC-MSA9`
                    -   `P-NEW-RURAL-1ST`
                        -   `P-NEW-STAND-RURAL`
                        -   `P-NEW-STD-RURAL-CHECK`
                    -   `P-NEW-RURAL-2ND`
            -   `P-NEW-SOL-COM-DEP-HOSP-YR`
            -   `P-NEW-LUGAR`
            -   `P-NEW-TEMP-RELIEF-IND`
            -   `P-NEW-FED-PPS-BLEND-IND`
            -   `FILLER`
        -   `PROV-NEWREC-HOLD2`
            -   `P-NEW-VARIABLES`
                -   `P-NEW-FAC-SPEC-RATE`
                -   `P-NEW-COLA`
                -   `P-NEW-INTERN-RATIO`
                -   `P-NEW-BED-SIZE`
                -   `P-NEW-OPER-CSTCHG-RATIO`
                -   `P-NEW-CMI`
                -   `P-NEW-SSI-RATIO`
                -   `P-NEW-MEDICAID-RATIO`
                -   `P-NEW-PPS-BLEND-YR-IND`
                -   `P-NEW-PRUF-UPDTE-FACTOR`
                -   `P-NEW-DSH-PERCENT`
                -   `P-NEW-FYE-DATE`
            -   `FILLER`
        -   `PROV-NEWREC-HOLD3`
            -   `P-NEW-PASS-AMT-DATA`
                -   `P-NEW-PASS-AMT-CAPITAL`
                -   `P-NEW-PASS-AMT-DIR-MED-ED`
                -   `P-NEW-PASS-AMT-ORGAN-ACQ`
                -   `P-NEW-PASS-AMT-PLUS-MISC`
            -   `P-NEW-CAPI-DATA`
                -   `P-NEW-CAPI-PPS-PAY-CODE`
                -   `P-NEW-CAPI-HOSP-SPEC-RATE`
                -   `P-NEW-CAPI-OLD-HARM-RATE`
                -   `P-NEW-CAPI-NEW-HARM-RATIO`
                -   `P-NEW-CAPI-CSTCHG-RATIO`
                -   `P-NEW-CAPI-NEW-HOSP`
                -   `P-NEW-CAPI-IME`
                -   `P-NEW-CAPI-EXCEPTIONS`
            -   `FILLER`
    -   `WAGE-NEW-INDEX-RECORD`: Wage index data.
        -   `W-MSA`
        -   `W-EFF-DATE`
        -   `W-WAGE-INDEX1`
        -   `W-WAGE-INDEX2`
        -   `W-WAGE-INDEX3`

## Program: LTCAL042

### Overview
This COBOL program, LTCAL042, is very similar to LTCAL032. It also calculates the Long-Term Care (LTC) payment for a given bill. It receives bill data, provider information, and wage index data as input. It performs edits, assembles pricing components, calculates the payment amount, and determines if any outliers apply. It then returns the calculated payment information and a return code (PPS-RTC) indicating the payment method and any reasons for non-payment. The program utilizes a copybook `LTDRG031` which appears to contain DRG-related data. The program is effective for bills starting July 1, 2003.  The main difference appears to be in the values used for calculation, and the special handling for provider `332006`.

### Business Functions
-   Calculates LTC payments based on DRG and other relevant data.
-   Applies payment methodologies, including normal DRG, short stay, and blend payments.
-   Calculates outlier payments.
-   Performs data validation and error handling.
-   Special handling for a specific provider.

### Programs Called and Data Structures Passed

-   **COPY LTDRG031**: Includes DRG information in a table.
    -   Data structure used: `W-DRG-TABLE` (defined within `LTDRG031`) containing `WWM-ENTRY` records.

-   **Called from**: The program is designed to be called by another program. The data structures are passed through the `LINKAGE SECTION`.

    -   `BILL-NEW-DATA`: Input bill data.
        -   `B-NPI10`
            -   `B-NPI8`
            -   `B-NPI-FILLER`
        -   `B-PROVIDER-NO`
        -   `B-PATIENT-STATUS`
        -   `B-DRG-CODE`
        -   `B-LOS`
        -   `B-COV-DAYS`
        -   `B-LTR-DAYS`
        -   `B-DISCHARGE-DATE`
            -   `B-DISCHG-CC`
            -   `B-DISCHG-YY`
            -   `B-DISCHG-MM`
            -   `B-DISCHG-DD`
        -   `B-COV-CHARGES`
        -   `B-SPEC-PAY-IND`
        -   `FILLER`
    -   `PPS-DATA-ALL`: Output payment data and related information.
        -   `PPS-RTC`
        -   `PPS-CHRG-THRESHOLD`
        -   `PPS-DATA`
            -   `PPS-MSA`
            -   `PPS-WAGE-INDEX`
            -   `PPS-AVG-LOS`
            -   `PPS-RELATIVE-WGT`
            -   `PPS-OUTLIER-PAY-AMT`
            -   `PPS-LOS`
            -   `PPS-DRG-ADJ-PAY-AMT`
            -   `PPS-FED-PAY-AMT`
            -   `PPS-FINAL-PAY-AMT`
            -   `PPS-FAC-COSTS`
            -   `PPS-NEW-FAC-SPEC-RATE`
            -   `PPS-OUTLIER-THRESHOLD`
            -   `PPS-SUBM-DRG-CODE`
            -   `PPS-CALC-VERS-CD`
            -   `PPS-REG-DAYS-USED`
            -   `PPS-LTR-DAYS-USED`
            -   `PPS-BLEND-YEAR`
            -   `PPS-COLA`
            -   `FILLER`
        -   `PPS-OTHER-DATA`
            -   `PPS-NAT-LABOR-PCT`
            -   `PPS-NAT-NONLABOR-PCT`
            -   `PPS-STD-FED-RATE`
            -   `PPS-BDGT-NEUT-RATE`
            -   `FILLER`
        -   `PPS-PC-DATA`
            -   `PPS-COT-IND`
            -   `FILLER`
    -   `PRICER-OPT-VERS-SW`: Option and version flags.
        -   `PRICER-OPTION-SW`
            -   `ALL-TABLES-PASSED`
            -   `PROV-RECORD-PASSED`
        -   `PPS-VERSIONS`
            -   `PPDRV-VERSION`
    -   `PROV-NEW-HOLD`: Provider-specific data.
        -   `PROV-NEWREC-HOLD1`
            -   `P-NEW-NPI10`
                -   `P-NEW-NPI8`
                -   `P-NEW-NPI-FILLER`
            -   `P-NEW-PROVIDER-NO`
                -   `P-NEW-STATE`
                -   `FILLER`
            -   `P-NEW-DATE-DATA`
                -   `P-NEW-EFF-DATE`
                    -   `P-NEW-EFF-DT-CC`
                    -   `P-NEW-EFF-DT-YY`
                    -   `P-NEW-EFF-DT-MM`
                    -   `P-NEW-EFF-DT-DD`
                -   `P-NEW-FY-BEGIN-DATE`
                    -   `P-NEW-FY-BEG-DT-CC`
                    -   `P-NEW-FY-BEG-DT-YY`
                    -   `P-NEW-FY-BEG-DT-MM`
                    -   `P-NEW-FY-BEG-DT-DD`
                -   `P-NEW-REPORT-DATE`
                    -   `P-NEW-REPORT-DT-CC`
                    -   `P-NEW-REPORT-DT-YY`
                    -   `P-NEW-REPORT-DT-MM`
                    -   `P-NEW-REPORT-DT-DD`
                -   `P-NEW-TERMINATION-DATE`
                    -   `P-NEW-TERM-DT-CC`
                    -   `P-NEW-TERM-DT-YY`
                    -   `P-NEW-TERM-DT-MM`
                    -   `P-NEW-TERM-DT-DD`
            -   `P-NEW-WAIVER-CODE`
                -   `P-NEW-WAIVER-STATE`
            -   `P-NEW-INTER-NO`
            -   `P-NEW-PROVIDER-TYPE`
            -   `P-NEW-CURRENT-CENSUS-DIV`
            -   `P-NEW-MSA-DATA`
                -   `P-NEW-CHG-CODE-INDEX`
                -   `P-NEW-GEO-LOC-MSAX`
                -   `P-NEW-GEO-LOC-MSA9`
                -   `P-NEW-WAGE-INDEX-LOC-MSA`
                -   `P-NEW-STAND-AMT-LOC-MSA`
                -   `P-NEW-STAND-AMT-LOC-MSA9`
                    -   `P-NEW-RURAL-1ST`
                        -   `P-NEW-STAND-RURAL`
                        -   `P-NEW-STD-RURAL-CHECK`
                    -   `P-NEW-RURAL-2ND`
            -   `P-NEW-SOL-COM-DEP-HOSP-YR`
            -   `P-NEW-LUGAR`
            -   `P-NEW-TEMP-RELIEF-IND`
            -   `P-NEW-FED-PPS-BLEND-IND`
            -   `FILLER`
        -   `PROV-NEWREC-HOLD2`
            -   `P-NEW-VARIABLES`
                -   `P-NEW-FAC-SPEC-RATE`
                -   `P-NEW-COLA`
                -   `P-NEW-INTERN-RATIO`
                -   `P-NEW-BED-SIZE`
                -   `P-NEW-OPER-CSTCHG-RATIO`
                -   `P-NEW-CMI`
                -   `P-NEW-SSI-RATIO`
                -   `P-NEW-MEDICAID-RATIO`
                -   `P-NEW-PPS-BLEND-YR-IND`
                -   `P-NEW-PRUF-UPDTE-FACTOR`
                -   `P-NEW-DSH-PERCENT`
                -   `P-NEW-FYE-DATE`
            -   `FILLER`
        -   `PROV-NEWREC-HOLD3`
            -   `P-NEW-PASS-AMT-DATA`
                -   `P-NEW-PASS-AMT-CAPITAL`
                -   `P-NEW-PASS-AMT-DIR-MED-ED`
                -   `P-NEW-PASS-AMT-ORGAN-ACQ`
                -   `P-NEW-PASS-AMT-PLUS-MISC`
            -   `P-NEW-CAPI-DATA`
                -   `P-NEW-CAPI-PPS-PAY-CODE`
                -   `P-NEW-CAPI-HOSP-SPEC-RATE`
                -   `P-NEW-CAPI-OLD-HARM-RATE`
                -   `P-NEW-CAPI-NEW-HARM-RATIO`
                -   `P-NEW-CAPI-CSTCHG-RATIO`
                -   `P-NEW-CAPI-NEW-HOSP`
                -   `P-NEW-CAPI-IME`
                -   `P-NEW-CAPI-EXCEPTIONS`
            -   `FILLER`
    -   `WAGE-NEW-INDEX-RECORD`: Wage index data.
        -   `W-MSA`
        -   `W-EFF-DATE`
        -   `W-WAGE-INDEX1`
        -   `W-WAGE-INDEX2`
        -   `W-WAGE-INDEX3`

## Program: LTDRG031

### Overview
This program is a COPY member containing a table of DRG (Diagnosis Related Group) codes and associated data. This data is used by the LTCAL032 and LTCAL042 programs for payment calculations. The data includes a DRG code, a relative weight (`WWM-RELWT`), and an average length of stay (`WWM-ALOS`).

### Business Functions
-   Provides DRG-specific data for payment calculations.

### Programs Called and Data Structures Passed
-   This is a `COPY` member and is not a stand-alone program.
-   It is included in LTCAL032 and LTCAL042
-   Data structure used: `W-DRG-TABLE` which is a REDEFINES of `W-DRG-FILLS`
    -   `WWM-ENTRY` (OCCURS 502 TIMES)
        -   `WWM-DRG` (PIC X(3))
        -   `WWM-RELWT` (PIC 9(1)V9(4))
        -   `WWM-ALOS` (PIC 9(2)V9(1))

# Summary
-   The core business value of these programs is to calculate and determine the correct payment amounts for Long-Term Care (LTC) claims.  This includes accurate DRG-based payment calculations, outlier payment determinations, and the application of blend payment rules. They ensure correct reimbursements based on the submitted claim data and provider-specific information.
-   LTCAL032 and LTCAL042 are very similar, both calculating LTC payments, but using different effective dates and slightly different business rules.
-   LTDRG031 is a supporting data structure, providing DRG information to the calculation programs.
