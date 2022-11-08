
from face_recognition import face_locations
import numpy as np
from typing import List, Dict
from app.models import BoundingBox
import cv2
from PIL.PngImagePlugin import PngImageFile

import time
from enum import Enum
from app.singleton import Singleton
from uuid import UUID, uuid4
from threading import Lock

class FaceDetectMethodEnum(str,Enum):
    HOG = 'HOG'
    CNN = 'CNN'
    HAAR = "HAAR"

demo_image = cv2.imread(r"../shared/assets/demo_faces/bezos_01.png")
DEFAULT_DISTANT_EPSILON = 50 # check this out!

class FaceDetector(metaclass=Singleton):
    def __init__(self, detect_method: FaceDetectMethodEnum=FaceDetectMethodEnum.HAAR, distant_epsilon: float = DEFAULT_DISTANT_EPSILON):
        self.__face_cascade = cv2.CascadeClassifier(r"./assets/haarcascade_frontalface_default.xml")
        self.__bounding_boxes: Dict[UUID,BoundingBox] = {}
        self.__new_bounding_boxes:  Dict[UUID,BoundingBox] = {}

        self.__detect_method: FaceDetectMethodEnum = detect_method
        self.__distant_epsilon: float = distant_epsilon # az a távolság amin belül keressük a bounding boxnak a párját az előző frame-n
        # itt azt tesszük fel, hogy két framen belül nem mehet két arc nagyon messze

        self.__bounding_boxes_lock = Lock()

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

        print(bounding_boxes)
        transformed_bounding_boxes = [BoundingBox(left=bounding_box[3],top=bounding_box[0],right=bounding_box[1],bottom=bounding_box[2]) for bounding_box in bounding_boxes]
        return transformed_bounding_boxes

    
    def update(self,frame: np.ndarray):
        t1 = time.time()
        new_bounding_boxes =  self.__detect_faces(frame)
        self.__new_bounding_boxes = {} # flushing the old cycles new_bounding_boxes detection
        tmp_bounding_boxes = {} # temporary pair for self.__bounding_boxes
        
        # detecting the new bounding boxes on purely geometrical data. 
        for new_bb in new_bounding_boxes:
            distances = {id_:(value-new_bb) for (id_,value) in self.__bounding_boxes.items()}
            near_ids = [id_ for id_ in distances if distances[id_]<self.__distant_epsilon] # ebbe elmenteni amik közel vannak és ezzel dolgozni tovább
            
            # no near bb found->this is a new bounding box
            if len(near_ids) == 0:
                new_uuid = uuid4()
                self.__new_bounding_boxes[new_uuid] = new_bb
                tmp_bounding_boxes[new_uuid] = new_bb
                continue
            
            # find the matching pair
            area_differences = {id_:(np.abs(value.area()-new_bb.area())) for (id_,value) in self.__bounding_boxes.items() if id_ in near_ids}
            closest_area_idx = np.argmin(list(area_differences.values()))
            matching_id = list(area_differences.keys())[closest_area_idx]
           
            tmp_bounding_boxes[matching_id] =  new_bb   
            with self.__bounding_boxes_lock:
                del self.__bounding_boxes[matching_id] # the old bounding box which has a matching pair, must be deleleted

      
        self.__bounding_boxes = tmp_bounding_boxes
        t2 = time.time()
        print(f"Detect and track time: {t2-t1}")
    
    def draw_bounding_boxes(self,arr: np.ndarray):
            for bb in (self.__bounding_boxes.values()):
                top_left = (bb.top,bb.left) 
                bottom_right = (bb.bottom,bb.right)
                color = (0,0,255)
                arr = cv2.rectangle(arr,top_left,bottom_right,color)

    # def crop_faces(self,arr: np.ndarray)->List[np.ndarray]:
    #      return [arr[bb.left:bb.right,bb.top:bb.bottom] for bb in self.__bounding_boxes]
    
    # def crop_new_faces(self,arr: np.ndarray)->List[np.ndarray]:
    #     return [arr[bb.left:bb.right,bb.top:bb.bottom] for bb in self.__new_bounding_boxes]

    def get_bounding_boxes(self)->Dict[UUID,BoundingBox]:
        return self.__bounding_boxes

    def get_new_bounding_boxes(self)->Dict[UUID,BoundingBox]:
        return self.__new_bounding_boxes



