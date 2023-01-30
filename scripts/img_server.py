#!/usr/bin/env python
import SocketServer
import socket
import cv2, rospy, time
import numpy
import sys
from std_msgs.msg import String



class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        data = self.request[0].strip()
        socket = self.request[1]
        print "{}wrote:".format(self.client_address[0])
        print data

        if data == 'F':
            ret, img=capture.read()
            jpg_str = cv2.imencode('.jpeg', img)
        if data == 'B':
            ret_2, img_2=capture_2.read()
            jpg_str = cv2.imencode('.jpeg', img_2)

        for i in numpy.array_split(jpg_str[1], 10):

            socket.sendto(i.tostring(), self.client_address)

        socket.sendto('__end__', self.client_address)


'''ROS setting'''
rospy.init_node('img_server')


'''HOST and PORT setting'''

HOST = '192.168.11.26'
PORT = 9999

'''camera setting'''

capture = cv2.VideoCapture(2)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
capture.set(cv2.CAP_PROP_FPS, 10)
if not capture:
    print("Could not open camera")
    sys.exit()

capture_2 = cv2.VideoCapture(0)
capture_2.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture_2.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
capture_2.set(cv2.CAP_PROP_FPS, 10)
if not capture:
    print("Could not open camera")
    sys.exit()

SocketServer.UDPServer.allow_reuse_address = True
server = SocketServer.UDPServer((HOST, PORT), TCPHandler)
server.capture = capture

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("finish")
    raise
server.shutdown()
sys.exit()





