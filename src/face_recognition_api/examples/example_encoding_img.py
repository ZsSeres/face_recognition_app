import base64
from PIL import Image
import base64
from io import BytesIO

# Encoding
img = Image.open(r"../assets/demo_faces/elon_01.png")
buffered = BytesIO()
img.save(buffered, format="PNG")
img_size = img.size
img_str = base64.b64encode(buffered.getvalue())

buff = BytesIO(img_str)
img2 = Image.open(buff.getbuffer())
img2.show()

# img2 = Image.open(img_str)
# img2.show()
# encoded_bytes = bytes(img_str)
# print(type(img_str))


