from typing import Tuple
from PIL.PngImagePlugin import PngImageFile
from src.shared.models import BoundingBox


class Drawer:
    "Class for drawing operations"
    
    # make it as effecient as possible

    @staticmethod
    def draw_bounding_box(img: PngImageFile,bounding_box: BoundingBox)->PngImageFile:
        #TODO
        pass

    @staticmethod
    def calc_label_pos(bounding_box: BoundingBox)->Tuple(int,int):
        #TODO
        pass

    @staticmethod
    def draw_label(img: PngImageFile,label_pos: Tuple(int,int),label: str)->PngImageFile:
        # TODO
        pass