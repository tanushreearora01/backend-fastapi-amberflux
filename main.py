from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks, Query, Header
from pydantic import BaseModel, ConfigDict
from fastapi.responses import FileResponse
from typing import Annotated
from sqlalchemy import text
from datetime import datetime
from models import Document, DocumentPage
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
import uuid
import shutil
import utils
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("app")


app = FastAPI()
models.Base.metadata.create_all(bind=engine)




class DocumentResponse(BaseModel):
    id: str
    filename: str
    size: int
    page_count: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentPageResponse(BaseModel):
    page_number: int 
    text: str
    chunks: list = []

class HealthResponse(BaseModel):
    status: str
    fastapi_version: str
    db_connection: bool 

class SearchResult(BaseModel):
    document_id: str
    filename: str
    page_number: int
    text_snippet: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def process_document_task(document_id: str, file_path: str):
    try:
        logger.info(f"Processing document: {document_id}")
        db = SessionLocal()
        
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            logger.error(f"Document not found: {document_id}")
            return
        
        pages_text = utils.extract_text_from_pdf(file_path)
        
        if not pages_text:
            document.status = "failed"
            db.commit()
            logger.error(f"Failed to extract text from: {document_id}")
            return
        
        for page_num, page_text in enumerate(pages_text, 1):
            chunk_size = int(os.getenv("CHUNK_SIZE", "800"))
            chunks = utils.split_text_into_chunks(page_text, chunk_size)
            
            for chunk_index, chunk in enumerate(chunks):
                page_record = DocumentPage(
                    document_id=document_id,
                    page_number=page_num,
                    text=chunk,
                    chunk_index=chunk_index
                )
                db.add(page_record)
        
        document.status = "ready"
        db.commit()
        db.close()
        
        logger.info(f"Document processed: {document_id}")
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        try:
            db = next(get_db())
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                document.status = "failed"
                db.commit()
            db.close()
        except:
            pass

def verify_api_key(x_api_key: str = Header(None)):
    api_key = os.getenv("API_KEY", "your-secret-key-here")
    if not x_api_key or x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.post("/documents", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _api_key_valid: bool = Depends(verify_api_key)
):
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    max_file_size = int(os.getenv("MAX_FILE_SIZE", "MAX_FILE_SIZE"))
    if file.size and file.size > max_file_size:
        logger.warning(f"File too large: {file.size} bytes")
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        document_id = str(uuid.uuid4())
        file_extension = ".pdf"
        storage_filename = f"{document_id}{file_extension}"
        file_path = os.path.join(os.getenv("STORAGE_FOLDER", str(Path.cwd() / "storage")), storage_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        page_count = utils.get_page_count(file_path)
        file_size = os.path.getsize(file_path)
        
        document = Document(
            id=document_id,
            filename=file.filename,
            size=file_size,
            page_count=page_count,
            status="processing"
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        
        background_tasks.add_task(process_document_task, document_id, file_path)
        
        logger.info(f"Document uploaded: {file.filename}")
        
        return DocumentResponse.model_validate(document)
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

@app.get("/documents", response_model=list[DocumentResponse])
async def get_documents(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    documents = db.query(Document).offset(offset).limit(limit).all()
    return [DocumentResponse.model_validate(doc) for doc in documents]

@app.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentResponse.model_validate(document)

@app.get("/documents/{document_id}/pages/{page_number}", response_model=DocumentPageResponse)
async def get_document_page(
    document_id: str, 
    page_number: int, 
    db: Session = Depends(get_db),
    _api_key_valid: bool = Depends(verify_api_key)
):

    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    page_chunks = db.query(DocumentPage).filter(
        DocumentPage.document_id == document_id,
        DocumentPage.page_number == page_number
    ).order_by(DocumentPage.chunk_index).all()
    
    if not page_chunks:
        raise HTTPException(status_code=404, detail="Page not found")
    
    full_text = ""
    chunks = []
    for chunk in page_chunks:
        full_text += chunk.text
        chunks.append(chunk.text)
    
    return DocumentPageResponse(
        page_number=page_number,
        text=full_text,
        chunks=chunks if len(chunks) > 1 else []
    )

@app.delete("/documents/{document_id}")
async def delete_document(
    document_id: str, 
    db: Session = Depends(get_db),
    _api_key_valid: bool = Depends(verify_api_key)
):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        file_extension = ".pdf"
        storage_filename = f"{document_id}{file_extension}"
        file_path = os.path.join(os.getenv("STORAGE_FOLDER", str(Path.cwd() / "storage")), storage_filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        

        db.delete(document)
        db.commit()
        
        logger.info(f"Document deleted: {document.filename}")
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Delete failed")

@app.get("/documents/{document_id}/download")
async def download_document(
    document_id: str, 
    db: Session = Depends(get_db),
    _api_key_valid: bool = Depends(verify_api_key)
):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_extension = ".pdf"
    storage_filename = f"{document_id}{file_extension}"
    file_path = os.path.join(os.getenv("STORAGE_FOLDER", str(Path.cwd() / "storage")), storage_filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=document.filename,
        media_type='application/pdf'
    )

@app.get("/search", response_model=list[SearchResult])
async def search_documents(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _api_key_valid: bool = Depends(verify_api_key)
):
    logger.info(f"Search: '{q}'")
    search_term = f"%{q.lower()}%"
    
    results = db.query(DocumentPage, Document).join(Document).filter(
        DocumentPage.text.ilike(search_term)
    ).limit(limit).all()
    
    search_results = []
    for page, document in results:
        text_lower = page.text.lower()
        search_lower = q.lower()
        
        pos = text_lower.find(search_lower)
        if pos >= 0:
            start = max(0, pos - 50)
            end = min(len(page.text), pos + len(q) + 50)
            snippet = page.text[start:end]
            
            if start > 0:
                snippet = "..." + snippet
            if end < len(page.text):
                snippet = snippet + "..."
        else:
            snippet = page.text[:100] + "..."
        
        search_results.append(SearchResult(
            document_id=document.id,
            filename=document.filename,
            page_number=page.page_number,
            text_snippet=snippet
        ))
    
    return search_results

@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    db_working = True
    try:
        db.execute(text("SELECT 1"))
    except:
        db_working = False
    
    return HealthResponse(
        status = "healthy" if db_working else "unhealthy",
        fastapi_version="0.104.1",
        db_connection = db_working
    )