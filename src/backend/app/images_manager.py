from tkinter import Image
import cv2
from uuid import UUID, uuid4
from typing import List
import os
import shutil

import numpy as np

absolute_path = os.path.dirname(__file__)
relative_path = r"../../shared/assets/faces" 
DEFAULT_FACES_BASE_PATH: str = os.path.join(absolute_path, relative_path)
DEFAULT_IMAGE_SHAPE: tuple = (256,256)

class ImagesManager:
    """This class is responsible for operations regarding images
        face images. Get face_uuid_names
        Delete images maybe important too.
    """
    # TODO: get_images_dir function!
    def __init__(self,base_path:str=DEFAULT_FACES_BASE_PATH,img_shape:tuple=DEFAULT_IMAGE_SHAPE):
        self.base_path = base_path
        self.img_shape = img_shape

        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)
    
    def save_image(self,face_uuid: UUID,image: np.ndarray)->str:
        """Steps:
            -> check if  directory with face_uuid name exist
            -> if not create
            -> generate an image name with file path
            -> save image with full path
            -> return file path
        """
        dir_path = os.path.join(self.base_path,str(face_uuid))
        
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # itt elvérzik hibával, akkor lehet, hogy üres directoryk összessége jön létre
        # ez a hiba akkor fordulhat elő, ha új face-k jönnek
        name_uuid = uuid4()
        file_path = os.path.join(dir_path,str(name_uuid))+'.png'
        
        cv2.imwrite(file_path,image)
        return file_path
       
    def load_images(self,face_uuid: UUID)-> List[np.ndarray]:
        images: List[np.ndarray] = []
        dir_path = os.path.join(self.base_path,str(face_uuid))
        
        if not os.path.exists(dir_path):
            return images
        
        for image_name in os.listdir(dir_path):
            if image_name.endswith('.png'):
              image_path = os.path.join(dir_path,image_name)
              image = cv2.imread(image_path)
              images.append(image)  

        return images
    
    def get_uuids(self)->List[UUID]:
        """Return the face uuids"""
        uuids: List[UUID] = []
        
        for dir_path in os.listdir(self.base_path):
            uuid = UUID(dir_path.split("//")[-1])
            uuids.append(uuid)
        
        return uuids

    def get_images_dir(self,face_uuid: UUID)->str:
        """Returns full path"""
        #TODO: test this!
        #print(f"Base path: {self.base_path}")
        #print(f"Face uuid: {face_uuid}")
        
        abs_path = os.path.abspath("../shared/assets/faces")
        print(abs_path)

        return os.path.join(abs_path,str(face_uuid))

    def delete_images_dir(self,face_uuid:UUID)->None:
        abs_path = os.path.abspath("../shared/assets/faces")

        full_path = os.path.join(abs_path,face_uuid)
        shutil.rmtree(full_path, ignore_errors=False, onerror=None)