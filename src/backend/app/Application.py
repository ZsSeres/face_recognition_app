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
from app.models import FrameInfo, Face, BoundingBox, Person
from app.image_ops import draw_bounding_boxes, crop_faces, draw_names
from typing import List, Dict
from uuid import UUID

DEFAULT_SAMPLE_PERIOD_TIME = 0.2


class Application(metaclass=Singleton):
    
    def __init__(self,options=None,sample_period_time: float = DEFAULT_SAMPLE_PERIOD_TIME):
        self.images_manager = ImagesManager()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()
        self.person_manager = PersonManager()

        self.options = options
        
        self.sampled_frames: Queue[np.ndarray] = Queue()
        self.processed_frame_info: FrameInfo = FrameInfo(bounding_boxes={},bounding_box_person_connector={})
        self.last_sample_time = 0
        self.sample_period_time = sample_period_time

        self.processing_thread: Thread = Thread(target=self.process_frame_func)
        self.is_process_thread_running: bool = True
        self.processing_thread.start()
        self.processed_frame_info_lock = threading.Lock()

        print("Application started!")

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
        main_thread_frame_info = FrameInfo(bounding_boxes={},bounding_box_person_connector={})
        # Copying buffer which can be used by both the main and processing thread 
        with self.processed_frame_info_lock:
            main_thread_frame_info:FrameInfo = self.processed_frame_info.copy(deep=True)
        
        draw_bounding_boxes(frame,list(main_thread_frame_info.bounding_boxes.values()))
        draw_names(frame=frame,bounding_boxes=main_thread_frame_info.bounding_boxes,bounding_boxes_person_connector=main_thread_frame_info.bounding_box_person_connector)
        
        return frame

    def process_frame_func(self):
        """This thread function responsible for processing a frame.
        
            Works form the sampled_frames and saves result to processed_frame_info,
            which can be accessed from the main thread. (e.g. for drawing bounding boxes.)
        """
        bounding_box_person_connector: Dict[UUID,Person] = {}

        while(self.is_process_thread_running):
            while(not (self.sampled_frames.empty())):
                frame = self.sampled_frames.get()

                self.face_detector.update(frame)
                bounding_boxes_with_ids = self.face_detector.get_bounding_boxes()
                new_bounding_boxes_with_ids = self.face_detector.get_new_bounding_boxes()
                
                # delete_old_connections
                old_bounding_box_ids = list(bounding_box_person_connector.keys())
                bounding_box_ids = list(bounding_boxes_with_ids.keys())
                new_bounding_box_ids = list(new_bounding_boxes_with_ids.keys())
                
                for old_id in old_bounding_box_ids:
                    if old_id not in bounding_box_ids:
                        del bounding_box_person_connector[old_id]

                
                new_faces = crop_faces(frame,list(new_bounding_boxes_with_ids.values()))

                for idx,face in enumerate(new_faces):
                    bounding_box_id = new_bounding_box_ids[idx]
                    face_uuid = self.face_recognizer.recognize_face(face)
                    
                    if face_uuid is None:
                        continue
                    
                    file_path = self.images_manager.get_images_dir(face_uuid)
                    face = Face(id=face_uuid,images_file_path=file_path)
                    self.person_manager.register_face(face)
                    
                    person = self.person_manager.find_person_by_face_uuid(face_uuid)
                    bounding_box_person_connector[bounding_box_id] = person

                # update_connections
                for id_ in bounding_box_person_connector:
                    person_id = bounding_box_person_connector[id_].id
                    updated_person = self.person_manager.get_person(person_id)
                    bounding_box_person_connector[id_] = updated_person 

                with self.processed_frame_info_lock:
                    self.processed_frame_info.bounding_boxes = bounding_boxes_with_ids
                    self.processed_frame_info.bounding_box_person_connector = bounding_box_person_connector
            
            time.sleep(0.4)
    
    def close_processing_thread(self):
        self.is_processing_thread_running = False
        self.processing_thread.join()


    
        
        