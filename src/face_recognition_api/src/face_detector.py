from PIL.PngImagePlugin import PngImageFile
from face_recognition import face_locations
import numpy as np
from typing import Tuple,List

def detect_faces(image:PngImageFile)->List[Tuple[int]]:
    """
    Returns list of face bounding boxes parameters.
    A bounding box parameter order is the following:
    (left,top,right,bottom)
    """
    
    transformed_bounding_boxes = []
    img_arr = np.asarray(image)
    
    bounding_boxes =  face_locations(img_arr,1,"cnn")
    transformed_bounding_boxes = [(bounding_box[3],bounding_box[0],bounding_box[1],bounding_box[2]) for bounding_box in bounding_boxes]
    return transformed_bounding_boxes