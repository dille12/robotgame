from robot_parts.part import Part
from numpy import array as v2
from robot_parts.module import Module
import math
import numpy
import core.func
import time
import random
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
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.shift_gear_tick = self.g.GT(12, oneshot=True)
        self.keypresses = []
        self.battery_left = 1
        self.enemy = None

    def engine_sound(self):
        self.speed_ratio = min([abs(self.vel)/self.top_speed, 1])
        sound = self.g.engine[round(self.speed_ratio * (len(self.g.engine)-1))]
        if sound.get_num_channels() == 0:
            for x in self.g.engine:
                x.stop()
            sound.play(loops = -1)

    def drive_AI(self):
        self.acceleration = self.track_power / (self.total_mass*9.81*30)
        self.top_speed = self.acceleration/(0.01010101)

        if not self.enemy:
            for x in self.g.parts:
                if x.core and x.player_controlled:
                    self.enemy = x
                    break
        try:
            delta = self.enemy.pos - self.pos
        except:
            return
        angle_to_enemy = -math.degrees(math.atan2(delta[1], delta[0]))
        distance_to_enemy = core.func.get_dist_points(self.pos, self.enemy.pos)

        angle_diff = core.func.get_angle_diff(self.angle, angle_to_enemy)

        if angle_diff > 25:
            self.angular_vel -= self.acceleration*3
        else:
            self.angular_vel += self.acceleration*3


        if distance_to_enemy > 900:
            self.vel += self.acceleration
        elif distance_to_enemy < 700:
            self.vel -= self.acceleration
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


        self.acceleration = self.track_power / (self.total_mass*9.81*30)
        self.top_speed = self.acceleration/(0.01010101)

        self.engine_sound()

        if not self.shift_gear_tick.tick():
            return

        if "s" in self.g.keypress_held_down:
            self.vel -=  self.acceleration
            self.g.battery_consumption += self.track_power / 216000

        elif "w" in self.g.keypress_held_down:
            self.vel += self.acceleration
            self.g.battery_consumption += self.track_power / 216000

        if "a" in self.g.keypress_held_down:
            self.angular_vel += self.acceleration*3 if "s" not in self.g.keypress_held_down else -self.acceleration*3
            self.g.battery_consumption += self.track_power / 216000

        elif "d" in self.g.keypress_held_down:
            self.angular_vel -= self.acceleration*3 if "s" not in self.g.keypress_held_down else -self.acceleration*3
            self.g.battery_consumption += self.track_power / 216000









class BigCore(Core):
    def __init__(self, game, pos):
        self.image = game.images["core_temp"]
        self.name = "Large Core"

        super().__init__(game, pos)

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
        self.track_power = 12000 #watt
        self.tracks = self.g.images["tracks"][self.g.zoom]
        self.desc["Track power: "] = ["track_power", "W"]

class SmallCore(Core):
    def __init__(self, game, pos):
        self.image = game.image("tank")

        self.name = "Small Core"
        self.random_hue = random.randint(0,360)


        super().__init__(game, pos)


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
        self.track_power = 4000 #watt
        self.tracks = self.g.image("tracks")[self.g.zoom]
        t = time.perf_counter()
        self.color(self.random_hue)
        print(time.perf_counter() - t)

        self.desc["Track power: "] = ["track_power", "W"]
