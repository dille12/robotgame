import pygame
import math
import random
from numpy import array as v2
import numpy

class Spark:
    def __init__(self, pos, game, angle = None):
        self.g = game
        self.g.particles.append(self)
        self.pos = v2(pos, dtype = numpy.float64)
        if angle and random.randint(0,10) != 0:
            self.angle = math.radians(angle + random.randint(-30,30))
        else:
            self.angle = math.radians(random.randint(0,360))
        self.vector = v2([math.cos(self.angle), math.sin(self.angle)], dtype = numpy.float64) * random.randint(5,15)
        self.size = random.randint(3,8)
        self.max_lifetime = random.randint(8,16)
        self.lifetime = 0
        self.color = [255,255,0]

    def tick(self):
        self.pos += self.vector + v2([random.randint(-3,3), random.randint(-3,3)], dtype = numpy.float64)
        self.color[1] *= random.uniform(0.9,1)
        pygame.draw.rect(self.g.screen, self.color, (self.g.campos(self.pos), (self.size * (1 - self.lifetime/self.max_lifetime), self.size * (1 - self.lifetime/self.max_lifetime))))
        self.lifetime += 1
        if self.lifetime >= self.max_lifetime:
            self.g.particles.remove(self)
