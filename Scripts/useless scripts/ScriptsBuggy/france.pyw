import json
import pygame 
import os 
import sys
import threading
import time

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
            print("[France DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()

if enable_debug:
    print("[France DEBUG] Initialising Pygame Audio Mixer")

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(15)

script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "console_log.txt")
JSON_PATH = os.path.join(script_directory, "data.json")

SOUND_PATH = os.path.join(resources_directory, "bullets.wav")

sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

# === Weapon Ammo Reader With Cooldown ===
def check_active_weapon_ammo():
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
            weapons = data.get("player", {}).get("weapons", {})
            for weapon_id, weapon_data in weapons.items():
                if weapon_data.get("state") == "reloading":
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_PATH))


# === Loop (demo/testing) ===
if __name__ == "__main__":
    while True:
        check_active_weapon_ammo()
        time.sleep(0.5)  # Check every 0.5s
