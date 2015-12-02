import pygame
import sys
from original import variables

__author__ = 'Markus Peterson'


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, text, group, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.font_color = color
        self.image =


class Main(variables.Variables):
    def __init__(self, screen, font, clock, ms, master):
        self.screen = screen
        self.font = font
        self.ms = ms
        self.clock = clock
        self.master = master

        self.current_choice = 1
        self.current_menu = {}

        self.menu_items
        self.menu = {
            1: 'Play game',
            2: 'Credits',
            3: 'Exit'
        }

    def draw(self):

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_choice = max(0, min(self.current_choice + 1, len(self.current_menu)))
                    elif event.key == pygame.K_DOWN:
                        self.current_choice = max(0, min(self.current_choice + 1, len(self.current_menu)))
                    elif event.key == pygame.K_RETURN:
                        ...
