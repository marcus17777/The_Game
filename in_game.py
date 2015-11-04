import pygame, tkinter, multiprocessing
import vars, map_generator, game_classes


__author__ = 'Markus Peterson'


# TODO Make FPS counter to work

# """
def fps_counter(screen, ms):
    #print(' ')
    fps_text = 'FPS: ' + str(1 // (ms / 1000))
    fps_surface = pygame.font.Font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))
#"""


class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        """
            Worker that takes tasks and executes them in another process and returns value.

        :param task_queue: Queue where all the tasks that have to be executed are stored here.
        :param result_queue: Queue where all the returns of tasks are stored
        """
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        """
            Just a override (sort of) of default multiprocess.Process run method.
            Executes tasks.
        """
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)

class Game(vars.Variables, tkinter.Frame):
    def __init__(self, screen, ms, master=None):
        vars.Variables.__init__(self)
        self.master = master
        self.World_map = map_generator.Map()
        self.camera_pos = [0, 0]
        self.mainplayer = game_classes.Player([self.world_map_width // 2, self.world_map_height // 2])
        #self.minimap = Minimap()

        # Create frame
        self.frame = tkinter.Frame(master=self.master)
        self.frame.pack(side='right')
        self.textbox = tkinter.Text(master=self.frame, width=16, height=4)
        self.textbox.pack()

    def get_vars(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_index = [[(self.mouse_pos[0]-self.camera_pos[0])//self.world_map_block_size,
                             (self.mouse_pos[1]-self.camera_pos[1])//self.world_map_block_size]]

    def display_collision(self):
        self.textbox.delete(1.0, 'end')
        for i in range(2, -1, -1):
            self.textbox.insert(1.0, self.mainplayer.around[3 * i:3 * (i + 1)])
            self.textbox.insert(1.0, "\n")

    def map_draw(self, screen, ms):
        self.camera_pos = [(self.screen_width//2 + self.world_map_block_size//2) - (self.mainplayer.pos[0]+1) * self.world_map_block_size,
                           (self.screen_height // 2 - (self.mainplayer.pos[1] + 1) * self.world_map_block_size)]

        self.World_map.blit_all_maps(screen, self.camera_pos)
        self.World_map.create_new_chunk(self.mainplayer.pos)
        # fps_counter(screen, ms)
        self.mainplayer.update(screen, ms, self.World_map.map_chunks[self.World_map.current_map_idx])
        self.display_collision()

    def map_generation(self):
        while True:
            self.World_map.create_new_chunk(self.mainplayer.pos)

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
                pygame.image.save(self.World_map.map_chunk_surfaces[self.World_map.current_map_idx],
                                  ('pics/pic[' + ", ".join(tuple(map(str, self.World_map.current_map_idx)))) + '].jpeg')
    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.mainplayer.move('stop_y')

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.mainplayer.move('stop_x')
