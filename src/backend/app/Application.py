import numpy as np
import cv2
from queue import Queue
from threading import Thread
import threading
import time

from app.singleton import Singleton
from app.face_detector import FaceDetector
from app.face_recognizer import FaceRecognizer
from app.images_manager import ImagesManager
from app.PersonManager import PersonManager
from app.models import FrameInfo, Face
from typing import List

DEFAULT_SAMPLE_PERIOD_TIME = 5


class Application(metaclass=Singleton):
    
    def __init__(self,options=None,sample_period_time: float = DEFAULT_SAMPLE_PERIOD_TIME):
        self.images_manager = ImagesManager()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()
        self.person_manager = PersonManager()

        self.options = options
        
        self.sampled_frames: Queue[np.ndarray] = Queue()
        self.processed_frame_info: FrameInfo = FrameInfo(bounding_boxes=[],names=[])
        self.last_sample_time = 0
        self.sample_period_time = sample_period_time

        self.processing_thread: Thread = Thread(target=self.process_frame_func)
        self.is_process_thread_running: bool = True
        self.processing_thread.start()
        self.processed_frame_info_lock = threading.Lock()

    def update_frame(self,frame: np.ndarray):
        """This is the main function of the application.
            It is supposed to called for every frame.
            It samples frames for processing and draws neccessary infos.
        """   
        current_time = time.time()
        
        if((current_time-self.last_sample_time)>self.sample_period_time):
            # make copy of numpy array
            copied_frame = frame.copy()
            self.sampled_frames.put(copied_frame)
            self.last_sample_time = current_time
        
        # mirror buffer of shared processed_frame_info buffer
        main_thread_frame_info = FrameInfo(bounding_boxes=[],names=[])
        # Copying buffer which can be used by both the main and processing thread 
        with self.processed_frame_info_lock:
            main_thread_frame_info = self.processed_frame_info.copy(deep=True)
        
        self.face_detector.draw_bounding_boxes(frame,main_thread_frame_info.bounding_boxes)
        #self.draw_names(frame,main_thread_frame_info.names)
        return frame

    def process_frame_func(self):
        """This thread function responsible for processing a frame.
        
            Works form the sampled_frames and saves result to processed_frame_info,
            which can be accessed from the main thread. (e.g. for drawing bounding boxes.)
        """
        while(self.is_process_thread_running):
            while(not (self.sampled_frames.empty())):
                frame = self.sampled_frames.get()

                bounding_boxes = self.face_detector.detect_faces(frame)
                faces = self.face_detector.crop_faces(frame,bounding_boxes)

                name_labels: List[str] = []
                for index,face in enumerate(faces):
                    face_uuid = self.face_recognizer.recognize_face(face)
                    
                    if face_uuid is None:
                        continue
                    
                    print(face_uuid)
                    file_path = self.images_manager.get_images_dir(face_uuid)
                    face = Face(id=face_uuid,file_path=file_path)

                    self.person_manager.register_face(face)
                    person = self.person_manager.find_person_by_face_uuid(face_uuid)
                    name_labels.append(person.name)
                    print(face_uuid)

                with self.processed_frame_info_lock:
                    self.processed_frame_info.bounding_boxes = bounding_boxes
                    #self.processed_frame_info.names = name_labels
            
            time.sleep(0.2)
    
    def close_processing_thread(self):
        self.is_processing_thread_running = False
        self.processing_thread.join()

    def draw_names(frame: np.ndarray,names: List[str]):
        for name in names:
            cv2.putText(frame,name,(100,100))
    
        
        