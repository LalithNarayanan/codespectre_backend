class WageIndex:
    def __init__(self, cbsa, msa=None, period=None, index_value=None):
        self.cbsa = cbsa  # CBSA object or code
        self.msa = msa  # MSA object or code
        self.period = period  # Effective date or period
        self.indexValue = index_value