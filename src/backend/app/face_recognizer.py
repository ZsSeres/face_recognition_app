from uuid import uuid4,UUID 

from app.singleton import Singleton
from app.images_manager import ImagesManager
from typing import List,Dict, Tuple, Optional
import face_recognition


import numpy as np

DEFAULT_RECOGNIZE_TOLERANCE = 0.6
DEFAULT_IDENTICAL_TOLERANCE = 0.1

class FaceRecognizer(metaclass=Singleton):
    
    def __init__(self,recognize_tolerance: float=DEFAULT_RECOGNIZE_TOLERANCE,identical_tolerance: float=DEFAULT_IDENTICAL_TOLERANCE):
        # Encode known faces
        # and load them into encoding manager
        self.face_encodings_dict: Dict[UUID,List[np.ndarray]] = {}
        self.recognize_tolerance: float = recognize_tolerance
        self.identical_tolerance: float = identical_tolerance
        
        uuids = ImagesManager().get_uuids()
        
        for uuid in uuids:
            images = ImagesManager().load_images(uuid)
            # ez helyett kimentés és olvasás 1 darab fájl
            encodings = [face_recognition.face_encodings(image)[0] for image in images]
            
            for encoding in encodings:
                self.add_encoding(encoding,uuid)

    def add_encoding(self,encoding: np.ndarray, uuid: UUID):
        if not uuid in self.face_encodings_dict:
            self.face_encodings_dict[uuid] = []
        
        self.face_encodings_dict[uuid].append(encoding)
    
    def get_min_distance_in_group(self,encoding: np.ndarray,group_uuid: UUID)->float:
        # Váltások csökkentése 1 darab array
        distances = face_recognition.face_distance(self.face_encodings_dict[group_uuid],encoding)
        return np.min(distances)
    
    def get_closest_group(self,encoding: np.ndarray)->Tuple[Optional[UUID],float]:
        # Gyorsítás:
        # -> Spatial index?
        # -> 1 darab numpy tömb
        #  
        closest_group_uuid = None
        absolute_min_distance = float(inf)

        for uuid in self.face_encodings_dict:
            group_min_distance = self.get_min_distance_in_group(encoding,uuid)

            if(absolute_min_distance>group_min_distance):
                absolute_min_distance = group_min_distance
                closest_group_uuid = uuid

            return (closest_group_uuid,absolute_min_distance)
    
    def recognize_face(self,image: np.ndarray)->UUID:
                
        encoding = face_recognition.face_encodings(image)[0]
        closest_uuid,min_distance = EncodingManager.encoding_manager.get_closest_group(encoding)

        if min_distance > self.recognize_tolerance:
            target_uuid = uuid4()
        else:
            target_uuid = closest_uuid

        if min_distance > self.identical_tolerance:
            ImagesManager().save_image(target_uuid,image)
            self.encoding_manager.add_encoding(encoding,target_uuid)
        
        return target_uuid    