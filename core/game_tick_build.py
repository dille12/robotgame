from hud_elements.build_hud import draw_build_hud
import pygame
import core.func
from numpy import array as v2
import numpy


def tick_build(game):
    dist = 10000
    parts_dist = {}
    parts_size = {}
    for core_part in game.parts:
        core_part.player_controlled = True
        if core_part.rect.collidepoint(game.mouse_pos):
            parts_dist[core.func.get_dist_points(core_part.pos, game.mouse_pos)] = core_part
        depth = core_part.recursive_get_parent_depth(0)
        if depth not in parts_size:
            parts_size[depth] = [core_part]
        else:
            parts_size[depth].append(core_part)
        core_part.closest = False
    if parts_dist:
        closest_part = parts_dist[min(parts_dist.keys())]
        closest_part.closest = True
    game.draw_modules_on_top.clear()
    for part_list in sorted(parts_size):
        for part in parts_size[part_list]:
            part.tick()

    not_connected = game.get_parts_not_connected()

    i = len(not_connected)
    for num, x in enumerate(not_connected):
        x.pos = v2([1650, game.res[1]/2 - i/2 * 60 + num * 60], dtype = numpy.float64)
        game.quicktext(x.name, 20, x.pos + [40,-5])
        for y in x.recursive_get_children(x, []):
            y.unset_parent()

    for x in game.draw_modules_on_top:
        rect = pygame.Rect(x[0], x[1],0,0)
        rect.inflate_ip(20,20)
        pygame.draw.rect(game.screen, [0,255,0], rect, 1)

    active_part = None
    for x in game.parts:
        if x.active and not x.moving and not x.rotate_turret:
            x.active_game_tick.tick()

            x.draw_info_box()

            break
        else:
            x.active_game_tick.value = 0


    draw_build_hud(game)
