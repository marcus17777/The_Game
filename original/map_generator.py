import operator
import os
import noise
import pygame
from original import variables

__author__ = 'Markus Peterson'


# TODO add some seed generator DONE.
# TODO add some minerals that spawn pretty randomly between red blocks. Add some rarity argument too.

class Map(variables.Variables):
    def __init__(self):
        """
            The class that holds all map_chunks and surfaces of all map_chunks.
        """
        self.map_chunks = {}
        self.map_chunk_surfaces = {}
        self.map_directory = 'maps/seed=%s/' % self.world_map_gen_seed
        os.makedirs(self.map_directory, exist_ok=True)
        self.current_map_idx = (0, 0)
        self.generate_map_chunk((0, 0))
        # for dx, dy in itertools.product(range(-1, 2), repeat=2): self.generate_map_chunk((dx, dy))

    def generate_map_chunk(self, xy):
        """
            Generates new map chunks into the position that is provided from the tuple xy.

        :param xy: A tuple that holds coordinates of the place where new map is needed.
        """
        filename = self.map_directory + 'map[%s, %s].txt' % (str(xy[0]), str(xy[1]))
        f = open(filename, 'wt')

        temp_map = []
        for _y in range(self.world_map_height):
            temp_map.append([])
            for _x in range(self.world_map_width):
                block = round(noise.snoise3((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                            (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                            self.world_map_gen_seed * 50,
                                            octaves=self.world_map_octaves,
                                            persistence=0) * 127.0 + 128.0)
                """
                block = round(noise.snoise2((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                            (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                            self.world_map_octaves) * 127.0 + 128.0)
                                           """
                if block >= 0.9 * 255:
                    block = 2
                elif block >= 0.5 * 255:
                    block = 1
                else:
                    block = 0
                temp_map[-1].append(block)
                # f.write("%s" % block)
                # f.write('\n')
        # f.close()
        self.map_chunks[xy] = temp_map
        self.create_map_chunk_surface(xy)

    def create_map_chunk_surface(self, xy):
        """
            Generates new surfaces from map chunks. Needed for bliting the chunks onto screen.

        :param xy: Position of the map_chunk on the whole map.
        """
        self.map_chunk_surfaces[xy] = pygame.Surface((self.world_map_width * self.world_map_block_size,
                                                      self.world_map_height * self.world_map_block_size))

        for m in range(self.world_map_height):
            for n in range(self.world_map_width):
                self.map_chunk_surfaces[xy].fill(self.world_map_colors[int(self.map_chunks[xy][m][n])],
                                                 (self.world_map_block_size * n, self.world_map_block_size * m,
                                                  self.world_map_block_size, self.world_map_block_size))

    def blit_all_maps(self, screen, camera_pos):
        """
            Blits all map surface onto the screen.

        :param screen: Surface, where all the maps are blited to.
        :param camera_pos: ä
        """
        for i in self.map_chunk_surfaces:
            screen.blit(self.map_chunk_surfaces[i],
                        ((i[0]) * self.world_map_width * self.world_map_block_size + camera_pos[0],
                         (i[1]) * self.world_map_height * self.world_map_block_size + camera_pos[1]))

    def get_current_chunk(self):
        current_chunk = []
        """
        for row in range(-1, 2):
            try:
                current_chunk += [i + j + k for i, j, k in zip(*[getattr(self.map_chunks[tuple(map(operator.add, self.current_map_idx, (column, row)))], [['' for n in range(self.world_map_width)] for m in range(self.world_map_height)]) for column in range(-1, 2)])]
            except: pass
        """
        # """
        for row in range(-1, 2):
            current_row = []
            for column in range(-1, 2):
                try:
                    current_row += [self.map_chunks[tuple(map(operator.add, self.current_map_idx, (column, row)))]]
                except:
                    current_row += [[['' for n in range(self.world_map_width)] for m in range(self.world_map_height)]]

            current_chunk += [i + j + k for i, j, k in zip(*current_row)]
        # """
        return current_chunk

    def get_map_gen_direction(self, player_pos):
        # Returns the direction in which new map should be generated
        direction = [0, 0]

        # Checks x axis
        if (player_pos[0] % self.world_map_width) > (self.world_map_width - self.world_map_gen_threshold_x):
            direction[0] = 1
        elif (player_pos[0] % self.world_map_width) < self.world_map_gen_threshold_x:
            direction[0] = -1

        # Checks y axis
        if (player_pos[1] % self.world_map_height) > (self.world_map_height - self.world_map_gen_threshold_y):
            direction[1] = 1
        elif (player_pos[1] % self.world_map_height) < self.world_map_gen_threshold_y:
            direction[1] = -1
        return direction

    def create_new_chunk(self, player_pos):
        direction = self.get_map_gen_direction(player_pos)
        self.current_map_idx = ((player_pos[0] // self.world_map_width), (player_pos[1] // self.world_map_height))
        self.new_map_idx = tuple(map(operator.add, self.current_map_idx, direction))

        if direction != [0, 0] or self.current_map_idx not in self.map_chunks:
            if self.new_map_idx not in self.map_chunks:
                self.generate_map_chunk(self.new_map_idx)

                if abs(direction[0]) + abs(direction[0]) == 2:
                    self.generate_map_chunk((self.new_map_idx[0], self.current_map_idx[1]))
                    self.generate_map_chunk((self.current_map_idx[0], self.new_map_idx[1]))


class MapGenerator(object):
    def __init__(self, position, x, y, z, octaves=1, persistence=0.5, lacunarity=2.0):
        """
            Perlin noise map generator class for multiprocessing.

        :param position: Position of the block on the map chunk
        :param x: x - offset for Perlin noise.
        :param y: y - offset for Perlin noise.
        :param z: z - offset for Perlin noise.
        :param octaves:
        :param persistence:
        :param lacunarity:
        """
        self.position = position
        self.x = x
        self.y = y
        self.z = z
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

    def __call__(self):
        return (
        round(noise.snoise3(self.x, self.y, self.x, self.octaves, self.persistence, self.lacunarity) * 127.0 + 128.0),
        self.position)
