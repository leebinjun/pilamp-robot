from __future__ import division
# -*- coding:utf-8 -*-
'''
'''

import time

import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from face.face_detection_hog import FaceDetect

class Tracker(object):

    last_btm_degree = 100 # 最近一次底部舵机的角度值记录
    last_top_degree = 40 # 最近一次顶部舵机的角度值记录

    btm_kp = 10 # 底部舵机的Kp系数
    top_kp = 10 # 顶部舵机的Kp系数

    offset_dead_block = 0.2 # 设置偏移量的死区


    def btm_servo_control(self, offset_x):
        '''
        底部舵机的比例控制
        这里舵机使用开环控制
        '''
        # global offset_dead_block # 偏移量死区大小
        # global btm_kp # 控制舵机旋转的比例系数
        # global last_btm_degree # 上一次底部舵机的角度
        
        # 设置最小阈值
        if abs(offset_x) < self.offset_dead_block:
            offset_x = 0

        # offset范围在-50到50左右
        delta_degree = offset_x * self.btm_kp
        # 计算得到新的底部舵机角度
        next_btm_degree = self.last_btm_degree + delta_degree
        # 添加边界检测
        if next_btm_degree < 0:
            next_btm_degree = 0
        elif next_btm_degree > 180:
            next_btm_degree = 180
        
        return int(next_btm_degree)

    def top_servo_control(self, offset_y):
        '''
        顶部舵机的比例控制
        这里舵机使用开环控制
        '''
        # global offset_dead_block
        # global top_kp # 控制舵机旋转的比例系数
        # global last_top_degree # 上一次顶部舵机的角度

        # 如果偏移量小于阈值就不相应
        if abs(offset_y) < self.offset_dead_block:
            offset_y = 0

        # offset_y *= -1
        # offset范围在-50到50左右
        delta_degree = offset_y * self.top_kp
        # 新的顶部舵机角度
        next_top_degree = self.last_top_degree + delta_degree
        # 添加边界检测
        if next_top_degree < 0:
            next_top_degree = 0
        elif next_top_degree > 180:
            next_top_degree = 180
        
        return int(next_top_degree)



    def calculate_offset(self, img_width, img_height, face):
        '''
        计算人脸在画面中的偏移量
        偏移量的取值范围： [-1, 1]
        '''
        (x, y, w, h) = face
        face_x = float(x + w/2.0)
        face_y = float(y + h/2.0)
        # 人脸在画面中心X轴上的偏移量
        offset_x = float(face_x / img_width - 0.5) * 2
        # 人脸在画面中心Y轴上的偏移量
        offset_y = float(face_y / img_height - 0.5) * 2

        return (offset_x, offset_y)



if __name__ == "__main__":
    
    import cv2
    import time

    import sys, os
    sys.path.append(os.path.dirname(__file__) + os.sep + '../')

    # 人脸检测face_detect
    from face.face_detection_hog import FaceDetect
    face_detect = FaceDetect()
    # 台灯机械臂arm_lamp
    from pirobot.robot import Armbot
    arm_lamp = Armbot()
    # 跟随计算track
    track = Tracker()

    # USB摄像头
    cap = cv2.VideoCapture(0)
    
    # 舵机角度初始化
    arm_lamp.set_cloud_platform_degree(track.last_btm_degree, track.last_top_degree)

    while cap.isOpened():
        # TODO 阅读最后一帧
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
            arm_lamp.set_cloud_platform_degree(next_btm_degree, next_top_degree)
            # 更新角度值
            track.last_btm_degree = next_btm_degree
            track.last_top_degree = next_top_degree
            print("X轴偏移量：{} Y轴偏移量：{}".format(offset_x, offset_y))
            print('底部角度： {} 顶部角度：{}'.format(next_btm_degree, next_top_degree))
        
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

    # 释放VideoCapture
    cap.release()
    # 关闭所有的窗口
    cv2.destroyAllWindows()
