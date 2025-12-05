import os
import json
import asyncio
import time
import threading
import random
import win32gui, win32con
import pygame
import tkinter as tk
from ctypes import windll
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")

VICTORY_IMAGE_PATH = os.path.join(RESOURCES_DIR, "cinema.png")
VICTORY_SOUND_PATH = os.path.join(RESOURCES_DIR, "boom.mp3")
DEFEAT_SOUND_PATH = os.path.join(RESOURCES_DIR, "tf2.mp3")
FLASH_IMAGE_PATH = os.path.join(RESOURCES_DIR, "lemur.png")
FLASH_SOUND_PATH = os.path.join(RESOURCES_DIR, "lemur.mp3")

last_death = 0
last_kills = 0
last_flashed = 0

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

on_cooldown = False
event_queue = []
working = False

pygame.mixer.init()

GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TOOLWINDOW = 0x00000080  # optional: hide from taskbar

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.0)

hwnd = root.winfo_id()

exstyle = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image_width = 1920
image_height = 1080
x_position = (screen_width // 2) - (image_width // 2)
y_position = (screen_height // 2) - (image_height // 2)
root.geometry(f"{image_width}x{image_height}+{x_position}+{y_position}")

preloaded_images = {}

def preload_image(path):
    if not os.path.exists(path):
        return None
    pil_img = Image.open(path).convert("RGBA")
    return ImageTk.PhotoImage(pil_img)

preloaded_images[VICTORY_IMAGE_PATH] = preload_image(VICTORY_IMAGE_PATH)
preloaded_images[FLASH_IMAGE_PATH] = preload_image(FLASH_IMAGE_PATH)

for item in KILL_PATHS + DEATH_PATHS:
    full_path = os.path.join(RESOURCES_DIR, item["image"])
    preloaded_images[full_path] = preload_image(full_path)

label = tk.Label(root, bg="black", borderwidth=0, highlightthickness=0)
label.pack()

root.withdraw()

def reset_cooldown():
    global on_cooldown
    on_cooldown = False

<<<<<<< HEAD:Scripts/Event_queue.py
async def process_event_queue(event_queue):
    for item in list(event_queue):
        func = globals().get(item)
        if func is None:
            try:
                event_queue.remove(item)
            except ValueError:
                pass
            continue
        try:
            await func()
        except Exception:
            pass
        try:
            event_queue.remove(item)
        except ValueError:
            pass

async def kill():
    global on_cooldown
=======
def process_event_queue(event_queue): # this needs to be revamped to await finishing the events in the queue to finish processing- do on updated version locally - why didnt it push?
    for item in event_queue:
        asyncio.run(globals()[item]())
        event_queue.remove(item)
    
async def kill(on_cooldown): # Test this - Non global
>>>>>>> 4b2ba317e2183d66fa345a062aafa2e4e7222439:Scripts/Event_queue test.py
    while on_cooldown:
        await asyncio.sleep(0.1)
    selected = random.choice(KILL_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images.get(img)
    if img_obj is None:
        return
    show_overlay(img_obj, snd)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def flash():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.1)
    img_obj = preloaded_images.get(FLASH_IMAGE_PATH)
    if img_obj is None:
        return
    show_overlay(img_obj, FLASH_SOUND_PATH)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def death():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.1)
    selected = random.choice(DEATH_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images.get(img)
    if img_obj is None:
        return
    show_overlay(img_obj, snd)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

async def win():
    global on_cooldown
    while on_cooldown:
        await asyncio.sleep(0.1)
    img_obj = preloaded_images.get(VICTORY_IMAGE_PATH)
    if img_obj is None:
        return
    show_overlay(img_obj, VICTORY_SOUND_PATH)
    on_cooldown = True
    threading.Timer(3.0, reset_cooldown).start()

def show_overlay(image_obj, sound_path):
    root.deiconify()
    root.lift()
    label.config(image=image_obj)
    label.image = image_obj
<<<<<<< HEAD:Scripts/Event_queue.py
    try:
        pygame.mixer.Sound(sound_path).play()
    except Exception:
        pass
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

loop = asyncio.new_event_loop()
def _start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=_start_loop, daemon=True).start()

def process_data_file(event_queue):
    global last_death, last_kills, last_flashed
=======

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

# Processing data file , just making event queue
def process_data_file(event_queue): # Test these values - Non Global 
    global working
>>>>>>> 4b2ba317e2183d66fa345a062aafa2e4e7222439:Scripts/Event_queue test.py
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        print("Trying to read JSON file")
        try:
            working = True # remove this when testing Async

            # Take time here
            
            data = json.load(f)
            print("Data loaded:")
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)
            if player_steamid == steamid:
                activity = data.get("player", {}).get("activity", "none")
                deaths = data.get("player", {}).get("match_stats", {}).get("deaths", 0)
                kills = data.get("player", {}).get("match_stats", {}).get("kills", 0)
                ct = data.get("map", {}).get("team_ct", {}).get("score", 0)
                t = data.get("map", {}).get("team_t", {}).get("score", 0)
                flashed = data.get("player", {}).get("state", {}).get("flashed", 0)
                team = data.get("player", {}).get("team", "")
                print("Here is the data we got: activity:", activity, "deaths:", deaths, "kills:", kills, "ct:", ct, "t:", t, "flashed:", flashed, "team:", team)
                if deaths > last_death:
                    last_death = deaths
                    event_queue.append("death")
                    if random.random() < 0.01:
                        subprocess.run(["start", "steam://run/2379780"], shell=True)
                if flashed > 0 and last_flashed == 0:
                    event_queue.append("flash")
                if kills > last_kills:
                    last_kills = kills
                    event_queue.append("kill")
                if ct == 13:
                    if team.upper() == "CT":
                        event_queue.append("win")
                    else:
                        try:
                            pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                        except Exception:
                            pass
                if t == 13:
                    if team.upper() == "T":
                        event_queue.append("win")
<<<<<<< HEAD:Scripts/Event_queue.py
                    else:
                        try:
                            pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                        except Exception:
                            pass
                asyncio.run_coroutine_threadsafe(process_event_queue(event_queue), loop)
                if activity == "menu" and kills + deaths != 0:
=======
                    else: 
                        pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                
                process_event_queue(event_queue)
                # take time again
                # Calculate time taken , print to log
                
                if activity == "menu":
                    print("[INFO] Kill count reset.")
>>>>>>> 4b2ba317e2183d66fa345a062aafa2e4e7222439:Scripts/Event_queue test.py
                    last_kills = 0
                    event_queue.clear()
                    last_flashed = flashed
        except json.JSONDecodeError:
            return

class DataFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("data.json"):
<<<<<<< HEAD:Scripts/Event_queue.py
            process_data_file(event_queue)
=======
            print("Watchdog detected change , processing JSON asset")
            if working == False:
                process_data_file(event_queue) # Maybe use Asyncio Create Task?
>>>>>>> 4b2ba317e2183d66fa345a062aafa2e4e7222439:Scripts/Event_queue test.py

observer = Observer()
observer.schedule(DataFileHandler(), path=SCRIPT_DIR, recursive=False)

def start_observer():
    observer.start()
    try:
        while True:
            time.sleep(1) # this needs to be revamped to await for the finished processing of process_data(event_queue)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

observer_thread = threading.Thread(target=start_observer, daemon=True)
observer_thread.start()

root.mainloop()
