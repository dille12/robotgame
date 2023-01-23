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
        children = x.recursive_get_children(x, [x])
        parts_by_depth = {}
        for child in children:
            depth = child.recursive_get_parent_depth(0)
            if depth not in parts_by_depth:
                parts_by_depth[depth] = [child]
            else:
                parts_by_depth[depth].append(child)

        for part_list in sorted(parts_by_depth):
            for part in parts_by_depth[part_list]:
                part.tick_drive()





    for x in game.bullets:
        x.tick()

    game.quicktext(f"{game.camera_pos}", 30, [10,10])
