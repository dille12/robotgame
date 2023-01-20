import pygame
import random
class Button:
    def __init__(self, game, x,y,text, intro = None, font = 150, dont_center = False):
        self.g = game
        self.x = x
        self.intro = intro
        self.y = y
        self.text = self.g.terminal[font].render(text, False, [255,255,255])
        self.w, self.h = self.text.get_size()
        if not dont_center:
            self.x -= self.w/2
        self.rect = pygame.Rect(self.x-5, self.y-5, self.w+10, self.h+10)
        self.active = False

    def tick(self):
        return_value = False
        if self.rect.collidepoint(self.g.mouse_pos):
            pygame.draw.rect(self.g.screen, [255,255,255], self.rect, 4)

            if not self.active:
                self.active = True
                if self.intro:
                    if self.g.state.bg is not self.intro:
                        self.g.state.intro_tick = 0
                        self.g.state.bg = self.intro
                        for x in self.g.button_sounds:
                            x.stop()
                        random.choice(self.g.button_sounds).play()

            if "mouse0" in self.g.keypress:
                self.g.sounds["menu_click2"].stop()
                self.g.sounds["menu_click2"].play()
                return_value = True

        else:
            pygame.draw.rect(self.g.screen, [100,100,100], self.rect, 2)
            if self.active:
                self.active = False

        self.g.screen.blit(self.text, (self.x, self.y))
        return return_value
