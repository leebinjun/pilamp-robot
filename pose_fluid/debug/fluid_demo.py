from paddle import fluid
import sys
import cv2
import paddle
import numpy as np
from Pose.estimator import FluidPoseEstimator
import Pose.common as common

sys.path.append("./Pose")
e = FluidPoseEstimator(graph_path = "./params", target_size=(432,368))
#image = cv2.imread("C:\\Users\\Bye_l\\Desktop\\tim.jpg")
cap = cv2.VideoCapture(0)
#humans = e.inference(image)
while True:
    # Detect
    _, image = cap.read()
    humans = e.inference(image)
    image_h, image_w = image.shape[:2]
    centers = {}
    for human in humans[:1]:  # 只取第一个人
        # draw point
        for i in range(common.CocoPart.Background.value):
            if i not in human.body_parts.keys():
                continue
            body_part = human.body_parts[i]
            center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            centers[i] = center
            # print(body_part)
            cv2.circle(image, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
        # draw line
        for pair_order, pair in enumerate(common.CocoPairsRender):
            if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                continue
            cv2.line(image, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
    cv2.imshow("frame", image)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
#cv2.imwrite("test.jpg", image)
