import random
import argparse
import pygame

__author__ = 'Markus Peterson'

# TODO argparser for seed input from command line ^.^ DONE
argparser = argparse.ArgumentParser(description='Mäng')
argparser.add_argument('seed', help='sisesta, et genereerida kindel kaart', default=None, nargs='?')
args = argparser.parse_args()


class SceneSwitcher(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class Variables:
    """
        Just a class to store variables. Can be used as a parent class for easy access in every module.
    """
    # MODULES
    module_main = None
    module_ingame = None
    module_map_generator = None
    module_game_classes = None
    module_spells = None
    module_inventory = None

    game = None
    # map_generator = None

    # SCREEN
    screen_width = 800
    screen_height = 600
    camera_pos = []

    # MAP_GEN
    world_map_width = 64
    world_map_height = 64
    world_map_block_size = 16
    world_map_gen_seed = int(args.seed) if args.seed is not None else random.random()

    world_map_octaves = 2
    world_map_frequency = 16 * world_map_octaves
    world_map_gen_threshold_x = 40
    world_map_gen_threshold_y = 40

    # PARTICLES AND SPELLS
    spell_group = pygame.sprite.Group()
    character_group = pygame.sprite.Group()

    # MINIMAP
    minimap_width = 150
    minimap_height = 150
    minimap_block_size = 2

    # COLORS
    world_map_colors = {
        0: (10, 10, 10),
        1: (100, 0, 0),
        2: (0, 0, 255),
        3: (45, 0, 0),
        4: (100, 0, 100),
        11: (100, 100, 10),
        12: (10, 100, 100),
        13: (0, 45, 0),
    }

    minimap_colors = {
        0: (25, 25, 25),
        1: (65, 65, 65),
        2: (75, 75, 75),
        3: (45, 0, 0),
        4: (100, 0, 100),
        11: (50, 100, 0),
        12: (10, 100, 100),
        13: (0, 45, 0),
    }
