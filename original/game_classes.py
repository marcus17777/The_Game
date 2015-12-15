import itertools
import pygame
import random
from original import variables

__author__ = 'Markus Peterson'


# TODO Make the fucking collision detection to work.
# TODO      Almost works
# TODO Create some other characters too. Ex. mobs or something.

class Character(variables.Variables):
    def __init__(self, pos):
        """
            The main class for creating different character classes. This is like a parent for every
            character in the game.
            Ex: Player.

        :param pos: Position of the character
        """
        if pos == None: self.spawn_randomly()
        self.pos = pos
        self.real_pos = self.pos
        self.move_direction = [0, 0]
        self.desired_direction = [0, 0]

    def spawn_randomly(self):
        # map_chunk = (int(random.random()*random.randint(0, 100)), int(random.random()*random.randint(0, 100)))
        map_chunk = (0, 0)
        while True:
            temp = [random.randint(0, self.screen_width // self.world_map_block_size),
                    random.randint(0, self.screen_height // self.world_map_block_size)]
            if self.game.map_generator.map_chunks[map_chunk][temp[1]][temp[0]] == 0:
                self.pos = temp
                break

    def collision_detect(self):
        """
            Collison detection for every character. Allows to move only on certain block on the map.
            Currently in development.
        :param map: The current map (9 chunks - 3x3) where the character is standing on.
        """
        # pos_on_map = (self.pos[0] % self.world_map_width + self.world_map_width,
        #               self.pos[1] % self.world_map_height + self.world_map_height)

        self.move_direction = [
            (1 - bool(self.game.map_generator.get_block(
                (self.real_pos[0] + self.desired_direction[0], self.real_pos[1])).state)) * self.desired_direction[0],
            (1 - bool(self.game.map_generator.get_block(
                (self.real_pos[0], self.real_pos[1] + self.desired_direction[1])).state)) * self.desired_direction[1]]
        if bool(self.game.map_generator.get_block(
                (self.real_pos[0] + self.move_direction[0], self.real_pos[1] + self.move_direction[1])).state) == True:
            self.move_direction = [0, 0]


class Player(Character):
    def __init__(self, pos=None):
        """
            The sublcass of Chaeracter. This is the main player that the user can move and control.

        :param pos: Position of the player.
        """
        Character.__init__(self, pos)
        self.color = (255, 0, 0)
        self.size = (self.world_map_block_size, 2 * self.world_map_block_size)
        self.pos_onscreen = [self.screen_width // 2 - self.size[0] / 2, self.screen_height // 2 - self.size[1] / 2]
        self.real_speed = 0.02

        self.weapon = self.module_spells.Shotgun(self)
        self.weapon.ammo = "SimpleBullet"  # Should be class name of the ammo
        self.weapon.amount_of_ammo = 1000

        self.tool = self.module_spells.BlockRemover(self, 10)

        self.inventory = self.module_inventory.Inventory(self)

        self.move_commands = {
            'forward': (1, -1),
            'backward': (1, 1),
            'right': (0, 1),
            'left': (0, -1),
            'stop_y': (1, 0),
            'stop_x': (0, 0)
        }

    def move(self, direction):
        """
            Function for modifying the move_direction tuple of the player using move_command dictionary.

        :param direction: The direction where player wants to move.
        """
        modifier = self.move_commands[direction]
        self.desired_direction[modifier[0]] = modifier[1]

    def update(self, screen, ms):
        """
            A function for updating the state and position on the map of the player.

        :param screen: A surface where the player is drawed.
        :param ms: A parameter that is used for movement speed calculations. The player should move always at the same
                    speed and the movement speed doesn't depend on the fps.
        :param current_chunk: Current chunk of the map where the player is currently standing on.
        """
        """
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), 3)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        """
        pygame.draw.rect(screen, (0, 100, 0), (
            self.pos_onscreen[0], self.pos_onscreen[1], self.world_map_block_size, self.world_map_block_size))

        if self.weapon != None: self.weapon.draw(screen)
        self.weapon.update(ms)

        self.collision_detect()
        self.real_pos = [self.real_pos[0] + self.move_direction[0] * self.real_speed * ms,
                         self.real_pos[1] + self.move_direction[1] * self.real_speed * ms]

        self.pos[0] = round(self.real_pos[0])
        self.pos[1] = round(self.real_pos[1])

        # print(self.pos)


class NPC(Character, pygame.sprite.Sprite):
    def __init__(self, pos=None, color=(100, 100, 0)):
        pygame.sprite.Sprite.__init__(self, variables.Variables.npc_group)
        Character.__init__(self, pos)

        self.virtual_mouse = [0, 0]
        self.pos = pos

        self.weapon = None
        self.ammo = None
        self.tool = None
        self.inventory = None

        self.size = (40, 40)
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit()
