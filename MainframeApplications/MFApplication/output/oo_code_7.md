Okay, let's define the functional specifications for a system, and then I'll provide the Java code based on an object-oriented design using containment and avoiding inheritance where possible.


**Functional Specifications:  Library Management System**

This system manages books and members in a library.  It should allow for:

* **Adding new members:**  Each member has a unique ID, name, and contact information (phone number and email).
* **Adding new books:** Each book has a unique ISBN, title, author, and publication year.  It also tracks the number of copies available.
* **Borrowing books:** A member can borrow a book if a copy is available. The system records the borrowing date.
* **Returning books:** A member can return a book. The system records the return date and calculates the number of days overdue (if any), applying a fine if overdue.  The fine is calculated at a rate of $0.50 per day overdue.
* **Searching for books:**  The system allows searching for books by title, author, or ISBN.
* **Generating reports:** The system can generate reports showing:
    * All members and their borrowing history.
    * All books and their availability.
    * Overdue books.


**Now, let's design and implement the Java code.**


```java
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

// Member Class
class Member {
    private int memberId;
    private String name;
    private String phone;
    private String email;
    private List<BorrowedBook> borrowedBooks = new ArrayList<>();

    public Member(int memberId, String name, String phone, String email) {
        this.memberId = memberId;
        this.name = name;
        this.phone = phone;
        this.email = email;
    }

    // Getters and setters for member attributes

    public int getMemberId() { return memberId; }
    public String getName() { return name; }
    public void addBorrowedBook(BorrowedBook book) { borrowedBooks.add(book); }
    public List<BorrowedBook> getBorrowedBooks() { return borrowedBooks; }


}

// Book Class
class Book {
    private String isbn;
    private String title;
    private String author;
    private int publicationYear;
    private int availableCopies;

    public Book(String isbn, String title, String author, int publicationYear, int availableCopies) {
        this.isbn = isbn;
        this.title = title;
        this.author = author;
        this.publicationYear = publicationYear;
        this.availableCopies = availableCopies;
    }

    // Getters and setters for book attributes
    public String getIsbn() { return isbn; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public int getAvailableCopies() { return availableCopies; }
    public void decreaseAvailableCopies() { availableCopies--; }
    public void increaseAvailableCopies() { availableCopies++; }


}

// BorrowedBook Class (Composition)
class BorrowedBook {
    private Book book;
    private Member member;
    private LocalDate borrowDate;
    private LocalDate returnDate;

    public BorrowedBook(Book book, Member member, LocalDate borrowDate) {
        this.book = book;
        this.member = member;
        this.borrowDate = borrowDate;
    }

    // Getters and setters for BorrowedBook attributes.  Including overdue calculation.
    public double calculateFine() {
        if (returnDate == null) return 0; //Not yet returned
        long overdueDays = ChronoUnit.DAYS.between(returnDate, LocalDate.now());
        return Math.max(0, overdueDays) * 0.5;
    }
    public void setReturnDate(LocalDate returnDate) { this.returnDate = returnDate; }
    public Book getBook() { return book; }


}

// Library Class (Composition)
class Library {
    private List<Member> members = new ArrayList<>();
    private List<Book> books = new ArrayList<>();

    public void addMember(Member member) { members.add(member); }
    public void addBook(Book book) { books.add(book); }

    public void borrowBook(int memberId, String isbn) {
        Member member = findMember(memberId);
        Book book = findBook(isbn);

        if (member != null && book != null && book.getAvailableCopies() > 0) {
            book.decreaseAvailableCopies();
            BorrowedBook borrowedBook = new BorrowedBook(book, member, LocalDate.now());
            member.addBorrowedBook(borrowedBook);
            System.out.println("Book borrowed successfully.");
        } else {
            System.out.println("Borrowing failed.");
        }
    }

    public void returnBook(int memberId, String isbn) {
        Member member = findMember(memberId);
        Book book = findBook(isbn);

        if (member != null && book != null) {
            BorrowedBook borrowedBook = findBorrowedBook(member, book);
            if(borrowedBook != null) {
                borrowedBook.setReturnDate(LocalDate.now());
                book.increaseAvailableCopies();
                System.out.println("Book returned. Fine: $" + borrowedBook.calculateFine());
            } else {
                System.out.println("Book not found in borrowing history.");
            }
        } else {
            System.out.println("Return failed.");
        }
    }


    //Helper methods for searching (Implementation omitted for brevity, but straightforward)
    private Member findMember(int memberId) { /*Implementation to find member by ID*/ return null; }
    private Book findBook(String isbn) { /*Implementation to find book by ISBN*/ return null; }
    private BorrowedBook findBorrowedBook(Member member, Book book) { /*Implementation to find BorrowedBook*/ return null; }


    //Report generation methods (Implementation omitted for brevity)
    public void generateMemberReport() {}
    public void generateBookReport() {}
    public void generateOverdueReport() {}
}


public class Main {
    public static void main(String[] args) {
        // Example usage
        Library library = new Library();
        // Add members and books...  Then borrow and return books.
    }
}
```

This code demonstrates the core functionality.  The `find...` helper methods in the `Library` class would require further implementation to complete the search functionality.  Similarly, report generation is sketched out but would need detailed implementation.  This example prioritizes demonstrating the object-oriented design using containment.  Error handling and more robust input validation could be added for production-level code.
