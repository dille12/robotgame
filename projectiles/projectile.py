import math
import pygame
import core.func
from numpy import array as v2
import numpy

class Projectile:
    def __init__(self, game, pos, angle):
        self.g = game
        self.angle = angle
        self.angle_rads = math.radians(angle)
        self.vector = v2([math.cos(self.angle_rads), math.sin(self.angle_rads)]) * 110
        self.image, r = core.func.rot_center(self.g.images["bullet"][self.g.zoom], 270-self.angle, pos[0], pos[1])
        self.pos = v2([r.x, r.y], dtype=numpy.float64)

    def tick(self):
        self.pos += self.vector
        self.g.screen.blit(self.image, self.pos)
