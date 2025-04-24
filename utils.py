from pydub import AudioSegment
import logging
from io import BytesIO
from PIL import Image
import speech_recognition as sr
import requests
import os
import google.generativeai as genai


logging.basicConfig(level=logging.INFO)

# Configure the API Key for Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Instantiate the GenerativeModel directly
model = genai.GenerativeModel('gemini-pro')



def convert_mp3_to_wav(mp3_path, wav_path):
  audio = AudioSegment.from_mp3(mp3_path)
  audio.export(wav_path, format="wav")
  logging.info(f"Converted MP3 to WAV: {wav_path}")  




  #Transcribing the audio file using Gemini Pro


def split_audio(audio_path, chunk_length_ms=60000):
  audio = AudioSegment.from_wav(audio_path)
  chunks = []
  for i in range(0, len(audio), chunk_length_ms):
    chunk = audio[i:i + chunk_length_ms]
    chunks.append(chunk)
  return chunks



def transcribe_audio_chunk(chunk, chunk_index):
  chunk_path = f"chunk_{chunk_index}.wav"
  chunk.export(chunk_path, format="wav")


  try: 
  
    with open(chunk_path, "rb") as audio_file:
      # response = openai.Audio.transcribe(
      #   model="whisperer-1",
      #   file =audio_file
      # )

      # text = response["text"]

      prompt = f"Based on the following description of an audio segment, provide a transcription of what was said: '{audio_file}'"
      response = model.generate_content(prompt)
      print(response.text)
      text = response.text
  
  except Exception as e:
    logging.error(f"An error has occurred with chunk {chunk_index}: {e}")
    text = ""

  finally:
    os.remove(chunk_path)
  return text


def transcribe_wav_to_text(wav_path):
  chunks = split_audio(wav_path)
  full_text = ""

  for i, chunk in enumerate(chunks):
    chunk_text = transcribe_audio_chunk(chunk, i)
    full_text += chunk_text + " "
    logging.info(f"Transcribed text: {full_text.strip()}") 
    return full_text.strip()


async def summarize_text(text):
  try:

  except Exception as e:
    logging.error(f"An error has occurred during text summarization: {e}")
    return "Summary generation failed"

  