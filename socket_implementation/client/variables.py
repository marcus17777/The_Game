__author__ = 'Markus Peterson'


class Variables:
    """
        Class for client to hold static variables accessable to all childclasses.
        Some variables are assigned to None. Their values are asked from the server and
        are assigned to these variables in the main.py.
    """
    variables = ['screen_width',
                 'screen_height',
                 'world_map_width',
                 'world_map_height',
                 'world_map_block_size',
                 'world_map_gen_seed',
                 'world_map_octaves',
                 'world_map_frequency',
                 'world_map_gen_threshold_x',
                 'world_map_gen_threshold_y',
                 'minimap_width',
                 'minimap_height',
                 'minimap_block_size',
                 'world_map_colors',
                 'minimap_colors']

    # Variables to make socket server static.
    serveraddr = ('0.0.0.0', 8000)
    clientaddr = ('0.0.0.0', 8000)
    client_recvlimit = 1024 * 10
    client = None

    # All other game vars.
    players = {}

    # Variables that are asked from the server
    screen_width = None
    screen_height = None
    world_map_width = None
    world_map_height = None
    world_map_block_size = None
    world_map_gen_seed = None
    world_map_octaves = None
    world_map_frequency = None
    world_map_gen_threshold_x = None
    world_map_gen_threshold_y = None
    minimap_width = None
    minimap_height = None
    minimap_block_size = None
    world_map_colors = None
    minimap_colors = None
