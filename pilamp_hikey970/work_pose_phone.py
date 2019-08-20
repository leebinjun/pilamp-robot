#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import time

import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

# 台灯机械臂arm_lamp
from pirobot.robot import Armbot
arm_lamp = Armbot(port=PORTNUM_ARMBOT)
from pose.vision import Handler
detector = Handler()

# 初始化工作姿态
arm_lamp.do_work_init_pos()

cap = cv2.VideoCapture(0)
cap.set(3, 320)  # set Width
cap.set(4, 240)  # set Height

while True:
    _, image = cap.read()
    _, image = cap.read()
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
        cmd = r"aplay ./etc/wav/phone.wav"
        os.system(cmd)

    if wrong_pose:  # 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
        print("***********************************************")
        print("*******Attention to sitting postur*************")
        print("***********************************************")
        detector.reset_pose()
        arm_lamp.do_shake_head()
        cmd = r"aplay ./etc/wav/pose.wav"
        os.system(cmd)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()

