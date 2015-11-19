__author__ = 'Markus Peterson'

import socket_implementation
import select
import datetime
import os


class Server:
    def __init__(self, address=socket_implementation.gethostbyname(socket_implementation.gethostname()), port=8000,
                 max_chatters=5):
        self.listener = socket_implementation.socket(socket_implementation.AF_INET, socket_implementation.SOCK_DGRAM)
        self.listener.bind((address, port))
        print(self.listener)
        self.read_list = [self.listener]
        self.write_list = []

        self.chatters = {}
        self.max_chatters = max_chatters
        os.makedirs('logs/', exist_ok=True)
        self.logfile = open('logs/' + datetime.datetime.now().strftime('(%Y.%m.%d %H-%M-%S)') + '.txt', mode='w')

    def send(self, message):
        for chatter in self.chatters:
            self.listener.sendto(message.encode('utf-8'), chatter)

    def run(self):
        print('Waiting...')
        try:
            while True:
                readable, writable, exceptional = (select.select(self.read_list, self.write_list, []))
                for f in readable:
                    if f is self.listener:
                        msg, addr = f.recvfrom(1024)
                        cmd = msg.decode('utf-8')[0]
                        msg = msg.decode('utf-8')[1:]
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        time = timestamp.split(' ')[1]
                        cmd_info = timestamp + ' ' + repr(addr) + ' ' + '(' + cmd + ')' + ' ' + msg
                        print(cmd_info)
                        self.logfile.write(cmd_info + '\n')
                        self.logfile.flush()
                        if cmd == 'c':
                            if len(self.chatters) < self.max_chatters:
                                self.chatters[addr] = msg
                                self.send((time + '\t' + self.chatters[addr] + " connected."))
                            else:
                                self.listener.sendto((time + '\t' + "Jututuba on juba täis.").encode('utf-8'), addr)
                        elif cmd == 'p':
                            if addr in self.chatters.keys():
                                self.send((time + '\t' + msg))
                        elif cmd == 'd':
                            if addr in self.chatters:
                                self.send((time + '\t' + self.chatters[addr] + " disconnected."))
                                del self.chatters[addr]
                        else:
                            print('Unexpected command: %s' % cmd)
        except KeyboardInterrupt as e:
            self.logfile.close()
            pass


if __name__ == '__main__':
    g = Server()
    g.run()
