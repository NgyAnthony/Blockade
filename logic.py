import numpy as np


class Board:
    def __init__(self):
        """ This constructor set the grid, two hands, sides, and the current turn."""
        # A matrice determines the board of 5 by 6
        self.playing_grid = [[{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}],
                             [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]]

        # Each hand is determined by a list of 6 elements.

        self.player_hand1 = [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]
        self.player_hand2 = [{'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}, {'card': None, 'img': None}]

        self.grid = []

        # Sides are determined by a list with the strings Blue and Red.
        self.sides = ["Blue", "Red"]

        # The current turn is first determined by select_firstplayer
        self.current_turn = None

        self.initial_distribution()
        self.select_firstplayer()
        self.whole_grid()

    def __repr__(self):
        return "\n{}\n{}\n{}\n{}\n{},\n{}\n, {}, {}, {}".format(self.playing_grid[0], self.playing_grid[1], self.playing_grid[2], self.playing_grid[3], self.playing_grid[4], self.playing_grid[5], self.player_hand1, self.player_hand2, self.current_turn)

    def __str__(self):
        return "\n[BOARD CLASS] \n Playing_grid: {} \n Player_hand1: {},\n Player_hand2: {},\n Grid: {},\n Current turn: {}".format(self.playing_grid, self.player_hand1, self.player_hand2, self.grid, self.current_turn)

    def whole_grid(self):
        """ Append all cards into the main grid"""
        self.grid.append(self.player_hand1)
        for i in self.playing_grid:
            self.grid.append(i)
        self.grid.append(self.player_hand2)

    def addHand(self, player):
        """ This function distributes cards to a player everytime his hand isn't full."""
        if player == self.player_hand1:
            side = "Blue"
        elif player == self.player_hand2:
            side = "Red"

        a = Dealer(side)
        picked_card = a.card
        player.append({'card': picked_card, 'img': None})

    def addToBoard(self, position, card):
        """ This function put the chosen card to the board."""
        (x, y) = position
        self.playing_grid[x][y].append(card)

    def initial_distribution(self):
        """ This function initialize the first set of cards"""
        # Distribute cards to the first player
        for x in range(len(self.player_hand1)):
            a = Dealer("Blue")
            card = a.card
            self.player_hand1[x]['card'] = card

        # Distribute cards to the second player
        for x in range(len(self.player_hand2)):
            a = Dealer("Red")
            card = a.card
            self.player_hand2[x]['card'] = card

        # Distribute cards to the grid
        for row in range(len(self.playing_grid)):
            for col in range(len(self.playing_grid[row])):
                side = np.random.choice(self.sides, 1)[0]
                a = Dealer(side)
                card = a.card
                self.playing_grid[row][col]['card'] = card

    def select_firstplayer(self):
        """ This function randomly chooses the first player."""
        self.current_turn = np.random.choice(self.sides, 1)[0]


class Dealer:
    def __init__(self, side):
        """ This constructor sets up a database for Directions, Numbers, and probabilities of Numbers."""
        self.directions = ("DtL-DtR", "DtL-DtR-DbR-DbL", "DtL-T-DtR", "DtL-T-DtR-R-DbR-B-DbL-L",
                           "L-R", "L-T-R", "L-T-R-B", "R-DbR-B-DbL-L", "T", "T-B")
        #"P", "PL", "PR"

        self.number_list = ("1", "1-2", "1-3", "2", "3", "4", "inf")
        # Probability of obtaining each number in order.
        self.p_number = [0.125, 0.15, 0.20, 0.20, 0.15, 0.125, 0.05]
        self.side = side

        self.getCard()

    def getCard(self):
        """Create a random Card"""
        self.random_number = np.random.choice(self.number_list, 1, p=self.p_number)[0]
        self.random_direction = np.random.choice(self.directions, 1)[0]
        self.card = Card(self.side, self.random_direction, self.random_number)


class Card:
    """ This class creates a card with side, direction and number as attributes"""
    def __init__(self, side, direction, number):
        self.side = side
        self.direction = direction
        self.number = number

        self.makeReadable()

    def makeReadable(self):
        """ This function allows create_sprite and create_handsprite to recognize the card/sprite association"""
        self.readable_path = "{}/{}/{}".format(self.side, self.direction, self.number)

    def __repr__(self):
        return "Card('{}', '{}', {})".format(self.side, self.direction, self.number)

    def __str__(self):
        return '\n[CARD CLASS] \n Side: {} - Direction: {} - Number : {}'.format(self.side, self.direction, self.number)