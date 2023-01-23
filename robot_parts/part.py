import pygame
from hud_elements.button import Button
from robot_parts.part_hud_elemets import Part_HUD_Elements
import core.func
from numpy import array as v2
import numpy
import math
class Part(Part_HUD_Elements):
    def __init__(self, name, game, pos, image):
        super().__init__()
        self.name = name
        self.g = game
        self.pos = v2(pos, dtype=numpy.float64)
        self.vel = 0
        self.angular_vel = 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 10, 10)
        self.image = image
        self.active = False
        self.sell_button = Button(game, 10,80, f"Sell: {self.name}", font = 50, dont_center = True)
        self.moving = False
        self.modules = []
        self.children = []
        self.parent = None
        self.attachable = False
        self.modular = False
        self.angle = 0
        self.extendable = False
        self.center = v2(self.image[self.g.zoom].get_rect().center, dtype=numpy.float64)
        self.modular_compability = ["None"]
        self.modular_type = "None"
        self.parent_angle_difference = 0
        self.turn_radius = 0
        self.rotate_turret = False
        self.delta_to_parent = None
        self.closest = False
        self.active_game_tick = self.g.GT(22, oneshot = True)
        self.core = False
        self.battery_life = 0
        self.tracks = None
        self.description = ""
        self.mass = 0
        self.satellite = None
        self.sensory_range = 0
        self.desc = {
            "Description: " : ["description", ""],
            "Modular type: " : ["modular_type", ""],
            "Links to:" : ["modular_compability", ""],
            "Mass: " : ["mass", "kg"],
            "Battery Capacity: " : ["battery_life", "Wh"],
        }

    def recursive_get_parent_depth(self, depth):
        if self.parent:
            depth = self.parent.recursive_get_parent_depth(depth + 1)
        return depth


    def recursive_get_children(self, part, parts):

        for x in part.children:
            if x not in parts:
                parts.append(x)
                parts = self.recursive_get_children(x, parts)

        return parts

    def get_total_delta(self, part, total, total_angle, end_point = None):
        if part.parent and part != end_point:
            total += numpy.copy(part.delta_to_parent)
            total_angle += part.angle
            total, total_angle = self.get_total_delta(part.parent, total, total_angle, end_point = end_point)

        return total, total_angle

    def get_available_modules(self, part = None):
        modules = []
        for x in self.modules:
            available = True
            if part:
                if part.modular_type not in self.modular_compability:
                    continue

            for y in self.children:
                if y == part or y.attachable:
                    continue
                if x == y.module:
                    available = False
                    break
            if available:
                modules.append(x)
        return modules


    def get_highest_parent(self, part):
        if part.parent:
            return self.get_highest_parent(part.parent)
        else:
            return part



    def move_children(self):
        children = []
        children = self.recursive_get_children(self, children)
        for x in children:

            core.func.pivot_child_around_parent(x)


            delta, delta_angle = self.get_total_delta(x.parent, numpy.copy(x.delta_to_parent), self.angle, end_point = self)
            x.pos = self.pos + delta

    def move(self):
        if not self.modular:
            posx = (self.g.mouse_pos[0] - self.delta[0])//10
            posy = (self.g.mouse_pos[1] - self.delta[1])//10
            self.pos[0] = posx*10
            self.pos[1] = posy*10
            self.move_children()


        else:
            modules = []
            for part in self.g.parts:
                for y in part.get_available_modules(part = self):

                    #def_pos = part.pos + y.vector

                    pos = core.func.rotate_point(y.vector, part.total_delta_angle)

                    modules.append([part.pos + pos, y, part])

                    self.g.draw_modules_on_top.append(part.pos + pos)

            min_dist = 1000
            curr_module = None
            for module_pos, module, part in modules:

                px, py = self.image[self.g.zoom].get_size()



                dist = core.func.get_dist_points(self.g.mouse_pos, module_pos)

                if dist < 100 and dist < min_dist:
                    min_dist = dist
                    curr_module = module
                    curr_module_pos = module_pos
                    parent_part = part

            if curr_module and core.func.get_dist_points(curr_module_pos, self.g.mouse_pos) < 100:
                self.pos = curr_module_pos

                self.set_parent(parent_part)
                self.module = curr_module

            else:
                self.pos = self.g.mouse_pos
                self.unset_parent()

            self.move_children()


    def set_parent(self, part):
        self.parent_angle_difference = core.func.get_angle_diff(self.angle, part.angle)
        self.parent = part
        for x in self.g.parts:
            if self in x.children:
                x.children.remove(self)

        self.parent.children.append(self)
        self.delta_to_parent = self.pos - self.parent.pos
        self.delta_to_parent = self.delta_to_parent.astype('int32')

    def unset_parent(self):
        self.parent = None

        self.parent_angle_difference = 0

        for x in self.g.parts:
            if self in x.children:
                x.children.remove(self)

        self.delta_to_parent = None

    def draw_satellite(self, pos, angle):
        if self.satellite:
            center = core.func.rotate_point(self.satellite_center, angle)
            r_image, r_rect = core.func.rot_center(self.satellite[self.g.zoom], angle + self.satellite_angle, pos[0] + center[0], pos[1] + center[1])
            self.g.screen.blit(r_image, [r_rect.x, r_rect.y])
            self.satellite_angle += 5
            if self.satellite_angle > 360:
                self.satellite_angle -= 360

    def draw_tracks(self, pos = None):
        if not isinstance(pos, numpy.ndarray):
            pos = self.pos
        if self.tracks:
            rot, rect = core.func.rot_center(self.tracks.copy(), self.angle, pos[0], pos[1])
            self.g.screen.blit(rot, (rect.x, rect.y))




    def rotate_around_pivot(self, angle = None, center = None, pos_override = None):
        if isinstance(pos_override, numpy.ndarray):
            pos = pos_override
        else:
            pos = self.pos

        if not angle:
            angle = self.angle
        if not center:
            realcenter = self.image[self.g.zoom].get_rect().center
        else:
            realcenter = center
        vector = v2([int(realcenter[0]), int(realcenter[1])])
        offset = vector - self.center

        center = pos + self.center

        center_vector = pygame.math.Vector2(center[0], center[1])

        offset_vector = pygame.math.Vector2(offset[0], offset[1])

        return core.func.rotate(self.image[self.g.zoom].copy(), angle, center_vector, offset_vector)


    def tick_drive(self):
        parents = core.func.recursive_get_parents(self, [self])

        total_angle = 0
        total_delta_vector = v2([0,0])
        for x in parents:
            total_angle += x.angle
            if x.parent:
                total_delta_vector += x.delta_to_parent
            else:
                core_pos = x.pos
                core_angle = x.angle


        pos = self.g.campos(core.func.rotate_point(total_delta_vector, core_angle))

        pos += core_pos

        rotated, rot_rect = self.rotate_around_pivot(angle = total_angle, pos_override = pos)
        self.rect = rot_rect
        self.rect.x -= self.center[0]
        self.rect.y -= self.center[1]
        blitpos = [self.rect.x, self.rect.y]

        self.draw_tracks(pos = pos)
        self.g.screen.blit(rotated, blitpos)
        self.draw_satellite(pos, total_angle)

        pygame.draw.rect(self.g.screen, [255,255,255], (pos, (3,3)))

    #    self.quicktext(f"{additions}", 20, blitpos)

        for x in self.children:
            x.tick_drive()

    def tick(self):

        if "w" in self.g.keypress_held_down and self.active:
            self.angle += 3
            self.move_children()

        self.current_center = self.center #core.func.rotate_point(self.center, delta_angle - self.angle)

        if self.parent:
            self.total_delta_pos, self.total_delta_angle = self.get_total_delta(self.parent,
                                                                                numpy.copy(self.delta_to_parent),
                                                                                self.angle,
                                                                                end_point = self)
        else:
            self.total_delta_pos, self.total_delta_angle = v2([0,0]), self.angle



        if self.total_delta_angle:
            rotated, rot_rect = self.rotate_around_pivot(angle = self.total_delta_angle)
        else:
            rotated = self.image[self.g.zoom]
            w, h = rotated.get_size()
            rot_rect = pygame.Rect(self.pos[0], self.pos[1], w, h)

        self.rect = rot_rect

        self.rect.x -= self.center[0]
        self.rect.y -= self.center[1]
        on_top = False
        if self.active:
            on_top = True

            if self.sell_button.tick():
                self.g.parts.remove(self)
                self.unset_parent()
                return


        if self.rect.collidepoint(self.g.mouse_pos) and self.closest:
            on_top = True
            if "mouse0" in self.g.keypress:
                self.g.sounds["select"].stop()
                self.g.sounds["select"].play()

                for x in self.g.parts:
                    if x != self:
                        x.active = False

                self.active = not self.active

            if "mouse2" in self.g.keypress and self.active:
                self.g.sounds["menu_click2"].stop()
                self.g.sounds["menu_click2"].play()
                self.moving = True
                self.delta = self.g.mouse_pos - self.pos

        pos_copy = numpy.copy(self.pos)

        if "mouse2" in self.g.keypress_held_down and self.moving and self.active:
            if self.attachable:
                self.attach()
            else:
                self.move()
        else:
            if self.moving:
                self.g.sounds["connect"].stop()
                self.g.sounds["connect"].play()
            self.moving = False

        delta = self.pos - pos_copy
        self.rect.x += delta[0]
        self.rect.y += delta[1]

        blitpos = [self.rect.x, self.rect.y]

        self.draw_tracks()

        if on_top:
            rect1 = self.rect.copy()
            rect1.inflate_ip(8,8)
            pygame.draw.rect(self.g.screen, [255,255,255], rect1, 1 if not self.active else 3)

        if self.active:
            if self.turn_radius:
                self.draw_turret_turn()
            if self.sensory_range:
                pygame.draw.circle(self.g.screen, [255,255,0], self.pos, self.sensory_range*100, 1)

        if self.rotate_turret:
            if "mouse2" not in self.g.keypress_held_down:
                self.rotate_turret = False
                self.g.sounds["connect"].stop()
                self.g.sounds["connect"].play()
            else:
                total = self.total_delta_angle - self.angle
                angle = math.degrees(math.atan2(self.g.mouse_pos[1] - self.pos[1], self.g.mouse_pos[0] - self.pos[0]))//5
                self.angle =  - total - 90 - angle*5

        self.g.screen.blit(rotated, blitpos)

        self.draw_satellite(self.pos, self.angle)

        pygame.draw.rect(self.g.screen, [255,255,255], (self.pos[0], self.pos[1], 3,3))



        #pygame.draw.rect(self.g.screen, [0,255,0], (self.pos[0] + self.current_center[0], self.pos[1] + self.current_center[1], 3,3))
