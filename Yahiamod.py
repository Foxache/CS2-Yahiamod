import importlib.util
import sys
import os
import subprocess
from sys import system

system('mode con: cols=200 lines=49')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if input("\nYahiamod requires administator privileges to run properly.\n\nYahiamod will change CounterStrike files but none are irreversable.\n\nYahiamod Hardmode can and will put your counterstrike directory at RISK. If it is hard to reinstall counterstrike it is not recommended.\nYou will be asked later if you want to enable hardmode.\n\n\nContinue? [N/y): ").lower() != 'y':
    print("Exiting...")
    exit()

print("Checking python version...")

if sys.version_info[0] < 3:
    print("Python version is not 3. Please install Python 3 for Yahiamod to function as intended.")
    input("Press any buttom to exit...")
    exit()

print("Checking for required libraries...")

with open('requirements.txt', 'r') as file:
    contents = file.read()
    line_count = contents.count('\n')
    
for y in range(0, line_count):
    with open('requirements.txt', 'r') as file:
        if 'missing_libraries' not in locals():
            missing_libraries = []
        lines = file.readlines()
        retrieved_line = lines[y]
        if importlib.util.find_spec(retrieved_line.strip()) is None:
            print(f"Missing library detected: {retrieved_line.strip()}")
            missing_libraries.append(retrieved_line.strip())


if len(missing_libraries) > 0:
    print("\nThe following libraries are missing:")
    for lib in missing_libraries:
        print(f"- {lib}")

    print("\nYahiamod can attempt to install the missing libraries using pip.")
    print("This process will use extra internet data\n Once the process is completed you will need to restart this program.")
    if input("Continue? [N/y): ").lower() != 'y':
        print("Exiting...")
        exit()

    print("Is PIP installed and added to PATH? (Python Package Manager. If you dont know input N)")
    if input("[N/y): ").lower() != 'y':
        print("Yahiamod cannot install pip for you.\n In 10 seconds the program will send you to the PIP website.\n if it does not open, the link is: https://pip.pypa.io/en/stable/installation/")
        import webbrowser
        import time
        time.sleep(10)
        webbrowser.open("https://pip.pypa.io/en/stable/installation/")
        print("Exiting...")
        exit()

    print("Attempting to install missing libraries...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', *missing_libraries])

    while True:
        time.sleep(2)
        print("If the installation was successful please restart the program now.\n Use CTRL+C to exit.")

print("Yahiamod starting...")

subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, 'Scripts', 'server_rewrite.py')])
