import requests
import json
import os
import re


API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

def extract_words_from_stream(stream_data):
    word_regex = r"\b\w+\w*"
    words = re.findall(word_regex, stream_data)
    return words

def request_server(model, stream=False, task="segncorrect", data=None, n=None):

    if task == "segncorrect":
        prompt = "You are a word segmenter and auto-corrector.\
        You are given a sentence with no spaces, you need to figure out where the spaces go & also correct the words if they are wrong. \
        Output a JSON with a key called `words` and a list of words. \
        Eg: {'words':['This', 'is','an','example']} \
        The sentence is: " + data

    elif task == "predict":
        prompt = "You are a word prediction model. \
        Given a partial sentence, your task is to predict the next n most likely words that could follow it. \
        The output should be in the form of a JSON object containing a key called `words` with a list of the top "+ n +" predicted words. \
        Eg: if the input sentence is 'How are you', the output can be {'words': ['doing', 'today', 'feeling', 'going']}. \
        The partial sentence is: " + data

    else:
        print("Invalid task")
        return

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
                return words

        else:
            data = json.loads(json.loads(response.text.strip("\n"))["response"])
            return data

    else:
        print("Error:", response.text)


if os.system("curl http://localhost:11434") != 0:
    os.system("start ollama serve & exit")
    print()
