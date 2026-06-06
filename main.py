import os
import sys
os.environ["PYTHONWARNINGS"] = "ignore"
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import pyaudio
sys.stderr = stderr

import threading
from PyQt6.QtWidgets import QApplication
from modules.orb import OrbWidget, orb_signals, set_state
from modules.listener import record_audio
from modules.stt import transcribe
from modules.brain import think
from modules.tts import speak

trigger = threading.Event()
stop_event = threading.Event()

def jarvis_loop():
    set_state("idle")

    while not stop_event.is_set():
        trigger.wait()
        if stop_event.is_set():
            break
        trigger.clear()

        set_state("listening")
        audio_path = record_audio()

        set_state("thinking")
        print("Transcribing...")
        user_input = transcribe(audio_path)
        print(f"You: {user_input}")

        print("Thinking...")
        response = think(user_input)
        print(f"Jarvis: {response}")

        set_state("speaking")
        speak(response)

        set_state("idle")

    print("Jarvis shutting down.")

def main():
    print("Jarvis is ready. Left-click orb to speak, right-click to quit.\n")

    orb_signals.listen_triggered.connect(lambda: trigger.set())
    orb_signals.quit_triggered.connect(lambda: (stop_event.set(), trigger.set(), app.quit()))

    loop_thread = threading.Thread(target=jarvis_loop, daemon=True)
    loop_thread.start()

    app = QApplication(sys.argv)
    orb = OrbWidget(orb_signals)
    orb.show()
    app.exec()

if __name__ == "__main__":
    main()