from robot_parts.part import Part

class CommandModule(Part):
    def __init__(self, name, game, pos, image):
        super().__init__(name, game, pos, image)
        self.description = "Contains remote control equipment."
        self.modular = True
        self.mass = 20
        self.modular_type = "Part"
        self.satellite = self.g.images["satellite"]
        self.satellite_center = [-9,8]
        self.satellite_angle = 0
        self.sensory_range = 4
        self.desc["Sensory Range: "] = ["sensory_range", "m"]
