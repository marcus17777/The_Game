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
        self.image = font.render("Credits", True, (255, 255, 255))
        self.rect = self.image.get_rect()

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        raise variables.SceneSwitcher('menu')

            self.ms = self.clock.tick(200)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image, ((self.screen_width - self.rect.width) // 2,
                                          (self.screen_height - self.rect.height) // 2))
            pygame.display.flip()
            self.master.update()
