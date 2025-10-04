import os
import time
from pynput.keyboard import Listener, Key, Controller
from queue import Queue

TRIGGER_KEYS = ['y', 'u']
TRIGGER_LENGTH = 10
TRIGGER_TEXT = "Mucho Texto"
SOUND_NAME = "texto"
RESOURCE_FOLDER = "resources" 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")

pygame.mixer.init()
kill_sound = pygame.mixer.Sound(KILL_SOUND_PATH)

keyboard2 = Controller()
typed_chars = []
listening = False
enable_debug = True
event_queue = Queue()

def on_press(key):
    global typed_chars, listening
    try:
        if hasattr(key, 'char') and key.char:
            char_lower = key.char.lower()
            if char_lower in TRIGGER_KEYS:
                listening = True
                typed_chars.clear()
            elif listening:
                typed_chars.append(char_lower)
        elif key in [Key.enter, Key.esc]:
            typed_chars.clear()
            listening = False

        if listening and len(typed_chars) >= TRIGGER_LENGTH:
            keyboard2.press(Key.enter)
            keyboard2.release(Key.enter)
            time.sleep(0.2)
            keyboard2.press('y')
            keyboard2.release('y')
            time.sleep(0.2)
            time.sleep(0.1)
            keyboard2.type(TRIGGER_TEXT)
            kill_sound.play()
            time.sleep(0.2)
            keyboard2.press(Key.enter)
            keyboard2.release(Key.enter)
            typed_chars.clear()
            listening = False

    except Exception as e:
        print(f"[DEBUG] Error detecting keypress: {e}")
        
listener = Listener(on_press=on_press)
listener.start()
listener.join()

