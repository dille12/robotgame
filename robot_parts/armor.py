from robot_parts.attachable import Attachable

class ArmorPlate(Attachable):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.desc["Flowstress: "] = ["flowstress", "MPa"]

class SteelArmor(ArmorPlate):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.mass = 12
        self.flowstress = 500
        self.description = "Simple steel armor plate."

class AluminumAlloyArmor(ArmorPlate):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.mass = 5
        self.flowstress = 400
        self.description = "Lighter but weaker armor."

class CarbonCompositeArmor(ArmorPlate):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.mass = 3
        self.flowstress = 900
        self.description = "Ultralight and resistant armor."
