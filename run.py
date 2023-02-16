import pygame
import random
from random import randint as rint
import random
import sys
import core.keypress
from core.gametick import GameTick
from numpy import array as v2
import time
from game import Game

# from robot_parts.part import Part
# from robot_parts.cores import Core, SmallCore, BigCore
# from robot_parts.battery import Battery
# from robot_parts.commandmodule import CommandModule
# from robot_parts.turret import KineticCannon, MachineGun
# from robot_parts.weapon_clamp import WeaponClamp
# from robot_parts.ceiling_clamp import CeilingClamp
# from robot_parts.armor import *
# from robot_parts.rack import Rack
# from robot_parts.attachable import Attachable

import robot_parts.part
import robot_parts.cores
import robot_parts.battery
import robot_parts.commandmodule
import robot_parts.turret
import robot_parts.weapon_clamp
import robot_parts.ceiling_clamp
import robot_parts.armor
import robot_parts.rack
import robot_parts.attachable




from hud_elements.button import Button


pygame.init()
pygame.font.init()

from prefabs.prebuilt import *

from prefabs.default import build_prefab

from core.game_tick_build import tick_build
from core.game_tick_drive import tick_drive


#screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()


#game = Game(screen)

#game.parts += build_prefab(game, "ULTRALIGHT_ATTACKER")
game.parts.append(robot_parts.cores.SmallCore(game, [500,500]))
game.parts.append(robot_parts.commandmodule.CommandModule(game, [500,500]))


game.parts.append(robot_parts.turret.Railgun(game, [500,500]))
game.parts.append(robot_parts.turret.MachineGun(game, [500,500]))
game.parts.append(robot_parts.turret.KineticCannon(game, [500,500]))
game.parts.append(robot_parts.weapon_clamp.WeaponClamp(game, [500,500]))

game.parts.append(robot_parts.ceiling_clamp.CeilingClamp(game, [500,500]))
game.parts.append(robot_parts.ceiling_clamp.CeilingClamp(game, [500,500]))
game.parts.append(robot_parts.battery.Battery(game, [500,500]))

game.parts.append(robot_parts.armor.SteelArmor(game, [500,500]))
game.parts.append(robot_parts.armor.AluminumAlloyArmor(game, [500,500]))
game.parts.append(robot_parts.armor.CarbonCompositeArmor(game, [500,500]))
game.parts.append(robot_parts.armor.CarbonCompositeArmor(game, [500,500]))

print(game.parts)



b1 = Button(game, 10,10, "Drive!", font = 50, dont_center = True)
b2 = Button(game, 10,200, "Print Info", font = 50, dont_center = True)

while 1:
    clock.tick(60)

    game.sleep = False

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
            game.state = "build_enemies"

        if b2.tick():
            game.print_robot_info()
        tick_build(game)


    elif game.state == "build_enemies":


        game.parts += build_prefab(game, "ULTRALIGHT_ATTACKER", [random.randint(100,2000),random.randint(100,2000)])

        game.depth_sorted_parts = game.sort_parts_by_depth()

        game.state = "drive"

    elif game.state == "drive":
        game.screen.fill((0, 0, 0))

        tick_drive(game)

    game.tick_time =  time.perf_counter() - t

    for x in game.impacts:
        pygame.draw.rect(game.screen, [255,0,0], (game.campos(x), (5,5)))

    game.quicktext(f"{1/game.tick_time:.0f}fps", 20, (20,125))
    game.quicktext(f"{game.tick_time/(1/60)*100:.0f}%", 20, (20,100))
    game.quicktext(f"{game.misses}", 20, (20,150))

    pygame.display.update()

    # if game.sleep:
    #     game.sleep = False
    #     time.sleep(1)
