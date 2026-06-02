import whisper
import os
import warnings
warnings.filterwarnings("ignore")

model = whisper.load_model("base") # loading the whisper model

def transcribe(audio_path):
    result = model.transcribe(audio_path) # transcribe the audio recorded from it's audio path provided from listner.py
    os.remove(audio_path) # to delete the file after transcribing.
    return result["text"].strip()


