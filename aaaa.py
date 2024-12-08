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
from functions.resource_path.path import resource_path
API_KEY = 'AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA'

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")
file_pathss = resource_path("ip_host.json")
with open(file_pathss) as f:
    settings = json.load(f)
    ip = settings["ip"]
    port = settings["port"]
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
            bạn đang nói với học sinh của bạn bằng cách xưng em đối với học sinh và xưng thầy với bạn chi tiết hơn nhé và cảm xúc như thầy trò nhé.
            Vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao 
            với trường hợp đó. ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao, 
            chỉ trả về hai giá trị 'Đúng' và 'Sai' thôi không ừm gì hết. 
            Các câu trả lời đúng sai như 'CÓ' hoặc 'KHÔNG' học sinh của tôi trả lời phải hoặc đúng hoặc 2 từ đó không dấu thì nhận diện giúp tôi. VÀ HÃY KIỂM TRA KẾT QUẢ CỦA HỌC SINH TÔI NHẬP VỚI KẾT QUẢ ĐÚNG VÌ CÓ MẤY LẦN HỌC SINH TÔI NHẬP ĐÚNG VỚI KẾT QUẢ ĐÚNG THÌ BẠN LẠI BẢO SAI
            NẾU CÁC CÂU TRẢ LỜI ĐÚNG CÓ SẴN TRONG MÁY MÀ CÓ DẤU MÀ CÂU TRẢ LỜI CỦA HỌC SINH CỦA TÔI MÀ CÓ Ý NGHĨA GIỐNG VẬY THÌ TRẢ LỜI ĐÚNG NHÉ NHƯ LÀ CÂU TRẢ LỜI LÀ KHÔNG MÀ HỌC SINH TÔI TRẢ LỜI LÀ KHONG THÌ ĐÚNG CÁC CÂU TRONG MÁY NHƯ LÀ PHẢI MÀ HỌC SINH CỦA TÔI TRẢ LỜI LÀ PHAI HOẶC CO THÌ CŨNG BẢO ĐÚNG.
            NÓI CHUNG CÁC CÂU TRẢ LỜI TRONG MÁY MÀ HỌC SINH CỦA TÔI TRẢ LỜI SÁT NGHĨA VỚI CÂU TRẢ LỜI ĐÓ THÌ CHO ĐÚNG
            ĐẶC BIỆT CHÚ Ý VÍ DỤ CÁC CÂU CÓ DẤU PHẨY NHƯ 5, 3, 2, 1 MÀ HỌC SINH TÔI TRẢ LỜI LÀ 5 3 2 1 MÀ KHÔNG CÓ DẤU PHẨY NGĂN CÁCH THÌ BẠN HÃY NÓI ĐÚNG NHÉ,
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
    url = f"http://{ip}:{port}/scores"
    data = {
        "name": username,
        "correct": correct,
        "score": score,
        "wrong": wrong
    }
    res = requests.post(url, json=data)
SAVE_STATE_FILE = "config/baitapdangdo.json"
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

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)

class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Virtual Keyboard")
        layout = QVBoxLayout()

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setAccessibleName("Input Field")
        layout.addWidget(self.input_field)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1),
            ('Enter', 3, 2), ('Backspace', 3, 0),
            ('Space', 4, 1), (',', 4, 0), ('/', 4, 2),
            ('<', 5, 0), ('>', 5, 2),
        ]

        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.setFixedSize(100, 100)
            button.setAccessibleName(f"Button {text}")
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            grid_layout.addWidget(button, row, col)

        self.setLayout(layout)

    def on_button_click(self, button_text):
        if button_text == "Enter":
            print("Entered:", self.input_field.text())
        elif button_text == "Backspace":
            self.input_field.backspace()
        elif button_text == "Space":
            self.input_field.insert(" ")
        else:
            self.input_field.insert(button_text)

# Ui_Dialog class definition
class Ui_Dialog(QtCore.QObject):
    check_finished = QtCore.pyqtSignal(bool, str)
    danoi = False

    def setupUi(self, Dialog, main_dialog=None):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Kiểm Tra Câu Hỏi")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: #f0f0f0;")
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        Dialog.showFullScreen()

        self.setup_ui_elements(Dialog)
        self.setup_signals()
        self.ask_chapter()

        self.load_saved_state()

        # Add VirtualKeyboard below the main UI elements
        self.virtual_keyboard = VirtualKeyboard()
        self.main_layout.addWidget(self.virtual_keyboard)

    def setup_ui_elements(self, Dialog):
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)

        self.cauhoi = QtWidgets.QTextBrowser(Dialog)
        self.cauhoi.setStyleSheet("font: 16pt 'MS Shell Dlg 2'; border: 2px solid #0078D7; border-radius: 8px;")
        self.main_layout.addWidget(self.cauhoi)

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

        self.main_layout.addLayout(stats_layout)

        self.nhapketqua = QtWidgets.QLineEdit(Dialog)
        self.nhapketqua.setStyleSheet("font: 26pt 'MS Shell Dlg 2'; color: #333333; border: 2px solid #0078D7; border-radius: 8px;")
        self.main_layout.addWidget(self.nhapketqua)

        self.checkbutton = QtWidgets.QPushButton("Kiểm tra", Dialog)
        self.checkbutton.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #0078D7; border-radius: 10px;")
        self.main_layout.addWidget(self.checkbutton)

        self.back_button = QtWidgets.QPushButton("Quay lại", Dialog)
        self.back_button.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #D70000; border-radius: 10px;")
        self.main_layout.addWidget(self.back_button)

        self.continue_button = QtWidgets.QPushButton("Tiếp tục bài tập", Dialog)
        self.continue_button.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #28A745; border-radius: 10px;")
        self.main_layout.addWidget(self.continue_button)

        self.main_layout.addStretch()

    def setup_signals(self):
        self.checkbutton.clicked.connect(self.check_answer)
        self.back_button.clicked.connect(self.go_back)
        self.continue_button.clicked.connect(self.load_saved_state)

    def save_current_state(self):
        """Lưu trạng thái bài tập vào file JSON."""
        state = {
            "question": self.cauhoi.toPlainText(),
            "correct": self.socaudung.value(),
            "wrong": self.socasai.value(),
            "current": self.current_question,
            "chapter": self.selected_chapter
        }
        with open(SAVE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)

    def load_saved_state(self):
        """Tải trạng thái bài tập từ file JSON hoặc yêu cầu bắt đầu từ chương mới."""
        if os.path.exists(SAVE_STATE_FILE):
            with open(SAVE_STATE_FILE, "r", encoding="utf-8") as f:
                self.state = json.load(f)
                if self.state.get("question"):  
                    self.cauhoi.setText(self.state.get("question", ""))
                    self.socaudung.display(self.state.get("correct", 0))
                    self.socasai.display(self.state.get("wrong", 0))
                    self.current_chapter = self.state.get("chapter")
                    self.oppp = self.state.get("current", 0)
                    with open(resource_path(f'AI/question_folder/{self.current_chapter}/questions.json'), 'r', encoding='utf-8') as f:
                        self.abczz = json.load(f)
                    speak("Đã tiếp tục bài tập từ trạng thái lưu trước.")
                else:
                    speak("Không có câu hỏi nào trong trạng thái lưu. Bắt đầu từ chương mới.")
                    self.ask_chapter()
        else:
            speak("Không tìm thấy trạng thái bài tập. Bắt đầu từ chương mới.")
            self.ask_chapter()
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
        self.back_button.clicked.connect(lambda: self.speak_button_function("Quay lại menu chính"))

    def speak_button_function(self, function_description):
        speak(function_description)

    def start_voice_recognition(self):
        self.checkbutton.setDisabled(True)
        self.thread = VoiceRecognitionThread()
        self.thread.recognized_text.connect(self.process_recognized_text)
        self.thread.start()

    def fetch_chapters(self):
        chapters = []
        for folder in os.listdir(resource_path("AI/question_folder")):
            if os.path.isdir(os.path.join(resource_path("AI/question_folder"), folder)):
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
            generate_questions_from_a_name_AI(self.selected_chapter, 3)

            self.load_questions()
        else:
            speak("Xin vui lòng thử lại.")

    def load_questions(self):
        try:
            with open(resource_path(f'AI/question_folder/{self.selected_chapter}/questions.json'), 'r', encoding='utf-8')as f:
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
        if self.state.get("chapter") is not None:
            question = self.abczz[self.oppp]["question"]
        else:
            question = self.cauhoi_dict[self.current_question]["question"]
        self.cauhoi.setText(question)
        speak(question)

    def check_answer(self):
        speak("Bạn đã nhấn kiểm tra câu trả lời, hãy chờ nhé")
        user_answer = self.nhapketqua.text().strip()
        if self.state.get("chapter") is not None:
            correct_answer = self.abczz[self.oppp]["answer"].strip()
        else:
            correct_answer = self.cauhoi_dict[self.current_question]["answer"].strip()

        if all(char.isdigit() or char.isspace() for char in user_answer):
            user_answer = ', '.join(user_answer.split())

        if correct_answer.lower() in ["có", "yes", "y"]:
            user_answer = user_answer.lower()
            if user_answer in ["có", "yes", "y", "co"]:
                user_answer = "phải"
        elif correct_answer.lower() in ["không", "no", "n"]:
            user_answer = user_answer.lower()
            if user_answer in ["không", "no", "n", "khong"]:
                user_answer = "không"
        elif "lớn hơn" in correct_answer.lower() or "lon hon" in correct_answer.lower():
            user_answer = user_answer.replace("lon hon", ">").replace("lớn hơn", ">")
        elif "bé hơn" in correct_answer.lower() or "be hon" in correct_answer.lower():
            user_answer = user_answer.replace("be hon", "<").replace("bé hơn", "<")

        is_correct, feedback = check_question_AI(
            question=self.cauhoi_dict[self.current_question]["question"],
            answer=correct_answer,
            user_answer=user_answer
        )
        print(user_answer)
        print(correct_answer)
        if is_correct:
            self.correct_answers += 1
            self.socaudung.display(self.correct_answers)
            speak("Chính xác! Em giỏi lắm!")
            self.nhapketqua.clear()
        else:
            self.incorrect_answers += 1
            self.socasai.display(self.incorrect_answers)
            speak(feedback)  
            self.nhapketqua.clear()
        self.current_question += 1
        if self.current_question < len(self.cauhoi_dict):
            self.show_question()
        else:
            speak("Bạn đã hoàn thành tất cả các câu hỏi trong chương này. Chúc mừng!")
            self.submit_scores()
            self.checkbutton.setDisabled(True)

    def go_back(self):
        speak("Bạn đã nhấn nút quay lại. Chuyển về menu chính.")
        self.checkbutton.setDisabled(True)
        self.back_button.setDisabled(True)
        QtWidgets.QApplication.instance().quit()

    def on_check_finished(self, is_correct, feedback):
        if is_correct:
            speak("Đúng!")
        else:
            speak("Sai!")
        speak(feedback)
        self.next_question()

    def submit_scores(self):
        with open(resource_path("config/private.json")) as f:
            file_data = json.load(f)
            username = file_data["username"]

        url = f"http://{ip}:{port}/scores/" + username
        data = requests.get(url).json()

        a = self.correct_answers 
        b = self.incorrect_answers 
        c = a - b  

        new_correct = data["user_correct"] + a
        new_wrong = data["user_fail"] + b
        new_score = data["user_score"] + len(self.cauhoi_dict)   

        send_data(new_score, new_correct, new_wrong, username)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.cauhoi_dict):
            self.show_question()
        else:
            speak("Bạn đã hoàn thành tất cả các câu hỏi.")
            self.submit_scores()  
            self.back_button()
if __name__ == "__main__":
    app = QApplication(sys.argv)  
    dialog = Ui_Dialog()  
    sys.exit(app.exec_())