import os
import json
import time
import threading
import pygame
import webbrowser
import random
import tkinter as tk
from tkinter import PhotoImage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
KILL_IMAGE_PATH = os.path.join(RESOURCES_DIR, "cantelope.png")
KILL_SOUND_PATH = os.path.join(RESOURCES_DIR, "jackpot.ogg")

last_kills = 0
last_round = 0
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

def trigger_kill_event():
    global on_cooldown
    if not on_cooldown:
        print("[EVENT] Kill detected!")
        urls = [
            "https://stake.com",
            "https://en.gameslol.net/deal-or-no-deal-754.html",
            "https://skybet.com/",
            "https://csgoempire.com/"
        ]

        webbrowser.open_new(random.choice(urls))
        on_cooldown = True
        threading.Timer(2.0, reset_cooldown).start()  # 1-second cooldown

def reset_cooldown():
    global on_cooldown
    on_cooldown = False

def process_data_file():
    global last_kills, last_round
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid:
                 round = data.get("map", {}).get("round", 0)
                kills = data.get("player", {}).get("state", {}).get("money", 0)
                if kills - last_kills >= 1500 and round != last_round:
                    trigger_kill_event()
                    last_round = round
                    last_kills = kills
                
                elif round < last_round:
                    print("[INFO] Kill count reset.")
                    last_kills = 0
                    last_round = 0

            else:
                print("NOT ABLE TO FIRE!")
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
            time.sleep(2)
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