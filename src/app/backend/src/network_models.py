import string
from typing import Dict
from uuid import UUID
from pydantic import BaseModel

from src.app.backend.src.models import Person

# this file contains network models for app_backend -> app_frontend communication

class GetPersonsResponse(BaseModel):
    persons: Dict[UUID,Person]

class MergePersonsRequest(BaseModel):
    to_person_id: UUID
    from_person_id: UUID

class RenamePersonRequest(BaseModel):
    new_name: str

# send back full person object with new name???