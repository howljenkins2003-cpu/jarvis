import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1#mono = 1 sterio = 2 we don't need sterio here.
RATE = 16000 #whisper expects the audio of sample rate 16k
OUTPUT_FILE = "input.wav"

def record_audio(duration=5):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Recording for {duration} seconds...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Done recording.")
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

