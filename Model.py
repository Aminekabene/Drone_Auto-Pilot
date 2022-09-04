import torch
import cv2

"""
 This class will allow us to easily load and run a pretrained yolov5 model on inferences
"""
class Yolo:

    def __init__(self):
        """
        Initiating all needed variables
        :param img: Image on which the model should run its predictions

        objects: stores the instances of each objects detetected ex: if 2 persons is detected there will be 2 entries
        under the key 0 that will point to the unique instanceId of each person and their coordinates.

        classes: Stores the classes names in order.
        """

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        self.model.to(self.device)
        self.objects={ 0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}, 13: {}, 14: {}, 15: {}, 16: {}, 17: {}, 18: {}, 19: {}, 20: {}, 21: {},
                       22: {}, 23: {}, 24: {}, 25: {}, 26: {}, 27: {}, 28: {}, 29: {}, 30: {}, 31: {}, 32: {}, 33: {}, 34: {}, 35: {}, 36: {}, 37: {}, 38: {}, 39: {}, 40: {}, 41: {}, 42: {}, 43: {}, 44: {},
                       45: {}, 46: {}, 47: {}, 48: {}, 49: {}, 50: {}, 51: {}, 52: {}, 53: {}, 54: {}, 55: {}, 56: {}, 57: {}, 58: {}, 59: {}, 60: {}, 61: {}, 62: {}, 63: {}, 64: {}, 65: {}, 66: {}, 67: {},
                       68: {}, 69: {}, 70: {}, 71: {}, 72: {}, 73: {}, 74: {}, 75: {}, 76: {}, 77: {}, 78:{}, 79: {}
                       }
        with open('./helper/coco.names', 'r') as f:
            self.classes = f.read().splitlines()

    def ComputeDetections(self,img):
        """
        Compute The predictions of the model given a sprecifc image.
        :return: returns the labels and cordinates of each object detected
        """

        results = self.model(img)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels,cords

    def emptyObjects(self):
        """
        ***This function must be called before running the model on a new image.***
        Empties the Objects Dictionary, so that it does not store the objects detected in the previous image.

        """
        self.objects = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {},
                        13: {}, 14: {}, 15: {}, 16: {}, 17: {}, 18: {}, 19: {}, 20: {}, 21: {},
                        22: {}, 23: {}, 24: {}, 25: {}, 26: {}, 27: {}, 28: {}, 29: {}, 30: {}, 31: {}, 32: {}, 33: {},
                        34: {}, 35: {}, 36: {}, 37: {}, 38: {}, 39: {}, 40: {}, 41: {}, 42: {}, 43: {}, 44: {},
                        45: {}, 46: {}, 47: {}, 48: {}, 49: {}, 50: {}, 51: {}, 52: {}, 53: {}, 54: {}, 55: {}, 56: {},
                        57: {}, 58: {}, 59: {}, 60: {}, 61: {}, 62: {}, 63: {}, 64: {}, 65: {}, 66: {}, 67: {},
                        68: {}, 69: {}, 70: {}, 71: {}, 72: {}, 73: {}, 74: {}, 75: {}, 76: {}, 77: {}, 78: {}, 79: {}
                        }

    def StoreInstanceOfObjs(self,labels, cords):
        """
        Store the objects detected and their instances in the objects dict. Assign a unique id to each instance of the same class and stores its coordinates.
        :param labels: labels of each object
        :param cords: coordinates of each object
        """
        for i in range(len(labels)):
            self.objects[labels[i].item()][(len(self.objects[labels[i].item()]) if len(self.objects[labels[i].item()]) != 0 else 0)] = cords[i]


    def getcordOfObj(self,classname, instanceId,img):
        """
        Get the coordinate of specific object.
        :param classname: String that represent the class name
        :param instanceId: Id of that instance
        :param img: Image
        :return: return the x1,y1,x2,y2 coordinates of specific object.
        """
        x_shape, y_shape = img.shape[1], img.shape[0]
        x1, y1, x2, y2= 0,0,0,0
        classid = self.classes.index(classname)
        if classid is not None:
            cord = self.objects[classid][instanceId]
            x1, y1, x2, y2 = int(cord[0] * x_shape), int(cord[1] * y_shape), int(cord[2] * x_shape), int(cord[3] * y_shape)

        return x1, y1, x2, y2

    def findCenter(self,x1, y1, x2, y2):
        """
        Find the center point.
        :param x1: xmin postion
        :param x2: xmax postion
        :param y1: ymin postion
        :param y2: ymax postion
        :return: return center point
        """
        xCenter = (x1 + x2) / 2
        yCenter = (y1 + y2) / 2
        return xCenter, yCenter

    def ComputeAreaObjRatio(self,x1, y1, x2, y2, img):
        """
        Compute the ratio that a given object's area occupies in the image
        :param x1: xmin postion
        :param x2: xmax postion
        :param y1: ymin postion
        :param y2: ymax postion
        :param img: image
        :return: the ratio that a given object's area occupies in the image
        """
        l= x2-x1
        w= y2-y1
        objarea= w*l
        h,w,_ = img.shape
        imgarea= h*w
        ratio= objarea*100/imgarea
        return ratio


    def PlotBoxes(self,img):
        """
        Plot the prediction boxes, labels and instance id of each object detected.
        :param img: image
        :return: returns the ploted image
        """
        x_shape, y_shape = img.shape[1], img.shape[0]
        for i in self.objects:
            if len(self.objects[i]) != 0:
                for j in self.objects[i]:
                    cord = self.objects[i][j]
                    row = cord
                    if row[4] >= 0.2:
                        x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                        bgr = (0, 255, 0)
                        cv2.rectangle(img, (x1, y1), (x2, y2), bgr, 2)
                        cv2.putText(img, self.classes[i] + " "+str(j), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return img

