from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module

class Core(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "A larger core for larger robots."
        self.core = True
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
        self.mass = 225
        self.modular_compability = ["Part"]
        self.track_power = 500 #watt
        self.tracks = self.g.images["tracks"][self.g.zoom]
        self.desc["Track power: "] = ["track_power", "W"]

class SmallCore(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "A small beginner robotcore."
        self.core = True
        self.modular = False
        self.extendable = True
        self.modules = (Module(v2([0,0])),
                        Module(v2([-50,0])),
                        Module(v2([50,0])),
                        )
        self.battery_life = 750
        self.mass = 125
        self.modular_compability = ["Part"]
        self.track_power = 250 #watt
        self.tracks = self.g.images["tracks"][self.g.zoom]
        self.desc["Track power: "] = ["track_power", "W"]
