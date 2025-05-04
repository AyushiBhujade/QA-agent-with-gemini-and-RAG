
import easyocr
from PIL import Image
from io import BytesIO

reader = easyocr.Reader(["en"])

def extract_text_from_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    result = reader.readtext(image)
    return " ".join([text for _, text, _ in result])
