# utils.py
import PyPDF2
import config

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        pages_text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                pages_text.append(text)
        return pages_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

def get_page_count(file_path):
    """Get number of pages in PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except:
        return 0

def split_text_into_chunks(text):
    """Split long text into smaller chunks"""
    if len(text) <= config.CHUNK_SIZE:
        return [text]
    
    chunks = []
    for i in range(0, len(text), config.CHUNK_SIZE):
        chunk = text[i:i + config.CHUNK_SIZE]
        chunks.append(chunk)
    return chunks

# def check_api_key(provided_key):
#     """Check if API key is valid"""
#     if config.API_KEY is None:
#         return True  # No API key required
#     return provided_key == config.API_KEY