import cv2

from aiortc import MediaStreamTrack
from av import VideoFrame
import time
from queue import Queue
from threading import Thread
from app.Application import Application
import numpy as np

DEFAULT_SAMPLE_PERIOD_TIME = 0.5

class VideoTransformer(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, app:Application,sample_period_time=DEFAULT_SAMPLE_PERIOD_TIME):
        super().__init__()  
        self.app = app
        self.track = track
        
    async def recv(self):    
        frame = await self.track.recv()
        arr = self.frame_to_ndarray(frame)
        self.app.update_frame(arr)
        new_frame = self.ndarray_to_frame(arr,frame)

        return new_frame

    def frame_to_ndarray(self,frame):
        return frame.to_ndarray(format="bgr24")

    def ndarray_to_frame(self,arr,old_frame):
        new_frame = VideoFrame.from_ndarray(arr, format="bgr24")
        new_frame.pts = old_frame.pts
        new_frame.time_base = old_frame.time_base

        return new_frame