#!/usr/bin/env python
import SocketServer
import socket
import sys

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	print(self.request.recv(1024).strip().decode())
	self.request.send(("hello world").encode("utf-8"))

HOST = '192.168.143.152'
PORT = 8080
SocketServer.TCPServer.allow_reuse_address = True
server = SocketServer.TCPServer((HOST, PORT), TCPHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.shutdown()
sys.exit()
