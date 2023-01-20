
from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module
from robot_parts.attachable import Attachable



class Rack(Attachable):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)

        self.modular = False

        self.extendable = True

        self.modules = (Module(v2([-25,-25])),
                        Module(v2([25,-25])),
                        Module(v2([-25,25])),
                        Module(v2([25,25])),
                        )
        self.battery_life = 100
        self.mass = 10

        self.modular_compability = ["Part"]
