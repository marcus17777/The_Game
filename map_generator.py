import noise, pygame, operator
import vars

__author__ = 'Markus Peterson'


class Map(vars.Variables):
    def __init__(self):
        self.maps = {}
        self.map_surfaces = {}
        self.generate_map((0, 0))
        self.current_map_idx = (0, 0)


    def generate_map(self, xy):
        filename = 'maps/map[' + str(xy[0]) + ', ' + str(xy[1]) + '].txt'
        f = open(filename, 'wt')
        # freq = 16.0 * self.world_map_octaves

        temp_map = []
        for _y in range(self.world_map_height):
            temp_map.append([])
            for _x in range(self.world_map_width):
                # """
                block = round(noise.snoise3((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                            (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                            0,
                                            octaves=self.world_map_octaves,
                                            persistence=0) * 127.0 + 128.0)
                # """
                """
                block = round(noise.snoise2((_x + xy[0] * self.world_map_width) / self.world_map_frequency,
                                            (_y + xy[1] * self.world_map_height) / self.world_map_frequency,
                                            self.world_map_octaves) * 127.0 + 128.0)
                                            """
                if block >= 0.5 * 255:
                    block = 1
                else:
                    block = 0
                f.write("%s" % block)
                temp_map[_y].append("%s" % block)
            f.write('\n')
        f.close()

        self.maps[xy] = temp_map
        self.create_map_surface(xy)

    def create_map_surface(self, xy):
        self.map_surfaces[xy] = pygame.Surface((self.world_map_width * self.world_map_block_size,
                                                self.world_map_height * self.world_map_block_size))

        for m in range(self.world_map_height):
            for n in range(self.world_map_width):
                self.map_surfaces[xy].fill(self.world_map_colors[int(self.maps[xy][m][n])],
                                           (self.world_map_block_size * n, self.world_map_block_size * m,
                                            self.world_map_block_size, self.world_map_block_size))

    def blit_all_maps(self, screen, camera_pos):
        for i in self.map_surfaces:
            screen.blit(self.map_surfaces[i],
                        ((i[0]) * self.world_map_width * self.world_map_block_size + camera_pos[0],
                         (i[1]) * self.world_map_height * self.world_map_block_size + camera_pos[1]))

    def get_map_gen_direction(self, player_pos):
        # Returns the direction in which new map should be generated
        direction = [0, 0]

        # Checks x axis
        if (player_pos[0] % self.world_map_width) > (self.world_map_width - self.world_map_gen_threshold):
            direction[0] = 1
        elif (player_pos[0] % self.world_map_width) < self.world_map_gen_threshold:
            direction[0] = -1

        # Checks y axis
        if (player_pos[1] % self.world_map_height) > (self.world_map_height - self.world_map_gen_threshold):
            direction[1] = 1
        elif (player_pos[1] % self.world_map_height) < self.world_map_gen_threshold:
            direction[1] = -1
        return direction

    def create_new_chunk(self, player_pos):
        direction = self.get_map_gen_direction(player_pos)
        self.current_map_idx = ((player_pos[0] // self.world_map_width), (player_pos[1] // self.world_map_height))

        if direction != [0, 0] or self.current_map_idx not in self.maps:
            new_map_idx = tuple(map(operator.add, self.current_map_idx, direction))

            if new_map_idx not in self.maps:
                self.generate_map(new_map_idx)

                if abs(direction[0]) + abs(direction[0]) == 2:
                    self.generate_map((new_map_idx[0], self.current_map_idx[1]))
                    self.generate_map((self.current_map_idx[0], new_map_idx[1]))
