import pygame
import os
import config
import sys

pygame.init()  # Prepare the PyGame module for use

font = pygame.font.Font(None, 42)


class CardSprite:
    """ This class creates sprite objects which are then added to the right 'card'/'img' in create_sprite"""
    def __init__(self, img, target_posn):
        self.image = img
        self.target_posn = target_posn
        (x, y) = target_posn
        self.posn = (x, y)
        self.rect = img.get_rect(topleft=(x, y))

    def __repr__(self):
        return 'CardSprite({}, {})'.format(self.image, self.posn)

    def update(self):
        pass

    def draw(self, target_surface):
        target_surface.blit(self.image, self.posn)


class Base:
    def __init__(self, title, width, height, framerate, fullscreen, game_board):
        if not fullscreen:
            self.window = pygame.display.set_mode((width, height))
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT = self.window.get_size()

        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.game_board = game_board

        self.player = ("Blue", "Red")
        self.DIRECTIONS_FILES = ("1.png", "1-2.png", "1-3.png", "2.png", "3.png", "4.png", "inf.png")
        (self.ASSETS_PATH, self.ASSETS_ACCESS, self.ASSETS_IDnPATH) = ([], [], [])
        (self.n_col, self.n_row) = (len(self.game_board.grid[0]), len(self.game_board.grid))  # This is an n_col * n_row board.
        (self.surface_x, self.surface_y) = (self.window.get_size())
        (self.sq_sz_x, self.sq_sz_y) = (self.surface_x // self.n_col, self.surface_y // self.n_row)
        (self.surface_x, self.surface_y) = (self.n_col * self.sq_sz_x, self.n_row * self.sq_sz_y)

        self.standard_colors = [(84, 175, 214), (214, 108, 84), (79, 79, 79)]  # Set up colors [blue, red, grey]

        self.surface = pygame.display.set_mode((self.surface_x, self.surface_y)) # Create the surface of (width, height) and its window.
        self.selected = None
        self.selected_img = None

    def logic(self, keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta):
        raise NotImplementedError()

    def paint(self, surface):
        raise NotImplementedError()

    def load_folders(self, images=False, sounds=False, music=False):
        """This function determines what files are opened."""
        if images:
            # Adjust the number of files in "Assets" dir.
            for side in self.player:
                for r, d, files in os.walk("Assets/{} Tiles".format(side)):
                    for file in files:  # Analyze every "file" name in the list of "files"
                        if file not in self.DIRECTIONS_FILES:
                            files.remove(file)  # Remove any parasite
                    for file in files:
                        self.ASSETS_PATH.append(str(r + "/" + file))

            # Transform 'Assets/Blue Tiles/L-T-R-B/1x/inf.png' into 'Blue Tiles/L-T-R-B/inf'
            for asset in self.ASSETS_PATH:
                directory, side, direction, dump, number_file = asset.split("/")
                number, extention = number_file.split(".")
                filter_side, word_tiles = side.split(" ")
                readable = "{}/{}/{}".format(filter_side, direction, number)
                self.ASSETS_ACCESS.append(readable)

            # Load every images with independant readable variables from ASSETS_ACCESS
            for x in range(len(self.ASSETS_ACCESS)):
                current_access = self.ASSETS_ACCESS[x]  # Readable path as variable
                current_access = pygame.transform.scale(pygame.image.load(self.ASSETS_PATH[x]),
                                                        (85, 85))  # Open images with previous variable as argument
                img_dict = {
                    'id': self.ASSETS_ACCESS[x],
                    'img': current_access
                }
                self.ASSETS_IDnPATH.append(img_dict)

        if sounds:
            self.sounds = {str(i)[:-4]: pygame.mixer.Sound("sounds/" + i) for i in os.listdir("sounds") if
                           os.path.isfile("sounds/" + i)}
        if music:
            self.music = {str(i)[:-4]: "music/" + i for i in os.listdir("music") if os.path.isfile("music/" + i)}

    def create_sprite(self):
        """This function creates sprites from the playing board and put them into each 'img' value"""
        for row in range(len(self.game_board.playing_grid)):
            for col in range(len(self.game_board.playing_grid[row])):
                readable = self.game_board.playing_grid[row][col]['card'].readable_path
                for id_image in self.ASSETS_IDnPATH:
                    if id_image.get('id') == readable:
                        card_offset_x = (self.sq_sz_x - id_image.get('img').get_width()) // 2
                        card_offset_y = (self.sq_sz_y - id_image.get('img').get_width()) // 2

                        a_card = CardSprite(id_image.get('img'),
                                            (col * self.sq_sz_x + card_offset_x, (row+1) * self.sq_sz_y + card_offset_y))
                        self.game_board.playing_grid[row][col]['img'] = a_card

    def create_handsprite(self, element):
        """This function creates sprites from player hands and put them into each 'img' value"""
        if element == self.game_board.player_hand1:
            row = 0
        elif element == self.game_board.player_hand2:
            row = 7

        for col in range(len(element)):
            readable = element[col]['card'].readable_path
            for id_image in self.ASSETS_IDnPATH:
                if id_image.get('id') == readable:
                    card_offset_x = (self.sq_sz_x - id_image.get('img').get_width()) // 2
                    card_offset_y = (self.sq_sz_y - id_image.get('img').get_width()) // 2
                    a_card = CardSprite(id_image.get('img'),
                                        (col * self.sq_sz_x + card_offset_x, row * self.sq_sz_y + card_offset_y))

                    element[col]['img'] = a_card

    def find_path(self):
        self.direct_indiv = ({'id': "L", 'pos': (-1, 0)},
                             {'id': "T", 'pos': (0, 1)},
                             {'id': "R", 'pos': (1, 0)},
                             {'id': "B", 'pos': (0, -1)},

                             {'id': "DtR", 'pos': (1, 1)},
                             {'id': "DbR", 'pos': (-1, -1)},
                             {'id': "DtL", 'pos': (-1, 1)},
                             {'id': "DbL", 'pos': (-1, -1)},

                             {'id': "P", 'pos': ((-1, 1), (1, 1))},
                             {'id': "PL", 'pos': (-1, 1)},
                             {'id': "PR", 'pos': (1, 1)})


    def main(self):
        keys = set()
        buttons = set()
        mousepos = (1, 1)

        while True:
            self.clock.tick(self.framerate)
            delta = float(self.clock.get_time()) / float(self.framerate)

            newkeys = set()
            newbuttons = set()
            lastmousepos = mousepos

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons.add(event.button)
                    newbuttons.add(event.button)
                    mousepos = event.pos
                    pos = pygame.mouse.get_pos()

                    for row in range(len(self.game_board.playing_grid)):
                        for col in range(len(self.game_board.playing_grid[row])):
                            if self.selected is not None and self.game_board.playing_grid[row][col]['img'].rect.collidepoint(pos):
                                self.game_board.playing_grid[row][col]['card'] = self.selected
                                self.game_board.playing_grid[row][col]['img'].image = self.selected_img
                                self.selected = None
                                self.selected_img = None

                    for card_dict in self.game_board.player_hand1:
                        if card_dict['img'].rect.collidepoint(pos):
                            self.selected = card_dict['card']
                            self.selected_img = card_dict['img'].image
                            #self.game_board.player_hand1.remove(card_dict)

                    for card_dict in self.game_board.player_hand2:
                        if card_dict['img'].rect.collidepoint(pos):
                            self.selected = card_dict['card']
                            self.selected_img = card_dict['img'].image
                            #self.game_board.player_hand2.remove(card_dict)

                if event.type == pygame.MOUSEBUTTONUP:
                    buttons.discard(event.button)
                    mousepos = event.pos

                if event.type == pygame.MOUSEMOTION:
                    mousepos = event.pos

                if event.type == pygame.KEYDOWN:
                    keys.add(event.key)
                    newkeys.add(event.key)

                if event.type == pygame.KEYUP:
                    keys.discard(event.key)

            self.logic(keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta)
            self.paint(self.window)
            self.window.blit(font.render("FPS: %i" % self.clock.get_fps(), True, (255, 255, 255)), (0, 0))

            pygame.display.update()
