from robot_parts.part import Part

class Battery(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "Small Li-ion battery."
        self.modular = True
        self.battery_life = 1500
        self.mass = 13
        self.modular_type = "Part"
