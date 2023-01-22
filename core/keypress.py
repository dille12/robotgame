import pygame
import core.func
import sys
from numpy import array as v2
import numpy

def key_press_manager(obj):

    obj.mouse_pos = v2(core.func.minus(list(pygame.mouse.get_pos()), obj.size_conv, op="*"), dtype=numpy.float64)
    # obj.mouse_pos = pygame.mouse.get_pos()
    obj.events = pygame.event.get()
    for event in obj.events:
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    for key, sign in [
        [pygame.K_w, "w"],
        [pygame.K_a, "a"],
        [pygame.K_s, "s"],
        [pygame.K_d, "d"],
        [pygame.K_x, "x"],
        [pygame.K_c, "c"],
        [pygame.K_z, "z"],
        [pygame.K_1, "1"],
        [pygame.K_2, "2"],
        [pygame.K_3, "3"],
        [pygame.K_4, "4"],
        [pygame.K_RETURN, "enter"],
        [pygame.K_BACKSPACE, "backspace"],
        [pygame.K_ESCAPE, "esc"],
        [pygame.K_DELETE, "del"],
        [pygame.K_t, "t"],
    ]:
        if keys[key]:
            if sign in obj.keypress:
                obj.keypress.remove(sign)
            elif sign not in obj.keypress_held_down:
                obj.keypress.append(sign)

            if sign not in obj.keypress_held_down:
                obj.keypress_held_down.append(sign)
        else:
            if sign in obj.keypress:
                obj.keypress.remove(sign)
            if sign in obj.keypress_held_down:
                obj.keypress_held_down.remove(sign)

    for x in range(3):
        sign = "mouse" + str(x)
        if pygame.mouse.get_pressed()[x]:
            if sign in obj.keypress:
                obj.keypress.remove(sign)
            elif sign not in obj.keypress_held_down:
                obj.keypress.append(sign)

            if sign not in obj.keypress_held_down:
                obj.keypress_held_down.append(sign)
        else:
            if sign in obj.keypress:
                obj.keypress.remove(sign)
            if sign in obj.keypress_held_down:
                obj.keypress_held_down.remove(sign)

    if "mouse0" in obj.keypress:
        obj.sounds["click"].play()
