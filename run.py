import pygame
import random
from random import randint as rint
import random
import sys
import core.keypress
from core.gametick import GameTick
from numpy import array as v2
import time

from robot_parts.part import Part
from robot_parts.cores import Core, SmallCore, BigCore
from robot_parts.battery import Battery
from robot_parts.commandmodule import CommandModule
from robot_parts.turret import KineticCannon, MachineGun
from robot_parts.weapon_clamp import WeaponClamp
from robot_parts.ceiling_clamp import CeilingClamp
from robot_parts.armor import *


from robot_parts.rack import Rack
from core.game_tick_build import tick_build
from core.game_tick_drive import tick_drive
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
        self.res2 = v2([1920, 1080])
        self.keypress = []
        self.keypress_held_down = []
        self.terminal = {}
        self.images = {}
        self.sounds = {}
        self.load_i = 0
        self.sound_volume = 1
        self.zoom = 0
        self.camera_pos = v2([0,0])
        self.camera_pos_target = v2([0,0])
        self.parts = []
        self.GT = GameTick
        self.darkened_surface = pygame.Surface(self.res).convert_alpha()
        self.darkened_surface.fill((0,0,0))
        self.darkened_surface.set_alpha(155)
        self.v_magnitude = 0
        self.last_mass = 0
        self.last_battery_capacity = 0
        self.mass = 0
        self.battery_life = 0
        self.bullets = []

        self.hud_tick = GameTick(22, oneshot = True)

        self.state = "build"

        self.draw_modules_on_top = []

        load_images(self, self.size_conv)
        load_sounds(self)

    def vibrate(self, magnitude):
        self.v_magnitude += magnitude

    def campos(self, pos):
        return pos - self.camera_pos

    def quicktext(self, text, size, pos):
        text_surf = self.terminal[size].render(text, False, [255,255,255])
        self.screen.blit(text_surf, pos)

    def camera_movement(self):
        camera_pan = 0.05
        mouse_pos_var = [
            camera_pan * (self.mouse_pos[0] - self.res[0] / 2),
            camera_pan * (self.mouse_pos[1] - self.res[1] / 2),
        ]

        self.camera_pos[0] += mouse_pos_var[0] + random.uniform(-self.v_magnitude, self.v_magnitude)
        self.camera_pos[1] += mouse_pos_var[1] + random.uniform(-self.v_magnitude, self.v_magnitude)

        self.v_magnitude *= 0.9

        camera_panning = 0.15
        self.camera_pos = core.func.minus(
            self.camera_pos,
            core.func.minus(
                core.func.minus(self.camera_pos_target, self.camera_pos, op="-"),
                [camera_panning, camera_panning],
                op="*",
            ),
        )





game = Game(screen)

#game.parts.append(BigCore("Core", game, [500,500], game.images["core_temp"]))

game.parts.append(SmallCore("Small Core", game, [600,500], game.images["tank"]))

game.parts.append(Battery("Small Battery", game, [500,500], game.images["battery"]))

game.parts.append(CommandModule("Command Module", game, [500,700], game.images["commandmodule"]))

game.parts.append(SteelArmor("Steel Armorplate", game, [500,500], game.images["armor"]))

game.parts.append(CarbonCompositeArmor("Carbonfiber Armor", game, [500,500], game.images["armor"]))

game.parts.append(WeaponClamp("Armament Clamp", game, [500,500], game.images["turret_base"]))

game.parts.append(KineticCannon("Kinetic Cannon", game, [500,500], game.images["turret"], center = [10,78]))

game.parts.append(MachineGun("Machine Gun", game, [500,500], game.images["turret_machine"], center = [10,50]))

game.parts.append(CeilingClamp("Ceiling Clamp", game, [600,600], game.images["turret_ceiling"]))




b1 = Button(game, 10,10, "Drive!", font = 50, dont_center = True)

while 1:
    clock.tick(60)

    core.keypress.key_press_manager(game)

    if "esc" in game.keypress:
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    t = time.perf_counter()

    if game.state == "build":
        game.screen.fill((102, 153, 255))
        if b1.tick():
            game.state = "drive"
        tick_build(game)
    elif game.state == "drive":
        game.screen.fill((0, 153, 0))

        tick_drive(game)

    tick_time = time.perf_counter() - t

    game.quicktext(f"{1/tick_time:.0f}fps", 20, (20,125))

    game.quicktext(f"{tick_time/(1/60)*100:.0f}%", 20, (20,100))

    pygame.display.update()
