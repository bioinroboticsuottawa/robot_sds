rostopic pub /pumpkin/playback_action/goal pumpkin_messages/PlaybackActionGoal -1 -- '{header: auto, goal: [['/home/rayshen/Dev/pumpkin_ws/src/pumpkin/playback/straight_hand/bye.yaml']]}'

sudo chmod a+rw /dev/ttyACM0
rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=57600