class WageIndexTable:
    def __init__(self, wage_indices=None):
        self.wage_indices = wage_indices if wage_indices else []

    def add_wage_index(self, wage_index):
        self.wage_indices.append(wage_index)

    def get_wage_index(self, cbsa_code, period):
        for wage_index in self.wage_indices:
            if wage_index.cbsa == cbsa_code and wage_index.period == period:
                return wage_index
        return None