# Python Tkinter Scale和LabeledScale用法 http://c.biancheng.net/view/2509.html
# python tkinter可以使用的颜色 - wjcaiyf的专栏 - CSDN博客 https://blog.csdn.net/wjciayf/article/details/79261005
'''
新版台灯的UI控制器

设置运动速度
调整5个舵机运动

#TODO@libing
开灯/关灯
切换灯模式

'''

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import tkinter as tk
from tkinter import Frame
from robot import Armbot
import config_a

class GUI(Frame):
    
    def __init__(self, master, **kw):


        Frame.__init__(self, master, **kw)
        frame = Frame(master, height=692+30, width=803+20, bg="Chocolate")
        frame.place(x=(720-692-10)/2, y=(840-803-10)/2)
        # 串口设置相关变量
        self.armbot = Armbot()

        # 创建画布，放置机械臂背景图
        self.ca = tk.Canvas(frame, 
                            background='white',
                            width=803,
                            height=692)
        self.bm = tk.PhotoImage(file="pirobot/a.gif")
        self.ca.place(x=(720-692-10)/2, y=(840-803-10)/2, width=803, height=692)
        self.ca.create_image(803/2 + 1, 692/2 + 1, image=self.bm)

        # 创建滑动条，速度
        self.scs = tk.Scale(frame, 
                            label='speed',                    # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=9999,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='crimson',            # 设置轨道的背景色
                            variable=self.armbot.speed,       # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=5000,                # 设置指示刻度细分
                            resolution=50,                    # 设置步长
                            bg='Lavenderblush',               # 设置背景颜色
                            command=self.set_speed)           # 设置绑定事件处理，函数或方法
        self.scs.place(x=50, y=50)
        self.scs.set(self.armbot.speed)

        # 创建滑动条，舵机1
        self.servo1_v = tk.StringVar()
        self.sc1 = tk.Scale(frame, 
                            label='servo1',                   # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=2200,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='blue',               # 设置轨道的背景色
                            variable=self.servo1_v,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=1500/3,              # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LightCyan',                   # 设置背景颜色
                            command=self.servo1_to_pos)       # 设置绑定事件处理，函数或方法
        self.sc1.place(x=255, y=600)
        self.sc1.set(config_a.INIT_POS[1])

        # 创建滑动条，舵机2
        self.servo2_v = tk.StringVar()
        self.sc2 = tk.Scale(frame, 
                            label='servo2',                   # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=2200,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='gold',               # 设置轨道的背景色
                            variable=self.servo2_v,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=400/4,               # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='lightyellow',                 # 设置背景颜色
                            command=self.servo2_to_pos)       # 设置绑定事件处理，函数或方法
        self.sc2.place(x=115, y=310)
        self.sc2.set(config_a.INIT_POS[2])
        
        # 创建滑动条，舵机3
        self.servo3_v = tk.StringVar()
        self.sc3 = tk.Scale(frame, 
                            label='servo3',                   # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=2200,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.servo3_v,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=900/3,               # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.servo3_to_pos)       # 设置绑定事件处理，函数或方法
        self.sc3.place(x=600, y=260)
        self.sc3.set(config_a.INIT_POS[3])

        # 创建滑动条，舵机4
        self.servo4_v = tk.StringVar()
        self.sc4 = tk.Scale(frame, 
                            label='servo4',                   # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=2200,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='gold',               # 设置轨道的背景色
                            variable=self.servo4_v,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=400/4,               # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='lightyellow',                 # 设置背景颜色
                            command=self.servo4_to_pos)       # 设置绑定事件处理，函数或方法
        self.sc4.place(x=115, y=510)
        self.sc4.set(config_a.INIT_POS[4])
        
        # 创建滑动条，舵机5
        self.servo5_v = tk.StringVar()
        self.sc5 = tk.Scale(frame, 
                            label='servo5',                   # 设置标签内容
                            from_=500,                        # 设置最大值
                            to=2200,                          # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.servo5_v,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=900/3,               # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.servo5_to_pos)       # 设置绑定事件处理，函数或方法
        self.sc5.place(x=600, y=460)
        self.sc5.set(config_a.INIT_POS[5])


        # 添加菜单
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade (label='File', menu=filemenu)

        filemenu.add_separator ()
        filemenu.add_command (label='Exit', command=master.quit)
        master.config(menu=menubar)

    def set_speed(self, v):
        print("speed set ", v)
        self.armbot.speed = v

    def servo1_to_pos(self, value1):
        print("servo1 to ", value1)
        self.armbot.one_servo_to_pos(servo_id=1, servo_pos=int(value1))

    def servo2_to_pos(self, value2):
        print("servo2 to ", value2)
        self.armbot.one_servo_to_pos(servo_id=2, servo_pos=int(value2))

    def servo3_to_pos(self, value3):
        print("servo3 to ", value3)
        self.armbot.one_servo_to_pos(servo_id=3, servo_pos=int(value3))

    def servo4_to_pos(self, value4):
        print("servo4 to ", value4)
        self.armbot.one_servo_to_pos(servo_id=4, servo_pos=int(value4))

    def servo5_to_pos(self, value5):
        print("servo5 to ", value5)
        self.armbot.one_servo_to_pos(servo_id=5, servo_pos=int(value5))



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Serial GUI")
    root.geometry("840x730")
    app = GUI(root)
    root.mainloop()



