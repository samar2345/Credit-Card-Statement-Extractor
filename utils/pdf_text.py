import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def extract_text_pdf(path: str) -> str:
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ''
            text_chunks.append(text)
    return '\n'.join(text_chunks)

def extract_text_pdf_ocr(path: str, dpi: int = 300) -> str:
    images = convert_from_path(path, dpi=dpi)
    all_text = []
    for img in images:
        txt = pytesseract.image_to_string(img)
        all_text.append(txt)
    return '\n'.join(all_text)
