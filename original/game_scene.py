import os
import sys
import tkinter
import pygame
from original import variables
from original import in_game
from original import map_generator
from original import game_classes
from original import spells

__author__ = 'Markus Peterson'


# TODO Make some menu somehere in Tk

class Main(variables.Variables):
    def __init__(self, screen, font, clock, ms, master):
        """
            Main class that hooks everything up and runs the game.
        """
        # setting things up
        # variables
        self.screen = screen
        self.font = font
        self.ms = ms
        self.clock = clock
        self.master = master

        # modules to be accessible from everywhere
        variables.Variables.module_ingame = in_game
        variables.Variables.module_map_generator = map_generator
        variables.Variables.module_game_classes = game_classes
        variables.Variables.module_spells = spells

        # The Game
        variables.Variables.game = in_game.Game(master=self.master)

    def run(self):
        print('in game')
        """
            The main game loop. Has event calling inside and draws everything onto screen using the map_draw function from in_game.
            Also updates pygame.display and root tkinter.Frame.
        """
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        # self.root.destroy()
                        sys.exit()
                    else:
                        # self.game.get_vars()
                        self.game.on_event(event)

                self.ms = self.clock.tick(200)
                self.screen.fill((80, 80, 80))
                self.game.map_draw(self.screen, self.font, self.ms)
                pygame.display.flip()
                self.master.update()
                # except Exception as e:
                # print('Exception: ', e)
        finally:
            print('asd')


if __name__ == '__main__':
    game = Main()
    game.run()
