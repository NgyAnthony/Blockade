SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800

BOARD_WIDTH = 450
BOARD_HEIGHT = 720

CARD_WIDTH = BOARD_HEIGHT // 8
CARD_HEIGHT = BOARD_HEIGHT // 8

TILE_WIDTH = CARD_WIDTH - 10
TILE_HEIGHT = CARD_WIDTH - 10

SCREEN_TITLE = "Blockade"
# If true, default width and height will be ignored and overridden
SCREEN_FULLSCREEN = False

COLORBLIND = ["NO"]
DIFFICULTY = ["EASY"]
SERVER = ['5.135.29.120:4000']

FRAMERATE = 15


class Config:
    def __init__(self, PLAYER, BOARD, TURN, REDSCORE, BLUESCORE):
        self.PLAYER = PLAYER
        self.BOARD = BOARD
        self.TURN = TURN
        self.REDSCORE = REDSCORE
        self.BLUESCORE = BLUESCORE


class AskBoard:
    def __init__(self, ask):
        self.ask = ask


class ResetBoard:
    def __init__(self, reset):
        self.reset = reset