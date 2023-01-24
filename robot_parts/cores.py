from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module
import math
import numpy
def calc_acceleration2(speed, power, mass):
    friction = 0.01
    g = 9.8
    force = power / speed
    net_force = force - (mass * g * friction)
    acceleration = net_force / mass
    return acceleration

def shift_integrand(integrand, track_power, mass, shift = 0):
    def dec(x):
        return integrand(x, track_power, mass) - shift
    return dec


class Core(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.shift_gear_tick = self.g.GT(30, oneshot=True)
        self.keypresses = []


    def drive(self):
        for key in ["w", "s"]:
            if key in self.g.keypress_held_down:
                if key in self.keypresses:
                    continue

                else:
                    self.shift_gear_tick.value = 0
                    self.keypresses.append(key)
                    self.g.sounds["shift_gear"].play()
            elif key in self.keypresses:
                self.keypresses.remove(key)

        if not self.shift_gear_tick.tick():
            return

        if "s" in self.g.keypress_held_down:
            self.vel -= 0.25

        elif "w" in self.g.keypress_held_down:
            self.vel += 0.25

        if "a" in self.g.keypress_held_down:
            self.angular_vel += 0.25 if "s" not in self.g.keypress_held_down else -0.25
        if "d" in self.g.keypress_held_down:
            self.angular_vel -= 0.25 if "s" not in self.g.keypress_held_down else -0.25









class BigCore(Core):
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

class SmallCore(Core):
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
