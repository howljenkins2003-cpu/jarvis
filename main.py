import os
import sys
os.environ["PYTHONWARNINGS"] = "ignore"
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import pyaudio
sys.stderr = stderr # to mute the warnings in the terminal.



from modules.listener import record_audio
from modules.stt import transcribe
from modules.brain import think
from modules.tts import speak

def main():
    print("Jarvis is ready. Press Enter to speak, Ctrl+C to exit.\n")
    
    while True:
        input("Press Enter to speak...")
        
        audio_path = record_audio()
        
        print("Transcribing...")
        user_input = transcribe(audio_path)
        print(f"You: {user_input}")
        
        print("Thinking...")
        response = think(user_input)
        print(f"Jarvis: {response}")
        
        speak(response)

if __name__ == "__main__":
    main()
