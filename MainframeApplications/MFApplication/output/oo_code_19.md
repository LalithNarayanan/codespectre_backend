```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Core Classes
class Customer {
    private String customerId;
    // Add other customer details as needed

    public Customer(String customerId) {
        this.customerId = customerId;
    }

    public String getCustomerId() {
        return customerId;
    }

    // Add getters and setters for other customer details
}

class Account {
    private String accountId;
    private String customerId;
    // Add balance information as needed

    public Account(String accountId, String customerId) {
        this.accountId = accountId;
        this.customerId = customerId;
    }

    public String getAccountId() {
        return accountId;
    }

    public String getCustomerId() {
        return customerId;
    }

    // Add getters and setters for other account details
}

class StandingOrder {
    private String standingOrderId;
    private Account fromAccount;
    private Account toAccount;
    private double amount;
    private String frequency;
    private LocalDate nextExecutionDate;
    private LocalDate creationDate;

    public StandingOrder(String standingOrderId, Account fromAccount, Account toAccount, double amount, String frequency, LocalDate nextExecutionDate) {
        this.standingOrderId = standingOrderId;
        this.fromAccount = fromAccount;
        this.toAccount = toAccount;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
        this.creationDate = LocalDate.now();
    }

    // Getters for all fields (omitted for brevity)

    public boolean isValid(StandingOrderValidator validator) {
        return validator.validate(this);
    }


}


// Supporting Classes
class CustomerFile {
    //Simulates reading from a file.  Replace with actual file I/O.
    public Customer getCustomer(String customerId) {
        //Replace with actual file reading logic
        if (customerId.equals("CUST123")) {
            return new Customer(customerId);
        }
        return null;
    }
}

class AccountFile {
    //Simulates reading from a file. Replace with actual file I/O.
    public Account getAccount(String accountId) {
        //Replace with actual file reading logic
        if (accountId.equals("ACCT456") || accountId.equals("ACCT789")) {
            return new Account(accountId, "CUST123");
        }
        return null;
    }
}

class StandingOrderValidator {
    public boolean validate(StandingOrder order) {
        if (order.amount < 0) {
            System.out.println("Error: Amount must be positive.");
            return false;
        }
        if (!order.frequency.equals("MONTHLY") && !order.frequency.equals("WEEKLY")) {
            System.out.println("Error: Invalid frequency.");
            return false;
        }
        return true;
    }
}

class DMSDataStore {
    private DMS dms; //Dependency Injection

    public DMSDataStore(DMS dms) {
        this.dms = dms;
    }

    public boolean createStandingOrder(StandingOrder order) {
        //Simulates interaction with the database. Replace with actual database interaction
        System.out.println("Storing Standing Order in DMS: " + order.standingOrderId);
        return dms.storeRecord(order); // Delegate to DMS for actual storage

    }

    public StandingOrder getStandingOrder(String standingOrderId) {
        //Simulates database retrieval.  Replace with actual database interaction
        System.out.println("Retrieving Standing Order from DMS: " + standingOrderId);
        return dms.getRecord(standingOrderId);
    }

    // Add methods for modifyStandingOrder etc.

}

class DMS {
    public boolean storeRecord(StandingOrder order) {
        // Simulate database storage - replace with actual database code.
        return true; // Replace with appropriate error handling and return values
    }

    public StandingOrder getRecord(String standingOrderId) {
        //Simulate database retrieval - replace with actual database code
        return new StandingOrder(standingOrderId, null, null, 0, "", LocalDate.now()); //Replace with actual data
    }
    // Add methods for modifyRecord etc.
}


// Application Class
class StandingOrderSystem {
    private CustomerFile customerFile;
    private AccountFile accountFile;
    private StandingOrderValidator validator;
    private DMSDataStore dmsDataStore;
    private Scanner scanner;

    public StandingOrderSystem(CustomerFile customerFile, AccountFile accountFile, StandingOrderValidator validator, DMSDataStore dmsDataStore) {
        this.customerFile = customerFile;
        this.accountFile = accountFile;
        this.validator = validator;
        this.dmsDataStore = dmsDataStore;
        this.scanner = new Scanner(System.in);
    }

    public void run() {
        String customerId = getCustomerIdFromUser();
        Customer customer = customerFile.getCustomer(customerId);
        if (customer == null) {
            System.out.println("Customer not found.");
            return;
        }

        Account fromAccount = getAccountFromUser("From", customer);
        if (fromAccount == null) return;

        Account toAccount = getAccountFromUser("To", customer);
        if (toAccount == null) return;

        StandingOrder order = getStandingOrderDetailsFromUser(fromAccount, toAccount);
        if (order == null) return;


        if (order.isValid(validator) && dmsDataStore.createStandingOrder(order)) {
            System.out.println("Standing order created successfully.");
        } else {
            System.out.println("Failed to create standing order.");
        }
    }

    private String getCustomerIdFromUser() {
        System.out.print("Enter Customer ID: ");
        return scanner.nextLine();
    }


    private Account getAccountFromUser(String accountType, Customer customer) {
        System.out.print("Enter " + accountType + " Account ID: ");
        String accountId = scanner.nextLine();
        Account account = accountFile.getAccount(accountId);
        if (account == null) {
            System.out.println(accountType + " Account not found.");
            return null;
        }
        if (!account.getCustomerId().equals(customer.getCustomerId())) {
            System.out.println(accountType + " Account does not belong to customer.");
            return null;
        }
        return account;
    }


    private StandingOrder getStandingOrderDetailsFromUser(Account fromAccount, Account toAccount) {
        System.out.print("Enter Standing Order ID: ");
        String standingOrderId = scanner.nextLine();
        System.out.print("Enter Amount: ");
        double amount = scanner.nextDouble();
        scanner.nextLine(); // Consume newline
        System.out.print("Enter Frequency (MONTHLY, WEEKLY): ");
        String frequency = scanner.nextLine();
        System.out.print("Enter Next Execution Date (YYYY-MM-DD): ");
        String nextExecutionDateStr = scanner.nextLine();
        LocalDate nextExecutionDate;
        try {
            nextExecutionDate = LocalDate.parse(nextExecutionDateStr, DateTimeFormatter.ISO_DATE);
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date format. Please use YYYY-MM-DD.");
            return null;
        }
        return new StandingOrder(standingOrderId, fromAccount, toAccount, amount, frequency, nextExecutionDate);
    }
}

public class Main {
    public static void main(String[] args) {
        CustomerFile customerFile = new CustomerFile();
        AccountFile accountFile = new AccountFile();
        StandingOrderValidator validator = new StandingOrderValidator();
        DMS dms = new DMS(); //Create the DMS object
        DMSDataStore dmsDataStore = new DMSDataStore(dms); // Inject DMS into DMSDataStore
        StandingOrderSystem system = new StandingOrderSystem(customerFile, accountFile, validator, dmsDataStore);
        system.run();
    }
}
```