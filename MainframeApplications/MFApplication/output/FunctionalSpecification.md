
# Batch Program Details
| Program Name | Input Attributes | Output Attributes | Business Logic |
|---|---|---|---|
| DMSSTORE | LINK-SO-RECORD (WS-SO-RECORD), WS-SO-DBKEY | LINK-DMS-STATUS, WS-RETURN-CODE | Stores a standing order record in the database. If successful, updates the customer's last modified date in the customer database.  Error codes and messages are returned if any of the database operations fail. |
| STORDSET | WS-CUSTOMER-ID, WS-FROM-ACCOUNT, WS-TO-ACCOUNT, WS-STANDING-ORDER-ID, WS-AMOUNT, WS-FREQUENCY, WS-NEXT-EXEC-DATE, WS-CURRENT-DATE |  None (Displays messages) |  Collects standing order details from user input, validates the data using STORDVAL, and calls DMSSTORE to store the record in the database. Displays success or error messages. |
| STORDVAL | WS-SO-RECORD | WS-RETURN-CODE, WS-MESSAGE | Validates the amount and frequency fields of a standing order record. Returns an error code and message if validation fails. |

