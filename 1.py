from pynput import keyboard
from threading import Thread
from time import sleep

import pyperclip
import json

# The key combinations to check
COMBINATIONS = [
]
hotkeyData = {}

# The currently active modifiers
current = set()

def loadDataFromFile():
    f = open('data.json')
    data = json.load(f)
    for x in data["Text"]:
        COMBINATIONS.append({keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode(char=x["Hotkey"])})
        hotkeyData[x["Hotkey"]] = x["Data"]

def on_press(key):
    if any([key in comb for comb in COMBINATIONS]):
        current.add(key)
        if any([all(k in current for k in comb) for comb in COMBINATIONS]):
            for x in current:
                try:
                    if key.char in hotkeyData:
                        pyperclip.copy(hotkeyData[key.char])
                except AttributeError:
                    print("Error")

    if key == keyboard.Key.esc:
        listener.stop()

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def main_function():
    print('Main function fired!')
    # rest of your code here...

loadDataFromFile()

with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard.listener:
    keyboard.listener.join()