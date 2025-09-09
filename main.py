from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class DocumentResponse(BaseModel):
    id: str
    filename: str
    size: int
    page_count: int
    status: str
    created_at: datetime

    class Cofing:
        from_attributes = True

class DocumentPageResponse(BaseModel):
    page_number: int 
    text: str
    chunks: list = []

class HealthResponse(BaseModel):
    status: str
    fastapi_version: str
    db_connection: bool 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/documents', response_model=DocumentResponse)
def create_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    pass

@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get('/health')
def app_health():
    return {'status':'ok'}