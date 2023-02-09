from robot_parts.attachable import Attachable
from numpy import array as v2
from robot_parts.module import Module


class WeaponClamp(Attachable):
    def __init__(self, game, pos):
        self.image = game.images["turret_base"]
        self.name = "Armament Clamp"
        super().__init__(game, pos)
        self.description = "Can attach weapons to walls."
        self.modular = False

        self.modules = (
                Module(v2([0,-5])),
                        )

        self.modular_compability = ["Weapon"]
        self.mass = 6
