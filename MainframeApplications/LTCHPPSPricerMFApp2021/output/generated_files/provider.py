class Provider:
    def __init__(self, npi, provider_number, provider_specific_data, wage_index_data):
        self.npi = npi
        self.providerNumber = provider_number
        self.providerSpecificData = provider_specific_data
        self.wageIndexData = wage_index_data #Could be a list of WageIndex objects