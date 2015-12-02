import tkinter
import pygame
import os
from original import intro_scene
from original import game_scene
from original import variables

__author__ = 'Markus Peterson'


class Main(variables.Variables):
    def __init__(self):
        # tkinter frame
        self.root = tkinter.Tk()
        self.PygameFrame = tkinter.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.PygameFrame.pack(side='left')
        os.environ['SDL_WINDOWID'] = str(self.PygameFrame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('The Game')
        self.PygameFrame.focus_set()
        self.screen.fill((80, 80, 80))
        self.font = pygame.font.Font(None, 18)
        self.clock = pygame.time.Clock()
        self.ms = self.clock.tick(50)

        self.scenes = {
            'intro': intro_scene.Main(self.screen, self.font, self.clock, self.ms, self.root),
            'menu': '',
            'game': game_scene.Main(self.screen, self.font, self.clock, self.ms, self.root),
            'outro': '',
        }

        self.current_scene = 'intro'

    def run(self):
        while True:
            try:
                self.scenes[self.current_scene].run()
            except variables.Scene_switcher as sw:
                self.current_scene = sw.value


if __name__ == '__main__':
    g = Main()
    g.run()
