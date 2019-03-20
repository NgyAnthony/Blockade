from base import *
from logic import *
import sys
sys.dont_write_bytecode = True


class Game(Base):
    def __init__(self):
        Base.__init__(self, config.SCREEN_TITLE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.FRAMERATE, config.SCREEN_FULLSCREEN, Board())
        self.load_folders(images=True)
        self.create_sprite()
        self.create_handsprite(self.game_board.player_hand1)
        self.create_handsprite(self.game_board.player_hand2)
        self.main()

    def logic(self, keys, newkeys, buttons, newbuttons, mousepos, lastmousepos, delta):
        pass

    def paint(self, surface):
        # Completely redraw the surface, starting with background.
        self.surface.fill((0, 200, 255))

        # Draw a fresh background (board with player1 and 2 sides)
        for row in range(len(self.game_board.grid)):
            # Determine which color must be used for the background.
            if row == 1:
                c_indx = 0
            elif row == 6:
                c_indx = 1
            else:
                c_indx = 2
            for col in range(len(self.game_board.grid[row])):
                the_square = (col * self.sq_sz_y, row * self.sq_sz_x, self.sq_sz_x, self.sq_sz_y)
                self.surface.fill(self.standard_colors[c_indx], the_square)

        # Now that the board is drawn, draw the cards.
        for row in range(len(self.game_board.grid)):
            for col in range(len(self.game_board.grid[row])):
                self.game_board.grid[row][col]['img'].draw(self.surface)


if __name__ == "__main__":
    g = Game()
    g.main()
