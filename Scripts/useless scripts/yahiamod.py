import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import queue
import winreg
import vdf
import shutil
import sys
import json
import random
import filecmp
import pygame
import webbrowser
import pyautogui
import logging
import tkinter as tk 
from threading import Thread
from ctypes import windll
from flask import Flask, request
from PIL import Image, ImageTk
from tkinter import messagebox

confirmation = messagebox.askyesno(
    "Yahiamod Confirmation",
    "Do you want to enable Hardmode?"
)

for y in range(1, random.randint(8,20)):
    if confirmation:
        string = "Are you "
        if random.randint(0,8) == 4:
            for x in range(1,y):
                    string = string + " REALLY "
            confirmation = messagebox.askyesno(
            "Hardmode?",
            string + " NOT sure?",
            )
            if confirmation:
                confirmation = False
                messagebox.showinfo(
                    "Hardmode is NOT enabled",
                    "Enjoy your regular Yahiamod experience!"
                )
        else:
            for x in range(1,y):
                    string = string + " REALLY "
            confirmation = messagebox.askyesno(
                "Hardmode?",
                string + "sure?",
            )
    else:
        break

if confirmation:
    messagebox.showinfo(
        "Hardmode Enabled",
        "Hardmode is now enabled. Good luck!"
    )
else:
    messagebox.showinfo(
        "Hardmode is NOT enabled",
        "Enjoy your regular Yahiamod experience!"
    )

debug = messagebox.askyesno(
    "Debug Mode",
    "Enable debug mode? (For troubleshooting purposes)"
)

if debug:
    print("[Init] Debug mode is ON \nget_counter_strike_path function defining...")

def get_counter_strike_path(font_path):
    yahiamice_changed = False
    fonts_changed = False
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

        if not steam_path and debug:
            print("Steam registry key not found.")
            return None
        
        if debug:
            print(f"Steam path: {steam_path}")
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

        if not os.path.exists(vdf_path) and debug:
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
                        if debug:
                            print("Found game!")
                            print("Trying to find Yahiamice Config")
                        try:
                            if debug:
                                print("Preparing to copy Yahiamice Config...")
                            yahiamice_path = os.path.join(game_folder, "game", "csgo", "cfg")
                            src_file = os.path.join(RESOURCES_DIR, "gamestate_integration_yahamouse.cfg")
                            dest_file = os.path.join(yahiamice_path, os.path.basename(src_file))
                            
                            if not os.path.exists(dest_file):
                                if debug:
                                    print("Replacing Yahiamice Config (different content)")
                                shutil.copy2(src_file, dest_file)
                                yahiamice_changed = True
                            elif debug:
                                print("Yahiamice Config already exists, skipping copy.")
                        
                        except Exception as e:
                                print(f"Error copying file: {e}")

                        FONT_PATH = os.path.join(game_folder, "game", "csgo", "panorama", "fonts")
                        if debug:
                            print(f"Fonts directory ready at: {FONT_PATH}\nApplying Comic Sans")

                        for y in range(0, 3):
                            try:
                                src_file = font_path[y]
                                if debug:
                                    print("Trying to copy from:", src_file)
                                dest_file = os.path.join(FONT_PATH, os.path.basename(src_file))

                                if os.path.exists(dest_file):
                                    # Compare existing file with source
                                    if filecmp.cmp(src_file, dest_file, shallow=False):
                                        if debug:
                                            print(f"Skipped {os.path.basename(src_file)} — already identical")
                                        continue
                                    else:
                                        os.remove(dest_file)
                                        if debug:
                                            print(f"Replacing {os.path.basename(src_file)} (different content)")
                                        fonts_changed = True
                                        
                                if debug:
                                    print("To:", dest_file)
                                shutil.copy2(src_file, dest_file)
                                if debug:
                                    print(f"Copied {src_file} -> {dest_file}")

                            except Exception as e:
                                print(f"Error copying file: {e}")

    except Exception as e:
        print(f"Error accessing registry or parsing VDF: {e}")
        return None

    if yahiamice_changed:
        messagebox.showinfo(
        "Yahiamice Config Updated",
        "Yahiamice config installed, please restart Counter Strike"
        )
        os._exit(0)


    if fonts_changed:
        messagebox.showinfo(
        "Fonts Updated",
        "Important files changed, please restart Counter Strike"
        )
        os._exit(0)

    return None

if debug:
    print("[Init] get_counter_strike_path function defined successfully\nSetting script directories...")    

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")

VICTORY_IMAGE_PATH = os.path.join(RESOURCES_DIR, "cinema.png")
VICTORY_SOUND_PATH = os.path.join(RESOURCES_DIR, "boom.mp3")
DEFEAT_SOUND_PATH = os.path.join(RESOURCES_DIR, "tf2.mp3")
FLASH_IMAGE_PATH = os.path.join(RESOURCES_DIR, "lemur.png")
FLASH_SOUND_PATH = os.path.join(RESOURCES_DIR, "lemur.mp3")
FONT_PATH = [os.path.join(RESOURCES_DIR, "fonts.conf"), os.path.join(RESOURCES_DIR, "ComicBD.ttf"), os.path.join(RESOURCES_DIR, "Comic.ttf")]
cs_directory = get_counter_strike_path(FONT_PATH)
parent_directory = os.path.dirname(SCRIPT_DIR)
last_data = ""
ui_queue = queue.Queue()

if debug:
    print("[Init] Setting up tkinter window...")

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

pygame.mixer.init()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image_width = 1920
image_height = 1080
x_position = (screen_width // 2) - (image_width // 2)
y_position = (screen_height // 2) - (image_height // 2)
root.geometry(f"{image_width}x{image_height}+{x_position}+{y_position}")
preloaded_images = {}

KILL_PATHS = [
    {"image": "cantelope.png", "sound": "cantaloupe.ogg"},
    {"image": "pineapple.png", "sound": "pineapple.ogg"},
    {"image": "cinema.png", "sound": "boom.mp3"},
    {"image": "weiner.png", "sound": "weiner.mp3"},
    {"image": "sins.png", "sound": "sins.wav"}
]
DEATH_PATHS = [
    {"image": "baby.png", "sound": "lobotomy.mp3"},
    {"image": "kys.png", "sound": "kys.mp3"},
    {"image": "nananaboobooboo.png", "sound": "gmod.mp3"},
    {"image": "awesome.png", "sound": "awesome.mp3"},
    {"image": "yahiamice.gif", "sound": "whatisapp.ogg"},
    {"image": "sleep.png", "sound": "sleep.mp3"}
]

if debug:
    print("[Init] Preloading images...")

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

if debug:
    print("[Main Definitions] Kill")

def kill():
    selected = random.choice(KILL_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images.get(img)
    if img_obj is None:
        return
    show_overlay(img_obj, snd)

def assist():
    assist_sound_path = os.path.join(RESOURCES_DIR, "slip.mp3")
    pygame.mixer.Sound(assist_sound_path).play()
    pyautogui.press('g')
    
if debug:
    print("[Main Definitions] Flash")

def flash():
    img_obj = preloaded_images.get(FLASH_IMAGE_PATH)
    if img_obj is None:
        return
    show_overlay(img_obj, FLASH_SOUND_PATH)

if debug:
    print("[Main Definitions] Death")

def death():
    selected = random.choice(DEATH_PATHS)
    img = os.path.join(RESOURCES_DIR, selected["image"])
    snd = os.path.join(RESOURCES_DIR, selected["sound"])
    img_obj = preloaded_images.get(img)
    if img_obj is None:
        return
    show_overlay(img_obj, snd)

def horse():
    img = os.path.join(RESOURCES_DIR, "horse.png")
    snd = os.path.join(RESOURCES_DIR, "horse.ogg")
    img_obj = preloaded_images.get(img)
    if img_obj is None:
        return
    show_overlay(img_obj, snd)
    pyautogui.press('g')
    messagebox.showinfo(
        "HORSE",
        "Horses suck so bad they made you drop your weapon.\n'fuck you.' - horse"
    )

if debug:
    print("[Main Definitions] Win")

def win():
    img_obj = preloaded_images.get(VICTORY_IMAGE_PATH)
    if img_obj is None:
        return
    show_overlay(img_obj, VICTORY_SOUND_PATH)

if debug:
    print("[Main Definitions] Stake")
    
def stake():
    urls = [
        "https://stake.com",
        "https://en.gameslol.net/deal-or-no-deal-754.html",
        "https://skybet.com/",
        "https://csgoempire.com/"
    ]
    webbrowser.open_new(random.choice(urls))
    stake_sound_path = os.path.join(RESOURCES_DIR, "jackpot.ogg")
    pygame.mixer.Sound(stake_sound_path).play()

if debug:
    print("[Main Definitions] Show Overlay")

def show_overlay(image_obj, sound_path):
    root.deiconify()
    root.lift()

    label.config(image=image_obj)
    label.image = image_obj

    pygame.mixer.Sound(sound_path).play()

    fade_in(0.0)  # ← THIS IS WHAT YOU ARE MISSING

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

if debug:
    print("Clearing earlier JSON, if it exists")

json_asset = os.path.join(SCRIPT_DIR, "data.json")
with open(json_asset, "w", encoding="utf-8") as f:
    json.dump({}, f)

if debug:
    print("[Init] Important video")

important_video_path = os.path.join(RESOURCES_DIR, "importantvideo.ogv")
important_video_rng = random.randint(0, 50)
if debug:
    print("Important Video chance: %d / 50", important_video_rng)
if random.random() < 0.02:
    os.startfile(important_video_path)

if debug:
    print("[Init] Starting flask server...")
app = Flask(__name__)

if debug:
    print("[SRV]Game Event")
@app.route("/", methods=["POST"])
def game_event():
    global last_data
    data = request.json
    data_path = os.path.join(SCRIPT_DIR, "data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    if debug:
        print("[SRV]Received: %s", data.get("player", {}).get("activity", "unknown"))
    
    # Shift to handling events
    # starts by checking if steamID match

    if last_data == "":
        last_data = data
        return "Counter Strike Response", 200

    steamid = data.get("provider", {}).get("steamid", 1)
    player_steamid = data.get("player", {}).get("steamid", 0)
    if player_steamid == steamid:
        deaths = data.get("player", {}).get("match_stats", {}).get("deaths", 0)
        last_deaths = last_data.get("player", {}).get("match_stats", {}).get("deaths", 0)

        if deaths > last_deaths:
            ui_queue.put(("death", None))

        kills = data.get("player", {}).get("match_stats", {}).get("kills", 0)
        last_kills = last_data.get("player", {}).get("match_stats", {}).get("kills", 0)
        if kills > last_kills:
            ui_queue.put(("kill", None))#
        
        assists = data.get("player", {}).get("match_stats", {}).get("assists", 0)
        last_assists = last_data.get("player", {}).get("match_stats", {}).get("assists", 0)
        if assists > last_assists:
            ui_queue.put(("assist", None))
        
        flashed = data.get("player", {}).get("state", {}).get("flashed", 0)
        last_flashed = last_data.get("player", {}).get("state", {}).get("flashed", 0)
        if flashed > 0 and last_flashed == 0:
            ui_queue.put(("flash", None))
        
        ct = data.get("map", {}).get("team_ct", {}).get("score", 0)
        t = data.get("map", {}).get("team_t", {}).get("score", 0)
        team = data.get("player", {}).get("team", "")

        if ct == 13:
            if team.upper() == "CT":
                ui_queue.put(("win", None))
            else:
                try:
                    pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                except Exception:
                    pass
        
        if t == 13:
            if team.upper() == "T":
                ui_queue.put(("win", None))
            else:
                try:
                    pygame.mixer.Sound(DEFEAT_SOUND_PATH).play()
                except Exception:
                    pass
        
        money = data.get("player", {}).get("state", {}).get("money", 0)
        last_money = last_data.get("player", {}).get("state", {}).get("money", 0)
        round = data.get("map", {}).get("round", 0)
        last_round = last_data.get("map", {}).get("round", 0)
        if money > last_money and round != last_round:
            ui_queue.put(("stake", None))

        health = data.get("player", {}).get("state", {}).get("health", 100)
        if random.random() < 1/100 and activity != "menu" and health > 0:
            ui_queue.put(("horse", None))

        activity = data.get("player", {}).get("activity", "none")
        if activity == "menu":
            if debug:
                print("[INFO] Kill count reset.")
            last_kills = 0
            last_flashed = flashed
        
        last_data = data

    return "Counter Strike Response", 200

# Running Flask then root.mainloop doesnt work so we define the instructions for starting the flask server in a seperate function
def run_server():
    if debug:
        print("[Init] Running flask server...")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

def process_ui_events():
    try:
        while True:
            event, payload = ui_queue.get_nowait()

            if event == "kill":
                kill()
            elif event == "death":
                death()
            elif event == "flash":
                flash()
            elif event == "win":
                win()
            elif event == "stake":
                win()
            elif event == "assist":
                stake()
            elif event == "horse":
                stake()

    except queue.Empty:
        pass

    root.after(50, process_ui_events)

if __name__ == "__main__":
    print("\n\n If you see an orange 'ctrl+c' to quit, Yahiamod is running properly! \n\n")
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    process_ui_events()
    root.mainloop()
