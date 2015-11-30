import pygame
import math
import itertools
import operator
from original import variables

__author__ = 'Markus Peterson'


class Cannon:
    def __init__(self, owner):
        """
            Abstract class for all weapons. Defines what general variables a weapon should have.

            :param owner: Current owner of the weapon. Default value is None and means that weapon has no owner.
        """
        self.owner = owner
        self.ammo = None
        self.amount_of_ammo = 0
        self.delay = 0

        self.starttick = 0

    def shoot(self, mouse_click_pos):
        """
            Method to override in subclasses.

        :param mouse_click_pos:
        """
        pass


class Tool(variables.Variables):
    def __init__(self, owner):
        """
            Abstract class for tools

        :param owner: Current owner of the tool.
        """
        self.owner = owner

    def work(self, mouse_click_pos):
        pass


class BlockRemover(Tool):
    def __init__(self, owner):
        Tool.__init__(self, owner)

    def work(self, mouse_click_pos):
        for dx, dy in itertools.product(range(-1, 2), repeat=2):
            self.game.map_generator.change_block(
                ((mouse_click_pos[0] - self.camera_pos[0]) // self.world_map_block_size + dx,
                 (mouse_click_pos[1] - self.camera_pos[1]) // self.world_map_block_size + dy), 0)



class Projectile(variables.Variables, pygame.sprite.Sprite):
    def __init__(self, pos, angle, lifetime, explode_size, color=(255, 255, 255)):
        """
            Class that is basically a sprite class that is used to create projectile particles. For ex. a bullet.

        :param pos: Starting position.
        :param angle: Describes the direction where the projectile particle should fly. Zero degrees is equal to East.
        :param lifetime: Time that describes how lone the projectile particle can fly.
        :param explode_size: Radius that describes the exploding range of the projectile particle when collided with something.
        :param color: Color of the projectile particle
        """
        pygame.sprite.Sprite.__init__(self, variables.Variables.spell_group)
        self.image = pygame.Surface((self.world_map_block_size // 2, self.world_map_block_size // 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = 0
        self.rect.y = 0
        self.starttick = pygame.time.get_ticks()

        self.lifetime = lifetime
        self.real_speed = 0.5
        self.explode_size = explode_size

        self.speed_x = self.real_speed * math.cos(angle)
        self.speed_y = self.real_speed * math.sin(angle)

    def update(self, camera_pos):
        """
            Update projectile particle position on the map

        :param camera_pos: Coordinates of the screen on the map.
        """
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        self.rect.x = self.pos[0] * self.world_map_block_size + camera_pos[0]
        self.rect.y = self.pos[1] * self.world_map_block_size + camera_pos[1]
        self.collision_detect()
        self.delete_on_time()

    def destroy(self):
        self.groups()[0].remove(self)

    def collision_detect(self):
        id, coords_on_map = self.game.map_generator.convert_coords(
            (round(self.pos[1] + self.speed_y), round(self.pos[0] + self.speed_x)))
        if self.game.map_generator.map_chunks[id][coords_on_map[1]][coords_on_map[0]] != 0:
            self.explode()
            # self.destroy()

    def delete_on_time(self):
        """
            Deletes the projectile particle when some time has passed.
        """
        if pygame.time.get_ticks() - self.starttick >= self.lifetime:
            self.destroy()

    # Override if needed. This just clears all blocks on the map in some radius when projectile is colliding with some block on the map.
    def explode(self):
        """
            When the projectile particle collides with the map it deletes some blocks in some radius.

        :param radius: Parameter
        """
        # radius = int((self.explode_size - 1) / 2)
        # try:
        #     if radius != 0:
        #         for dy, dx in itertools.product(range(-radius, radius), repeat=2):
        #             self.game.map_generator.change_block((round(self.pos[0] + self.speed_x + dx),
        #                                                   round(self.pos[1] + self.speed_y + dy),
        #                                                   0), 0)
        # except:
        #     pass
        print('asd')
        self.game.map_generator.change_block((int(self.pos[0] + self.speed_x),
                                              int(self.pos[1] + self.speed_y)), 0)


class SingleShotCannon(Cannon, variables.Variables):
    def __init__(self, owner):
        """
            Weapon that shots single bullet at a time.

        :param owner: The owner of this weapon.
        """
        Cannon.__init__(self, owner)

    def shoot(self, mouse_click_pos):
        """
            Creates instances of the ammo.

        :param mouse_click_pos: Mouse position on the map when clicked. Comes from the pygame event loop.
        """
        if self.amount_of_ammo > 0:
            eval(self.ammo + "({0}, {1})".format(self.owner.pos,
                                                 math.atan2(mouse_click_pos[1] - self.owner.pos_onscreen[1],
                                                            mouse_click_pos[0] - self.owner.pos_onscreen[0])))
            self.amount_of_ammo -= 1


class Shotgun(Cannon, variables.Variables):
    def __init__(self, owner):
        """
            Weapon that shots bullets in a cone.
        :param owner:
        """
        Cannon.__init__(self, owner)
        self.delay = 1000

    def shoot(self, mouse_click_pos):
        if self.amount_of_ammo > 0 and pygame.time.get_ticks() - self.starttick > self.delay:
            angle = math.atan2(mouse_click_pos[1] - self.owner.pos_onscreen[1],
                               mouse_click_pos[0] - self.owner.pos_onscreen[0])
            self.starttick = pygame.time.get_ticks()
            eval(self.ammo + "({0}, {1})".format(self.owner.pos, angle - math.pi / 15))
            eval(self.ammo + "({0}, {1})".format(self.owner.pos, angle))
            eval(self.ammo + "({0}, {1})".format(self.owner.pos, angle + math.pi / 15))

            # for i in range(0, 101):
            # eval(self.ammo + "({0}, {1})".format(self.owner.pos, i * 2 * math.pi/100))
            # self.amount_of_ammo -= 3


class SimpleBullet(Projectile):
    def __init__(self, pos, mouse_click_pos):
        Projectile.__init__(self, pos, mouse_click_pos, 100, 3, (255, 255, 255))
