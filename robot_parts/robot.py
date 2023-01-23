class Robot:
    def __init__(self, core, game):
        self.core = core
        self.parts = []
        self.g = game

    def add_part(self, part):
        self.parts.append(part)
        part.robot = self

    def tick(self):
        pass
