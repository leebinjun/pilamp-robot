
/*setup()*/
void setup()
{
    Serial.begin(9600);
    attachMyServo();
    initStepmotor();
    initLed();
    defaultAct();
    toArrAct(standSt);
    Serial.println("ok!");
}

/*loop()*/
void loop()
{
    readSerial();
    loopAct(); 
    //while(1);
}
