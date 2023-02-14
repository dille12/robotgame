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
import game
import pygame

screen = pygame.display.set_mode((1920, 1080))

game = game.Game(screen)


DEFAULT_LIGHT_ATTACKER = {
0 : [
    robot_parts.cores.SmallCore(game, [500,500]),
    None,
    [0, 0],
    0    ],
1 : [
    robot_parts.weapon_clamp.WeaponClamp(game, [500,500]),
    0,
    [0, -49],
    0    ],
2 : [
    robot_parts.turret.MachineGun(game, [500,500]),
    1,
    [0, -5],
    -90.0    ],
3 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, 0],
    270    ],
}

DEFAULT_MEDIUM_ATTACKER = {
0 : [
    robot_parts.cores.SmallCore(game, [500,500]),
    None,
    [0, 0],
    0    ],
1 : [
    robot_parts.weapon_clamp.WeaponClamp(game, [500,500]),
    0,
    [0, -49],
    0    ],
2 : [
    robot_parts.turret.MachineGun(game, [500,500]),
    1,
    [0, -5],
    -90.0    ],
3 : [
    robot_parts.ceiling_clamp.CeilingClamp(game, [500,500]),
    0,
    [-50, 0],
    0    ],
4 : [
    robot_parts.turret.KineticCannon(game, [500,500]),
    3,
    [0, 0],
    -90.0    ],
5 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, 20],
    270    ],
6 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, -20],
    270    ],
7 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [45, -40],
    0    ],
8 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [45, 41],
    180    ],
}

RAILGUNNER_LIGHT = {
0 : [
    robot_parts.cores.SmallCore(game, [500,500]),
    None,
    [0, 0],
    0    ],
1 : [
    robot_parts.ceiling_clamp.CeilingClamp(game, [500,500]),
    0,
    [-50, 0],
    0    ],
2 : [
    robot_parts.turret.Railgun(game, [500,500]),
    1,
    [0, 0],
    -90.0    ],
3 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, 20],
    270    ],
4 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, -20],
    270    ],
5 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [45, -40],
    0    ],
6 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [45, 41],
    180    ],
7 : [
    robot_parts.commandmodule.CommandModule(game, [500,500]),
    0,
    [0, 0],
    0    ],
}
ULTRALIGHT_ATTACKER = {
0 : [
    robot_parts.cores.SmallCore(game, [500,500]),
    None,
    [0, 0],
    0    ],
1 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, -25],
    270    ],
2 : [
    robot_parts.armor.SteelArmor(game, [500,500]),
    0,
    [78, 20],
    270    ],
3 : [
    robot_parts.ceiling_clamp.CeilingClamp(game, [500,500]),
    0,
    [0, 0],
    0    ],
4 : [
    robot_parts.turret.LMG(game, [500,500]),
    3,
    [0, 0],
    -90.0    ],
}
