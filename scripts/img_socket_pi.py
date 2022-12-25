#!/usr/bin/env python
import SocketServer
import socket
import cv2
import numpy
import sys

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	self.data = self.request.recv(1024).strip()
	ret, frame=capture.read()
	jpegstring = cv2.imencode('.jpg', frame)[1].tostring()
	self.request.send(jpegstring)

'''HOST and PORT setting'''

HOST = '192.168.143.152'
PORT = 8080

'''camera setting'''

capture = cv2.VideoCapture(0)
#capture.set(3,320)
#capture.set(4,240)
if not capture:
    print("Could not open camera")
    sys.exit()


SocketServer.TCPServer.allow_reuse_address = True
server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
server.capture = capture

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.shutdown()
sys.exit()
