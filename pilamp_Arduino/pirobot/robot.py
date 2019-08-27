#coding=utf-8
import sys
import time
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
sys.path.append(r"./pirobot")

from com import ComThread
import config_a

class Armbot(ComThread):
    '''
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = ComThread.__new__(cls, *args, **kw)
        return cls._instance
    '''
    def __init__(self, port = 'COM12'):
        # super(Armbot, self).__init__()
        self.port = port
        self.dict_servo = {1:1467, 2:1500, 3:1400, 4:1500, 5:1500}
        self.speed = config_a.SPEEDRATE
        self.start()
    
    def one_servo_to_pos(self, servo_id, servo_pos):
        print("servo %d get to position %d" % (servo_id, servo_pos))
        d = '#' + str(servo_id) + 'P' + str(servo_pos) + 'T' + str(self.speed) + '\r\n'
        print("command: ", d)
        self.l_serial.write(d.encode())
        return self.get_ok()

    def servos_to_pos(self, dict_servo):
        d = ''
        for i in range(1,6):
            print("servo %d get to position %d" % (i, dict_servo[i]))
            d += '#' + str(i) + 'P' + str(dict_servo[i]) 
        d += 'T' + str(self.speed) + '\r\n'
        print("command: ", d)
        self.l_serial.write(d.encode())
        return self.get_ok()


    # 用于人脸追踪，设置P1 P2两个舵机角度
    def set_cloud_platform_degree(self, bottom_degree, top_degree):
        '''
        command = '#1P1500#2P1500T1000\r\n'
        '''
        bottom_degree = 180 - bottom_degree
        # top_degree = 180 - top_degree
        p1_degree = int(1000 + bottom_degree*800/180)
        p2_degree = int(800  + top_degree*800/180)
        byte_raw = '#1P' + str(p1_degree) + '#2P' + str(p2_degree) + 'T800' + '\r\n'
        # print("d:", byte_raw)
        self.l_serial.write(byte_raw.encode())
    
    # 用于人脸追踪，找不到人时低头
    def do_bow_head(self):
        byte_raw = '#1P1400#2P1600T1000' + '\r\n'
        # print("d:", byte_raw)
        self.l_serial.write(byte_raw.encode())
    
    # 人脸追踪初始姿势
    def do_play_init_pos(self):
        byte_raw = '#1P1400#2P1000#3P800#5P1400T4000' + '\r\n'
        # print("d:", byte_raw)
        self.l_serial.write(byte_raw.encode())

    # 姿态检查初始姿势
    def do_work_init_pos(self):
        byte_raw = '#1P1400#2P1200#3P1650#5P1400T4000' + '\r\n'
        # print("d:", byte_raw)
        self.l_serial.write(byte_raw.encode())

    # 用于姿势提醒，摇晃
    def do_shake_head(self):
        byte_raw = '#1P1600T1000' + '\r\n'
        self.l_serial.write(byte_raw.encode())
        time.sleep(1)
        byte_raw = '#1P1200T1000' + '\r\n'
        self.l_serial.write(byte_raw.encode())
        time.sleep(1)
        byte_raw = '#1P1600T1000' + '\r\n'
        self.l_serial.write(byte_raw.encode())
        time.sleep(1)
        byte_raw = '#1P1200T1000' + '\r\n'
        self.l_serial.write(byte_raw.encode())
        time.sleep(1)
        byte_raw = '#1P1400T600' + '\r\n'
        self.l_serial.write(byte_raw.encode())


if __name__ == '__main__':
    myarm = Armbot()
    temp_a = 0
    while(temp_a != 99):
        temp_a = int(input('input the action:'))
        if temp_a == 1:
            myarm.do_bow_head()
        if temp_a == 2:
            myarm.do_shake_head()
        if temp_a == 3:
            myarm.do_play_init_pos()
        if temp_a == 4:
            myarm.do_work_init_pos()
        elif temp_a == 5:
            input_x = int(input('input the id:'))
            input_y = int(input('input the pos:'))
            myarm2 = Armbot()
            # print(id(myarm))
            # print(id(myarm2))
            myarm2.one_servo_to_pos(input_x, input_y)
        elif temp_a == 6:
            input_s = int(input('input the signal:'))
            myarm.go_air_pump(input_s)
        elif temp_a == 7:
            input_x = float(input('input the x:'))
            input_y = float(input('input the y:'))
            input_z = int(input('input the z:'))
            myarm.go_to_pos(input_x, input_y, input_z)
            
        elif temp_a == 9:
            input_last_x = float(input('input the last_x:'))
            input_last_y = float(input('input the last_y:'))
            input_new_x = int(input('input the new_x:'))
            input_new_y = int(input('input the new_y:'))
            alist = [input_new_x, input_new_y, input_last_x, input_last_y]
            myarm.move(alist)


