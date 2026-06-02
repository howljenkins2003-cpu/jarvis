import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#as config file is on root folder this is used to access that

from groq import Groq
from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant. 
You are direct, efficient, and slightly cold. No unnecessary filler. 
Keep responses concise — you are speaking out loud, not writing an essay."""

conversation_history = []

def think(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    
    return reply