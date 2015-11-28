import tkinter
import pygame
# from original import map_generator
from socket_implementation.client import variables
from socket_implementation.client import game_classes
from socket_implementation.client import game_map

__author__ = 'Markus Peterson'


# TODO Make FPS counter to work

# """
def fps_counter(screen, ms):
    """
        Just a fps_counter to debug how good the game is running.
        Not working atm.

    :param screen: Surface, where fps_counter is blited to.
    :param ms: Needed for fps calculation.
    """
    fps_text = 'FPS: ' + str(1 // (ms / 1000))
    fps_surface = pygame.font.Font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))


# """


class Game(variables.Variables, tkinter.Frame):
    def __init__(self, screen, ms, master=None):
        """
            The class that handles game mechanics and all other stuff.

        :param screen: Surface, where all the stuff are blited to.
        :param ms: Parameter that is needed for character movement and fps calculation.
        :param master: The parent of the current tkinter.Frame.
        """
        variables.Variables.__init__(self)
        tkinter.Frame.__init__(self)
        self.master = master
        self.World_map = game_map.World_Map()
        self.camera_pos = [0, 0]
        self.mainplayer = game_classes.Player([self.world_map_width // 2, self.world_map_height // 2])
        # self.minimap = Minimap()

        # Create frame
        self.frame = tkinter.Frame(master=self.master)
        self.frame.pack(side='right')
        self.textbox = tkinter.Text(master=self.frame, width=16, height=4)
        self.textbox.pack()

    def get_vars(self):
        """
            Just to get some variables needed for game mechanics in a nice way.
        """
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_index = [[(self.mouse_pos[0] - self.camera_pos[0]) // self.world_map_block_size,
                             (self.mouse_pos[1] - self.camera_pos[1]) // self.world_map_block_size]]

    def display_collision(self):
        """
            For displaying collision detection for debugging.
        """
        self.textbox.delete(1.0, 'end')
        for i in range(2, -1, -1):
            self.textbox.insert(1.0, self.mainplayer.around[3 * i:3 * (i + 1)])
            self.textbox.insert(1.0, "\n")

    def draw_all_other_players(self, screen, camera_pos):
        print(self.players)
        for pos in self.players.values():
            try:
                pos = list(map(int, pos))
                pygame.draw.rect(screen, (0, 100, 0), (
                    pos[0] + camera_pos[0], pos[1] + camera_pos[1], self.world_map_block_size,
                    self.world_map_block_size))
            except:
                pass


    def map_draw(self, screen, ms):
        """
            Function that draws the game onto the screen surface.

        :param screen: Surface, where all the stuff are blited to.
        :param ms: Parameter that is needed for character movement and fps calculation.
        """
        self.camera_pos = [(self.screen_width // 2 + self.world_map_block_size // 2) - (
            self.mainplayer.pos[0] + 1) * self.world_map_block_size,
                           (self.screen_height // 2 - (self.mainplayer.pos[1] + 1) * self.world_map_block_size)]

        # self.World_map.blit_all_maps(screen, self.camera_pos)
        # self.World_map.create_new_chunk(self.mainplayer.pos)
        # fps_counter(screen, ms)
        self.mainplayer.update(screen, ms, [])  # self.World_map.get_chunk(self.World_map.current_map_idx))
        self.draw_all_other_players(screen, self.camera_pos)
        self.display_collision()

    def on_event(self, event):
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

            elif event.key == pygame.K_p:
                pygame.image.save(self.World_map.map_chunks_surfaces[self.World_map.current_map_idx],
                                  ('pics/pic[' + ", ".join(tuple(map(str, self.World_map.current_map_idx)))) + '].jpeg')

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.mainplayer.move('stop_y')

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.mainplayer.move('stop_x')
