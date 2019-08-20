from __future__ import division
import cv2
import time
import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..//')

class FaceDetect(object):
    conf_threshold = 0.7

    def __init__(self, 
                 configFile = "./face/models/deploy.prototxt", 
                 modelFile = "./face/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"):
        self.modelFile = modelFile
        self.configFile = configFile
        self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        self.frameOpencvDnn = None

    def detect(self, frame):
        self.frameOpencvDnn = frame.copy()
        frameHeight = self.frameOpencvDnn.shape[0]
        frameWidth = self.frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(self.frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

        self.net.setInput(blob)
        detections = self.net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv2.rectangle(self.frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)

    def show(self):
        cv2.imshow("FaceDetect", self.frameOpencvDnn)


if __name__ == "__main__" :

    face_detect = FaceDetect()

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    while ret:
        ret, img = cap.read()

        face_detect.detect(img)
        face_detect.show()
 
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
