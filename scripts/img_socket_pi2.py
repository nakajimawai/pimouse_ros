#!/usr/bin/env python
import SocketServer
import socket
import cv2, rospy, pickle, io
import numpy
import sys
from std_msgs.msg import String

class TCPHandler(SocketServer.BaseRequestHandler):
    
    rospy.init_node('tcp_imager',anonymous=0)
    pub=rospy.Publisher('imgtopic',String,queue_size=10)

    def handle(self):
        
	self.time_sta = rospy.Time.now()
	
	self.data = self.request.recv(1024).strip()
	#pub.publish(self.data)

	#self.time_sta = rospy.Time.now()
	ret, frame=capture.read()
	jpegstring = cv2.imencode('.jpg', frame)[1].tostring()


	self.request.send(jpegstring)

	self.time_end = rospy.Time.now()
	self.tim = self.time_end.to_sec() - self.time_sta.to_sec()
	print(self.tim)
        '''
        data = self.request[0].strip()
        socket = self.request[1]
        print "{}wrote:".format(self.client_address[0])
        print data
        ret, frame=capture.read()        
	#jpegstring = cv2.imencode('.jpg', frame)[1].tostring()
	#frame_io = io.BytesIO()
	#frame.save(frame_io ,format="JPEG")
        jpegstring = pickle.dumps(frame)
	socket.sendto(jpegstring, self.client_address)
	'''
	
'''HOST and PORT setting'''

HOST = '192.168.143.152'
PORT = 8081

'''camera setting'''

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,320)
capture.set(cv2.CAP_PROP_FPS, 10)
if not capture:
    print("Could not open camera")
    sys.exit()


SocketServer.TCPServer.allow_reuse_address = True
server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
server.capture = capture

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("finish")
    raise
server.shutdown()
sys.exit()
