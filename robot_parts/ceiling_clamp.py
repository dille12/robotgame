from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module


class CeilingClamp(Part):
    def __init__(self, game, pos):
        self.image = game.images["turret_ceiling"]
        self.name = "Ceiling Clamp"
        
        super().__init__(game, pos)

        self.description = "Can link cannons to modules."
        self.modular = True

        self.modules = (
                Module(v2([0,0])),
                        )
        self.modular_type = "Part"
        self.modular_compability = ["Weapon"]
        self.mass = 4.5
