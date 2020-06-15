#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import time
import dlib
import sys

sys.path.append("./pose/Pose")
sys.path.append("./pose")
import common
from estimator import FluidPoseEstimator


class Handler(object):
    def __init__(self):
        super().__init__()
        self.detector = dlib.simple_object_detector("./pose/bj_detector.svm")
        self.e = FluidPoseEstimator(graph_path="./params", target_size=(432, 368))
        self.fps_time = 0
        self.result = None
        # 和姿态检测有关的变量
        # 原理： 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
        self.count_rightpose = 0  # 计数器
        self.zero_pos = None  # 头部位置
        self.threshold_rightpose = 40  # 偏离距离阈值
        self.phone_count = 0

    def reset_pose(self):
        self.count_rightpose = 0

    def reset_phone(self):
        self.phone_count = 0

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 1)
        humans = self.e.inference(image)

        # 画人体姿态图
        image_h, image_w = image.shape[:2]
        centers = {}
        for human in humans[:1]:  # 只取第一个人
            # draw point
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue
                body_part = human.body_parts[i]
                center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                centers[i] = center
                # print(body_part)
                cv2.circle(image, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
            # draw line
            for pair_order, pair in enumerate(common.CocoPairsRender):
                if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                    continue
                cv2.line(image, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)

        # 标记帧率
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - self.fps_time)),
                    (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        # 框取手机
        for k, d in enumerate(rects):
            cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)

        self.fps_time = time.time()

        # 判读坐姿是否正确
        if 0 in centers:
            if self.zero_pos is None:
                self.zero_pos = centers[0]
            print("[Position Detector] head pos:", centers[0])
            print("[Position Detector] zero pos:", self.zero_pos)
            if abs(centers[0][0] - self.zero_pos[0]) + abs(centers[0][1] - self.zero_pos[1]) > self.threshold_rightpose:  # 如果偏离得太远
                self.count_rightpose += 1
            else:  # 否则计数清零
                self.count_rightpose = 0
        else:  # 检测不到也算错误姿势
            self.count_rightpose += 1

        # 判断是否在玩手机
        if len(rects) > 0:
            self.phone_count += 1
        else:
            if self.phone_count > 0:
                self.phone_count = 0

        # 结果
        print("[Phone    Detector] Found " + str(len(rects)) + " Phone.")
        print("[Position Reportor] count_rightpose:", self.count_rightpose)

        return image, self.count_rightpose > 10, self.phone_count > 5
