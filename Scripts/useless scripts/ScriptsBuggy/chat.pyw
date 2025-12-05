import tkinter as tk
import cv2
from PIL import Image, ImageTk
from pynput.mouse import Listener
from pynput.keyboard import Listener, Controller, Key
import pygame
import threading
import time
from flask import Flask, request
from flask_socketio import SocketIO
import queue
from random import randint
import os

#config
script_directory = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = os.path.join(script_directory, "muchotexto.ogg")
HOST_STEAM_ID = "76561199128394910"  # Replace with actual Steam ID
controller = Controller()
keyboard = Controller()
typed_chars = []
listening = False
in_match = True

# important video 
important_video_path = os.path.join(script_directory, "importantvideo.ogv")
important_video_rng = randint(0,50)
if important_video_rng == 50:
    os.startfile(important_video_path)

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
            print("[MUCHO DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()

print("flask name")
app = Flask(__name__)
event_queue = queue.Queue()  # Queue for handling events safely

print("TKinter root")
# Create a global Tkinter root instance
root = tk.Tk()
root.withdraw()  # Hide the main window until needed

print("process queue")
def process_queue():
    while not event_queue.empty():
        event_queue.get()()  # Execute the function from the queue
    root.after(100, process_queue)  # Check queue periodically
        
def play_sound_texto():
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_PATH)
    pygame.mixer.music.play()
    
def on_press(key):
    global typed_chars, listening
    
    print("checking for y")
    if hasattr(key, 'char') and key.char and in_match == True:  # Check for valid character input
        print("check valid input True")
        if key.char.lower() == 'y' or key.char.lower() == 'u':  # Start listening when 'y' is pressed
            listening = True
            print(listening)
            print(typed_chars)
            typed_chars.clear()  # Ensure fresh tracking starts after 'y'
        elif listening:  # Only track characters if 'y' was pressed first
            typed_chars.append(key.char)
            print(typed_chars)

    elif key in [Key.enter, Key.esc]:  # Stop listening if Enter/Escape is pressed early
        typed_chars.clear()
        print("enter pressed")
        listening = False
        print(listening)
    
    if len(typed_chars) >= 10 and listening:  # Enter pressed after 'y'
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.press('y')
        keyboard.release('y')
        time.sleep(0.5)
        controller.type("Mucho Texto")
        play_sound_texto()
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        typed_chars.clear()  # Reset input tracking
        listening = False  # Reset trigger after execution

# Start listening for keyboard events
keyboard_thread = threading.Thread(target=lambda: Listener(on_press=on_press).start(), daemon=True)
keyboard_thread.start()
    
print("game event")
@app.route("/", methods=["POST"])
def game_event():
    data = request.json

    print("Received request:", data)  # logs litteraly fucking everything making console unreadable
        
    map_data = data.get("map", {})
    if map_data:
        print("got map data")
        current_round = map_data.get("round", 0)
        if 0 < current_round:
            print("in-match")
            in_match = True
        else:
            in_match = False
            print("not in match")

    return "", 200

print("if name main")
if __name__ == "__main__":
    root.after(100, process_queue)  # Start queue processing

    # Start Flask in its own thread without blocking Tkinter
    flask_thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, threaded=True))
    flask_thread.daemon = True
    flask_thread.start()

    root.mainloop()  # Keep Tkinter running

