class RuralFloorFactorTable:
    def __init__(self, rural_floor_factors=None):
        self.rural_floor_factors = rural_floor_factors if rural_floor_factors else []

    def add_rural_floor_factor(self, rural_floor_factor):
        self.rural_floor_factors.append(rural_floor_factor)

    def get_rural_floor_factor(self, cbsa_code, effective_date):
        for factor in self.rural_floor_factors:
            if factor.cbsaCode == cbsa_code and factor.effectiveDate == effective_date:
                return factor
        return None