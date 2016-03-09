/*
 * Author: Ray Shen
 * Date Created: 08/03/2016
 * 
 * robot hand control
 *
 * This sketch controls a robot hand with 5 Futaba S3114 servos
 * using ROS and the arduiono
 * 
 */

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

Servo servo;

Servo servo_1; // 65-145
Servo servo_2; // 50-90
Servo servo_3; // 40-90
Servo servo_4; // 45-75
Servo servo_5; // 85-100

void servo_cb( const std_msgs::UInt16& cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}

void servo_1_cb( const std_msgs::UInt16& cmd_msg){
  servo_1.write(cmd_msg.data); //set servo angle, should be from 65-145
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
void servo_2_cb( const std_msgs::UInt16& cmd_msg){
  servo_2.write(cmd_msg.data); //set servo angle, should be from 50-90
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
void servo_3_cb( const std_msgs::UInt16& cmd_msg){
  servo_3.write(cmd_msg.data); //set servo angle, should be from 40-90
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
void servo_4_cb( const std_msgs::UInt16& cmd_msg){
  servo_4.write(cmd_msg.data); //set servo angle, should be from 45-75
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
void servo_5_cb( const std_msgs::UInt16& cmd_msg){
  servo_5.write(cmd_msg.data); //set servo angle, should be from 85-100
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}

ros::Subscriber<std_msgs::UInt16> sub("servo", servo_cb);

ros::Subscriber<std_msgs::UInt16> sub_1("servo_1", servo_1_cb);
ros::Subscriber<std_msgs::UInt16> sub_2("servo_2", servo_2_cb);
ros::Subscriber<std_msgs::UInt16> sub_3("servo_3", servo_3_cb);
ros::Subscriber<std_msgs::UInt16> sub_4("servo_4", servo_4_cb);
ros::Subscriber<std_msgs::UInt16> sub_5("servo_5", servo_5_cb);

void setup(){
  pinMode(13, OUTPUT);

  nh.initNode();
  nh.subscribe(sub);
  
  nh.subscribe(sub_1);
  nh.subscribe(sub_2);
  nh.subscribe(sub_3);
  nh.subscribe(sub_4);
  nh.subscribe(sub_5);

  servo.attach(5);
  
  servo_1.attach(6); //attach it to pin 6
  servo_2.attach(7); //attach it to pin 7
  servo_3.attach(8); //attach it to pin 8
  servo_4.attach(9); //attach it to pin 9
  servo_5.attach(10); //attach it to pin 10
}

void loop(){
  nh.spinOnce();
  delay(1);
}

