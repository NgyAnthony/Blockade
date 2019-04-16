from base import *
import sys
sys.dont_write_bytecode = True


class Game(Base):
    def __init__(self):
        Base.__init__(self, config.SCREEN_TITLE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.FRAMERATE, config.SCREEN_FULLSCREEN)
        self.load_folders(images=True)
        if p.PLAYER == "P2":
            self.reverse_playingboard()
        self.create_sprite()
        self.create_handsprite(self.game_board.player_hand1)
        self.create_handsprite(self.game_board.player_hand2)
        self.main()  # Launch the pygame while loop

    def paint(self, surface):
        """ This function draws the background and the cards on the board"""
        # Completely redraw the surface, starting with background.
        self.surface.fill(self.standard_colors[2]['rgb'])
        self.rect = pygame.Rect((self.surface_x / 2 - (config.BOARD_WIDTH / 2)), 0, 500, 800)

        # Draw a fresh background (board with player1 and 2 sides)
        for row in range(len(self.game_board.grid)):
            # Determine which color must be used for the background.
            if p.PLAYER == "P1":
                if row == 1:
                    c_indx = 0
                elif row == 6:
                    c_indx = 1
                else:
                    c_indx = 2
            if p.PLAYER == "P2":
                if row == 1:
                    c_indx = 1
                elif row == 6:
                    c_indx = 0
                else:
                    c_indx = 2
            for col in range(len(self.game_board.grid[row])):
                the_square = (col * self.sq_sz_y + (self.surface_x / 2 - (config.BOARD_WIDTH / 2)),
                              row * self.sq_sz_x, self.sq_sz_x, self.sq_sz_y)
                if config.COLORBLIND[0] == "NO":
                    self.surface.fill(self.standard_colors[c_indx]['rgb'], the_square)
                else:
                    self.surface.fill(self.colorblind[c_indx]['rgb'], the_square)

        # Now that the background is coloured, draw the cards.

        for col in range(len(self.game_board.player_hand1)):
            self.game_board.player_hand1[col]['img'].draw(self.surface)

        for row in range(len(self.game_board.playing_grid)):
            for col in range(len(self.game_board.playing_grid[row])):
                self.game_board.playing_grid[row][col]['img'].draw(self.surface)

        for col in range(len(self.game_board.player_hand2)):
            self.game_board.player_hand2[col]['img'].draw(self.surface)

        pygame.draw.rect(self.surface, self.standard_colors[3]['rgb'], self.rect, 5)


if __name__ == "__main__":
    g = Game()
    g.main()
