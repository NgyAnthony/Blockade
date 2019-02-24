import numpy as np


class Board:
    def __init__(self):
        """ This constructor set the grid, two hands, sides, and the current turn."""
        # A matrice determines the board of 5 by 6
        self.grid = [[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None]]

        # Each hand is determined by a list of 6 elements.
        self.player_hand1 = [None, None, None, None, None, None]
        self.player_hand2 = [None, None, None, None, None, None]

        # Sides are determined by a list with the strings Blue and Red.
        self.sides = ["Blue", "Red"]

        # The current turn is first determined by select_firstplayer
        self.current_turn = None

    def addHand(self, player):
        """ This function distributes cards to a player everytime his hand isn't full."""
        if player == self.player_hand1:
            side = "Blue"
        elif player == self.player_hand2:
            side = "Red"

        picked_card = Dealer(side)
        player.append(picked_card)

    def addToBoard(self, position, card):
        """ This function put the chosen card to the board."""
        pass

    def game_tracker(self):
        """ This function initialize the first set of cards"""
        # Distribute cards to the first player
        if None in self.player_hand1:
            for x in range(len(self.player_hand1)):
                card = Dealer("Blue")
                self.player_hand1[x] = card

        # Distribute cards to the second player
        if None in self.player_hand2:
            for x in range(len(self.player_hand1)):
                card = Dealer("Red")
                self.player_hand1[x] = card

        # Distribute cards to the grid
        if None in self.grid:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    side = np.random.choice(self.sides, 1)
                    card = Dealer(side)
                    self.grid[row][col] = card

    def select_firstplayer(self):
        """ This function randomly chooses the first player."""
        self.current_turn = np.random.choice(self.sides, 1)


class Dealer:
    def __init__(self, side):
        self.directions = ("DtL-DtR", "DtL-DtR-DbR-DbL", "DtL-T-DtR", "DtL-T-DtR-R-DbR-B-DbL-L",
                           "L-R", "L-T-R", "L-T-R-B", "P", "PL", "PR", "R-DbR-B-DbL-L", "T", "B")
        self.number = ("1", "1-2", "1-3", "2", "3", "4", "inf")
        self.p_number = [0.125, 0.15, 0.20, 0.20, 0.15, 0.125, 0.05]
        self.side = side
        self.getCard()

    def __repr__(self):
        return "Dealer('{}', '{}', {})".format(self.side, self.random_direction, self.random_number)

    def __str__(self):
        return 'Side: {} - Direction: {} - Number : {}'.format(self.side, self.random_direction, self.random_number)

    def getCard(self):
        self.random_number = np.random.choice(self.number, 1, p=self.p_number)
        self.random_direction = np.random.choice(self.directions, 1)
        Card(self.side, self.random_direction, self.random_number)


class Card:
    def __init__(self, side, direction, number):
        self.side = side
        self.direction = direction
        self.number = number


a = Dealer("Blue")
print(a)