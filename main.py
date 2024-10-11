from functions.login_register.logn import login_register_main
from functions.microphone.micro import check
from functions.keyboard.keyboards import speak
from AI.bot import generate_questions_from_a_name_AI
from AI.bot import get_data_from_given_question_and_ask_AI
from functions.microphone.micro import recognize_speech
import keyboard
from functions.get_lesson_from_server.upload import upload
from functions.get_lesson_from_server.get import download_file
import json
import requests
# 123
# bài tập 
# bài giảng
# giáo viên lấy kết quả tổng các bài kiểm tra
# đăng ký đăng nhập
# bảng cửu chương
# nhập từ bàn phím
# AI về tạo bài tập với check kết quả
def check_number():
    speak("Vui lòng nói số bài tập.")
    num = recognize_speech()

    if num is None:
        speak("Xin lỗi, tôi không nghe rõ. Vui lòng thử lại.")
        return check_number()

    numbers = {
        "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5,
        "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10
    }
    if num.startswith("số "):
        num = num.split(" ", 1)[1]

    if num in numbers:
        return numbers[num]
    elif num.isdigit():
        return int(num)
    else:
        speak("Vui lòng nói một số hợp lệ.")
        return check_number()

def create_pratice():
    speak("Hãy nói chương mà bạn muốn.")
    chapter = check()

    if chapter:
        speak(f"Chương bạn chọn là {chapter}.")
        num_of_exercises = check_number()

        if num_of_exercises:
            speak(f"Bạn đã chọn {num_of_exercises} bài tập.")
            generate_questions_from_a_name_AI(chapter, num_of_exercises)
        else:
            speak("Vui lòng nhập số hợp lệ.")
            create_pratice()
def pratice():
    speak("Hãy nói chương mà bạn muốn luyện tập")
    chapter = check()
    if chapter.strip():
        get_data_from_given_question_and_ask_AI(str(chapter))

def manu(
):
    speak("Chào bạn đã tới chương trình")
    speak("Nếu bạn muốn nói gì thì cứ nhấn Q nhé")
    
    while True:
        if keyboard.is_pressed('q'):
            check()
def send_data(score, correct, wrong, username):
    url = "http://127.0.0.1:5000/scores"
    data = {
        "name": username,
        "correct": correct,
        "score": score,
        "wrong": wrong
    }
    res = requests.post(url, json=data)

def receive_data_from_server():
    url = "http://127.0.0.1:5000/get_information_ranks"
    res = requests.get(url)
    response = res.json()
    print(res.json())
    for name, data in response.items():
        print(f"{name}")
        print(f"{data["rank"]}")
        print(f"{data["user_correct"]}")
        print(f"{data["user_fail"]}")
        print(f"{data["user_score"]}")
        print("----------------")

#generate_questions_from_a_name_AI("số thực", 15)
# k = 'sus.txt'
# upload(k)
# k = 'sus.txt'
# download_file(k)

with open("config/score.json") as f:
    settings = json.load(f)
    old_score = settings["user_score"]
    old_correct = settings["user_correct"]
    old_wrong = settings["user_wrong"]
    username = settings["user"]
def submit_scores():
    a, b, c = get_data_from_given_question_and_ask_AI("số nguyên tố")
    new_correct = old_correct + a
    new_wrong = old_wrong + b
    new_score = old_score + c
    speak(f"chúc mừng bạn đã đúng được {a} câu và {b} câu sai tổng kết điểm là {c}")
    data = {
            "user_score": {new_score},
            "user_correct": {new_correct},
            "user_wrong": {new_wrong}
        }
    with open("config/score.json") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    send_data(new_score, new_correct, new_wrong, username)
receive_data_from_server()

# lay bai giang
from functions.get_lesson_from_server.get import get_lessons_info, download_file

def baigiang(name):
    k = download_file(name)
    if k == True:
        speak("Bạn có muốn nghe giảng bây giờ luôn không nói Có hoặc không để tiếp tục")
        t = check()
        if t == "có":
            with open(f"baigiang/{name}", "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                speak(line.strip())
        else:
            manu()
