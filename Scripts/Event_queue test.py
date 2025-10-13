import os
import json
import asyncio
import time
import threading
import random
import pygame
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk
import subprocess

    # revising scripts into one, testing a 

    # watchdog reads data
    # data is compared against values 
    # events that are fired should be appended to an events queue
    # order of importance dictated by index 
    # index determined by order of the code , highest priority added first.
    # will always be done chronologically 

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")

VICTORY_IMAGE_PATH = os.path.join(RESOURCES_DIR, "cinema.png")
VICTORY_SOUND_PATH = os.path.join(RESOURCES_DIR, "boom.mp3")
DEFEAT_SOUND_PATH = os.path.join(RESOURCES_DIR, "tf2.mp3")
FLASH_IMAGE_PATH = os.path.join(RESOURCES_DIR, "lemur.png")
FLASH_SOUND_PATH = os.path.join(RESOURCES_DIR, "lemur.mp3")

KILL_PATHS = [
    {"image": "cantelope.png", "sound": "cantaloupe.ogg"},
    {"image": "pineapple.png", "sound": "pineapple.ogg"},
    {"image": "cinema.png", "sound": "boom.mp3"},
    {"image": "sins.png", "sound": "sins.wav"}
]
DEATH_PATHS = [
    {"image": "baby.png", "sound": "lobotomy.mp3"},
    {"image": "nananaboobooboo.png", "sound": "gmod.mp3"},
    {"image": "awesome.png", "sound": "awesome.mp3"},
    {"image": "sleep.png", "sound": "sleep.mp3"}
]

# defining used variables
last_kills = 0
last_death = 0
on_cooldown = False
event_queue = []

pygame.mixer.init()

root = tk.Tk()
root.overrideredirect(True)  # No border/title
root.attributes("-topmost", True) # Keeps priority
root.attributes("-alpha", 0.0)  # Start invisible

# Screen geometry
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image_width = 1920
image_height = 1080
x_position = (screen_width // 2) - (image_width // 2)
y_position = (screen_height // 2) - (image_height // 2)
root.geometry(f"{image_width}x{image_height}+{x_position}+{y_position}")

# Pre-loading images to avoid a change while image is still visible to user.
preloaded_images = {}

def preload_image(path):
    if not os.path.exists(path):
        print(f"[ERROR] Image not found: {path}")
        return None
    pil_img = Image.open(path).convert("RGBA")
    return ImageTk.PhotoImage(pil_img)

# Preload all resources
preloaded_images[VICTORY_IMAGE_PATH] = preload_image(VICTORY_IMAGE_PATH)
preloaded_images[FLASH_IMAGE_PATH] = preload_image(FLASH_IMAGE_PATH)

for item in KILL_PATHS + DEATH_PATHS:
    full_path = os.path.join(RESOURCES_DIR, item["image"])
    preloaded_images[full_path] = preload_image(full_path)

label = tk.Label(root, bg="black", borderwidth=0, highlightthickness=0)
label.pack()

root.withdraw() # hides root to prevent preloading from showing any images

def reset_cooldown():
    global on_cooldown
    on_cooldown = False

def process_event_queue(event_queue):
    for item in event_queue:
        asyncio.run(globals()[item]())
    
async def kill():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.5)
    selected = random.choice(KILL_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images[img]
    show_overlay(img_obj, snd)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def flash():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.5)
    img_obj = preloaded_images[FLASH_IMAGE_PATH]
    sound_path = FLASH_SOUND_PATH
    show_overlay(img_obj, sound_path)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def death():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.5)
    selected = random.choice(DEATH_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images.get(img)

    if img_obj is None:
        print(f"[ERROR] Preloaded image missing: {img}")
        return

    show_overlay(img_obj, snd)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def win():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.5)
    img_obj = preloaded_images[VICTORY_IMAGE_PATH]
    show_overlay(img_obj, VICTORY_SOUND_PATH)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

def show_overlay(image_obj, sound_path):
    root.deiconify()
    root.lift()
    label.config(image=image_obj)
    label.image = image_obj

    pygame.mixer.Sound(sound_path).play()

    def fade_in(alpha=0.0):
        if alpha < 1.0:
            root.attributes("-alpha", alpha)
            root.after(10, fade_in, alpha + 0.05)
        else:
            root.attributes("-alpha", 1.0)
            root.after(2500, fade_out, 1.0)

    def fade_out(alpha):
        if alpha > 0:
            root.attributes("-alpha", alpha)
            root.after(10, fade_out, alpha - 0.05)
        else:
            root.attributes("-alpha", 0.0)
            root.withdraw()  

    fade_in()

# Processing data file , just making event queue
def process_data_file():
    global last_death, last_kills, event_queue
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            steamid = data.get("provider", {}).get("steamid", 1) # steam id to ensure the data collected is about the player
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid: # Data collection
                deaths = data.get("player", {}).get("match_stats", {}).get("deaths", 0)
                kills = data.get("player", {}).get("match_stats", {}).get("kills", 0)
                team = data.get("player", {}).get("team", "NaN")
                ct = data.get("map", {}).get("team_ct", {}).get("score", 0)
                t = data.get("map", {}).get("team_t", {}).get("score", 0)
                flashed = data.get("player", {}).get("state", {}).get("flashed", 0)
                activity = data.get("player", {}).get("activity", "none")

                if deaths > last_death:
                    event_queue.append("death")
                    if random.random() < 0.01:
                        subprocess.run(["start", "steam://run/2379780"], shell=True)
                
                if flashed > 0:
                    event_queue.append("flash")

                if kills > last_kills:
                    event_queue.append("kill")

                if ct == 13: # working?
                    if team.upper() == "CT":
                        event_queue.append("win")
                    else: # this can stay as non-event queue , it does not show an image
                        pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()

                if t == 13:
                    if team.upper() == "T":
                        event_queue.append("win")
                    else: 
                        pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                
                process_event_queue(event_queue)
                last_death = deaths
                last_kills = kills
                
                if activity == "menu":
                    print("[INFO] Kill count reset.")
                    last_kills = 0
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON data.")    
    
# Watchdog on data.json 

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