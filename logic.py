import numpy as np


class Board:
    def __init__(self):
        """A list of lists with dicts inside is the model being used for the playing grid.
        This model allows us to use [row] and [col] when iterating through the playing grid.
        Player hands are a list of dict, no list has been nested inside the list because player hands
        are limites to one row, however this means that player hands must be iterated only with [col]."""

        # A matrice determines the playing grid of 5 by 6
        self.playing_grid = [[{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]]

        # Each hand is determined by a list of 6 dict
        self.player_hand1 = [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]
        self.player_hand2 = [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]

        # This list is a matrice of 5 by 8. Player hand 1 is at array [0] and player hand 2 is at array [7]
        self.grid = []

        # Sides are determined by a list with the strings Blue and Red
        self.sides = ["Blue", "Red"]

        self.coordinates = ({"id": "DtL", "xy": (-1, -1)}, {"id": "DbL", "xy": (-1, 1)}, {"id": "DtR", "xy": (1, -1)},
                            {"id": "DbR", "xy": (1, 1)}, {"id": "T", "xy": (0, -1)}, {"id": "R", "xy": (1, 0)},
                            {"id": "B", "xy": (0, 1)}, {"id": "L", "xy": (-1, 0)})

        self.initial_distribution()
        self.trace()
        self.whole_grid()

    def __repr__(self):
        return "\n{}\n{}\n{}\n{}\n{},\n{}\n, {}, {}".format(self.playing_grid[0], self.playing_grid[1], self.playing_grid[2], self.playing_grid[3], self.playing_grid[4], self.playing_grid[5], self.player_hand1, self.player_hand2)

    def __str__(self):
        return "\n[BOARD CLASS] \n Playing_grid: {} \n Player_hand1: {},\n Player_hand2: {},\n Grid: {}".format(self.playing_grid, self.player_hand1, self.player_hand2, self.grid)

    def addHand(self, player):
        """ This function distributes cards to a player everytime his hand isn't full."""
        if player == self.player_hand1:
            side = "Blue"
        elif player == self.player_hand2:
            side = "Red"

        a = Dealer(side)
        picked_card = a.card
        player.append({'card': picked_card, 'img': None})

    def initial_distribution(self):
        """Each for loop iterates through the player hands or the board and get the key of 'card' inside the dict of
        the current iteration and assign the returned object created by the Dealer class to the value of 'card'. """
        # Distribute cards to the first player
        for col in range(len(self.player_hand1)):
            a = Dealer("Blue")  # Assign the instance of Dealer to a variable
            card = a.card  # Take the card object created out of the Dealer instance
            self.player_hand1[col]['card'] = card  # Assign that card to the value associated with the key

        # Distribute cards to the second player
        for col in range(len(self.player_hand2)):
            a = Dealer("Red")
            card = a.card
            self.player_hand2[col]['card'] = card

        # Distribute cards to the grid
        for row in range(len(self.playing_grid)):
            for col in range(len(self.playing_grid[row])):
                side = np.random.choice(self.sides, 1)[0]
                a = Dealer(side)
                card = a.card
                self.playing_grid[row][col]['card'] = card

    def whole_grid(self):
        """Each list created are appended to grid. This will result in a nested list with dict."""
        self.grid.append(self.player_hand1)
        for i in self.playing_grid:
            self.grid.append(i)
        self.grid.append(self.player_hand2)

    def trace(self):
        for row in range(len(self.playing_grid)):
            for col in range(len(self.playing_grid[row])):
                self.card = self.playing_grid[row][col]['card']
                self.tosp = self.card.direction  # Split the str directions of the card
                self.split_directions = self.tosp.split("-")  # create a list, split by "-"

                for ind_direct in self.split_directions:  # iterate through the created list
                    for a_dict in self.coordinates:  # iterate through coordinates default list
                        if ind_direct == a_dict['id']:
                            x, y = a_dict['xy']

                            if self.card.number == "inf":
                                for number in range(5):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    self.check_ifin_board(coords_nb, col, row)

                            elif self.card.number == "1-2":
                                for number in range(1, 2):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    self.check_ifin_board(coords_nb, col, row)

                            elif self.card.number == "1-3":
                                for number in range(1, 3):
                                    coords_nb = self.calculate_coords(x, y, number)
                                    self.check_ifin_board(coords_nb, col, row)

                            else:
                                coords_nb = self.calculate_coords(x, y, self.card.number)
                                self.check_ifin_board(coords_nb, col, row)
                print(self.card.targets)

    def calculate_coords(self, x, y, number):
        x_calc = int(x) * int(number)
        y_calc = int(y) * int(number)
        coords_nb = (x_calc, y_calc)
        return coords_nb

    def check_ifin_board(self, coords_nb, col, row):
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
                if self.card.side == "Red" and self.playing_grid[new_pos_y][new_pos_x]['card'].side == "Red":
                    self.card.targets.append(self.playing_grid[new_pos_y][new_pos_x]['card'])
            except:
                pass


class Dealer:
    """Dealer creates a database of all available card parameters, it then creates a Card instance with randomly
    picked parameters based on probabilities."""
    def __init__(self, side):
        """ This constructor sets up a database for Directions, Numbers, and probabilities of Numbers."""
        self.directions = ("DtL-DtR", "DtL-DtR-DbR-DbL", "DtL-T-DtR", "DtL-T-DtR-R-DbR-B-DbL-L",
                           "L-R", "L-T-R", "L-T-R-B", "R-DbR-B-DbL-L", "T", "T-B")
        #"P", "PL", "PR"

        self.number_list = ("1", "1-2", "1-3", "2", "3", "4", "inf")

        # Probability of obtaining each number in order.
        self.p_number = [0.4, 0.05, 0.05, 0.35, 0.05, 0.05, 0.05]
        self.side = side

        self.getCard()

    def getCard(self):
        """Pick random number and direction, assign them to a variable and create a Card instance with those
        variables as arguments."""
        self.random_number = np.random.choice(self.number_list, 1, p=self.p_number)[0]
        self.random_direction = np.random.choice(self.directions, 1)[0]
        self.card = Card(self.side, self.random_direction, self.random_number)


class Card:
    """ This class creates a card instance with side, direction and number as attributes"""
    def __init__(self, side, direction, number):
        self.side = side
        self.direction = direction
        self.number = number
        self.xy_directions = []
        self.targets = []

        self.makeReadable()

    def makeReadable(self):
        """ This function allows create_sprite and create_handsprite to recognize the card/sprite association"""
        self.readable_path = "{}/{}/{}".format(self.side, self.direction, self.number)

    def __repr__(self):
        return "Card('{}', '{}', {})".format(self.side, self.direction, self.number)

    def __str__(self):
        return '\n[CARD CLASS] \n Side: {} - Direction: {} - Number : {}'.format(self.side, self.direction, self.number)


class PathFinder:
    def __init__(self, playing_grid):
        self.playing_grid = playing_grid
        self.directions = ("DtL-DtR", "DtL-DtR-DbR-DbL", "DtL-T-DtR", "DtL-T-DtR-R-DbR-B-DbL-L",
                    "L-R", "L-T-R", "L-T-R-B", "R-DbR-B-DbL-L", "T", "T-B")
