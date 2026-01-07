import tkinter as tk
import random
import os
import pyautogui
import pygame
from PIL import Image, ImageTk
import psutil
import sys

# Global variables
prev_ping = random.randint(1, 15)
playing = False
groups = [(1, 10), (11, 250), (251, 550), (551, 999)]
script_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(script_directory, "recourses")
SOUND_PATH = os.path.join(resources_directory, "internet.mp3")
screenshot_path = os.path.join(script_directory, "screenshot.png")
pixelated_path = os.path.join(script_directory, "pixelated_dingus.png")


# Initialize Tkinter window
root = tk.Tk()
root.withdraw()

ping_window = tk.Toplevel()
ping_window.geometry("200x50+30+30")
ping_window.attributes('-topmost', True)
ping_window.overrideredirect(True)
ping_window.config(bg="black")

ping_label = tk.Label(ping_window, text="Ping: --", font=("Comic Sans MS", 18, "bold"), fg="white", bg="black")
ping_label.pack(expand=True, fill="both")


def play_sound_moroccan():
    global playing
    if not playing:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_PATH)
        pygame.mixer.music.play(-1)
        playing = True


def stop_moroccan_sound():
    global playing
    if playing:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        playing = False


def capture_screenshot():
    global screenshot_path, pixelated_path

    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    img = Image.open(screenshot_path)
    img_size = random.randint(1, 20)
    small_size = (img.width // img_size, img.height // img_size)
    img = img.resize(small_size, Image.NEAREST)
    img = img.resize((img.width * img_size, img.height * img_size), Image.NEAREST)
    img.save(pixelated_path)

    root.after(5000, capture_screenshot)


def update_ping():
    global prev_ping, playing
    current_group = next(i for i, (low, high) in enumerate(groups) if low <= prev_ping <= high)

    low, high = groups[current_group]
    prev_ping = random.randint(low, high)

    group_colors = {0: "white", 1: "green", 2: "orange", 3: "red"}
    ping_label.config(text=f"Ping: {prev_ping}ms", fg=group_colors[current_group])

    if current_group == 3:
        if not playing:
            play_sound_moroccan()
    else:
        if playing:
            stop_moroccan_sound()

    if prev_ping > 850:
        trigger_event()

    root.after(500, update_ping)


def trigger_event():
    global pixelated_path
    print("Trigger event fired!")
    root.after(125)
    capture_screenshot()

    overlay = tk.Toplevel()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-topmost', True)

    img = Image.open(pixelated_path)
    image = ImageTk.PhotoImage(img)
    label = tk.Label(overlay, image=image)
    label.image = image
    label.pack(expand=True, fill="both")

    overlay.after(500, lambda: overlay.destroy())


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
    if not check_yahamouse_running():
        print("[LAG Debug] yahamouse.py not running. Exiting...")
        root.destroy()
        sys.exit()
    root.after(5000, monitor_yahamouse)  # Check again in 5 seconds


# Start monitoring and GUI loops
monitor_yahamouse()
update_ping()
root.mainloop()
