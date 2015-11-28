import os
import noise
from socket_implementation.server import variables

__author__ = 'Markus Peterson'


# TODO add some seed generator DONE.
# TODO add some minerals that spawn pretty randomly between red blocks. Add some rarity argument too.

class Map(variables.Variables):
    def __init__(self):
        """
            The class that holds all map_chunks and surfaces of all map_chunks.
        """
        variables.Variables.__init__(self)
        self.map_chunks = {}
        self.map_directory = 'maps/seed=%s/' % self.world_map_gen_seed
        os.makedirs(self.map_directory, exist_ok=True)

    def get_chunk(self, xy):
        return self.map_chunks.get(xy, self.generate_map_chunk(xy))

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
                f.write("%s" % block)
                f.write('\n')
        f.close()
        self.map_chunks[xy] = temp_map
        return temp_map
