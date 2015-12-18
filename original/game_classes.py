import itertools
import math
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
        self.real_pos = pos
        self.size = (0, 0)
        self.move_direction = [0, 0]
        self.desired_direction = [0, 0]
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

        try:
            calc_pos = [self.pos[0] + (self.size[0] // (2 * self.world_map_block_size)),
                        self.pos[1] + (self.size[1] // (2 * self.world_map_block_size))]
            self.move_direction = [
                (1 - bool(self.game.map_generator.get_block(
                        (calc_pos[0] + self.desired_direction[0], calc_pos[1])).state)) * self.desired_direction[0],
                (1 - bool(self.game.map_generator.get_block(
                        (calc_pos[0], calc_pos[1] + self.desired_direction[1])).state)) * self.desired_direction[1]]
            if bool(self.game.map_generator.get_block(
                    (calc_pos[0] + self.move_direction[0], calc_pos[1] + self.move_direction[1])).state) == True:
                self.move_direction = [0, 0]
        except KeyError as e:
            self.game.map_generator.generate_map_chunk(e.args[0])


class Spectator(Character):
    def __init__(self, pos):
        Character.__init__(self, pos)
        self.real_speed = 0.02
        self.weapon = self.module_spells.SpectatorGun(self)

    def update(self, screen, ms):
        self.move_direction = self.desired_direction
        self.real_pos = [self.real_pos[0] + self.move_direction[0] * self.real_speed * ms,
                         self.real_pos[1] + self.move_direction[1] * self.real_speed * ms]

        self.pos = list(map(round, self.real_pos))


class Player(Character):
    def __init__(self, pos=None):
        """
            The sublcass of Character. This is the main player that the user can move and control.

        :param pos: Position of the player.
        """
        Character.__init__(self, pos)
        self.color = (0, 0, 255)
        self.size = (self.world_map_block_size, self.world_map_block_size)
        self.pos_onscreen = [self.screen_width // 2 - self.size[0] / 2, self.screen_height // 2 - self.size[1] / 2]
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.hit_score = 0
        self.hurt_score = 0

        self.real_speed = 0.02

        self.weapon = self.module_spells.SingleShotCannon(self)
        self.weapon.ammo = "SimpleBullet"  # Should be class name of the ammo
        self.weapon.amount_of_ammo = 1000

        self.tool = self.module_spells.BlockRemover(self, 1000000000000000000, 3)

        self.inventory = self.module_inventory.Inventory(self)

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
        screen.blit(self.image, self.pos_onscreen)

        if self.weapon != None: self.weapon.draw(screen)
        self.weapon.update(ms)

        self.collision_detect()
        # self.move_direction = self.desired_direction
        self.real_pos = [self.real_pos[0] + self.move_direction[0] * self.real_speed * ms,
                         self.real_pos[1] + self.move_direction[1] * self.real_speed * ms]

        self.pos = list(map(round, self.real_pos))

        # print(self.pos)

    def shoot(self, mouse_pos):
        self.weapon.shoot(math.atan2(mouse_pos[1] - self.pos_onscreen[1], mouse_pos[0] - self.pos_onscreen[0]))


class ML(variables.Variables):
    epoch = 0

    def __init__(self, number_of_inputs, number_of_outputs):
        self.input = []
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.init_weight = math.sqrt(6 / (self.number_of_inputs + self.number_of_outputs))
        self.structure = [
            [random.uniform(-self.init_weight, self.init_weight) for input in range(self.number_of_inputs)] for output
            in range(self.number_of_outputs)]
        self.hit_score = 0
        self.hurt_score = 0

    def hypothesis(self):
        return [math.atan(sum([self.input[i] * self.structure[node][i] for i in range(self.number_of_inputs)])) for node
                in range(self.number_of_outputs)]

    def mutate(self, mutation_coefficient):
        for i in range(len(self.structure)):
            for j in range(len(self.structure[i])):
                self.structure[i][j] += random.gauss(0, 1) / 3 * mutation_coefficient

    @staticmethod
    def learn():
        temp = sorted(list(variables.Variables.character_group), key=lambda x: x.hit_score - x.hurt_score)
        print(temp)
        variables.Variables.character_group.empty()
        variables.Variables.character_group.add(*temp[0:round(len(temp) * 0.2)])
        variables.Variables.character_group.add(
                NPC(4, 20, pos=[variables.Variables.world_map_width // 2, variables.Variables.world_map_height // 2])
                for i in range(len(temp) - round(len(temp) * 0.2)))
        ML.epoch += 1


class NPC(ML, Character, pygame.sprite.Sprite):
    def __init__(self, sectors, vision_radius, pos=None, color=None):
        pygame.sprite.Sprite.__init__(self, variables.Variables.character_group)
        Character.__init__(self, pos)

        ML.__init__(self, sectors, 3)

        self.virtual_mouse = [0, 0]
        self.vision_radius = vision_radius
        self.sectors = sectors
        self.sector_angle = 360 / sectors

        self.weapon = self.module_spells.SingleShotCannon(self)
        self.weapon.ammo = "SimpleBullet"  # Should be class name of the ammo
        self.weapon.amount_of_ammo = -1
        self.tool = None
        self.inventory = None

        self.size = (self.world_map_block_size * 2, self.world_map_block_size * 2)
        self.color = color if color != None else (
        random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.real_pos[0]
        self.rect.y = self.real_pos[1]

    @staticmethod
    def calc_distance(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def get_vision(self):
        temp = [-1 for i in range(self.sectors)]
        for other in self.character_group:
            if other != self and self.calc_distance(self.pos, other.pos) <= self.vision_radius:
                temp[int(math.atan2(other.pos[1] - self.pos[1], other.pos[0] - self.pos[0]) // self.sector_angle)] = 1
        self.input = temp

    def take_action(self, ms):
        self.get_vision()
        hypothesis = list(self.hypothesis())
        self.desired_direction = list(map(lambda x: 1 if x > 0 else -1 if x < 0 else 0, hypothesis[0:2]))
        self.collision_detect()
        # self.move_direction = self.desired_direction

        self.real_pos[0] += (hypothesis[0] * self.move_direction[0]) * 0.01 * ms
        self.real_pos[1] += (hypothesis[1] * self.move_direction[1]) * 0.01 * ms

        self.pos = list(map(round, self.real_pos))

        if hypothesis[2] > 0:
            self.weapon.shoot(math.atan2(hypothesis[1], hypothesis[0]))

    def update(self, ms):
        self.take_action(ms)
        # print(self.hit_others_score, self.hurt_score, self.hypothesis())
        self.rect.x = self.real_pos[0] * self.world_map_block_size + self.camera_pos[0]
        self.rect.y = self.real_pos[1] * self.world_map_block_size + self.camera_pos[1]
