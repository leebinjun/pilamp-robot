# -*- coding:utf-8 -*-
'''
PC使用PySerial发送数据
负责与ESP32主控的舵机云台进行通信
------------------------------------
## 注意
运行此程序的时候，需要修改设备的权限，
sudo chmod 777 /dev/ttyUSB?  ，其中 ? = 0,1,2,...
或者使用管理员权限运行脚本
sudo python xxxxx.py

'''
import serial
import struct
import time

# 串口号 默认为 /dev/ttyUSB0
# ser_dev = '/dev/ttyUSB1'
ser_dev = 'com12'

# 创建一个串口实例
ser = serial.Serial(ser_dev, 9600, timeout=1, bytesize=8)

def set_cloud_platform_degree(bottom_degree, top_degree):
    global ser
    '''
    command = '#1P1500#2P1500T1000\r\n'
    '''
    bottom_degree = 180 - bottom_degree
    # top_degree = 180 - top_degree
    p1_degree = int(1000 + bottom_degree*800/180)
    p2_degree = int(800  + top_degree*800/180)
    byte_raw = '#1P' + str(p1_degree) + '#2P' + str(p2_degree) + 'T1000' + '\r\n'

    ser.write(byte_raw.encode())

if __name__ == "__main__":

    while True:
        # 测试角度
        set_cloud_platform_degree(100, 100)
        # 每隔10s发送一次数据
        time.sleep(10)

