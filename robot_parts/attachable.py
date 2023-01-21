import core.func
from robot_parts.part import Part
import pygame
from numpy import array as v2

class Attachable(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.attachable = True


    def attach(self):

        closest = None
        closest_dist = 100


        posx = (self.g.mouse_pos[0])//5
        posy = (self.g.mouse_pos[1])//5
        mp = v2([posx*5, posy*5])


        for part in self.g.parts:
            if part == self or not part.extendable:
                continue
            x, y, dir = core.func.closest_point(part.rect, mp)
            if not dir:
                continue
            dist = core.func.get_dist_points([x,y], mp)
            if dist < closest_dist:
                closest = [x,y,dir]
                closest_dist = dist
                closest_part = part

        if closest:
            x,y,dir = closest
            self.set_parent(closest_part)
        else:
            self.angle = 0
            self.pos = mp
            self.unset_parent()
            self.move_children()
            return

        angles = {
            "left" : 90,
            "right" : 270,
            "down" : 180,
            "up" : 0,
        }

        ang = angles[dir]

        #if not self.extendable:

        self.angle = ang - self.parent.angle

        center_rotated = core.func.rotate_point(self.center, self.angle)

        self.pos[0] = x
        self.pos[1] = y

        if dir in ["up", "down"]:
            self.pos[1] -= center_rotated[1]
        else:
            self.pos[0] -= center_rotated[0]

        self.move_children()
        text = self.g.terminal[10].render(dir, False, [255,255,255])
        self.g.screen.blit(text, self.pos - [0,60])
