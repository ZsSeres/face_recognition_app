from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.app.backend.src.frontend_router import frontend_router

# Fast API config
app = FastAPI(debug=True)

@app.on_event("startup")
def on_startup():
    print("FastAPI server started")
  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(frontend_router)