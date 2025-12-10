class ReportGenerator:
    def generate_report(self, claims):
        #Logic to generate report based on claims data
        report = "Medicare Payment Report:\n"
        for claim in claims:
            report += f"Claim ID: {claim.billData['claim_id']}, Payment: {claim.calculate_payment()}\n"  #Example
        return report