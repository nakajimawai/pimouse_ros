#!/usr/bin/python
# _*_ coding: utf-8 _*_

import socket, rospy, time, struct
from std_msgs.msg import String
from pimouse_ros.msg import StringArray

str = [True for _ in range(16)]

'''sending by socket'''
def send_laser_msg(msg):
    #data = '|'.join(msg.data).encode()
    #print(msg)
    s_time = time.time()

    data = struct.pack('b'*len(msg), *(msg))
    HOST = '192.168.11.4'
    PORT = 50000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print(msg)

    client.sendall(data)

    e_time = time.time()
    ex_time = e_time - s_time
    print("ex_time: {:.10f}sec".format(ex_time))

    client.close()

'''callback_function'''
def callback(msg):
    #rospy.loginfo('Received: %s', msg.data)

    global str
    for i in range(4):
        if msg.data[i] != str[i]:
    	    str = msg.data
	    sub_array = msg.data[0:4]   #Extract only obstacle information
	    send_laser_msg(sub_array)
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
