
from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module
from robot_parts.attachable import Attachable



class Rack(Attachable):
    def __init__(self, game, pos):
        self.image = game.images["rack"]
        self.name = "Rack"
        
        super().__init__(game, pos)

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
