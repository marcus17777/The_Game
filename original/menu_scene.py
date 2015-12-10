import pygame
import sys
from original import variables

__author__ = 'Markus Peterson'


class MenuNode(variables.Variables):
    def __init__(self, font=None, text=None, childs=None, command=None, color1=(255, 255, 255), color2=(255, 0, 0)):
        self.text = text
        self.childs = childs
        self.font_color = color1
        self.chosen_font_color = color2
        self.command = command

        self.images = {
            1: font.render(text, True, self.chosen_font_color),  # Represents chosen node
            0: font.render(text, True, self.font_color)  # Represents normal node
        }
        self.current_state = 0
        self.image = self.images[self.current_state]
        self.current_option = 0

    def move_between_options(self, direction):
        self.current_option = max(0, min(self.current_option + direction, len(self.childs) - 1))

    def __call__(self):
        option = self.childs[self.current_option]
        if option.childs is None:
            option.command()
        else:
            return self, option

    def draw_childs(self, surface):
        startpos = (self.screen_width // 2, (self.screen_height - len(self.childs) * 30) // 2)
        for i in range(len(self.childs)):
            surface.blit(self.childs[i].image, (startpos[0], startpos[1] + i * 30))

    def update_childs(self):
        for i in range(len(self.childs)):
            temp = self.childs[i]
            if i == self.current_option:
                temp.current_state = 1
            else:
                temp.current_state = 0
            temp.image = temp.images[temp.current_state]


class Main(variables.Variables):
    def __init__(self, screen, font, clock, ms, master):
        self.screen = screen
        self.font = font
        self.ms = ms
        self.clock = clock
        self.master = master

        self.menu = MenuNode(self.font, '', childs=[
            MenuNode(self.font, 'Play game', command=lambda: self.change_scene('game')),
            MenuNode(self.font, 'Intro', command=lambda: self.change_scene('intro')),
            MenuNode(self.font, 'Options', childs=[
                MenuNode(self.font, 'A'),
                MenuNode(self.font, 'B'),
                MenuNode(self.font, 'C')
            ]),
            MenuNode(self.font, 'Credits', command=lambda: self.change_scene('credits')),
            MenuNode(self.font, 'Exit', command=lambda: self.exit_game())
        ])
        self.current_menu = self.menu
        self.last_nodes = []

    def change_scene(self, _str):
        raise variables.SceneSwitcher(_str)

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def select_option(self):
        last_node, self.current_menu = self.current_menu()
        self.last_nodes.append(last_node)

    def escape(self):
        if self.last_nodes != []:
            self.current_menu.current_option = 0
            self.current_menu = self.last_nodes[-1]
            self.last_nodes.pop()
        else:
            self.exit_game()


    def run(self):
        print('in menu')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_menu.move_between_options(-1)
                    elif event.key == pygame.K_DOWN:
                        self.current_menu.move_between_options(+1)
                    elif event.key == pygame.K_RETURN:
                        self.select_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.escape()

            self.ms = self.clock.tick(200)
            self.screen.fill((0, 0, 0))
            self.current_menu.update_childs()
            self.current_menu.draw_childs(self.screen)
            pygame.display.flip()
            self.master.update()
