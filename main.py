from fastapi import FastAPI
from pydantic import BaseModel
from typing import List



app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get('/health')
def app_health():
    return {'status':'ok'}