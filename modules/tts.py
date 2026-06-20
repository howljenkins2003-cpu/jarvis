import edge_tts
import asyncio
import subprocess
import os
import re
import uuid

VOICE = "en-GB-RyanNeural"
RATE = "+20%"

def split_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[!?])\s+', text) if s.strip()]

async def _generate(text, filename):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(filename)

async def _generate_and_play(text):
    filename = f"response_{uuid.uuid4().hex}.mp3"
    try:
        await _generate(text, filename)
        subprocess.run(["mpg123", "-q", filename])
    except Exception as e:
        print(f"[TTS error]: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

async def _speak_async(text):
    sentences = split_sentences(text)
    if not sentences:
        return

    files = [f"response_{uuid.uuid4().hex}.mp3" for _ in sentences]

    await _generate(sentences[0], files[0])

    for i in range(len(sentences)):
        if i + 1 < len(sentences):
            gen_task = asyncio.create_task(_generate(sentences[i + 1], files[i + 1]))

        subprocess.run(["mpg123", "-q", files[i]])
        if os.path.exists(files[i]):
            os.remove(files[i])

        if i + 1 < len(sentences):
            await gen_task

def speak_chunk(text):
    asyncio.run(_generate_and_play(text))

def finalize_speak():
    pass

def speak(text):
    asyncio.run(_speak_async(text))