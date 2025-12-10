class DRG:
    def __init__(self, drg_code, relative_weight, average_length_of_stay, description, ip_threshold=None, effective_date=None):
        self.drgCode = drg_code
        self.relativeWeight = relative_weight
        self.averageLengthOfStay = average_length_of_stay
        self.description = description
        self.ipThreshold = ip_threshold
        self.effectiveDate = effective_date