import pygame
import random

class BattleInfo:
    def __init__(self, init_pos, part, game, color, text):

        self.part = part
        self.g = game
        self.color = color
        self.text = text
        self.hor = random.choice([0,-1])

        text = self.g.terminal[20].render(self.text, False, color)


        self.init_pos = init_pos + [-self.hor*150, -random.randint(100,200)]
        self.rect = pygame.Rect(self.init_pos[0] - 50 * (self.hor-1)/2, self.init_pos[1]-50, 50, 50)
        self.rect.w,self.rect.h = text.get_size()
        self.rect.w += 10
        self.rect.h += 10
        self.rect.x = self.init_pos[0] - self.rect.w
        self.rect.y = self.init_pos[1] - self.rect.h
        self.gametick = self.g.GT(30)
        self.phase = 0

    def tick(self, pos):
        if self.phase == 4:
            self.part.info = None
            return
        if not self.gametick.tick():
            if self.phase == 0:
                ratio = self.gametick.ratio()
                ratio = ratio ** 0.2
            elif self.phase == 3:
                ratio = 1-self.gametick.ratio()
                ratio = ratio ** 0.2
            else:
                ratio = random.uniform(0.95,1)

            color = (self.color[0] * random.uniform(0.5,1), self.color[1] * random.uniform(0.5,1), self.color[2] * random.uniform(0.5,1))
            if random.randint(0,20) == 0:
                color = (255- color[0], 255 - color[1], 255 - color[2])

            text = self.g.terminal[20].render(self.text, False, color)
            w, h = (text.get_size()[0] + 10) * ratio, (text.get_size()[1] + 10) * ratio
            self.g.screen.blit(text, [self.rect.x + 5,self.rect.y +5], area = [0,0, w-5, h-5])

            self.rect.w = w
            self.rect.h = h

            pygame.draw.rect(self.g.screen, color, self.rect, 2)

            pygame.draw.line(self.g.screen, color, pos, self.rect.bottomleft if self.hor else self.rect.bottomright)

        else:
            self.phase += 1
            self.gametick.value = 0
