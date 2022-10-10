from tkinter import Image
from PIL.PngImagePlugin import PngImageFile
from PIL import Image
from uuid import UUID, uuid4
from typing import List
import os

DEFAULT_FACES_BASE_PATH: str = "../assets/faces"
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
    
    def save_image(self,face_uuid: UUID,image: PngImageFile)->str:
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
        
        image.save(file_path)
        return file_path
       
    def load_images(self,face_uuid: UUID)-> List[PngImageFile]:
        images: List[PngImageFile] = []
        dir_path = os.path.join(self.base_path,str(face_uuid))
        
        if not os.path.exists(dir_path):
            return images
        
        for image_name in os.listdir(dir_path):
            if image_name.endswith('.png'):
              image_path = os.path.join(dir_path,image_name)
              print(image_path)
              image = Image.open(image_path)
              images.append(image)  

        return images
    
    def get_uuids(self)->List[UUID]:
        """Return the face uuids"""
        uuids: List[UUID] = []
        
        for dir_path in os.listdir(self.base_path):
            uuid = UUID(dir_path.split("//")[-1])
            uuids.append(uuid)
        
        return uuids