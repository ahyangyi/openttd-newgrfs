class ACargo:
    def __init__(self, label, cargo_class, capacity_multiplier=0x100, weight=16):
        self.label = label
        self.cargo_class = cargo_class
        self.capacity_multiplier = capacity_multiplier
        self.weight = weight
