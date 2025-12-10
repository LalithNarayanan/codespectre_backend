class DRGTable:
    def __init__(self, drgs=None):
        self.drgs = drgs if drgs else []

    def add_drg(self, drg):
        self.drgs.append(drg)

    def get_drg(self, drg_code):
        for drg in self.drgs:
            if drg.drgCode == drg_code:
                return drg
        return None