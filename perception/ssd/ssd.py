import numpy as np
import cv2 

# Labels of Network.
ClassNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }


class SSDDetect(object):
    conf_threshold = 0.2

    def __init__(self,
                 prototxt = "./ssd/MobileNetSSD_deploy.prototxt",
                 weights = "./ssd/MobileNetSSD_deploy.caffemodel"):
        self.prototxt = prototxt
        self.weights  = weights
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.weights)

        self.frameSSD = None

    def detect(self, frame):
        self.frameSSD = frame.copy()
        frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction
        
        # MobileNet requires fixed dimensions for input image(s)
        # so we have to ensure that it is resized to 300x300 pixels.
        # set a scale factor to image because network the objects has differents size. 
        # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
        # after executing this command our "blob" now has the shape:
        # (1, 3, 300, 300)
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        self.net.setInput(blob)
        #Prediction of network
        detections = self.net.forward()

        #Size of frame resize (300x300)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        #For get the class and location of object detected, 
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > self.conf_threshold: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = self.frameSSD.shape[0]/300.0  
                widthFactor = self.frameSSD.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(self.frameSSD, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                            (0, 255, 0))

                # Draw label and confidence of prediction in frame resized
                if class_id in ClassNames:
                    label = ClassNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(self.frameSSD, (xLeftBottom, yLeftBottom - labelSize[1]),
                                        (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                        (255, 255, 255), cv2.FILLED)
                    cv2.putText(self.frameSSD, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    print(label) #print class and confidence
        

    def show(self):
        cv2.imshow("frame", self.frameSSD)


if __name__ == "__main__":
    
    ssd_detect = SSDDetect()

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()

    while ret:
        ret, img = cap.read()

        ssd_detect.detect(img)
        ssd_detect.show()

        
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

  



    
