import edge_tts
import asyncio
import subprocess
import os

VOICE = "en-GB-RyanNeural" # ryan voice.

async def _speak_async(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("response.mp3")
    subprocess.run(["mpg123", "-q", "response.mp3"])
    os.remove("response.mp3")

def speak(text):
    asyncio.run(_speak_async(text))

