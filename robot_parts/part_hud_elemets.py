
import pygame
from numpy import array as v2
import core.func
import math


class Part_HUD_Elements:
    def __init__(self):
        pass

    def quicktext(self, text, size, pos, area = None):
        text = self.g.terminal[size].render(text, False, [255,255,255])
        if area:
            self.g.screen.blit(text, pos, area = area)
        else:
            self.g.screen.blit(text, pos)

    def color(self, hue):
        s = self.image[self.g.zoom]

        if self.tracks:
            l = [self.tracks, s]
        else:
            l = [s]

        for surface in l:
            for x in range(surface.get_width()):
                for y in range(surface.get_height()):
                    rgb = surface.get_at((x,y))
                    color = pygame.Color(rgb)
                    h, s, l, a = color.hsla
                    color.hsla = (h+hue)%360,s,l,a
                    surface.set_at((x,y), color)



    def draw_turret_turn(self):
        ang_rad = math.radians(self.turn_radius)
        ang_rad1 = math.radians(-self.total_delta_angle - 90)

        for a in [ang_rad1-ang_rad, ang_rad1 + ang_rad]:
            v = v2([math.cos(a) * 1000, math.sin(a) * 1000])
            pygame.draw.line(self.g.screen, [0,255,0], self.pos, self.pos + v)


        rotation_distance = 200
        pos = (self.pos[0] + math.cos(ang_rad1) * rotation_distance, self.pos[1] + math.sin(ang_rad1) * rotation_distance)
        pygame.draw.circle(self.g.screen, [0,255,0], pos, 10)
        rect = pygame.Rect(pos[0], pos[1], 0,0)
        rect.inflate_ip(20,20)
        if rect.collidepoint(self.g.mouse_pos) and "mouse2" in self.g.keypress:
            self.g.sounds["select"].stop()
            self.g.sounds["select"].play()
            self.rotate_turret = True



    def draw_active_texts(self):
        text = self.g.terminal[10].render(self.name, False, [255,255,255])
        self.g.screen.blit(text, self.pos - [0,45])

        text = self.g.terminal[10].render("Angle: " + str(self.angle) + " Total angle:" + str(self.total_delta_angle), False, [255,255,255])
        self.g.screen.blit(text, self.pos - [0,75])

        if self.parent:
            text = self.g.terminal[10].render(f"Distance: {self.delta_to_parent}", False, [255,255,255])
            self.g.screen.blit(text, self.pos - [0,30])
        if self.children:
            string = ""
            for x in self.children:
                string += x.name + ", "

            text = self.g.terminal[10].render(f"Links to: {string}", False, [255,255,255])
            self.g.screen.blit(text, self.pos - [0,15])



    def draw_info_box(self):
        value = self.active_game_tick.value
        ratio = value/self.active_game_tick.max_value
        ratio_rev = 1 - ratio
        quarter = [0,0]

        quarter[0] = 1 if self.pos[0] < self.g.res[0]/2 else -1
        quarter[1] = 1 if self.pos[1] < self.g.res[1]/2 else -1

        rect = pygame.Rect(self.pos[0]-100, self.pos[1]-200, 300, 400)
        rect.x += 230*quarter[0]
        rect.y += 230*quarter[1]
        def_pos = v2([rect.x, rect.y])

        rect.w *= (ratio**0.2)
        rect.h *= (ratio**0.1)

        blit_area = (0,0,rect.w, rect.h)

        closest_edge = core.func.get_closest_point_from_list(self.pos, [(rect.x, rect.y), (rect.x, rect.y + rect.h), (rect.x + rect.w, rect.y), (rect.x + rect.w, rect.y + rect.h)])

        pygame.draw.line(self.g.screen, [255,255,255], closest_edge, self.pos, 2)

        self.g.screen.blit(self.g.darkened_surface, (rect.x, rect.y), area = blit_area)

        self.g.screen.blit(self.g.images["y_line"][0], (rect.x, rect.y + 40), area = (rect.w, 0, rect.w, rect.h)) #

        pygame.draw.rect(self.g.screen, [255,255,255], rect, 4)

        text = self.g.terminal[30].render(self.name, False, [255,255,255])

        blit_area2 = [text.get_rect().w * ratio_rev ** 5, 0 , blit_area[2], blit_area[3]]

        self.g.screen.blit(text, def_pos + [4 ,4], area = blit_area2)

    #    self.quicktext(self.name, 30, )

        y_pos = 70

        for key in self.desc:
            end = self.desc[key][1]
            value = self.__dict__[self.desc[key][0]]
            if key == "Description: ":
                self.quicktext(f"{value}" , 15, def_pos + [4,y_pos], area = blit_area2)
                y_pos += 10
            else:
                self.quicktext(f"{key}{value}{end}", 15, def_pos + [4,y_pos], area = blit_area2)
            y_pos += 20



    def draw_rotated_rect(self):
        if self.hull < 0:
            return
        rotate_rect = self.image_rect.copy()
        points = core.func.rotate_rectangle_around_pivot(rotate_rect, self.draw_angle, self.center)
        for point_1 in points:
            point_1 += self.delta_vector - self.center + (1920-150, 1080-150)
        ratio_green = min([self.hull/100, 1])
        ratio_red = min([(200-self.hull)/100, 1])
        i1 = points[-1]
        for i in points:
            pygame.draw.line(self.g.screen, [255*ratio_red,255*ratio_green,0], i, i1, 1)
            i1 = i
