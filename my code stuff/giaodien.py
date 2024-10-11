import random
import time
import os
import pygame
import gtts
from gtts import gTTS
import sys
import json
import msvcrt  
import tkinter as tk
import os


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
def on_hover(event, button_name):
    speak(button_name)

root = tk.Tk()
root.title("Giao diện Nút Bấm")

button = tk.Button(root, text="Bài Giảng", width=100, height=10)
button.pack(pady=20)


button.bind("<Enter>", lambda event: on_hover(event, button['text']))

button1 = tk.Button(root, text="Luyện Tập", width=100, height=10)
button1.pack(pady=20)


button1.bind("<Enter>", lambda event: on_hover(event, button['text']))


root.mainloop()
