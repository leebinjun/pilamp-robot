#coding=utf-8

# print(serial.CR)
# b'\r'

# print(serial.LF)
# b'\n'
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from voice.speech import SpeechThread

import threading
import time
sys.path.append('/home/shunya/.local/lib/python3.5/site-packages')
import serial
import cv2

class LightThread:
    def __init__(self, port='COM3'):
    #构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = port
        self.ID = None
        self.data = None
        # 灯状态
        self.on = False

   #定义串口等待的函数
    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        # self.stop()

    #启动串口的函数
    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 9600
        #设置等待时间，若超出这停止等待
        self.l_serial.timeout = 2
        self.l_serial.open()
        #判断串口是否已经打开
        if self.l_serial.isOpen() is not True:
            print("serial init failed.")
            exit()
    
    def get_info(self):
        data = ''
        data = data.encode('utf-8')                        #由于串口使用的是字节，故而要进行转码，否则串口会不识别
        n = self.l_serial.inWaiting()                      #获取接收到的数据长度
        if n: 
            #读取数据并将数据存入data
            data = data + self.l_serial.read(n)
            #输出接收到的数据
            print('get data from serial port:', data)
            return data
        else:
            return None       

    def go_led_on(self):
        if self.on:
            return self.get_info()
        else:
            self.on = True
            d = '3'+'\r\n'
            self.l_serial.write(d.encode())
            return self.get_info()

    def go_led_off(self):
        if self.on:
            self.on = False
            d = '3'+'\r\n'
            self.l_serial.write(d.encode())
            return self.get_info()
        else:
            return self.get_info()

    def go_led_change(self):
        d = '4'+'\r\n'
        self.l_serial.write(d.encode())
        return self.get_info()

    def go_led_high(self):
        d = '1'+'\r\n'
        self.l_serial.write(d.encode())
        return self.get_info()

    def go_led_low(self):
        d = '2'+'\r\n'
        self.l_serial.write(d.encode())
        return self.get_info()


if __name__ == '__main__':
    ser_lamp = LightThread()
    ser_speech = SpeechThread()
    temp_a = 0
    ser_lamp.start()
    ser_speech.start()
    while 1:
        tmp = ser_speech.get_info()
        if tmp:
            if tmp[-1] == 1:
                ser_lamp.go_led_on()
                print('02 light on')
            elif tmp[-1] == 2:
                ser_lamp.go_led_off()
                print('02 light off')
            elif tmp[-1] == 3:
                ser_lamp.go_led_change()
                print('01 change')
            elif tmp[-1] == 5:
                ser_lamp.go_led_high()
                print('03 high')
            elif tmp[-1] == 6:
                ser_lamp.go_led_low()
                print('04 low')


