from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from io import BytesIO
from pydub import AudioSegment
from PIL import Image
import logging
import speech_recognition as sr
import requests
import google.generativeai as genai
from schemas import LyricsPayload



# Configure the API Key for Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Instantiate the GenerativeModel directly
model = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

logging.basicConfig(level=logging.INFO)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


if not os.path.exists("converted_files"):
    os.makedirs("converted_files")
    

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request":{} })   


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), prompt: str = Form(...)):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    #AUDIO PROCESSING
    wav_file_location = f"converted_files/{file.filename.replace('.mp3', '.wav')}"

    #TODO : CONVERT .MP3 TO .WAV