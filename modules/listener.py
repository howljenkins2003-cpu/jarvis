import pyaudio
import wave
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1#mono = 1 sterio = 2 we don't need sterio here.
RATE = 16000 #whisper expects the audio of sample rate 16k
OUTPUT_FILE = "input.wav"
SILENCE_THRESHOLD = 1000
SILENCE_DURATION = 2

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")
    frames = []
    silent_chunks = 0
    started = False #ignore the initial silence (waits for us to talk)

    while True:
        data = stream.read(CHUNK)
        volume = np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16).astype(np.float32)**2))
        if volume > SILENCE_THRESHOLD:
            started = True
            silent_chunks = 0
            frames.append(data)
        elif started:
            silent_chunks += 1
            frames.append(data)
            if silent_chunks > int(RATE / CHUNK * SILENCE_DURATION):
                break

    print("Done.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(OUTPUT_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return OUTPUT_FILE
