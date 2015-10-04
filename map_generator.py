__author__ = 'Markus Peterson'

import noise, pygame, operator
import vars


class Map(vars.Variables):
    def __init__(self):
        self.maps = {}
        self.map_surfaces = {}
        self.generate_map((0, 0))
        self.generate_map((-1, 0))
        self.join_all_maps()

    def generate_map(self, xy):
        #filename = 'maps/map[' + str(x) + ', ' + str(y) + '].txt'
        #f = open(filename, 'wt')
        freq = 16.0 * self.world_map_octaves

        temp_map = []
        for _y in range(self.world_map_height):
            temp_map.append([])
            for _x in range(self.world_map_width):
                item = round(noise.snoise3((_x+xy[0]*self.world_map_width) / freq, (_y+xy[1]*self.world_map_height) / freq, 0, octaves=self.world_map_octaves, persistence=0) * 127.0 + 128.0)
                # item = round(noise.snoise2((_x+x) / freq, (_y+y) / freq, vars.map_octaves) * 127.0 + 128.0)
                if item >= 0.5*255:
                    item = 1
                else:
                    item = 0
                #f.write("%s" % item)
                temp_map[_y].append("%s" % item)
            #f.write('\n')
        #f.close()
        self.maps[xy] = temp_map
        self.create_map_surface(xy)

    def create_map_surface(self, xy):
        self.map_surfaces[xy] = pygame.Surface((self.world_map_width*self.world_map_block_size,
                                                self.world_map_height*self.world_map_block_size))
        for m in range(len(self.maps[xy])):
            for n in range(len(self.maps[xy][m])):
                self.map_surfaces[xy].fill(self.world_map_colors[int(self.maps[xy][m][n])],
                                          (self.world_map_block_size*n, self.world_map_block_size*m,
                                           self.world_map_block_size, self.world_map_block_size))

    def join_all_maps(self):
        temp_x = []
        temp_y = []

        for i in self.map_surfaces:
            temp_x.append(i[0])
            temp_y.append(i[1])

        greatest_positive_x = max(temp_x)
        greatest_positive_y = max(temp_y)
        greatest_negative_x = min(temp_x)
        greatest_negative_y = min(temp_y)


        whole_map_size = [greatest_positive_x + abs(greatest_negative_x),
                          greatest_positive_y + abs(greatest_negative_y)]

        self.whole_map_surface = pygame.Surface((whole_map_size[0]*self.world_map_width*self.world_map_block_size,
                                                 whole_map_size[1]*self.world_map_height*self.world_map_block_size))
        self.whole_map_surface.fill((80, 80, 80))

        for i in self.map_surfaces:
            self.whole_map_surface.blit(self.map_surfaces[i], ((i[0]) * self.world_map_width*self.world_map_block_size,
                                                               (i[1]) * self.world_map_height*self.world_map_block_size))



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
        if direction != [0, 0]:
            current_map_idx = ((player_pos[0]//self.world_map_width), (player_pos[1]//self.world_map_height))
            new_map_idx = tuple(map(operator.add, current_map_idx, direction))
            if new_map_idx not in self.maps:
                self.generate_map(new_map_idx)
                self.join_all_maps()
                """
                if abs(direction[0]) + abs(direction[0]) == 2:
                    self.generate_map((new_map_idx[0], current_map_idx[1]))
                    self.generate_map((current_map_idx[0], new_map_idx[1]))"""

