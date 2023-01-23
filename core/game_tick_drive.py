from numpy import array as v2
import math
import numpy

def tick_drive(game):
    game.camera_movement()
    game.screen.blit(game.images["map"][game.zoom], game.campos((0,0)))
    cores = []
    for x in game.parts:
        if x.core:
            cores.append(x)
            game.camera_pos_target = x.pos - game.res2/2

    for x in cores:

        x.drive()
        x.angle += x.angular_vel
        rads = 2*math.pi - math.radians(x.angle)
        vector = x.vel* v2([math.cos(rads), math.sin(rads)], dtype=numpy.float64)
        x.pos += vector
        x.vel *= 0.95
        x.angular_vel *= 0.8
        x.tick_drive()

    game.quicktext(f"{game.camera_pos}", 30, [10,10])
