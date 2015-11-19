import socket
import select
import pickle
from socket_implementation.server import map_generator
from socket_implementation.server import variables

__author__ = 'Markus Peterson'


# TODO integrate map_genetator somewhere here.

class Server(variables.Variables):
    def __init__(self, serveraddr=socket.gethostbyname(socket.gethostname()), serverport=8000, max_players=5):
        variables.Variables.__init__(self)
        self.serveraddr = (serveraddr, serverport)

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(self.serveraddr)
        print(self.listener)

        self.read_list = [self.listener]
        self.write_list = []
        self.exceptional = []

        self.players = {}
        self.particles = {}
        self.max_players = max_players

    def run(self):
        try:
            print('Running...')
            while True:
                readable, writable, exceptional = select.select(self.read_list, self.write_list, self.exceptional, 0)
                for r in readable:
                    if r is self.listener:
                        msg, addr = r.recvfrom(1024)
                        msg = pickle.loads(msg)
                        cmd = msg[0]
                        msg = msg[1]

                        print(cmd, msg)

                        if 'new connection' in cmd:
                            self.players[addr] = msg

                        elif 'request' in cmd:
                            if 'player_positions' in cmd:
                                for addr, pos in self.players.items():
                                    self.listener.sendto(pos, addr)
                            elif 'variable' in cmd:
                                if msg in self.variables:
                                    self.listener.sendto(pickle.dumps(('respond variable', (eval('self.' + msg)))),
                                                         addr)

                        elif 'update' in cmd:
                            if 'player position' in cmd:
                                self.players[addr] = msg

                                # TODO flag and command control.

        finally:
            pass


if __name__ == '__main__':
    g = Server()
    g.run()
