import os
from groq import Groq
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def transcribe(audio_path):
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=(audio_path, f.read()),
            model="whisper-large-v3-turbo",
            response_format="text"
        )
    os.remove(audio_path)
    return result.strip()