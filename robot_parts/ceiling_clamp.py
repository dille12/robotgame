from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module


class CeilingClamp(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "Can link cannons to modules."
        self.modular = True

        self.modules = (
                Module(v2([0,0])),
                        )
        self.modular_type = "Part"
        self.modular_compability = ["Weapon"]
        self.mass = 4.5
