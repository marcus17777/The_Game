__author__ = 'Markus Peterson'

import socket_implementation, select, tkinter, random


class Client(tkinter.Frame):
    def __init__(self, serverip, serverport, ip, master=None):
        tkinter.Frame.__init__(self)
        self.master = master
        self.name = 'Markus'
        self.clientport = random.randrange(8000, 8999)
        self.connection = socket_implementation.socket(socket_implementation.AF_INET, socket_implementation.SOCK_DGRAM)
        self.connection.bind((ip, self.clientport))

        self.serverip = serverip
        self.serverport = serverport

        self.read_list = [self.connection]
        self.write_list = []

        self.message = tkinter.StringVar()

        self.setup_tkinter()

    def send_message(self, message):
        if message is not '':
            self.connection.sendto(('p' + self.name + ':  ' + message).encode('utf-8'),
                                   (self.serverip, self.serverport))
            self.message.set('')

    def setup_tkinter(self, width=400, height=400):
        self.Chatbox = tkinter.Text(master=self.master, width=100, height=20)
        self.Sendbox = tkinter.Entry(master=self.master, textvariable=self.message, width=100)
        self.Sendbutton = tkinter.Button(master=self.master, text='Send',
                                         command=lambda: self.send_message(self.message.get()))
        self.Sendbox.bind('<Return>', lambda event: self.send_message(self.message.get()))
        self.Sendbox.focus_set()
        self.Chatbox.pack(side='top')
        self.Sendbox.pack(side='top')
        self.Sendbutton.pack(side='top')

    def run(self):
        try:
            self.connection.sendto(('c' + self.name).encode('utf-8'), (self.serverip, self.serverport))
            while True:
                readable, writable, exceptional = (select.select(self.read_list, self.write_list, [], 0))
                for f in readable:
                    if f is self.connection:
                        msg, ip = f.recvfrom(1024)
                        print(ip, msg)
                        for message in msg.decode('utf-8').split('|'):
                            try:
                                self.Chatbox.insert('end', message + '\n')
                            except:
                                pass
                self.master.update()
        finally:
            self.connection.sendto(('d' + self.name).encode('utf-8'), (self.serverip, self.serverport))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('ChatClient')
    app = Client('83.187.137.206', 8000, master=root, ip='83.187.137.206')
    app.run()
