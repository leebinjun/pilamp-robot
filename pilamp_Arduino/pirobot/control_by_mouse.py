# -*- coding: utf-8 -*- 
'''
Python捕捉和模拟鼠标事件的方法_python_脚本之家 https://www.jb51.net/article/67172.htm

鼠标控制器

通过鼠标事件控制台灯运动

左右移动: 5号舵机旋转
前后移动: 3号舵机旋转
按滚轮左右移动: 1号舵机旋转
按滚轮前后移动: 2号舵机旋转

#TODO@libing
滚轮前后移动: 调光亮度
左键点击: 开灯/关灯
右键点击：切换灯模式

注意：
1. 只能运行在windows平台上
PyHook库依赖于另一个Python库PyWin32，PyWin32只能运行在Windows平台。
2. 程序一直处于监听状态死循环，通过移动鼠标触发TypeError退出
移动鼠标到在Position.x<80后会触发报错：TypeError: MouseSwitch() missing 8 required positional arguments: 'msg', 'x', 'y', 'data', 'flags', 'time', 'hwnd', and 'window_name'，程序退出
'''

class Control(object):

    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    # 角度值
    degree_yaw_s1   = 1460  # 1000-1467-1900
    degree_yaw_s5   =  838  #  838- 838-1231
    degree_pitch_s3 =  800  #  800- 800-1600
    degree_pitch_s2 = 1600  # 1400-1600-2200

    # 按滚轮标志位
    flag_wheel_on = False

    # 鼠标原点坐标
    position_x = 500 
    position_y = 500


    # 相对位置初始化
    def init_position(self, Position:(int, int), is_show=False):
        self.position_x = Position[0]
        self.position_y = Position[1]
        if is_show:
            print(f"init positon ok! x: {self.position_x}, y: {self.position_y}")

    # 接收鼠标事件，更新角度值
    def update_degrees(self, Message: int, Position: (int, int), Wheel: int, is_show=False):
        if Message == 519: # 如果检测到按滚轮
            self.flag_wheel_on = True
        elif Message == 520: # 如果检测到按滚轮松开
            self.flag_wheel_on = False
        elif Message == 512:
            if self.flag_wheel_on:      # 按滚轮，更新舵机值S1 S2
                self.degree_yaw_s1   = 1400 + Position[0] - self.position_x
                self.degree_pitch_s2 = 1200 + 2*(Position[1] - self.position_y)
            else:                       # 松开滚轮，更新舵机值S3 S5
                self.degree_yaw_s5   = 1400 + Position[0] - self.position_x
                self.degree_pitch_s3 = 1200 + Position[1] - self.position_y
        # 限幅
        self.degree_yaw_s1 = max(1000, self.degree_yaw_s1)
        self.degree_yaw_s1 = min(1900, self.degree_yaw_s1)
        self.degree_yaw_s5 = max( 838, self.degree_yaw_s5)
        self.degree_yaw_s5 = min(1231, self.degree_yaw_s5)
        self.degree_pitch_s2 = max(1400, self.degree_pitch_s2)
        self.degree_pitch_s2 = min(2200, self.degree_pitch_s2)
        self.degree_pitch_s3 = max( 800, self.degree_pitch_s3)
        self.degree_pitch_s3 = min(1600, self.degree_pitch_s3)
    
        if is_show:
            print(f"s1:{self.degree_yaw_s1}", end=" ")
            print(f"s2:{self.degree_pitch_s2}", end=" ")
            print(f"s3:{self.degree_pitch_s3}", end=" ")
            print(f"s5:{self.degree_yaw_s5}", end=" ")


    def get_degrees(self):
        return self.degree_pitch_s2, self.degree_pitch_s3, self.degree_yaw_s1, self.degree_yaw_s5



if __name__ == "__main__":
    
    import pythoncom, pyHook  

    import sys,os
    sys.path.append(os.path.dirname(__file__) + os.sep + '../')
    sys.path.append(r"./pirobot")

    # 初始化台灯舵机控制器lamp
    from pirobot.robot import Armbot
    lamp = Armbot()

    # 初始化鼠标控制器control
    morse_control = Control()


    i = -1
    def OnMouseEvent(event, is_show=False):
        global i

        if i == -1:
            morse_control.init_position(event.Position, is_show=True)

        # 更新morse_control控制器的值
        morse_control.update_degrees( event.Message, event.Position, event.Wheel, is_show=True)
        if is_show:   
            # print('MessageName:',event.MessageName)
            print('Message:',event.Message)
            # print('Time:',event.Time)
            # print('Window:',event.Window)
            # print('WindowName:',event.WindowName)
            print('Position:',event.Position)
            # print('Wheel:',event.Wheel)
            # print('Injected:',event.Injected)
            # print('---')

        # 更新舵机动作，每20次做一次更新
        i = i + 1 
        if i % 20 == 0:      
            i = 0
            degree_s2, degree_s3, degree_s1, degree_s5 = morse_control.get_degrees()
                    
            if is_show:
                print("servo1 to ", degree_s1)
                print("servo2 to ", degree_s2)
                print("servo3 to ", degree_s3)
                print("servo5 to ", degree_s5)

            lamp.one_servo_to_pos(servo_id=1, servo_pos=degree_s1)
            lamp.one_servo_to_pos(servo_id=2, servo_pos=degree_s2)
            lamp.one_servo_to_pos(servo_id=3, servo_pos=degree_s3)
            lamp.one_servo_to_pos(servo_id=5, servo_pos=degree_s5)
        
        # 返回 True 可将事件传给其它处理程序，否则停止传播事件 
        return True

    def main():
        # 创建钩子管理对象 
        hm = pyHook.HookManager() 
        # 监听所有鼠标事件 
        hm.MouseAll = OnMouseEvent # 等效于hm.SubscribeMouseAll(OnMouseEvent) 
        # 开始监听鼠标事件 
        hm.HookMouse() 
        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()

    main()
