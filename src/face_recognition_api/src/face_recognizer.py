from uuid import uuid4,UUID 
from PIL.PngImagePlugin import PngImageFile

from src.shared.singleton import Singleton
from src.face_recognition_api.src.images_manager import ImagesManager
from src.face_recognition_api.src.encodings_manager import EncodingManager

DEFAULT_RECOGNIZE_TOLERANCE = 0.6
DEFAULT_IDENTICAL_TOLERANCE = 0.1

class FaceRecognizer(metaclass=Singleton):
    images_manager: ImagesManager = ImagesManager()
    encoding_manager: EncodingManager = EncodingManager()
    
    def __init__(self,recognize_tolerance: float=DEFAULT_RECOGNIZE_TOLERANCE,identical_tolerance: float=DEFAULT_IDENTICAL_TOLERANCE):
        # Encode known faces
        # and load them into encoding manager
        self.recognize_tolerance: float = recognize_tolerance
        self.identical_tolerance: float = identical_tolerance
        
        uuids = self.images_manager.get_uuids()
        
        for uuid in uuids:
            images = self.images_manager.load_images(uuid)
            # ez helyett kimentés és olvasás 1 darab fájl
            encodings = [self.encoding_manager.create_encoding(image) for image in images]
            
            for encoding in encodings:
                self.encoding_manager.add_encoding(encoding,uuid)

    def recognize_face(self,image:PngImageFile)->UUID:
                
        encoding = self.encoding_manager.create_encoding(image)
        closest_uuid,min_distance = self.encoding_manager.get_closest_group(encoding)

        if min_distance > self.recognize_tolerance:
            target_uuid = uuid4()
        else:
            target_uuid = closest_uuid

        if min_distance > self.identical_tolerance:
            self.images_manager.save_image(target_uuid,image)
            self.encoding_manager.add_encoding(encoding,target_uuid)
        
        return target_uuid    