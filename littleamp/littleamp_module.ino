
void readSerial()
{
    // 输入格式：<XX,99>
    // comDo = XX
    // loopvalue = 99  
    if(Serial.available())
    {
        k=Serial.read();
        Serial.println(k);
        if(k>='A'&&k<='Z')
            comD+=k;
        else if(k>='0' && k<='9')
            v=v*10+k-'0';
        else if(k=='>')
        {
            comDo=comD;
            if(v==0)
                loopvalue=1;
            else
                loopvalue=v;
            comD="";
            v=0;
        }
    }
}

void loopAct()
{
//    if(comDo == "ZS")
//    {
//        do{
//            foo = cal_target();
//            toArrAct(foo);
//            target_dis2 = target_x*target_x + target_y*target_y;
//        }while(target_dis2 < 5.0)
//        Serial.println("y");
//    }

    ////新增测试
    if(comDo == "XX")
    {
        comDo = "";
        int times = 0;
        do{
            times += mytest();
            if(comDo == "XX")
            {
                toArrAct(tmpSt);
                comDo = "";
            }
        }while(times<loopvalue);
    }

    ////步进电机测试
    if(comDo == "TE")
    {
        stepgo(false, loopvalue);
        delay(500);
        Serial.println("10");
    }
    if(comDo == "TA")
    {
        stepgo(true, 50);
        delay(500);
        Serial.println("10");
    }

    ////灯测试
    if(comDo == "LW")
    {
        digitalWrite(ledColdPin, LOW);
        delay(500);
        Serial.println("LW");
    }
    if(comDo == "LC")
    {
        digitalWrite(ledWarmPin, LOW); 
        delay(500);
        Serial.println("LC");
    }
    if(comDo == "LO")
    {
        digitalWrite(ledWarmPin, LOW); 
        digitalWrite(ledColdPin, LOW);
        delay(500);
        Serial.println("LO");
    }
    if(comDo == "LB")
    {
        digitalWrite(ledWarmPin, HIGH); 
        digitalWrite(ledColdPin, HIGH);
        delay(500);
        Serial.println("LB");
    }
    
    ///舵机测试
    if(comDo=="FW")
    {
        int which = loopvalue%10;
        int loopp = loopvalue/10;
        do{
          switch(which){
          case 1:
            currentHeadYaw   += 2;
            updateAct();
            break;
          case 2:
            currentHeadPitch += 2;
            updateAct();
            break;
          case 3:
            currentBodyUp    += 2;
            updateAct();
            break;
          case 4:
            currentBodyDown  += 2;
            updateAct();
            break;   
          }         
//            Serial.println("currentHeadPitch");
//            Serial.println(currentHeadPitch); 
        }while(--loopp);
        //toArrAct(walkEnd);
        Serial.println("y");
    }

   else  if(comDo=="BW")
    {
        int which = loopvalue%10;
        int loopp = loopvalue/10;
        do{
          switch(which){
          case 1:
            currentHeadYaw   -= 2;
            updateAct();
            break;
          case 2:
            currentHeadPitch -= 2;
            updateAct();
            break;
          case 3:
            currentBodyUp    -= 2;
            updateAct();
            break;
          case 4:
            currentBodyDown  -= 2;
            updateAct();
            break;     
          }       
//            Serial.println("currentHeadPitch");
//            Serial.println(currentHeadPitch); 
        }while(--loopp);
        //toArrAct(walkEnd);
        Serial.println("y");
//      do{
//              currentHeadYaw   -= 2;
//              currentHeadPitch -= 2;
//              currentBodyUp    -= 2;
//              currentBodyDown  -= 2;
//              updateAct();
//              
//              Serial.println("currentHeadPitch");
//              Serial.println(currentHeadPitch); 
//          }while(--loopvalue);
//          //toArrAct(walkEnd);
//          Serial.println("y");
     }

   else if(comDo=="AB")
  {
       do{
              currentHeadYaw   -= 0;
              currentHeadPitch -= 1;
              currentBodyUp    += 2;
              currentBodyDown  -= 0;
              updateAct();
              
              Serial.println("currentHeadPitch");
              Serial.println(currentHeadPitch); 
          }while(--loopvalue);
          //toArrAct(walkEnd);
          Serial.println("y");
  }

   else if(comDo=="AC")
  {
       do{
              currentHeadYaw   += 0;
              currentHeadPitch += 1;
              currentBodyUp    -= 2;
              currentBodyDown  += 0;
              updateAct();
              
              Serial.println("currentHeadPitch");
              Serial.println(currentHeadPitch); 
          }while(--loopvalue);
          //toArrAct(walkEnd);
          Serial.println("y");
  }
  else if(comDo=="LT")
  {
    do{
        toArrAct(turnL);
    }while(--loopvalue);
    Serial.println("y");
  }
  else
  if(comDo=="RT")
  {
    do{
      toArrAct(turnR);
    }while(--loopvalue);
      Serial.println("y");
  }
 else
  if(comDo=="WX")
  {
    
    do{
      toArrAct(wobble);
    }while(--loopvalue);
  }
  else
  if(comDo=="WY")
  {
    do{
      toArrAct(wobbleL);
    }while(--loopvalue);
      Serial.println("y");
  }
  else
  if(comDo=="WZ")
  {
    
    do{
      toArrAct(wobbleR);
    }while(--loopvalue);
      Serial.println("y");
  }
  else
  if(comDo=="TX")
  {
    do{
      toArrAct(tapFeet);
    }while(--loopvalue);
      Serial.println("y");
  }
   else
  if(comDo=="TY")
  {
    do{
      toArrAct(tapLF);
    }while(--loopvalue);
      Serial.println("y");
  }
 else
  if(comDo=="TZ")
  {
    do{
      toArrAct(tapRF);
    }while(--loopvalue);
     Serial.println("y");
  }
  else
  if(comDo=="LX")
  {
    do{
      toArrAct(shakeL);
    }while(--loopvalue);
    Serial.println("y");
  }
  else
  if(comDo=="LY")
  {
    do{
      toArrAct(shakeLL);
    }while(--loopvalue);
     Serial.println("y");
  }
  else
  if(comDo=="LZ")
  {
    do{
      toArrAct(shakeRL);
    }while(--loopvalue);
     Serial.println("y");
  }
  else
  if(comDo=="SX")
  {
    do{
      toArrAct(shakeH);
    }while(--loopvalue);
    Serial.println("y");
  }
  else
  if(comDo=="ST")
  {

    do{
      toArrAct(standSt);
    }while(--loopvalue);
      Serial.println("y");
  }
 else
  if(comDo=="BX")
  {
    do{
      toArrAct(bounce);
    }while(--loopvalue);
    Serial.println("y");
  }
  else 
  if(comDo=="ZY")
  {
    do{
 
       toArrAct(bothBo);
    }while(--loopvalue);
    toArrAct(walkEnd); 
    Serial.println("y");
  }
  else 
  if(comDo=="TK")
  {
    do{
 
      toArrAct(taiSky);
    }while(--loopvalue);
    Serial.println("y");
  }
  else 
  if(comDo=="DZ")
  {
    do{
       toArrAct(onlyleg);
     }while(--loopvalue);
   Serial.println("y");
  }
  else if(comDo=="DE")
  {
    delay(1000);
  }
   else 
  if(comDo=="TB")
  {
    do{
 
       toArrAct(tapBw);
     }while(--loopvalue);
   Serial.println("y");
  }
    else 
  if(comDo=="US")
  {
    do{
   
       toArrAct(upSleg);
     }while(--loopvalue);
   Serial.println("y");
  }
  comDo="";
 }
