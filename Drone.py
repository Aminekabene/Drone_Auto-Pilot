import torch
import cv2
from djitellopy import tello
from time import sleep
from Model import Yolo

cap = cv2.VideoCapture(0)
yolo = Yolo()

while True:
    ret, img = cap.read()

    if ret == True:

        labels, cords = yolo.ComputeDetections(img)
        yolo.emptyObjects()
        yolo.StoreInstanceOfObjs(labels,cords)
        img = yolo.PlotBoxes(img)
        cv2.imshow("Object Detections",img)

        if cv2.waitKey(1)== 13:
            break

