from base import *  # Importer le fichier base.py
import sys  # Librairie standard python
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
        self.rect = pygame.Rect((self.surface_x / 2 - (config.BOARD_WIDTH / 2)), 0, config.BOARD_WIDTH, config.BOARD_HEIGHT)

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

        if self.side == "Red":
            self.mycolor = self.standard_colors[1]['rgb']
            self.enemy_color = self.standard_colors[0]['rgb']

        if self.side == "Blue":
            self.mycolor = self.standard_colors[0]['rgb']
            self.enemy_color = self.standard_colors[1]['rgb']

        pygame.draw.rect(self.surface, self.mycolor, self.rect, 5)
        self.button("Reset", 20, self.surface_y - 200, 150, 50, self.standard_colors[5]['rgb'], self.standard_colors[6]['rgb'], self.reset)
        self.button("Règles", 20, self.surface_y - 270, 150, 50, self.standard_colors[5]['rgb'], self.standard_colors[6]['rgb'], self.rules)
        self.button("Quitter", 20, self.surface_y - 130, 150, 50, self.standard_colors[9]['rgb'], self.standard_colors[7]['rgb'], self.quit)

        scoreadv = self.scoreadv()
        self.button("Score adv. : %s" % scoreadv, self.surface_x - 250, 20, 150, 100, self.enemy_color, self.enemy_color, None)

        score = self.score()
        self.button("Score : %s" % score, self.surface_x - 250, self.surface_y - 200, 150, 50, self.mycolor, self.mycolor, None)

        turn = self.whosturn()
        self.button("Tour : %s" % turn, self.surface_x - 250, self.surface_y - 270, 150, 50, self.mycolor, self.mycolor, None)

        roads = self.roads_established
        self.button("Routes : %s" % roads, self.surface_x - 250, self.surface_y - 130, 150, 50, self.mycolor, self.mycolor, None)

        info = self.information
        self.button(info, 0, self.surface_y - 60, 1024, 28, self.standard_colors[3]['rgb'], self.standard_colors[3]['rgb'], None)


if __name__ == "__main__":
    g = Game()
    g.main()
