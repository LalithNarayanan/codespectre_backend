class Claim:
    def __init__(self, bill_data, provider, drg, payment_data, cbsa, pricer_options):
        self.billData = bill_data
        self.provider = provider
        self.drg = drg
        self.paymentData = payment_data
        self.cbsa = cbsa
        self.pricerOptions = pricer_options
        self.paymentCalculation = PaymentCalculation(self)  # Composition

    def calculate_payment(self):
        return self.paymentCalculation.calculate_payment()