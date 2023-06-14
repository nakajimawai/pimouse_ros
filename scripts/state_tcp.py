#!/usr/bin/python
# _*_ coding: utf-8 _*_

import socket, rospy, struct
from std_msgs.msg import Bool

'''sending by socket'''
def send_state(msg):
    data = struct.pack('?', msg)
    HOST = '192.168.11.4'
    PORT = 50010
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(data)
    client.close()

'''callback_function'''
def callback_state(msg):
    print(msg)
    send_state(msg.data)

def listener():
    rospy.init_node('state_tcp', anonymous=True)
    rospy.Subscriber('state_msg', Bool, callback_state)
    rospy.spin()

if __name__ == '__main__':
    listener()
