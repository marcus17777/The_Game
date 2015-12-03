import pygame
import sys
from original import variables

__author__ = 'Markus Peterson'


class Menu(variables.Variables):
    def __init__(self, childs):
        self.childs = childs

    def __getitem__(self, item):
        return self.childs[item]

    def draw_childs(self, surface):
        startpos = (self.screen_width // 2, (self.screen_height - len(self.childs) * 30) // 2)

        for i in range(len(self.childs)):
            surface.blit(self.childs[i], (startpos[0], startpos[1] + i * 30))


class MenuNode(Menu):
    def __init__(self, font, text, childs=None, command=None, color1=(255, 255, 255), color2=(255, 0, 0)):
        Menu.__init__(self, childs)
        self.text = text
        self.font_color = color1
        self.chosen_font_color = color2
        self.command = command
        # self.pos = pos

        self.images = {
            'chosen': font.render(text, False, self.chosen_font_color),
            'normal': font.render(text, False, self.font_color)
        }
        self.current_state = 'normal'
        self.image = self.images[self.current_state]

    def __call__(self):
        self.command()

    def flip(self):
        if self.current_state == 'normal':
            self.current_state = 'chosen'
        elif self.current_state == 'chosen':
            self.current_state = 'normal'
        self.image = self.images[self.current_state]


class Main(variables.Variables):
    def __init__(self, screen, font, clock, ms, master):
        self.screen = screen
        self.font = font
        self.ms = ms
        self.clock = clock
        self.master = master

        self.menu = Menu([
            MenuNode(self.font, 'Play game', command=lambda: self.change_scene('game')),
            MenuNode(self.font, 'Intro', command=lambda: self.change_scene('intro')),
            MenuNode(self.font, 'Exit', command=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        ])
        self.current_choice = 0
        self.menu[self.current_choice].flip()

    def change_scene(self, _str):
        raise variables.Scene_switcher(_str)

    def run(self):
        print('in menu')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.menu[self.current_choice].flip()
                        self.current_choice = max([0, min(self.current_choice - 1, len(self.menu.childs) - 1)])
                        self.menu[self.current_choice].flip()
                    elif event.key == pygame.K_DOWN:
                        self.menu[self.current_choice].flip()
                        self.current_choice = max(0, min(self.current_choice + 1, len(self.menu.childs) - 1))
                        self.menu[self.current_choice].flip()
                    elif event.key == pygame.K_RETURN:
                        self.menu[self.current_choice].command()

            self.ms = self.clock.tick(200)
            self.screen.fill((0, 0, 0))
            self.menu.draw_childs(self.screen)
            pygame.display.flip()
            self.master.update()
