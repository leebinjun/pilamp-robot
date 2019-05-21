import multiprocessing as mp
import cv2
import time
import numpy as np
import tensorflow as tf
from PIL import Image, ImageTk
from matplotlib.pylab import *
import tkinter as tk

from face.face import FaceDetect
from pose.pose import PoseDetect
from ssd.ssd import SSDDetect
from handgesture.hand import HandDetect

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

def job1(frame_queue, fq):
    print("face detect")
    
    face_detect = FaceDetect()

    while True:
        if frame_queue.empty():
            cv2.waitKey(1)
            continue

        frame = frame_queue.get()
        print("job1111111111")
        
        face_detect.detect(frame)
        face_detect.show()
 
        key = cv2.waitKey(100)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def job2(frame_queue, b):
    print("open pose")

    pose_detect = PoseDetect()

    while True:
        if frame_queue.empty():
            cv2.waitKey(1)
            continue

        frame = frame_queue.get()
        print("job22222222222")
        
        pose_detect.detect(frame)
        pose_detect.show()
 
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def job3(frame_queue, b):
    print("handgesture detect")

    hand_detect = HandDetect()

    while True:
        if frame_queue.empty():
            cv2.waitKey(1)
            continue

        frame = frame_queue.get()
        print("job3333333333")

        hand_detect.detect(frame)
        hand_detect.show()

        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def job4(frame_queue, fq4):
    print("SSD")
     
    ssd_detect = SSDDetect()

    while True:
        if frame_queue.empty():
            cv2.waitKey(1)
            continue

        frame = frame_queue.get()
        print("job4444444444444")

        ssd_detect.detect(frame)
        ssd_detect.show()

        
        key = cv2.waitKey(10)
        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def job5(fq0, fq1, fq2, fq3, fq4):
    root = tk.Tk()
    root.title("GUI")
    root.geometry("840x730")
    
    imgLabel4 = tk.Label(root)
    # imgLabel4.grid(row=0, column=0, sticky=tk.E)
    imgLabel4.pack()
    print("aaaaaaaaaaaaaaa")

    def func1():
        cv2.waitKey(10)
        if not fq1.empty():
            print("bbbbbbbbb")
            frame = fq1.get()
            img4 = Image.fromarray(frame) #将图像转换成Image对象
            photo4 = ImageTk.PhotoImage(img4)
            imgLabel4.photo4 = photo4
            imgLabel4.config(image = photo4)
            root.after(1, func1) # 一段时间后执行video_loop()函数
        else:
            print("!!!!!!!!")
            root.after(1, func1) # 一段时间后执行video_loop()函数

    func1()
    root.mainloop()

if __name__ == "__main__":
    
    
    frame_queue = mp.Queue(5)
    fq4 = mp.Queue(5)
    fq1 = mp.Queue(5)

    p0 = mp.Process(target = job0, args = (frame_queue,2))
    p1 = mp.Process(target = job1, args = (frame_queue, fq1))
    p2 = mp.Process(target = job2, args = (frame_queue,2))
    p3 = mp.Process(target = job3, args = (frame_queue,2))
    p4 = mp.Process(target = job4, args = (frame_queue, fq4))
    # p5 = mp.Process(target = job5, args = (0, fq1, 2, 3, fq4))


    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    # p5.start()



