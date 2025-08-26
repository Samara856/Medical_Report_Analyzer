import pytesseract

# Docker container Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(image_path):
    try:
        return pytesseract.image_to_string(image_path)
    except Exception as e:
        return f"OCR failed: {str(e)}"
