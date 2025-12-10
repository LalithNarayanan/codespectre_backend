
       ******************************************************************
       * STORDVAL.CBL - Standing Order Validation Program               *
       ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. STORDVAL.
       DATA DIVISION.
       LINKAGE SECTION.
           COPY WS-SO-RECORD.
           01 WS-RETURN-CODE PIC 9(4).
       WORKING-STORAGE SECTION.
           COPY COMMON-STORAGE.
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           IF WS-SO-AMOUNT < ZERO
               MOVE 1 TO WS-RETURN-CODE
               MOVE "Amount must be positive." TO WS-MESSAGE
               GO TO END-PROGRAM.
           END-IF.

           IF WS-SO-FREQ NOT = "MONTHLY" AND WS-SO-FREQ NOT = "WEEKLY"
               MOVE 2 TO WS-RETURN-CODE
               MOVE "Invalid Frequency." TO WS-MESSAGE
               GO TO END-PROGRAM.
           END-IF.
           MOVE ZERO TO WS-RETURN-CODE.
       END-PROGRAM.
           EXIT PROGRAM.
