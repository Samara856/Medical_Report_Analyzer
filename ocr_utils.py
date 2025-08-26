import pytesseract
from PIL import Image
import platform

# OS অনুযায়ী Tesseract path set করা
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    # Linux server এ সাধারণly /usr/bin/tesseract থাকে
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)
