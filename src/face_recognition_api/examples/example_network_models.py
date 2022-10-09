from src.shared.network_models import RecognizeFaceRequest
from src.shared.image_transfer_converter import ImageTransferConverter

from PIL import Image
from PIL.PngImagePlugin import PngImageFile


# Sending
# Docs-nál csekkolni, hogy felismeri-e a file feltöltést
img = Image.open(r"../assets/demo_faces/elon_01.png")
encoded_bytes=ImageTransferConverter.encode_img(img)
req = RecognizeFaceRequest(encoded_image_bytes = encoded_bytes)
json = req.json()

# Receive
resp=RecognizeFaceRequest.parse_raw(json)
rec_img = ImageTransferConverter.decode_bytes(resp.encoded_image_bytes)
rec_img.show()