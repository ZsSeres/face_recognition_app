from app.singleton import Singleton
from app.face_detector import FaceDetector
from app.face_recognizer import FaceRecognizer

from app.images_manager import ImagesManager
import numpy as np

class Application(metaclass=Singleton):
    
    def __init__(self,options=None):
        self.images_manager = ImagesManager()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()

    def process_frame(self,frame: np.ndarray):
        bounding_boxes = self.face_detector.detect_faces(frame)
        self.face_detector.draw_bounding_boxes(frame,bounding_boxes)