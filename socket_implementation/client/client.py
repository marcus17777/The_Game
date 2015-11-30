import socket
import select
import pickle
import random
from socket_implementation.client import variables

__author__ = 'Markus Peterson'


# TODO create client application for the server.


class ExitGame(Exception):
    pass


class Client(variables.Variables):
    def __init__(self, serveraddr, serverport, clientaddr=socket.gethostbyname(socket.gethostname()),
                 clientport=random.randrange(8000, 8999)):
        variables.Variables.__init__(self)
        self.serveraddr = (serveraddr, serverport)
        self.clientaddr = (clientaddr, clientport)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(self.clientaddr)
        self.client.connect(self.serveraddr)
        print(self.client)

        self.read_list = [self.client]
        self.write_list = []
        self.exceptional = []

    def run(self):
        try:
            self.client.send(pickle.dumps(('new connection', 'asd')))
            for var in self.variables:
                self.client.send(pickle.dumps(('request variable', var)))
                msg, addr = self.client.recvfrom(1024)
                msg = pickle.loads(msg)
                cmd = msg[0]
                msg = msg[1]
                if 'respond variable' in cmd:
                    exec('self.' + var + ' = ' + repr(msg))

            while True:
                readable, writable, exceptional = select.select(self.read_list, self.write_list, self.exceptional, 0)
                for f in readable:
                    if f is self.client:
                        try:
                            msg, addr = f.recvfrom(1024)
                            msg = pickle.loads(msg)
                            cmd = msg[0]
                            msg = msg[1]
                        except:
                            pass

                        if 'update' in cmd:
                            if 'map_chunk' in cmd:
                                # Change map
                                self


        except ExitGame:
            print("Game has quit normally.")


if __name__ == '__main__':
    g = Client('172.17.175.170', 8000)
    g.run()
