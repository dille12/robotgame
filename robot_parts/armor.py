from robot_parts.attachable import Attachable
import projectiles.projectile

class ArmorPlate(Attachable):
    def __init__(self, game, pos):
        self.image = game.images["armor"]
        super().__init__(game, pos)
        self.desc["Vickers Hardness: "] = ["HV", ""]
        self.desc["Maximum angle for ricochet: "] = ["approx_angle_of_insertion", ""]


    def get_approx_angle(self):
        for angle in range(5,90,1):
            if not projectiles.projectile.projectile_ricochet(1, 10, 40, self.HV, angle):
                self.approx_angle_of_insertion = angle
                break


class SteelArmor(ArmorPlate):
    def __init__(self, game, pos):
        self.name = "Steel Armorplate"

        super().__init__(game, pos)
        self.mass = 12
        self.HV = 100
        self.description = "Simple steel armor plate."
        self.get_approx_angle()

class AluminumAlloyArmor(ArmorPlate):
    def __init__(self, game, pos):
        self.name = "Aluminium Alloy Armor"

        super().__init__(game, pos)
        self.mass = 5
        self.HV = 130
        self.description = "Lighter but weaker armor."
        self.get_approx_angle()

class CarbonCompositeArmor(ArmorPlate):
    def __init__(self, game, pos):
        self.name = "Composite Armor"

        super().__init__(game, pos)
        self.mass = 3
        self.HV = 150
        self.description = "Ultralight and resistant armor."
        self.get_approx_angle()
