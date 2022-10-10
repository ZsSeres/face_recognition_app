from src.app.backend.src.models import Face,Person
from src.app.backend.src.name_generator import name_generator

from typing import Dict, List
from uuid import UUID, uuid4
from itertools import chain


#TODO: make it work with messages
class PersonNotFoundException(Exception):
    """Person not found"""
    pass


class PersonManager:
    """Class that responsible for Person management.
    
        Supported operations:
        -> adding new person, using a face
        -> renaming a person
        -> merging two persons 

    """
    
    __persons: Dict[UUID,Person] = {}

    def __init__(self,initial_persons: List[Person]):
        """Load persons from some kind of holder: file or DB."""
        pass
    
    def create_person(self,face: Face):
        
        #check if the face is registered to another person
        registered_face_ids = [person.faces for person in self.__persons.values()]
        registered_face_ids = list(chain.from_iterable(registered_face_ids))
        if face.id in registered_face_ids:
            #TODO: custom error instead of this???
            raise ValueError()

        gen_id = uuid4()
        gen_name = name_generator()

        person = Person(id=gen_id,name=gen_name,faces=[face])
        self.__persons[gen_id]=person
        
    def __raise_if_person_not_found(self,person_id: UUID):
        if person_id not in self.__persons:
            raise PersonNotFoundException()
    
    def rename_person(self,person_id: UUID,new_name: str):
        self.__raise_if_person_not_found(person_id)
        # check the validity of the new_name?
        self.__persons[person_id].name = new_name

    def merge_person(self,to_person_id: UUID, from_person_id: UUID):
        """merges from_person to to_person and deletes from_person"""
        # check whether this is a deep or a shallow copy
        to_person = self.get_person(to_person_id)
        from_person = self.get_person(from_person_id)

        to_person.faces.append(from_person.faces)
        self.__delete_person(from_person_id)

    def __delete_person(self,person_id: UUID):
        self.__raise_if_person_not_found(person_id)

        del self.__persons[person_id]
    
    def get_person(self,person_id: UUID)->Person:
        self.__raise_if_person_not_found(person_id)
        
        return self.__persons[person_id]

    def get_all_persons(self)->Dict[UUID,Person]:
        # Consider this to return a list instead of dict
        return self.__persons


    