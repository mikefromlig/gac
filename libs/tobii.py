#!/usr/bin/python
# Michael ORTEGA - Vancouver - SFU Surrey - 08/26/15

import socket


class tobii:

    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = None
        self.init()
        self.data = None

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.UDP_IP, self.UDP_PORT))

    def recv_data(self):
        self.sock.send(b'last_position')
        try:
            res = self.sock.recv(1024)
            self.data = str(res)[2:-1]
            return self.data
        except:
            return None
