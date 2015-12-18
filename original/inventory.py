import pygame
import sys
from original import variables

__author__ = 'Markus Peterson'


class Item(variables.Variables):
    def __init__(self, name, quantity, image):
        self.name = name
        self.quantity = quantity
        self.image = image

    def __str__(self):
        return "Item: %s, Quantity: %d" % (self.name, self.quantity)


class Inventory(variables.Variables):
    def __init__(self, owner):
        self.owner = owner
        self.items = []

        self.backround = pygame.transform.scale(pygame.image.load('pics/minecraft_inventory_window.jpg'), (400, 400))
        # First tile (20, 372), (96, 439)
        self.rect = self.backround.get_rect()
        self.rect.x = (self.screen_width - self.rect.width) // 2
        self.rect.y = (self.screen_height - self.rect.height) // 2

    def __add__(self, other):
        self.items.append(other)

    def __sub__(self, other):
        self.items.remove(other)

    def display(self, screen):
        # screen.fill((0, 0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        return
            screen.blit(self.backround, self.rect)
            pygame.display.flip()
            self.game.master.update()
