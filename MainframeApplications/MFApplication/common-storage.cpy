******************************************************************
       * COMMON-STORAGE.CPY                                               *
       * Common Storage for Standing Order System                       *
       ******************************************************************
       01  WS-COMMON-STORAGE.
           05  WS-FILE-STATUS       PIC XX.
           05  WS-DMS-STATUS        PIC XX.
           05  WS-RETURN-CODE       PIC 9(4).
           05  WS-CURRENT-DATE      PIC 9(8).
           05  WS-MESSAGE           PIC X(256).
           05  WS-CUSTOMER-ID       PIC X(10).
           05  WS-ACCOUNT-ID        PIC X(15).
           05  WS-STANDING-ORDER-ID PIC X(20).
           05  WS-AMOUNT            PIC 9(10)V99.
           05  WS-FREQUENCY         PIC X(10).
           05  WS-NEXT-EXEC-DATE    PIC 9(8).
           05  WS-FROM-ACCOUNT      PIC X(15).
           05  WS-TO-ACCOUNT        PIC X(15).
           05  WS-SO-STATUS         PIC X(10).
           05  WS-CREATION-DATE     PIC 9(8).
           05  WS-LAST-MOD-DATE     PIC 9(8).
           05 WS-CUSTOMER-RECORD.
               10 WS-CUST-ID         PIC X(10).
               10 WS-CUST-NAME       PIC X(50).
               10 WS-CUST-ADDRESS    PIC X(100).
               10 WS-CUST-PHONE      PIC X(20).
           05 WS-ACCOUNT-RECORD.
               10 WS-ACCT-ID         PIC X(15).
               10 WS-ACCT-CUST-ID    PIC X(10).
               10 WS-ACCT-BALANCE    PIC 9(12)V99.
               10 WS-ACCT-TYPE       PIC X(10).
           05 WS-SO-RECORD.
               10 WS-SO-ID           PIC X(20).
               10 WS-SO-CUST-ID      PIC X(10).
               10 WS-SO-FROM-ACCT    PIC X(15).
               10 WS-SO-TO-ACCT      PIC X(15).
               10 WS-SO-AMOUNT       PIC 9(10)V99.
               10 WS-SO-FREQ         PIC X(10).
               10 WS-SO-NEXT-EXEC     PIC 9(8).
               10 WS-SO-STAT         PIC X(10).
               10 WS-SO-CREAT-DATE   PIC 9(8).
               10 WS-SO-LAST-MOD     PIC 9(8).