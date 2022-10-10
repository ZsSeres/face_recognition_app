from pydantic import BaseModel
from typing import Tuple
import uuid


# TODO: move this to app
# class Face(BaseModel):
#     id_: uuid.UUID
#     label: Optional[str]
#     file_path: str

class BoundingBox(BaseModel):
    """Model class which represents a bounding box.
    
        Attributes:
            left
            top
            right
            bottom
    """
    
    left: int
    top: int
    right: int
    bottom: int

    def to_tuple(self)->Tuple[int]:
        """Returns the attributes in a tuple with the following order:
            (left,top,right,bottom)
        """
        return (self.left,self.top,self.right,self.bottom)
    
    def get_width(self)->int:
        pass
    
    def get_height(self)->int:
        pass
    
    def area(self)->int:
        """Calculate the are of the bounding box."""
        pass