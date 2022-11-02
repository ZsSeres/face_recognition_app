from src.app.backend.src.APIManager import APIManager
from src.app.backend.src.PersonManager import PersonManager
from src.shared.models import BoundingBox
from src.app.backend.src.models import Face

from PIL.PngImagePlugin import PngImageFile
from enum import Enum
from typing import List

class DetectRecognizeStrategy(str,Enum):
    pass

# TODO
def draw_bounding_box_and_label(img: PngImageFile,bounding_box: BoundingBox,label: str):
    # maybe seperate draw_bounding_box and draw_label
    pass

async def detect_and_recognize(start_img: PngImageFile,strategy: DetectRecognizeStrategy)->PngImageFile:
    bounding_boxes: List[BoundingBox] = await APIManager().detect_faces(start_img)
    cropped_imgs = [start_img.crop(bounding_box.to_tuple()) for bounding_box in bounding_boxes]

    for cropped_img in  cropped_imgs:
        id = await APIManager().recognize_face(cropped_img)
        img_dir = await APIManager().get_images_dir(id)
        face = Face(id,img_dir)

        PersonManager().register_face(face)

        #draw_bounding_box_and_label()    
        
