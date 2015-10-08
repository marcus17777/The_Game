import sys, os, pygame, tkinter
import vars, in_game

__author__ = 'Markus Peterson'



class Main(vars.Variables):
    def __init__(self):
        # setting things up
        # tkinter frame
        self.root = tkinter.Tk()
        self.PygameFrame = tkinter.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.PygameFrame.pack(side='left')
        os.environ['SDL_WINDOWID'] = str(self.PygameFrame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.init()
        pygame.display.set_caption('The Game')
        self.PygameFrame.focus_set()
        self.screen.fill((80, 80, 80))
        self.clock = pygame.time.Clock()
        self.ms = self.clock.tick(50)

        #The Game
        self.game = in_game.Game(master=self.root)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #self.root.destroy()
                    sys.exit()
                else:
                    self.game.get_vars()
                    self.game.on_event(event)

            self.ms = self.clock.tick(200)
            self.screen.fill((80, 80, 80))
            self.game.draw(self.screen, self.ms)
            pygame.display.flip()
            self.root.update()


game = Main()
game.run()