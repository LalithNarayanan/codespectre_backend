# Step 1: Analyze Context 1

## Program: PROG1
### Overview
This program appears to be a batch processing program. It likely reads input data, performs some calculations or transformations, and then writes output data. Based on the code, it interacts with a file named `INPUT-FILE` and writes to a file named `OUTPUT-FILE`. It also uses a working storage section to define data structures.

### Business Functions
*   Reading input data from a file.
*   Writing output data to a file.
*   Data manipulation/processing (the specifics depend on what is done inside the `PERFORM` statements).

### Called Programs and Data Structures Passed
*   None. This program does not call any other programs.

# Step 2: Analyze Context 2

## Program: PROG2
### Overview
This program is another batch processing program. It reads from `INPUT-FILE` and writes to `OUTPUT-FILE`. It contains error handling, as indicated by the `INVALID KEY` clauses. It also likely performs data validation or transformation.

### Business Functions
*   Reading input data from a file.
*   Writing output data to a file.
*   Data validation.
*   Error handling (specifically, handling `INVALID KEY` errors).
*   Data manipulation/processing, as implied by the `PERFORM` statements.

### Called Programs and Data Structures Passed
*   None. This program does not call any other programs.

# Step 3: Analyze Context 3

## Program: PROG3
### Overview
This program is another batch processing program. It reads from a file named `INPUT-FILE` and writes to a file named `OUTPUT-FILE`. It uses `COMP-3` fields, indicating packed decimal data, which is common in COBOL for representing numeric values.

### Business Functions
*   Reading input data from a file.
*   Writing output data to a file.
*   Data manipulation/processing, as indicated by the `PERFORM` statements.

### Called Programs and Data Structures Passed
*   None. This program does not call any other programs.

# Summary
This analysis has broken down the provided COBOL programs, identifying their basic functionality, the business functions they perform, and any program calls they make along with the associated data structures. Each program appears to be a self-contained batch process, reading from one file and writing to another, with data manipulation and, in some cases, error handling, performed in between.
