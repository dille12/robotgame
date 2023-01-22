from robot_parts.part import Part

class Turret(Part):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image)

        self.modular = True
        self.battery_life = 0
        if center:
            self.center[0] = int(center[0])
            self.center[1] = int(center[1])

        self.modular_type = "Weapon"

        self.desc["Projectile Caliper: "] = ["bullet_caliper", "mm"]
        self.desc["Rounds Per Minute: "] = ["rpm", "r/m"]


class KineticCannon(Turret):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image, center = center)
        self.bullet_caliper = 25
        self.description = "Slow cannon with high caliper."
        self.rpm = 100

        self.mass = 45
        self.turn_radius = 25





class MachineGun(Turret):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image, center = center)
        self.bullet_caliper = 7.62
        self.description = "Fast firing machine gun with low stopping power."
        self.mass = 30
        self.turn_radius = 45
        self.rpm = 500
