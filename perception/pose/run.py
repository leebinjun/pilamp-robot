#! /usr/bin/python3
# -*- coding: utf-8 -*- 

from Pose import pose_utils

import numpy as np
import cv2
import time
import base64


cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height


import sys
sys.path.append("./Pose")

import argparse
import logging
import time

import common

from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
parser.add_argument('--camera', type=int, default=0)
parser.add_argument('--zoom', type=float, default=1.0)
parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
parser.add_argument('--show-process', type=bool, default=False,
                    help='for debug purpose, if enabled, speed for inference is dropped.')
parser.add_argument('--serial', type=str, default='COM6')                   
args = parser.parse_args()

logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
w, h = model_wh(args.resolution)
e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
logger.debug('cam read+')
# cam = cv2.VideoCapture(args.camera)
ret_val, image = cap.read()
logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))


None_img = np.array([0, 0.5, 1], dtype=float)
num_photo = 0                 # num of photo
time_last = int(time.time())
open_time = int(time.time())       # flag avoid contiu open
 

# 和姿态检测有关的变量
# 原理： 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
count_rightpose = 0        # 计数器
zero_pos = None            # 头部位置
threshold_rightpose = 100  # 偏离距离阈值

if __name__ == "__main__":
    
    while True:

        ret_val, image = cap.read()
        ret_val, image = cap.read()
        # logger.debug('image preprocess')
        if args.zoom < 1.0:
            canvas = np.zeros_like(image)
            img_scaled = cv2.resize(image, None, fx=args.zoom, fy=args.zoom, interpolation=cv2.INTER_LINEAR)
            dx = (canvas.shape[1] - img_scaled.shape[1]) // 2
            dy = (canvas.shape[0] - img_scaled.shape[0]) // 2
            canvas[dy:dy + img_scaled.shape[0], dx:dx + img_scaled.shape[1]] = img_scaled
            image = canvas
        elif args.zoom > 1.0:
            dx = (img_scaled.shape[1] - image.shape[1]) // 2
            dy = (img_scaled.shape[0] - image.shape[0]) // 2
            image = img_scaled[dy:image.shape[0], dx:image.shape[1]]

        # logger.debug('image process')
        humans = e.inference(image)

        # logger.debug('postprocess')
        
        # image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        # print("humans:", humans)
        # for human in humans:
        #     print("humans[0]:", humans[0])
        #     print("human:", human)
        #     print("human.body_parts:", human.body_parts)
 
        # print body key point info.
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



        # logger.debug('show')
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.namedWindow('result')  
        cv2.imshow('result', cv2.resize(image, (640, 480)))
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        
        # logger.debug('data process')
        # print("centers:", centers)
             

        if 0 in centers:
            if zero_pos == None:
                zero_pos = centers[0]
            print("head pos:", centers[0])
            print("zero pos:", zero_pos)
            if abs(centers[0][0] - zero_pos[0]) + abs(centers[0][1] - zero_pos[1]) > threshold_rightpose:  # 如果偏离得太远
                count_rightpose += 1
            else: # 否则计数清零
                count_rightpose = 0 
        else: # 检测不到也算错误姿势
            count_rightpose += 1
            
        print("count_rightpose:", count_rightpose)
        if count_rightpose > 10:  # 不能检测到头部次数 或 偏离起始位置距离大于阈值次数 到达一定次数时，认为姿态不正确。
            print("***********************************************")
            print("*******Attention to sitting postur*************")
            print("***********************************************")
            count_rightpose = 0

        # logger.debug('finished+')

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    
    
    cap.release()
    cv2.destroyAllWindows()









