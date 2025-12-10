Okay, let's define the functional specifications first.  I'll propose a system, and then we can proceed with the object-oriented design and Java code.


**Functional Specifications:  Library Management System**

This system manages books and members within a library.  The system should allow:

1. **Adding new books:**  Each book has a title, author, ISBN, and availability status (available/borrowed).

2. **Adding new members:** Each member has a name, member ID, and a list of currently borrowed books.

3. **Borrowing books:** A member can borrow a book if it's available. The system should update the book's availability and add the book to the member's borrowed books list.  It should also record the borrowing date.

4. **Returning books:** A member can return a book.  The system should update the book's availability and remove the book from the member's borrowed books list. It should also record the return date.

5. **Searching for books:** The system should allow searching for books by title, author, or ISBN.

6. **Generating reports:** The system should generate reports listing all books, all members, and books borrowed by a specific member.


Now, with these functional specifications, I can provide the object-oriented design emphasizing composition and then generate the Java code.  I'll focus on clear responsibilities and low coupling.  We can iterate on this design if needed.
