import sys
import json
import threading
import os
import speech_recognition as sr
from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
import google.generativeai as genai
from functions.microphone.micro import check
from AI.bot import generate_questions_from_a_name_AI
API_KEY = 'AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA'

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")

def check_question_AI(question, answer, user_answer):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            f"""Giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: 
            Hãy giải bài toán: "{question}". Kết quả học sinh gửi tôi là "{user_answer}"
            và kết quả đúng của câu hỏi là "{answer}". Bạn hãy kiểm tra nếu kết quả này là đúng hay sai. 
            Nếu đúng, không tạo câu trả lời mà chỉ in ra 'Đúng' và nếu sai 'Sai' và để chữ 'Sai' ở đầu câu 
            thì trả về các bước để khắc phục nhưng không được nêu ra đáp án. Bạn nhắc nhở rằng 
            bạn đang nói với học sinh của bạn bằng cách xưng em chi tiết hơn nhé và cảm xúc như thầy trò nhé.
            Vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao 
            với trường hợp đó. ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao, 
            chỉ trả về hai giá trị 'Đúng' và 'Sai' thôi không ừm gì hết. 
            Các câu trả lời đúng sai như 'CÓ' hoặc 'KHÔNG' học sinh của tôi trả lời phải hoặc đúng hoặc 2 từ đó không dấu thì nhận diện giúp tôi. VÀ HÃY KIỂM TRA KẾT QUẢ CỦA HỌC SINH TÔI NHẬP VỚI KẾT QUẢ ĐÚNG VÌ CÓ MẤY LẦN HỌC SINH TÔI NHẬP ĐÚNG VỚI KẾT QUẢ ĐÚNG THÌ BẠN LẠI BẢO SAI
            VÍ DỤ CÁC CÂU CÓ DẤU PHẨY NHƯ 5, 3, 2, 1 MÀ HỌC SINH TÔI TRẢ LỜI LÀ 5 3 2 1 THÌ BẠN HÃY NÓI ĐÚNG NHÉ
            """ 
        )

        if "Đúng" in response.text:
            return True, response.text
        elif "Sai" in response.text:
            return False, response.text
    except Exception as e:
        print(f"Error during API call: {e}")
    
    return False, "Đã xảy ra lỗi khi kiểm tra câu trả lời."
import requests
def send_data(score, correct, wrong, username):
    url = "http://127.0.0.1:5000/scores"
    data = {
        "name": username,
        "correct": correct,
        "score": score,
        "wrong": wrong
    }
    res = requests.post(url, json=data)

def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.5 
    recognizer.energy_threshold = 200  

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language='vi-VN')
            speak(f"Bạn đã nói: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            speak("Xin vui lòng nói...")
            return None
        except sr.UnknownValueError:
            speak("Xin lỗi, tôi không thể hiểu bạn.")
            return None
        except sr.RequestError as e:
            speak(f"Không thể kết nối đến dịch vụ nhận dạng giọng nói: {e}")
            return None

class Ui_Dialog(QtCore.QObject):
    check_finished = QtCore.pyqtSignal(bool, str)
    danoi = False
    
    def setupUi(self, Dialog, main_dialog=None):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Kiểm Tra Câu Hỏi")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: #f0f0f0;")

        self.setup_ui_elements(Dialog)
        self.setup_signals()
        self.ask_chapter()

    def setup_ui_elements(self, Dialog):
        main_layout = QtWidgets.QVBoxLayout(Dialog)

        self.cauhoi = QtWidgets.QTextBrowser(Dialog)
        self.cauhoi.setStyleSheet("font: 16pt 'MS Shell Dlg 2'; border: 2px solid #0078D7; border-radius: 8px;")
        main_layout.addWidget(self.cauhoi)

        stats_layout = QtWidgets.QHBoxLayout()

        self.label_3 = QtWidgets.QLabel("Số câu đúng:", Dialog)
        self.label_3.setStyleSheet("font: 16pt 'MS Shell Dlg 2';")
        stats_layout.addWidget(self.label_3)

        self.socaudung = QtWidgets.QLCDNumber(Dialog)
        self.socaudung.setStyleSheet("background-color: #A0D0E0; border-radius: 5px;")
        stats_layout.addWidget(self.socaudung)

        self.label_2 = QtWidgets.QLabel("Số câu sai:", Dialog)
        self.label_2.setStyleSheet("font: 16pt 'MS Shell Dlg 2';")
        stats_layout.addWidget(self.label_2)

        self.socasai = QtWidgets.QLCDNumber(Dialog)
        self.socasai.setStyleSheet("background-color: #E0A0A0; border-radius: 5px;")
        stats_layout.addWidget(self.socasai)

        main_layout.addLayout(stats_layout)

        self.nhapketqua = QtWidgets.QLineEdit(Dialog)
        self.nhapketqua.setStyleSheet("font: 26pt 'MS Shell Dlg 2'; color: #333333; border: 2px solid #0078D7; border-radius: 8px;")
        main_layout.addWidget(self.nhapketqua)

        self.checkbutton = QtWidgets.QPushButton("Kiểm tra", Dialog)
        self.checkbutton.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #0078D7; border-radius: 10px;")
        main_layout.addWidget(self.checkbutton)

        self.back_button = QtWidgets.QPushButton("Quay lại", Dialog)
        self.back_button.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #D70000; border-radius: 10px;")
        main_layout.addWidget(self.back_button)

        self.cauhoi.setMinimumHeight(200)
        self.nhapketqua.setMinimumHeight(50)

        main_layout.addStretch()

        self.checkbutton.enterEvent = lambda event: self.speak_button_function("Kiểm tra câu trả lời.")
        self.back_button.enterEvent = lambda event: self.speak_button_function("Quay lại chương trước.")
        self.nhapketqua.enterEvent = lambda event: self.speak_button_function("Nhập Kết Quả Tại Đây")


    class MouseEventFilter(QtCore.QObject):
        def eventFilter(self, source, event):
            if event.type() == QtCore.QEvent.Enter:
                if isinstance(source, QtWidgets.QPushButton):
                    source.enterEvent(event)
            return super().eventFilter(source, event)
        
    def setup_signals(self):
        self.checkbutton.clicked.connect(self.check_answer)
        self.back_button.clicked.connect(self.go_back)
        self.check_finished.connect(self.on_check_finished)
        self.nhapketqua.textChanged.connect(self.on_text_changed)
        self.checkbutton.clicked.connect(lambda: self.speak_button_function("Kiểm tra câu trả lời."))
        self.back_button.clicked.connect(lambda: self.speak_button_function("Quay lại chương trước."))

    def speak_button_function(self, function_description):
        speak(function_description)

    def start_voice_recognition(self):
        self.checkbutton.setDisabled(True)
        self.thread = VoiceRecognitionThread()
        self.thread.recognized_text.connect(self.process_recognized_text)
        self.thread.start()

    def fetch_chapters(self):
        chapters = []
        for folder in os.listdir("AI/question_folder"):
            if os.path.isdir(os.path.join("AI/question_folder", folder)):
                chapters.append(folder)
        return chapters

    def ask_chapter(self):
        if not self.danoi:  
            chapters = self.fetch_chapters()
            if chapters:
                speak("Chọn chương bạn muốn kiểm tra.")
                for chapter in chapters:
                    speak(f"Chương: {chapter}")

                self.voice_recognition = VoiceRecognitionThread()
                self.voice_recognition.recognized_text.connect(self.on_chapter_recognized)
                self.voice_recognition.start()
                self.danoi = True

    def on_chapter_recognized(self, chapter_name):
        if chapter_name:
            self.selected_chapter = chapter_name.lower()
            speak(f"Bạn đã chọn chương: {self.selected_chapter}")
            generate_questions_from_a_name_AI(self.selected_chapter, 10)
            self.load_questions()
        else:
            speak("Xin vui lòng thử lại.")

    def load_questions(self):
        try:
            with open(f'AI/question_folder/{self.selected_chapter}/questions.json', 'r', encoding='utf-8') as f:
                self.cauhoi_dict = json.load(f)

            self.current_question = 0
            self.correct_answers = 0
            self.incorrect_answers = 0
            self.show_question()
            self.checkbutton.setEnabled(True) 

        except FileNotFoundError:
            speak("Không tìm thấy câu hỏi cho chương này.")
        except json.JSONDecodeError:
            speak("Có lỗi xảy ra khi đọc file câu hỏi.")

    def on_text_changed(self):
        if self.nhapketqua.text():
            last_char = self.nhapketqua.text()[-1] 
            if last_char == " ":
                speak("dấu cách")
            else:
                speak(f"{last_char}")

    def show_question(self):
        question = self.cauhoi_dict[self.current_question]["question"]
        self.cauhoi.setText(question)
        speak(question)

    def check_answer(self):
        speak("bạn đã nhấn kiểm tra câu trả lời hãy chờ nhé")
        user_answer = self.nhapketqua.text().strip()
        correct_answer = self.cauhoi_dict[self.current_question]["answer"].strip()

    
        if ',' in correct_answer:
            user_answer = correct_answer.replace(" ", ", ")

  
        if correct_answer.lower() in ["có", "yes", "y"]:
            user_answer = "có"
        elif correct_answer.lower() in ["không", "no", "n"]:
            user_answer = "không"
        elif correct_answer.lower() in ["lon hon", "lớn hơn"]:
            user_answer = user_answer.replace("lon hon", ">")
        elif correct_answer.lower() in ["be hon", "bé hơn"]:
            user_answer = user_answer.replace("be hon", "<")
        user_answer = user_answer


        is_correct, feedback = check_question_AI(self.cauhoi_dict[self.current_question]["question"], correct_answer, user_answer)

        if is_correct:
            self.correct_answers += 1
            self.socaudung.display(self.correct_answers)
            self.nhapketqua.clear()
        else:
            self.incorrect_answers += 1
            self.socasai.display(self.incorrect_answers)
            self.nhapketqua.clear()

        print(user_answer)
        print(correct_answer)
        self.check_finished.emit(is_correct, feedback)

    def on_check_finished(self, is_correct, feedback):
        if is_correct:
            speak("Đúng!")
        else:
            speak("Sai!")
        speak(feedback)
        self.next_question()

    def submit_scores(self):
        with open("config/private.json") as f:
            file_data = json.load(f)
            username = file_data["username"]

        url = "http://127.0.0.1:5000/scores/" + username
        data = requests.get(url).json()

        a = self.correct_answers 
        b = self.incorrect_answers 
        c = a - b  

        new_correct = data["user_correct"] + a
        new_wrong = data["user_fail"] + b
        new_score = data["user_score"] + len(self.cauhoi_dict)   

        send_data(new_score, new_correct, new_wrong, username)
    def go_back(self):
        speak("Quay lại.")

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.cauhoi_dict):
            self.show_question()
        else:
            speak("Bạn đã hoàn thành tất cả các câu hỏi.")
            self.submit_scores()  
            self.back_button()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    app.installEventFilter(MouseEventFilter())
