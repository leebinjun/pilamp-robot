#! /usr/bin/python3
# -*- coding: utf-8 -*-
# 未来的config文件
PORTNUM_ARMBOT = '/dev/ttyUSB2'
PORTNUM_SPEECH = '/dev/ttyUSB1'
PORTNUM_LIGHTS = '/dev/ttyUSB0'

import cv2
import time

import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

# USB摄像头
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # set Width
cap.set(4, 240)  # set Height

# 坐姿和手机检测器detector
from pose.vision import Handler
detector = Handler()
# 人脸检测器face_detect
from face.face_detection_hog import FaceDetect
face_detect = FaceDetect()
# 台灯机械臂arm_lamp
from pirobot.robot import Armbot
arm_lamp = Armbot(port=PORTNUM_ARMBOT)
# 跟随计算track
from track.face_track import Tracker
track = Tracker()
# 语音指示监听
from voice.speech import SpeechThread
speaker = SpeechThread(port=PORTNUM_SPEECH)
# 灯控制
from light.led import LightThread
light = LightThread(port=PORTNUM_LIGHTS)



# 初始化工作姿态
arm_lamp.do_work_init_pos()
speaker.start()
light.start()


# 模式标志位
# 0: listening
# 1: working
# 2: playing
mode = 0
count_noface = 0
img_logo = cv2.imread("/home/shunya/pilamp/etc/pilamp.png")

def listen():
    print("[listen]")
    global mode
    global count_noface
    cv2.imshow("pilamp", img_logo)
    k = cv2.waitKey(100)
    # print("k:", k)
    if k == ord('l'):
        print('03 learn')
        mode = 1
        arm_lamp.do_work_init_pos()
    if k == ord('p'):
        print('04 play')
        arm_lamp.do_play_init_pos()
        mode = 2
        arm_lamp.set_cloud_platform_degree(track.last_btm_degree, track.last_top_degree)
    tmp = speaker.get_info()
    if tmp:
        if tmp[-1] == 1:
            print('01 light on')
            light.go_led_on()
        elif tmp[-1] == 2:
            print('02 light off')
            light.go_led_off()
        elif tmp[-1] == 3:
            print('03 work')
            mode = 1
            # 舵机角度初始化
            arm_lamp.do_work_init_pos()
        elif tmp[-1] == 4:
            print('04 play')
            mode = 2
            # 舵机角度初始化
            arm_lamp.do_play_init_pos()
            arm_lamp.set_cloud_platform_degree(track.last_btm_degree, track.last_top_degree)
            # 找不到人脸计数
            count_noface = 0

while cap.isOpened():
    if mode == 0:
        listen()

    elif mode == 2:

        # TODO 阅读最后一帧
        ret, img = cap.read()
        ret, img = cap.read()
        ret, img = cap.read()
        ret, img = cap.read()
        # 画面水平翻转
        # img = cv2.flip(img, 1)
        
        # Converting the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        box = face_detect.detect(img, gray)
        face_detect.show(img)
        
        if box:
            # 当前画面有人脸
            (x, y, w, h) = box
            # 在原彩图上绘制矩形
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)

            img_height, img_width,_ = img.shape
            print("img h:{} w:{}".format(img_height, img_width))
            # 计算x轴与y轴的偏移量
            (offset_x, offset_y) = track.calculate_offset(img_width, img_height, (x, y, w, h))
            # 计算下一步舵机要转的角度
            next_btm_degree = track.btm_servo_control(offset_x)
            next_top_degree = track.top_servo_control(offset_y)
            # 舵机转动
            # TODO@libing:此处有next_btm_degree未赋值的bug
            arm_lamp.set_cloud_platform_degree(next_btm_degree, next_top_degree)
            # 更新角度值
            track.last_btm_degree = next_btm_degree
            track.last_top_degree = next_top_degree
            # print("X轴偏移量：{} Y轴偏移量：{}".format(offset_x, offset_y))
            # print('底部角度： {} 顶部角度：{}'.format(next_btm_degree, next_top_degree))
            
            count_noface = 0

        else:
            count_noface += 1
            if count_noface > 10: # 如果找不到人脸次数到10
                # 做一个低头的动作
                arm_lamp.do_bow_head()
                # 播放语音
                cmd = r"aplay /home/shunya/pilamp/etc/wav/fail.wav"
                os.system(cmd)
                
                time.sleep(3)  

                # 舵机转动
                arm_lamp.set_cloud_platform_degree(next_btm_degree, next_top_degree)
                time.sleep(2)
            
                count_noface = 0


        # 等待键盘事件
        key = cv2.waitKey(1)
        if key == ord('q'):
            # 退出程序
            break
        elif key == ord('r'):
            print('舵机重置')
            # 重置舵机
            # 最近一次底部舵机的角度值记录
            last_btm_degree = 100
            # 最近一次顶部舵机的角度值记录
            last_top_degree = 40
            # 舵机角度初始化
            arm_lamp.set_cloud_platform_degree(next_btm_degree, next_top_degree)

        listen()

    elif mode == 1:
        _, image = cap.read()
        _, image = cap.read()
        _, image = cap.read()
        _, image = cap.read()

        image, wrong_pose, exist_phone = detector.detect(image)

        cv2.namedWindow('result')
        cv2.imshow('result', cv2.resize(image, (640, 480)))
        if cv2.waitKey(1) == 27:
            break

        if exist_phone:
            print("***********************************************")
            print("*******Attention to study carefully************")
            print("***********************************************")
            detector.reset_phone()
            arm_lamp.do_shake_head()
            cmd = r"aplay /home/shunya/pilamp/etc/wav/phone.wav"
            os.system(cmd)

        if wrong_pose:  # 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
            print("***********************************************")
            print("*******Attention to sitting postur*************")
            print("***********************************************")
            detector.reset_pose()
            arm_lamp.do_shake_head()
            cmd = r"aplay /home/shunya/pilamp/etc/wav/pose.wav"
            os.system(cmd)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

        listen()



# 释放VideoCapture
cap.release()
# 关闭所有的窗口
cv2.destroyAllWindows()
