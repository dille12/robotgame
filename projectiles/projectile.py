import math
import pygame
import core.func
from numpy import array as v2
import numpy
import random
from projectiles.spark import Spark
from hud_elements.battle_info import BattleInfo


class Projectile:
    def __init__(self, owner, game, pos, angle, caliper = 5):
        self.lifetime = 20
        self.g = game
        self.caliper = caliper
        self.owner = owner
        self.angle = angle
        self.angle_rads = math.radians(angle)
        self.divisions = 10
        self.vector = v2([math.cos(self.angle_rads), math.sin(self.angle_rads)]) * 110 / self.divisions
        self.image, r = core.func.rot_center(self.g.images["bullet"][self.g.zoom], 270-self.angle, pos[0], pos[1])
        self.pos = v2([r.x, r.y], dtype=numpy.float64)
        self.mask = pygame.mask.from_surface(self.image)
        self.HV = random.randint(35,45)

        self.energy = 1

    def kill(self):
        if self in self.g.bullets:
            self.g.bullets.remove(self)

    def tick(self):
        self.lifetime -= 1

        if self.lifetime > 18:
            self.pos += self.vector * self.divisions
            return

        for i in range(self.divisions):
            self.pos += self.vector

            self.center = self.pos + self.image.get_rect().center

            for depth in sorted(self.g.depth_sorted_parts, reverse = True):
                for part in self.g.depth_sorted_parts[depth]:
                    if part.mask and part.highest_parent != self.owner:
                        point = part.mask.overlap(self.mask, - part.maskpos + self.pos)
                        if point:
                            v = v2(point)
                            #part.info = BattleInfo(self.g.campos(part.pos + v), part, part.g, [255,255,0], "IMPACT")
                            #(pos, self, self.g, [255,0,0], "Reloading 0%")
                            self.kill()

                            impact_angle = part.impact_angle(self.center, part.maskpos + point, self.angle)
                            dam = True
                            if impact_angle:
                                angle = abs(core.func.get_angle_diff(self.angle, impact_angle)) - 45
                                if projectile_ricochet(1, 10, self.HV, part.HV, angle):
                                    self.g.bullets.append(Projectile(part, self.g, part.maskpos + point, impact_angle, self.caliper))
                                    dam = False
                                    self.g.sound("ricochet")
                            else:
                                impact_angle = self.angle

                            #self.g.impacts.append(part.maskpos + point)
                            if dam:
                                part.hull -= self.caliper

                            for i in range(random.randint(10, 30)):
                                Spark(part.maskpos + point, self.g, angle = impact_angle)

                            return

            self.g.screen.blit(self.image, self.g.campos(self.pos))


        if self.lifetime < 0:
            self.kill()


def projectile_ricochet(m_projectile, v_projectile, HV_projectile, HV_armor, angle_of_incidence):
    # Calculate the critical energy and angle for ricochet
    angle_of_incidence = math.radians(angle_of_incidence)
    E_critical = ((HV_armor**2)/(16*m_projectile)) * (math.cos(angle_of_incidence))**2
    # Check if the argument of asin is within the domain of [-1, 1]
    sin_argument = math.sqrt(HV_armor/HV_projectile)*math.sin(angle_of_incidence)
    if sin_argument >= 1:
        angle_critical = math.pi/2
    elif sin_argument <= -1:
        angle_critical = -math.pi/2
    else:
        angle_critical = math.asin(sin_argument)


    projectile_energy = (1/2) * m_projectile * v_projectile**2


    # Check if the projectile has enough energy to ricochet
    if 0 < angle_of_incidence < angle_critical and projectile_energy < E_critical:
        print("RICOCHET")
        return True
    else:
        print("NO RICOCHET")
        return False
