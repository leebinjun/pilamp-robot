#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import os
import logging
from vision import Handler

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)  # set Width
    cap.set(4, 240)  # set Height
    detector = Handler()

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
            cmd = r"aplay phone.wav"
            os.system(cmd)

        if wrong_pose:  # 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
            print("***********************************************")
            print("*******Attention to sitting postur*************")
            print("***********************************************")
            detector.reset_pose()
            cmd = r"aplay pose.wav"
            os.system(cmd)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
