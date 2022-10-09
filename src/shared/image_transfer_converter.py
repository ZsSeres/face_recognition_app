from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from io import BytesIO
import base64

class ImageTransferConverter:
    @staticmethod
    def encode_img(img: PngImageFile)->bytes:
        buffered = BytesIO()
        img.save(buffered,format="PNG")
        
        return base64.b64encode(buffered.getvalue())
    
    @staticmethod
    def decode_bytes(encoded_bytes: bytes)->PngImageFile:
        decoded_bytes = base64.b64decode(encoded_bytes)
        buffered = BytesIO(decoded_bytes)
        
        return Image.open(buffered)