from functions.keyboard.keyboards import speak
from functions.keyboard.keyboards import input_with_speak
import random
from AI.bot import random_10_cau_hoi_nhan_cong_tru 

def ten_question():
    questions = random_10_cau_hoi_nhan_cong_tru()
    correct = 0
    for question in questions:
        k, a, b, res = question
        
        if k == 1:
            speak(f"Số đầu tiên là: {a}")
            speak(f"Số thứ hai là: {b}")
            speak(f"Tích của {a} và {b} là gì?")
        elif k == 2:
            speak(f"Số đầu tiên là: {a}")
            speak(f"Số thứ hai là: {b}")
            speak(f"Tổng của {a} và {b} là gì?")
        elif k == 3:
            speak(f"Số đầu tiên là: {a}")
            speak(f"Số thứ hai là: {b}")
            speak(f"Hiệu của {a} và {b} là gì?")
        
        user_input = float(input_with_speak("Hãy Nhập Kết Quả Nhé"))
        
        if user_input == res:
            speak("Bạn đã đúng")
            correct += 1
        else:
            speak("Bạn đã sai")
    
    speak(f"Bạn đã làm xong 10 câu hỏi về cộng, trừ, nhân. Bạn đúng được {correct} trên tổng số 10 câu hỏi.")

def bang_cuu_chuong_tu_1_10():
    for i in range(1, 11):
        speak(f"Bảng cửu chương số {i} là")
        for j in range(1, 11):
            res = i * j
            speak(f"{i} nhân cho {j} là {res}")

def bang_cuu_chuong_cua_1_so(n):
    speak(f"Bảng cửu chương số {n}")
    for i in range(1, 11):
        res = n * i 
        speak(f"{n} nhân {i} là {res}")
