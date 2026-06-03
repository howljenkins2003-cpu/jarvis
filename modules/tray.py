import os
os.environ['PYSTRAY_BACKEND'] = 'appindicator'

import pystray
from PIL import Image, ImageDraw
import threading

def create_icon():
    img = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 56, 56), fill=(0, 120, 255))
    return img

def start_tray(trigger: threading.Event, stop_event: threading.Event):
    def on_listen(icon, item):
        trigger.set()

    def on_quit(icon, item):
        stop_event.set()
        icon.stop()

    icon = pystray.Icon(
        "Jarvis",
        create_icon(),
        "Jarvis",
        menu=pystray.Menu(
            pystray.MenuItem("Listen", on_listen),
            pystray.MenuItem("Quit", on_quit)
        )
    )
    icon.run()