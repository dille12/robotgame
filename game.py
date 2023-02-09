from core.gametick import GameTick
from numpy import array as v2
import pygame
import random
from texture.texture import load_images
from sounds.sounds import load_sounds
import core.func

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
        self.particles = []
        self.impacts = []
        self.tick_time = 1/60
        self.misses = 0
        self.hud_tick = GameTick(22, oneshot = True)
        self.explosion_list = []

        self.state = "build"

        self.draw_modules_on_top = []

        load_images(self, self.size_conv)
        load_sounds(self)

    def sort_parts_by_depth(self):
        parts = {}
        for x in self.parts:
            depth = x.recursive_get_parent_depth(0)
            if depth not in parts:
                parts[depth] = [x]
            else:
                parts[depth].append(x)
        return parts

    def get_parts_not_connected(self):
        for x in self.parts:
            if x.core:
                core = x
                break

        children = core.recursive_get_children(core, [core])
        not_connected = []
        for x in self.parts:
            if x not in children and not x.parent:
                not_connected.append(x)

        return not_connected

    def load_robot(self):
        pass


    def sound(self, key):

        if key + "1" in self.sounds:
            i = 0
            sounds = []
            while True:
                i += 1
                if key + str(i) in self.sounds:
                    sounds.append(key + str(i))
                else:
                    break

            key1 = random.choice(sounds)
            self.sounds[key1].stop()
            self.sounds[key1].play()
            return

        self.sounds[key].stop()
        self.sounds[key].play()

    def vibrate(self, magnitude):
        self.v_magnitude += magnitude

    def campos(self, pos):
        return pos - self.camera_pos

    def rev_campos(self, pos):
        return pos + self.camera_pos

    def quicktext(self, text, size, pos):
        text_surf = self.terminal[size].render(text, False, [255,255,255])
        self.screen.blit(text_surf, pos)

    def print_robot_info(self):
        for x in self.parts:
            if x.core:
                children = x.recursive_get_children(x, [x])
                break
        d = {}
        for i, x in enumerate(children):
            d[i] = x

        print("{")
        for x in d:
            t = str(type(d[x]))
            t1 = t.split("'")[1]
            parent = -1
            for y in d:
                if d[y] == d[x].parent:
                    parent = y
                    break

            try:
                x1,y1 = d[x].delta_to_parent
            except:
                x1,y1 = 0,0


            print(f"{x} : [\n    {t1}(game, [500,500]),\n    {parent if parent != -1 else None},\n    [{x1}, {y1}],\n    {d[x].angle}    ],")



            # print("angle:", d[x].angle)
            # print("delta_to_parent:", d[x].delta_to_parent)


        print("}")
        #print(x.name, x.parent, x.angle, x.angle_to_parent, x.delta_to_parent)



    def camera_movement(self):
        camera_pan = 0.1
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
