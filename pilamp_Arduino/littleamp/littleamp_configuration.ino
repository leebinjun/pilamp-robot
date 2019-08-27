

#include <Servo.h>

/*Class four Servos*/
Servo headYaw_servo;
Servo headPitch_servo;
Servo bodyUp_servo;
Servo bodyDown_servo;

/*define pins for servo*/
int headYaw_pin   = 6;
int headPitch_pin = 7;
int bodyUp_pin    = 8;
int bodyDown_pin  = 9;

/*define pins for stepmotor*/
int dirPin = 10;
int stepperPin = 11;

/*define pins for led*/
int ledColdPin = 3;
int ledWarmPin = 2;

/*Array for inital state*/
const int standSt[] = {
1,0,0,0,0,
300,1600,1600,1100,1500};

/*Array for target state*/
int tmpSt[] = {
1,0,0,0,0,
300,1600,1600,1100,1500};

/*updata the state of the servos*/
int currentHeadYaw, currentHeadPitch, currentBodyUp, currentBodyDown;
int startHeadYaw,   startHeadPitch,   startBodyUp,   startBodyDown;

/* store each action and the time*/
const int headYawCenter = 1600;
const int headPitchCenter = 1700;
const int bodyUpCenter = 1100;
const int bodyDownCenter = 1500;


int actDo[5];
long timeAtlastAct;

int defaultArr[5]={100, headYawCenter, headPitchCenter, bodyUpCenter, bodyDownCenter};

char k;
String comD="";
String comDo="";
int v=0;
int loopvalue;

/*target following*/
int target_x=0,target_y=0;
int target_dis2=0;
float target_dis=0;




