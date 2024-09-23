import time
from functions.keyboard.keyboards import speak
from functions.keyboard.keyboards import input_with_speak
from functions.maths.math import ten_question, bang_cuu_chuong_cua_1_so, bang_cuu_chuong_tu_1_10
from functions.microphone.micro import recognize_speech
# nói 1 thay vì nhấn 1
def mainop():
    while True:
        # speak("Chào bạn đã đến tới phần mềm cùng em học toán sáu")
        speak("Nói tham gia toán cộng để tham gia vào làm bài kiểm tra về nhân chia cộng trừ nhé")
        speak("Nói xem bảng cửu chương để xem lại bảng cửu chương nhé")
        t = recognize_speech()
        print(t)
        # if t == "một":
        #     ten_question()
        # elif t == "hai":
        #     speak("Bạn muốn mình đọc hết từ một tới mười hay là một số thôi nhỉ")
        #     time.sleep(0.5)
        #     k = input_with_speak("Nhập y thì mình sẽ đọc từ một tới mười còn không nhập n để mình đọc một số mà bạn muốn nhé")
        #     if k.lower() == "y":
        #         bang_cuu_chuong_tu_1_10()
        #     elif k.lower() == "n":
        #         num = input_with_speak("nhập số bạn muốn nào")
        #         bang_cuu_chuong_cua_1_so(int(num))

if __name__ == "__main__":
    mainop()
