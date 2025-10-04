import json
import pygame 
import os 
import psutil
import sys
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
            print("[21 DEBUG] yahamouse.py not running. Exiting main server.")
            os._exit(0)  
        time.sleep(5)  

threading.Thread(target=monitor_yahamouse, daemon=True).start()


if enable_debug:
    print("[21 DEBUG] Initialising Pygame Audio Mixer")

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(15)

script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "resources")
log_directory = os.path.join(script_directory, "logs")
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "console_log.txt")
JSON_PATH = os.path.join(script_directory, "data.json")

SOUND_PATH_21 = os.path.join(resources_directory, "twennyone.wav")
SOUND_PATH_9 = os.path.join(resources_directory, "nine.wav")
SOUND_PATH_10 = os.path.join(resources_directory, "ten.wav")

sys.stdout = Logger(log_path)
sys.stderr = sys.stdout

# === Sound Map ===
SOUND_MAP = {
    "21": {"path": SOUND_PATH_21, "channel": 1},
    "9": {"path": SOUND_PATH_9, "channel": 2},
    "10": {"path": SOUND_PATH_10, "channel": 3},
}

cooldown_seconds = 3  # cooldown duration per ammo_clip value
last_played_time = {}  # stores timestamps of last play per ammo_clip

# === Sound Player ===
def play_sound_by_name(name):
    sound_info = SOUND_MAP.get(name)
    if sound_info:
        if enable_debug:
            print(f"[21 DEBUG] Playing sound for ammo_clip: {name}")
        pygame.mixer.Channel(sound_info["channel"]).play(pygame.mixer.Sound(sound_info["path"]))

# === Weapon Ammo Reader With Cooldown ===
def check_active_weapon_ammo():
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
            weapons = data.get("player", {}).get("weapons", {})
            for weapon_id, weapon_data in weapons.items():
                if weapon_data.get("state") == "active":
                    ammo_clip = str(weapon_data.get("ammo_clip"))
                    if enable_debug:
                        print(f"[21 DEBUG] Active weapon ammo_clip: {ammo_clip}")
                    if ammo_clip in SOUND_MAP:
                        now = time.time()
                        last_time = last_played_time.get(ammo_clip, 0)
                        if now - last_time >= cooldown_seconds:
                            play_sound_by_name(ammo_clip)
                            last_played_time[ammo_clip] = now
                        else:
                            if enable_debug:
                                print(f"[21DEBUG] Cooldown active for ammo_clip {ammo_clip}")
                    break
    except Exception as e:
        if enable_debug:
            print(f"[21 ERROR] {e}")

# === Loop (demo/testing) ===
if __name__ == "__main__":
    while True:
        check_active_weapon_ammo()
        time.sleep(0.5)  # Check every 0.5s
