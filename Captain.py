import cv2
from Model import Yolo
from Drone import Drone

yolo = Yolo()
mydrone = Drone()
pErrors=[0,0,0,0]

mydrone.me.takeoff()


while True:
    img = mydrone.getImage()

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
        Drone.x1, Drone.y1, Drone.x2, Drone.y2 = yolo.getcordOfObj(classname, instanceId, img) # returns 0 if no object found
        xc, yc = yolo.findCenter(Drone.x1, Drone.y1, Drone.x2, Drone.y2)
        areaRatio= yolo.ComputeAreaObjRatio(Drone.x1, Drone.y1, Drone.x2, Drone.y2,img)

        pErrors= mydrone.trackObject(xc,yc,areaRatio,img,pErrors)
        print("Area Ratio: "+ str(areaRatio))

        cv2.rectangle(img, (Drone.x1, Drone.y1), (Drone.x2, Drone.y2), (0,0,255), 2)
        cv2.circle(img, (int(xc),int(yc)), 5, (0,0,255), 5)

    cv2.imshow("Object Tracking",img)

    if cv2.waitKey(1)== 13:
        mydrone.stop()
        break
