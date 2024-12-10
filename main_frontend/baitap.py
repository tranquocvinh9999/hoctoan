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
import database.database  as db
import requests

API_KEY = 'AIzaSyAxoki6CsXdtMdWuSEwyXQ4tUGDNOLCIGA'
import re
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
            Các câu trả lời đúng sai như 'CÓ' hoặc 'KHÔNG' học sinh của tôi trả lời phải hoặc đúng hoặc 2 từ đó không dấu thì nhận diện giúp tôi.HOẶC 'PHẢI' HOẶC 'KHÔNG' MÀ HỌC SINH TÔI TRẢ LỜI 'PHAI' hoặc 'phai' HOẶC 'KHONG' HOẶC 'HONG' thì cũng tính nhé. VÀ HÃY KIỂM TRA KẾT QUẢ CỦA HỌC SINH TÔI NHẬP VỚI KẾT QUẢ ĐÚNG VÌ CÓ MẤY LẦN HỌC SINH TÔI NHẬP ĐÚNG VỚI KẾT QUẢ ĐÚNG THÌ BẠN LẠI BẢO SAI
            VÍ DỤ CÁC CÂU CÓ DẤU PHẨY (LIỆT KÊ) NHƯ 5, 3, 2, 1 MÀ HỌC SINH TÔI TRẢ LỜI LÀ 5 3 2 1 THÌ BẠN HÃY CHO LÀ ĐÚNG NHÉ VÌ HỌC SINH TÔI CÓ THỂ KHÔNG BIẾT DẤU PHẨY Ở ĐÂU MÀ CHỈ BIẾT DẤU CÁCH THÔI
            """ 
        )

        if "Đúng" in response.text:
            return True, response.text
        elif "Sai" in response.text:
            return False, response.text
    except Exception as e:
        print(f"Error during API call: {e}")
    
    return False, "Đã xảy ra lỗi khi kiểm tra câu trả lời."

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
    # def __init__(self):   

    def load_username(self):
        with open("config/private.json") as f:
            file_data = json.load(f)
            username = file_data["username"]
        return username

    def setupUi(self, Dialog, main_dialog=None):
        self.questions = []  # Initialize questions as an empty list
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Kiểm Tra Câu Hỏi")
        Dialog.showFullScreen()
        Dialog.setStyleSheet("background-color: #f0f0f0;")
        self.username = self.load_username()
        self.mouse_filter = self.MouseEventFilter()

        self.setup_ui_elements(Dialog)
        self.setup_signals()

        if not self.check_existing_questions():
            self.ask_chapter()
        else:
            self.show_question()

    def setup_ui_elements(self, Dialog):
        main_layout = QtWidgets.QVBoxLayout(Dialog)
        Dialog.setWindowState(QtCore.Qt.WindowFullScreen)  # Fullscreen mode
        Dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        # Khu vực câu hỏi
        self.cauhoi = QtWidgets.QTextBrowser(Dialog)
        self.cauhoi.setStyleSheet("font: 16pt 'MS Shell Dlg 2'; border: 2px solid #0078D7; border-radius: 8px;")
        self.cauhoi.setAccessibleName("Khu vực hiển thị câu hỏi")
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
        self.nhapketqua.setAccessibleName("Ô nhập kết quả")
        main_layout.addWidget(self.nhapketqua)

        # Nút kiểm tra
        self.checkbutton = QtWidgets.QPushButton("Kiểm tra", Dialog)
        self.checkbutton.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #0078D7; border-radius: 10px;")
        self.checkbutton.setAccessibleName("Nút Kiểm Tra Câu Trả Lời")
        self.checkbutton.setAccessibleDescription("Nhấn nút này để kiểm tra câu trả lời.")
        self.checkbutton.installEventFilter(self.mouse_filter)
        main_layout.addWidget(self.checkbutton)

        # Nút quay lại
        self.back_button = QtWidgets.QPushButton("Quay lại", Dialog)
        self.back_button.setStyleSheet("font: 14pt 'MS Reference Sans Serif'; color: white; background-color: #D70000; border-radius: 10px;")
        self.back_button.setAccessibleName("Nút Quay Lại")
        self.back_button.setAccessibleDescription("Nhấn nút này để quay lại chương trước.")
        main_layout.addWidget(self.back_button)

        # Bàn phím ảo
        self.setup_virtual_keyboard(main_layout)

    class MouseEventFilter(QtCore.QObject):
        def eventFilter(self, source, event):
            if event.type() == QtCore.QEvent.Enter and isinstance(source, QtWidgets.QPushButton):
                text = source.text()
                if text == 'C': 
                    speak("Đây là nút xóa kí tự")  
                elif text == "-":
                    speak("đây là dấu âm")
                else:
                    speak(f"Nút: {text}") 
            return super().eventFilter(source, event)
    def keyPressEvent(self, key):
        print(f"Key pressed: {key}") 
        if key == 'C':
            self.nhapketqua.clear()
        elif key == '<':
            self.nhapketqua.setText(self.nhapketqua.text()[:-1])
        elif isinstance(key, str):
            self.nhapketqua.setText(self.nhapketqua.text() + key)

    def setup_virtual_keyboard(self, layout):
        keyboard_layout = QtWidgets.QGridLayout()
        keys = [
        ['7', '8', '9', 'C'],
        ['4', '5', '6', '<'],
        ['1', '2', '3', '0'],
        ['+', '-', '*', '/'],
        ]

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = QtWidgets.QPushButton(key)
                button.setFixedSize(60, 60)
                button.setStyleSheet("font: 16pt 'MS Shell Dlg 2'; background-color: #E0E0E0; border: 1px solid #0078D7; border-radius: 5px;")
                button.setAccessibleName(f"Nút {key}")
                button.setAccessibleDescription(f"Nút {key} dùng để nhập số hoặc phép toán.")
                button.clicked.connect(lambda _, k=key: self.keyPressEvent(k))
                keyboard_layout.addWidget(button, row, col)

        keyboard_widget = QtWidgets.QWidget()
        keyboard_widget.setLayout(keyboard_layout)
        layout.addWidget(keyboard_widget)
    
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

    def check_existing_questions(self):

        username = self.get_username()

        data = db.get_current_exercise_by_username(username)
        
        if data is not None:
            if "question" in data and data["question"]:
                self.selected_chapter = data["chapter"]
                self.correct_answers = data["correct"]
                self.incorrect_answers = data["wrong"]
                self.current_question = data["current"]
                self.questions = data["question"]
                self.socasai.display(self.incorrect_answers)
                self.socaudung.display(self.correct_answers)
                speak(f"Tìm thấy bài tập đang làm trong chương {self.selected_chapter}. Tiếp tục từ câu hỏi số {self.current_question + 1}.")
                self.load_questions(data["question"])
                return True
        return False



    def fetch_chapters(self):
        return db.get_all_chapter()

    def add_new_question(self):
        speak("Xin hãy đọc tên bài tập mới.")
        new_question_name = recognize_speech()

        if new_question_name:
            speak(f"Bạn đã chọn bài tập mới: {new_question_name}")

            self.selected_chapter = new_question_name
            generate_questions_from_a_name_AI(self.selected_chapter, 3)
            db.reset_pratice_chapter(self.selected_chapter)
            self.load_questions()
        else:
            speak("Không thể nhận diện tên bài tập. Vui lòng thử lại.")

    def ask_chapter(self):
        self.chapter_menu_dialog = QtWidgets.QDialog()
        self.chapter_menu_dialog.setWindowTitle("Chọn Chương")
        self.chapter_menu_dialog.setStyleSheet("background-color: #f0f0f0;")


        self.chapter_menu_dialog.showMaximized()


        self.chapter_menu_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        layout = QtWidgets.QVBoxLayout(self.chapter_menu_dialog)

    
        chapters = self.fetch_chapters()
        if chapters:
            speak("Chọn chương bạn muốn kiểm tra.")

            chapters_layout = QtWidgets.QVBoxLayout()
            for chapter in chapters:
                chapter_button = QtWidgets.QPushButton(f"Chương: {chapter}", self.chapter_menu_dialog)
                chapter_button.setAccessibleName(f"Nút chọn chương {chapter}")
                chapter_button.setStyleSheet(
                "font: 18pt 'MS Shell Dlg 2'; background-color: #0078D7; color: white; "
                "border-radius: 10px; padding: 10px; margin: 5px;")
                chapter_button.clicked.connect(lambda _, ch=chapter: self.on_chapter_button_clicked(ch))
                chapters_layout.addWidget(chapter_button)
            layout.addLayout(chapters_layout)
        layout.addStretch()

        buttons_layout = QtWidgets.QHBoxLayout()
        add_new_question_button = QtWidgets.QPushButton("Thêm bài tập mới", self.chapter_menu_dialog)
        add_new_question_button.setAccessibleName("Nút thêm bài tập mới")
        add_new_question_button.setStyleSheet(
        "font: 18pt 'MS Shell Dlg 2'; background-color: #00A300; color: white; "
        "border-radius: 10px; padding: 10px; margin: 5px;")
        add_new_question_button.clicked.connect(self.add_new_question)
        buttons_layout.addWidget(add_new_question_button)

        close_button = QtWidgets.QPushButton("Đóng", self.chapter_menu_dialog)
        close_button.setStyleSheet(
        "font: 18pt 'MS Shell Dlg 2'; background-color: #D70000; color: white; "
        "border-radius: 10px; padding: 10px; margin: 5px;")
        close_button.clicked.connect(self.chapter_menu_dialog.close)
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        self.chapter_menu_dialog.exec_()

    def on_chapter_button_clicked(self, chapter_name):

        self.selected_chapter = chapter_name
        speak(f"Bạn đã chọn chương: {self.selected_chapter}")
        self.chapter_menu_dialog.close() 
        generate_questions_from_a_name_AI(self.selected_chapter, 3)
        db.reset_pratice_chapter(self.selected_chapter)
        self.load_questions()

    def load_questions(self, current_question_text=None):
        try:
            # # Đường dẫn tới file câu hỏi
            # question_file = f"AI/question_folder/{self.selected_chapter}/questions.json"

            # # Mở và đọc file câu hỏi
            # with open(question_file, "r", encoding="utf-8") as f:
            #     self.cauhoi_dict = json.load(f)
            
            # Khởi tạo danh sách câu hỏi
            self.questions = db.get_all_questions_by_chapter(self.selected_chapter)
            self.current_question = 0
            self.correct_answers = 0
            self.incorrect_answers = 0

            # Nếu có chỉ định câu hỏi hiện tại, tìm kiếm câu hỏi đó
            if current_question_text:
                for idx, question in enumerate(self.cauhoi_dict):
                    if question.get("question") == current_question_text:  # Kiểm tra khóa "question"
                        self.current_question = idx
                        break
                else:
                    # Nếu không tìm thấy câu hỏi tương ứng
                    speak(f"Câu hỏi '{current_question_text}' không được tìm thấy.")
                    return  # Dừng hàm nếu không tìm thấy câu hỏi

            # Hiển thị câu hỏi và kích hoạt button
            self.show_question()
            self.checkbutton.setEnabled(True)

        except FileNotFoundError:
            speak("Không tìm thấy danh sách câu hỏi của chương này.")
        except json.JSONDecodeError:
            speak("Có lỗi xảy ra khi đọc danh sách câu hỏi.")
        except Exception as e:
            print(e)

    def on_text_changed(self):
        if self.nhapketqua.text():
            last_char = self.nhapketqua.text()[-1] 
            if last_char == " ":
                speak("dấu cách")
            else:
                speak(f"{last_char}")

    def format_question_to_speech(self, question):
        # Loại bỏ các ký tự không cần thiết và giữ nguyên dấu
        question = question.strip()
        question = question.replace('=', '').replace('?', '').strip()
    
        # Tách các thành phần của câu hỏi: số, toán tử và từ chữ
        components = re.findall(r'[\d\-]+|[\+\-\*/]|[a-zA-Zàáạảãâầấậẩẫăằắặẳẵêềếệểễíìíịỉĩóòóọỏõôồốộổỗơờớợởỡùủũúụưừứựửữýỳýỵỷỹđ]+', question)
    
        # Chuyển đổi các toán tử thành từ tương ứng
        operators = {'+': 'cộng', '-': 'trừ', '*': 'nhân', '/': 'chia'}
        
        # Xử lý các số âm
        for i in range(len(components)):
            #If i is not the last element
            if i < len(components) - 1:
                if (components[i].startswith('-') and components[i + 1] not in operators) :
                    components[i] = f"âm {components[i][1:]}"  # Đọc số âm

        spoken_question = ""
    
        for comp in components:
            if comp in operators:
                spoken_question += f"{operators[comp]} "
            else:
                spoken_question += f"{comp} "

        return spoken_question.strip()

    def show_question(self):
        # Kiểm tra nếu không còn câu hỏi nào
        if self.current_question >= len(self.questions):
            speak("Bạn đã hoàn thành chương này. Chúc mừng!")
            self.submit_scores()
            self.cauhoi.setText("Bạn đã hoàn thành tất cả câu hỏi.")
            return

        # Lấy câu hỏi hiện tại
        question_data = self.questions[self.current_question]
        question_text = question_data["question"]
        self.cauhoi.setText(question_text)

        # Xử lý và làm sạch câu hỏi để đọc
        question_text_cleaned = question_text.strip().replace('=', '').replace('?', '').replace(' ', '')
        print(question_text_cleaned)
        self.cauhoi.setAccessibleDescription(question_text)

        spoken_question = self.format_question_to_speech(question_text)
        print(f"Đọc câu hỏi: {spoken_question}")  # In ra câu hỏi để kiểm tra
        speak(f"Câu hỏi là: {spoken_question}")

    def check_answer(self):
        self.checkbutton.setDisabled(True)
        speak("bạn đã nhấn kiểm tra câu trả lời hãy chờ nhé")
        user_answer = self.nhapketqua.text().strip() 
        # correct_answer = self.cauhoi_dict[self.current_question]["answer"].strip() 
        correct_answer = self.questions[self.current_question]["answer"].strip()
        if correct_answer.lower() in ["có", "yes", "y", "phai", "dung"]:
            user_answer = "phải"
        elif correct_answer.lower() in ["không", "no", "n", "khong", "sai"]:
            user_answer = "không"
        elif correct_answer.lower() in ["lon hon", "lớn hơn"]:
            user_answer = user_answer.replace("lon hon", ">")
        elif correct_answer.lower() in ["be hon", "bé hơn"]:
            user_answer =  user_answer.replace("be hon", "<")

        is_correct, feedback = check_question_AI(self.questions[self.current_question], correct_answer, user_answer)

        if is_correct:
            self.correct_answers += 1
            self.socaudung.display(self.correct_answers)
            self.nhapketqua.clear()
            speak(feedback)
        else:
            self.incorrect_answers += 1
            self.socasai.display(self.incorrect_answers)
            self.nhapketqua.clear()
            speak(feedback)
        
        self.nhapketqua.clear()
        self.checkbutton.setDisabled(False)
        self.current_question += 1  
        self.save_current_state()  
        self.show_question()  

        print(user_answer)  
        print(correct_answer)  
        self.check_finished.emit(is_correct, feedback) 

    def get_username(self):
        with open("config/private.json") as f:
            file_data = json.load(f)
            username = file_data["username"]
        return username
        
    def save_current_state(self):
        username = self.get_username()

        if db.update_current_exercise_by_username(
            username, 
            self.cauhoi_dict[self.current_question]["question"],
            self.correct_answers,
            self.incorrect_answers,
            self.current_question,
            self.selected_chapter
        ) != 200:
            print("Lỗi khi lưu trạng thái:")

    def on_check_finished(self, valid, feedback):
        if valid:
            self.socaudung.display(self.correct_answers)
        else:
            self.socasai.display(self.incorrect_answers)
        self.checkbutton.setDisabled(False)

        if self.current_question < len(self.questions):
            self.show_question()
        else:
            speak("Bạn đã hoàn thành bài tập.")
            self.submit_scores()
            self.reset_quiz()

    def reset_baitapdangdo(self):  
        db.reset_current_exercise_by_username(self.get_username())

    def reset_quiz(self):
        self.reset_baitapdangdo()
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.current_question = 0
        self.back_button.click()

    def submit_scores(self): 
        username = self.get_username()
        data = db.get_scores(username)

        a = self.correct_answers 
        b = self.incorrect_answers 
        c = a - b  

        new_correct = data["user_correct"] + a
        new_wrong = data["user_fail"] + b
        new_score = data["user_score"] + 3  

        db.submit_scores(new_score, new_correct, new_wrong, username)

    def go_back(self):
        speak("Quay lại.")
    def clear_baitapdangdo_file():
        username = self.get_username()

        db.remove_current_exercise_by_username(username)
        speak("Dữ liệu trong bài tập dang dở đã được xóa")
 
    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.cauhoi_dict):
            self.show_question()
        else:
            speak("Bạn đã hoàn thành tất cả các câu hỏi.")
            self.submit_scores()  
            self.clear_baitapdangdo_file() 
            self.back_button.click()

# fix phần đọc dấu
