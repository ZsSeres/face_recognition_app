from tkinter import Image
from PIL.PngImagePlugin import PngImageFile
from PIL import Image
from uuid import UUID, uuid4
from typing import List
import os


import numpy as np

absolute_path = os.path.dirname(__file__)
print(f"Absolute path: {absolute_path}")
relative_path = r"../../shared/assets/faces" 
DEFAULT_FACES_BASE_PATH: str = os.path.join(absolute_path, relative_path)
print(f"Base path: {DEFAULT_FACES_BASE_PATH}")
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
        image = Image.fromarray(image)
        dir_path = os.path.join(self.base_path,str(face_uuid))
        
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # itt elvérzik hibával, akkor lehet, hogy üres directoryk összessége jön létre
        # ez a hiba akkor fordulhat elő, ha új face-k jönnek
        name_uuid = uuid4()
        file_path = os.path.join(dir_path,str(name_uuid))+'.png'
        
        image.save(file_path)
        return file_path
       
    def load_images(self,face_uuid: UUID)-> List[np.ndarray]:
        images: List[PngImageFile] = []
        dir_path = os.path.join(self.base_path,str(face_uuid))
        
        if not os.path.exists(dir_path):
            return images
        
        for image_name in os.listdir(dir_path):
            if image_name.endswith('.png'):
              image_path = os.path.join(dir_path,image_name)
              print(image_path)
              image = Image.open(image_path)
              images.append(np.asarray(image))  

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
        return os.path.join(os.getcwd(),self.base_path,face_uuid)