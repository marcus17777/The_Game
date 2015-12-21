import pygame
import math
import itertools
import operator
import copy
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
    def __init__(self, owner, radius, break_radius):
        self.radius = radius
        self.break_radius = break_radius
        Tool.__init__(self, owner)

    def work(self, mouse_click_pos):
        if ((mouse_click_pos[0] - self.owner.pos_onscreen[0]) ** 2 + (
            mouse_click_pos[1] - self.owner.pos_onscreen[1]) ** 2) <= (self.radius * self.world_map_block_size) ** 2:
            for dx, dy in itertools.product(range(-self.break_radius, self.break_radius + 1), repeat=2):
                self.game.map_generator.change_block(
                    ((mouse_click_pos[0] - int(self.camera_pos[0])) // self.world_map_block_size + dx,
                     (mouse_click_pos[1] - int(self.camera_pos[1])) // self.world_map_block_size + dy), 0)


class Projectile(variables.Variables, pygame.sprite.Sprite):
    def __init__(self, parent_weapon, angle, lifetime, explode_size, color=(255, 255, 255)):
        """
            Class that is basically a sprite class that is used to create projectile particles. For ex. a bullet.

        :param pos: Starting position.
        :param angle: Describes the direction where the projectile particle should fly. Zero degrees is equal to East.
        :param lifetime: Time that describes how lone the projectile particle can fly.
        :param explode_size: Radius that describes the exploding range of the projectile particle when collided with something.
        :param color: Color of the projectile particle
        """
        self.parent_weapon = parent_weapon
        pygame.sprite.Sprite.__init__(self, variables.Variables.spell_group)
        self.image = pygame.Surface((self.world_map_block_size // 2, self.world_map_block_size // 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = self.parent_weapon.owner.pos[:]
        self.rect.x = 0
        self.rect.y = 0
        self.starttick = pygame.time.get_ticks()

        self.lifetime = lifetime
        self.real_speed = 0.04
        self.explode_size = explode_size

        self.speed_x = self.real_speed * math.cos(angle)
        self.speed_y = self.real_speed * math.sin(angle)

    def update(self, ms):
        """
            Update projectile particle position on the map

        :param camera_pos: Coordinates of the screen on the map.
        """
        self.pos[0] += self.speed_x * ms
        self.pos[1] += self.speed_y * ms
        self.rect.x = self.pos[0] * self.world_map_block_size + self.camera_pos[0]
        self.rect.y = self.pos[1] * self.world_map_block_size + self.camera_pos[1]
        self.collision_detect()
        self.delete_on_time()

    def destroy(self):
        self.groups()[0].remove(self)

    def collision_detect(self):
        # id, coords_on_map = self.game.map_generator.convert_coords(
        #     (round(self.pos[1] + self.speed_y), round(self.pos[0] + self.speed_x)))
        # if self.game.map_generator.map_chunks[id][coords_on_map[1]][coords_on_map[0]] != 0:
        #     self.explode()
        #     self.destroy()
        a = pygame.sprite.spritecollideany(self, self.character_group)
        if a != None:
            a.hurt_score += 1
            self.parent_weapon.owner.hit_score += 1
            if isinstance(self.parent_weapon.owner, self.module_game_classes.Player):
                for i in a.groups():
                    i.remove(a)
                self.destroy()

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
        self.shot_delay = 500

    def shoot(self, angle):
        """
            Creates instances of the ammo.

        :param mouse_click_pos: Mouse position on the map when clicked. Comes from the pygame event loop.
        """
        if (
                self.amount_of_ammo > 0 or self.amount_of_ammo == -1) and pygame.time.get_ticks() - self.starttick > self.shot_delay:
            eval(self.ammo + "(self, {0})".format(angle))
            self.starttick = pygame.time.get_ticks()
            if self.amount_of_ammo != -1: self.amount_of_ammo -= 1

    def draw(self, screen):
        pass

    def update(self, screen):
        pass


class Shotgun(Cannon, variables.Variables):
    def __init__(self, owner):
        """
            Weapon that shots bullets in a cone.
        :param owner:
        """
        Cannon.__init__(self, owner)
        self.cartridge_image = pygame.transform.scale(pygame.image.load('pics/shotgun_alpha.jpg'), (20, 10))
        self.image_rect = self.cartridge_image.get_rect()

        self.shot_delay = 500
        self.reload_delay = 600
        self.max_magazine = 7
        self.current_magazine = self.max_magazine

        self.reloading = False
        self.reloading_starttick = 0
        self.reloading_time_per_bullet = 30

    def draw(self, screen):
        for i in range(self.current_magazine):
            screen.blit(self.cartridge_image, (self.screen_width - (self.max_magazine - i) * (self.image_rect[2] + 20),
                                               self.screen_height - 20))

    def shoot(self, angle):
        self.reloading = False
        if self.current_magazine > 0 and pygame.time.get_ticks() - self.starttick > self.shot_delay:
            self.starttick = pygame.time.get_ticks()
            eval(self.ammo + "(self, {0})".format(angle - math.pi / 15))
            eval(self.ammo + "(self, {0})".format(angle))
            eval(self.ammo + "(self, {0})".format(angle + math.pi / 15))
            self.current_magazine -= 1

            # for i in range(0, 101):
            # eval(self.ammo + "({0}, {1})".format(self.owner.pos, i * 2 * math.pi/100))
            self.amount_of_ammo -= 3

    def update(self, ms):
        if self.reloading and self.current_magazine < self.max_magazine and (
                    pygame.time.get_ticks() - self.reloading_starttick) * ms % self.reloading_time_per_bullet == 0:
            self.current_magazine += 1
        elif self.current_magazine >= self.max_magazine:
            self.reloading = False

    def reload(self):
        self.reloading_starttick = pygame.time.get_ticks()
        self.reloading = True


class SimpleBullet(Projectile):
    def __init__(self, parent, angle):
        Projectile.__init__(self, parent, angle, 700, 3, (255, 255, 255))


class SpectatorGun(variables.Variables):
    def __init__(self, owner):
        self.owner = owner
        self.next_index = 0

    def shoot(self, pos):
        try:
            self.owner.pos = list(self.character_group)[self.next_index].pos

            self.next_index = (self.next_index + 1) % (len(list(self.character_group)) - 1)
        except Exception as e:
            print(e)
            pass
