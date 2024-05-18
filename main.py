from typing import Union

import base64
import io
import json
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "S.E.T.I."}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    if file.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        return JSONResponse(content={"error": "Invalid file format. Only PDF, PNG and JPG files are allowed."}, status_code=400)

    bytes = await file.read()
    bytes_data = base64.b64encode(bytes).decode('utf-8')

    # Use OpenCV to get the text from the file
    image = cv2.imdecode(np.frombuffer(bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(image)

    return JSONResponse(content={"text": text})
