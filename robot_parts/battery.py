from robot_parts.part import Part

class Battery(Part):
    def __init__(self, game, pos):
        self.image = game.images["battery"]
        self.name = "Li-ion Battery"

        super().__init__(game, pos)
        self.description = "Small Li-ion battery."
        self.modular = True
        self.battery_life = 1500
        self.mass = 13
        self.modular_type = "Part"
