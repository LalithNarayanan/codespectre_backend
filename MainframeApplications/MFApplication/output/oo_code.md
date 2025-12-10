```java
// ValidationResult.java
class ValidationResult {
    String returnCode;
    String message;

    public ValidationResult(String returnCode, String message) {
        this.returnCode = returnCode;
        this.message = message;
    }

    @Override
    public String toString() {
        return "ValidationResult{" +
                "returnCode='" + returnCode + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
}

// StandingOrder.java
class StandingOrder {
    String customerId;
    String fromAccount;
    String toAccount;
    String standingOrderId;
    double amount;
    String frequency;
    String nextExecutionDate;
    String dbKey;
    ValidationResult validationResult;


    public StandingOrder(String customerId, String fromAccount, String toAccount, String standingOrderId, double amount, String frequency, String nextExecutionDate) {
        this.customerId = customerId;
        this.fromAccount = fromAccount;
        this.toAccount = toAccount;
        this.standingOrderId = standingOrderId;
        this.amount = amount;
        this.frequency = frequency;
        this.nextExecutionDate = nextExecutionDate;
    }

    public ValidationResult getValidationResult() {
        return validationResult;
    }

    public void setValidationResult(ValidationResult validationResult) {
        this.validationResult = validationResult;
    }

    // Getters and setters for all attributes
    public String getCustomerId() { return customerId;}
    // ... other getters and setters ...

}


// StandingOrderValidator.java
class StandingOrderValidator {
    public ValidationResult validate(StandingOrder standingOrder) {
        if (standingOrder.amount <= 0) {
            return new ValidationResult("ERR001", "Amount must be greater than zero.");
        }
        if (!standingOrder.frequency.matches("^(DAILY|WEEKLY|MONTHLY)$")) {
            return new ValidationResult("ERR002", "Invalid frequency.  Must be DAILY, WEEKLY, or MONTHLY.");
        }
        return new ValidationResult("OK", "Standing order is valid.");
    }
}

// DatabaseInterface.java
interface DatabaseInterface {
    String storeStandingOrder(StandingOrder standingOrder);
    // Add other database interaction methods as needed.
}


// SqlDatabase.java
class SqlDatabase implements DatabaseInterface {
    @Override
    public String storeStandingOrder(StandingOrder standingOrder) {
        // Simulate database interaction. Replace with actual database code.
        System.out.println("Storing standing order in SQL database: " + standingOrder.standingOrderId);
        //Simulate updating customer last modified date.
        System.out.println("Updating customer last modified date for customer ID: " + standingOrder.customerId);
        return "OK"; // Or return an error code as needed.
    }
}


// UserInterface.java
interface UserInterface {
    StandingOrder collectStandingOrderData();
    void displayMessage(String message);
}

// ConsoleUI.java
class ConsoleUI implements UserInterface {
    @Override
    public StandingOrder collectStandingOrderData() {
        //Implementation to collect data from console.  Replace with actual implementation.
        System.out.println("Enter Customer ID:");
        String customerId = "123"; //Replace with scanner input

        // ... collect other data ...
        return new StandingOrder(customerId, "ACCT1", "ACCT2", "SO123", 100.0, "MONTHLY", "2024-10-26");
    }

    @Override
    public void displayMessage(String message) {
        System.out.println(message);
    }
}


// STORDSET.java
class STORDSET {
    public static void main(String[] args) {
        UserInterface ui = new ConsoleUI();
        StandingOrderValidator validator = new StandingOrderValidator();
        DatabaseInterface db = new SqlDatabase();

        StandingOrder so = ui.collectStandingOrderData();
        ValidationResult result = validator.validate(so);
        so.setValidationResult(result);

        if (result.returnCode.equals("OK")) {
            String dbResult = db.storeStandingOrder(so);
            ui.displayMessage("Standing order stored successfully. DB Result: " + dbResult);
        } else {
            ui.displayMessage("Error storing standing order: " + result.message);
        }
    }
}


//STORDVAL - functionality within StandingOrderValidator
//DMSSTORE - functionality within SqlDatabase.storeStandingOrder

```