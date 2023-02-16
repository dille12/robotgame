from numpy import array as v2
import math
import numpy
#from hud_elements.battle_hud import draw_rotated_rects
import random

from prefabs.default import build_prefab


def tick_drive(game):
    game.camera_movement()
    game.screen.blit(game.images["map"][game.zoom], game.campos((0,0)))
    cores = []

    for x in game.parts:
        if x.core:
            cores.append(x)
            if x.player_controlled:
                game.camera_pos_target = x.pos - game.res2/2

    if len(cores) == 1:

        for i in range(1,2):
            game.parts += build_prefab(game, random.choice(["ULTRALIGHT_MINI", "ULTRALIGHT_ATTACKER","DEFAULT_LIGHT_ATTACKER", "DEFAULT_MEDIUM_ATTACKER", "RAILGUNNER_LIGHT"]), [random.randint(0,2000),random.randint(0,2000)])

        game.depth_sorted_parts = game.sort_parts_by_depth()

    cores = []

    for x in game.parts:
        if x.core:
            cores.append(x)

    for x in cores:

        game.battery_consumption = 0
        children = x.recursive_get_children(x, [x])
        parts_by_depth = {}
        total_mass = 0
        total_battery_life = 0
        for child in children:
            total_mass += child.mass
            total_battery_life += child.battery_life
            depth = child.recursive_get_parent_depth(0)
            if depth not in parts_by_depth:
                parts_by_depth[depth] = [child]
            else:
                parts_by_depth[depth].append(child)

        x.total_mass = total_mass
        if x.player_controlled:
            x.drive()
        else:
            x.drive_AI()
        x.angle += (x.angular_vel * (1 - 0.5/(1+abs(x.vel))))
        rads = 2*math.pi - math.radians(x.angle)
        vector = x.vel* v2([math.cos(rads), math.sin(rads)], dtype=numpy.float64)
        x.pos += vector
        x.vel *= 0.99
        x.angular_vel *= 0.8

        for part_list in sorted(parts_by_depth):
            for part in parts_by_depth[part_list]:
                part.tick_drive()

                if part.player_controlled:
                    part.draw_rotated_rect()
                    game.battery_consumption += part.passive_consumption / 216000




        x.battery_left -= game.battery_consumption/total_battery_life

        if x.battery_left < 0:
            x.kill()

        if x.player_controlled:

            game.quicktext(f"{x.vel:.1f}m/s", 20, [1920-250,1080-50])
            game.quicktext(f"{x.total_mass:.1f}kg", 20, [1920-125,1080-50])
            game.quicktext(f"Battery: {x.battery_left * 100:.1f}%", 20, [1920-250,1080-250])




    for x in game.bullets:
        x.tick()

    for x in game.explosion_list:
        x.tick()

    for x in game.particles:
        x.tick()





    #game.quicktext(f"{game.camera_pos}", 30, [10,10])
    game.quicktext(f"{game.battery_consumption}", 30, [10,10])
