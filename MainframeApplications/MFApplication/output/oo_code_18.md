```java
import java.time.LocalDate;
import java.util.Optional;

class StandingOrder {
    private final String customerId;
    private final String fromAccountId;
    private final String toAccountId;
    private final String standingOrderId;
    private final double amount;
    private final String frequency;
    private LocalDate nextExecutionDate;
    private LocalDate lastModifiedDate;

    public StandingOrder(String customerId, String fromAccountId, String toAccountId, String standingOrderId, double amount, String frequency, LocalDate nextExecutionDate) {
        this.customerId = customerId;
        this.fromAccountId = fromAccountId;
        this.toAccountId = toAccountId;
        this.standingOrderId = standingOrderId;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
        this.lastModifiedDate = LocalDate.now();
    }

    // Getters for all fields (omitted for brevity)

    public LocalDate getNextExecutionDate() {
        return nextExecutionDate;
    }

    public void setNextExecutionDate(LocalDate nextExecutionDate) {
        this.nextExecutionDate = nextExecutionDate;
    }


    @Override
    public String toString() {
        return "StandingOrder{" +
                "customerId='" + customerId + '\'' +
                ", fromAccountId='" + fromAccountId + '\'' +
                ", toAccountId='" + toAccountId + '\'' +
                ", standingOrderId='" + standingOrderId + '\'' +
                ", amount=" + amount +
                ", frequency='" + frequency + '\'' +
                ", nextExecutionDate=" + nextExecutionDate +
                ", lastModifiedDate=" + lastModifiedDate +
                '}';
    }
}

class Customer {
    private final String customerId;
    private final String name; //Optional

    public Customer(String customerId, String name) {
        this.customerId = customerId;
        this.name = name;
    }

    // Getters (omitted for brevity)

    public String getCustomerId() {
        return customerId;
    }
}

class Account {
    private final String accountId;
    private final String customerId;
    //private double balance; //Optional

    public Account(String accountId, String customerId) {
        this.accountId = accountId;
        this.customerId = customerId;
    }

    // Getters (omitted for brevity)

    public String getCustomerId() { return customerId; }
}

class StandingOrderValidator {
    public ValidationResult validate(StandingOrder standingOrder) {
        if (standingOrder.getAmount() < 0) {
            return new ValidationResult(false, "Amount must be positive.");
        }
        if (!standingOrder.getFrequency().equals("MONTHLY") && !standingOrder.getFrequency().equals("WEEKLY")) {
            return new ValidationResult(false, "Invalid frequency.");
        }
        return new ValidationResult(true, "");
    }

    static class ValidationResult {
        private final boolean isValid;
        private final String errorMessage;

        public ValidationResult(boolean isValid, String errorMessage) {
            this.isValid = isValid;
            this.errorMessage = errorMessage;
        }

        public boolean isValid() {
            return isValid;
        }

        public String getErrorMessage() {
            return errorMessage;
        }
    }
}


class DatabaseManager {
    // Simulate database interactions (replace with actual DB calls)
    public Optional<Customer> getCustomer(String customerId) {
        // Simulate DB lookup
        if (customerId.equals("123")) {
            return Optional.of(new Customer("123", "John Doe"));
        }
        return Optional.empty();
    }

    public Optional<Account> getAccount(String accountId) {
        // Simulate DB lookup
        if (accountId.equals("456")) {
            return Optional.of(new Account("456", "123"));
        }
        return Optional.empty();
    }

    public void storeStandingOrder(StandingOrder standingOrder) {
        System.out.println("Standing order stored: " + standingOrder);
    }

    public void modifyCustomer(Customer customer) {
        System.out.println("Customer modified: " + customer);
    }
}

class StandingOrderSetup {
    private final StandingOrderValidator validator;
    private final DatabaseManager dbManager;

    public StandingOrderSetup(StandingOrderValidator validator, DatabaseManager dbManager) {
        this.validator = validator;
        this.dbManager = dbManager;
    }

    public void setupStandingOrder() {
        //Simulate user input (replace with actual UI interaction)
        String customerId = "123";
        String fromAccountId = "456";
        String toAccountId = "789";
        String standingOrderId = "SO123";
        double amount = 100.0;
        String frequency = "MONTHLY";
        LocalDate nextExecutionDate = LocalDate.now().plusMonths(1);


        StandingOrder standingOrder = new StandingOrder(customerId, fromAccountId, toAccountId, standingOrderId, amount, frequency, nextExecutionDate);

        Optional<Customer> customer = dbManager.getCustomer(customerId);
        Optional<Account> fromAccount = dbManager.getAccount(fromAccountId);
        Optional<Account> toAccount = dbManager.getAccount(toAccountId);


        if (customer.isEmpty() || fromAccount.isEmpty() || toAccount.isEmpty() || !customer.get().getCustomerId().equals(fromAccount.get().getCustomerId())) {
            System.out.println("Error: Invalid customer or account information.");
            return;
        }

        StandingOrderValidator.ValidationResult validationResult = validator.validate(standingOrder);
        if (validationResult.isValid()) {
            dbManager.storeStandingOrder(standingOrder);
            dbManager.modifyCustomer(customer.get()); //Update last modified date
            System.out.println("Standing order setup successfully.");
        } else {
            System.out.println("Error: " + validationResult.getErrorMessage());
        }
    }
}

public class Main {
    public static void main(String[] args) {
        StandingOrderSetup setup = new StandingOrderSetup(new StandingOrderValidator(), new DatabaseManager());
        setup.setupStandingOrder();
    }
}
```