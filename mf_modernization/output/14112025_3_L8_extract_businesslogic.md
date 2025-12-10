```yaml
- Service Name: LTCAL032
  Overview: Main program to calculate LTC payments
  Execution Flow:
    - Paragraph: 0000-MAINLINE-CONTROL
      Description: This is the main control paragraph. It orchestrates the program's execution by calling other paragraphs in a specific sequence to perform the LTC payment calculation.
      Code: |-
        ```cobol
        0000-MAINLINE-CONTROL.
        056500
                 PERFORM 0100-INITIAL-ROUTINE
                    THRU 0100-EXIT.
        063400       PERFORM 1000-EDIT-THE-BILL-INFO
                 THRU 1000-EXIT.
        063600       IF PPS-RTC = 00
        065800          PERFORM 1700-EDIT-DRG-CODE
                       THRU 1700-EXIT.
        063500
        063600       IF PPS-RTC = 00
        063700          PERFORM 2000-ASSEMBLE-PPS-VARIABLES
                       THRU 2000-EXIT.
        063800
        063900       IF PPS-RTC = 00
        064000          PERFORM 3000-CALC-PAYMENT
                       THRU 3000-EXIT
        064000          PERFORM 7000-CALC-OUTLIER
                       THRU 7000-EXIT.

                 IF PPS-RTC < 50
        064000          PERFORM 8000-BLEND
                       THRU 8000-EXIT.

        064200       PERFORM 9000-MOVE-RESULTS
                    THRU 9000-EXIT.
        064300
        061800       GOBACK.
        061900
        ```
    - Paragraph: 0100-INITIAL-ROUTINE
      Description: Initializes working storage variables and sets up initial values.
      Code: |-
        ```cobol
        062000 0100-INITIAL-ROUTINE.
        062100
                 MOVE ZEROS TO PPS-RTC.
        062200       INITIALIZE PPS-DATA.
        062300       INITIALIZE PPS-OTHER-DATA.
        062400       INITIALIZE HOLD-PPS-COMPONENTS.
        062500
        063000       MOVE .72885 TO PPS-NAT-LABOR-PCT.
        063000       MOVE .27115 TO PPS-NAT-NONLABOR-PCT.
        063000       MOVE 34956.15 TO PPS-STD-FED-RATE.
        063000       MOVE 24450 TO H-FIXED-LOSS-AMT.
        063000       MOVE 0.934 TO PPS-BDGT-NEUT-RATE.
        062100
        062000 0100-EXIT.
        062100          EXIT.
        063100
        ```
    - Paragraph: 1000-EDIT-THE-BILL-INFO
      Description: Performs data validation checks on the input bill data.  If any edits fail, it sets the PPS-RTC to an appropriate error code.
      Code: |-
        ```cobol
        064500***************************************************************
        064600*    BILL DATA EDITS IF ANY FAIL SET PPS-RTC                  *
        064700*    AND DO NOT ATTEMPT TO PRICE.                             *
        064800***************************************************************
        064400 1000-EDIT-THE-BILL-INFO.
        065100
        065200       IF (B-LOS NUMERIC) AND (B-LOS > 0)
        065400          MOVE B-LOS TO H-LOS
        065500       ELSE
        065600          MOVE 56 TO PPS-RTC.
        065900
        067700       IF PPS-RTC = 00
        067800         IF P-NEW-WAIVER-STATE
        067900            MOVE 53 TO PPS-RTC.

        068000       IF PPS-RTC = 00
        068200           IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR
        068300              (B-DISCHARGE-DATE < W-EFF-DATE))
        068400              MOVE 55 TO PPS-RTC.
        068500
        068600       IF PPS-RTC = 00
        068700           IF P-NEW-TERMINATION-DATE > 00000000
        068800              IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE
        069000                 MOVE 51 TO PPS-RTC.
        069100
        069200       IF PPS-RTC = 00
        069300           IF B-COV-CHARGES NOT NUMERIC
        069400              MOVE 58 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60
                         MOVE 61 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF (B-COV-DAYS NOT NUMERIC) OR
                           (B-COV-DAYS = 0 AND H-LOS > 0)
                         MOVE 62 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF B-LTR-DAYS > B-COV-DAYS
                         MOVE 62 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                          COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS
                          COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS.
        072700

        072700       IF PPS-RTC = 00
                          PERFORM 1200-DAYS-USED
                             THRU 1200-DAYS-USED-EXIT.
        072700

        072900 1000-EXIT.
        073000          EXIT.
        ```
    - Paragraph: 1200-DAYS-USED
      Description: Calculates the number of regular and lifetime reserve days used based on the input data.
      Code: |-
        ```cobol
        072700
        072900 1200-DAYS-USED.
        073000
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
        072700
        072900 1200-DAYS-USED-EXIT.
        073000          EXIT.
        ```
    - Paragraph: 1700-EDIT-DRG-CODE
      Description: Searches the DRG code in a table (LTDRG031). If the DRG code is not found, sets PPS-RTC to 54. If found, calls 1750-FIND-VALUE.
      Code: |-
        ```cobol
        073200***************************************************************
        073300*    FINDS THE DRG CODE IN THE TABLE                          *
        073400***************************************************************
        073100 1700-EDIT-DRG-CODE.
        073500
        065000       MOVE B-DRG-CODE TO PPS-SUBM-DRG-CODE.
                   IF PPS-RTC = 00
        074500          SEARCH ALL WWM-ENTRY
        074600             AT END
        074700                MOVE 54 TO PPS-RTC
        074800          WHEN WWM-DRG (WWM-INDX) = PPS-SUBM-DRG-CODE
        075200             PERFORM 1750-FIND-VALUE
                         THRU 1750-EXIT
                    END-SEARCH.

               1700-EXIT.
                    EXIT.
        ```
    - Paragraph: 1750-FIND-VALUE
      Description: Moves the relative weight and average length of stay from the DRG table (LTDRG031) to the PPS-DATA area.
      Code: |-
        ```cobol
        073200***************************************************************
        073300*    FINDS THE VALUE IN THE DRG CODE TABLE                    *
        073400***************************************************************
        073100 1750-FIND-VALUE.
        073500
        075300          MOVE WWM-RELWT (WWM-INDX) TO PPS-RELATIVE-WGT.
        075400          MOVE WWM-ALOS (WWM-INDX) TO PPS-AVG-LOS.

               1750-EXIT.
                    EXIT.
        ```
    - Paragraph: 2000-ASSEMBLE-PPS-VARIABLES
      Description: Assembles the necessary PPS variables, including wage index and blend indicators. Sets the PPS-RTC to an error code if the wage index or blend year is invalid.
      Code: |-
        ```cobol
        077100***************************************************************
        077200*    THE APPROPRIATE SET OF THESE PPS VARIABLES ARE SELECTED  *
        077300*    DEPENDING ON THE BILL DISCHARGE DATE AND EFFECTIVE DATE  *
        077400*    OF THAT VARIABLE.                                        *
        077500***************************************************************
        077600***  GET THE PROVIDER SPECIFIC VARIABLE AND WAGE INDEX
        077700***************************************************************
        077000 2000-ASSEMBLE-PPS-VARIABLES.
        077800
        077800       IF W-WAGE-INDEX1 NUMERIC AND W-WAGE-INDEX1 > 0
        077800          MOVE W-WAGE-INDEX1 TO PPS-WAGE-INDEX
        077800       ELSE
        077800          MOVE 52 TO PPS-RTC
        077800          GO TO 2000-EXIT.
        077800
        079400       IF P-NEW-OPER-CSTCHG-RATIO NOT NUMERIC
        080100          MOVE 65 TO PPS-RTC.

                   MOVE P-NEW-FED-PPS-BLEND-IND TO PPS-BLEND-YEAR.

                   IF PPS-BLEND-YEAR > 0 AND PPS-BLEND-YEAR < 6
                      NEXT SENTENCE
                   ELSE
                      MOVE 72 TO PPS-RTC
                      GO TO 2000-EXIT.
        080200
                   MOVE 0 TO H-BLEND-FAC.
                   MOVE 1 TO H-BLEND-PPS.
                   MOVE 0 TO H-BLEND-RTC.
        080200
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
        080200
        077000 2000-EXIT.
                    EXIT.
        ```
    - Paragraph: 3000-CALC-PAYMENT
      Description: Calculates the standard payment amount based on the input data and various factors. It then determines if the short-stay logic applies and calls the 3400-SHORT-STAY paragraph if necessary.
      Code: |-
        ```cobol
        080500***************************************************************
        080600*    IF THE BILL DATA HAS PASSED ALL EDITS (RTC=00)           *
        080700*        CALCULATE THE STANDARD PAYMENT AMOUNT.               *
        080900*        CALCULATE THE SHORT-STAY OUTLIER AMOUNT.             *
        081100***************************************************************
        080400 3000-CALC-PAYMENT.
        081300
                   MOVE P-NEW-COLA TO PPS-COLA.

        091600       COMPUTE PPS-FAC-COSTS ROUNDED =
                           P-NEW-OPER-CSTCHG-RATIO * B-COV-CHARGES.


        081300       COMPUTE H-LABOR-PORTION ROUNDED =
                           (PPS-STD-FED-RATE * PPS-NAT-LABOR-PCT)
                             * PPS-WAGE-INDEX.

        081300
        081300       COMPUTE H-NONLABOR-PORTION ROUNDED =
                           (PPS-STD-FED-RATE * PPS-NAT-NONLABOR-PCT)
                             * PPS-COLA.
        081300
        081300
        081300       COMPUTE PPS-FED-PAY-AMT ROUNDED =
                           (H-LABOR-PORTION + H-NONLABOR-PORTION).
        081300
                   COMPUTE PPS-DRG-ADJ-PAY-AMT ROUNDED =
                        (PPS-FED-PAY-AMT * PPS-RELATIVE-WGT).

                   COMPUTE H-SSOT = (PPS-AVG-LOS / 6) * 5.
        083900       IF H-LOS <= H-SSOT
        083300          PERFORM 3400-SHORT-STAY
                         THRU 3400-SHORT-STAY-EXIT.
        086400
        086500 3000-EXIT.
        086500          EXIT.
        088800
        ```
    - Paragraph: 3400-SHORT-STAY
      Description: Calculates the short stay payment amount and determines if it should be used instead of the DRG adjusted payment. Sets the PPS-RTC accordingly.
      Code: |-
        ```cobol
        080500***************************************************************
        080600*    IF THE LENGTH OF STAY IS LESS THAN OR EQUAL TO 5/6       *
        080700*      OF THE AVG. LENGTH OF STAY THEN:                       *
        080900*      - CALCULATE THE SHORT-STAY COST.                       *
        080900*      - CALCULATE THE SHORT-STAY PAYMENT AMOUNT.             *
        080900*      - PAY THE LEAST OF:                                    *
        080900*          - SHORT STAY COST                                  *
        080900*          - SHORT STAY PAYMENT AMOUNT                        *
        080900*          - DRG ADJUSTED PAYMENT AMOUNT                      *
        080900*      - SET RETURN CODE TO INDICATE SHORT STAY PAYMENT       *
        081100***************************************************************
        087300 3400-SHORT-STAY.
        089200

        091400       COMPUTE H-SS-COST ROUNDED =
                           (PPS-FAC-COSTS * 1.2).
        089200

        091400       COMPUTE H-SS-PAY-AMT ROUNDED =
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
        091600
        087300 3400-SHORT-STAY-EXIT.
        091700          EXIT.
        088800
        ```
    - Paragraph: 7000-CALC-OUTLIER
      Description: Calculates the outlier threshold and payment amount.  Sets the PPS-RTC to indicate outlier payment if applicable.
      Code: |-
        ```cobol
        080500***************************************************************
        080600*   CALCULATE THE OUTLIER THRESHOLD                           *
        080700*   CALCULATE THE OUTLIER PAYMENT AMOUNT IF THE FACILTY COST  *
        080900*     IS GREATER THAN THE OUTLIER THRESHOLD                   *
        080900*   SET RETURN CODE TO INDICATE OUTLIER PAYMENT METHOD        *
        081100***************************************************************
        087300 7000-CALC-OUTLIER.
        091600

        091600       COMPUTE PPS-OUTLIER-THRESHOLD ROUNDED =
                           PPS-DRG-ADJ-PAY-AMT + H-FIXED-LOSS-AMT.
        091600

                   IF PPS-FAC-COSTS > PPS-OUTLIER-THRESHOLD
        091600          COMPUTE PPS-OUTLIER-PAY-AMT ROUNDED =
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

        087300 7000-EXIT.
        091700          EXIT.
        ```
    - Paragraph: 8000-BLEND
      Description: Applies blending logic based on the PPS-BLEND-YEAR. Calculates the final payment amount and sets the PPS-RTC.
      Code: |-
        ```cobol
        080500***************************************************************
        080600*   CALCULATE THE "FINAL" PAYMENT AMOUNT.                     *
        080700*   SET RTC FOR SPECIFIED BLEND YEAR INDICATOR.               *
        081100***************************************************************
        087300 8000-BLEND.

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

        087300 8000-EXIT.
        091700          EXIT.
        ```
    - Paragraph: 9000-MOVE-RESULTS
      Description: Moves the calculated results to the output PPS-DATA-ALL area.
      Code: |-
        ```cobol
        091800
               9000-MOVE-RESULTS.

        056600       IF PPS-RTC < 50
        056700          MOVE H-LOS                 TO  PPS-LOS
        058300          MOVE 'V03.2'               TO  PPS-CALC-VERS-CD
        058400       ELSE
        062200          INITIALIZE PPS-DATA
        062300          INITIALIZE PPS-OTHER-DATA
        061200          MOVE 'V03.2'                TO  PPS-CALC-VERS-CD.
        097000

        097100 9000-EXIT.
        097100          EXIT.
        061700
        097300******        L A S T   S O U R C E   S T A T E M E N T   *****
        ```
  Business Rules:
    - Payment Calculation: The program calculates LTC payments based on the DRG (Diagnosis Related Group), length of stay, and other factors.
    - Short Stay: If the length of stay is less than or equal to 5/6 of the average length of stay, the short-stay payment logic is applied.
    - Outlier Payments:  If the facility costs exceed the outlier threshold, an outlier payment is calculated.
    - Blending:  The program applies blending logic based on the PPS blend year.
  Data validation and error handling logic:
    - B-LOS Validation: If B-LOS (Length of Stay) is not numeric or is less than or equal to zero, PPS-RTC (Return Code) is set to 56 (Invalid Length of Stay).
    - Waiver State Check: If P-NEW-WAIVER-STATE is true, PPS-RTC is set to 53.
    - Discharge Date Edits: Checks if the discharge date is valid. If the discharge date is before the provider's or wage's effective date, or if the discharge date is greater than or equal to the termination date, an error code is set.
    - B-COV-CHARGES Validation:  If B-COV-CHARGES (Covered Charges) is not numeric, PPS-RTC is set to 58.
    - B-LTR-DAYS Validation: If B-LTR-DAYS (Lifetime Reserve Days) is not numeric or exceeds 60, PPS-RTC is set to 61.
    - B-COV-DAYS Validation: If B-COV-DAYS (Covered Days) is not numeric, or if B-COV-DAYS is zero while H-LOS is greater than zero, PPS-RTC is set to 62.
    - B-LTR-DAYS vs B-COV-DAYS Validation: If B-LTR-DAYS is greater than B-COV-DAYS, PPS-RTC is set to 62.
    - DRG Code Validation:  If the DRG code is not found in the DRG table, PPS-RTC is set to 54.
    - Wage Index Validation: If the wage index is invalid, PPS-RTC is set to 52.
    - COLA and Provider Specific Rate Validation: If P-NEW-COLA is not numeric, PPS-RTC is set to 50.
    - Operating Cost-to-Charge Ratio Validation: If P-NEW-OPER-CSTCHG-RATIO is not numeric, PPS-RTC is set to 65.
    - Blend Year Validation:  If PPS-BLEND-YEAR is not within the valid range (1-5), PPS-RTC is set to 72.

- Service Name: LTCAL042
  Overview: Main program to calculate LTC payments, similar to LTCAL032, but with different effective dates and potentially updated logic.
  Execution Flow:
    - Paragraph: 0000-MAINLINE-CONTROL
      Description: This is the main control paragraph. It orchestrates the program's execution by calling other paragraphs in a specific sequence to perform the LTC payment calculation.
      Code: |-
        ```cobol
        0000-MAINLINE-CONTROL.
        056500
                 PERFORM 0100-INITIAL-ROUTINE
                    THRU 0100-EXIT.
        063400       PERFORM 1000-EDIT-THE-BILL-INFO
                 THRU 1000-EXIT.
        063600       IF PPS-RTC = 00
        065800          PERFORM 1700-EDIT-DRG-CODE
                       THRU 1700-EXIT.
        063500
        063600       IF PPS-RTC = 00
        063700          PERFORM 2000-ASSEMBLE-PPS-VARIABLES
                       THRU 2000-EXIT.
        063800
        063900       IF PPS-RTC = 00
        064000          PERFORM 3000-CALC-PAYMENT
                       THRU 3000-EXIT
        064000          PERFORM 7000-CALC-OUTLIER
                       THRU 7000-EXIT.

                 IF PPS-RTC < 50
        064000          PERFORM 8000-BLEND
                       THRU 8000-EXIT.

        064200       PERFORM 9000-MOVE-RESULTS
                    THRU 9000-EXIT.
        064300
        061800       GOBACK.
        061900
        ```
    - Paragraph: 0100-INITIAL-ROUTINE
      Description: Initializes working storage variables and sets up initial values.
      Code: |-
        ```cobol
        062000 0100-INITIAL-ROUTINE.
        062100
                 MOVE ZEROS TO PPS-RTC.
        062200       INITIALIZE PPS-DATA.
        062300       INITIALIZE PPS-OTHER-DATA.
        062400       INITIALIZE HOLD-PPS-COMPONENTS.
        062500
        063000       MOVE .72885 TO PPS-NAT-LABOR-PCT.
        063000       MOVE .27115 TO PPS-NAT-NONLABOR-PCT.
        063000       MOVE 35726.18 TO PPS-STD-FED-RATE.
        063000       MOVE 19590 TO H-FIXED-LOSS-AMT.
        063000       MOVE 0.940 TO PPS-BDGT-NEUT-RATE.
        062100
        062000 0100-EXIT.
        062100          EXIT.
        063100
        ```
    - Paragraph: 1000-EDIT-THE-BILL-INFO
      Description: Performs data validation checks on the input bill data. If any edits fail, it sets the PPS-RTC to an appropriate error code.
      Code: |-
        ```cobol
        064500***************************************************************
        064600*    BILL DATA EDITS IF ANY FAIL SET PPS-RTC                  *
        064700*    AND DO NOT ATTEMPT TO PRICE.                             *
        064800***************************************************************
        064400 1000-EDIT-THE-BILL-INFO.
        065100
        065200       IF (B-LOS NUMERIC) AND (B-LOS > 0)
        065400          MOVE B-LOS TO H-LOS
        065500       ELSE
        065600          MOVE 56 TO PPS-RTC.
        065900
                   IF PPS-RTC = 00
                     IF P-NEW-COLA NOT NUMERIC
                        MOVE 50 TO PPS-RTC.

        067700       IF PPS-RTC = 00
        067800         IF P-NEW-WAIVER-STATE
        067900            MOVE 53 TO PPS-RTC.

        068000       IF PPS-RTC = 00
        068200           IF ((B-DISCHARGE-DATE < P-NEW-EFF-DATE) OR
        068300              (B-DISCHARGE-DATE < W-EFF-DATE))
        068400              MOVE 55 TO PPS-RTC.
        068500

        068600       IF PPS-RTC = 00
        068700           IF P-NEW-TERMINATION-DATE > 00000000
        068800              IF B-DISCHARGE-DATE >= P-NEW-TERMINATION-DATE
        069000                 MOVE 51 TO PPS-RTC.
        069100

        069200       IF PPS-RTC = 00
        069300           IF B-COV-CHARGES NOT NUMERIC
        069400              MOVE 58 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF B-LTR-DAYS NOT NUMERIC OR B-LTR-DAYS > 60
                         MOVE 61 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF (B-COV-DAYS NOT NUMERIC) OR
                           (B-COV-DAYS = 0 AND H-LOS > 0)
                         MOVE 62 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                      IF B-LTR-DAYS > B-COV-DAYS
                         MOVE 62 TO PPS-RTC.
        072700

        072700       IF PPS-RTC = 00
                          COMPUTE H-REG-DAYS = B-COV-DAYS - B-LTR-DAYS
                          COMPUTE H-TOTAL-DAYS = H-REG-DAYS + B-LTR-DAYS.
        072700

        072700       IF PPS-RTC = 00
                          PERFORM 1200-DAYS-USED
                             THRU 1200-DAYS-USED-EXIT.
        072700

        072900 1000-EXIT.
        073000          EXIT.
        ```
    - Paragraph: 1200-DAYS-USED
      Description: Calculates the number of regular and lifetime reserve days used based on the input data.
      Code: |-
        ```cobol
        072700
        072900 1200-DAYS-USED.
        073000
                     IF (B-LTR-DAYS > 0) AND (H-REG-DAYS = 0)
                        IF B-LTR-DAYS > H-LOS
                           MOVE H-LOS TO PPS-LTR-DAYS-USED
                        ELSE
                           MOVE B-LTR-DAYS