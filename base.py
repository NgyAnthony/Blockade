import pygame
import os
import config
import sys
from network import Network

pygame.init()  # Prepare the PyGame module for use

font = pygame.font.Font(None, 42)

n = Network()
p = n.getP()
print(p.TURN) #gotta update it or the turn never ends yea ok

class CardSprite:
    """ This class creates sprite objects which are then added to the right 'card'/'img' in create_sprite"""
    def __init__(self, img, target_posn, sq_sz_x, sq_sz_y, side, hand):
        self.image = img
        self.target_posn = target_posn
        self.sq_sz_x = sq_sz_x
        self.sq_sz_y = sq_sz_y
        self.hand = hand
        self.side = side
        (x, y) = target_posn
        self.posn = (x, y)
        self.rect = img.get_rect(topleft=(x, y))
        self.filp_img()

    def __repr__(self):
        return 'CardSprite({}, {})'.format(self.image, self.posn)

    def filp_img(self):
        if p.PLAYER == "P1" and "Blue" in self.side:
            if self.hand:
                self.image = pygame.transform.scale(pygame.image.load("Other_assets/blue_hidden.png"), (85, 85))
            else:
                self.image = pygame.transform.flip(self.image, False, True)

        elif p.PLAYER == "P2" and "Red" in self.side:
            if self.hand:
                self.image = pygame.transform.scale(pygame.image.load("Other_assets/red_hidden.png"), (85, 85))
            else:
                self.image = pygame.transform.flip(self.image, False, True)

    def draw(self, target_surface):
        target_surface.blit(self.image, self.posn)


class Base:
    def __init__(self, title, width, height, framerate, fullscreen):
        if not fullscreen:
            self.window = pygame.display.set_mode((width, height))
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT = self.window.get_size()

        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.game_board = p.BOARD

        self.player = ("Blue", "Red")
        self.DIRECTIONS_FILES = ("1.png", "1-2.png", "1-3.png", "2.png", "3.png", "4.png", "inf.png")
        (self.ASSETS_PATH, self.ASSETS_ACCESS, self.ASSETS_IDnPATH) = ([], [], [])
        (self.n_col, self.n_row) = (len(self.game_board.grid[0]), len(self.game_board.grid))  # This is an n_col * n_row board.
        (self.surface_x, self.surface_y) = (self.window.get_size())

        #(self.sq_sz_x, self.sq_sz_y) = (config.CARD_WIDTH, config.CARD_HEIGHT)
        (self.sq_sz_x, self.sq_sz_y) = (config.BOARD_WIDTH // self.n_col, config.BOARD_HEIGHT // self.n_row)

        self.standard_colors = [{'color': 'Blue', 'rgb': (84, 175, 214)},
                                {'color': 'Red', 'rgb': (214, 108, 84)},
                                {'color': 'Grey', 'rgb': (79, 79, 79)},
                                {'color': 'White', 'rgb': (236, 240, 241)}]  # Set up colors [blue, red, grey]

        self.colorblind = [{'color': 'Blue', 'rgb': (61, 3, 255)}, {'color': 'Red', 'rgb': (237, 0, 0)},
                           {'color': 'Grey', 'rgb': (79, 79, 79)}, {'color': 'White', 'rgb': (236, 240, 241)}]

        self.surface = pygame.display.set_mode((self.surface_x, self.surface_y)) # Create the surface of (width, height) and its window.
        self.selected = None
        self.reversed_playingboard = [[],[],[],[],[],[]]

    def logic(self, keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta):
        raise NotImplementedError()

    def paint(self, surface):
        raise NotImplementedError()

    def load_folders(self, images=False, sounds=False, music=False):
        """ Load every assets."""
        if images:
            # Adjust the number of files in "Assets" dir.
            for side in self.player:
                for r, d, directory in os.walk("Assets/{} Tiles".format(side)):
                    for file in directory:  # Analyze every "file" name in the directory
                        if file not in self.DIRECTIONS_FILES:
                            directory.remove(file)  # Remove any parasite
                    for file in directory:
                        self.ASSETS_PATH.append(str(r + "/" + file))  # Append the path to the file to a list.

            # Transform 'Assets/Blue Tiles/L-T-R-B/1x/inf.png' into 'Blue Tiles/L-T-R-B/inf'
            for asset in self.ASSETS_PATH:
                directory, side, direction, dump, number_file = asset.split("/")
                number, extention = number_file.split(".")
                filter_side, word_tiles = side.split(" ")
                readable = "{}/{}/{}".format(filter_side, direction, number)
                self.ASSETS_ACCESS.append(readable)

            # Load every images with independent readable variables from ASSETS_ACCESS
            for x in range(len(self.ASSETS_ACCESS)):
                current_access = self.ASSETS_ACCESS[x]  # Readable path as variable
                current_access = pygame.transform.scale(pygame.image.load(self.ASSETS_PATH[x]), (85, 85))  # Open images with previous variable as argument
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
    # Create a new playing board with the cards in the the reversed order
    # Generate the sprites normally
    # Display them

    # But then when P2 moves on the board and sends his own board the board must be reversed again so that P1
    # can see it normal. There shouldn't be any conflict.
    # Okay, go.

    def reverse_playingboard(self):
        xrow = 0
        for row in range(len(self.game_board.playing_grid) -1, -1, -1):
            for col in range(len(self.game_board.playing_grid[row]) -1, -1, -1):
                standard_dict = self.game_board.playing_grid[row][col]
                self.reversed_playingboard[xrow].append(standard_dict)
            xrow += 1
        self.game_board.playing_grid = self.reversed_playingboard

    def create_sprite(self):
        """This function creates sprites from the playing board and put them into each 'img' value"""
        hand = False

        for row in range(len(self.game_board.playing_grid)):
            for col in range(len(self.game_board.playing_grid[row])):
                readable = self.game_board.playing_grid[row][col]['card'].readable_path
                for id_image in self.ASSETS_IDnPATH:
                    if id_image.get('id') == readable:
                        card_offset_x = (self.sq_sz_x - id_image.get('img').get_width()) // 2
                        card_offset_y = (self.sq_sz_y - id_image.get('img').get_width()) // 2

                        a_card = CardSprite(id_image.get('img'), (col * self.sq_sz_x + card_offset_x +
                                                                  (self.surface_x / 2 - (config.BOARD_WIDTH / 2)),
                                                                  (row + 1) * self.sq_sz_y + card_offset_y),
                                            self.sq_sz_x, self.sq_sz_y, id_image.get('id'), hand)
                        self.game_board.playing_grid[row][col]['img'] = a_card


    def create_handsprite(self, element):
        """This function creates sprites from player hands and put them into each 'img' value"""
        hand = True
        if p.PLAYER == "P1":
            if element == self.game_board.player_hand1:
                row = 0
            elif element == self.game_board.player_hand2:
                row = 7

        elif p.PLAYER == "P2":
            if element == self.game_board.player_hand1:
                row = 7
            elif element == self.game_board.player_hand2:
                row = 0

        for col in range(len(element)):
            readable = element[col]['card'].readable_path
            for id_image in self.ASSETS_IDnPATH:
                if id_image.get('id') == readable:
                    card_offset_x = (self.sq_sz_x - id_image.get('img').get_width()) // 2
                    card_offset_y = (self.sq_sz_y - id_image.get('img').get_width()) // 2
                    a_card = CardSprite(id_image.get('img'),
                                        (col * self.sq_sz_x + card_offset_x + (self.surface_x / 2 - (config.BOARD_WIDTH / 2)),
                                         row * self.sq_sz_y + card_offset_y), self.sq_sz_x, self.sq_sz_y, id_image.get('id'), hand)

                    element[col]['img'] = a_card

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

                    # when click is on playing_grid
                    for row in range(len(self.game_board.playing_grid)):
                        for col in range(len(self.game_board.playing_grid[row])):
                            # Look if there is a selected card in memory and if click is on playing_grid
                            if self.selected is not None and self.game_board.playing_grid[row][col]['img'].rect.collidepoint(pos):
                                # modify parameters of card on board by card in memory
                                self.game_board.playing_grid[row][col]['card'] = self.selected['card']
                                self.game_board.playing_grid[row][col]['img'].image = self.selected['img'].image

                                if self.selected['card'].side == "Blue":
                                    hand = self.game_board.player_hand1
                                elif self.selected['card'].side == "Red":
                                    hand = self.game_board.player_hand2

                                hand.remove(self.selected)  # remove used card from hand
                                self.game_board.addHand(hand)  # call method addHand to get random card
                                self.create_handsprite(hand)  # create new hand_sprite for the whole new hand
                                self.selected = None  # reset select hand memory

                    # when click is on player_hand1
                    for card_dict in self.game_board.player_hand1:
                        if card_dict['img'].rect.collidepoint(pos) and p.TURN == "P2" and p.PLAYER == "P2":
                            self.selected = card_dict
                            self.game_board.current_turn = "Red"

                    # when click is on player_hand2
                    for card_dict in self.game_board.player_hand2:
                        if card_dict['img'].rect.collidepoint(pos) and p.TURN == "P1" and p.PLAYER == "P1":
                            self.selected = card_dict
                            self.game_board.current_turn = "Blue"

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

            self.paint(self.surface)
            self.window.blit(font.render("FPS: %i" % self.clock.get_fps(), True, (255, 255, 255)), (0, 0))

            pygame.display.update()
