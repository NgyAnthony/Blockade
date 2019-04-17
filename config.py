SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800

BOARD_WIDTH = 500
BOARD_HEIGHT = 800

CARD_WIDTH = 100
CARD_HEIGHT = 100

SCREEN_TITLE = "Blockade"
# If true, default width and height will be ignored and overridden
SCREEN_FULLSCREEN = False

COLORBLIND = ["NO"]
DIFFICULTY = ["EASY"]
SERVER = ['5.135.29.120:4000']

FRAMERATE = 5


class Config:
    def __init__(self, PLAYER, BOARD, TURN):
        self.PLAYER = PLAYER
        self.BOARD = BOARD
        self.TURN = TURN


class AskBoard:
    def __init__(self, ask):
        self.ask = ask