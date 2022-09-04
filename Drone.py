import time

from djitellopy import tello
from time import sleep
import numpy as np


class Drone:

    # Coordinates of the object we want to track
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0

    def __init__(self):

        # Connecting Drone
        self.me = tello.Tello()
        self.me.connect()
        print("Battery: " + str(self.me.get_battery()) + "%")

       # Speed infos
        self.fb= 0
        self.updw= 0
        self.lfrt= 0
        self.fb_range= (25,60)
        self.pid = [0.5,0.5,0]

    def getImage(self):
        return self.me.get_frame_read().frame

    def trackObject(self, x, y, area_ratio,img, pErrors):

        h, w, _ = img.shape

        # Correcting speed for front and backward movements
        if area_ratio > self.fb_range[0] and area_ratio < self.fb_range[1]:
            self.fb=0
        elif area_ratio < self.fb_range[0]:
            front_error = self.fb_range[0]-area_ratio
            self.fb= self.pid[0] * front_error + self.pid[1]* (front_error- pErrors[0])
            self.fb=int(np.clip(self.fb,-100,100))
        elif area_ratio > self.fb_range[1]:
            back_error = self.fb_range[1]-area_ratio
            self.fb = self.pid[0] * back_error + self.pid[1] * (back_error - pErrors[1])
            self.fb=int(np.clip(self.fb,-100,100))

        # Correcting speed for left and right movements
        if x == 0:
            self.lfrt=0
        else:
            lfrt_error = x - w//2
            self.lfrt =  self.pid[0] * lfrt_error + self.pid[1]* (lfrt_error- pErrors[2])
            self.lfrt= int(np.clip(self.lfrt,-100,100))

        # Correction seep for up and down movements
        if y == 0:
            self.updw=0
        else:
            updw_error = y - h//2
            self.updw =  self.pid[0] * updw_error + self.pid[1]* (updw_error- pErrors[3])
            self.updw= int(np.clip(self.updw,-100,100))

        print("Front & back speed: "+str(self.fb) + ", Left & Right speed: " + str(self.lfrt)+ ", Up and Down speed: "+str(self.updw))

        return front_error, back_error, lfrt_error, updw_error



mydrone = Drone()

mydrone.me.takeoff()
mydrone.me.send_rc_control(0,50,0,0)

mydrone.me.send_rc_control(0,0,0,0)
mydrone.me.land()