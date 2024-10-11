import requests
from functions.keyboard.keyboards import speak
from functions.microphone.micro import check
from functions.microphone.micro import recognize_speech


def upload(file_path):
    url = "http://127.0.0.1:5000/upload"
    with open(file_path, 'rb') as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            speak("bài giảng đã được tải lên thành công")
        else:
            speak("gửi bài giảng thất bại")
