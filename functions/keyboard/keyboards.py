import time
import os
import pygame
from gtts import gTTS
import sys
import json
from functions.resource_path.path import resource_path
pygame.mixer.init()

with open(resource_path("config/data.json")) as f:
    setting = json.load(f)
    file_counter = setting.get("filecount", 0)

def get_next_file_name():
    global file_counter
    file_counter += 1
    with open(resource_path("config/data.json"), "w") as f:
        json.dump({"filecount": file_counter}, f)
    return f'stuff/temp_{file_counter}.mp3'

def speak(text):
    file_path = get_next_file_name()
    lang = 'vi'
    tts = gTTS(text, lang=lang, slow=False)
    print(file_path)
    print(os.path.abspath(file_path))

    tts.save(file_path)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)