import tkinter
import pygame
from original import variables


__author__ = 'Markus Peterson'


# TODO Make FPS counter to work

# """
def fps_counter(screen, font, ms):
    """
        Just a fps_counter to debug how good the game is running.
        Not working atm.

    :param screen: Surface, where fps_counter is blited to.
    :param ms: Needed for fps calculation.
    """
    fps_text = 'FPS: ' + str(1 // (ms / 1000))
    fps_surface = font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))


# """


class Game(variables.Variables, tkinter.Frame):
    def __init__(self, master=None):
        """
            The class that handles game mechanics and all other stuff.

        :param screen: Surface, where all the stuff are blited to.
        :param ms: Parameter that is needed for character movement and fps calculation.
        :param master: The parent of the current tkinter.Frame.
        """
        tkinter.Frame.__init__(master)
        self.master = master
        self.map_generator = self.module_map_generator.MapGenerator()
        self.mainplayer = self.module_game_classes.Player([self.world_map_width // 2, self.world_map_height // 2])
        # self.minimap = Minimap()

        # Create frame
        self.frame = tkinter.Frame(master=self.master)
        self.frame.pack(side='right')
        self.starttick = pygame.time.get_ticks()

        for i in range(10):
            self.module_game_classes.NPC(30, 20, pos=[self.world_map_width // 2, self.world_map_height // 2])

    def get_vars(self):
        """
            Just to get some variables needed for game mechanics in a nice way.
        """
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_index = [[(self.mouse_pos[0] - self.camera_pos[0]) // self.world_map_block_size,
                             (self.mouse_pos[1] - self.camera_pos[1]) // self.world_map_block_size]]

    def map_draw(self, screen, font, ms):
        """
            Function that draws the game onto the screen surface.

        :param screen: Surface, where all the stuff are blited to.
        :param ms: Parameter that is needed for character movement and fps calculation.
        """
        variables.Variables.camera_pos = [(self.screen_width // 2 + self.world_map_block_size // 2) - (
        self.mainplayer.real_pos[0] + 1) * self.world_map_block_size,
                                          (self.screen_height // 2 - (
                                          self.mainplayer.real_pos[1] + 1) * self.world_map_block_size)]

        self.map_generator.blit_all_maps(screen, self.camera_pos)
        self.map_generator.create_new_chunk(self.mainplayer.pos)
        fps_counter(screen, font, ms)
        self.mainplayer.update(screen, ms)
        self.spell_group.draw(screen)
        self.character_group.draw(screen)
        self.spell_group.update(ms)
        self.character_group.update(ms)

        if (pygame.time.get_ticks() - self.starttick) % 2000 == 0:
            self.module_game_classes.NPC.learn()

    def on_event(self, event, screen):
        """
            Just a function to get all events in a nice way and to react on them.

        :param event: The event that is analyzed.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.mainplayer.move('forward')

            elif event.key == pygame.K_DOWN:
                self.mainplayer.move('backward')

            elif event.key == pygame.K_LEFT:
                self.mainplayer.move('left')

            elif event.key == pygame.K_RIGHT:
                self.mainplayer.move('right')

            elif event.key == pygame.K_i:
                self.mainplayer.inventory.display(screen)

            elif event.key == pygame.K_r:
                self.mainplayer.weapon.reload()

            elif event.key == pygame.K_p:
                pygame.image.save(self.map_generator.map_chunk_surfaces[self.map_generator.current_map_idx],
                                  ('pics/pic[' + ", ".join(
                                      tuple(map(str, self.map_generator.current_map_idx)))) + '].jpeg')
            elif event.key == pygame.K_ESCAPE:
                raise variables.SceneSwitcher('menu')

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.mainplayer.move('stop_y')

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.mainplayer.move('stop_x')

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print(event)
            if event.button == 1:
                self.mainplayer.shoot(event.pos)
                # pass
            elif event.button == 3:
                self.mainplayer.tool.work(event.pos)
