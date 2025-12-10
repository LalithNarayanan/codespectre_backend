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
        - 1000-EDIT-THE-BILL-INFO: Performs data validation edits.
        - 1700-EDIT-DRG-CODE: Edits the DRG code.
        - 2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables.
        - 3000-CALC-PAYMENT: Calculates the payment.
        - 7000-CALC-OUTLIER: Calculates outlier payments.
        - 8000-BLEND: Performs blending calculations.
        - 9000-MOVE-RESULTS: Moves the results.
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
        - MOVE ZEROS TO PPS-RTC: Initializes PPS-RTC to zero.
        - INITIALIZE PPS-DATA: Initializes PPS-DATA to zero.
        - INITIALIZE PPS-OTHER-DATA: Initializes PPS-OTHER-DATA to zero.
        - INITIALIZE HOLD-PPS-COMPONENTS: Initializes HOLD-PPS-COMPONENTS to zero.
        - MOVE .72885 TO PPS-NAT-LABOR-PCT: Moves the value .72885 to PPS-NAT-LABOR-PCT.
        - MOVE .27115 TO PPS-NAT-NONLABOR-PCT: Moves the value .27115 to PPS-NAT-NONLABOR-PCT.
        - MOVE 34956.15 TO PPS-STD-FED-RATE: Moves the value 34956.15 to PPS-STD-FED-RATE.
        - MOVE 24450 TO H-FIXED-LOSS-AMT: Moves the value 24450 to H-FIXED-LOSS-AMT.
        - MOVE 0.934 TO PPS-BDGT-NEUT-RATE: Moves the value 0.934 to PPS-BDGT-NEUT-RATE.
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
    - Name: 0100-EXIT
      Description: Exit paragraph for 0100-INITIAL-ROUTINE.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1000-EDIT-THE-BILL-INFO
      Description: Edits the input bill data.
      Calls:
        - Checks if B-LOS is numeric and greater than 0, and sets PPS-RTC to 56 if not.
        - Checks if P-NEW-WAIVER-STATE is true and sets PPS-RTC to 53 if true.
        - Checks if B-DISCHARGE-DATE is less than P-NEW-EFF-DATE or W-EFF-DATE and sets PPS-RTC to 55 if true.
        - Checks if P-NEW-TERMINATION-DATE is greater than 00000000 and B-DISCHARGE-DATE is greater than or equal to P-NEW-TERMINATION-DATE and sets PPS-RTC to 51 if true.
        - Checks if B-COV-CHARGES is not numeric and sets PPS-RTC to 58 if true.
        - Checks if B-LTR-DAYS is not numeric or greater than 60 and sets PPS-RTC to 61 if true.
        - Checks if B-COV-DAYS is not numeric or if B-COV-DAYS is 0 and H-LOS is greater than 0 and sets PPS-RTC to 62 if true.
        - Checks if B-LTR-DAYS is greater than B-COV-DAYS and sets PPS-RTC to 62 if true.
        - COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS: Computes H-REG-DAYS.
        - COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS: Computes H-TOTAL-DAYS.
        - 1200-DAYS-USED: Performs the days used calculation.
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
    - Name: 1000-EXIT
      Description: Exit paragraph for 1000-EDIT-THE-BILL-INFO.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1200-DAYS-USED
      Description: Calculates the number of days used based on B-LTR-DAYS, H-REG-DAYS and H-LOS.
      Calls:
        - Multiple IF statements to calculate and move values to PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on different conditions related to the covered days and lifetime reserve days.
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
    - Name: 1200-DAYS-USED-EXIT
      Description: Exit paragraph for 1200-DAYS-USED.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1700-EDIT-DRG-CODE
      Description: Searches the DRG code in the lookup table.
      Calls:
        - MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE: Moves B-DRG-CODE to PPS-SUBM-DRG-CODE.
        - SEARCH ALL WWM-ENTRY: Searches the DRG code in the table.
        - 1750-FIND-VALUE: Performs DRG value lookup if found.
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
    - Name: 1700-EXIT
      Description: Exit paragraph for 1700-EDIT-DRG-CODE.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1750-FIND-VALUE
      Description: Finds the value in the DRG code table.
      Calls:
        - MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT: Moves the relative weight.
        - MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS: Moves the average LOS.
      CodeSnippet: |
        MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT.
        MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS.
    - Name: 1750-EXIT
      Description: Exit paragraph for 1750-FIND-VALUE.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 2000-ASSEMBLE-PPS-VARIABLES
      Description: Assembles PPS variables.
      Calls:
        - Checks if W-WAGE-INDEX1 is numeric and greater than 0 and moves it to PPS-WAGE-INDEX, otherwise sets PPS-RTC to 52.
        - Checks if P-NEW-OPER-CSTCHG-RATIO is not numeric and sets PPS-RTC to 65.
        - MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR: Moves the value to PPS-BLEND-YEAR.
        - Checks if PPS-BLEND-YEAR is within the valid range (1-5), otherwise sets PPS-RTC to 72.
        - Sets initial values for H-BLEND-FAC, H-BLEND-PPS, and H-BLEND-RTC.
        - Based on PPS-BLEND-YEAR, sets blend factors and return code modifiers.
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
    - Name: 2000-EXIT
      Description: Exit paragraph for 2000-ASSEMBLE-PPS-VARIABLES.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 3000-CALC-PAYMENT
      Description: Calculates the standard payment amount.
      Calls:
        - MOVE P-NEW-COLA TO PPS-COLA: Moves the value to PPS-COLA.
        - COMPUTE PPS-FAC-COSTS ROUNDED: Computes the facility costs.
        - COMPUTE H-LABOR-PORTION ROUNDED: Computes the labor portion.
        - COMPUTE H-NONLABOR-PORTION ROUNDED: Computes the non-labor portion.
        - COMPUTE PPS-FED-PAY-AMT ROUNDED: Computes the federal payment amount.
        - COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED: Computes the DRG adjusted payment amount.
        - COMPUTE H-SSOT: Computes the short-stay outlier threshold.
        - 3400-SHORT-STAY: Performs short-stay calculations if applicable.
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
    - Name: 3000-EXIT
      Description: Exit paragraph for 3000-CALC-PAYMENT.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 3400-SHORT-STAY
      Description: Calculates short-stay payments.
      Calls:
        - COMPUTE H-SS-COST ROUNDED: Computes the short-stay cost.
        - COMPUTE H-SS-PAY-AMT ROUNDED: Computes the short-stay payment amount.
        - Multiple IF statements to determine the final payment amount and set the PPS-RTC based on comparisons of H-SS-COST, H-SS-PAY-AMT, and PPS-DRG-ADJ-PAY-AMT.
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
    - Name: 3400-SHORT-STAY-EXIT
      Description: Exit paragraph for 3400-SHORT-STAY.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 7000-CALC-OUTLIER
      Description: Calculates outlier payments.
      Calls:
        - COMPUTE PPS-OUTLIER-THRESHOLD ROUNDED: Computes the outlier threshold.
        - COMPUTE PPS-OUTLIER-PAY-AMT ROUNDED: Computes the outlier payment amount.
        - Conditional logic to determine the outlier payment and set the PPS-RTC based on various conditions.
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
    - Name: 7000-EXIT
      Description: Exit paragraph for 7000-CALC-OUTLIER.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 8000-BLEND
      Description: Calculates the final payment amount for blended payments.
      Calls:
        - COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED: Computes the adjusted DRG payment amount.
        - COMPUTE PPS-NEW-FAC-SPEC-RATE ROUNDED: Computes the new facility specific rate.
        - COMPUTE PPS-FINAL-PAY-AMT: Computes the final payment amount.
        - ADD H-BLEND-RTC TO PPS-RTC: Adds the blend return code to PPS-RTC.
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
    - Name: 8000-EXIT
      Description: Exit paragraph for 8000-BLEND.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 9000-MOVE-RESULTS
      Description: Moves the results to the output data structure.
      Calls:
        - Moves values from HOLD-PPS-COMPONENTS and constants to PPS-DATA and PPS-OTHER-DATA depending on PPS-RTC.
      CodeSnippet: |
        IF PPS-RTC < 50
           MOVE H-LOS                 TO  PPS-LOS
           MOVE 'V03.2'               TO  PPS-CALC-VERS-CD
        ELSE
           INITIALIZE PPS-DATA
           INITIALIZE PPS-OTHER-DATA
           MOVE 'V03.2'                TO  PPS-CALC-VERS-CD.
    - Name: 9000-EXIT
      Description: Exit paragraph for 9000-MOVE-RESULTS.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
  BusinessRules:
    - Calculates payment for LTC DRGs.
    - Uses DRG table LTDRG031 for lookups.
    - Applies normal, short-stay, outlier, and blended payment methodologies.
    - Considers provider-specific data, dates, budget neutrality.
  DataValidation:
    - B-LOS must be numeric and >0 (Error code 56)
    - B-COV-CHARGES must be numeric (Error code 58)
    - B-LTR-DAYS must be numeric and <=60 (Error code 61)
    - B-COV-DAYS must be numeric (Error code 62)
    - B-LTR-DAYS must be less than or equal to B-COV-DAYS (Error code 62)
    - P-NEW-WAIVER-STATE must be false (Error code 53)
    - B-DISCHARGE-DATE must be greater or equal to P-NEW-EFF-DATE, and W-EFF-DATE(Error code 55)
    - P-NEW-TERMINATION-DATE must be less than B-DISCHARGE-DATE (Error code 51)
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
        - 1000-EDIT-THE-BILL-INFO: Performs data validation edits.
        - 1700-EDIT-DRG-CODE: Edits the DRG code.
        - 2000-ASSEMBLE-PPS-VARIABLES: Assembles PPS variables.
        - 3000-CALC-PAYMENT: Calculates the payment.
        - 7000-CALC-OUTLIER: Calculates outlier payments.
        - 8000-BLEND: Performs blending calculations.
        - 9000-MOVE-RESULTS: Moves the results.
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
        - MOVE ZEROS TO PPS-RTC: Initializes PPS-RTC to zero.
        - INITIALIZE PPS-DATA: Initializes PPS-DATA to zero.
        - INITIALIZE PPS-OTHER-DATA: Initializes PPS-OTHER-DATA to zero.
        - INITIALIZE HOLD-PPS-COMPONENTS: Initializes HOLD-PPS-COMPONENTS to zero.
        - MOVE .72885 TO PPS-NAT-LABOR-PCT: Moves the value .72885 to PPS-NAT-LABOR-PCT.
        - MOVE .27115 TO PPS-NAT-NONLABOR-PCT: Moves the value .27115 to PPS-NAT-NONLABOR-PCT.
        - MOVE 35726.18 TO PPS-STD-FED-RATE: Moves the value 35726.18 to PPS-STD-FED-RATE.
        - MOVE 19590 TO H-FIXED-LOSS-AMT: Moves the value 19590 to H-FIXED-LOSS-AMT.
        - MOVE 0.940 TO PPS-BDGT-NEUT-RATE: Moves the value 0.940 to PPS-BDGT-NEUT-RATE.
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
    - Name: 0100-EXIT
      Description: Exit paragraph for 0100-INITIAL-ROUTINE.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1000-EDIT-THE-BILL-INFO
      Description: Edits the input bill data.
      Calls:
        - Checks if B-LOS is numeric and greater than 0, and sets PPS-RTC to 56 if not.
        - Checks if P-NEW-COLA is not numeric and sets PPS-RTC to 50 if not.
        - Checks if P-NEW-WAIVER-STATE is true and sets PPS-RTC to 53 if true.
        - Checks if B-DISCHARGE-DATE is less than P-NEW-EFF-DATE or W-EFF-DATE and sets PPS-RTC to 55 if true.
        - Checks if P-NEW-TERMINATION-DATE is greater than 00000000 and B-DISCHARGE-DATE is greater than or equal to P-NEW-TERMINATION-DATE and sets PPS-RTC to 51 if true.
        - Checks if B-COV-CHARGES is not numeric and sets PPS-RTC to 58 if true.
        - Checks if B-LTR-DAYS is not numeric or greater than 60 and sets PPS-RTC to 61 if true.
        - Checks if B-COV-DAYS is not numeric or if B-COV-DAYS is 0 and H-LOS is greater than 0 and sets PPS-RTC to 62 if true.
        - Checks if B-LTR-DAYS is greater than B-COV-DAYS and sets PPS-RTC to 62 if true.
        - COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS: Computes H-REG-DAYS.
        - COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS: Computes H-TOTAL-DAYS.
        - 1200-DAYS-USED: Performs the days used calculation.
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
    - Name: 1000-EXIT
      Description: Exit paragraph for 1000-EDIT-THE-BILL-INFO.
      Calls:
        - EXIT: Exits the paragraph.
      CodeSnippet: |
        EXIT.
    - Name: 1200-DAYS-USED
      Description: Calculates the number of days used based on B-LTR-DAYS, H-REG-DAYS and H-LOS.
      Calls:
        - Multiple IF statements to calculate and move values to PPS-LTR-DAYS-USED and PPS-REG-DAYS-USED based on different conditions related to the covered days and lifetime reserve days.
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
                    MOVE H-LOS TO PPS-REG-