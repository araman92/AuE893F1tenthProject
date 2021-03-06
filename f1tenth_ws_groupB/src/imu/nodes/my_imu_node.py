#!/usr/bin/env python

# Copyright (c) 2012, Tang Tiong Yew
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Willow Garage, Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import rospy
import serial
import string
import math
import sys

#from time import time
from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler
from dynamic_reconfigure.server import Server
from razor_imu_9dof.cfg import imuConfig
#from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

degrees2rad = math.pi/180.0
rospy.init_node("razor_node")


#We only care about the most recent measurement, i.e. queue_size=1
pub = rospy.Publisher('imu', Imu, queue_size=1)
#srv = Server(imuConfig, reconfig_callback)  # define dynamic_reconfigure callback
#diag_pub = rospy.Publisher('diagnostics', DiagnosticArray, queue_size=1)
diag_pub_time = rospy.get_time();

imuMsg = Imu()

default_port='/dev/ttyACM0'
port = rospy.get_param('~port', default_port)

# Check your COM port and baud rate
rospy.loginfo("Opening %s...", port)
try:
    ser = serial.Serial(port=port, baudrate=115200, timeout=1)
except serial.serialutil.SerialException:
    rospy.logerr("IMU not found at port "+port + ". Did you specify the correct port in the launch file?")
    #exit
    sys.exit(0)

roll=0
pitch=0
yaw=0
seq=0

rospy.loginfo("Giving the razor IMU board 5 seconds to boot...")
rospy.sleep(5) # Sleep for 5 seconds to wait for the board to boot


while not rospy.is_shutdown():
    line = ser.readline()
    line = line.replace("#YPRAG=","")   # Delete "#YPRAG="
    #f.write(line)                     # Write to the output log file
    words = string.split(line,",")    # Fields split
    if len(words) > 2:
        #in AHRS firmware z axis points down, in ROS z axis points up (see REP 103)
        yaw_deg = -float(words[0])
        yaw_deg = yaw_deg
        if yaw_deg > 180.0:
            yaw_deg = yaw_deg - 360.0
        if yaw_deg < -180.0:
            yaw_deg = yaw_deg + 360.0
        yaw = yaw_deg*degrees2rad
        #in AHRS firmware y axis points right, in ROS y axis points left (see REP 103)
        pitch = -float(words[1])*degrees2rad
        roll = float(words[2])*degrees2rad

        # Publish message
        # AHRS firmware accelerations are negated
        # This means y and z are correct for ROS, but x needs reversing
        imuMsg.linear_acceleration.x = -float(words[1])
        imuMsg.linear_acceleration.y = float(words[2]) 
        imuMsg.linear_acceleration.z = float(words[3]) 
	#imuMsg.gyro.x = -float(words[5])
	#imuMsg.gyro.y = float(words[6])
	#imuMsg.gyro.z = float(words[7])
	#imuMsg.magnetometer.x = -float(words[8])
	#imuMsg.magnetometer.y = float(words[9])
	#imuMsg.magnetometer.z = float(words[10])

        #imuMsg.angular_velocity.x = float(words[6])
        #in AHRS firmware y axis points right, in ROS y axis points left (see REP 103)
        #imuMsg.angular_velocity.y = -float(words[7])
        #in AHRS firmware z axis points down, in ROS z axis points up (see REP 103) 
        #imuMsg.angular_velocity.z = -float(words[8])

    imuMsg.header.stamp= rospy.Time.now()
    imuMsg.header.frame_id = 'base_imu_link'
    imuMsg.header.seq = seq
    seq = seq + 1
    pub.publish(imuMsg)

        
ser.close
#f.close
