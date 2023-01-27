from numpy import array as v2
import numpy
def build_prefab(game, parts):
    part_list = []
    for key in parts:
        part, parent_index, delta, angle = parts[key]
        part.g = game
        part.angle = angle
        if parent_index != None:
            print("Tying part", part.name, "to", parts[parent_index][0].name)
            part.set_parent(parts[parent_index][0])
            part.delta_to_parent = v2(delta)
        if part.core:
            core = part

        part_list.append(part)


    core.pos = v2([300,300], dtype=numpy.float64)
    core.move_children()

    return part_list
