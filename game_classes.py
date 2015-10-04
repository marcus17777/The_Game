__author__ = 'Markus Peterson'
import pygame, itertools
import vars

class Character(vars.Variables):
    def __init__(self, pos):
        self.pos = pos

    def collision_detect(self, map):
        around = []
        for dx, dy in itertools.product(range(-3, 4), repeat=2):
            around.append(map[self.pos[0]+dx][self.pos[1]+dy])
        print(around)


class Player(Character):
    def __init__(self, pos):
        Character.__init__(self, pos)
        self.color = (255, 0, 0)
        self.size = (self.world_map_block_size, 2*self.world_map_block_size)
        self.pos_onscreen = [self.screen_width//2 - self.size[0]/2,
                             self.screen_height//2 - self.size[1]/2]
        self.speed_xy = [0, 0]
        #self.real_speed = 0.04 //default
        self.real_speed = 0.125
        self.real_pos = self.pos

    def move(self, direction):
        def modify_speed_xy(index, value):
            self.speed_xy[index] = value

        move_commands = {
            'forward':  (1, -1),
            'backward': (1, 1),
            'right':    (0, 1),
            'left':     (0, -1),
            'stop_y':   (1, 0),
            'stop_x':   (0, 0)
        }
        modifier = move_commands[direction]
        modify_speed_xy(modifier[0], modifier[1])

    def update(self, screen, ms, map):
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), 3)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        self.real_pos = [self.real_pos[0]+self.speed_xy[0]*self.real_speed*ms, self.real_pos[1]+self.speed_xy[1]*self.real_speed*ms]

        #self.pos_onscreen[0] = self.pos[0] = round(self.real_pos[0])
        #self.pos_onscreen[1] = self.pos[1] = round(self.real_pos[1])
        self.pos[0] = round(self.real_pos[0])
        self.pos[1] = round(self.real_pos[1])
        #print(self.pos)
        #self.collision_detect(map)

#mainplayer = Player((0, 0))