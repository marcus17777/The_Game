import os
import sys
import tkinter
import pygame
from original import variables
from original import in_game
from original import map_generator
from original import game_classes
from original import spells
from original import inventory

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
        variables.Variables.module_main = self
        variables.Variables.module_ingame = in_game
        variables.Variables.module_map_generator = map_generator
        variables.Variables.module_game_classes = game_classes
        variables.Variables.module_spells = spells
        variables.Variables.module_inventory = inventory

        # The Game
        variables.Variables.game = in_game.Game(master=self.master)

    def run(self):
        print('in game')
        """
            The main game loop. Has event calling inside and draws everything onto screen using the map_draw function from in_game.
            Also updates pygame.display and root tkinter.Frame.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # self.root.destroy()
                    sys.exit()
                else:
                    # self.game.get_vars()
                    self.game.on_event(event, self.screen)

            self.ms = self.clock.tick(300)
            self.screen.fill((80, 80, 80))
            self.game.map_draw(self.screen, self.font, self.ms)
            pygame.display.flip()
            self.master.update()


if __name__ == '__main__':
    root = tkinter.Tk()
    PygameFrame = tkinter.Frame(root, width=variables.Variables.screen_width, height=variables.Variables.screen_height)
    PygameFrame.pack(side='left')
    os.environ['SDL_WINDOWID'] = str(PygameFrame.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    # pygame
    screen = pygame.display.set_mode((variables.Variables.screen_width, variables.Variables.screen_height))
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption('The Game')
    root.protocol('WM_DELETE_WINDOW', lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
    PygameFrame.focus_set()
    screen.fill((80, 80, 80))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    ms = clock.tick(50)
    game = Main(screen, font, clock, ms, root)
    game.run()
