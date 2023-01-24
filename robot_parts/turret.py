from robot_parts.part import Part
from numpy import array as v2
import math
import pygame
import core.func
from projectiles.projectile import Projectile
import random
from hud_elements.battle_info import BattleInfo


class Turret(Part):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image)

        self.modular = True
        self.battery_life = 0
        if center:
            self.center[0] = int(center[0])
            self.center[1] = int(center[1])

        self.modular_type = "Weapon"

        self.ammo_in_clip = 0
        self.reload_tick = self.g.GT(120, oneshot = True)
        self.reload_tick.max_out()

        self.recoil = 2

        self.firing_tick = 0

        self.desc["Projectile Caliper: "] = ["bullet_caliper", "mm"]
        self.desc["Rounds Per Minute: "] = ["rpm", "r/m"]
        self.desc["Rounds In Clip: "] = ["clip_size", "r"]

    def fire(self, pos, angle):

        if not self.reload_tick.tick():
            self.ammo_in_clip = self.clip_size
            if self.info:
                self.info.text = f"Reloading {round(self.reload_tick.value*100/self.reload_tick.max_value)}%"

            return

        if self.ammo_in_clip == 0 or ("r" in self.g.keypress):
            self.reload_tick.value = 0
            self.info = BattleInfo(pos, self, self.g, [255,0,0], "Reloading 0%")
            return

        if "mouse0" in self.g.keypress_held_down and self.firing_tick <= 0:
            self.firing_tick += 1/(self.rpm/3600)
            self.g.sounds[self.sound].stop()
            self.g.sounds[self.sound].play()
            self.g.vibrate(self.shake)
            self.g.bullets.append(Projectile(self.highest_parent, self.g, self.g.rev_campos(pos), 270-angle - self.turn + random.uniform(-self.recoil, self.recoil), caliper = self.bullet_caliper))
            self.ammo_in_clip -= 1



    def tick_weapons(self, pos, angle):

        angle = angle % 360

        delta = self.g.mouse_pos - pos
        angle_to_mouse = math.atan2(delta[1], delta[0])

        for a in [-self.turn_radius, self.turn_radius]:
            rad = math.radians(270 - (a + angle))
            vector = v2([math.cos(rad), math.sin(rad)])
            pos1 = vector * 25 + pos
            pos2 = vector * 75 + pos
            pygame.draw.line(self.g.screen, [0,255,0], pos1, pos2, 1)

        if core.func.angle_between_angles2(math.degrees(angle_to_mouse), 270 - (angle-self.turn_radius), 270 - (angle+self.turn_radius)):

            self.turn_target = core.func.get_angle_diff(0,  math.degrees(angle_to_mouse) + angle - 270)

            #self.quicktext(str(self.turn_target), 40, pos)
            dist = core.func.get_dist_points(pos, self.g.mouse_pos)
            rads = math.radians( - self.turn + 270 - angle)
            vector = v2([math.cos(rads), math.sin(rads)])
            for i in range(1, 11):

                pos1 = vector * dist/20 * i * 2 + pos
                pos2 = vector * dist/20 * (i*2+1)  + pos
                pygame.draw.line(self.g.screen, [0,255,0], pos1, pos2, 1)

            self.fire(pos, angle)

        else:
            self.turn_target = 0

        if abs(self.turn - self.turn_target) < self.turn_speed:
            self.turn = self.turn_target

        elif self.turn < self.turn_target:
            self.turn += self.turn_speed
        else:
            self.turn -= self.turn_speed

        if self.firing_tick > 0:
            self.firing_tick -= 1





class KineticCannon(Turret):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image, center = center)
        self.bullet_caliper = 25
        self.description = "Slow cannon with high caliper."
        self.rpm = 98
        self.clip_size = 10
        self.mass = 45
        self.turn_radius = 45
        self.sound = "cannon_fire_large"
        self.shake = 5





class MachineGun(Turret):
    def __init__(self, name, game, pos, image, center = None):
        super().__init__(name, game, pos, image, center = center)
        self.bullet_caliper = 7.62
        self.description = "Fast firing machine gun with low stopping power."
        self.mass = 30
        self.turn_radius = 70
        self.rpm = 567
        self.clip_size = 100
        self.sound = "cannon_fire_medium"
        self.shake = 2
