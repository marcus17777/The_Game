import pygame, tkinter
import vars, map_generator, game_classes

__author__ = 'Markus Peterson'


#def fps_counter(screen, ms):
    #print(' ')
    #fps_text = 'FPS: ' + str(1//(ms/1000))
    #fps_surface = std_font.render(fps_text, False, (255, 255, 255))
    #screen.blit(fps_surface, (0, 0))
#"""


class Game(vars.Variables, tkinter.Frame):
    def __init__(self, master=None):
        vars.Variables.__init__(self)
        self.World_map = map_generator.Map()
        self.camera_pos = [0, 0]
        self.mainplayer = game_classes.Player([self.world_map_width // 2, self.world_map_height // 2])
        #self.minimap = Minimap()

    def get_vars(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_index = [[(self.mouse_pos[0]-self.camera_pos[0])//self.world_map_block_size,
                             (self.mouse_pos[1]-self.camera_pos[1])//self.world_map_block_size]]

    def draw(self, screen, ms):
        self.camera_pos = [(self.screen_width//2 + self.world_map_block_size//2) - (self.mainplayer.pos[0]+1) * self.world_map_block_size,
                           (self.screen_height//2 - self.mainplayer.pos[1] * self.world_map_block_size)]

        self.World_map.create_new_chunk(self.mainplayer.pos)
        self.World_map.blit_all_maps(screen, self.camera_pos)
        self.mainplayer.update(screen, ms)

    def on_event(self, event):
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
                pygame.image.save(self.World_map.map_surfaces[(0, 0)], 'pic.jpeg')
    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.mainplayer.move('stop_y')

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.mainplayer.move('stop_x')
