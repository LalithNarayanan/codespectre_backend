Okay, let's define the functional specifications first.  We'll design a system for managing a library.


**Functional Specifications:**

The library system should manage books, members, and loans.

* **Books:** Each book has a unique ISBN, title, author, and current availability status (available or borrowed).  The system should allow for searching books by ISBN, title, or author.

* **Members:** Each member has a unique member ID, name, and contact information (e.g., phone number, email).  The system should allow for adding new members and searching for existing members by ID or name.  Members can borrow a limited number of books (e.g., 3).

* **Loans:** A loan represents a book borrowed by a member.  It includes the book, the member, the loan date, and the due date.  The system should allow for recording new loans, marking loans as returned, and identifying overdue loans.  The system should prevent members from borrowing more books than allowed and prevent borrowing unavailable books.


**Object-Oriented Design (based on containment and avoiding inheritance):**

Based on these specifications, here's an object-oriented design:

* **Core Objects:** `Book`, `Member`, `Loan`, `Library`.

* **Relationships:**
    * `Library` contains a collection of `Book` objects (composition).
    * `Library` contains a collection of `Member` objects (composition).
    * `Library` contains a collection of `Loan` objects (composition).
    * `Loan` contains a `Book` object (composition).
    * `Loan` contains a `Member` object (composition).

* **Responsibilities and Attributes:**

    * **`Book`:**
        * **Attributes:** `isbn` (String), `title` (String), `author` (String), `isAvailable` (boolean)
        * **Responsibilities:**  Provide access to its attributes.

    * **`Member`:**
        * **Attributes:** `memberId` (int), `name` (String), `contactInfo` (String), `booksBorrowed` (List<Loan>)
        * **Responsibilities:** Provide access to its attributes,  check if member can borrow more books.

    * **`Loan`:**
        * **Attributes:** `book` (`Book`), `member` (`Member`), `loanDate` (Date), `dueDate` (Date), `isReturned` (boolean)
        * **Responsibilities:** Provide access to its attributes, calculate overdue status.

    * **`Library`:**
        * **Attributes:** `books` (List<Book>), `members` (List<Member>), `loans` (List<Loan>), `maxBooksPerMember` (int)
        * **Responsibilities:** Add/remove books and members, record loans, search for books and members, identify overdue loans, manage loan limits.


**Java Code:**

```java
import java.util.*;

class Book {
    String isbn;
    String title;
    String author;
    boolean isAvailable;

    public Book(String isbn, String title, String author) {
        this.isbn = isbn;
        this.title = title;
        this.author = author;
        this.isAvailable = true;
    }

    // Getters and setters for attributes...
}

class Member {
    int memberId;
    String name;
    String contactInfo;
    List<Loan> booksBorrowed;
    int maxBooks;

    public Member(int memberId, String name, String contactInfo, int maxBooks) {
        this.memberId = memberId;
        this.name = name;
        this.contactInfo = contactInfo;
        this.booksBorrowed = new ArrayList<>();
        this.maxBooks = maxBooks;
    }

    // Getters and setters for attributes...
    public boolean canBorrowMore(){
        return booksBorrowed.size() < maxBooks;
    }
}

class Loan {
    Book book;
    Member member;
    Date loanDate;
    Date dueDate;
    boolean isReturned;

    public Loan(Book book, Member member, Date loanDate, Date dueDate) {
        this.book = book;
        this.member = member;
        this.loanDate = loanDate;
        this.dueDate = dueDate;
        this.isReturned = false;
    }

    // Getters and setters for attributes...
    public boolean isOverdue(){
        return new Date().after(dueDate) && !isReturned;
    }
}

class Library {
    List<Book> books;
    List<Member> members;
    List<Loan> loans;
    int maxBooksPerMember;

    public Library(int maxBooksPerMember) {
        this.books = new ArrayList<>();
        this.members = new ArrayList<>();
        this.loans = new ArrayList<>();
        this.maxBooksPerMember = maxBooksPerMember;
    }

    // Methods to add/remove books, members, record loans, search, manage overdue loans etc...  (Implementation omitted for brevity)
}


public class Main {
    public static void main(String[] args) {
        Library library = new Library(3); // Max 3 books per member

        // Add books, members, and loans... (Example omitted for brevity)
    }
}
```

This provides a basic structure.  You would need to add the implementation details for adding/removing books and members, searching, recording loans, handling returns, and managing overdue loans within the `Library` class.  Error handling and input validation should also be added for a production-ready system.  This example showcases the core object-oriented design principles requested.
