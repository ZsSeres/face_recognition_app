from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.app.backend.src.frontend_router import frontend_router
from src.app.backend.src.PersonManager import PersonManager
from src.app.backend.src.APIManager import APIManager

# Fast API config
app = FastAPI(debug=True)   

@app.on_event("startup")
def on_startup():
    #Initialization of Singletons
    PersonManager()
    APIManager()
    
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