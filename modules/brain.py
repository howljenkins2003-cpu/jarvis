import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config import GROQ_API_KEY, MODEL
from modules.tools import AVAILABLE_TOOLS, TOOL_SCHEMAS

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant.
You are direct, efficient, and slightly cold. No unnecessary filler.
Keep responses concise — you are speaking out loud, not writing an essay.
You have access to tools for checking system status. Use them when relevant."""

conversation_history = []

def think(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        # Record the assistant's tool-call request in history
        conversation_history.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [tc.model_dump() for tc in message.tool_calls]
        })

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func = AVAILABLE_TOOLS.get(func_name)

            if func:
                args = json.loads(tool_call.function.arguments or "{}")
                if args is None:
                    args = {}
                result = func(**args)
            else:
                result = f"Error: tool '{func_name}' not found."

            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        # Second call — Groq turns the tool result into a spoken reply
        follow_up = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        )
        reply = follow_up.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    else:
        reply = message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply