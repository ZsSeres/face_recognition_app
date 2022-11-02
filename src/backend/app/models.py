from pydantic import BaseModel
from uuid import UUID
from typing import List, Tuple


class Face(BaseModel):
    """Dataclass for person faces.

        One person can have multiple faces.

        Attributes:
            id(UUID): unique identifier
            images_file_path: file_path for the face images
    """
    
    id: UUID
    images_file_path: str


class Person(BaseModel):
    """Data class that represents a person.
    
        Attributes:
            id(UUID): uniquie identifier
            name(str): name of the person
            faces(List[Faces]): list of registered Face objects for the person
    """
    
    id: UUID
    name: str
    faces: List[Face]

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

class FrameInfo(BaseModel):
    bounding_boxes: List[BoundingBox]