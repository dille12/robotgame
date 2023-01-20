from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module


class Core(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)

        self.modular = False

        self.extendable = True



        self.modules = (Module(v2([-75,-25])),
                        Module(v2([-25,-25])),
                        Module(v2([25,-25])),
                        Module(v2([75,-25])),
                        Module(v2([-75,25])),
                        Module(v2([-25,25])),
                        Module(v2([25,25])),
                        Module(v2([75,25])),
                        )


        self.battery_life = 1000
        self.mass = 20

        self.modular_compability = ["Part"]
