import pygame
import random
from random import randint as rint
import sys
import core.keypress
from core.gametick import GameTick
from numpy import array as v2

from robot_parts.part import Part
from robot_parts.r_core import Core
from robot_parts.battery import Battery
from robot_parts.turret import Turret
from robot_parts.weapon_clamp import WeaponClamp
from robot_parts.ceiling_clamp import CeilingClamp

from robot_parts.rack import Rack



from robot_parts.attachable import Attachable

from hud_elements.button import Button

from texture.texture import load_images
from sounds.sounds import load_sounds

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

pygame.init()
pygame.font.init()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.size_conv = [1,1]
        self.res = (1920, 1080)
        self.keypress = []
        self.keypress_held_down = []
        self.terminal = {}
        self.images = {}
        self.sounds = {}
        self.load_i = 0
        self.sound_volume = 1
        self.zoom = 0
        self.camera_pos = v2([0,0])
        self.parts = []
        self.GT = GameTick
        self.darkened_surface = pygame.Surface(self.res).convert_alpha()
        self.darkened_surface.fill((0,0,0))
        self.darkened_surface.set_alpha(155)

        load_images(self, self.size_conv)
        load_sounds(self)





game = Game(screen)

game.parts.append(Core("Core", game, [500,500], game.images["core_temp"]))

game.parts.append(Rack("Rack", game, [500,500], game.images["rack"]))

game.parts.append(Battery("Small Battery", game, [500,500], game.images["battery"]))

game.parts.append(Attachable("Armor Plate", game, [500,500], game.images["armor"]))

game.parts.append(WeaponClamp("Armament Clamp", game, [500,500], game.images["turret_base"]))

game.parts.append(Turret("Kinetic Cannon", game, [500,500], game.images["turret"], center = [10,78]))

game.parts.append(CeilingClamp("Ceiling Clamp", game, [600,600], game.images["turret_ceiling"]))




b1 = Button(game, 10,10, "Moro", font = 50, dont_center = True)

while 1:
    clock.tick(60)

    core.keypress.key_press_manager(game)

    if "esc" in game.keypress:
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    game.screen.fill((102, 153, 255))

    if b1.tick():
        pass
    dist = 10000
    parts_dist = {}
    parts_size = {}
    for core_part in game.parts:
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
    for part_list in sorted(parts_size):
        for part in parts_size[part_list]:
            part.tick()

    active_part = None
    for x in game.parts:
        if x.active and not x.moving and not x.rotate_turret:
            x.active_game_tick.tick()

            x.draw_info_box()

            break
        else:
            x.active_game_tick.value = 0

    pygame.display.update()
