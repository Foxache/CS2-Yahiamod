import time
import json
import random
import threading
import queue
import os
import sys
import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pynput import mouse, keyboard
from pynput.keyboard import Key

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

script_directory = os.path.dirname(os.path.abspath(__file__))
log_directory = os.path.join(script_directory, "logs")
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "console_log.txt")
sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

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
            print("[FISH DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()

try:
    pygame.mixer.init()
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Failed to initialize sound: {e}")
    sys.exit(1)

resources_directory = os.path.join(script_directory, "resources")
IMAGE_PATH_FISH = os.path.join(resources_directory, "fishondafloo.png")
SOUND_PATH_FISH = os.path.join(resources_directory, "fish.mp3")
JSON_PATH = os.path.join(script_directory, "data.json")

event_queue = queue.Queue()

root = tk.Tk()
root.withdraw()

mouse_pressed = False
fish_rng = random.randint(1, 10)
current_round = 0
last_click_time = 0

# --- Helper to run functions in daemon threads with exception logging ---
def run_in_thread(target):
    def wrapper():
        try:
            target()
        except Exception as e:
            print(f"[THREAD ERROR] {e}", file=sys.stderr)
    threading.Thread(target=wrapper, daemon=True).start()

def get_current_round():
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
            return data.get("map", {}).get("round", 0)
    except FileNotFoundError:
        return 0

def update_round():
    global current_round
    while True:
        new_round = get_current_round()
        if new_round != current_round:
            current_round = new_round
            print(f"Updated current_round: {current_round}")
        time.sleep(1)

# --- Sound and Visual Fish Effect ---
def play_sound_fish():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_PATH_FISH))

def fish():
    root.deiconify()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.state("zoomed")

    for widget in root.winfo_children():
        widget.destroy()

    img = Image.open(IMAGE_PATH_FISH).convert("RGBA")
    image_tk = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    canvas.create_image(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, anchor="center", image=image_tk)
    canvas.image = image_tk

    run_in_thread(play_sound_fish)
    root.after(2500, root.withdraw)

# --- Mouse Listener ---
def on_click(x, y, button, pressed):
    global mouse_pressed, fish_rng, current_round, last_click_time

    if button == mouse.Button.left:
        if pressed and not mouse_pressed and time.time() - last_click_time > 0.3:
            mouse_pressed = True
            last_click_time = time.time()
            print("[FISH DEBUG] Click Detected")

            if current_round == fish_rng and event_queue.empty():
                event_queue.put(lambda: root.after(1000, fish))
        elif not pressed:
            mouse_pressed = False

def start_listeners():
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    # Do NOT join() here, keep thread running in background

# --- Start Threads ---
run_in_thread(update_round)
run_in_thread(start_listeners)

# --- Start TK mainloop ---
root.mainloop()
