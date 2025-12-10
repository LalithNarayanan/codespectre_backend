******************************************************************
       * DMSSTORE.CBL - DMS Store Program                              *
       ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DMSSTORE.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. UNISYS-CLEARPATH.
       OBJECT-COMPUTER. UNISYS-CLEARPATH.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY COMMON-STORAGE.
           01 WS-DMS-AREA.
               05 WS-SO-DBKEY        PIC X(8).
               05 WS-SO-RECORD-AREA.
                   COPY WS-SO-RECORD.
           01 WS-DMS-ERROR-AREA.
               05 WS-DMS-ERROR-CODE  PIC 9(8).
               05 WS-DMS-ERROR-TEXT  PIC X(256).
       LINKAGE SECTION.
           01 LINK-SO-RECORD.
               COPY WS-SO-RECORD.
           01 LINK-DMS-STATUS PIC XX.
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           * Move the linked record into the working storage area.
           MOVE LINK-SO-RECORD TO WS-SO-RECORD-AREA.

           * Attempt to store the standing order record into the database.
           DMS STORE RECORD STANDING-ORDER-RECORD
               USING WS-SO-RECORD-AREA
               DBKEY WS-SO-DBKEY
               ERROR WS-DMS-ERROR-AREA.

           IF WS-DMS-ERROR-CODE NOT = ZERO
               MOVE "DS" TO LINK-DMS-STATUS
               MOVE WS-DMS-ERROR-CODE TO WS-RETURN-CODE
               DISPLAY "DMS STORE Error: " WS-DMS-ERROR-CODE
               DISPLAY "DMS Error Text: " WS-DMS-ERROR-TEXT
               GO TO END-PROGRAM.
           END-IF.

           * Now, let's assume we want to update the customer's last modified date
           * in the customer database as well.
           MOVE WS-SO-CUST-ID TO WS-CUSTOMER-ID.

           DMS GET RECORD CUSTOMER-RECORD
               USING WS-CUSTOMER-ID
               ERROR WS-DMS-ERROR-AREA.

           IF WS-DMS-ERROR-CODE NOT = ZERO
               MOVE "DG" TO LINK-DMS-STATUS
               MOVE WS-DMS-ERROR-CODE TO WS-RETURN-CODE
               DISPLAY "DMS GET Error: " WS-DMS-ERROR-CODE
               DISPLAY "DMS Error Text: " WS-DMS-ERROR-TEXT
               GO TO END-PROGRAM.
           END-IF.

           MOVE WS-CURRENT-DATE TO WS-CUST-LAST-MODIFIED-DATE.

           DMS MODIFY RECORD CUSTOMER-RECORD
               USING WS-CUSTOMER-RECORD
               ERROR WS-DMS-ERROR-AREA.

           IF WS-DMS-ERROR-CODE NOT = ZERO
               MOVE "DM" TO LINK-DMS-STATUS
               MOVE WS-DMS-ERROR-CODE TO WS-RETURN-CODE
               DISPLAY "DMS MODIFY Error: " WS-DMS-ERROR-CODE
               DISPLAY "DMS Error Text: " WS-DMS-ERROR-TEXT
               GO TO END-PROGRAM.
           END-IF.

           MOVE "00" TO LINK-DMS-STATUS.
           MOVE ZERO TO WS-RETURN-CODE.

       END-PROGRAM.
           EXIT PROGRAM.