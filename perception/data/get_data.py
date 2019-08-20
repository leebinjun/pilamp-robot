import cv2
import time


cap = cv2.VideoCapture(0)
ret, img = cap.read()

while ret:
    ret, img = cap.read()
    cv2.imshow("", img)
    
    k = cv2.waitKey(10)
    if k == ord("q"):
        break

    if k == ord("s"):
        file_name = './data/a' + str(time.time()) + ".jpg"
        cv2.imwrite(file_name, img)














