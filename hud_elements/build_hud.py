import math
import pygame
from scipy.integrate import quad
import numpy
import time
from scipy.optimize import fsolve

def calc_acceleration2(speed, power, mass):
    friction = 0.01
    g = 9.8
    force = power / speed
    net_force = force - (mass * g * friction)
    acceleration = net_force / mass
    return acceleration

def calc_acceleration(x, track_power, mass):
    output = math.sqrt(track_power/(2*mass*x))
    return output


def shift_integrand(integrand, track_power, mass, shift = 0):
    def dec(x):
        return integrand(x, track_power, mass) - shift
    return dec

def draw_build_hud(game):
    rx, ry = game.res
    for x in game.parts:
        if x.core:
            core = x
            break

    children = []
    children = core.recursive_get_children(core, children)
    mass = core.mass
    electricity = core.battery_life
    for x in children:
        mass += x.mass
        electricity += x.battery_life

    if mass != game.mass or electricity != game.battery_life:
        game.last_mass = game.mass
        game.last_battery_capacity = game.battery_life
        game.hud_tick.value = 0

    game.mass = mass
    game.battery_life = electricity


    ratio = (game.hud_tick.value/game.hud_tick.max_value)**0.2

    app_mass = mass*ratio + game.last_mass * (1-ratio) + 0.01

    game.quicktext(f"Mass: {app_mass:.1f}kg", 50, (20, ry-200))
    game.quicktext(f"Battery Capacity: {electricity*ratio + game.last_battery_capacity * (1-ratio):.1f}Wh", 50, (20, ry-140))

    dec = shift_integrand(calc_acceleration2, core.track_power, app_mass)
    acceleration, error = quad(dec, 1, numpy.inf)

    x_0 = 1

    dec2 = shift_integrand(calc_acceleration2, core.track_power, app_mass, 0.1)

    x_value = fsolve(dec2, x_0)[0]

    game.quicktext(f"Top speed: {acceleration:.1f}m/s in {x_value:.1f} seconds", 50, (20, ry-70))

    game.hud_tick.tick()


if __name__ == '__main__':
    def acceleration(t, mass, power):
        velocity = power / (mass * t)
        return velocity
