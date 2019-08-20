import multiprocessing as mp
import cv2
import time
import numpy as np
import tensorflow as tf
from PIL import Image
from matplotlib.pylab import *
 

def job0(frame_queue, b):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        f = frame.copy()
        frame_queue.put(f)
        print("job0000000")

        cv2.rectangle(frame, (50, 100), (200, 400), (255, 255, 0), 2)
        cv2.imshow("cam", frame)
        
        key = cv2.waitKey(1)
        # 按'q'健退出循环
        if key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()


def detectFaceOpenCVDnn(net, frame):
    conf_threshold = 0.7

    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

def job1(frame_queue, b):
    print("face detect")
    
    modelFile = "./face/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "./face/models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

    
    frame_count = 0
    tt_opencvDnn = 0

    while(1):
        if frame_queue.empty():
            cv2.waitKey(1)
            continue
        
        frame = frame_queue.get()
        print("job1111111111")
        frame_count += 1

        t = time.time()
        outOpencvDnn, bboxes = detectFaceOpenCVDnn(net,frame)
        tt_opencvDnn += time.time() - t
        fpsOpencvDnn = frame_count / tt_opencvDnn
        label = "FPS : {:.2f}".format(fpsOpencvDnn)
        cv2.putText(outOpencvDnn, label, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Face Detection", outOpencvDnn)

        if frame_count == 1:
            tt_opencvDnn = 0

        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break


def job2(frame_queue, b):
    print("open pose")

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
    parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
    parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
    parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')

    args = parser.parse_args()

    BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

    POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

    inWidth = args.width
    inHeight = args.height

    net = cv2.dnn.readNetFromTensorflow(".\pose\graph_opt.pb")


    while cv2.waitKey(1) < 0:
        
        if frame_queue.empty():
            cv2.waitKey(1)
            continue
        
        frame = frame_queue.get()
        print("job2222222222")

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        
        net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

        assert(len(BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(BODY_PARTS)):
            # Slice heatmap of corresponging body's part.
            heatMap = out[0, i, :, :]

            # Originally, we try to find all the local maximums. To simplify a sample
            # we just find a global one. However only a single pose at the same time
            # could be detected this way.
            _, conf, _, point = cv2.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]
            # Add a point if it's confidence is higher than threshold.
            points.append((int(x), int(y)) if conf > args.thr else None)

        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:
                cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        t, _ = net.getPerfProfile()
        freq = cv2.getTickFrequency() / 1000
        cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv2.imshow('OpenPose using OpenCV', frame)

        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break


def job3(frame_queue, b):
    # model
    classes = ['fist','five','one','yes']
    model_dir = './handgesture/model/model.ckpt'
    saver = tf.train.import_meta_graph(model_dir+".meta")

    with tf.Session() as sess:
        saver.restore(sess, model_dir)
        x = tf.get_default_graph().get_tensor_by_name("images:0")
        keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
        y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")

        bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        while True:
                
            img = frame_queue.get()
            print("job33333333")
            img = img[100:400,50:200, :] 
            fgmask = bs.apply(img) # 背景分割器，该函数计算了前景掩码
            # 二值化阈值处理，前景掩码含有前景的白色值以及阴影的灰色值，在阈值化图像中，将非纯白色（244~255）的所有像素都设为0，而不是255
            th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
            # 下面就跟基本运动检测中方法相同，识别目标，检测轮廓，在原始帧上绘制检测结果
            dilated = cv2.dilate(th, es, iterations=10) # 形态学膨胀
            image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
            # rasp
            # contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
            continue_flag = 0
            for c in contours:
                if cv2.contourArea(c) > 8000: #1600:
                    (a, b, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(img, (a, b), (a + w, b + 200), (255, 255, 0), 2)
                
            # print(time.time())
            img_roc = th[b:b+200, a:a+w]
            img_roc_resize = cv2.resize(img_roc, (28, 28))
            # print(img_roc_resize.shape)
            cv2.imwrite("roc.jpg", img_roc_resize)
            filename = "roc.jpg"
            # Read image
            pil_im = array(Image.open(filename).convert('L').resize((28,28)),dtype=float32)
            #pil_im = (255-pil_im)/255.0
            pil_im = pil_im.reshape((1,28*28))
        
            time1 = time.time()
            prediction = sess.run(y, feed_dict={x:pil_im, keep_prob: 1.0})
            index = np.argmax(prediction)
            time2 = time.time()
            print("The classes is: %s. (the probability is %g)" % (classes[index], prediction[0][index]))
            print("Using time %g" % (time2-time1))

            font=cv2.FONT_HERSHEY_SIMPLEX#使用默认字体
            # im=np.zeros((50,50,3),np.uint8) 
            img_result=cv2.putText(img,'%s (score = %.5f)' % 
                (classes[index], prediction[0][index]),(0,40), font,1.2,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细

            # cv2.imshow('mog', fgmask)
            cv2.imshow('thresh', th)
            # cv2.imshow('detection', img)
            cv2.imshow('ret', img_result)

            key = cv2.waitKey(500) & 0xFF
            # 按'q'健退出循环
            if key == ord('q'):
                break


def job4(frame_queue, b):
    # Labels of Network.
    classNames = { 0: 'background',
        1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
        5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
        10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
        14: 'motorbike', 15: 'person', 16: 'pottedplant',
        17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

    #Load the Caffe model 
    # net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)
    prototxt = r".\ssd\MobileNetSSD_deploy.prototxt"
    weights = r".\ssd\MobileNetSSD_deploy.caffemodel"
    net = cv2.dnn.readNetFromCaffe(prototxt, weights)

    while True:
        # Capture frame-by-frame
        if frame_queue.empty():
            continue
        frame = frame_queue.get()
        frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

        # MobileNet requires fixed dimensions for input image(s)
        # so we have to ensure that it is resized to 300x300 pixels.
        # set a scale factor to image because network the objects has differents size. 
        # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
        # after executing this command our "blob" now has the shape:
        # (1, 3, 300, 300)
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        net.setInput(blob)
        #Prediction of network
        detections = net.forward()

        #Size of frame resize (300x300)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        #For get the class and location of object detected, 
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > 0.2: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                            (0, 255, 0))

                # Draw label and confidence of prediction in frame resized
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                        (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                        (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    print(label) #print class and confidence

        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        
        key = cv2.waitKey(100) & 0xFF
        # 按'q'健退出循环
        if key == ord('q'):
            break

if __name__ == "__main__":
    
    frame_queue = mp.Queue(5)
    p0 = mp.Process(target = job0, args = (frame_queue,2))
    p1 = mp.Process(target = job1, args = (frame_queue,2))
    p2 = mp.Process(target = job2, args = (frame_queue,2))
    p3 = mp.Process(target = job3, args = (frame_queue,2))
    p4 = mp.Process(target = job4, args = (frame_queue,2))

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # p1.join()
    # p2.join()


