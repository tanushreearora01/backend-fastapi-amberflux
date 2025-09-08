from fastapi import FastAPI
from pydantic import BaseModel
from typing import List



app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Hello World'}