import random, argparse, multiprocessing

__author__ = 'Markus Peterson'

# TODO argparser for seed input from command line ^.^ DONE
argparser = argparse.ArgumentParser(description='Mäng')
argparser.add_argument('seed', help='sisesta, et genereerida kindel kaart', default=None, nargs='?')
args = argparser.parse_args()


class Variables:
    """
        Just a class to store variables. Can be used as a parent class for easy access in every module.
    """
    # SCREEN
    screen_width = 1200
    screen_height = 900

    # MAP_GEN
    world_map_width = 64
    world_map_height = 64
    world_map_block_size = 4
    world_map_gen_seed = int(args.seed) if args.seed is not None else random.random()

    world_map_octaves = 2
    world_map_frequency = 16 * world_map_octaves
    world_map_gen_threshold_x = 20
    world_map_gen_threshold_y = 20

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
