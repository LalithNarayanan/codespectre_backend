# Step: Analyze COBOL Programs

## Program: LTCAL032

### Overview
This COBOL program, LTCAL032, calculates Long-Term Care (LTC) payments based on the DRG (Diagnosis Related Group) system. It takes bill data as input, performs edits, assembles pricing components, calculates payment, and handles outliers. It calls a copybook, LTDRG031, which contains the DRG table.

### Calls to External Resources
-   The program **calls** the copybook `LTDRG031`.

### SQL Queries
-   None

### CICS Calls
-   None

## Program: LTCAL042

### Overview
This COBOL program, LTCAL042, is similar to LTCAL032, calculating LTC payments using DRG. It also takes bill data as input, performs edits, assembles pricing components, calculates payment, and handles outliers. The main difference appears to be an updated version, likely with different calculation logic and data. It calls a copybook, LTDRG031, which contains the DRG table.

### Calls to External Resources
-   The program **calls** the copybook `LTDRG031`.

### SQL Queries
-   None

### CICS Calls
-   None

## Program: LTDRG031

### Overview
This COBOL program, LTDRG031, is a copybook containing a table (W-DRG-TABLE) with DRG codes, relative weights, and average lengths of stay. It is used by LTCAL032 and LTCAL042 to look up DRG-specific information during payment calculations.

### Calls to External Resources
-   None

### SQL Queries
-   None

### CICS Calls
-   None

# Summary
-   LTCAL032 and LTCAL042 calculate LTC payments, calling the copybook LTDRG031.
-   LTDRG031 contains DRG data used in the payment calculations.
-   There are no database, web service, online transaction system or CICS calls found in these programs.
