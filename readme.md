# Lyrics Extractor and Image Generator Web Application

## Project Description
The **Lyrics Extractor and Image Generator** web application is a comprehensive tool designed to transform audio files into visual art. Leveraging advanced speech recognition and state-of-the-art AI models, this application allows users to:
- Upload MP3 files.
- Transcribe the audio into text.
- Summarize the content.
- Generate visually appealing images based on the summarized text.

---

## Features

1. **MP3 to Text Transcription**  
   - Users can upload MP3 files which are then converted to WAV format for processing.  
   - The application uses Google's speech recognition to accurately transcribe the audio content into text.

2. **Text Summarization**  
   - After transcription, the full text is summarized into a concise, single-sentence description using OpenAI's GPT-3.5-turbo model.  
   - Provides a clear and succinct representation of the audio content.

3. **AI-Powered Image Generation**  
   - The summarized text is used as a prompt to generate high-quality images using OpenAI's DALL-E model.  
   - The images visually align with the summarized content, offering a creative representation of the audio input.

4. **User-Friendly Interface**  
   - A clean and intuitive HTML interface allows users to easily upload files, select languages, and view results.  
   - Ensures a seamless experience from audio upload to image generation.

5. **Dynamic Feedback**  
   - Displays the transcribed text, summarized content, and generated image in a well-organized format.  
   - Provides immediate feedback on the transcription and image generation process.

---

## Technical Specifications

- **Backend:** Built with FastAPI to handle file uploads, audio conversion, transcription, summarization, and image generation.  
- **Frontend:** HTML interface using jQuery for dynamic content updates and form handling.  
- **Speech Recognition:** Utilizes the `speech_recognition` and `pydub` libraries for audio processing and transcription.  
- **AI Integration:** Employs OpenAI's API for both text summarization (using GPT-3.5-turbo) and image generation (using DALL-E).  
- **File Handling:** Efficiently manages uploaded and converted files, with automated cleanup after processing.  
- **Environment Configuration:** Uses `python-dotenv` to manage API keys and other configuration settings.

---

## How It Works

1. **Upload:** Users upload an MP3 file via the web interface.  
2. **Conversion:** The application converts the MP3 file to WAV format.  
3. **Transcription:** The audio content is transcribed into text using Google's speech recognition.  
4. **Summarization:** The transcribed text is summarized into a concise description.  
5. **Image Generation:** An image is generated based on the summarized text using OpenAI's DALL-E model.  
6. **Display:** The full transcription, summary, and generated image are displayed on the web interface.

---

> *This project demonstrates the power of combining speech recognition with advanced AI models to create a unique and engaging user experience. The resulting images offer a visual interpretation of audio content, opening new avenues for creativity and expression.*
