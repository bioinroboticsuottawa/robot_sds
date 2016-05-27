#!/usr/bin/env bash
# 
# Author: Ray Shen
# Date Created: 08/03/2016
# 
# test shell scripts for publishing ROS topics
# requires roscore and rosserial running
# rosserial subscribes to topics that the embedded ROS node of robot hand subscribes to
# and relay the messages upon reception to the embedded ROS node
# 

# measured servo angles for the robot hand
# 	servo_1; // 65-145
# 	servo_2; // 50-90
# 	servo_3; // 40-90
# 	servo_4; // 45-75
# 	servo_5; // 85-100

# case $1 in
# 	0)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 65
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 50
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 40
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 45
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 85
# 		echo 'option_0';;
# 	1)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 65
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 40
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 45
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 85
# 		echo 'option_1';;
# 	2)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 65
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 45
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 85
# 		echo 'option_2';;
# 	3)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 65
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 75
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 85
# 		echo 'option_3';;
# 	4)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 65
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 75
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 100
# 		echo 'option_4';;
# 	5)
# 		rostopic pub -1 servo_1 std_msgs/UInt16 -- 145
# 		rostopic pub -1 servo_2 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_3 std_msgs/UInt16 -- 90
# 		rostopic pub -1 servo_4 std_msgs/UInt16 -- 75
# 		rostopic pub -1 servo_5 std_msgs/UInt16 -- 100
# 		echo 'option_5';;
# 	*)
# 		echo 'invalid_option';;
# esac

case $1 in
	0)
		sh ./fingers/finger_1.sh 65 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 50 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 40 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 45 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 85 & PID_5=$!
		sleep 0.5
		echo 'option_0';;
	1)
		sh ./fingers/finger_1.sh 65 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 90 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 40 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 45 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 85 & PID_5=$!
		sleep 0.5
		echo 'option_1';;
	2)
		sh ./fingers/finger_1.sh 65 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 90 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 90 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 45 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 85 & PID_5=$!
		sleep 0.5
		echo 'option_2';;
	3)
		sh ./fingers/finger_1.sh 65 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 90 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 90 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 75 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 85 & PID_5=$!
		sleep 0.5
		echo 'option_3';;
	4)
		sh ./fingers/finger_1.sh 65 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 90 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 90 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 75 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 100 & PID_5=$!
		sleep 0.5
		echo 'option_4';;
	5)
		sh ./fingers/finger_1.sh 145 & PID_1=$!
		sleep 0.5
		sh ./fingers/finger_2.sh 90 & PID_2=$!
		sleep 0.5
		sh ./fingers/finger_3.sh 90 & PID_3=$!
		sleep 0.5
		sh ./fingers/finger_4.sh 75 & PID_4=$!
		sleep 0.5
		sh ./fingers/finger_5.sh 100 & PID_5=$!
		sleep 0.5
		echo 'option_5';;
	*)
		echo 'invalid_option';;
esac

wait $PID_1
wait $PID_2
wait $PID_3
wait $PID_4
wait $PID_5

