import math
import pygame
import core.func
from numpy import array as v2
import numpy
import random
from projectiles.spark import Spark
from hud_elements.battle_info import BattleInfo


class Projectile:
    def __init__(self, owner, game, pos, angle):
        self.lifetime = 20
        self.g = game
        self.owner = owner
        self.angle = angle
        self.angle_rads = math.radians(angle)
        self.divisions = 10
        self.vector = v2([math.cos(self.angle_rads), math.sin(self.angle_rads)]) * 110 / self.divisions
        self.image, r = core.func.rot_center(self.g.images["bullet"][self.g.zoom], 270-self.angle, pos[0], pos[1])
        self.pos = v2([r.x, r.y], dtype=numpy.float64)
        self.mask = pygame.mask.from_surface(self.image)

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

            for part in self.g.parts:
                if part.mask and part.highest_parent != self.owner:
                    point = part.mask.overlap(self.mask, - part.maskpos + self.pos)
                    if point:
                        v = v2(point)
                        #part.info = BattleInfo(self.g.campos(part.pos + v), part, part.g, [255,255,0], "IMPACT")
                        #(pos, self, self.g, [255,0,0], "Reloading 0%")
                        self.kill()

                        for i in range(random.randint(10, 30)):
                            Spark(part.maskpos + point, self.g, angle = self.angle)

                        return

            self.g.screen.blit(self.image, self.g.campos(self.pos))


        if self.lifetime < 0:
            self.kill()
