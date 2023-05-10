#!/usr/bin/python
# _*_ coding: utf-8 _*_

import socket, rospy
from std_msgs.msg import String

'''sending by socket'''
def send_laser_msg(msg):
    HOST = '192.168.11.4'
    PORT = 50000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(msg)
    client.close()

'''callback_function'''
def callback(msg):
    send_laser_msg(msg.data)

def listener():
    rospy.init_node('laser_tcp', anonymous=True)
    rospy.Subscriber('laser_msg', String, callback)
    rospy.spin()

if __name__ == '__main__':
    send_laser_msg('nothing')
    listener()
