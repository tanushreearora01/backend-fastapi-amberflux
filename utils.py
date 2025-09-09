import PyPDF2
import logging

logger = logging.getLogger("utils")

def extract_text_from_pdf(file_path):
    try:
        pages_text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                pages_text.append(text)
        return pages_text
    except Exception as e:
        logger.error(f"PDF read error: {e}")
        return []

def get_page_count(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except:
        return 0

def split_text_into_chunks(text, chunk_size=800):
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks