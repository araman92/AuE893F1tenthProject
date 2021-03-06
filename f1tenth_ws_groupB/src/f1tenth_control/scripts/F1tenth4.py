#!/usr/bin/env python

'''
Author: Longxiang Guo
Latest Update: 20170413
All rights reserved
'''

import rospy
import math
import numpy as np
import time
import pid
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from keyboard.msg import Key

middle = 4
sect_increment = 30
indicis = np.arange(0,2,1)

def chunks(list,n):
    return (list[i:i+n] for i in xrange(0, len(list), n))

def closest(list, Number):
    aux = []
    for valor in list:
        aux.append(abs(Number-valor))
    if not aux:
        return middle
    else:
        return aux.index(min(aux))


class Navigate():
    def __init__(self):

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=50)
        self.depth_subscriber = rospy.Subscriber('/scan', LaserScan, self.DepthCallback, queue_size=50)
        self.teleop_subscriber = rospy.Subscriber('/keyboard/keyup', Key, self.KeyCallback, queue_size=50)
        self.depth = LaserScan()
        self.mindis = np.zeros(9)
        self.minpos = np.zeros(9)
        self.avgdis = np.zeros(9)
        self.avgwidth = np.zeros(9)
        self.absmindis = 9
        self.globalmin = 9
        self.globalmax = 0.1
        self.globalminpos = 0
        self.globalmaxpos = 0
        self.maxavgpos = 0
	self.spd = 0
        self.offset = 0
        self.sidemaxavg = 0
        self.strcontroller = pid.PID(100, 0, 70, -0.1, 0.1)
    
    def KeyCallback(self,msg):
        keyinput =  msg.code
        if keyinput == 32:
            self.spd = 0
        elif keyinput == 273:
            self.spd+= 1
        elif keyinput == 274:
            self.spd-= 1 

    def DepthCallback(self, msg):
        self.depth = msg
        self.Sort()
        self.offsetestimate()

    def Sort(self):

        n = 120
        ranges = list(self.depth.ranges)
        total = len(ranges)
        for i in range(total):
            ranges[i] = min(ranges[i], 9)
        
        self.globalmin = min(ranges)
        self.globalmax = max(ranges)
        self.globalminpos = ranges.index(self.globalmin)*self.depth.angle_increment + self.depth.angle_min
        self.globalmaxpos = ranges.index(self.globalmax)*self.depth.angle_increment + self.depth.angle_min
        chunk_range = list(chunks(ranges, n))
        for j in range(9):
            minvalue = min(chunk_range[j])
            self.mindis[j] = minvalue
            minindices = chunk_range[j].index(minvalue)

            minpos = self.depth.angle_min + (j*n + minindices + 1) * self.depth.angle_increment
            self.minpos[j] = minpos

            avgvalue = sum(chunk_range[j]) / len(chunk_range[j])
            self.avgdis[j] = avgvalue

            avgwid = avgvalue * math.sin(n*self.depth.angle_increment)
            self.avgwidth[j] = avgwid
            #rospy.loginfo("minvalue: %f, minpos: %f, avgvalue: %f, avgwid: %f", minvalue,minpos, avgvalue,avgwid )
    def offsetestimate(self):
        
        leftavgs = np.flipud(self.avgdis[6:8])
        leftangles = np.flipud(np.radians((6+indicis-middle)*sect_increment))
        rightavgs = self.avgdis[1:3]
        rightangles = np.radians((1+indicis-middle)*sect_increment)
        leftx = np.multiply(np.sin(leftangles),leftavgs)
        lefty = np.multiply(np.cos(leftangles),leftavgs)
        rightx = np.multiply(np.sin(rightangles),rightavgs)
        righty = np.multiply(np.cos(rightangles),rightavgs)
        middlex = (leftx + rightx)/2
        middley = (lefty + righty)/2
        p = np.poly1d(np.polyfit(middley,middlex,1))
        self.offset = p(0)
        self.sidmaxavg = max([max(leftavgs),max(rightavgs)])

    def IntelMove(self):
        vel_msg = Twist()
        vel_msg.linear.x = 0.
        vel_msg.linear.y = 0.
        vel_msg.linear.z = 0.
        vel_msg.angular.x = 0.
        vel_msg.angular.y = 0.
        vel_msg.angular.z = 0.
        spd = 0.
        rot = 0.
        speeddead = 0
        speedlimit = 22
        rotatelimit = 90

        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            maxavg = max(self.avgdis[2:7])
            maxavgpos = [m for m, n in enumerate(self.avgdis[2:7]) if n == maxavg]
            minavg = min(self.avgdis[1:8])
            minavgpos = np.argmin(self.avgdis[1:8])
            target = maxavgpos[closest(maxavgpos,2)] + 2
            desiredangle = math.radians((target - middle) * sect_increment)

            if self.globalmin > 0.7:
                spd = speeddead + 1* self.globalmin
            elif self.globalmin > 0.2:
                spd = speeddead + 0.5* self.globalmin
            else:
                spd = 0
                rospy.loginfo("Too Close ")

	    spd = self.spd

            if self.avgdis[middle] < 2:
                targetangle = 6*desiredangle
            elif abs(self.offset)<1 and self.sidemaxavg<6 and spd > 0:
                targetangle = 4*desiredangle + 1*math.atan(5*self.offset/spd)
            else:
                targetangle = 4*desiredangle

            avoidanglepos = self.globalminpos
            avoidanglepos = np.clip(avoidanglepos, -1.570796, 1.570796)
            avoidanglepos = np.sign(avoidanglepos)*(2-abs(avoidanglepos))
            avoidzonepos = math.radians((np.argmin(self.avgdis) - middle) * sect_increment)
            avoidzonepos = np.clip(avoidzonepos, -1.570796, 1.570796)
            avoidzonepos = np.sign(avoidzonepos)*(1.6-abs(avoidzonepos))
            avoidangle = math.atan(math.sin(avoidanglepos)/np.square(self.globalmin)) 
            avoidzone = math.atan(math.sin(avoidzonepos)/np.square(minavg)) 

            rot = self.strcontroller.update_PID(targetangle - 0.4*avoidangle - 0.15*avoidzone)

            vel_msg.linear.x = min(speedlimit, spd)
            absrot = abs(rot)
            temprot = min(absrot, rotatelimit)

            if rot > 0:
                vel_msg.angular.z = -temprot
            else:
                vel_msg.angular.z = temprot

            rospy.loginfo("target: %f , avoid: %f , spd: %f , rot: %f ", targetangle, avoidangle, vel_msg.linear.x, vel_msg.angular.z)
            self.cmd_vel.publish(vel_msg)
            rate.sleep()

        self.cmd_vel.publish(Twist())
    def shutdown(self):
        rospy.loginfo("Stop F1tenth")
        self.cmd_vel.publish(Twist())
        time.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('F1tenth', anonymous=False)
        navi = Navigate()

        while not rospy.is_shutdown():
            time.sleep(0.1)
            navi.IntelMove()


    except rospy.ROSInterruptException:
        rospy.loginfo("Node Terminated")
