from pydub import AudioSegment  # Library for audio processing (splitting, conversion, normalization)
import logging  # For logging information and debugging messages
from io import BytesIO  # For handling in-memory file objects
import speech_recognition as sr  # Library for audio transcription
import os  # For interacting with environment variables
import google.generativeai as genai  # For using Gemini AI model
import traceback  # For detailed error tracebacks

# Configure logging to display information and errors in the terminal
logging.basicConfig(level=logging.INFO)

# Set up the Gemini API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Instantiate the GenerativeModel for Gemini AI
model = genai.GenerativeModel('gemini-2.0-flash')


def convert_mp3_to_wav(mp3_path, wav_path, normalize_audio=False):
    """
    Converts an MP3 file to WAV format, with an optional step to normalize audio.
    
    Args:
        mp3_path (str): Path to the MP3 file.
        wav_path (str): Path where the converted WAV file will be saved.
        normalize_audio (bool): Whether to normalize the audio for consistent volume.
    """
    # Load MP3 audio file
    audio = AudioSegment.from_mp3(mp3_path)
    
    # Optional normalization step to improve clarity
    if normalize_audio:
        audio = audio.normalize()
        logging.info("Audio has been normalized for consistent volume.")

    # Export the audio in WAV format
    audio.export(wav_path, format="wav")
    logging.info(f"Converted MP3 to WAV: {wav_path}")


def split_audio(audio_path, chunk_length_ms=60000):
    """
    Splits a WAV audio file into smaller chunks of specified duration.
    
    Args:
        audio_path (str): Path to the WAV file.
        chunk_length_ms (int): Length of each chunk in milliseconds.
    
    Returns:
        list: A list of AudioSegment objects representing the chunks.
    """
    # Load the WAV audio file
    audio = AudioSegment.from_wav(audio_path)

    # Normalize audio to enhance transcription accuracy
    audio = audio.normalize()
    logging.info("Audio has been normalized for chunking.")

    # Divide audio into chunks of specified length
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]  # Extract a single chunk
        chunks.append(chunk)  # Add the chunk to the list
        logging.info(f"Created chunk {len(chunks)} with duration {len(chunk)} ms.")
    
    return chunks


def transcribe_audio_chunk(chunk, chunk_index):
    """
    Transcribes a single audio chunk using Google Speech Recognition and refines it with Gemini AI.
    
    Args:
        chunk (AudioSegment): An audio chunk to be processed.
        chunk_index (int): The index of the chunk (used for logging).
    
    Returns:
        str: The transcription text, potentially refined by Gemini.
    """
    logging.info(f"Processing chunk {chunk_index} with duration {len(chunk)} ms.")

    # Check for empty or invalid chunks
    if len(chunk) == 0:
        logging.error(f"Chunk {chunk_index} is empty or corrupted.")
        return ""

    recognizer = sr.Recognizer()  # Initialize the recognizer for transcription

    try:
        # Export the chunk to an in-memory file object (BytesIO)
        audio_file = BytesIO()
        chunk.export(audio_file, format="wav")  # Save chunk as WAV in memory
        audio_file.seek(0)  # Reset the file pointer to the beginning
        
        # Use AudioFile from speech_recognition to process the in-memory file
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)  # Read and process the audio data
        
        # Transcribe the audio using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        logging.info(f"Google Speech Recognition transcription for chunk {chunk_index}: {text}")

        # Refine transcription using Gemini AI
        # prompt = f"Refine the transcription: '{text}'"
        prompt = f"Ensure this transcription reflects the original audio exactly, without changing the meaning or structure: '{text}'"

        logging.info(f"Prompt sent to Gemini: {prompt}")
        response = model.generate_content(prompt)  # Generate refined transcription
        refined_text = response.text.strip()
        logging.info(f"Gemini-refined transcription: {refined_text}")

        return refined_text

    except Exception as e:
        # Log the error along with detailed traceback for debugging
        logging.error(f"Error transcribing chunk {chunk_index}: {e}")
        logging.error(traceback.format_exc())
        return ""


def transcribe_wav_to_text(wav_path):
    """
    Splits a WAV file into chunks, transcribes each chunk, and combines the results into a full text.
    
    Args:
        wav_path (str): Path to the WAV file.
    
    Returns:
        str: The combined transcription text from all audio chunks.
    """
    chunks = split_audio(wav_path)  # Split the audio into chunks
    full_text = ""  # Initialize the variable to store the combined text

    # Iterate through each chunk and transcribe it
    for i, chunk in enumerate(chunks):
        chunk_text = transcribe_audio_chunk(chunk, i)  # Transcribe the chunk
        full_text += chunk_text + " "  # Append the chunk's transcription to the full text
        logging.info(f"Accumulated transcription after chunk {i}: {full_text.strip()}")

    return full_text.strip()


async def summarize_text(text):
    """
    Summarizes a given text using Gemini AI.
    
    Args:
        text (str): The text to be summarized.
    
    Returns:
        str: The summarized version of the text.
    """
    try:
        # Send the text to Gemini for summarization
        prompt = f"Summarize the following text in one sentence:\n{text}\n The output should be in the format- Summary: Value"
        logging.info(f"Prompt sent to Gemini for summarization: {prompt}")
        response = model.generate_content(prompt)  # Generate summary
        summary = response.text.strip()
        logging.info(f"Generated summary: {summary}")
        return summary

    except Exception as e:
        # Log errors with detailed traceback for debugging
        logging.error(f"An error occurred during text summarization: {e}")
        logging.error(traceback.format_exc())
        return "Summary generation failed."
