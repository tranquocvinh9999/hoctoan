import tkinter as tk
from gtts import gTTS
import os
import pygame

def speak(text):
    # Tạo âm thanh từ văn bản
    tts = gTTS(text=text, lang='vi')
    tts.save("temp.mp3")
    
    # Phát âm thanh
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

def on_hover(event, button_name):
    # Khi di chuột vào nút bấm
    speak(button_name)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giao diện Nút Bấm")

# Tạo nút bấm
button = tk.Button(root, text="Nút Bấm 1", width=210)
button.pack(pady=20)

# Gán sự kiện di chuột vào nút bấm
button.bind("<Enter>", lambda event: on_hover(event, button['text']))
button1 = tk.Button(root, text="Nút Bấm 2", width=50)
button1.pack(pady=20)

# Gán sự kiện di chuột vào nút bấm
button1.bind("<Enter>", lambda event: on_hover(event, button['text']))

# Chạy vòng lặp chính
root.mainloop()
