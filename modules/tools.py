import psutil

def get_system_status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()

    result = f"CPU usage: {cpu}%. RAM usage: {ram}%."
    if battery:
        plugged = "plugged in" if battery.power_plugged else "on battery"
        result += f" Battery at {battery.percent}%, {plugged}."
    else:
        result += " No battery detected (desktop system)."

    return result

# Maps tool name -> actual python function
AVAILABLE_TOOLS = {
    "get_system_status": get_system_status,
}

# Schemas Groq needs to know these tools exist
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "Get current CPU usage, RAM usage, and battery status of the computer.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]