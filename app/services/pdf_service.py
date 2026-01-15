from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf = PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF Extract Error: {e}")
        return ""