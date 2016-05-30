#!/usr/bin/env bash
# 
# Author: Ray Shen
# Date Created: 27/05/2016
# 
# sending ROS messages to the robot and execute actions
# 

MASTER=pumpkinpi
source /home/rayshen/Dev/pumpkin_ws/devel/setup.bash
export ROS_MASTER_URI=http://$MASTER:11311

case $1 in
	rectangle)
		rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- "{header: auto, goal: [['/home/ubuntu/workspace/pumpkin_ws/src/pumpkin/playback/straight_hand/rectangle.yaml']]}"
		sleep 0.5
		echo 'rectangle';;
	circle)
		rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- "{header: auto, goal: [['/home/ubuntu/workspace/pumpkin_ws/src/pumpkin/playback/straight_hand/circle.yaml']]}"
		echo 'circle';;
	triangle)
		rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- "{header: auto, goal: [['/home/ubuntu/workspace/pumpkin_ws/src/pumpkin/playback/straight_hand/triangle.yaml']]}"
		sleep 0.5
		echo 'triangle';;
	wave)
		rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- "{header: auto, goal: [['/home/ubuntu/workspace/pumpkin_ws/src/pumpkin/playback/straight_hand/bye.yaml']]}"
		sleep 0.5
		echo 'wave';;
	rotate)
		rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- "{header: auto, goal: [['/home/ubuntu/workspace/pumpkin_ws/src/pumpkin/playback/straight_hand/rotate.yaml']]}"
		sleep 0.5
		echo 'rotate';;
	*)
		echo 'invalid_option';;
esac
