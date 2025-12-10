```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Optional;

// Data Transfer Objects (DTOs) mirroring COBOL copybooks.  Replace with actual field types.
class StandingOrderRecord {
    String standingOrderId;
    String customerId;
    String fromAccountId;
    String toAccountId;
    double amount;
    String frequency;
    LocalDate nextExecutionDate;
    String status;

    // Constructor, getters, and setters
    public StandingOrderRecord(String standingOrderId, String customerId, String fromAccountId, String toAccountId, double amount, String frequency, LocalDate nextExecutionDate, String status) {
        this.standingOrderId = standingOrderId;
        this.customerId = customerId;
        this.fromAccountId = fromAccountId;
        this.toAccountId = toAccountId;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
        this.status = status;
    }

    // Getters and Setters
    public String getStandingOrderId() { return standingOrderId; }
    public void setStandingOrderId(String standingOrderId) { this.standingOrderId = standingOrderId; }
    // ... (Getters and setters for other fields) ...

}

class CustomerRecord {
    String customerId;
    String name;
    String address;
    LocalDate lastModifiedDate;

    // Constructor, getters, and setters
}

class AccountRecord {
    String accountId;
    String customerId;
    double balance;
    String accountType;

    // Constructor, getters, and setters
}


// Database Interaction Classes (replace with actual database implementations)
class CustomerDatabase {
    Optional<CustomerRecord> getCustomer(String customerId) {
        // Replace with actual database query
        return Optional.empty();
    }

    void updateCustomer(CustomerRecord customer) {
        // Replace with actual database update
    }
}

class AccountDatabase {
    Optional<AccountRecord> getAccount(String accountId) {
        // Replace with actual database query
        return Optional.empty();
    }
}

class StandingOrderDatabase {
    String storeStandingOrder(StandingOrderRecord standingOrder) {
        // Replace with actual database insert.  Return unique ID or error message
        return "SO12345";
    }

    Optional<StandingOrderRecord> retrieveStandingOrder(String standingOrderId) {
        // Replace with actual database query
        return Optional.empty();
    }

    void updateStandingOrder(StandingOrderRecord standingOrder) {
        // Replace with actual database update
    }
}

// Validation Class
class StandingOrderValidator {
    boolean isValid(StandingOrderRecord so) {
        return so.amount > 0 && (so.frequency.equals("MONTHLY") || so.frequency.equals("WEEKLY"));
    }

    String getErrorMessage(StandingOrderRecord so) {
        if (so.amount <= 0) return "Amount must be positive.";
        if (!so.frequency.equals("MONTHLY") && !so.frequency.equals("WEEKLY")) return "Invalid frequency.";
        return null;
    }
}


// Facade Class
class StandingOrderProcessor {
    private final CustomerDatabase customerDb;
    private final AccountDatabase accountDb;
    private final StandingOrderDatabase standingOrderDb;
    private final StandingOrderValidator validator;

    public StandingOrderProcessor(CustomerDatabase customerDb, AccountDatabase accountDb,
                                 StandingOrderDatabase standingOrderDb, StandingOrderValidator validator) {
        this.customerDb = customerDb;
        this.accountDb = accountDb;
        this.standingOrderDb = standingOrderDb;
        this.validator = validator;
    }

    String createStandingOrder(String customerId, String fromAccountId, String toAccountId,
                              double amount, String frequency, String nextExecutionDateString) {
        try {
            LocalDate nextExecutionDate = LocalDate.parse(nextExecutionDateString, DateTimeFormatter.ISO_DATE);
            StandingOrderRecord so = new StandingOrderRecord(null, customerId, fromAccountId, toAccountId, amount, frequency, nextExecutionDate, "ACTIVE");


            Optional<CustomerRecord> customer = customerDb.getCustomer(customerId);
            Optional<AccountRecord> fromAccount = accountDb.getAccount(fromAccountId);
            Optional<AccountRecord> toAccount = accountDb.getAccount(toAccountId);

            if (customer.isEmpty() || fromAccount.isEmpty() || toAccount.isEmpty() || !customer.get().customerId.equals(fromAccount.get().customerId) || !customer.get().customerId.equals(toAccount.get().customerId)) {
                return "Customer or account not found, or account mismatch.";
            }


            if (!validator.isValid(so)) {
                return validator.getErrorMessage(so);
            }

            String standingOrderId = standingOrderDb.storeStandingOrder(so);
            customerDb.updateCustomer(customer.get()); //Update customer last modified date
            return "Standing order created successfully. ID: " + standingOrderId;

        } catch (DateTimeParseException e) {
            return "Invalid date format. Use YYYY-MM-DD";
        } catch (Exception e) {
            return "Error creating standing order: " + e.getMessage();
        }
    }
}


public class Main {
    public static void main(String[] args) {
        // Initialize database and validator objects
        CustomerDatabase customerDb = new CustomerDatabase();
        AccountDatabase accountDb = new AccountDatabase();
        StandingOrderDatabase standingOrderDb = new StandingOrderDatabase();
        StandingOrderValidator validator = new StandingOrderValidator();

        StandingOrderProcessor processor = new StandingOrderProcessor(customerDb, accountDb, standingOrderDb, validator);

        // Example usage
        String result = processor.createStandingOrder("CUST123", "ACCT456", "ACCT789", 100.0, "MONTHLY", "2024-03-15");
        System.out.println(result);
    }
}
```