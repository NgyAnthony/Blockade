import pygame
import os
import config
import sys
from network import Network
from config import AskBoard, ResetBoard
import webbrowser

pygame.init()  # Prepare the PyGame module for use

font = pygame.font.Font(None, 42)

n = Network()
p = n.getP()


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
                self.image = pygame.transform.scale(pygame.image.load("Other_assets/blue_hidden.png"), (config.TILE_HEIGHT, config.TILE_WIDTH))
            else:
                self.image = pygame.transform.flip(self.image, False, True)

        elif p.PLAYER == "P2" and "Red" in self.side:
            if self.hand:
                self.image = pygame.transform.scale(pygame.image.load("Other_assets/red_hidden.png"), (config.TILE_HEIGHT, config.TILE_WIDTH))
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

        self.standard_colors = [{'color': '0Blue', 'rgb': (84, 175, 214)},
                                {'color': '1Red', 'rgb': (214, 108, 84)},
                                {'color': '2Grey', 'rgb': (79, 79, 79)},
                                {'color': '3White', 'rgb': (236, 240, 241)},
                                {'color': '4Black', 'rgb': (0, 0, 0)},
                                {'color': '5Green', 'rgb': (0, 153, 51)},
                                {'color': '6Lightgreen', 'rgb': (0, 204, 102)},
                                {'color': '7Lightred', 'rgb': (255, 102, 102)},
                                {'color': '8Lightblue', 'rgb': (51, 153, 255)},
                                {'color': '9Brightred', 'rgb': (255, 51, 0)}]  # Set up colors [blue, red, grey]

        self.colorblind = [{'color': 'Blue', 'rgb': (61, 3, 255)}, {'color': 'Red', 'rgb': (237, 0, 0)},
                           {'color': 'Grey', 'rgb': (79, 79, 79)}, {'color': 'White', 'rgb': (236, 240, 241)}]

        self.surface = pygame.display.set_mode((self.surface_x, self.surface_y)) # Create the surface of (width, height) and its window.
        self.selected = None
        self.init_road = None
        self.roads_number = 0
        self.reversed_playingboard = [[],[],[],[],[],[]]
        self.roads = []
        self.roads_established = 0
        self.information = "Bienvenue dans Blockade, lisez les règles avant de jouer !"

        self.coordinates = ({"id": "DtL", "xy": (-1, -1)}, {"id": "DbL", "xy": (-1, 1)}, {"id": "DtR", "xy": (1, -1)},
                            {"id": "DbR", "xy": (1, 1)}, {"id": "T", "xy": (0, -1)}, {"id": "R", "xy": (1, 0)},
                            {"id": "B", "xy": (0, 1)}, {"id": "L", "xy": (-1, 0)})

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
                current_access = pygame.transform.scale(pygame.image.load(self.ASSETS_PATH[x]), (config.TILE_HEIGHT, config.TILE_WIDTH))  # Open images with previous variable as argument
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

    def reverse_playingboard(self):
        """This function takes the playing board and reverse its x and y axis"""
        xrow = 0
        for row in range(len(self.game_board.playing_grid) -1, -1, -1):
            for col in range(len(self.game_board.playing_grid[row]) -1, -1, -1):
                standard_dict = self.game_board.playing_grid[row][col]
                self.reversed_playingboard[xrow].append(standard_dict)
            xrow += 1
        self.game_board.playing_grid = self.reversed_playingboard
        self.reversed_playingboard = [[],[],[],[],[],[]]

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

    def erase_sprite(self):
        """Erase all sprites/pygame objects in the board"""
        for row in range(len(self.game_board.playing_grid)):
            for col in range(len(self.game_board.playing_grid[row])):
                self.game_board.playing_grid[row][col]['img'] = None

        for col in range(len(self.game_board.player_hand1)):
            self.game_board.player_hand1[col]['img'] = None
            self.game_board.player_hand2[col]['img'] = None

    def trace(self):
        """Find out the available path of each card"""
        for row in range(len(self.game_board.playing_grid)):
            for col in range(len(self.game_board.playing_grid[row])):
                self.card = self.game_board.playing_grid[row][col]['card']
                self.tosp = self.card.direction  # Split the str directions of the card
                self.split_directions = self.tosp.split("-")  # create a list, split by "-"
                if p.PLAYER == "P1":
                    self.side = "Red"
                    self.enemy_side = "Blue"
                elif p.PLAYER == "P2":
                    self.side = "Blue"
                    self.enemy_side = "Red"

                for ind_direct in self.split_directions:  # iterate through the created list
                    for a_dict in self.coordinates:  # iterate through coordinates default list
                        if ind_direct == a_dict['id']:
                            x, y = a_dict['xy']

                            if self.card.number == "inf":
                                for number in range(1, 5):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    if coords_nb == (0, 0):
                                        pass
                                    else:
                                        self.check_ifin_board(coords_nb, col, row)
                            elif self.card.number == "1-2":
                                for number in range(2):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    if coords_nb == (0, 0):
                                        pass
                                    else:
                                        self.check_ifin_board(coords_nb, col, row)
                            elif self.card.number == "1-3":
                                for number in range(3):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    if coords_nb == (0, 0):
                                        pass
                                    else:
                                        self.check_ifin_board(coords_nb, col, row)

                            else:
                                coords_nb = self.calculate_coords(x, y, self.card.number)
                                self.check_ifin_board(coords_nb, col, row)

    def calculate_coords(self, x, y, number):
        """Take the template coordinates and multiple it by the assigned number of the card."""
        x_calc = int(x) * int(number)
        y_calc = int(y) * int(number)
        coords_nb = (x_calc, y_calc)
        return coords_nb

    def check_ifin_board(self, coords_nb, col, row):
        """Set x and y position of the target card based on adjusted coordinates and col/row position of shooter card"""
        if coords_nb[0] == 0:
            new_pos_x = col
            new_pos_y = coords_nb[1] + row
        elif coords_nb[1] == 0:
            new_pos_x = coords_nb[0] + col
            new_pos_y = row
        else:
            new_pos_x = coords_nb[0] + col
            new_pos_y = coords_nb[1] + row

        if 0 <= new_pos_x <= 4 and 0 <= new_pos_y <= 5:
            try:
                if self.card.side == self.side and self.game_board.playing_grid[new_pos_y][new_pos_x]['card'].side == self.side:
                    self.card.targets.append(self.game_board.playing_grid[new_pos_y][new_pos_x]['card'])
            except:
                pass

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.standard_colors[4]['rgb'])
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.window, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.window.blit(textSurf, textRect)

    def reset(self):
        return n.send(ResetBoard(p.PLAYER))

    def quit(self):
        pygame.quit()
        sys.exit()
        return

    def whosturn(self):
        if p.TURN == "P1":
            return "Red"
        elif p.TURN == "P2":
            return "Blue"

    def score(self):
        if self.side == "Red":
            return p.REDSCORE
        elif self.side == "Blue":
            return p.BLUESCORE

    def scoreadv(self):
        if self.side == "Red":
            return p.BLUESCORE
        elif self.side == "Blue":
            return p.REDSCORE

    def check_if_road_alive(self):
        for road in self.roads:
            for tile in road:
                if tile not in self.game_board.playing_grid:
                    self.information = "Vous avez perdu une route."
                    print("A ROAD HAS BEEN BROKEN.")
                    self.roads_established -= 1
                    self.roads.remove(road)
                    break

    def add_score(self):
        if self.side == "Red":
            p.REDSCORE += self.roads_established
        elif self.side == "Blue":
            p.BLUESCORE += self.roads_established

    def rules(self):
        webbrowser.open('https://github.com/NgyAnthony/Blockade')

    def main(self):
        keys = set()
        buttons = set()
        mousepos = (1, 1)

        while True:
            "Ask and receive from the server his board and update the client by reinitializing the sprites."
            asked_board = n.send(AskBoard(p.PLAYER))  # Send a request to the server to send the board to the client
            p.BOARD = asked_board.BOARD  # Replace the board in config.
            p.TURN = asked_board.TURN  # Replace the current turn in config.
            self.game_board.playing_grid = p.BOARD.playing_grid  # Replace the current playing grid.
            if p.PLAYER == "P2":
                self.reverse_playingboard()  # Reverse the board because the format of the server board is not reversed.
            self.create_sprite()
            self.create_handsprite(self.game_board.player_hand1)
            self.create_handsprite(self.game_board.player_hand2)
            self.trace()

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
                    self.pos = pygame.mouse.get_pos()

                    # when click is on playing_grid
                    for row in range(len(self.game_board.playing_grid)):
                        for col in range(len(self.game_board.playing_grid[row])):
                            if self.selected is None and self.game_board.playing_grid[row][col]['img'].rect.collidepoint(self.pos):
                                self.colliding_card = self.game_board.playing_grid[row][col]['card']

                                # Click is on enemy card
                                if self.colliding_card.side == self.enemy_side:
                                    if self.roads_number > 0:
                                        self.roads.remove(self.roads[self.roads_number - 1])
                                        self.roads_number -= 1
                                        self.init_road = None
                                        self.information = "Vous avez annulé la création de chemin."
                                        print("YOU STOPPED BUILDING")

                                # Click is first click and on own card and on friendly camp
                                elif self.colliding_card.side == self.side and self.init_road is None and row == 5:
                                    self.init_road = self.colliding_card
                                    self.roads.append([self.init_road])
                                    self.roads_number += 1
                                    self.information = "Création d'un chemin."
                                    print("YOU ARE CREATING A ROAD")

                                # Click is on own side and previous card is in memory
                                elif self.colliding_card.side == self.side and self.init_road is not None:
                                    # Return True if colliding card is in targets of init_card
                                    for card in self.init_road.targets:
                                        if card.side == self.colliding_card.side and card.direction == self.colliding_card.direction and card.number == self.colliding_card.number:
                                            self.check_ifin_target = True
                                            break
                                        else:
                                            self.check_ifin_target = False

                                    # Click is on enemy camp and colliding card is in targets
                                    if self.check_ifin_target and row == 0:
                                        self.roads_established += 1
                                        self.information = "Un chemin a été créé."
                                        print("YOU HAVE ESTABLISHED A ROAD")
                                        self.add_score()

                                    # Click is on a target and not in the friendly camp
                                    elif self.check_ifin_target and row != 5:
                                        self.init_road = self.colliding_card
                                        self.roads[self.roads_number - 1].append(self.init_road)
                                        self.information = "Vous avez rajouté une carte au chemin."
                                        print("YOU ADDED %s TO YOUR ROAD" % self.init_road)

                                    # If no condition satisfied, remove road.
                                    elif self.check_ifin_target is False:
                                        self.roads.remove(self.roads[self.roads_number - 1])
                                        self.roads_number -= 1
                                        self.init_road = None
                                        self.information = "Vous ne pouvez pas construire ici."
                                        print("YOU FAILED TO BUILD A ROAD")

                            # Look if there is a selected card in memory and if click is on playing_grid
                            elif self.selected is not None and self.game_board.playing_grid[row][col]['img'].rect.collidepoint(self.pos) and self.init_road is None:
                                self.check_if_road_alive()
                                # modify parameters of card on board by card in memory
                                self.game_board.playing_grid[row][col]['card'] = self.selected['card']
                                self.game_board.playing_grid[row][col]['img'].image = self.selected['img'].image
                                self.information = "Vous avez rajouté une carte."
                                print("YOU PUT A CARD ON THE PLAYING BOARD")
                                # identify which hand was played
                                if self.selected['card'].side == "Blue":
                                    hand = self.game_board.player_hand1
                                elif self.selected['card'].side == "Red":
                                    hand = self.game_board.player_hand2

                                hand.remove(self.selected)  # remove used card from hand
                                self.game_board.addHand(hand)  # call method addHand to get random card
                                self.create_handsprite(hand)  # create new hand_sprite for the whole new hand
                                self.selected = None  # reset select hand memory

                                # Change the turn in the config instance
                                if p.TURN == "P1":
                                    p.TURN = "P2"
                                elif p.TURN == "P2":
                                    p.TURN = "P1"

                                # Send the new board created by the client to the server
                                if p.PLAYER == "P2":
                                    self.erase_sprite()  # Sprites can't be sent through the network so we erase it
                                    self.reverse_playingboard()  # Normal format to send it to the server
                                    p2 = n.send(p)  # Send the config instance
                                    # Reversed format and recreate the sprites
                                    self.reverse_playingboard()
                                    self.create_sprite()
                                    self.create_handsprite(self.game_board.player_hand1)
                                    self.create_handsprite(self.game_board.player_hand2)

                                elif p.PLAYER == "P1":
                                    self.erase_sprite()
                                    p2 = n.send(p)
                                    self.create_sprite()
                                    self.create_handsprite(self.game_board.player_hand1)
                                    self.create_handsprite(self.game_board.player_hand2)

                    # when click is on player_hand1
                    for card_dict in self.game_board.player_hand1:
                        if card_dict['img'].rect.collidepoint(self.pos) and p.TURN == "P2" and p.PLAYER == "P2":
                            self.selected = card_dict
                            self.game_board.current_turn = "Red"
                            self.information = "Vous avez pris une carte."
                            print("YOU SELECTED A CARD IN YOUR HAND")

                    # when click is on player_hand2
                    for card_dict in self.game_board.player_hand2:
                        if card_dict['img'].rect.collidepoint(self.pos) and p.TURN == "P1" and p.PLAYER == "P1":
                            self.selected = card_dict
                            self.game_board.current_turn = "Blue"
                            self.information = "Vous avez pris une carte."
                            print("YOU SELECTED A CARD IN YOUR HAND")

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
