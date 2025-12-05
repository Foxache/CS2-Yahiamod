import json
import pygame 
import os 
import sys
import time
import threading
import webbrowser
from pynput.keyboard import Key, Controller

class Logger:  # Logging for debugging
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
cooldown_duration = 1.0  # in seconds
keyboard = Controller()
last_trigger_time = 0  # track last time we fired

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
            print("[Yahiamice DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()

if enable_debug:
    print("[Yahiamice DEBUG] Initialising Pygame Audio Mixer")
pygame.mixer.init()
pygame.mixer.set_num_channels(1)

if enable_debug:
    print("[Yahiamice DEBUG] Initialising directories")
script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "console_log.txt")
JSON_PATH = os.path.join(script_directory, "data.json")

if enable_debug:
    print("[Yahiamice DEBUG] Logging")
sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

def check_assists():
    global last_trigger_time

    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)

        assists = data.get("player", {}).get("match_stats", {}).get("assists", 0)
        previous_assists = data.get("previously", {}).get("player", {}).get("match_stats", {}).get("assists", 0)

        if assists > previous_assists:
            now = time.time()
            if now - last_trigger_time >= cooldown_duration:
                last_trigger_time = now
                print(f"[Yahiamice] Assist increase detected: {previous_assists} → {assists}")
                webbrowser.open("https://www.twitch.tv/yahiamice")  # Yahiamice assists you too
                keyboard.press(Key.alt)
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
                keyboard.release(Key.alt)

    except Exception as e:
        print(f"[ERROR] While checking assists: {e}")

# === Main Loop ===
if enable_debug:
    print("[Yahiamice DEBUG] Main loop")
if __name__ == "__main__":
    while True:
        check_assists()
        time.sleep(0.5)
