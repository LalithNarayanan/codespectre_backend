# import os 
# import shutil 
# import zipfile 
# import tempfile 
from pathlib import Path 
from typing import List, Dict, Union, Optional 

from fastapi import FastAPI, UploadFile, File, HTTPException 
from fastapi.responses import JSONResponse


# app = FastAPI()


def list_directory_contents(path: Path) -> Union[Dict, List]:
    
    if not path.is_dir():
        return {"name": path.name, "type" : "file"}
    contents = [] 
    for item in sorted(path.iterdir()):
        if item.is_dir():
            contents.append({
                     "name" : item.name,
                     "type":"folder",
                     "contents": list_directory_contents(item)
                 })
        else:
            contents.append({
                "name": item.name,
                "type":"file"
            })
    return contents


### to get list of programs in the logical unit

def programs_list_logical_unit(file_content):
    programs =[]
    for log_unit in file_content:
        for prgm in log_unit.get('programs'):
            programs.append(f"{log_unit.get('id')} - {prgm}")
    return programs




#### sample mermaid class diagram code
def sample_mermaid_class_diagram():
    return """
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
            """.strip()


    
        
















