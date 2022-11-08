from app.models import Face,Person, Persons
from app.name_generator import name_generator
from app.singleton import Singleton

from typing import Dict, List
from uuid import UUID, uuid4
from itertools import chain
from pathlib import Path
import os
from threading import Thread
import threading
import time

#TODO: make it work with messages
class PersonNotFoundException(Exception):
    """Person not found"""
    pass

absolute_path = os.path.dirname(__file__)
relative_path = r"../../shared/assets/persons.json" 
DEFAULT_SAVE_PATH = os.path.join(absolute_path, relative_path)
DEFAULT_SAVE_PERIOD_TIME = 10

class PersonManager(metaclass=Singleton):
    """Class that responsible for Person management.
    
        Supported operations:
        -> adding new person, using a face
        -> renaming a person
        -> merging two persons
        -> in progress: saving option! 

    """
    
    __persons: Persons = Persons()
    __need_to_save: bool = False

    def __init__(self,save_period_time: float=DEFAULT_SAVE_PERIOD_TIME,save_path: str = DEFAULT_SAVE_PATH):
        """Load persons from some kind of holder: file or DB."""
        self.__save_period_time = save_period_time
        self.__save_path = save_path

        # Reading back saved info
        save_file_path = Path(self.__save_path)
        save_file_path.touch(exist_ok = True)
        with open(save_file_path, 'r') as content_file:
            content = content_file.read()
            if not len(content):
                content = "{}"
            
            self.__persons = Persons.parse_raw(content)

        self.flag_lock = threading.Lock()
        self.persons_lock = threading.Lock() # from main thread only lock when writing, because save thread doesn't write the persons

        self.saving_thread: Thread = Thread(target=self.save_thread_func)
        self.is_save_thread_running: bool = True
        self.saving_thread.start()
        
    def register_face(self,face: Face)->UUID:
        """Returns Persons UID"""
        # if the face_id is already registered to another person
        # simply return, that means no creation is necessary
        # if the face id is new creates a new person

        # check if the face is registered to another person
        registered_face_ids = [person.faces for person in self.__persons.persons.values()]
        registered_face_ids = list(chain.from_iterable(registered_face_ids))
        
        if face.id in registered_face_ids:
            return

        self.__create_person(face=face)
        self.__write_need_to_save()

    def __create_person(self,face: Face):
        gen_id = uuid4()
        gen_name = name_generator()

        person = Person(id=gen_id,name=gen_name,faces=[face])
        with self.persons_lock:
            self.__persons.persons[str(gen_id)]=person
        
    def __raise_if_person_not_found(self,person_id: UUID):
        if str(person_id) not in self.__persons.persons:
            raise PersonNotFoundException()
    
    def rename_person(self,person_id: UUID,new_name: str):
        self.__raise_if_person_not_found(person_id)
        # check the validity of the new_name?
        with self.person_lock:
            self.__persons.persons[str(person_id)].name = new_name
        self.__write_need_to_save()

    def merge_person(self,to_person_id: UUID, from_person_id: UUID):
        """merges from_person to to_person and deletes from_person"""
        # check whether this is a deep or a shallow copy
        to_person = self.get_person(to_person_id)
        from_person = self.get_person(from_person_id)

        with self.persons_lock:
            to_person.faces.append(from_person.faces)
            self.__delete_person(from_person_id)
        self.__write_need_to_save()

    def __delete_person(self,person_id: UUID):
        self.__raise_if_person_not_found(person_id)

        del self.__persons.persons[str(person_id)]
    
    def get_person(self,person_id: UUID)->Person:
        self.__raise_if_person_not_found(person_id)
        
        return self.__persons.persons[str(person_id)]

    def find_person_by_face_uuid(self,face_uuid: UUID)->Person:
        persons = list(self.__persons.persons.values())
        
        for person in persons:
            face_uuids = [face.id for face in person.faces]

            if face_uuid in face_uuids:
                return person
    
    def get_on_screen_persons(self,face_uuids:UUID)->List[Person]:
        persons =  [self.find_person_by_face_uuid(uuid) for uuid in face_uuids]
        return persons
    
    def get_all_persons(self)->Dict[UUID,Person]:
        # Consider this to return a list instead of dict
        return self.__persons.persons

    def __write_need_to_save(self,value:bool = True):
        with self.flag_lock:
            self.__need_to_save = value

    def save_thread_func(self):
        """Thread function that deals with saving."""
        
        while(self.is_save_thread_running):
            with self.flag_lock:
                need_to_save = self.__need_to_save
            print("Checking saving...")
            if(need_to_save):
                print("Saving persons...")
                with self.persons_lock:
                    jsondata = self.__persons.json(indent = 4)    
                try:
                    p = Path(self.__save_path)
                    p.write_text(jsondata)
                except OSError as e:
                    print(f"Failed to save config {repr(e)}")
                
                self.__write_need_to_save(False)
            
            time.sleep(self.__save_period_time)
    