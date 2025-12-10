```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Scanner;

// Represents a Customer
class Customer {
    private int id;
    private LocalDate lastModifiedDate;

    public Customer(int id) {
        this.id = id;
        this.lastModifiedDate = LocalDate.now();
    }

    public int getId() {
        return id;
    }

    public LocalDate getLastModifiedDate() {
        return lastModifiedDate;
    }

    public void updateLastModifiedDate() {
        this.lastModifiedDate = LocalDate.now();
    }

    @Override
    public String toString() {
        return "Customer{" +
                "id=" + id +
                ", lastModifiedDate=" + lastModifiedDate.format(DateTimeFormatter.ISO_DATE) +
                '}';
    }
}

// Represents an Account
class Account {
    private int id;
    private int customerId;

    public Account(int id, int customerId) {
        this.id = id;
        this.customerId = customerId;
    }

    public int getId() {
        return id;
    }

    public int getCustomerId() {
        return customerId;
    }

    @Override
    public String toString() {
        return "Account{" +
                "id=" + id +
                ", customerId=" + customerId +
                '}';
    }
}


// Represents a Standing Order
class StandingOrder {
    private int id;
    private int customerId;
    private int fromAccountId;
    private int toAccountId;
    private double amount;
    private String frequency;
    private LocalDate nextExecutionDate;
    private String status;
    private LocalDate creationDate;
    private LocalDate lastModifiedDate;

    public StandingOrder(int id, int customerId, int fromAccountId, int toAccountId, double amount, String frequency, LocalDate nextExecutionDate) {
        this.id = id;
        this.customerId = customerId;
        this.fromAccountId = fromAccountId;
        this.toAccountId = toAccountId;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
        this.status = "ACTIVE";
        this.creationDate = LocalDate.now();
        this.lastModifiedDate = LocalDate.now();
    }

    public boolean isValid() {
        return amount > 0 && (frequency.equals("MONTHLY") || frequency.equals("WEEKLY"));
    }

    // Getters and Setters (omitted for brevity)


    @Override
    public String toString() {
        return "StandingOrder{" +
                "id=" + id +
                ", customerId=" + customerId +
                ", fromAccountId=" + fromAccountId +
                ", toAccountId=" + toAccountId +
                ", amount=" + amount +
                ", frequency='" + frequency + '\'' +
                ", nextExecutionDate=" + nextExecutionDate.format(DateTimeFormatter.ISO_DATE) +
                ", status='" + status + '\'' +
                ", creationDate=" + creationDate.format(DateTimeFormatter.ISO_DATE) +
                ", lastModifiedDate=" + lastModifiedDate.format(DateTimeFormatter.ISO_DATE) +
                '}';
    }
}

// Simulates Database interaction (replace with actual DB calls)
class DMSDatabase {
    //In a real application, this would interact with a real database.  This is a placeholder.
    public int storeStandingOrder(StandingOrder so) {
        System.out.println("Storing Standing Order in DMS: " + so);
        return 0; //0 indicates success.  Non-zero indicates error.
    }

    public Customer getCustomer(int customerId) {
        System.out.println("Retrieving Customer from DMS: " + customerId);
        //In a real application, this would query the database
        return new Customer(customerId);
    }

    public int modifyCustomer(Customer customer) {
        System.out.println("Modifying Customer in DMS: " + customer);
        return 0; //0 indicates success.  Non-zero indicates error.
    }
}

// Simulates File Handling (replace with actual file I/O)
class FileHandler {
    //In a real application, this would read from CUSTOMER.DAT and ACCT.DAT files. This is a placeholder.
    public Customer getCustomer(int customerId) {
        System.out.println("Retrieving Customer from file: " + customerId);
        return new Customer(customerId);
    }

    public Account getAccount(int accountId) {
        System.out.println("Retrieving Account from file: " + accountId);
        return new Account(accountId, 1); //Assuming customer ID 1 for simplicity
    }
}

// Main orchestrator
class StandingOrderManager {
    private FileHandler fileHandler;
    private DMSDatabase dmsDatabase;

    public StandingOrderManager(FileHandler fileHandler, DMSDatabase dmsDatabase) {
        this.fileHandler = fileHandler;
        this.dmsDatabase = dmsDatabase;
    }

    public void createStandingOrder(Scanner scanner) {
        System.out.println("Creating new Standing Order...");

        System.out.print("Enter Customer ID: ");
        int customerId = scanner.nextInt();
        scanner.nextLine(); // Consume newline

        System.out.print("Enter From Account ID: ");
        int fromAccountId = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Enter To Account ID: ");
        int toAccountId = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Enter Amount: ");
        double amount = scanner.nextDouble();
        scanner.nextLine();

        System.out.print("Enter Frequency (MONTHLY/WEEKLY): ");
        String frequency = scanner.nextLine().toUpperCase();

        System.out.print("Enter Next Execution Date (YYYY-MM-DD): ");
        LocalDate nextExecutionDate = null;
        try {
            nextExecutionDate = LocalDate.parse(scanner.nextLine(), DateTimeFormatter.ISO_DATE);
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date format. Please use YYYY-MM-DD.");
            return;
        }

        Customer customer = fileHandler.getCustomer(customerId);
        Account fromAccount = fileHandler.getAccount(fromAccountId);
        Account toAccount = fileHandler.getAccount(toAccountId);

        if (customer == null || fromAccount == null || toAccount == null || fromAccount.getCustomerId() != customerId || toAccount.getCustomerId() != customerId) {
            System.out.println("Invalid Customer or Account information.");
            return;
        }


        StandingOrder standingOrder = new StandingOrder(1, customerId, fromAccountId, toAccountId, amount, frequency, nextExecutionDate);

        if (!standingOrder.isValid()) {
            System.out.println("Invalid Standing Order data.");
            return;
        }

        int dmsStatus = dmsDatabase.storeStandingOrder(standingOrder);
        if (dmsStatus != 0) {
            System.out.println("Error storing standing order in DMS.");
            return;
        }

        customer.updateLastModifiedDate();
        int modifyStatus = dmsDatabase.modifyCustomer(customer);
        if (modifyStatus != 0) {
            System.out.println("Error modifying customer in DMS.");
            return;
        }

        System.out.println("Standing Order created successfully: " + standingOrder);
    }
}


public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        FileHandler fileHandler = new FileHandler();
        DMSDatabase dmsDatabase = new DMSDatabase();
        StandingOrderManager manager = new StandingOrderManager(fileHandler, dmsDatabase);

        manager.createStandingOrder(scanner);
        scanner.close();
    }
}
```