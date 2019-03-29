/*function of initial the stepmotor*/
void initStepmotor()
{
    pinMode(dirPin, OUTPUT);
    pinMode(stepperPin, OUTPUT);
}

/*function of initial the led*/
void initLed()
{
    pinMode(ledWarmPin, OUTPUT);
    pinMode(ledColdPin, OUTPUT);
}

/*function of stepmotor test*/
void stepgo(boolean dir,int steps){
  digitalWrite(dirPin, dir);
  delay(50);
  for(int i=0;i<steps;i++){
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(2000); 
  }
}

/*function of attach four Servos*/
void attachMyServo()
{
    headYaw_servo.attach(headYaw_pin  , headYawCenter-600  , headYawCenter+600  );
    headPitch_servo.attach(headPitch_pin, headPitchCenter-500, headPitchCenter+500);
    bodyUp_servo.attach(bodyUp_pin   , bodyUpCenter-500   , bodyUpCenter+500   );
    bodyDown_servo.attach(bodyDown_pin , bodyDownCenter-500 , bodyDownCenter+500 );
}

/*initialize the state*/
void defaultAct()
{
    currentHeadYaw   = headYawCenter;
    currentHeadPitch = headPitchCenter;
    currentBodyUp    = bodyUpCenter;
    currentBodyDown  = bodyDownCenter;
    updateAct();
    startHeadYaw   = headYawCenter;
    startHeadPitch = headPitchCenter;
    startBodyUp    = bodyUpCenter;
    startBodyDown  = bodyDownCenter;
}

/*Serco.write */
void updateAct()
{
    headYaw_servo.  writeMicroseconds(currentHeadYaw);
    headPitch_servo.writeMicroseconds(currentHeadPitch);
    bodyUp_servo.   writeMicroseconds(currentBodyUp);
    bodyDown_servo. writeMicroseconds(currentBodyDown);
}

/*function of analysis each action*/
void toArrAct(const int *currAnim)
{
  int stepAnim=*currAnim;
  char flag_fram;

  currAnim +=5;
  Serial.print("currAnim:");
  Serial.println(*currAnim);
  
  timeAtlastAct=millis();

  while(stepAnim)
  {
    Serial.println("helllllllll!");
    for(int i=0;i<5;i++)
    {
      actDo[i]=*(currAnim++);
      Serial.println(actDo[i]);
    }
    currentHeadYaw=actDo[1];
    currentHeadPitch=actDo[2];
    currentBodyUp=actDo[3];
    currentBodyDown=actDo[4];
    flag_fram=1;

    while(flag_fram)
    {
      long currTime =millis();
      int timeBetweenF = currTime - timeAtlastAct;
      Serial.print("timeBetweenF:");
      Serial.println(timeBetweenF);
      Serial.print("actDo[0]:");
      Serial.println(actDo[0]);
      //while(1);
      
      if(timeBetweenF >= actDo[0])
      {
        currentHeadYaw=actDo[1];
        currentHeadPitch=actDo[2];
        currentBodyUp=actDo[3];
        currentBodyDown=actDo[4];
        updateAct();
        startHeadYaw=currentHeadYaw;
        startHeadPitch=currentHeadPitch;
        startBodyUp=currentBodyUp;
        startBodyDown=currentBodyDown;

        timeAtlastAct=currTime;
        flag_fram=0;
      }
      float time_f = (currTime - timeAtlastAct)/(float)actDo[0];
      Serial.println(time_f);
      currentHeadYaw=startHeadYaw+(actDo[1]-startHeadYaw)*time_f;
      currentHeadPitch=startHeadPitch+(actDo[2]-startHeadPitch)*time_f;
      currentBodyUp=startBodyUp+(actDo[3]-startBodyUp)*time_f;
      currentBodyDown=startBodyDown+(actDo[4]-startBodyDown)*time_f;
      updateAct();
    }
    stepAnim--;
  }
  //defaultAct();

}

int tmp[4] = {0,0,0,0};
int tmp_i = 0;
int mytest()
{
//    int tmp[4] = {0,0,0,0};
//    int i = 0;
    if(Serial.available())
    {
        k=Serial.read();
        Serial.println(k);
        if(k>='A'&&k<='Z')
            comD+=k;
        else if(k>='0' && k<='9')
        {
            tmp[tmp_i]=tmp[tmp_i]*10+k-'0';
            Serial.println(tmp_i, tmp[tmp_i]);
        }   
        else if(k==',')
        {
            tmp_i++;
//            Serial.println(",,,,");
            if(tmp_i==4)
                Serial.println("wrong:too much num!");
        }
        else if(k=='>')
        {
            for(int i=0;i<4;i++)
            {
                tmpSt[i+6] = tmp[i];
                tmp[i] = 0;
                Serial.println(tmpSt[i+6]);
            }
            tmp_i = 0;
            comDo=comD;
            comD="";
            return 1;
        }
    }
    return 0;
}

