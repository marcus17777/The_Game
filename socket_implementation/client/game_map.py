import pickle
import operator
import pygame
from socket_implementation.client import variables

__author__ = 'Markus Peterson'


class World_Map(variables.Variables):
    def __init__(self):
        self.map_chunks = {}
        self.map_chunks_surfaces = {}
        self.current_map_idx = (0, 0)

    def get_chunk(self, xy):
        try:
            return self.map_chunks[xy]
        except KeyError:
            self.client.send(pickle.dumps(('request map_chunk', xy)))
            msg, addr = self.client.recvfrom(self.client_recvlimit)
            msg = pickle.loads(msg)
            cmd = msg[0]
            msg = msg[1]
            if 'respond map_chunk' in cmd:
                self.map_chunks[msg[1]] = msg[0]
                self.map_chunks_surfaces[msg[1]] = self.create_map_chunk_surface(msg[0])
                return msg

    def get_chunk_surface(self, xy):
        try:
            return self.map_chunks_surfaces[xy]
        except KeyError:
            self.map_chunks_surfaces[xy] = self.create_map_chunk_surface(self.get_chunk(xy))
            return self.map_chunks_surfaces[xy]

    def create_map_chunk_surface(self, chunk):
        """
            Generates new surfaces from map chunks. Needed for bliting the chunks onto screen.
        """
        temp = pygame.Surface((self.world_map_width * self.world_map_block_size,
                               self.world_map_height * self.world_map_block_size))

        for m in range(self.world_map_height):
            for n in range(self.world_map_width):
                temp.fill(self.world_map_colors[int(chunk[m][n])],
                          (self.world_map_block_size * n, self.world_map_block_size * m,
                           self.world_map_block_size, self.world_map_block_size))
        return temp

    def blit_all_maps(self, screen, camera_pos):
        """
            Blits all map surface onto the screen.

        :param screen: Surface, where all the maps are blited to.
        :param camera_pos: ä
        """
        for i in self.map_chunks_surfaces:
            screen.blit(self.map_chunks_surfaces[i],
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
                self.get_chunk(self.new_map_idx)

                if abs(direction[0]) + abs(direction[0]) == 2:
                    self.get_chunk((self.new_map_idx[0], self.current_map_idx[1]))
                    self.get_chunk((self.current_map_idx[0], self.new_map_idx[1]))
