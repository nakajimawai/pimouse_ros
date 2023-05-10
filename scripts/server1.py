#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import time
import socket
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger
 
######################tcp begining
HOST='192.168.11.26'
 
PORT=8080
 
BUFFER=4096
 
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
sock.bind((HOST,PORT))
 
sock.listen(5)
 
################ros begining
rospy.init_node('tcptalker',anonymous=0)
pub_tcp=rospy.Publisher('tcptopic',String,queue_size=10)
pub_cmd_vel=rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rospy.wait_for_service('/motor_on')
rospy.wait_for_service('/motor_off')

print 'i am listening'
 
while not rospy.is_shutdown():
    vel = Twist()
    con,addr=sock.accept()
    try:
        con.settimeout(1000)
        buf=con.recv(BUFFER)
	if buf == b"":
	    break
	elif buf == b"run":
	    service_proxy = rospy.ServiceProxy('/motor_on', Trigger)
	    service_proxy()
	elif buf == b"fin":
            service_proxy = rospy.ServiceProxy('/motor_off', Trigger)
            service_proxy()
	else:
	    print(buf)
            if buf == b"w":
		vel.linear.x = 0.035
	    elif buf == b"x":
		vel.linear.x = -0.035
            elif buf == b"a":
                vel.angular.z = 3.14/18
            elif buf == b"d":
                vel.angular.z = -3.14/18
            elif buf == b"s":
                vel.linear.x = 0
		vel.angular.z = 0

	pub_cmd_vel.publish(vel)
	pub_tcp.publish(buf)
    except socket.timeout:
        print 'time out'
    con.send('yes i recve')
 
con.close()
