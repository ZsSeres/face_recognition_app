from typing import List,Tuple
from uuid import UUID
from pydantic import BaseModel

class RecognizeFaceRequest(BaseModel):
    encoded_image_bytes: bytes

    class Config:
        arbitrary_types_allowed = True

class RecognizeFaceResponse(BaseModel):
    face_uuid: UUID


class DetectFacesRequest(BaseModel):
    encoded_image_bytes: bytes


class DetectFacesResponse(BaseModel):
    face_bounding_boxes: List[Tuple[int]]
