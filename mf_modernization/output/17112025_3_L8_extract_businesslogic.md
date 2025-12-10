```yaml
- ProgramName: LTCAL032
  Overview: >
    This program calculates LTC payments using PPS rules. It performs billing edits,
    DRG lookups, payment computations (including short-stay, outliers, blends), and
    sets output fields. It uses `LTDRG031` as a DRG lookup table.
  Paragraphs:
    - Name: 0000-MAINLINE-CONTROL
      Description: Main control paragraph orchestrating overall processing.
      Calls:
        - 0100-INITIAL-ROUTINE: Initializes variables.
        - 1000-EDIT-THE-BILL-INFO: Performs data validation.
        - 1700-EDIT-DRG-CODE: Looks up DRG code in a table.
        - 2000-ASSEMBLE-PPS-VARIABLES: Assembles variables needed for PPS calculation.
        - 3000-CALC-PAYMENT: Calculates the payment amount.
        - 7000-CALC-OUTLIER: Calculates outlier payments.
        - 8000-BLEND: Applies blending logic.
        - 9000-MOVE-RESULTS: Moves final results to output fields.
      CodeSnippet: |
        PERFORM 0100-INITIAL-ROUTINE
           THRU 0100-EXIT.
        PERFORM 1000-EDIT-THE-BILL-INFO
           THRU 1000-EXIT.
        IF PPS-RTC = 00
           PERFORM 1700-EDIT-DRG-CODE
              THRU 1700-EXIT.
        IF PPS-RTC = 00
           PERFORM 2000-ASSEMBLE-PPS-VARIABLES
              THRU 2000-EXIT.
        IF PPS-RTC = 00
           PERFORM 3000-CALC-PAYMENT
              THRU 3000-EXIT
           PERFORM 7000-CALC-OUTLIER
              THRU 7000-EXIT.
        IF PPS-RTC < 50
           PERFORM 8000-BLEND
              THRU 8000-EXIT.
        PERFORM 9000-MOVE-RESULTS
           THRU 9000-EXIT.
        GOBACK.
    - Name: 0100-INITIAL-ROUTINE
      Description: Initializes variables and constants in working storage.
      Calls:
        - Initializes PPS-RTC to zero.
        - Initializes PPS-DATA, PPS-OTHER-DATA, and HOLD-PPS-COMPONENTS to zero.
        - Sets constants for PPS-NAT-LABOR-PCT, PPS-NAT-NONLABOR-PCT, PPS-STD-FED-RATE, H-FIXED-LOSS-AMT, and PPS-BDGT-NEUT-RATE.
      CodeSnippet: |
        MOVE ZEROS TO PPS-RTC.
        INITIALIZE PPS-DATA.
        INITIALIZE PPS-OTHER-DATA.
        INITIALIZE HOLD-PPS-COMPONENTS.
        MOVE .72885 TO PPS-NAT-LABOR-PCT.
        MOVE .27115 TO PPS-NAT-NONLABOR-PCT.
        MOVE 34956.15 TO PPS-STD-FED-RATE.
        MOVE 24450 TO H-FIXED-LOSS-AMT.
        MOVE 0.934 TO PPS-BDGT-NEUT-RATE.
    - Name: 1000-EDIT-THE-BILL-INFO
      Description: Edits the bill data for validity. Sets PPS-RTC if errors are found.
      Calls:
        - Checks if B-LOS is numeric and > 0, setting PPS-RTC = 56 if not.
        - Checks if P-NEW-WAIVER-STATE is true, setting PPS-RTC = 53 if true.
        - Checks if B-DISCHARGE-DATE is before P-NEW-EFF-DATE or W-EFF-DATE, setting PPS-RTC = 55 if true.
        - Checks if P-NEW-TERMINATION-DATE is valid and B-DISCHARGE-DATE is >= P-NEW-TERMINATION-DATE, setting PPS-RTC = 51 if true.
        - Checks if B-COV-CHARGES is numeric, setting PPS-RTC = 58 if not.
        - Checks if B-LTR-DAYS is numeric and <= 60, setting PPS-RTC = 61 if not.
        - Checks if B-COV-DAYS is numeric or zero and H-LOS > 0, setting PPS-RTC = 62 if not.
        - Checks if B-LTR-DAYS > B-COV-DAYS, setting PPS-RTC = 62 if true.
        - Computes H-REG-DAYS and H-TOTAL-DAYS.
        - Calls 1200-DAYS-USED to calculate the days used.
      CodeSnippet: |
        IF (B-LOS NUMERIC) AND (B-LOS > 0)
           MOVE B-LOS TO H-LOS
        ELSE
           MOVE 56 TO PPS-RTC.
        IF PPS-RTC = 00
          IF P-NEW-WAIVER-STATE
             MOVE 53 TO PPS-RTC.
        IF PPS-RTC = 00
           IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR
              (B-DISCHARGE-DATE < W-EFF-DATE))
              MOVE 55 TO PPS-RTC.
        IF PPS-RTC = 00
           IF P-NEW-TERMINATION-DATE > 00000000
              IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE
                 MOVE 51 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-COV-CHARGES NOT NUMERIC
              MOVE 58 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60
              MOVE 61 TO PPS-RTC.
        IF PPS-RTC = 00
           IF (B-COV-DAYS NOT NUMERIC) OR
                (B-COV-DAYS = 0 AND H-LOS > 0)
              MOVE 62 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-LTR-DAYS > B-COV-DAYS
              MOVE 62 TO PPS-RTC.
        IF PPS-RTC = 00
           COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS
           COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS.
        IF PPS-RTC = 00
           PERFORM 1200-DAYS-USED
              THRU 1200-DAYS-USED-EXIT.
    - Name: 1200-DAYS-USED
      Description: Calculates PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on B-LTR-DAYS, H-REG-DAYS, and H-LOS.
      Calls:
        - Logic to determine the appropriate values for PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on the length of stay, lifetime reserve days, and covered days.
      CodeSnippet: |
        IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)
           IF B-LTR-DAYS > H-LOS
              MOVE H-LOS TO PPS-LTR-DAYS-USED
           ELSE
              MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED
        ELSE
          IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)
             IF H-REG-DAYS > H-LOS
                MOVE H-LOS TO PPS-REG-DAYS-USED
             ELSE
                MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
          ELSE
             IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)
               IF H-REG-DAYS > H-LOS
                  MOVE H-LOS TO PPS-REG-DAYS-USED
                  MOVE 0 TO PPS-LTR-DAYS-USED
               ELSE
                  IF H-TOTAL-DAYS > H-LOS
                     MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
                     COMPUTE PPS-LTR-DAYS-USED =
                                       H-LOS - H-REG-DAYS
                  ELSE
                     IF H-TOTAL-DAYS <= H-LOS
                        MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
                        MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED
                     ELSE
                        NEXT SENTENCE
             ELSE
                NEXT SENTENCE.
    - Name: 1700-EDIT-DRG-CODE
      Description: Searches the DRG table (WWM-ENTRY) for the DRG code (B-DRG-CODE).
      Calls:
        - Moves B-DRG-CODE to PPS-SUBM-DRG-CODE.
        - Searches the WWM-ENTRY table for a matching DRG code.
        - If not found, sets PPS-RTC = 54.
        - Calls 1750-FIND-VALUE if a match is found.
      CodeSnippet: |
        MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE.
        IF PPS-RTC = 00
           SEARCH ALL WWM-ENTRY
              AT END
                MOVE 54 TO PPS-RTC
              WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE
                PERFORM 1750-FIND-VALUE
                   THRU 1750-EXIT
              END-SEARCH.
    - Name: 1750-FIND-VALUE
      Description: Moves the relative weight (WWM-RELWT) and average length of stay (WWM-ALOS) from the DRG table to PPS-RELATIVE-WGT and PPS-AVG-LOS respectively.
      Calls:
        - Moves WWM-RELWT (WWM-INDX) to PPS-RELATIVE-WGT.
        - Moves WWM-ALOS (WWM-INDX) to PPS-AVG-LOS.
      CodeSnippet: |
        MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT.
        MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS.
    - Name: 2000-ASSEMBLE-PPS-VARIABLES
      Description: Assembles the PPS variables needed for the calculation.
      Calls:
        - Checks the wage index and provider-specific data and sets error codes if invalid.
        - Determines the blend year and sets related variables.
      CodeSnippet: |
        IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0
           MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX
        ELSE
           MOVE 52 TO PPS-RTC
           GO TO 2000-EXIT.
        IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC
           MOVE 65 TO PPS-RTC.
        MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR.
        IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6
           NEXT SENTENCE
        ELSE
           MOVE 72 TO PPS-RTC
           GO TO 2000-EXIT.
        MOVE 0 TO H-BLEND-FAC.
        MOVE 1 TO H-BLEND-PPS.
        MOVE 0 TO H-BLEND-RTC.
        IF PPS-BLEND-YEAR = 1
           MOVE .8 TO H-BLEND-FAC
           MOVE .2 TO H-BLEND-PPS
           MOVE 4 TO H-BLEND-RTC
        ELSE
          IF PPS-BLEND-YEAR = 2
             MOVE .6 TO H-BLEND-FAC
             MOVE .4 TO H-BLEND-PPS
             MOVE 8 TO H-BLEND-RTC
          ELSE
            IF PPS-BLEND-YEAR = 3
               MOVE .4 TO H-BLEND-FAC
               MOVE .6 TO H-BLEND-PPS
               MOVE 12 TO H-BLEND-RTC
            ELSE
              IF PPS-BLEND-YEAR = 4
                 MOVE .2 TO H-BLEND-FAC
                 MOVE .8 TO H-BLEND-PPS
                 MOVE 16 TO H-BLEND-RTC.
    - Name: 3000-CALC-PAYMENT
      Description: Calculates the standard payment amount.
      Calls:
        - Moves P-NEW-COLA to PPS-COLA.
        - Computes PPS-FAC-COSTS.
        - Computes H-LABOR-PORTION, H-NONLABOR-PORTION, PPS-FED-PAY-AMT, and PPS-DRG-ADJ-PAY-AMT.
        - Calls 3400-SHORT-STAY if H-LOS <= H-SSOT.
      CodeSnippet: |
        MOVE P-NEW-COLA TO PPS-COLA.
        COMPUTE PPS-FAC-COSTS ROUNDED =
            P-NEW-OPER-CSTCHG-RATIO * B-COV-CHARGES.
        COMPUTE H-LABOR-PORTION ROUNDED =
           (PPS-STD-FED-RATE * PPS-NAT-LABOR-PCT)
             * PPS-WAGE-INDEX.
        COMPUTE H-NONLABOR-PORTION ROUNDED =
           (PPS-STD-FED-RATE * PPS-NAT-NONLABOR-PCT)
             * PPS-COLA.
        COMPUTE PPS-FED-PAY-AMT ROUNDED =
           (H-LABOR-PORTION + H-NONLABOR-PORTION).
        COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED =
             (PPS-FED-PAY-AMT * PPS-RELATIVE-WGT).
        COMPUTE H-SSOT = (PPS-AVG-LOS / 6) * 5.
        IF H-LOS <= H-SSOT
           PERFORM 3400-SHORT-STAY
              THRU 3400-SHORT-STAY-EXIT.
    - Name: 3400-SHORT-STAY
      Description: Calculates short-stay payment.
      Calls:
        - Computes H-SS-COST and H-SS-PAY-AMT.
        - Determines the short stay payment based on comparisons.
      CodeSnippet: |
        COMPUTE H-SS-COST ROUNDED =
            (PPS-FAC-COSTS * 1.2).
        COMPUTE H-SS-PAY-AMT ROUNDED =
             ((PPS-DRG-ADJ-PAY-AMT / PPS-AVG-LOS) * H-LOS) * 1.2.
        IF H-SS-COST < H-SS-PAY-AMT
           IF H-SS-COST < PPS-DRG-ADJ-PAY-AMT
              MOVE H-SS-COST TO PPS-DRG-ADJ-PAY-AMT
              MOVE 02 TO PPS-RTC
           ELSE
              NEXT SENTENCE
        ELSE
           IF H-SS-PAY-AMT < PPS-DRG-ADJ-PAY-AMT
              MOVE H-SS-PAY-AMT TO PPS-DRG-ADJ-PAY-AMT
              MOVE 02 TO PPS-RTC
           ELSE
              NEXT SENTENCE.
    - Name: 7000-CALC-OUTLIER
      Description: Calculates outlier payments.
      Calls:
        - Computes PPS-OUTLIER-THRESHOLD.
        - Computes PPS-OUTLIER-PAY-AMT if applicable.
        - Sets PPS-RTC based on outlier conditions.
        - Adjusts PPS-LTR-DAYS-USED if necessary.
      CodeSnippet: |
        COMPUTE PPS-OUTLIER-THRESHOLD ROUNDED =
           PPS-DRG-ADJ-PAY-AMT + H-FIXED-LOSS-AMT.
        IF PPS-FAC-COSTS > PPS-OUTLIER-THRESHOLD
           COMPUTE PPS-OUTLIER-PAY-AMT ROUNDED =
              ((PPS-FAC-COSTS - PPS-OUTLIER-THRESHOLD) * .8)
                * PPS-BDGT-NEUT-RATE * H-BLEND-PPS.
        IF B-SPEC-PAY-IND = '1'
           MOVE 0 TO PPS-OUTLIER-PAY-AMT.
        IF PPS-OUTLIER-PAY-AMT > 0 AND PPS-RTC = 02
           MOVE 03 TO PPS-RTC.
        IF PPS-OUTLIER-PAY-AMT > 0 AND PPS-RTC = 00
           MOVE 01 TO PPS-RTC.
        IF PPS-RTC = 00 OR 02
           IF PPS-REG-DAYS-USED > H-SSOT
              MOVE 0 TO PPS-LTR-DAYS-USED
           ELSE
              NEXT SENTENCE.
        IF PPS-RTC = 01 OR 03
           IF (B-COV-DAYS < H-LOS) OR PPS-COT-IND = 'Y'
             COMPUTE PPS-CHRG-THRESHOLD ROUNDED =
              PPS-OUTLIER-THRESHOLD / P-NEW-OPER-CSTCHG-RATIO
             MOVE 67 TO PPS-RTC
           ELSE
             NEXT SENTENCE
        ELSE
          NEXT SENTENCE.
    - Name: 8000-BLEND
      Description: Calculates the final payment amount based on the blend year.
      Calls:
        - Computes PPS-DRG-ADJ-PAY-AMT, PPS-NEW-FAC-SPEC-RATE, and PPS-FINAL-PAY-AMT.
        - Adds H-BLEND-RTC to PPS-RTC.
      CodeSnippet: |
        COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED =
              (PPS-DRG-ADJ-PAY-AMT * PPS-BDGT-NEUT-RATE)
                * H-BLEND-PPS.
        COMPUTE PPS-NEW-FAC-SPEC-RATE ROUNDED =
               (P-NEW-FAC-SPEC-RATE * PPS-BDGT-NEUT-RATE)
                 * H-BLEND-FAC.
        COMPUTE PPS-FINAL-PAY-AMT =
             PPS-DRG-ADJ-PAY-AMT + PPS-OUTLIER-PAY-AMT
                 + PPS-NEW-FAC-SPEC-RATE
        ADD H-BLEND-RTC TO PPS-RTC.
    - Name: 9000-MOVE-RESULTS
      Description: Moves the results to the output fields.
      Calls:
        - Moves the calculated values to the output fields.
      CodeSnippet: |
        IF PPS-RTC < 50
           MOVE H-LOS                 TO  PPS-LOS
           MOVE 'V03.2'               TO  PPS-CALC-VERS-CD
        ELSE
          INITIALIZE PPS-DATA
          INITIALIZE PPS-OTHER-DATA
          MOVE 'V03.2'                TO  PPS-CALC-VERS-CD.
  BusinessRules:
    - Calculates payment for LTC DRGs.
    - Uses DRG table LTDRG031 for lookups.
    - Applies normal, short-stay, outlier, and blended payment methodologies.
    - Considers provider-specific data, dates, budget neutrality.
  DataValidation:
    - B-LOS must be numeric and >0 (Error code 56)
    - B-COV-CHARGES must be numeric (Error code 58)
    - B-LTR-DAYS must be numeric and <=60 (Error code 61)
    - B-COV-DAYS must be numeric and not equal to zero if H-LOS is greater than zero (Error code 62)
    - B-LTR-DAYS must be less than or equal to B-COV-DAYS (Error code 62)
    - Wage index must be numeric and greater than zero (Error code 52)
    - P-NEW-COLA must be numeric (Error code 50)
  ErrorHandling:
    - Stores error state in PPS-RTC 50-99.
    - On error, PPS-RTC triggers skip/exit logic.
- ProgramName: LTCAL042
  Overview: >
    This program calculates LTC payments using PPS rules. It performs billing edits,
    DRG lookups, payment computations (including short-stay, outliers, blends), and
    sets output fields. It uses `LTDRG031` as a DRG lookup table.
  Paragraphs:
    - Name: 0000-MAINLINE-CONTROL
      Description: Main control paragraph orchestrating overall processing.
      Calls:
        - 0100-INITIAL-ROUTINE: Initializes variables.
        - 1000-EDIT-THE-BILL-INFO: Performs data validation.
        - 1700-EDIT-DRG-CODE: Looks up DRG code in a table.
        - 2000-ASSEMBLE-PPS-VARIABLES: Assembles variables needed for PPS calculation.
        - 3000-CALC-PAYMENT: Calculates the payment amount.
        - 7000-CALC-OUTLIER: Calculates outlier payments.
        - 8000-BLEND: Applies blending logic.
        - 9000-MOVE-RESULTS: Moves final results to output fields.
      CodeSnippet: |
        PERFORM 0100-INITIAL-ROUTINE
           THRU 0100-EXIT.
        PERFORM 1000-EDIT-THE-BILL-INFO
           THRU 1000-EXIT.
        IF PPS-RTC = 00
           PERFORM 1700-EDIT-DRG-CODE
              THRU 1700-EXIT.
        IF PPS-RTC = 00
           PERFORM 2000-ASSEMBLE-PPS-VARIABLES
              THRU 2000-EXIT.
        IF PPS-RTC = 00
           PERFORM 3000-CALC-PAYMENT
              THRU 3000-EXIT
           PERFORM 7000-CALC-OUTLIER
              THRU 7000-EXIT.
        IF PPS-RTC < 50
           PERFORM 8000-BLEND
              THRU 8000-EXIT.
        PERFORM 9000-MOVE-RESULTS
           THRU 9000-EXIT.
        GOBACK.
    - Name: 0100-INITIAL-ROUTINE
      Description: Initializes variables and constants in working storage.
      Calls:
        - Initializes PPS-RTC to zero.
        - Initializes PPS-DATA, PPS-OTHER-DATA, and HOLD-PPS-COMPONENTS to zero.
        - Sets constants for PPS-NAT-LABOR-PCT, PPS-NAT-NONLABOR-PCT, PPS-STD-FED-RATE, H-FIXED-LOSS-AMT, and PPS-BDGT-NEUT-RATE.
      CodeSnippet: |
        MOVE ZEROS TO PPS-RTC.
        INITIALIZE PPS-DATA.
        INITIALIZE PPS-OTHER-DATA.
        INITIALIZE HOLD-PPS-COMPONENTS.
        MOVE .72885 TO PPS-NAT-LABOR-PCT.
        MOVE .27115 TO PPS-NAT-NONLABOR-PCT.
        MOVE 35726.18 TO PPS-STD-FED-RATE.
        MOVE 19590 TO H-FIXED-LOSS-AMT.
        MOVE 0.940 TO PPS-BDGT-NEUT-RATE.
    - Name: 1000-EDIT-THE-BILL-INFO
      Description: Edits the bill data for validity. Sets PPS-RTC if errors are found.
      Calls:
        - Checks if B-LOS is numeric and > 0, setting PPS-RTC = 56 if not.
        - Checks if P-NEW-COLA is numeric, setting PPS-RTC = 50 if not.
        - Checks if P-NEW-WAIVER-STATE is true, setting PPS-RTC = 53 if true.
        - Checks if B-DISCHARGE-DATE is before P-NEW-EFF-DATE or W-EFF-DATE, setting PPS-RTC = 55 if true.
        - Checks if P-NEW-TERMINATION-DATE is valid and B-DISCHARGE-DATE is >= P-NEW-TERMINATION-DATE, setting PPS-RTC = 51 if true.
        - Checks if B-COV-CHARGES is numeric, setting PPS-RTC = 58 if not.
        - Checks if B-LTR-DAYS is numeric and <= 60, setting PPS-RTC = 61 if not.
        - Checks if B-COV-DAYS is numeric or zero and H-LOS > 0, setting PPS-RTC = 62 if not.
        - Checks if B-LTR-DAYS > B-COV-DAYS, setting PPS-RTC = 62 if true.
        - Computes H-REG-DAYS and H-TOTAL-DAYS.
        - Calls 1200-DAYS-USED to calculate the days used.
      CodeSnippet: |
        IF (B-LOS NUMERIC) AND (B-LOS > 0)
           MOVE B-LOS TO H-LOS
        ELSE
           MOVE 56 TO PPS-RTC.
        IF PPS-RTC = 00
          IF P-NEW-COLA NOT NUMERIC
             MOVE 50 TO PPS-RTC.
        IF PPS-RTC = 00
           IF P-NEW-WAIVER-STATE
              MOVE 53 TO PPS-RTC.
        IF PPS-RTC = 00
           IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR
              (B-DISCHARGE-DATE < W-EFF-DATE))
              MOVE 55 TO PPS-RTC.
        IF PPS-RTC = 00
           IF P-NEW-TERMINATION-DATE > 00000000
              IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE
                 MOVE 51 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-COV-CHARGES NOT NUMERIC
              MOVE 58 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60
              MOVE 61 TO PPS-RTC.
        IF PPS-RTC = 00
           IF (B-COV-DAYS NOT NUMERIC) OR
                (B-COV-DAYS = 0 AND H-LOS > 0)
              MOVE 62 TO PPS-RTC.
        IF PPS-RTC = 00
           IF B-LTR-DAYS > B-COV-DAYS
              MOVE 62 TO PPS-RTC.
        IF PPS-RTC = 00
           COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS
           COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS.
        IF PPS-RTC = 00
           PERFORM 1200-DAYS-USED
              THRU 1200-DAYS-USED-EXIT.
    - Name: 1200-DAYS-USED
      Description: Calculates PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on B-LTR-DAYS, H-REG-DAYS, and H-LOS.
      Calls:
        - Logic to determine the appropriate values for PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on the length of stay, lifetime reserve days, and covered days.
      CodeSnippet: |
        IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)
           IF B-LTR-DAYS > H-LOS
              MOVE H-LOS TO PPS-LTR-DAYS-USED
           ELSE
              MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED
        ELSE
          IF (H-REG-DAYS > 0) AND (B-LTR-DAYS = 0)
             IF H-REG-DAYS > H-LOS
                MOVE H-LOS TO PPS-REG-DAYS-USED
             ELSE
                MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
          ELSE
             IF (H-REG-DAYS > 0) AND (B-LTR-DAYS > 0)
               IF H-REG-DAYS > H-LOS
                  MOVE H-LOS TO PPS-REG-DAYS-USED
                  MOVE 0 TO PPS-LTR-DAYS-USED
               ELSE
                  IF H-TOTAL-DAYS > H-LOS
                     MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
                     COMPUTE PPS-LTR-DAYS-USED =
                                       H-LOS - H-REG-DAYS
                  ELSE
                     IF H-TOTAL-DAYS <= H-LOS
                        MOVE H-REG-DAYS TO PPS-REG-DAYS-USED
                        MOVE B-LTR-DAYS TO PPS-LTR-DAYS-USED
                     ELSE
                        NEXT SENTENCE
             ELSE
                NEXT SENTENCE.
    - Name: 1700-EDIT-DRG-CODE
      Description: Searches the DRG table (WWM-ENTRY) for the DRG code (B-DRG-CODE).
      Calls:
        - Moves B-DRG-CODE to PPS-SUBM-DRG-CODE.
        - Searches the WWM-ENTRY table for a matching DRG code.
        - If not found, sets PPS-RTC = 54.
        - Calls 1750-FIND-VALUE if a match is found.
      CodeSnippet: |
        MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE.
        IF PPS-RTC = 00
           SEARCH ALL WWM-ENTRY
              AT END
                MOVE 54 TO PPS-RTC
              WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE
                PERFORM 1750-FIND-VALUE
                   THRU 1750-EXIT
              END-SEARCH.
    - Name: 1750-FIND-VALUE
      Description: Moves the relative weight (WWM-RELWT) and average length of stay (WWM-ALOS) from the DRG table to PPS-RELATIVE-WGT and PPS-AVG-LOS respectively.
      Calls:
        - Moves WWM-RELWT (WWM-INDX) to PPS-RELATIVE-WGT.
        - Moves WWM-ALOS (WWM-INDX) to PPS-AVG-LOS.
      CodeSnippet: |
        MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT.
        MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS.
    - Name: 2000-ASSEMBLE-PPS-VARIABLES
      Description: Assembles the PPS variables needed for the calculation.
      Calls:
        - Checks the wage index and provider-specific data and sets error codes if invalid.
        - Determines the blend year and sets related variables.
      CodeSnippet: |
           IF P-NEW-FY-BEGIN-DATE >= 20031001 AND
              B-DISCHARGE-DATE >= P-NEW-FY-BEGIN-DATE
           IF W-WAGE-INDEX2 NUMERIC AND W-WAGE-INDEX2 > 0
              MOVE W-WAGE-INDEX2 TO PPS-WAGE-INDEX
           ELSE
              MOVE 52 TO PPS-RTC
              GO TO 2000-EXIT
           ELSE
           IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0
              MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX
           ELSE
              MOVE 52 TO PPS-RTC
              GO TO 2000-EXIT.
        IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC
           MOVE 65 TO PPS-RTC.
        MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR.
        IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6
           NEXT SENTENCE
        ELSE
           MOVE 72 TO PPS-RTC
           GO TO 2000-EXIT.
        MOVE 0 TO H-BLEND-FAC.
        MOVE 1 TO H-BLEND-PPS.
        MOVE 0 TO H-BLEND-RTC.
        IF PPS-BLEND-YEAR = 1
           MOVE .8 TO H-BLEND-FAC
           MOVE .2 TO H-BLEND-PPS
           MOVE 4 TO H-BLEND-RTC
        ELSE
          IF PPS-BLEND-YEAR = 2
             MOVE .6 TO H-BLEND-FAC
             MOVE .4 TO H-BLEND-PPS
             MOVE 8 TO H-BLEND-RTC
          ELSE
            IF PPS-BLEND-YEAR = 3
               MOVE .4 TO H-BLEND-FAC
               MOVE .6 TO H-BLEND-PPS
               MOVE 12 TO H-BLEND-RTC
            ELSE
              IF PPS-BLEND-YEAR = 4
                 MOVE .2 TO H-BLEND-FAC
                 MOVE .8 TO H-BLEND-PPS
                 MOVE 16 TO H-BLEND-RTC.
    - Name: 3000-CALC-PAYMENT
      Description: Calculates the standard payment amount.
      Calls:
        - Moves P-NEW-COLA to PPS-COLA.
        - Computes PPS-FAC-COSTS.
        - Computes H-LABOR-PORTION, H-NONLABOR-PORTION, PPS-FED-PAY-AMT, and PPS-DRG-ADJ-PAY-AMT.
        - Calls 3400-SHORT-STAY if H-LOS <= H-SSOT.
      CodeSnippet: |
        MOVE P-NEW-COLA TO PPS-COLA.
        COMPUTE PPS-FAC-COSTS ROUNDED =
            P-NEW-OPER-CSTCHG-RATIO * B-COV-CHARGES.
        COMPUTE H-LABOR-PORTION ROUNDED =
           (PPS-STD-FED-RATE * PPS-NAT-LABOR-PCT)
             * PPS-WAGE-INDEX.
        COMPUTE H-NONLABOR-PORTION ROUNDED =
           (PPS-STD-FED-RATE * PPS-NAT-NONLABOR-PCT)
             * PPS-COLA.
        COMPUTE PPS-FED-PAY-AMT ROUNDED =
           (H-LABOR-PORTION + H-NONLABOR-PORTION).
        COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED =
             (PPS-FED-PAY-AMT * PPS-RELATIVE-WGT).
        COMPUTE H-SSOT = (PPS-AVG-LOS / 6) * 5.
        IF H-LOS <= H-SSOT
           PERFORM 3400-SHORT-STAY
              THRU 3400-SHORT-STAY-EXIT.
    - Name: 3400-SHORT-STAY
      Description: Calculates short-stay payment.
      Calls:
        - Calls 4000-SPECIAL-PROVIDER if P-NEW-PROVIDER-NO = '332006'.
        - Computes H-SS