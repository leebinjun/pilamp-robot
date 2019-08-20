import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
sys.path.append(r".\face")

import numpy as np
import dlib
import cv2
import argparse
from face.image_utility import save_image, generate_random_color, draw_border
from imutils import face_utils, video


class FaceDetect(object):
    conf_threshold = 0.7

    def __init__(self, 
                 configFile = './face/shape_predictor_68_face_landmarks.dat'):
       
        self.predictor = dlib.shape_predictor(configFile)
        self.T = 0.6
        self.detector = dlib.get_frontal_face_detector()       
       
       
        # self.modelFile = modelFile
        # self.configFile = configFile
        # self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        self.frameHOG = None

    def detect(self, image, gray):
        (img_h, img_w) = image.shape[:2]
        cv2.putText(image, "HOG method", (img_w - 200, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (205, 92, 92), 2)
        # Get faces into webcam's image
        rects = self.detector(gray, 0)
        
        index = -1 # 记录最终返回的脸序号
        max_face = [] # 格式 [x1, y1, w, h] img中面积最大的人脸
        # For each detected face, find the landmark.
        for (i, rect) in enumerate(rects):
            # Finding points for rectangle to draw on face
            x1, y1, x2, y2, w, h = rect.left(), rect.top(), rect.right() + \
                1, rect.bottom() + 1, rect.width(), rect.height()
            # cv2.rectangle(image, (x1, y1), (x1 + w, y1 + h), (205, 92, 92), 2)
            
            if i == 0:
                index = 0
                max_face = [x1, y1, w, h]
            if i > 0: # 如果多于一张人脸
                if w*h > max_face[2]*max_face[3]:
                    index = i
                    max_face = [x1, y1, w, h]

        if len(max_face) == 0:  # 如果没有检测到脸
            return None 
        (x, y, w, h) = max_face  
        if w < 10 or h < 10:
            return None  
            
        # 画图标记
        draw_border(image, (x, y), (x+w, y+h), (205, 92, 92), 2, 10, 20)
        # show the face number
        cv2.putText(image, "Hello #{}".format(index + 1), (x1 - 20, y1 - 20),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.6, (205, 92, 92), 2)
        # Make the prediction and transfom it to numpy array
        shape = self.predictor(gray, rects[index])
        shape = face_utils.shape_to_np(shape)
        # Draw on our image, all the finded cordinate points (x,y)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        # 返回面积最大的人脸坐标
        return max_face 

    def show(self, image):
        # show the output frame
        # adding brightness and contrast -> α⋅p(i,j)+β where p(i.j) is pixel value for each point
        image = cv2.convertScaleAbs(image, alpha=1.0, beta=0)
        cv2.imshow("Facial Landmarks", cv2.resize(image, (640, 480)))


if __name__ == "__main__" :

    face_detect = FaceDetect()

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    while ret:
        ret, img = cap.read()
        
        # Converting the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_detect.detect(img, gray)
        face_detect.show(img)
 
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()





















