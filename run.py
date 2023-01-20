import pygame
import random
from random import randint as rint
import sys
import core.keypress
from numpy import array as v2

from robot_parts.part import Part
from robot_parts.r_core import Core
from robot_parts.battery import Battery
from robot_parts.turret import Turret
from robot_parts.weapon_clamp import WeaponClamp
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

        load_images(self, self.size_conv)
        load_sounds(self)





game = Game(screen)

game.parts.append(Core("Core", game, v2([500,500]), game.images["core_temp"]))

game.parts.append(Rack("Rack", game, v2([400,900]), game.images["rack"]))


game.parts.append(Battery("Small Battery", game, v2([500,600]), game.images["battery"]))

game.parts.append(Battery("Small Battery", game, v2([500,700]), game.images["battery"]))

game.parts.append(Attachable("Armor Plate", game, v2([500,900]), game.images["armor"]))

game.parts.append(Attachable("Armor Plate", game, v2([500,900]), game.images["armor"]))

game.parts.append(Attachable("Armor Plate", game, v2([500,900]), game.images["armor"]))

game.parts.append(Attachable("Armor Plate", game, v2([500,900]), game.images["armor"]))

game.parts.append(WeaponClamp("Armament Clamp", game, v2([900,900]), game.images["turret_base"]))

game.parts.append(Turret("Kinetic Cannon", game, v2([1000,900]), game.images["turret"], center = [17,9]))

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
    for core_part in game.parts:
        core_part.tick()


    pygame.display.update()
