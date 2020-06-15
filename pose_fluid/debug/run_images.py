#! /usr/bin/python3
# -*- coding: utf-8 -*- 

from Pose import pose_utils

import numpy as np
import cv2
import time
import base64


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
e = TfPoseEstimator(get_graph_path(args.model), target_size=(1080, 1920))
logger.debug('cam read+')
# cam = cv2.VideoCapture(args.camera)
# ret_val, image = cap.read()
# logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))



None_img = np.array([0, 0.5, 1], dtype=float)
num_photo = 0                 # num of photo
time_last = int(time.time())
open_time = int(time.time())       # flag avoid contiu open
 




if __name__ == "__main__":
    
    import os
    for filename in os.listdir(r"./file"):              #listdir的参数是文件夹的路径
        # ret_val, image = cap.read()
        file_path = ".\\file\\" + filename
        print(file_path)     
        image = cv2.imread(file_path, -1)
        #使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
        # print("s",image_p.shape)
        # image = cv2.resize(image_p, (320,240))
        print(image.shape)
        cv2.imshow('resultss', image)


        logger.debug('image preprocess+')
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

        logger.debug('image process+')
        humans = e.inference(image)

        logger.debug('postprocess+')
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        # for human in humans:
        #     print("human:", human)
        #     print("human.body_parts:", human.body_parts)
 
        # print body key point info.
        image_h, image_w = image.shape[:2]
        centers = {}
        for human in humans:
            # draw point
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue
                body_part = human.body_parts[i]
                center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                centers[i] = center
                # print(body_part)
                # cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
        print(centers)


        logger.debug('show+')
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.namedWindow('result')  
        cv2.imshow('result', image)
        cv2.imwrite('rst'+filename, image)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        logger.debug('finished+')

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    
    
    cap.release()
    cv2.destroyAllWindows()









