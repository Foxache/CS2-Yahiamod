import json
import pygame 
import os 
import sys
import time
import webbrowser
import threading
import psutil
import queue
import tkinter as tk
from PIL import Image, ImageTk
from pynput.keyboard import Key, Controller

class Logger:
    def __init__(self, logfile):
        self.terminal = sys.stdout
        self.log = open(logfile, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

enable_debug = True
cooldown_duration = 1.0
keyboard = Controller()
last_trigger_time = 0
previous_kills = 0

def check_yahamouse_running():
    for proc in psutil.process_iter(['cmdline', 'name']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('yahamouse' in part.lower() for part in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def monitor_yahamouse():
    while True:
        if not check_yahamouse_running():
            print("[CANTALOUPE DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()
# --- Path setup ---
script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "console_log.txt")
JSON_PATH = os.path.join(script_directory, "data.json")
IMAGE_PATH = os.path.join(resources_directory, "cantelope.png")
SOUND_PATH = os.path.join(resources_directory, "cantaloupe.ogg")

# --- Logging Setup ---
sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

# --- Audio Setup ---
pygame.mixer.init()
pygame.mixer.set_num_channels(1)

# --- Tkinter + queue setup ---
event_queue = queue.Queue()
root = tk.Tk()
root.withdraw()

def play_cantaloupe():
    try:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_PATH))
    except Exception as e:
        print(f"[ERROR] Playing sound: {e}")

def show_image():
    time.sleep(0.8)
    root.deiconify()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.state("zoomed")
    root.attributes("-alpha", 1.0)

    for widget in root.winfo_children():
        widget.destroy()

    img = Image.open(IMAGE_PATH).convert("RGBA")
    image_tk = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    canvas.create_image(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, anchor="center", image=image_tk)
    canvas.image = image_tk

    event_queue.put(play_cantaloupe)
    root.after(2500, root.withdraw)

def process_queue():
    while not event_queue.empty():
        try:
            event_queue.get_nowait()()
        except queue.Empty:
            break
    root.after(5, process_queue)

def check_assists():
    global previous_kills
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)

        kills = data.get("player", {}).get("match_stats", {}).get("kills", 0)
        if kills > previous_kills:
            show_image()
        previous_Kills = kills
        

    except Exception as e:
        print(f"[ERROR] While checking assists: {e}")
        
def run_loop():
    while True:
        check_assists()
        time.sleep(0.5)


if __name__ == "__main__":
    if enable_debug:
        print("[CANTALOUPE DEBUG] Starting main loop")
    root.after(100, process_queue)
    threading.Thread(target=lambda: run_loop(), daemon=True).start()
    root.mainloop()

