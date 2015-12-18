import pygame
import sys
from original import variables

__author__ = 'Markus Peterson'


class Main(variables.Variables):
    def __init__(self, screen, font, clock, ms, master):
        self.screen = screen
        self.font = font
        self.ms = ms
        self.clock = clock
        self.master = master

        # self.fade_rate = 1
        # self.image = self.font.render("Tere", False, (255, 255, 255)).convert()
        self.movie = pygame.movie.Movie('pics/intro.mpg')
        self.movie.set_display(self.screen, self.screen.get_rect())

    def run(self):
        print('in intro')
        self.movie.play()
        while self.movie.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.movie.rewind()
                        self.movie.stop()
                        raise variables.SceneSwitcher('menu')

            self.ms = self.clock.tick(200)
            pygame.display.flip()
            self.master.update()
        self.movie.rewind()
        self.movie.stop()
        raise variables.SceneSwitcher('menu')
