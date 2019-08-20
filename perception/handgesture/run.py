import sys, os
sys.path.append(os.path.dirname(__file__) + os.sep + '..//')

import cv2
import numpy as np
import tensorflow as tf
import time
from PIL import Image
from matplotlib.pylab import *


# model
classes = ['fist','five','one','yes']
model_dir = './handgesture/model/model.ckpt'
saver = tf.train.import_meta_graph(model_dir+".meta")

with tf.Session() as sess:
    saver.restore(sess, model_dir)
    x = tf.get_default_graph().get_tensor_by_name("images:0")
    keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
    y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")

    cap = cv2.VideoCapture(0) # 参数0表示第一个摄像头
    # cap.set(3, 240)
    # cap.set(4, 320)

    bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    while True:
            
        ret, img = cap.read()
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

        key = cv2.waitKey(1) & 0xFF
        # 按'q'健退出循环
        if key == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
