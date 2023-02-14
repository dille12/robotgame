from robot_parts.part import Part
from numpy import array as v2
import math
import pygame
import core.func
from projectiles.projectile import Projectile
import random
from hud_elements.battle_info import BattleInfo


class Turret(Part):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        self.modular = True
        self.battery_life = 0
        self.modular_type = "Weapon"

        self.ammo_in_clip = 0
        self.reload_tick = self.g.GT(120, oneshot = True)
        self.reload_tick.max_out()

        self.recoil = 2

        self.firing_tick = 0

        self.desc["Projectile Caliper: "] = ["bullet_caliper", "mm"]
        self.desc["Rounds Per Minute: "] = ["rpm", "r/m"]
        self.desc["Rounds In Clip: "] = ["clip_size", "r"]
        self.desc["Max Rotation: "] = ["turn_radius", " degrees"]
        self.desc["Rotation speed: "] = ["turn_speed_second", " degrees/s"]
        self.desc["Turning Power: "] = ["turn_power", "W"]
        self.desc["Firing Power: "] = ["firing_power", "W"]

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

        if ("mouse0" in self.g.keypress_held_down or not self.player_controlled) and self.firing_tick <= 0:

            if not self.player_controlled:
                if self.highest_parent:
                    if self.highest_parent.enemy:
                        distance_to_enemy = core.func.get_dist_points(self.highest_parent.enemy.pos, self.highest_parent.pos)
                        if distance_to_enemy > 1000:
                            return

            self.firing_tick += 1/(self.rpm/3600)
            self.g.sounds[self.sound].stop()
            self.g.sounds[self.sound].play()
            self.g.vibrate(self.shake)
            self.g.bullets.append(Projectile(self.highest_parent, self.g, self.g.rev_campos(pos), 270-angle - self.turn + random.uniform(-self.recoil, self.recoil), caliper = self.bullet_caliper))
            self.ammo_in_clip -= 1
            self.g.battery_consumption += self.firing_power * (self.rpm/216000)



    def tick_weapons(self, pos, angle):

        angle = angle % 360
        dont_fire = False
        if self.player_controlled:
            delta = self.g.mouse_pos - pos
        else:
            if self.highest_parent:
                if self.highest_parent.enemy:
                    delta = self.g.campos(self.highest_parent.enemy.pos - pos)




        angle_to_mouse = math.atan2(delta[1], delta[0])
        if self.player_controlled:
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
            if self.player_controlled:
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
            self.g.battery_consumption += self.turn_power / 216000
        else:
            self.turn -= self.turn_speed
            self.g.battery_consumption += self.turn_power / 216000

        if self.firing_tick > 0:
            self.firing_tick -= 1





class KineticCannon(Turret):
    def __init__(self, game, pos):
        self.image = game.images["turret"]
        self.name = "Kinetic Cannon"

        super().__init__(game, pos)
        self.bullet_caliper = 25
        self.description = "Slow cannon with high caliper."
        self.rpm = 98
        self.clip_size = 10
        self.mass = 45
        self.turn_radius = 45
        self.sound = "cannon_fire_large"
        self.shake = 5
        self.firing_power = 1750
        self.turn_power = 75
        self.turn_speed = 0.35
        self.turn_speed_second = self.turn_speed*60
        self.center = v2([10,78])

class Railgun(Turret):
    def __init__(self, game, pos):
        self.image = game.images["railgun"]
        self.name = "M1 Railgun"

        super().__init__(game, pos)
        self.bullet_caliper = 250
        self.description = "Massive but destructive cannon."
        self.rpm = 60
        self.clip_size = 5
        self.mass = 100
        self.turn_radius = 38
        self.sound = "railgun_large"
        self.shake = 10
        self.firing_power = 5000
        self.turn_power = 150
        self.turn_speed = 0.25
        self.turn_speed_second = self.turn_speed*60
        self.center = v2([19,95])

class LMG(Turret):
    def __init__(self, game, pos):
        self.image = game.images["turret_machine"]
        self.name = "Light Machine Gun"

        super().__init__(game, pos)
        self.bullet_caliper = 3
        self.description = "Light cannon for small targets."
        self.rpm = 300
        self.clip_size = 30
        self.mass = 30
        self.turn_radius = 40
        self.sound = "cannon_fire_small"
        self.shake = 0.5
        self.firing_power = 50
        self.turn_power = 25
        self.turn_speed = 0.3
        self.turn_speed_second = self.turn_speed*60
        self.center = v2([10,50])
        self.recoil = 10





class MachineGun(Turret):
    def __init__(self, game, pos):
        self.image = game.images["turret_machine"]
        self.name = "Machine Gun"

        super().__init__(game, pos)
        self.bullet_caliper = 4
        self.description = "Fast firing machine gun with low stopping power."
        self.mass = 30
        self.turn_radius = 70
        self.rpm = 567
        self.clip_size = 100
        self.sound = "cannon_fire_medium"
        self.shake = 2
        self.firing_power = 75
        self.turn_power = 50
        self.turn_speed = 0.65
        self.turn_speed_second = self.turn_speed*60
        self.center = v2([10,50])
        self.recoil = 4
