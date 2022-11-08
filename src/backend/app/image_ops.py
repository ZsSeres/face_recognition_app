import cv2
import numpy as np
from typing import List, Dict
from uuid import UUID

from app.models import BoundingBox, Person


def draw_bounding_boxes(arr: np.ndarray,bounding_boxes:List[BoundingBox]):
            for bb in (bounding_boxes):
                top_left = (bb.top,bb.left) 
                bottom_right = (bb.bottom,bb.right)
                color = (0,0,255)
                arr = cv2.rectangle(arr,top_left,bottom_right,color)

def crop_faces(arr: np.ndarray,bounding_boxes:List[BoundingBox])->List[np.ndarray]:
        return [arr[bb.left:bb.right,bb.top:bb.bottom] for bb in bounding_boxes]

def draw_names(frame: np.ndarray,bounding_boxes: Dict[UUID,BoundingBox], bounding_boxes_person_connector: Dict[UUID,Person]):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (0, 0, 255)
    thickness = 2
    

    for id_ in bounding_boxes:
        org = (bounding_boxes[id_].bottom,bounding_boxes[id_].left)
        name = bounding_boxes_person_connector[id_].name
        cv2.putText(frame,name, org, font, 
               fontScale, color, thickness, cv2.LINE_AA)