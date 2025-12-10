```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Scanner;

//Data Classes
class StandingOrder {
    private String standingOrderId;
    private String customerId;
    private String fromAccountId;
    private String toAccountId;
    private double amount;
    private String frequency;
    private LocalDate nextExecutionDate;
    private String status;
    private LocalDate creationDate;
    private LocalDate lastModifiedDate;

    public StandingOrder(String standingOrderId, String customerId, String fromAccountId, String toAccountId, double amount,
                         String frequency, LocalDate nextExecutionDate, String status, LocalDate creationDate,
                         LocalDate lastModifiedDate) {
        this.standingOrderId = standingOrderId;
        this.customerId = customerId;
        this.fromAccountId = fromAccountId;
        this.toAccountId = toAccountId;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
        this.status = status;
        this.creationDate = creationDate;
        this.lastModifiedDate = lastModifiedDate;
    }


    public boolean isValid() {
        return amount > 0 && (frequency.equals("MONTHLY") || frequency.equals("WEEKLY"));
    }

    @Override
    public String toString() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        return "StandingOrder{" +
                "standingOrderId='" + standingOrderId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", fromAccountId='" + fromAccountId + '\'' +
                ", toAccountId='" + toAccountId + '\'' +
                ", amount=" + amount +
                ", frequency='" + frequency + '\'' +
                ", nextExecutionDate=" + nextExecutionDate.format(formatter) +
                ", status='" + status + '\'' +
                ", creationDate=" + creationDate.format(formatter) +
                ", lastModifiedDate=" + lastModifiedDate.format(formatter) +
                '}';
    }

    // Getters and Setters (omitted for brevity)

    public String getCustomerId() { return customerId;}
    public void setLastModifiedDate(LocalDate lastModifiedDate) { this.lastModifiedDate = lastModifiedDate; }

}

class Customer {
    private String customerId;
    private String customerName;
    // ... other customer details

    public Customer(String customerId, String customerName) {
        this.customerId = customerId;
        this.customerName = customerName;
    }

    public String getCustomerId() {
        return customerId;
    }

    @Override
    public String toString() {
        return "Customer{" +
                "customerId='" + customerId + '\'' +
                ", customerName='" + customerName + '\'' +
                '}';
    }
    // Getters and Setters (omitted for brevity)
}

class Account {
    private String accountId;
    private String customerId;
    private double accountBalance;
    // ... other account details

    public Account(String accountId, String customerId, double accountBalance) {
        this.accountId = accountId;
        this.customerId = customerId;
        this.accountBalance = accountBalance;
    }

    public String getAccountId() { return accountId;}
    public String getCustomerId() { return customerId;}

    @Override
    public String toString() {
        return "Account{" +
                "accountId='" + accountId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", accountBalance=" + accountBalance +
                '}';
    }
    // Getters and Setters (omitted for brevity)
}


//Interface Classes
class DatabaseInterface {
    //Simulates Database interaction.  Replace with actual DB calls in a real application.
    public void storeStandingOrder(StandingOrder order) {
        System.out.println("Standing order stored in database: " + order);
    }

    public Customer getCustomer(String customerId) {
        //Simulate DB lookup. Replace with actual DB call.
        if (customerId.equals("123")) {
            return new Customer("123", "John Doe");
        } else {
            return null;
        }

    }

    public void updateCustomer(Customer customer) {
        System.out.println("Customer updated in database: " + customer);
    }

    public String getErrorCode() { return "00"; }
    public String getErrorMessage() { return "No errors"; }
}

class FileInterface {
    //Simulates file interaction. Replace with actual file I/O in a real application
    public Customer getCustomer(String customerId) {
        //Simulate file lookup. Replace with actual file read.
        if (customerId.equals("123")) {
            return new Customer("123", "John Doe");
        } else {
            return null;
        }
    }

    public Account getAccount(String accountId) {
        //Simulate file lookup. Replace with actual file read.
        if (accountId.equals("456")) {
            return new Account("456", "123", 1000.0);
        } else {
            return null;
        }
    }

    public String getErrorCode() { return "00"; }
    public String getErrorMessage() { return "No errors"; }
}

//Manager Class
class StandingOrderManager {
    private DatabaseInterface dbInterface;
    private FileInterface fileInterface;
    private Scanner scanner;

    public StandingOrderManager(DatabaseInterface dbInterface, FileInterface fileInterface) {
        this.dbInterface = dbInterface;
        this.fileInterface = fileInterface;
        this.scanner = new Scanner(System.in);
    }

    public void createStandingOrder() {
        System.out.println("Enter customer ID:");
        String customerId = scanner.nextLine();

        System.out.println("Enter from account ID:");
        String fromAccountId = scanner.nextLine();

        System.out.println("Enter to account ID:");
        String toAccountId = scanner.nextLine();

        System.out.println("Enter amount:");
        double amount = scanner.nextDouble();
        scanner.nextLine(); // consume newline

        System.out.println("Enter frequency (MONTHLY or WEEKLY):");
        String frequency = scanner.nextLine();

        System.out.println("Enter next execution date (yyyy-MM-dd):");
        LocalDate nextExecutionDate = null;
        try {
            nextExecutionDate = LocalDate.parse(scanner.nextLine(), DateTimeFormatter.ISO_DATE);
        } catch (DateTimeParseException e) {
            System.err.println("Invalid date format. Please use yyyy-MM-dd.");
            return;
        }


        //Retrieve Customer and Account from FileInterface
        Customer customer = fileInterface.getCustomer(customerId);
        Account fromAccount = fileInterface.getAccount(fromAccountId);
        Account toAccount = fileInterface.getAccount(toAccountId);


        if (customer == null || fromAccount == null || toAccount == null || !fromAccount.getCustomerId().equals(customerId) || !toAccount.getCustomerId().equals(customerId)) {
            System.err.println("Invalid customer or account IDs.");
            return;
        }

        String standingOrderId = "SO-" + System.currentTimeMillis(); //Generate unique ID
        StandingOrder order = new StandingOrder(standingOrderId, customerId, fromAccountId, toAccountId, amount, frequency, nextExecutionDate, "ACTIVE", LocalDate.now(), LocalDate.now());

        if (order.isValid()) {
            dbInterface.storeStandingOrder(order);
            customer.toString();
            dbInterface.updateCustomer(customer); //Update last modified date
            System.out.println("Standing order created successfully!");
        } else {
            System.err.println("Invalid standing order data.");
        }
    }
}

public class Main {
    public static void main(String[] args) {
        DatabaseInterface db = new DatabaseInterface();
        FileInterface file = new FileInterface();
        StandingOrderManager manager = new StandingOrderManager(db, file);
        manager.createStandingOrder();
    }
}
```