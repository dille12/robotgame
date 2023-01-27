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


DEFAULT_LIGHT_ATTACKER = {
0 : [
    robot_parts.cores.SmallCore('Small Core', game, [500,500], game.images["tank"]),
    None,
    [0, 0],
    0    ],
1 : [
    robot_parts.weapon_clamp.WeaponClamp('Armament Clamp', game, [500,500], game.images["turret_base"]),
    0,
    [0, -49],
    0    ],
2 : [
    robot_parts.turret.MachineGun('Machine Gun', game, [500,500], game.images["turret_machine"]),
    1,
    [0, -5],
    -90.0    ],
3 : [
    robot_parts.armor.SteelArmor('Steel Armorplate', game, [500,500], game.images["armor"]),
    0,
    [78, 0],
    270    ],
}
