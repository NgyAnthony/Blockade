import pygame
import os
import logic


class CardSprite:
    def __init__(self, img, target_posn):
        self.image = img
        self.target_posn = target_posn
        (x, y) = target_posn
        self.posn = (x, y)


def draw_board():

    pygame.init()  # Prepare the PyGame module for use
    main_surface = pygame.display.set_mode((1366, 768))  # Determine the main_surface and its size
    PLAYER = ("Blue", "Red")
    DIRECTIONS_FILES = ("1.png", "1-2.png", "1-3.png", "2.png", "3.png", "4.png", "inf.png")
    ASSETS_PATH = []
    ASSETS_ACCESS = []

    # Adjust the number of files in "Assets" dir.
    for side in PLAYER:
        for r, d, files in os.walk("Assets/{} Tiles".format(side)):
            for file in files:  # Analyze every "file" name in the list of "files"
                if file not in DIRECTIONS_FILES:
                    files.remove(file)  # Remove any parasite
            for file in files:
                ASSETS_PATH.append(str(r + "/" + file))

    # Transform 'Assets/Blue Tiles/L-T-R-B/1x/inf.png' into 'Blue Tiles/L-T-R-B/inf'
    for asset in ASSETS_PATH:
        directory, side, direction, dump, number_file = asset.split("/")
        number, extention = number_file.split(".")
        readable = "{}/{}/{}".format(side, direction, number)
        ASSETS_ACCESS.append(readable)

    # Load every images with independant readable variables from ASSETS_ACCESS
    for x in range(len(ASSETS_ACCESS)):
        current_access = ASSETS_ACCESS[x]  # Readable path as variable
        current_access = pygame.image.load(ASSETS_PATH[x])  # Open images with previous variable as argument
        print(current_access)

draw_board()