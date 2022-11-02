import cv2

from aiortc import MediaStreamTrack
from av import VideoFrame
from face_detector import FaceDetector
import time
from queue import Queue
from threading import Thread

from models import FrameInfo
import numpy as np

DEFAULT_SAMPLE_PERIOD_TIME = 0.5

class VideoTransformer(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, sample_period_time=DEFAULT_SAMPLE_PERIOD_TIME):
        super().__init__()  
        self.track = track
        self.sampled_frames: Queue[np.ndarray] = Queue()
        self.processed_frame_info: FrameInfo = FrameInfo(bounding_boxes=[])
        self.last_sample_time = 0
        self.sample_period_time = sample_period_time

        self.processing_thread: Thread = Thread(target=self.processing_thread_func)
        self.is_process_thread_running: bool = True
        self.processing_thread.start()

    async def recv(self):    
        frame = await self.track.recv()
        
        current_time = time.time()
        arr = self.frame_to_ndarray(frame)
        if((current_time-self.last_sample_time)>self.sample_period_time):
            self.sampled_frames.put(arr)
            self.last_sample_time = current_time
       
        # arr = detect_faces(arr)    
        arr = FaceDetector().draw_bounding_boxes(arr,self.processed_frame_info.bounding_boxes)

        new_frame = self.ndarray_to_frame(arr,frame)
        return new_frame 

    def processing_thread_func(self):
        while self.is_process_thread_running:
            print(f"Is quueue empty{self.sampled_frames.empty()}")
                # print("In the loop")
                # frame = self.sampled_frames.get()
                # t1 = time.time()
                # self.processed_frame_info.bounding_boxes = FaceDetector().detect_faces(frame) 
                # t2 = time.time()
                # print(f"Process time: {t2-t1}")

    def frame_to_ndarray(self,frame):
        return frame.to_ndarray(format="bgr24")

    def ndarray_to_frame(self,arr,old_frame):
        new_frame = VideoFrame.from_ndarray(arr, format="bgr24")
        new_frame.pts = old_frame.pts
        new_frame.time_base = old_frame.time_base

        return new_frame