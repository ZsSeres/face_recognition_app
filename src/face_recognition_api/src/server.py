from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_utils.tasks import repeat_every

from src.face_recognition_api.src.router import router
from src.face_recognition_api.src.face_recognizer import FaceRecognizer

# Fast API config
app = FastAPI(debug=True)

@app.on_event("startup")
def on_startup():
    # Initiallise main classes
    FaceRecognizer()
    
    print("FastAPI server started")
  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(router)
