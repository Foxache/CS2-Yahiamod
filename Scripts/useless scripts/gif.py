import tkinter as tk
import os 
import threading
import time
import json
from PIL import Image, ImageTk, ImageSequence
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
GIF_PATH = os.path.join(RESOURCES_DIR, "chat.gif")

root = tk.Tk()
root.geometry("+0-427") 
root.overrideredirect(True)  # Removes title bar
root.attributes("-topmost", True)
root.configure(bg="black")  # You can change this if needed

gif = Image.open(GIF_PATH)
frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
print(f"[INFO] Total frames loaded: {len(frames)}")

gif_label = tk.Label(root, bg="black", bd=0, highlightthickness=0)
gif_label.pack()

root.withdraw()

frame_index = 0
last_health = 100
delay = 2000

def animate():
    global frame_index
    gif_label.configure(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)    

def process_data_file():
    global last_kills, delay
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            health = data.get("player", {}).get("state", {}).get("health", last_health)
            viewers = data.get("map",{}).get("current_spectators", 0)
            steamid = data.get("provider", {}).get("steamid", 1)
            player_steamid = data.get("player", {}).get("steamid", 0)

            if player_steamid == steamid:
                # Detect transition: alive → dead
                if last_health > 0 and health == 0:
                    if viewers <= 0:
                        root.withdraw()  
                    elif viewers > 0:
                        root.deiconify()  
                    elif viewers == 1:
                        delay = 1000
                    elif viewers == 2:
                        delay = 750
                    else:  # 3+
                        delay = 100

                    root.after(delay, animate)
                
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

animate()
root.mainloop()

