Okay, let's design a system.  I'll provide functional specifications for a simple library management system.  You can then use these specifications to create the object-oriented design and Java code.


**Functional Specifications: Library Management System**

The system should manage books, members, and loans.  It should allow for:

1. **Adding new books:**  Each book needs a title, author, ISBN, and availability status (available/borrowed).

2. **Adding new members:** Each member needs a name, member ID, and contact information (e.g., phone number or email).

3. **Borrowing books:** A member can borrow a book if it's available.  The system should record the loan date and due date (e.g., two weeks from the loan date).

4. **Returning books:** A member can return a book. The system should record the return date and update the book's availability status.

5. **Searching for books:** The system should allow searching for books by title, author, or ISBN.

6. **Viewing member information:**  The system should allow viewing a member's borrowing history.


**Additional Requirements:**

* The system should handle exceptions gracefully (e.g., attempting to borrow an unavailable book).
* The system should be designed for extensibility (e.g., adding new types of library materials in the future).


Now, please provide the object-oriented design based on these specifications, focusing on containment, and then the Java code implementing that design.  I'll review your design and code for correctness and best practices.
