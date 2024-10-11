import requests
from functions.keyboard.keyboards import speak

def get_lessons_info(folder_name):
    url = f'http://localhost:5000/download/info/{folder_name}'  
    response = requests.get(url)
    if response.status_code == 200:
        info = response.text
        print("Thông tin bài giảng:\n", info)
    else:
        print("Tải dữ liệu thất bại!")

def download_file(file_name):
    url = f'http://localhost:5000/download/{file_name}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"baigiang/{file_name}", 'wb') as f:
            f.write(response.content)
        speak(f"Bài giảng {file_name} đã được tải về.")
        return True
    else:
        speak("Tải file thất bại.")
        return False


def handler(name):
    name.lower()
    k = name.replace(" ", "")
    get_lessons_info(k)
    