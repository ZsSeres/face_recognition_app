from pydantic import BaseModel
from uuid import UUID
from typing import List


class Face(BaseModel):
    id: UUID
    images_file_path: str


class Person(BaseModel):
    id: UUID
    name: str
    faces: List[Face]