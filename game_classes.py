import pygame, itertools
import vars

__author__ = 'Markus Peterson'


class Character(vars.Variables):
    def __init__(self, pos):
        self.pos = pos

    def collision_detect(self, map):
        around = []
        pos_on_map = (self.pos[0] % (self.world_map_width - 1), self.pos[1] % (self.world_map_height - 1))
        print(self.pos, pos_on_map)
        for dx, dy in itertools.product(range(-1, 1 + 1), repeat=2):
            if dx == dy == 0:
                around.append("#")
            else:
                around.append(map[pos_on_map[0] + dx][pos_on_map[1] + dy])
        return around


class Player(Character):
    def __init__(self, pos):
        Character.__init__(self, pos)
        self.color = (255, 0, 0)
        self.size = (self.world_map_block_size, 2*self.world_map_block_size)
        self.pos_onscreen = [self.screen_width//2 - self.size[0]/2,
                             self.screen_height//2 - self.size[1]/2]
        self.move_direction = [0, 0]
        # self.real_speed = 0.04 # default
        self.real_speed = 0.05
        self.real_pos = self.pos

        self.move_commands = {
            'forward':  (1, -1),
            'backward': (1, 1),
            'right':    (0, 1),
            'left':     (0, -1),
            'stop_y':   (1, 0),
            'stop_x':   (0, 0)
        }

    def move(self, direction):
        modifier = self.move_commands[direction]
        self.move_direction[modifier[0]] = modifier[1]

    def update(self, screen, ms):
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), 3)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        self.real_pos = [self.real_pos[0] + self.move_direction[0] * self.real_speed * ms,
                         self.real_pos[1] + self.move_direction[1] * self.real_speed * ms]

        self.pos[0] = round(self.real_pos[0])
        self.pos[1] = round(self.real_pos[1])
        #print(self.collision_detect(map))
