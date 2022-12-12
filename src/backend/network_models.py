from pydantic import BaseModel
from app.models import Person
from typing import List

class GetPersonsResponse(BaseModel):
    persons: List[Person]