import sys
import os
import random
import json
import queue
import psutil
import time
import threading
from flask import Flask, request

# Set terminal size
os.system("mode con: cols=178 lines=50")

class Logger: # So people can acutally send me logs of my shitty code.. wait.. do i want this?
    def __init__(self, logfile):
        self.terminal = sys.stdout
        self.log = open(logfile, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

enable_debug = True  

lines = [
    "░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░ ",
    "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ",
    "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ",
    "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  ",
    "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ ",
    "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ ",
    "░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░  ",
    "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
    "                         ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗     ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗ ",
    "                         ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗    ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗",
    "                         ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝    █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝",
    "                         ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗",
    "                         ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║    ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║",
    "                         ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"
]

total_duration = 0.5
total_chars = sum(len(line) for line in lines)
char_delay = total_duration / total_chars


for line in lines:
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()
	
if enable_debug:
    print("[SERVER DEBUG] Directory Initialistion")

script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "recourses")
log_directory = os.path.join(script_directory, "logs")
log_path = os.path.join(log_directory, "console_log.txt")
parent_directory = os.path.dirname(script_directory)

sys.stdout = Logger(log_path)
sys.stderr = sys.stdout 

if enable_debug:
    print("[SERVER DEBUG] Clearing ealier JSON , if it exists")  

json_asset = os.path.join(script_directory, "data.json")
with open(json_asset, "w", encoding="utf-8") as f:
    json.dump({}, f)
        
important_video_path = os.path.join(resources_directory, "importantvideo.ogv")
important_video_rng = random.randint(0, 50)
if enable_debug:
    print("[SERVER DEBUG] Important Video chance:", important_video_rng)
if random.random() < 0.02:
    os.startfile(important_video_path)

if enable_debug:
    print("[SERVER DEBUG] Flask name")
app = Flask(__name__)
event_queue = queue.Queue() 

if enable_debug:
    print("[SERVER DEBUG] Process queue")
def process_queue():
    while not event_queue.empty():
        try:
            event_queue.get_nowait()()  # Avoid blocking on empty queue
        except queue.Empty:
            break  
    root.after(5, process_queue)  # Reduce delay for faster processing
    
if enable_debug:
    print("[SERVER DEBUG] Game Event")
@app.route("/", methods=["POST"])
def game_event():
    data = request.json
    data_path = os.path.join(script_directory, "data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("[SERVER DEBUG] Received:", data.get("player", {}).get("activity", "unknown"))
    return "Counter Strike Response", 200

if __name__ == "__main__":
    if enable_debug:
        print("[SERVER DEBUG] Starting Flask server on http://127.0.0.1:5000")

    app.run(host="127.0.0.1", port=5000)

#▓█████▄  ██▓ ███▄    █   ▄████  █    ██   ██████ ▓█████▄  ▒█████   ███▄    █   ▄████  █    ██  ██▓     █    ██   ██████ 
#▒██▀ ██▌▓██▒ ██ ▀█   █  ██▒ ▀█▒ ██  ▓██▒▒██    ▒ ▒██▀ ██▌▒██▒  ██▒ ██ ▀█   █  ██▒ ▀█▒ ██  ▓██▒▓██▒     ██  ▓██▒▒██    ▒ 
#░██   █▌▒██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▒██░░ ▓██▄   ░██   █▌▒██░  ██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▒██░▒██░    ▓██  ▒██░░ ▓██▄   
#░▓█▄   ▌░██░▓██▒  ▐▌██▒░▓█  ██▓▓▓█  ░██░  ▒   ██▒░▓█▄   ▌▒██   ██░▓██▒  ▐▌██▒░▓█  ██▓▓▓█  ░██░▒██░    ▓▓█  ░██░  ▒   ██▒
#░▒████▓ ░██░▒██░   ▓██░░▒▓███▀▒▒▒█████▓ ▒██████▒▒░▒████▓ ░ ████▓▒░▒██░   ▓██░░▒▓███▀▒▒▒█████▓ ░██████▒▒▒█████▓ ▒██████▒▒
# ▒▒▓  ▒ ░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ░▒   ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
# ░ ▒  ▒  ▒ ░░ ░░   ░ ▒░  ░   ░ ░░▒░ ░ ░ ░ ░▒  ░ ░ ░ ▒  ▒   ░ ▒ ▒░ ░ ░░   ░ ▒░  ░   ░ ░░▒░ ░ ░ ░ ░ ▒  ░░░▒░ ░ ░ ░ ░▒  ░ ░
# ░ ░  ░  ▒ ░   ░   ░ ░ ░ ░   ░  ░░░ ░ ░ ░  ░  ░   ░ ░  ░ ░ ░ ░ ▒     ░   ░ ░ ░ ░   ░  ░░░ ░ ░   ░ ░    ░░░ ░ ░ ░  ░  ░  
#   ░     ░           ░       ░    ░           ░     ░        ░ ░           ░       ░    ░         ░  ░   ░           ░  
# ░                                                ░                                                                     

