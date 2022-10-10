from pydantic import BaseModel
from uuid import UUID
from typing import List


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