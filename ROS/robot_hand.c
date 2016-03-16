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

//#define SV1 1
#define SV2 1
#define SV3 1
#define SV4 1
//#define SV5 1

ros::NodeHandle  nh;

//Servo servo;

#ifdef SV1
Servo servo_1; // 65-145
#endif
#ifdef SV2
Servo servo_2; // 50-90
#endif
#ifdef SV3
Servo servo_3; // 40-90
#endif
#ifdef SV4
Servo servo_4; // 45-75
#endif
#ifdef SV5
Servo servo_5; // 85-100
#endif

//void servo_cb( const std_msgs::UInt16& cmd_msg){
//  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
//  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
//}

#ifdef SV1
void servo_1_cb( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data<65 || cmd_msg.data>145) return;
  servo_1.write(cmd_msg.data); //set servo angle, should be from 65-145
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
#endif
#ifdef SV2
void servo_2_cb( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data<50 || cmd_msg.data>90) return;
  servo_2.write(cmd_msg.data); //set servo angle, should be from 50-90
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
#endif
#ifdef SV3
void servo_3_cb( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data<40 || cmd_msg.data>90) return;
  servo_3.write(cmd_msg.data); //set servo angle, should be from 40-90
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
#endif
#ifdef SV4
void servo_4_cb( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data<45 || cmd_msg.data>75) return;
  servo_4.write(cmd_msg.data); //set servo angle, should be from 45-75
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
#endif
#ifdef SV5
void servo_5_cb( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data<85 || cmd_msg.data>100) return;
  servo_5.write(cmd_msg.data); //set servo angle, should be from 85-100
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
}
#endif

//ros::Subscriber<std_msgs::UInt16> sub("servo", servo_cb);

#ifdef SV1
ros::Subscriber<std_msgs::UInt16> sub_1("servo_1", servo_1_cb);
#endif
#ifdef SV2
ros::Subscriber<std_msgs::UInt16> sub_2("servo_2", servo_2_cb);
#endif
#ifdef SV3
ros::Subscriber<std_msgs::UInt16> sub_3("servo_3", servo_3_cb);
#endif
#ifdef SV4
ros::Subscriber<std_msgs::UInt16> sub_4("servo_4", servo_4_cb);
#endif
#ifdef SV5
ros::Subscriber<std_msgs::UInt16> sub_5("servo_5", servo_5_cb);
#endif

void setup(){
  pinMode(13, OUTPUT);

  nh.initNode();
//  nh.subscribe(sub);

#ifdef SV1
  nh.subscribe(sub_1);
#endif
#ifdef SV2
  nh.subscribe(sub_2);
#endif
#ifdef SV3
  nh.subscribe(sub_3);
#endif
#ifdef SV4
  nh.subscribe(sub_4);
#endif
#ifdef SV5
  nh.subscribe(sub_5);
#endif

//  servo.attach(4);
  
#ifdef SV1
  servo_1.attach(6); //attach it to pin 6
#endif
#ifdef SV2
  servo_2.attach(7); //attach it to pin 7
#endif
#ifdef SV3
  servo_3.attach(8); //attach it to pin 8
#endif
#ifdef SV4
  servo_4.attach(9); //attach it to pin 9
#endif
#ifdef SV5
  servo_5.attach(10); //attach it to pin 10
#endif
}

void loop(){
  nh.spinOnce();
  delay(1);
}
