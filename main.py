import os
import sys
os.environ["PYTHONWARNINGS"] = "ignore"
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import pyaudio
sys.stderr = stderr

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from modules.orb import OrbWidget, orb_signals, set_state
from modules.listener import record_audio
from modules.stt import transcribe
from modules.brain import think
from modules.tts import speak
import threading

stop_event = threading.Event()

def jarvis_loop():
    set_state("listening")
    while not stop_event.is_set():
        audio_path = record_audio()

        set_state("thinking")
        print("Transcribing...")
        user_input = transcribe(audio_path)
        print(f"You: {user_input}")

        if any(word in user_input.lower() for word in ["exit", "goodbye", "shut down", "shutdown"]):
            print("Jarvis: Goodbye.")
            speak("Goodbye.")
            stop_event.set()
            orb_signals.quit_triggered.emit()
            break

        print("Thinking...")
        response = think(user_input)
        print(f"Jarvis: {response}")

        set_state("speaking")
        speak(response)

        set_state("listening")

    print("Jarvis shutting down.")

def main():
    global app
    print("Jarvis is online.\n")

    app = QApplication(sys.argv)
    orb = OrbWidget(orb_signals)
    orb_signals.quit_triggered.connect(app.quit)

    loop_thread = threading.Thread(target=jarvis_loop, daemon=True)
    loop_thread.start()

    orb.show()
    set_state("listening")
    app.exec()

if __name__ == "__main__":
    main()