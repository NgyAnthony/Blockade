# coding=utf-8
"""
EXAMPLE 2
Game menu with 3 difficulty options.
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import pygame and libraries
from pygame.locals import *
from random import randrange
import os
import pygame

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

DEVS = ['Developpeur: {0}'.format("NGUYEN Anthony"),
        'Designer graphique: {0}'.format("u/elheber"),
        PYGAMEMENU_TEXT_NEWLINE,
        'Email: {0}'.format("nguyen.anthony.dev@gmail.com"),
        'Git: {0}'.format("github.com/NgyAnthony/Blockade")]


COLOR_BACKGROUND = (79, 79, 79)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 3
MENU_BACKGROUND_COLOR = (0, 173, 238)
WINDOW_SIZE = (1366, 768)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Blockade')
clock = pygame.time.Clock()
dt = 1 / FPS

# Global variables
DIFFICULTY = ['EASY']
COLORBLIND = ['NO']
SERVER = ['5.135.29.120:4000']



# -----------------------------------------------------------------------------


def change_difficulty(d):
    """
    Change difficulty of the game.

    :return:
    """
    print('Selected difficulty: {0}'.format(d))
    DIFFICULTY[0] = d


def change_color(c):
    """
    Specify if player is colorblind.

    :return:
    """

    print('Colorblind : {0}'.format(c))
    COLORBLIND[0] = c

def change_server(s):
    """
    Specify which server is used.

    :return:
    """

    print('Server : {0}'.format(s))
    SERVER[0] = s



def random_color():
    """
    Return random color.

    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font):
    """
    Main game function

    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :return: None
    """
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    if difficulty == 'EASY':
        f = font.render('Playing as baby', 1, COLOR_WHITE)
    elif difficulty == 'MEDIUM':
        f = font.render('Playing as normie', 1, COLOR_WHITE)
    elif difficulty == 'HARD':
        f = font.render('Playing as god', 1, COLOR_WHITE)
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))

    # Draw random color and text
    bg_color = random_color()
    f_width = f.get_size()[0]

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)

    while True:
        # Clock tick
        clock.tick(60)

        # Application events
        playevents = pygame.event.get()
        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 217
                    return

        # Pass events to main_menu
        main_menu.mainloop(playevents)

        # Continue playing
        surface.fill((0, 102, 204))
        surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
        pygame.display.flip()


def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------


# <------> EN LIGNE MENU <------>

config = pygameMenu.TextMenu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.fonts.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size_title=30,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.8),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                text_color=COLOR_BLACK,
                                text_fontsize=20,
                                title='Configuration',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

config.add_selector('Serveur', [('5.135.29.120:4000', '5.135.29.120'),
                                             ('127.0.0.1:4000', '127.0.0.1')],
                       onreturn=None,
                       onchange=change_server)

config.add_selector('Daltonien ?', [('Non', 'NON'),
                                             ('Oui', 'OUI')],
                       onreturn=None,
                       onchange=change_color)
config.add_line(PYGAMEMENU_TEXT_NEWLINE)

config.add_option('Retour au menu', PYGAME_MENU_BACK)

# <------> PLAY MENU <------>
play_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_color_title=COLOR_WHITE,
                            menu_height=int(WINDOW_SIZE[1] * 0.8),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Jouer',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
# When pressing return -> play(DIFFICULTY[0], font)
play_menu.add_option("Jouer contre l'IA", PYGAME_MENU_BACK)
play_menu.add_option("Jouer en ligne/local", PYGAME_MENU_BACK)
play_menu.add_option("Hoster un serveur local", PYGAME_MENU_BACK)
play_menu.add_option('Retrouner au menu', PYGAME_MENU_BACK)

# <------> DEVS MENU <------>
devs_menu = pygameMenu.TextMenu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.fonts.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size_title=30,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.8),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                text_color=COLOR_BLACK,
                                text_fontsize=20,
                                title='Credits',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
for m in DEVS:
    devs_menu.add_line(m)
devs_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
devs_menu.add_option('Retour au menu', PYGAME_MENU_BACK)

# <------> TUTORIAL <------>
tutorial = pygameMenu.TextMenu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.fonts.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size_title=30,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=COLOR_WHITE,
                                menu_height=int(WINDOW_SIZE[1] * 0.8),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                text_color=COLOR_BLACK,
                                text_fontsize=20,
                                title='Tutoriel',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

tutorial.add_option('Retour au menu', PYGAME_MENU_BACK)

# <------> MAIN MENU <------>
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_color_title=COLOR_WHITE,
                            menu_height=int(WINDOW_SIZE[1] * 0.8),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Menu principal',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.add_option('Jouer', play_menu)
main_menu.add_option('Tutoriel', tutorial)
main_menu.add_option('Config', config)
main_menu.add_option('Credits', devs_menu)
main_menu.add_option('Quitter', PYGAME_MENU_EXIT)


# -----------------------------------------------------------------------------
# Main loop
while True:
    pygame.font.init()

    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)


    # Flip surface
    pygame.display.flip()
