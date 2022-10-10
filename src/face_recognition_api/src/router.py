from fastapi import APIRouter

from src.shared.network_models import RecognizeFaceRequest,RecognizeFaceResponse,DetectFacesRequest,DetectFacesResponse
from src.shared.image_transfer_converter import ImageTransferConverter
from src.face_recognition_api.src.face_recognizer import FaceRecognizer
from  src.face_recognition_api.src.face_detector import detect_faces

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/recognize_face",response_model=RecognizeFaceResponse)
async def recognize_face(body: RecognizeFaceRequest)->RecognizeFaceResponse:
    img = ImageTransferConverter.decode_bytes(body.encoded_image_bytes)
    face_uuid = FaceRecognizer().recognize_face(img)

    resp = RecognizeFaceResponse(face_uuid=face_uuid)
    return resp


@router.post("/detect_faces",response_model=DetectFacesResponse)
async def detect_faces(body: DetectFacesRequest)->DetectFacesResponse:
    img = ImageTransferConverter.decode_bytes(body.encoded_image_bytes)

    img.show()

    face_bounding_boxes = detect_faces(img)
    resp = DetectFacesResponse(face_bounding_boxes=face_bounding_boxes)

    return resp