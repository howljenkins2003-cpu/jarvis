import whisper
import os

model = whisper.load_model("base")

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    return result["text"].strip()


if __name__ == "__main__":
    from listener import record_audio
    path = record_audio(duration=5)
    text = transcribe(path)
    print(f"You said: {text}")