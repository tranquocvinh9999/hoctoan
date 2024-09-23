import random
import time
import os
import pygame
import gtts
from gtts import gTTS
import sys
import json
import msvcrt  
vietnamese = False

pygame.mixer.init()

with open("config/data.json") as f:
    setting = json.load(f)
    file_counter = setting.get("filecount", 0)

def get_next_file_name():
    global file_counter
    file_counter += 1
    with open("config/data.json", "w") as f:
        json.dump({"filecount": file_counter}, f)
    return f'stuff/temp_{file_counter}.mp3'

def speak(text):
    file_path = get_next_file_name()
    lang = 'vi'
    tts = gTTS(text, lang=lang)
    
    tts.save(file_path)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
def input_with_speak(prompt):
    speak(prompt)
    result = ""
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8')
            if char in ('\r', '\n'):
                break
            if char.isdigit() or char == '.' or char.islower():
                result += char
                speak(char)
            elif char == '\b': 
                if result:
                    result = result[:-1]
                    speak("backspace")
    return result
