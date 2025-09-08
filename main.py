from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

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

@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get('/health')
def app_health():
    return {'status':'ok'}