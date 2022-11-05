
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

class FaceDetector(metaclass=Singleton):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(r"./assets/haarcascade_frontalface_default.xml")
    
    def detect_faces(self,arr: np.ndarray, method: FaceDetectMethodEnum=FaceDetectMethodEnum.HAAR)->List[BoundingBox]:
        transformed_bounding_boxes = []
        
        if method == FaceDetectMethodEnum.HAAR:
            grey = cv2.cvtColor(arr,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(grey,1.1,4)
            transformed_bounding_boxes = [BoundingBox(left=y,top=x,right=y+h,bottom=x+w) for (x,y,w,h) in faces]

            return transformed_bounding_boxes
        
        elif method == FaceDetectMethodEnum.CNN:
            bounding_boxes =  face_locations(arr,1,"cnn")
        
        elif method == FaceDetectMethodEnum.HOG:
            bounding_boxes =  face_locations(arr,1,"hog")

        transformed_bounding_boxes = [BoundingBox(left=bounding_box[3],top=bounding_box[0],right=bounding_box[1],bottom=bounding_box[2]) for bounding_box in bounding_boxes]
        return transformed_bounding_boxes
    # # only for debugging porpuses
    # def demo_detect(self):
    #     grey = cv2.cvtColor(demo_image,cv2.COLOR_BGR2GRAY)
    #     faces = self.face_cascade.detectMultiScale(grey,1.1,4)
    
    def draw_bounding_boxes(self,arr: np.ndarray, bounding_boxes: List[BoundingBox]):
            for bb in bounding_boxes:
                top_left = (bb.top,bb.left) 
                bottom_right = (bb.bottom,bb.right)
                color = (0,0,255)
                arr = cv2.rectangle(arr,top_left,bottom_right,color)

    def crop_faces(self,arr: np.ndarray, bounding_boxes: List[BoundingBox])->List[np.ndarray]:
        return [arr[bb.left:bb.right,bb.top:bb.bottom] for bb in bounding_boxes]
   



