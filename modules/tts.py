from gtts import gTTS
import subprocess
import os

def speak(text):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save("response.mp3")
    subprocess.run(["mpg123", "-q", "response.mp3"])
    os.remove("response.mp3")

