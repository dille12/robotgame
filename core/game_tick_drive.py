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
        if "d" in game.keypress_held_down:
            x.angle -= 1

        if "a" in game.keypress_held_down:
            x.angle += 1

        rads = 2*math.pi - math.radians(x.angle)

        if "w" in game.keypress_held_down:
            x.pos += 3 * v2([math.cos(rads) * 3, math.sin(rads) * 3], dtype=numpy.float64)

        elif "s" in game.keypress_held_down:
            x.pos -= 3 * v2([math.cos(rads) * 3, math.sin(rads) * 3], dtype=numpy.float64)

        x.tick_drive()

    game.quicktext(f"{game.camera_pos}", 30, [10,10])
