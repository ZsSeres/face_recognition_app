from cmath import inf
import face_recognition
import numpy as np
from uuid import UUID
from typing import List, Dict, Optional, Tuple
from PIL.PngImagePlugin import PngImageFile


class EncodingManager:
    # külön 2 párhuzamos lista
    face_encodings_dict: Dict[UUID,List[np.ndarray]] = {}

    def add_encoding(self,encoding: np.ndarray, uuid: UUID)->np.ndarray:
        if not uuid in self.face_encodings_dict:
            self.face_encodings_dict[uuid] = []
        
        self.face_encodings_dict[uuid].append(encoding)
        return encoding
        
    @staticmethod
    def create_encoding(image:PngImageFile)->np.ndarray:
        img_arr: np.ndarray = np.asarray(image)
        return face_recognition.face_encodings(img_arr)[0]

    def get_uuids(self)->List[UUID]:
        return list(self.face_encodings_dict.keys())
    
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
    
    # Ez lehet a lassabb mert ez a ritkábban
    def get_encodings(self,uuid: UUID)->List[np.ndarray]:        
        if uuid not in self.face_encodings_dict:
            return []
        return self.face_encodings_dict[uuid]
