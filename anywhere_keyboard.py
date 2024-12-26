import os
import time
import server
import requests
import pyautogui
import pyperclip 
from pynput import keyboard

INACTIVITY_THRESHOLD = 5

last_pressed_time = time.time()

def on_press(key):
    global last_pressed_time
    last_pressed_time = time.time()

def check_inactivity():
    global last_pressed_time
    current_time = time.time()
    if current_time - last_pressed_time >= INACTIVITY_THRESHOLD:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.press('backspace')
        clipboard_content = pyperclip.paste()
        return clipboard_content

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    try:
        clipboard = check_inactivity()
        if clipboard is None:
            continue
        time.sleep(1)

        data = server.request_server(model="mistral", stream=False, task="segncorrect", data="` " + clipboard + " `")
        # print(data)
        for word in data['words']:
            for i in word:
                pyautogui.press(i)
            pyautogui.press("space")
        pyperclip.copy('')

    except KeyboardInterrupt:
        exit()
    except requests.exceptions.ConnectionError:
        os.system("start ollama serve & exit")
        server.request_server(model="mistral", stream=False, task="segncorrect", data="` " + clipboard + " `")

    # print("\n\n")
