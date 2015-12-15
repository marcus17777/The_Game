import operator
import os
import noise
import pygame
import itertools
from original import variables

__author__ = 'Markus Peterson'


# TODO add some seed generator DONE.
# TODO add some minerals that spawn pretty randomly between red blocks. Add some rarity argument too.

class MapGenerator(variables.Variables):
    def __init__(self, ):
        """
            The class that holds all map_chunks and surfaces of all map_chunks.
        """
        self.map_directory = 'maps/seed=%s/' % self.world_map_gen_seed
        self.map_chunks = {}
        os.makedirs(self.map_directory, exist_ok=True)
        self.current_map_idx = (0, 0)
        self.generate_map_chunk((0, 0))
        # for dx, dy in itertools.product(range(-1, 2), repeat=2): self.generate_map_chunk((dx, dy))

    def __getitem__(self, item):
        return self.map_chunks[item]

    def get_block(self, pos):
        idx, pos_on_map = self.convert_coords(pos)
        return self.map_chunks[idx][pos_on_map[1]][pos_on_map[0]]


    def change_block(self, pos, new_id):
        idx, pos_on_map = self.convert_coords(pos)
        self.map_chunks[idx][pos_on_map[1]][pos_on_map[0]].change_block(new_id)

    def generate_map_chunk(self, xy):
        self.map_chunks[xy] = Chunk(xy)

    def convert_coords(self, pos):
        map_chunk_id = (pos[0] // self.world_map_width,
                        pos[1] // self.world_map_height)
        pos_on_map = (pos[0] % self.world_map_width,
                      pos[1] % self.world_map_height)
        print(map_chunk_id, pos_on_map, pos)
        return map_chunk_id, pos_on_map

    def blit_all_maps(self, screen, camera_pos):
        """
            Blits all map surface onto the screen.
        :param screen: Surface, where all the maps are blited to.
        :param camera_pos: ääöö
        """
        for index, chunk in self.map_chunks.items():
            screen.blit(chunk.surface,
                        ((index[0]) * self.world_map_width * self.world_map_block_size + camera_pos[0],
                         (index[1]) * self.world_map_height * self.world_map_block_size + camera_pos[1]))

    # def get_current_chunk(self):
    #     current_chunk = []
    #     """
    #     for row in range(-1, 2):
    #         try:
    #             current_chunk += [i + j + k for i, j, k in zip(*[getattr(self.map_chunks[tuple(map(operator.add, self.current_map_idx, (column, row)))], [['' for n in range(self.world_map_width)] for m in range(self.world_map_height)]) for column in range(-1, 2)])]
    #         except: pass
    #     """
    #     # """
    #     for row in range(-1, 2):
    #         current_row = []
    #         for column in range(-1, 2):
    #             try:
    #                 current_row += [self.map_chunks[tuple(map(operator.add, self.current_map_idx, (column, row)))]]
    #             except:
    #                 current_row += [[[None for n in range(self.world_map_width)] for m in range(self.world_map_height)]]
    #
    #         current_chunk += [i + j + k for i, j, k in zip(*current_row)]
    #     # """
    #     return current_chunk

    def get_map_gen_direction(self, player_pos):
        # Returns the direction in which new map should be generated
        direction = [0, 0]

        # Checks x axis
        if player_pos[0] > (self.world_map_width - self.world_map_gen_threshold_x):
            direction[0] = 1
        elif player_pos[0] < self.world_map_gen_threshold_x:
            direction[0] = -1

        # Checks y axis
        if player_pos[1] > (self.world_map_height - self.world_map_gen_threshold_y):
            direction[1] = 1
        elif player_pos[1] < self.world_map_gen_threshold_y:
            direction[1] = -1
        return direction

    def create_new_chunk(self, player_pos):
        self.current_map_idx, player_pos_on_map = self.convert_coords(player_pos)
        direction = self.get_map_gen_direction(player_pos_on_map)
        new_map_idx = tuple(map(operator.add, self.current_map_idx, direction))

        if direction != [0, 0] or self.current_map_idx not in self.map_chunks:
            if new_map_idx not in self.map_chunks:
                self.generate_map_chunk(new_map_idx)

                if abs(direction[0]) + abs(direction[0]) == 2:
                    self.generate_map_chunk((new_map_idx[0], self.current_map_idx[1]))
                    self.generate_map_chunk((self.current_map_idx[0], new_map_idx[1]))


class Chunk(variables.Variables):
    def __init__(self, index):
        self.index = index
        self.blocks = []
        self.surface = pygame.Surface((self.world_map_block_size * self.world_map_width,
                                       self.world_map_block_size * self.world_map_height))
        self.generate_chunk(self.index)

    def __getitem__(self, item):
        return self.blocks[item]

    def generate_chunk(self, xy):
        """
            Generates new map chunks into the position that is provided from the tuple xy.
        :param xy: A tuple that holds coordinates of the place where new map is needed.
        """
        # filename = self.map_directory + 'map[%s, %s].txt' % (str(xy[0]), str(xy[1]))
        # f = open(filename, 'wt')

        for _y in range(self.world_map_height):
            self.blocks.append([])
            for _x in range(self.world_map_width):
                temp = round(noise.snoise3((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                           (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                           self.world_map_gen_seed * 50,
                                           octaves=self.world_map_octaves,
                                           persistence=0) * 127.0 + 128.0)
                """
                block = round(noise.snoise2((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                            (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                            self.world_map_octaves) * 127.0 + 128.0)
                                           """
                if temp >= 0.9 * 255:
                    state = 2
                elif temp >= 0.5 * 255:
                    state = 1
                else:
                    state = 0
                self.surface.fill(self.world_map_colors[state],
                                  (self.world_map_block_size * _x, self.world_map_block_size * _y,
                                   self.world_map_block_size, self.world_map_block_size))
                self.blocks[-1].append(Block(self, (_x, _y), state))
                # f.write("%s" % block)
                # f.write('\n')
                # f.close()


class Block(variables.Variables):
    def __init__(self, chunk, index, state):
        self.chunk = chunk
        self.index = index
        self.state = state
        self.item = None

    def change_block(self, new_state):
        self.state = new_state
        self.chunk.surface.fill(self.world_map_colors[self.state],
                                (self.world_map_block_size * self.index[0], self.world_map_block_size * self.index[1],
                                 self.world_map_block_size, self.world_map_block_size))

    def delete_block(self):
        self.change_block(0)
        return self.item
