from pydantic import BaseModel
from typing import Optional
import uuid

class Cat(BaseModel):
    name: str
    cuteness: int

class Face(BaseModel):
    id_: uuid.UUID
    label: Optional[str]
    file_path: str

class Position(BaseModel):
    x: float
    y: float

class BoundingBox(BaseModel):
    left: int
    top: int
    right: int
    bottom: int