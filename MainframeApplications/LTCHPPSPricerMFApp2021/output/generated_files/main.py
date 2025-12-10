from claim import Claim
from provider import Provider
from drg import DRG
from cbsa import CBSA
from wage_index import WageIndex
from payment_calculation import PaymentCalculation
from report_generator import ReportGenerator

# Example Usage
bill_data = {"claim_id": 123, "length_of_stay": 5, "cost": 5000}
provider = Provider("12345", "ABC", {"some": "data"}, [WageIndex("12345", index_value=1.0)])
drg = DRG("001", 1.0, 4, "DRG Description", ip_threshold=3)
payment_data = {"base_payment": 5000}
cbsa = CBSA("12345", provider.wageIndexData[0])
pricer_options = {"blend_year": False}

claim = Claim(bill_data, provider, drg, payment_data, cbsa, pricer_options)
report_generator = ReportGenerator()
report = report_generator.generate_report([claim])
print(report)


```