import sys
import os
import random
import json
import queue
import vdf # New - pip install vdf  
import winreg # New - pip install winreg
import psutil
import shutil
import time
import threading
import filecmp
from flask import Flask, request

# add new packages to Readme on GIT

# Set terminal size
os.system("mode con: cols=178 lines=50")

class Logger: # So people can acutally send me logs of my code.. wait.. do i want this? 
	# this code isnt working right! It needs to check if there is already a log and not add to it! My current log file is like 2.2b lines long. 
	# TODO: Date the logs with the time they start: SERVER-LOG_DD/MM/YY_HH:MM
	# TODO: Output values in a readable manner so we can track values accurately
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
    
def get_counter_strike_path(font_path):
    try:
        csgo_app_id = "730"
        steam_path = None

        # Try both registry paths
        for reg_path in [r"SOFTWARE\Valve\Steam", r"SOFTWARE\WOW6432Node\Valve\Steam"]:
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                steam_path = winreg.QueryValueEx(registry_key, "InstallPath")[0]
                winreg.CloseKey(registry_key)
                break
            except FileNotFoundError:
                continue

        if not steam_path:
            print("Steam registry key not found.")
            return None

        print(f"Steam path: {steam_path}")
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

        if not os.path.exists(vdf_path):
            print(f"libraryfolders.vdf not found at: {vdf_path}")
            return None

        with open(vdf_path, encoding='utf-8') as f:
            vdf_data = vdf.load(f)

        libraries = vdf_data.get('libraryfolders', {})
        for key, library in libraries.items():
            if isinstance(library, dict) and 'apps' in library:
                if csgo_app_id in library['apps']:
                    game_folder = os.path.join(library['path'], 'steamapps', 'common', 'Counter-Strike Global Offensive')
                    if os.path.exists(game_folder):
                        print("Found game!")
                        fonts_path = os.path.join(game_folder, "game", "csgo", "panorama", "fonts")
                        print(f"Fonts directory ready at: {fonts_path}\nApplying Comic Sans")

                        for y in range(0, 3):
                            try:
                                src_file = font_path[y]
                                print("Trying to copy from:", src_file)
                                dest_file = os.path.join(fonts_path, os.path.basename(src_file))

                                if os.path.exists(dest_file):
                                    # Compare existing file with source
                                    if filecmp.cmp(src_file, dest_file, shallow=False):
                                        print(f"Skipped {os.path.basename(src_file)} — already identical")
                                        continue
                                    else:
                                        os.remove(dest_file)
                                        print(f"Replacing {os.path.basename(src_file)} (different content)")

                                print("To:", dest_file)
                                shutil.copy2(src_file, dest_file)
                                print(f"Copied {src_file} -> {dest_file}")

                            except Exception as e:
                                print(f"Error copying file: {e}")

    except Exception as e:
        print(f"Error accessing registry or parsing VDF: {e}")
        return None

script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
log_path = os.path.join(log_directory, "console_log.txt")
font_path = [os.path.join(resources_directory, "fonts.conf"), os.path.join(resources_directory, "ComicBD.ttf"), os.path.join(resources_directory, "Comic.ttf")]
cs_directory = get_counter_strike_path(font_path)
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
        print(cs_directory)

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

