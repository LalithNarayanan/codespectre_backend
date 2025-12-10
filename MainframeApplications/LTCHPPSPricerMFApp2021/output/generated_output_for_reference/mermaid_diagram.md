  
        classDiagram
    class MedicarePaymentCalculator {
        -fiscalYearStrategy : FiscalYearStrategy
        -providerTypeStrategy : ProviderTypeStrategy
        -drgTableManager : DRGTableManager
        -wageIndexManager : WageIndexManager
        +calculatePayment(billRecord : BillRecord) : PaymentSummary
    }

    class BillRecord {
        -attributes : ... // From BILL-NEW-DATA
    }

    class PaymentSummary {
        -attributes : ... // From PPS-DATA-ALL and PPS-PAYMENT-DATA
    }

    class DRGTableManager {
        -drgTables : DRGTable[]
        +getDRGData(drgCode : String, fiscalYear : int) : DRGData
    }

    class DRGTable {
        -fiscalYear : int
        -drgData : ...
        +lookupDRG(drgCode : String) : DRGData
    }

    class WageIndexManager {
        -wageIndexTables : WageIndexTable[]
        +getWageIndex(location : String, date : Date, providerType : String) : double
    }

    class WageIndexTable {
        -indexType : String
        -year : int
        -indexData : ...
    }

    class RuralFloorFactorTable {
        -data : ... //From RUFL200
    }

    class PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class LTCAL032Strategy extends PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class LTCAL162Strategy extends PaymentCalculationStrategy {
        +calculatePayment(billRecord : BillRecord, drgData : DRGData, wageIndex : double) : double
    }

    class FiscalYearStrategy {
        +getPaymentCalculationStrategy(fiscalYear : int) : PaymentCalculationStrategy
    }

    class ProviderTypeStrategy {
        +getPaymentCalculationStrategy(providerType : String) : PaymentCalculationStrategy
    }

    class DRGData {
        -weight : double
        -otherAttributes : ...
    }

    MedicarePaymentCalculator -- BillRecord : uses
    MedicarePaymentCalculator -- PaymentSummary : creates
    MedicarePaymentCalculator -- FiscalYearStrategy : uses
    MedicarePaymentCalculator -- ProviderTypeStrategy : uses
    MedicarePaymentCalculator -- DRGTableManager : uses
    MedicarePaymentCalculator -- WageIndexManager : uses

    DRGTableManager -- DRGTable : manages

    WageIndexManager -- WageIndexTable : manages

    FiscalYearStrategy .. PaymentCalculationStrategy : creates
    ProviderTypeStrategy .. PaymentCalculationStrategy : creates

    PaymentCalculationStrategy <|-- LTCAL032Strategy
    PaymentCalculationStrategy <|-- LTCAL162Strategy

    MedicarePaymentCalculator .. DRGData : uses
    MedicarePaymentCalculator .. Date : uses // Assuming 'Date' is a standard type

    PaymentCalculationStrategy .. BillRecord : uses
    PaymentCalculationStrategy .. DRGData : uses