import requests
import json
import os
import re
import time
import pyautogui
import pyperclip
from pynput import keyboard

API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}
INACTIVITY_THRESHOLD = 5

last_pressed_time = time.time()

def extract_words_from_stream(stream_data):
    word_regex = r"\b\w+\w*"
    words = re.findall(word_regex, stream_data)
    return words

def request_server(model, prompt, stream=True):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "format": "json"
    }

    response = requests.post(API_URL, headers=HEADERS, json=data, stream=stream)

    if response.status_code == 200:
        if stream:
            for chunk in response.iter_content(chunk_size=1024):
                stream_data = json.loads(chunk.decode("utf-8"))["response"]
                words = extract_words_from_stream(stream_data)
                for i, j in enumerate(words):
                    if i == 0 and j == "words":
                        continue
                    else:
                        pyautogui.write(j + ' ')  

        else:
            data = json.loads(json.loads(response.text.strip("\n"))["response"])
            for i in data['words']:
                pyautogui.write(i + ' ')  

    else:
        print("Error:", response.text)

def on_press(key):
    global last_pressed_time
    last_pressed_time = time.time()

def check_inactivity():
    global last_pressed_time
    current_time = time.time()
    if current_time - last_pressed_time >= INACTIVITY_THRESHOLD:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        clipboard_content = pyperclip.paste()
        return clipboard_content

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    prompt = "You are a word segmenter and auto-corrector.\
    You are given a sentence with no spaces, you need to figure out where the spaces go & also correct the words if they are wrong. \
    Output a JSON with a key called `words` and a list of words. \
    Eg: {'words':['This', 'is','an','example']} \
    The sentence is: "

    try:
        clipboard = check_inactivity()
        if clipboard is None:
            continue
        time.sleep(1)

        request_server(model="gemma2:2b", prompt=prompt + "' " + clipboard + " '", stream=True)

    except KeyboardInterrupt:
        exit()
    except requests.exceptions.ConnectionError:
        os.system("start ollama serve & exit")
        request_server(model="gemma2:2b", prompt=prompt, stream=True)

    print("\n\n")
