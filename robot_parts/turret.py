from robot_parts.part import Part

class Turret(Part):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image)

        self.modular = True

        self.battery_life = 0
        self.mass = 45
        self.angle = 90

        self.modular_type = "Weapon"

        if center:
            self.center[0] = int(center[0])
            self.center[1] = int(center[1])
