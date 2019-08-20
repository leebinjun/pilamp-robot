import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..//')

import cv2
import numpy as np
import tensorflow as tf
import time
from PIL import Image
from matplotlib.pylab import *

class HandDetect(object):
    classes = ['fist','five','one','yes']

    __bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    __es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    def __init__(self, modelDir = './handgesture/model/model.ckpt'):
        self.modelDir = modelDir
        self.saver = tf.train.import_meta_graph(modelDir+".meta")
        
        self.frameHand = None

    def detect(self, frame):
        self.frameHand = frame.copy()
        frame_roc = frame[100:400, 50:200, :] 

        # frame预处理
        fgmask = self.__bs.apply(frame_roc) # 背景分割器，该函数计算了前景掩码
        # 二值化阈值处理，前景掩码含有前景的白色值以及阴影的灰色值，在阈值化图像中，将非纯白色（244~255）的所有像素都设为0，而不是255
        th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
        # 下面就跟基本运动检测中方法相同，识别目标，检测轮廓，在原始帧上绘制检测结果
        dilated = cv2.dilate(th, self.__es, iterations=10) # 形态学膨胀
        image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
        # contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
        continue_flag = 0
        b, a, w = 999, 50, 200
        for c in contours:
            if cv2.contourArea(c) > 8000: #1600:
                (a, b, w, h) = cv2.boundingRect(c)
                # cv2.rectangle(frame_roc, (a, b), (a + w, b + 200), (255, 255, 0), 2)
        if b > 100:
            b = 100
        
        
        img_roc = th[b:b+200, a:a+w]
        # img_roc = frame_roc[b:b+200, a:a+w]
        img_roc_resize = cv2.resize(img_roc, (28, 28))
        
        # cv2.imshow('roc', img_roc_resize)
        cv2.imwrite("roc.jpg", img_roc_resize)
        filename = "roc.jpg"
        # Read image
        pil_im = array(Image.open(filename).convert('L').resize((28,28)),dtype=float32)
        #pil_im = (255-pil_im)/255.0
        pil_im = pil_im.reshape((1,28*28))

        with tf.Session() as sess:
            self.saver.restore(sess, self.modelDir)
            x = tf.get_default_graph().get_tensor_by_name("images:0")
            keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
            y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")

            # time1 = time.time()
            prediction = sess.run(y, feed_dict={x:pil_im, keep_prob: 1.0})
            index = np.argmax(prediction)
            # print("The classes is: %s. (the probability is %g)" % (self.classes[index], prediction[0][index]))
            # time2 = time.time()
            # print(f"Using time {time2-time1}")

            font = cv2.FONT_HERSHEY_SIMPLEX#使用默认字体
            # im=np.zeros((50,50,3),np.uint8) 
            img_result = cv2.putText(th,'%s (score = %.5f)' % 
                (self.classes[index], prediction[0][index]),(0,40), font,1.2,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细

            # cv2.imshow('thresh', th)
            # print(type(th))
            # print(th)
            # assert(th.shape() == (300,150,3))
            th2 = th[:, np.newaxis]
            th3 = np.concatenate((th2,th2,th2), axis=1)
            th4 = np.swapaxes(th3, axis1=1, axis2=2) 
            self.frameHand[100:400, 50:200, :] = th4
            # cv2.imshow('ret', self.frameHand)
    
    def show(self):
        cv2.imshow('ret', self.frameHand)


if __name__ == "__main__":

    hand_detect = HandDetect()

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()

    while ret:
        ret, img = cap.read()

        hand_detect.detect(img)
        hand_detect.show()

        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
