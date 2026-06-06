Here's the full `README.md`:

```markdown
# Jarvis — Personal AI Voice Assistant

A personal AI voice assistant built in Python on Ubuntu. Speaks, listens, thinks, and responds continuously. Features an animated orb as visual presence.

---

## Features
- Continuous voice conversation — no button pressing
- Animated orb with state indicators (listening, thinking, speaking, idle)
- Direct, efficient personality via system prompt
- Auto-exits on voice command ("Jarvis exit")

---

## Tech Stack
- **STT** — OpenAI Whisper (base model, CPU)
- **Brain** — Groq API (llama-3.3-70b-versatile)
- **TTS** — edge-tts (en-GB-RyanNeural) + mpg123
- **Mic input** — PyAudio + numpy RMS detection
- **Orb** — PyQt6

---

## Requirements

### System dependencies
```bash
sudo apt install ffmpeg mpg123
```

### Python dependencies
```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/howljenkins2003-cpu/jarvis.git
cd jarvis
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Setup alias (optional but recommended)
Add this to your `~/.bashrc`:
```bash
alias jarvis='cd ~/Desktop/Bibek/jarvis && source venv/bin/activate && python main.py'
```
Then reload:
```bash
source ~/.bashrc
```

---

## Usage

### Run
```bash
jarvis
```
Or without alias:
```bash
cd jarvis
source venv/bin/activate
python main.py
```

Jarvis starts listening immediately. Speak naturally. Jarvis responds and keeps listening.

### Stop
Say **"Jarvis exit"** or **"Jarvis shutdown"** to quit cleanly.
Or right-click the orb → Quit.

---

## Project Structure
```
jarvis/
├── main.py              # entry point
├── config.py            # API keys and settings
├── .env                 # API keys — never commit this
├── requirements.txt
├── README.md
└── modules/
    ├── stt.py           # speech to text (Whisper)
    ├── tts.py           # text to speech (edge-tts)
    ├── brain.py         # LLM API call (Groq)
    ├── listener.py      # mic input and audio capture
    └── orb.py           # animated orb (PyQt6)
```

---

## Versioning
- **v0** — project skeleton ✅
- **v1** — working voice loop ✅
- **v1.5** — conversation memory + edge-tts ✅
- **v2** — animated orb + continuous conversation ✅
- **v3** — wake word (planned)
- **v4** — system control tools (planned)
- **v5+** — web search, file reading, ESP32/RC car, home automation (planned)

---

## Notes
- Runs on Ubuntu with X11
- CPU only (no GPU required)
- Python 3.14+
- Groq API key required (free tier available at console.groq.com)
```
