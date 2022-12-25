#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import time
import socket
import rospy, cv2
from std_msgs.msg import String
 
######################tcp begining
HOST='192.168.11.26'
 
PORT=8080
 
BUFFER=4096
 
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
sock.bind((HOST,PORT))
 
sock.listen(5)
 
################ros begining
rospy.init_node('tcptalker',anonymous=0)
pub=rospy.Publisher('tcptopic',String,queue_size=10)
 
print 'i am listening'
 
while not rospy.is_shutdown():
    con,addr=sock.accept()
    try:
        con.settimeout(1000)
        buf=con.recv(BUFFER)
	if buf == b"":
	    break
	else:
	    print(buf)
            pub.publish(buf)

        '''camera setting'''

        capture = cv2.VideoCapture(0)
        #capture.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
        #capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
        if not capture:
            print("Could not open camera")
            sys.exit()
        ret, frame=capture.read()
        jpegstring = cv2.imencode('.jpg', frame)[1].tostring()
        con.send(jpegstring)


    except socket.timeout:
        print 'time out'
#    con.send('yes i recve')
#    con.send(jpegstring)
con.close()
