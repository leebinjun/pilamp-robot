'''
1 通信参数
USB转串口(TTL电平)   COM3   波特率9600, 8位数据位, 1位停止位, 无校验位

2 命令格式
命令                                   功能             说明
#STOP\r\n                       |  停止当前动作   |  停止当前所有动作    
#1P1500T100\r\n                 |  控制单个舵机   |  数据 1 是舵机的通道
                                                    数据 1500 是舵机的位置，范围是 500-2500
                                                    数据 100 是执行的时间，表示速度，范围是 100-9999
#1P15001P15001P1500T100\r\n     |  控制多个舵机   |  该命令是同时执行的，也就是所有的舵机都是一起动的

3 注意
\r\n是命令的结束符，必须得有。
所有命令中都不含空格。
\r\n 是 2 个字符，是回车符和换行符，是十六进制数 0x0D 和 0x0A，是 Chr(13) 和 Chr(10) 。
舵机驱动分辨率：0.5us , 0.045 度。

'''
import sys
sys.path.append('/home/shunya/.local/lib/python3.5/site-packages')
import serial
import threading
import time

class ComThread(object):
    def __init__(self):
    #构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = None
        self.ID = None
        self.data = None

    #查看可用的串口
    def Check_Comx(self):
        import serial.tools.list_ports
        comlist = list(serial.tools.list_ports.comports())
        if len(comlist) <= 0:
            print("Wrong：Not Found Com, Please Check The Connection.")
            return 0
        else:
            return comlist 

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
            
    def get_ok(self):
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
    
    

if __name__ == "__main__":
    
    myserial = ComThread()
    alist = myserial.Check_Comx()
    print(alist)
    for i in alist:
        print(str(i))

