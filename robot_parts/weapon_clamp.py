from robot_parts.attachable import Attachable
from numpy import array as v2
from robot_parts.module import Module


class WeaponClamp(Attachable):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "Can attach weapons to walls."
        self.modular = False

        self.modules = (
                Module(v2([0,-5])),
                        )

        self.modular_compability = ["Weapon"]
        self.mass = 6
