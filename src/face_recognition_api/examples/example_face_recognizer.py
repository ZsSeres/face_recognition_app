from src.face_recognition_api.src.face_recognizer import FaceRecognizer
from PIL import Image


face_rec = FaceRecognizer()
img = Image.open(r"../assets/demo_faces/elon_02.png")
id_ = face_rec.recognize_face(img)
print(id_)