import requests
from functions.keyboard.keyboards import speak
from functions.microphone.micro import check
from functions.microphone.micro import recognize_speech
import json
with open("ip_host.json") as f:
    settings = json.load(f)
    ip = settings["ip"]
    port = settings["port"]

def upload(file_path):
    url = f"http://{ip}:{port}/upload"
    with open(file_path, 'rb') as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            speak("bài giảng đã được tải lên thành công")
        else:
            speak("gửi bài giảng thất bại")
