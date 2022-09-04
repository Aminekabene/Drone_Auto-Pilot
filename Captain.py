import cv2
from Model import Yolo
import numpy as np

cap = cv2.VideoCapture(0)
yolo = Yolo()
pErrors=[0,0,0,0]
fb_range= (40,50)
pid = [0.5,0.5,0]
x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0


def trackObject(x, y, area_ratio, img, pErrors):
    h, w, _ = img.shape
    front_error, back_error, lfrt_error, updw_error= 0,0,0,0

    # Correcting speed for front and backward movements
    if area_ratio > fb_range[0] and area_ratio < fb_range[1]:
        fb = 0
    elif area_ratio < fb_range[0]:
        front_error = fb_range[0] - area_ratio
        fb = pid[0] * front_error + pid[1] * (front_error - pErrors[0])
        fb = int(np.clip(fb, -100, 100))
    elif area_ratio > fb_range[1]:
        back_error = fb_range[1] - area_ratio
        fb = pid[0] * back_error + pid[1] * (back_error - pErrors[1])
        fb = int(np.clip(fb, -100, 100))

    # Correcting speed for left and right movements
    if x == 0:
        lfrt = 0
    else:
        lfrt_error = x - w // 2
        lfrt = pid[0] * lfrt_error + pid[1] * (lfrt_error - pErrors[2])
        lfrt = int(np.clip(lfrt, -100, 100))

    # Correction seep for up and down movements
    if y == 0:
        updw = 0
    else:
        updw_error = y - h // 2
        updw = pid[0] * updw_error + pid[1] * (updw_error - pErrors[3])
        updw = int(np.clip(updw, -100, 100))

    print("Front & back speed: " + str(fb) + ", Left & Right speed: " + str(
        lfrt) + ", Up & Down speed: " + str(updw))

    return front_error, back_error, lfrt_error, updw_error



while True:
    ret, img = cap.read()

    if ret == True:

        labels, cords = yolo.ComputeDetections(img)
        yolo.emptyObjects()
        yolo.StoreInstanceOfObjs(labels,cords)
        img = yolo.PlotBoxes(img)

        with open('./helper/TrackCommands.txt') as f:
            lines = f.readlines()

        if len(lines) != 0:
            command = lines[0].split()
            classname= command[0]
            instanceId= int(command[1])
            x1, y1, x2, y2 = yolo.getcordOfObj(classname, instanceId, img) #*** should return 0 if no object found
            xc, yc = yolo.findCenter(x1, y1, x2, y2)
            areaRatio= yolo.ComputeAreaObjRatio(x1, y1, x2, y2,img)

            pErrors= trackObject(xc,yc,areaRatio,img,pErrors)
            print("Area Ratio: "+ str(areaRatio))

            cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
            cv2.circle(img, (int(xc),int(yc)), 5, (0,0,255), 5)


        cv2.imshow("Object Detections",img)

        if cv2.waitKey(1)== 13:
            break
