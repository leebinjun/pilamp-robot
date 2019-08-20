#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################


import cv2
import argparse
import numpy as np

classes_file = r"objectdetect-yolo\yolov3.txt"
with open(classes_file, 'r') as f:
    classes = [line.strip() for line in f.readlines()]


COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


class YOLODetect(object):


    def __init__(self,
                 configs = r"objectdetect-yolo\yolov3-tiny.cfg", 
                 weights = r"objectdetect-yolo\yolov3-tiny.weights"
                 ):
        self.configs = configs
        self.weights = weights

        self.net = cv2.dnn.readNetFromDarknet(self.configs, self.weights)
        
        self.frameYOLO = None
    
    def detect(self, frame):
        self.frameYOLO = frame.copy()

        Width = frame.shape[1]
        Height = frame.shape[0]
        scale = 0.006 #0.006

        blob = cv2.dnn.blobFromImage(self.frameYOLO, scale, (416,416), (0,0,0), True, crop=False)

        self.net.setInput(blob)

        outs = self.net.forward(get_output_layers(self.net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.01
        nms_threshold = 0.4


        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])


        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_prediction(self.frameYOLO, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

        # cv2.imshow("object detection", self.frameYOLO)
        # cv2.waitKey()
            
        # cv2.imwrite("object-detection.jpg", self.frameYOLO)
        # cv2.destroyAllWindows()

    def show(self):
        cv2.imshow("frame", self.frameYOLO)



if __name__ == "__main__":

    yolo_detect = YOLODetect()

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()

    while ret:
        ret, img = cap.read()

        yolo_detect.detect(img)
        yolo_detect.show()

        
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()





