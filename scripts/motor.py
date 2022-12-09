#!/usr/bin/env python
#encording: utf8
import sys, rospy, math, time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from pimouse_ros.srv import TimedMotion

flag = 0

class Motor():
    #flag = 0
    def __init__(self):
        if not self.set_power(False): sys.exit(1)

        rospy.on_shutdown(self.set_power)
        self.sub_raw = rospy.Subscriber('motor_raw',MotorFreqs,self.callback_raw_freq)
	#socket
	self.sub_sct = rospy.Subscriber('tcptopic',String,self.callback_sct)
	#laser
	self.sub_laser = rospy.Subscriber('scan', LaserScan, self.callback_laser)
	#self.sub_laser2 = rospy.Subscriber('scan', LaserScan, self.callback_laser2)
        self.sub_cmd_vel=rospy.Subscriber('cmd_vel',Twist,self.callback_cmd_vel)
	self.srv_on = rospy.Service('motor_on', Trigger, self.callback_on)
	self.srv_off = rospy.Service('motor_off', Trigger, self.callback_off)
	self.srv_tm = rospy.Service('timed_motion', TimedMotion, self.callback_tm)
	self.last_time = rospy.Time.now()
	self.using_cmd_vel = False

    def set_power(self,onoff=False):
	en="/dev/rtmotoren0"
	try:
	    with open(en,'w') as f:
		f.write("1\n" if onoff else "0\n")
	    self.is_on=onoff
	    return True
	except:
	    rospy.logerr("cannot write to" + en)

	    return False

    def set_raw_freq(self,left_hz,right_hz):
	if not self.is_on:
	    rospy.logerr("not enpowered")
	    return

	try:
	    with open("/dev/rtmotor_raw_l0",'w') as lf,\
		 open("/dev/rtmotor_raw_r0",'w') as rf:
		lf.write(str(int(round(left_hz))) + "\n")
		rf.write(str(int(round(right_hz))) + "\n")
		print("set_success")
	except:
	    rospy.logerr("cannot write to rtmotor_raw_*")

    def onoff_response(self,onoff):
	d = TriggerResponse()
	d.success = self.set_power(onoff)
	d.message = "ON" if self.is_on else "OFF"
	return d

    def callback_on(self,message): return self.onoff_response(True)
    def callback_off(self,message): return self.onoff_response(False)

    def callback_raw_freq(self,message):
	self.set_raw_freq(message.left_hz,message.right_hz)

    def callback_cmd_vel(self,message):
        forward_hz = 80000.0*message.linear.x/(9*math.pi)
	rot_hz = 400.0*message.angular.z/math.pi
	self.set_raw_freq(forward_hz-rot_hz, forward_hz+rot_hz)

	self.using_cmd_vel = True
	self.alst_time = rospy.Time.now()

    def callback_sct(self,message):
		print("go")
		if (message.data == "w"): self.set_raw_freq(400,400)
		elif(message.data == "x"): self.set_raw_freq(-400,-400)
		elif(message.data == "a"): self.set_raw_freq(25,100)
		elif(message.data == "d"): self.set_raw_freq(100,25)
		elif(message.data == "s"): self.set_raw_freq(0,0)
		else: pass

    def callback_laser(self, message):
        print("receive scan_data")
        global flag
        print(flag)
        if flag == 0:
	    for i in message.ranges:
	        if((0 < i) and (i < 0.15)):
                    self.set_raw_freq(0,0)
                    flag = 1
                    break
                    #time.sleep(1)
	        else:
	            continue

        elif flag == 1:
            self.set_raw_freq(-200, -200)
            #time.sleep(0.5)
            cnt = len(message.ranges)
            print(cnt)
            for j in message.ranges:
                if((0 < j) and (j < 0.2)):
                    cnt -= 1
                    break
            print(cnt)
            if cnt == len(message.ranges):
                print("no obstacle")
                self.set_raw_freq(0,0)
                flag = 0
    #def callback_laser2(self, message)

    def callback_tm(self,message):
	if not self.is_on:
	    rospy.logerr("not enpowered")
	    return False

	dev ="/dev/rtmotor0"
	try:
	    with open(dev,'w') as f:
		f.write("%d %d %d\n" %(message.left_hz,message.right_hz,message.duration_ms))
	except:
	    rospy.logerr("cannot write to "+ dev)
	    return False

	return True

if __name__=='__main__':
    rospy.init_node('motors')
    m=Motor()

    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
	if m.using_cmd_vel and rospy.Time.now().to_sec() - m.last_time.to_sec() >= 1.0:
	    m.set_raw_freq(0,0)
            m.using_cmd_vel = False
	rate.sleep()
