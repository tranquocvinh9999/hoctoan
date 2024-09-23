import tkinter as tk
from tkinter import ttk
from functions.keyboard.keyboards import speak, input_with_speak
from AI.bot import random_10_cau_hoi_nhan_cong_tru
import random

class MathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Học Toán")
        
        self.frames = {}
        self.create_frames()
        
        self.show_frame("MainFrame")

    def create_frames(self):
        # Tạo trang chính
        main_frame = tk.Frame(self.root)
        self.frames["MainFrame"] = main_frame
        main_frame.pack(fill="both", expand=True)

        # Nút để làm bài kiểm tra 10 câu hỏi
        button_10_questions = tk.Button(main_frame, text="Làm 10 Câu Hỏi", command=self.start_ten_question)
        button_10_questions.pack(pady=10)

        # Nút để đọc bảng cửu chương từ 1 đến 10
        button_bang_cuu_chuong_tu_1_10 = tk.Button(main_frame, text="Đọc Bảng Cửu Chương 1-10", command=self.bang_cuu_chuong_tu_1_10)
        button_bang_cuu_chuong_tu_1_10.pack(pady=10)

        # Nút để đọc bảng cửu chương của một số cụ thể
        button_bang_cuu_chuong_cua_1_so = tk.Button(main_frame, text="Đọc Bảng Cửu Chương Của Một Số", command=self.bang_cuu_chuong_cua_1_so)
        button_bang_cuu_chuong_cua_1_so.pack(pady=10)

        # Tạo trang nhập số
        self.question_frame = tk.Frame(self.root)
        self.frames["QuestionFrame"] = self.question_frame

        # Nhãn và ô nhập
        self.label_question = tk.Label(self.question_frame, text="")
        self.label_question.pack(pady=10)

        self.entry_answer = tk.Entry(self.question_frame)
        self.entry_answer.pack(pady=10)

        self.submit_button = tk.Button(self.question_frame, text="Gửi Kết Quả", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.question_frame, text="")
        self.result_label.pack(pady=10)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def start_ten_question(self):
        self.questions = random_10_cau_hoi_nhan_cong_tru()
        self.current_question = 0
        self.correct = 0
        self.next_question()

    def next_question(self):
        if self.current_question < len(self.questions):
            k, a, b, res = self.questions[self.current_question]
            self.label_question.config(text=self.get_question_text(k, a, b))
            self.entry_answer.delete(0, tk.END)
            self.result_label.config(text="")
            self.show_frame("QuestionFrame")
        else:
            speak(f"Bạn đã làm xong 10 câu hỏi. Bạn đúng được {self.correct} trên tổng số 10 câu hỏi.")
            self.show_frame("MainFrame")

    def get_question_text(self, k, a, b):
        if k == 1:
            return f"Số đầu tiên là: {a}, Số thứ hai là: {b}. Tích của {a} và {b} là gì?"
        elif k == 2:
            return f"Số đầu tiên là: {a}, Số thứ hai là: {b}. Tổng của {a} và {b} là gì?"
        elif k == 3:
            return f"Số đầu tiên là: {a}, Số thứ hai là: {b}. Hiệu của {a} và {b} là gì?"

    def submit_answer(self):
        try:
            user_input = float(self.entry_answer.get())
            k, a, b, res = self.questions[self.current_question]

            if user_input == res:
                speak("Bạn đã đúng")
                self.correct += 1
            else:
                speak("Bạn đã sai")

            self.current_question += 1
            self.next_question()
        except ValueError:
            speak("Vui lòng nhập một số hợp lệ.")

    def bang_cuu_chuong_tu_1_10(self):
        for i in range(1, 11):
            speak(f"Bảng cửu chương số {i} là")
            for j in range(1, 11):
                res = i * j
                speak(f"{i} nhân cho {j} là {res}")

    def bang_cuu_chuong_cua_1_so(self):
        n = int(input_with_speak("Hãy Nhập Số Bảng Cửu Chương:"))
        self.bang_cuu_chuong_cua_1_so(n)

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = MathApp(root)
    root.mainloop()
