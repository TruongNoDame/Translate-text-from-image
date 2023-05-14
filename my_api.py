from fastapi import FastAPI, Request, File, UploadFile
# from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import json
import cv2
import numpy as np

from CRAFT_pytorch.my_CRAFT import My_CRAFT
from text_recognition.my_recogniter import Recogniter


detector =  My_CRAFT(trained_model="models/craft_mlt_25k.pth")
recogniter = Recogniter("models/TPS-ResNet-BiLSTM-CTC.pth", "TPS", "ResNet", "BiLSTM", "CTC")

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ocr")
async def ocr(image: UploadFile = File(...)):

    img = cv2.cvtColor(cv2.imdecode(np.fromstring(await image.read(), np.uint8),
     cv2.IMREAD_COLOR), cv2.COLOR_RGB2BGR)
    img = np.array(img)

    word_images = detector.detect(img)
    results = recogniter.infer(word_images)

    return {"result": results}


if __name__ == '__main__':
    import uvicorn

    app_str = 'my_api:app'
    uvicorn.run(app_str, host='localhost', port=8000, reload=True, workers=1)
