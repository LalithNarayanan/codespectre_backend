## Functional Specifications: Library Management System

This system manages books, members, and loans within a library.  The core functionality includes:

* **Adding new books:**  The system should allow librarians to add new books, specifying title, author, ISBN, and publication year.  It should handle duplicate ISBNs gracefully (e.g., by preventing addition or reporting an error).

* **Adding new members:** The system should allow librarians to add new library members, recording their name, address, and membership ID.  It should prevent duplicate membership IDs.

* **Loaning books:** Members can borrow books. The system should track the loan date, due date (calculated based on a loan period, e.g., 2 weeks), and whether a book is currently loaned.  It should prevent loaning books that are already loaned.

* **Returning books:** Members can return books. The system should update the loan status and record the return date.  It should calculate and display any overdue fines (based on a daily fine rate).

* **Searching for books:**  Librarians and members should be able to search for books by title, author, or ISBN.

* **Generating reports:** The system should generate reports showing all books, all members, currently loaned books, and overdue books.


Now, let's proceed with the object-oriented design based on your specifications.  I will provide the design in a separate response.  After that, I will create the Java code.
