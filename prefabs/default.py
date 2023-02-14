from numpy import array as v2
import numpy
import core.func
from prefabs.prebuilt import *

def build_prefab(game, parts, return_pos = [500,500]):

    parts = eval(parts)

    part_list = []

    for key in parts:
        parts[key][0] = parts[key][0].copy()


    for key in parts:
        part, parent_index, delta, angle = parts[key]
        part.g = game
        part.angle = angle
        if parent_index != None:
            parent = parts[parent_index][0]

            print("Tying part", part.name, "to", parent.name)
            part.set_parent(parent)
            part.delta_to_parent = v2(delta)
            parent.move_children()
            if part.modular:
                connect_to_module(part, parent)


        if part.core:
            core = part

        part_list.append(part)



    core.pos = v2(return_pos, dtype=numpy.float64)
    core.move_children()


    return part_list

def connect_to_module(part, parent):
    modules = parent.get_available_modules()
    dist = float("inf")
    m = None
    for x in modules:
        d = core.func.get_dist_points(x.vector, part.pos)
        if d < dist:
            dist = d
            m = x
    print("Connecting", part.name, "To Module")
    part.module = m
