from PIL import Image
from src.face_recognition_api.src.face_detector import detect_faces

img = Image.open(r"../assets/demo_faces/elon_01.png")
face_bounding_boxes = detect_faces(img)

for face_bounding_box in face_bounding_boxes:
    cropped_img = img.crop(face_bounding_box.to_tuple())
    cropped_img.show()
