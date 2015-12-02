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

        self.fade_rate = 1
        self.screen.fill((100, 100, 100))
        self.image = self.font.render("Tere", False, (255, 255, 255)).convert()
        self.screen.blit(self.image, (0, 0))

    def run(self):
        print('in intro')
        fade = 0
        fadeIn = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        raise variables.Scene_switcher('game')

            if fade >= 255 and fadeIn:
                fadeIn = False
                self.fade_rate = -self.fade_rate
            elif fade <= 0 and not fadeIn:
                raise variables.Scene_switcher('game')
            else:
                fade += self.fade_rate
                self.image.set_alpha(fade)

            self.ms = self.clock.tick(200)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.image, (self.screen_width // 2, self.screen_height // 2))

            pygame.display.flip()
            self.master.update()
