
       ******************************************************************
       * STORDSET.CBL - Standing Order Setup Program                   *
       ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. STORDSET.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. UNISYS-CLEARPATH.
       OBJECT-COMPUTER. UNISYS-CLEARPATH.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CUSTOMER-FILE ASSIGN TO "CUST.DAT"
               ORGANIZATION IS INDEXED
               ACCESS MODE IS RECORD KEY
               RECORD KEY IS WS-CUSTOMER-ID
               FILE STATUS IS WS-FILE-STATUS.
           SELECT ACCOUNT-FILE ASSIGN TO "ACCT.DAT"
               ORGANIZATION IS INDEXED
               ACCESS MODE IS RECORD KEY
               RECORD KEY IS WS-ACCOUNT-ID
               FILE STATUS IS WS-FILE-STATUS.
       DATA DIVISION.
       FILE SECTION.
           FD CUSTOMER-FILE.
           01 CUSTOMER-RECORD.
               COPY WS-CUSTOMER-RECORD.
           FD ACCOUNT-FILE.
           01 ACCOUNT-RECORD.
               COPY WS-ACCOUNT-RECORD.
       WORKING-STORAGE SECTION.
           COPY COMMON-STORAGE.
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY "Enter Customer ID: ".
           ACCEPT WS-CUSTOMER-ID.
           OPEN INPUT CUSTOMER-FILE.
           READ CUSTOMER-FILE INTO WS-CUSTOMER-RECORD
               INVALID KEY DISPLAY "Customer not found."
               GO TO END-PROGRAM.
           END-READ.
           CLOSE CUSTOMER-FILE.

           DISPLAY "Enter From Account ID: ".
           ACCEPT WS-FROM-ACCOUNT.
           MOVE WS-FROM-ACCOUNT TO WS-ACCOUNT-ID.
           OPEN INPUT ACCOUNT-FILE.
           READ ACCOUNT-FILE INTO WS-ACCOUNT-RECORD
               INVALID KEY DISPLAY "From Account not found."
               GO TO END-PROGRAM.
           END-READ.
           CLOSE ACCOUNT-FILE.
           IF WS-ACCT-CUST-ID NOT = WS-CUSTOMER-ID
               DISPLAY "From Account does not belong to customer."
               GO TO END-PROGRAM.
           END-IF.

           DISPLAY "Enter To Account ID: ".
           ACCEPT WS-TO-ACCOUNT.
           MOVE WS-TO-ACCOUNT TO WS-ACCOUNT-ID.
           OPEN INPUT ACCOUNT-FILE.
           READ ACCOUNT-FILE INTO WS-ACCOUNT-RECORD
               INVALID KEY DISPLAY "To Account not found."
               GO TO END-PROGRAM.
           END-READ.
           CLOSE ACCOUNT-FILE.
           IF WS-ACCT-CUST-ID NOT = WS-CUSTOMER-ID
               DISPLAY "To Account does not belong to customer."
               GO TO END-PROGRAM.
           END-IF.

           DISPLAY "Enter Standing Order ID: ".
           ACCEPT WS-STANDING-ORDER-ID.
           DISPLAY "Enter Amount: ".
           ACCEPT WS-AMOUNT.
           DISPLAY "Enter Frequency (MONTHLY, WEEKLY): ".
           ACCEPT WS-FREQUENCY.
           DISPLAY "Enter Next Execution Date (YYYYMMDD): ".
           ACCEPT WS-NEXT-EXEC-DATE.

           ACCEPT WS-CURRENT-DATE FROM DATE YYYYMMDD.

           MOVE WS-STANDING-ORDER-ID TO WS-SO-ID.
           MOVE WS-CUSTOMER-ID TO WS-SO-CUST-ID.
           MOVE WS-FROM-ACCOUNT TO WS-SO-FROM-ACCT.
           MOVE WS-TO-ACCOUNT TO WS-SO-TO-ACCT.
           MOVE WS-AMOUNT TO WS-SO-AMOUNT.
           MOVE WS-FREQUENCY TO WS-SO-FREQ.
           MOVE WS-NEXT-EXEC-DATE TO WS-SO-NEXT-EXEC.
           MOVE "ACTIVE" TO WS-SO-STAT.
           MOVE WS-CURRENT-DATE TO WS-SO-CREAT-DATE.
           MOVE WS-CURRENT-DATE TO WS-SO-LAST-MOD.

           CALL 'STORDVAL' USING WS-SO-RECORD, WS-RETURN-CODE.
           IF WS-RETURN-CODE NOT = ZERO
               DISPLAY "Validation Error: " WS-MESSAGE
               GO TO END-PROGRAM.
           END-IF.

           CALL 'DMSSTORE' USING WS-SO-RECORD, WS-DMS-STATUS.
           IF WS-DMS-STATUS NOT = ZERO
               DISPLAY "Database Error: " WS-DMS-STATUS
               GO TO END-PROGRAM.
           END-IF.

           DISPLAY "Standing Order Created.".

       END-PROGRAM.
           STOP RUN.