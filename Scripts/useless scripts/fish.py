import time
import json
import random
import threading
import queue
import os
import sys
import pygame
import tkinter as tk
from PIL import Image, ImageTk
from pynput import mouse, keyboard  # Added keyboard
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

print("[FISH DEBUG] Pygame Mixer Init")
pygame.mixer.init()

print("[FISH DEBUG] Script Paths")
script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
log_path = os.path.join(log_directory, "console_log.txt")

sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

IMAGE_PATH_FISH = os.path.join(resources_directory, "fishondafloo.png")
SOUND_PATH_FISH = os.path.join(resources_directory, "fish.mp3")
JSON_PATH = os.path.join(resources_directory, "round_data.json")

print("[FISH DEBUG] Event Queue")
event_queue = queue.Queue()

print("[FISH DEBUG] TKinter Root")
root = tk.Tk()
root.withdraw()

print("[FISH DEBUG] Variables")
mouse_pressed = False
fish_rng = random.randint(1, 10)
current_round = 0
last_click_time = 0

def on_key_press(key):
    try:
        if key == Key.f12:
            print("[FISH DEBUG] Kill switch (F12) pressed. Exiting...")
            os._exit(0)
    except Exception as e:
        print(f"[FISH DEBUG] Key press error: {e}")

def start_keyboard_listener():
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()

print("[FISH DEBUG] get_current_round ")
def get_current_round():
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
            return data.get("current_round", 0)
    except FileNotFoundError:
        return 0

print("[FISH DEBUG] update round")
def update_round():
    global current_round
    while True:
        new_round = get_current_round()
        if new_round != current_round:
            current_round = new_round
            print(f"Updated current_round: {current_round}")
        time.sleep(1)

print("[FISH DEBUG] Round updating in separate thread")
round_thread = threading.Thread(target=update_round, daemon=True)
round_thread.start()

print("[FISH DEBUG] Sound")
def play_sound_fish():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_PATH_FISH))

print("[FISH DEBUG] Fish")
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

    threading.Thread(target=play_sound_fish).start()
    root.after(2500, lambda: root.withdraw())

def on_click(x, y, button, pressed):
    global mouse_pressed, fish_rng, current_round, last_click_time

    if button == mouse.Button.left:
        if pressed and not mouse_pressed and time.time() - last_click_time > 0.3:
            mouse_pressed = True
            last_click_time = time.time()
            print("[FISH DEBUG] Click Detected")

            if current_round == fish_rng and not event_queue.qsize():
                event_queue.put(lambda: root.after(1000, fish))
        elif not pressed:
            mouse_pressed = False

print("[FISH DEBUG] Listener Def")
def start_listeners():
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

print("[FISH DEBUG] Start listening for mouse")
listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()

print("[FISH DEBUG] Start listening for kill switch")
keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
keyboard_thread.start()

print("[FISH DEBUG] TKinter mainloop")
root.mainloop()
