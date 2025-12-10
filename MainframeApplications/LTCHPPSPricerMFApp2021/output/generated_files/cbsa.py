class CBSA:
    def __init__(self, cbsa_code, wage_index):
        self.cbsaCode = cbsa_code
        self.wageIndex = wage_index #Could be a list of WageIndex objects