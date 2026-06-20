import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config import GROQ_API_KEY, MODEL
from modules.tts import speak_chunk
import threading
import queue

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant.
You are direct, efficient, and slightly cold. No unnecessary filler.
Keep responses concise — you are speaking out loud, not writing an essay."""

conversation_history = []

def think(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        stream=True
    )

    full_response = ""
    buffer = ""
    tts_queue = queue.Queue()
    done_event = threading.Event()

    def tts_worker():
        while True:
            chunk = tts_queue.get()
            if chunk is None:
                break
            speak_chunk(chunk)
            tts_queue.task_done()
        done_event.set()

    worker = threading.Thread(target=tts_worker, daemon=True)
    worker.start()

    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token is None:
            continue
        buffer += token
        full_response += token
        print(token, end="", flush=True)

        if any(p in buffer for p in ["!", "?", ","]) and len(buffer.split()) > 6:
            tts_queue.put(buffer.strip())
            buffer = ""

    print()
    if buffer.strip():
        tts_queue.put(buffer.strip())

    # Signal worker to stop and wait for it to finish
    tts_queue.put(None)
    done_event.wait()

    conversation_history.append({"role": "assistant", "content": full_response})
    return None