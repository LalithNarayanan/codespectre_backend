Okay, let's define the functional specifications first.  We'll design a system for managing a library.


**Functional Specifications for a Library Management System:**

The system should manage books, members, and loans.  It should allow for:

1. **Adding new books:**  Each book needs a title, author, ISBN, and publication year.  Multiple copies of the same book can exist.

2. **Adding new members:** Each member needs a name, address, and membership ID.

3. **Loaning books to members:**  The system should track which books are currently loaned out to which members, including the loan date and due date.  It should prevent loaning out books that are already checked out.  It should also handle overdue books.

4. **Returning books:**  When a member returns a book, the system should update the loan status and calculate any fines (if overdue).

5. **Searching for books:** The system should allow searching for books by title, author, or ISBN.

6. **Generating reports:**  The system should generate reports on overdue books, books currently on loan, and members with outstanding fines.


Now, let's proceed to the object-oriented design using containment and then the Java code.


**Object-Oriented Design:**

We'll use containment (aggregation and composition) to model the relationships between objects.  Inheritance would create tight coupling and make extending the system difficult.  For example, if we used inheritance to represent different types of members (e.g., student members, faculty members), changes to the base class would affect all subclasses.  Containment allows for more flexibility.


**Key Objects and Responsibilities:**

* **Library:**  This is the main container object. It contains collections of `Book` and `Member` objects. It manages the loaning and returning of books.  It also handles report generation.

* **Book:** Represents a single book.  It contains information about the title, author, ISBN, publication year, and copies.  It is composed of `BookCopy` objects.

* **BookCopy:** Represents a single physical copy of a book. It tracks the book's availability (loaned or available).


* **Member:** Represents a library member. It contains information about the member's name, address, and membership ID.

* **Loan:** Represents a book loan. It tracks the book copy, member, loan date, and due date.  It calculates fines for overdue books.


**Relationships:**

* **Library *contains* many Book:** Aggregation.  The Library can exist without the books.

* **Book *contains* many BookCopy:** Composition. A Book cannot exist without at least one BookCopy.

* **Library *contains* many Member:** Aggregation.

* **Library *contains* many Loan:** Aggregation.

* **Loan *contains* BookCopy:** Composition. A Loan needs a book copy.

* **Loan *contains* Member:** Composition.  A loan needs a member.


**Java Code:**

```java
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

class Book {
    String title;
    String author;
    String isbn;
    int publicationYear;
    List<BookCopy> copies;

    public Book(String title, String author, String isbn, int publicationYear) {
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publicationYear = publicationYear;
        this.copies = new ArrayList<>();
    }

    public void addCopy() {
        copies.add(new BookCopy(this));
    }
    //Getters and setters...
}

class BookCopy {
    Book book;
    boolean available;

    public BookCopy(Book book) {
        this.book = book;
        this.available = true;
    }
    //Getters and setters...

}

class Member {
    String name;
    String address;
    String memberId;

    public Member(String name, String address, String memberId) {
        this.name = name;
        this.address = address;
        this.memberId = memberId;
    }
    //Getters and setters...
}

class Loan {
    BookCopy bookCopy;
    Member member;
    Date loanDate;
    Date dueDate;

    public Loan(BookCopy bookCopy, Member member, Date loanDate, Date dueDate) {
        this.bookCopy = bookCopy;
        this.member = member;
        this.loanDate = loanDate;
        this.dueDate = dueDate;
    }
    //Getters and setters and methods to calculate fines...
}

class Library {
    List<Book> books;
    List<Member> members;
    List<Loan> loans;

    public Library() {
        this.books = new ArrayList<>();
        this.members = new ArrayList<>();
        this.loans = new ArrayList<>();
    }

    public void addBook(Book book) {
        books.add(book);
    }

    public void addMember(Member member) {
        members.add(member);
    }

    public void loanBook(BookCopy bookCopy, Member member, Date loanDate, Date dueDate) {
        if (bookCopy.available) {
            loans.add(new Loan(bookCopy, member, loanDate, dueDate));
            bookCopy.available = false;
        } else {
            System.out.println("Book is not available");
        }
    }

    //Methods for returning books, searching, generating reports etc.
}


public class Main {
    public static void main(String[] args) {
        Library library = new Library();
        //Example usage...
    }
}
```

This is a basic framework.  You would need to add methods for returning books, searching, generating reports, handling overdue books and fines, and robust error handling.  Remember to add appropriate getters and setters for all classes.  This design emphasizes modularity and extensibility, crucial for a well-structured library management system.
