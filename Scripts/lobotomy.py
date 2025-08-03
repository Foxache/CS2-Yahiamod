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
KILL_IMAGE_PATH = os.path.join(RESOURCES_DIR, "baby.png")
KILL_SOUND_PATH = os.path.join(RESOURCES_DIR, "lobotomy.mp3")

last_kills = 0
on_cooldown = False

pygame.mixer.init()
kill_sound = pygame.mixer.Sound(KILL_SOUND_PATH)

root = tk.Tk()
root.overrideredirect(True)  # Removes border/title bar
root.attributes("-topmost", True)
root.attributes("-alpha", 1.0)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

image_width = 1920
image_height = 1080

x_position = (screen_width // 2) - (image_width // 2)
y_position = (screen_height // 2) - (image_height // 2)


root.geometry(f"{image_width}x{image_height}+{x_position}+{y_position}")


overlay_image = tk.PhotoImage(file=KILL_IMAGE_PATH)
label = tk.Label(root, image=overlay_image, bg="white")
label.pack()

root.withdraw()  

def show_kill_overlay():
    root.deiconify()  # Show the overlay
    root.lift()  # Bring to front
    root.attributes("-alpha", 1.0)  
    
    def fade_step(alpha):
        if alpha > 0:
            root.attributes("-alpha", alpha)  
            root.after(100, fade_step, alpha - 0.10)  # Gradual fade effect
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
            kills = data.get("player", {}).get("match_stats", {}).get("deaths", 0)
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid:
                if kills > last_kills:
                    trigger_kill_event()
                    last_kills = kills
                
                elif kills == 0 and last_kills != 0:
                    print("[INFO] Kill count reset.")
                    last_kills = 0
                
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