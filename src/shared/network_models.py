from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.shared.models import BoundingBox

class RecognizeFaceRequest(BaseModel):
    encoded_image_bytes: bytes

class RecognizeFaceResponse(BaseModel):
    face_uuid: UUID

class DetectFacesRequest(BaseModel):
    encoded_image_bytes: bytes

class DetectFacesResponse(BaseModel):
    face_bounding_boxes: List[BoundingBox]

