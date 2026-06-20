from dotenv import load_dotenv
import os

load_dotenv()

#brain and stt
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

#voice 
FISH_API_KEY = os.getenv("FISH_API_KEY")
FISH_VOICE_ID = "e0d7279559794041979dcd8d4409d713"



TTS_LANGUAGE = "en"
TTS_SLOW = False