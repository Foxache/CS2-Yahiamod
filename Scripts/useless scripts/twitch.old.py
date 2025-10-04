import os
import json
import time
import threading
import pygame
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FUCKING TEST THIS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
KILL_GIF_PATH = os.path.join(RESOURCES_DIR, "chat.gif")  # Replace with your GIF
KILL_SOUND_PATH = os.path.join(RESOURCES_DIR, "kill.wav")  # Optional sound

last_kills = 0
on_cooldown = False
enabled = False
is_animating = False
frame_index = 0

pygame.mixer.init()
kill_sound = pygame.mixer.Sound(KILL_SOUND_PATH)

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="black")

gif = Image.open(KILL_GIF_PATH)
frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
print(f"[INFO] Total frames loaded: {len(frames)}")

gif_label = tk.Label(root, bg="black", bd=0, highlightthickness=0)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
gif_width = frames[0].width()
gif_height = frames[0].height()

x_pos = screen_width - gif_width - 50
y_pos = int(screen_height / 2 - gif_height / 2)

gif_label.place(x=x_pos, y=y_pos)
gif_label.place_forget()  # Hide initially

def animate_gif():
    global frame_index, is_animating
    if not is_animating:
        is_animating = True
        def loop():
            global frame_index
            if not is_animating:
                return
            gif_label.configure(image=frames[frame_index])
            frame_index = (frame_index + 1) % len(frames)
            root.after(100, loop)
        loop()

def show_kill_overlay():
    global frame_index
    kill_sound.play()
    frame_index = 0
    gif_label.place(x=x_pos, y=y_pos)
    animate_gif()
    root.after(2000, hide_kill_overlay)

def hide_kill_overlay():
    global is_animating
    is_animating = False
    gif_label.place_forget()

def trigger_kill_event():
    global on_cooldown
    if not on_cooldown:
        print("[EVENT] Kill detected!")
        show_kill_overlay()
        on_cooldown = True
        threading.Timer(2.0, reset_cooldown).start()

def reset_cooldown():
    global on_cooldown
    on_cooldown = False

def process_data_file():
    global last_kills, enabled
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            kills = data.get("map", {}).get("current_spectators", 0)
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid:
                if kills > last_kills and not enabled:
                    trigger_kill_event()
                    last_kills = kills
                    enabled = True
                elif last_kills > kills:
                    enabled = False
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
