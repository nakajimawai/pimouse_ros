#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import time
import socket
import rospy
from std_msgs.msg import String
 
######################tcp begining
HOST='192.168.143.152'
 
PORT=8008
 
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
            time.sleep(1)
    except socket.timeout:
        print 'time out'
    con.send('yes i recve')
 
con.close()
