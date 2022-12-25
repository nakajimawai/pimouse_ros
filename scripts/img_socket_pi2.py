#!/usr/bin/env python
import SocketServer
import socket
import cv2, rospy
import numpy
import sys
from std_msgs.msg import String

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	self.data = self.request.recv(1024).strip()

	rospy.init_node('tcptalker',anonymous=0)
	pub=rospy.Publisher('tcptopic',String,queue_size=10)
	pub.publish(self.data)

	ret, frame=capture.read()
	jpegstring = cv2.imencode('.jpg', frame)[1].tostring()
	self.request.send(jpegstring)

'''HOST and PORT setting'''

HOST = '192.168.11.26'
PORT = 8080

'''camera setting'''

capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
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
