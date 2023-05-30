#!/usr/bin/python
# _*_ coding: utf-8 _*_

import socket, rospy, time
from std_msgs.msg import String
from pimouse_ros.msg import StringArray

str = ['first', 'first', 'first', 'first']

'''sending by socket'''
def send_laser_msg(msg):
    #print(msg)
    #print(msg.data)
    #print(iter(msg.data))
    data = '|'.join(msg.data).encode()

    
    HOST = '192.168.11.4'
    PORT = 50000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(data)


    client.close()

'''callback_function'''
def callback(msg):
    #rospy.loginfo('Received: %s', msg.data)

    global str
    for i in range(4):
        if msg.data[i] != str[i]:
    	    str = msg.data
	    send_laser_msg(msg)
	    break
        else:
	    continue

def listener():
    rospy.init_node('laser_tcp', anonymous=True)
    rospy.Subscriber('laser_msg', StringArray, callback)
    rospy.spin()

if __name__ == '__main__':
    #send_laser_msg(str)
    listener()
