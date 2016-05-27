#!/usr/bin/env bash
# 
# Author: Ray Shen
# Date Created: 08/03/2016
# 
# a temporal script as a work-around to prevent rostopic pub latching
# 

/opt/ros/indigo/bin/rostopic pub -1 servo_5 std_msgs/UInt16 -- $1
