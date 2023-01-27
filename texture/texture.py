import pygame
import os
from os import listdir
from os.path import isfile, join
import core.func


def load_images(game, size_conversion):


    game.explosion = core.func.load_animation("anim/expl1", 10, 41)

    for x in range(1, 151):
        game.terminal[x] = pygame.font.Font(
            "texture/terminal.ttf", round(x / size_conversion[0])
        )

    for path in ["sprites", "non_alpha"]:

        mypath = os.path.abspath(os.getcwd()) + f"/texture/{path}/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for x in onlyfiles:
            if path == "sprites":
                temp = pygame.image.load(f"{mypath}/{x}").convert_alpha()
            else:
                temp = pygame.image.load(f"{mypath}/{x}").convert()
            game.loading = f"{mypath}/{x}"
            game.images[x.removesuffix(".png")] = {}
            for i in range(2):
                exp = (4/5) ** i


                size = temp.get_size()
                image = pygame.transform.scale(
                    temp.copy(), [size[0] * exp / size_conversion[0], size[1]* exp / size_conversion[1]]
                )

                game.images[x.removesuffix(".png")][i] = image
                game.load_i += 1

# if __name__ == "__main__":
#     load_images(game, 1)
