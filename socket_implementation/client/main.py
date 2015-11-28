import os
import sys
import tkinter
import pygame
import socket
import select
import pickle
import random
from socket_implementation.client import in_game
from socket_implementation.client import variables

__author__ = 'Markus Peterson'


# TODO Make some menu somewhere in Tk


class ExitGame(Exception):
    pass


class Main(variables.Variables):
    def __init__(self, serveraddr, serverport, clientaddr=socket.gethostbyname(socket.gethostname()),
                 clientport=random.randrange(8000, 8999)):
        """
            Main class that hooks everything up and runs the game.
        """
        # setting things up
        variables.Variables.__init__(self)

        # Socket client
        variables.Variables.serveraddr = (serveraddr, serverport)
        variables.Variables.clientaddr = (clientaddr, clientport)

        variables.Variables.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # variables.Variables.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        variables.Variables.client.bind(self.clientaddr)
        variables.Variables.client.connect(self.serveraddr)
        print(self.client)

        self.read_list = [self.client]
        self.write_list = []
        self.exceptional = []

        # Get variables from the server
        self.get_variables()

        # tkinter frame
        self.root = tkinter.Tk()
        self.PygameFrame = tkinter.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.PygameFrame.pack(side='left')
        os.environ['SDL_WINDOWID'] = str(self.PygameFrame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('The Game')
        self.PygameFrame.focus_set()
        self.screen.fill((80, 80, 80))
        self.clock = pygame.time.Clock()
        self.ms = self.clock.tick(50)

        # The Game
        self.game = in_game.Game(self.screen, self.ms, master=self.root)

    def get_variables(self):
        self.client.send(pickle.dumps(('new connection')))
        for var in self.variables:
            self.client.send(pickle.dumps(('request variable', var)))
            msg, addr = self.client.recvfrom(self.client_recvlimit)
            msg = pickle.loads(msg)
            cmd = msg[0]
            msg = msg[1]
            if 'respond variable' in cmd:
                exec('variables.Variables.' + var + ' = ' + repr(msg))

    def run(self):
        """
            The main game loop. Has event calling inside and draws
            everything onto screen using the map_draw function
            from in_game.py.

            Also updates pygame.display and root tkinter.Frame.
        """
        try:
            while True:
                # Socket client
                readable, writable, exceptional = select.select(self.read_list, self.write_list, self.exceptional, 0)
                for f in readable:
                    if f is self.client:
                        try:
                            msg, addr = f.recvfrom(self.client_recvlimit)
                            msg = pickle.loads(msg)
                            cmd = msg[0]
                            msg = msg[1]
                            # print(cmd, msg)
                        finally:
                            pass

                        if 'update' in cmd:
                            if 'player position' in cmd:
                                variables.Variables.players[addr] = msg

                # Game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise ExitGame
                    else:
                        self.game.get_vars()
                        self.game.on_event(event)

                self.ms = self.clock.tick(200)
                self.screen.fill((80, 80, 80))
                self.game.map_draw(self.screen, self.ms)
                pygame.display.flip()
                self.root.update()
        except ExitGame:
            print("Game has quit normally.")
        finally:
            self.client.send(pickle.dumps(('disconnect', '')))
            pygame.quit()
            self.root.destroy()
            sys.exit()

if __name__ == '__main__':
    game = Main(serveraddr='192.168.1.176', serverport=8000, clientaddr='192.168.1.176')
    game.run()
