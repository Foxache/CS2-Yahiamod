import os
import json
import time
import threading
import pygame
import tkinter as tk
from tkinter import PhotoImage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
KILL_IMAGE_PATH = os.path.join(RESOURCES_DIR, "lemur.png")
KILL_SOUND_PATH = os.path.join(RESOURCES_DIR, "lemur.mp3")

last_kills = 0
on_cooldown = False

pygame.mixer.init()
kill_sound = pygame.mixer.Sound(KILL_SOUND_PATH)

root = tk.Tk()
root.overrideredirect(True)  # Removes border/title bar
root.attributes("-topmost", True)
root.state("zoomed")
root.attributes("-alpha", 1.0)

overlay_image = PhotoImage(file=KILL_IMAGE_PATH)
label = tk.Label(root, image=overlay_image, bg="white")
label.pack()
root.withdraw()  # Hide initially

def show_kill_overlay():
    root.deiconify()  # Show the overlay
    root.lift()  # Bring to front
    root.attributes("-alpha", 1.0)  
    
    def fade_step(alpha):
        if alpha > 0:
            root.attributes("-alpha", alpha)  
            root.after(100, fade_step, alpha - 0.06)  # Gradual fade effect
        else:
            root.withdraw()  
            
    root.after(1000, fade_step,1.0)

def trigger_kill_event():
    global on_cooldown
    if not on_cooldown:
        print("[EVENT] Death detected!")
        kill_sound.play()
        show_kill_overlay()
        on_cooldown = True
        threading.Timer(10.0, reset_cooldown).start()  # 1-second cooldown

def reset_cooldown():
    global on_cooldown
    on_cooldown = False

def process_data_file():
    global last_kills
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            flashed = data.get("player", {}).get("state", {}).get("flashed", 0)
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid:
                if flashed > 0:
                    trigger_kill_event()
                    
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON data.")

class DataFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("data.json"):
            process_data_file()


observer = Observer()
observer.schedule(DataFileHandler(), path=SCRIPT_DIR, recursive=False)

def start_observer():
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[EXIT] Manual interrupt received.")
    finally:
        observer.stop()
        observer.join()
        print("[EXIT] Observer stopped.")

observer_thread = threading.Thread(target=start_observer, daemon=True)
observer_thread.start()

root.mainloop()

print("[EXIT] Script fully terminated.")