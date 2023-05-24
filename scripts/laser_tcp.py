#!/usr/bin/python
# _*_ coding: utf-8 _*_

import socket, rospy, time
from std_msgs.msg import String

str = 'first'

'''sending by socket'''
def send_laser_msg(msg):
    s_time = time.time()
    HOST = '192.168.11.4'
    PORT = 50000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(msg)

    e_time = time.time()
    ex_time = e_time - s_time
    print("ex_time: {:.10f}sec".format(ex_time))

    client.close()

'''callback_function'''
def callback(msg):
    global str
    if msg.data == str:
	pass
    else:
	str = msg.data
        send_laser_msg(msg.data)

def listener():
    rospy.init_node('laser_tcp', anonymous=True)
    rospy.Subscriber('laser_msg', String, callback)
    rospy.spin()

if __name__ == '__main__':
    send_laser_msg('nothing')
    listener()
