
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int val; //定义一个全局变量val，用来存放串口接收到的数据的。


void setup()
{
    // 运行指示灯
    pinMode(13, OUTPUT);//设置13脚为输出脚，同时13脚是接到板子内部LED的。
    // 4路继电器
    pinMode(4, OUTPUT);//设置4脚为输出脚
    pinMode(5, OUTPUT);//设置5脚为输出脚
    pinMode(6, OUTPUT);//设置6脚为输出脚
    pinMode(7, OUTPUT);//设置7脚为输出脚
    // 串口初始化
    Serial.begin(9600);//设置串口波特率为9600buad
    // reserve 200 bytes for the inputString:
    inputString.reserve(200);
    // 运行指示灯初始化
    digitalWrite(13, LOW);//先令13脚为低电平，LED熄灭。
    // 4路继电器初始化
    digitalWrite(7, HIGH);//先令4脚为低电平，LED熄灭。
    digitalWrite(6, HIGH);//先令5脚为低电平，LED熄灭。
    digitalWrite(5, HIGH);//先令6脚为低电平，LED熄灭。
    digitalWrite(4, HIGH);//先令7脚为低电平，LED熄灭。
    // 等待初始化完成
    delay(2000);//延时2秒钟，等待模块初始化完毕，这个不能省略，如果发现启动后没语音提示，可以再延长一点试试。
    Serial.print("ready");//准备好了
}
void loop()//循环执行
{
    if (stringComplete) {
        Serial.println(inputString);
        // clear the string:
        val = (char)inputString[0];
        inputString = "";
        stringComplete = false;
        if ('1' == val)//如果喊“开灯”模块会发送“开灯”对应的返回值“001”（十进制）给arduino，所以只要判断数字是不是1，是就证明识别到“开灯”了。
        {
            digitalWrite(7, LOW);//如果识别到关灯，就熄灭LED。
            delay(200);
            digitalWrite(7, HIGH);//如果识别到开灯，就点亮LED
            Serial.print("ok");
        }
        if ('2' == val)//如果喊“关灯”模块会发送“关灯”对应的返回值“002”（十进制）给arduino，所以只要判断数字是不是2，是就证明识别到“关灯”了。
        {
            digitalWrite(6, LOW);//如果识别到关灯，就熄灭LED。
            delay(200);
            digitalWrite(6, HIGH);//如果识别到关灯，就熄灭LED。
            Serial.print("ok");
        }
        if ('3' == val)//如果喊“关灯”模块会发送“关灯”对应的返回值“002”（十进制）给arduino，所以只要判断数字是不是2，是就证明识别到“关灯”了。
        {
            digitalWrite(5, LOW);//如果识别到关灯，就熄灭LED。
            delay(200);
            digitalWrite(5, HIGH);//如果识别到关灯，就熄灭LED。
            Serial.print("ok");
        }
        if ('4' == val)//如果喊“关灯”模块会发送“关灯”对应的返回值“002”（十进制）给arduino，所以只要判断数字是不是2，是就证明识别到“关灯”了。
        {
            digitalWrite(4, LOW);//如果识别到关灯，就熄灭LED。
            delay(200);
            digitalWrite(4, HIGH);//如果识别到关灯，就熄灭LED。
            Serial.print("ok");
        }
    }
    // 正常运行中
    digitalWrite(13, LOW);//先令13脚为低电平，LED熄灭。
    delay(100);
    digitalWrite(13, HIGH);//先令13脚为低电平，LED熄灭。
    delay(100);
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
    while (Serial.available()) {
        // get the new byte:
        char inChar = (char)Serial.read();
        // add it to the inputString:
        inputString += inChar;
        // if the incoming character is a newline, set a flag
        // so the main loop can do something about it:
        if (inChar == '\n') {
            stringComplete = true;
        }
    }
}




