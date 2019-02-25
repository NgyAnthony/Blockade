import pygame
import os
from logic import *


class CardSprite:
    def __init__(self, img, target_posn):
        self.image = img
        self.target_posn = target_posn
        (x, y) = target_posn
        self.posn = (x, y)

    def update(self):
        pass

    def draw(self, target_surface):
        target_surface.blit(self.image, self.posn)


def draw_board():
    game_board = Board()
    pygame.init()  # Prepare the PyGame module for use
    #main_surface = pygame.display.set_mode((1366, 768))  # Determine the main_surface and its size
    PLAYER = ("Blue", "Red")
    DIRECTIONS_FILES = ("1.png", "1-2.png", "1-3.png", "2.png", "3.png", "4.png", "inf.png")
    ASSETS_PATH = []
    ASSETS_ACCESS = []
    ASSETS_IDnPATH = []

    standard_colors = [(84, 175, 214), (214, 108, 84), (79, 79, 79)] # Set up colors [blue, red, grey]

    n_col = len(game_board.grid[0])  # This is an n_col * n_row board.
    n_row = len(game_board.grid)
    surface_x = 500  # Proposed physical surface size.
    surface_y = 600
    sq_sz_x = surface_x // n_col  # sq_sz_x is the length of a square on the x axis
    sq_sz_y = surface_y // n_row  # sq_sz_y is the length of a square on the y axis
    surface_x = n_col * sq_sz_x  # Adjust to exactly fit n squares
    surface_y = n_row * sq_sz_y

    # Create the surface of (width, height) and its window.
    surface = pygame.display.set_mode((surface_x, surface_y))
    #surface = pygame.display.set_mode((1366, 768))

    all_sprites = []      # Keep a list of all sprites in the game

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
        filter_side, word_tiles = side.split(" ")
        readable = "{}/{}/{}".format(filter_side, direction, number)
        ASSETS_ACCESS.append(readable)

    # Load every images with independant readable variables from ASSETS_ACCESS
    for x in range(len(ASSETS_ACCESS)):
        current_access = ASSETS_ACCESS[x]  # Readable path as variable
        current_access = pygame.transform.scale(pygame.image.load(ASSETS_PATH[x]), (85, 85))  # Open images with previous variable as argument
        img_dict = {
            'id': ASSETS_ACCESS[x],
            'img': current_access
        }
        ASSETS_IDnPATH.append(img_dict)

    # Create a sprite object for each card, and populate all_sprite.
    for row in range(len(game_board.grid)):
        for col in range(len(game_board.grid[row])):
            readable = game_board.grid[row][col].readable_path
            for id_image in ASSETS_IDnPATH:
                if id_image.get('id') == readable:
                    card_offset_x = (sq_sz_x - id_image.get('img').get_width()) // 2
                    card_offset_y = (sq_sz_y - id_image.get('img').get_width()) // 2
                    a_card = CardSprite(id_image.get('img'),
                                        (col * sq_sz_x + card_offset_x, row * sq_sz_y + card_offset_y))
                    all_sprites.append(a_card)
    while True:
        # Look for an event from keyboard, mouse
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:  # Window close button clicked ?
            break  # Leave game loop

        # Completely redraw the surface, starting with background.
        surface.fill((0, 200, 255))

        # Draw a fresh background (board with player1 and 2 sides)
        for row in range(len(game_board.grid)):
            # Determine which color must be used.
            if row == 0:
                c_indx = 0
            elif row == 5:
                c_indx = 1
            else:
                c_indx = 2
            for col in range(len(game_board.grid[row])):
                the_square = (col*sq_sz_y, row*sq_sz_x, sq_sz_x, sq_sz_y)
                surface.fill(standard_colors[c_indx], the_square)

        # Now that the board is drawn, draw the cards.
        for sprite in all_sprites:
            sprite.draw(surface)

        pygame.display.flip()

draw_board()