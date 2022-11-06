
from face_recognition import face_locations
import numpy as np
from typing import List
from app.models import BoundingBox
import cv2
from PIL.PngImagePlugin import PngImageFile

import time
from enum import Enum
from app.singleton import Singleton

class FaceDetectMethodEnum(str,Enum):
    HOG = 'HOG'
    CNN = 'CNN'
    HAAR = "HAAR"

demo_image = cv2.imread(r"../shared/assets/demo_faces/bezos_01.png")
DEFAULT_DISTANT_EPSILON = 40 # check this out!

class FaceDetector(metaclass=Singleton):
    def __init__(self, detect_method: FaceDetectMethodEnum=FaceDetectMethodEnum.HAAR, distant_epsilon: float = DEFAULT_DISTANT_EPSILON):
        self.__face_cascade = cv2.CascadeClassifier(r"./assets/haarcascade_frontalface_default.xml")
        self.__bounding_boxes: List[BoundingBox] = []
        self.__new_bounding_boxes: List[BoundingBox] = []

        self.__detect_method: FaceDetectMethodEnum = detect_method
        self.__distant_epsilon: float = distant_epsilon # az a távolság amin belül keressük a bounding boxnak a párját az előző frame-n
        # itt azt tesszük fel, hogy két framen belül nem mehet két arc nagyon messze
    
    def __detect_faces(self,arr: np.ndarray)->List[BoundingBox]:
        transformed_bounding_boxes = []
        
        if self.__detect_method == FaceDetectMethodEnum.HAAR:
            grey = cv2.cvtColor(arr,cv2.COLOR_BGR2GRAY)
            faces = self.__face_cascade.detectMultiScale(grey,1.1,4)
            transformed_bounding_boxes = [BoundingBox(left=y,top=x,right=y+h,bottom=x+w) for (x,y,w,h) in faces]

            return transformed_bounding_boxes
        
        elif self.__detect_method == FaceDetectMethodEnum.CNN:
            bounding_boxes =  face_locations(arr,1,"cnn")
        
        elif self.__detect_method == FaceDetectMethodEnum.HOG:
            bounding_boxes =  face_locations(arr,1,"hog")

        transformed_bounding_boxes = [BoundingBox(left=bounding_box[3],top=bounding_box[0],right=bounding_box[1],bottom=bounding_box[2]) for bounding_box in bounding_boxes]
        return transformed_bounding_boxes

    
    def update(self,frame: np.ndarray):
        new_bounding_boxes =  self.__detect_faces(frame)
        self.__new_bounding_boxes = [] # flushing the old cycles new_bounding_boxes detection
        
        # detecting the new bounding boxes on purely geometrical data. 
        for new_bb in new_bounding_boxes:
            distances = [new_bb - bb for bb in self.__bounding_boxes]
            near_bb_indeces = [idx for idx,d in enumerate(distances) if d < self.__distant_epsilon]
        
            # no near bb found->this is a new bounding box
            if len(near_bb_indeces) == 0:
                self.__new_bounding_boxes.append(new_bb)
                continue
            
            area_differences = [(np.abs(new_bb.area()-self.__bounding_boxes[near_bb_i].area()),near_bb_i) for near_bb_i in near_bb_indeces]
            closest_area_index = np.argmin([a_diff[0] for a_diff in area_differences])
            print(closest_area_index)

            element_to_remove_index = area_differences[closest_area_index][1]
            print(element_to_remove_index)
            del self.__bounding_boxes[element_to_remove_index] # the old bounding box which has data has a matching pair

        self.__bounding_boxes = new_bounding_boxes
    
    def draw_bounding_boxes(self,arr: np.ndarray):
            for bb in self.__bounding_boxes:
                top_left = (bb.top,bb.left) 
                bottom_right = (bb.bottom,bb.right)
                color = (0,0,255)
                arr = cv2.rectangle(arr,top_left,bottom_right,color)

    def crop_faces(self,arr: np.ndarray)->List[np.ndarray]:
        return [arr[bb.left:bb.right,bb.top:bb.bottom] for bb in self.__bounding_boxes]
   
    def get_bounding_boxes(self)->List[BoundingBox]:
        return self.__bounding_boxes

    def get_new_bounding_boxes(self)->List[BoundingBox]:
        return self.__new_bounding_boxes



