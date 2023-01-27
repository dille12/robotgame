
class Explosion:
    def __init__(self, game, pos):
        self.pos = pos - [200,150]
        self.g = game
        self.lifetime = 0
        self.g.explosion_list.append(self)
        self.g.sound("explosion")

    def tick(self):
        if self.lifetime < len(self.g.explosion):
            self.g.screen.blit(self.g.explosion[self.lifetime], self.g.campos(self.pos))
            self.lifetime += 1

        else:
            self.g.explosion_list.remove(self)
