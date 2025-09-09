import logging
import PyPDF2
from typing import List, Optional

logger = logging.getLogger("utils")

def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Returns a list of page texts. Empty string for pages with no extractable text.
    """
    try:
        pages_text: List[str] = []
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text() or ""   # guard None
                pages_text.append(text)
        return pages_text
    except Exception as e:
        logger.error(f"PDF read error: {e}")
        return []

def get_page_count(file_path: str) -> int:
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)
    except Exception:
        return 0

def split_text_into_chunks(text: Optional[str], chunk_size: int = 800) -> List[str]:
    text = text or ""  # guard None
    if len(text) <= chunk_size:
        return [text]
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
