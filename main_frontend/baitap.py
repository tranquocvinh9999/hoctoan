import sys
import json
import threading
import os
import speech_recognition as sr
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
from functions.keyboard.keyboards import speak
import google.generativeai as genai
from functions.microphone.micro import check
from AI.bot import generate_questions_from_a_name_AI
import database.database  as db
import requests, keyboard

API_KEY = 'AIzaSyAtRaqjHzf1AgEaDK7qTC0HH62sk7Jp48Y'
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
            f"""

Giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra:

Hãy giải bài toán: "{question}". Kết quả học sinh gửi tôi là "{user_answer}" và kết quả đúng của câu hỏi là "{answer}".

Bạn hãy kiểm tra và chỉ trả về một trong hai giá trị sau:

Nếu câu trả lời của học sinh đúng: 'Đúng'.

Bao gồm trường hợp đúng nhưng sai cách trình bày hoặc chính tả.
Nếu câu trả lời sai: 'Sai'.

Kèm một giải thích ngắn gọn lý do sai và cách khắc phục, nhưng không tiết lộ đáp án.
Ngôn từ hướng đến học sinh, gần gũi và dễ hiểu.
Ví dụ: Nếu học sinh sai, nhấn mạnh cần chú ý tính toán hoặc cách trình bày cuối cùng.
Giải thích ý nghĩa của các câu trả lời không rõ ràng như 'CÓ', 'KHÔNG', hoặc 'HONG' trước khi đánh giá.
 """ 
        )

        if "Đúng" in response.text:
            return True, response.text
        elif "Sai" in response.text:
            return False, response.text
    except Exception as e:
        print(f"Error during API call: {e}")
    
    return False, "Đã xảy ra lỗi khi kiểm tra câu trả lời."
class Ui_Dialog(QtCore.QObject):
    check_finished = QtCore.pyqtSignal(bool, str)

    def load_username(self):
        with open("config/private.json") as f:
            file_data = json.load(f)
            username = file_data["username"]
        return username

    def setupUi(self, Dialog, main_dialog=None):
        self.questions = []  
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Kiểm Tra Câu Hỏi")
        Dialog.showFullScreen()
        Dialog.setStyleSheet("background-color: #f0f0f0;")
        self.username = self.load_username()
        self.mouse_filter = self.MouseEventFilter()

        self.setup_ui_elements(Dialog)
        self.setup_signals()
        self.selected_chapter = ""
        if not self.check_existing_questions():
            self.ask_chapter()
        else:
            self.show_question()

    def setup_ui_elements(self, Dialog):
        main_layout = QtWidgets.QVBoxLayout(Dialog)
        Dialog.setWindowState(QtCore.Qt.WindowFullScreen)
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    
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
        self.nhapketqua.enterEvent = lambda event: speak("Đây là phần nhập câu trả lời")  
        main_layout.addWidget(self.nhapketqua)

    # Nút kiểm tra
        self.checkbutton = QtWidgets.QPushButton("Kiểm tra", Dialog)
        self.checkbutton.setStyleSheet("font: 20pt 'MS Reference Sans Serif'; color: white; background-color: #0078D7; border-radius: 12px;")
        self.checkbutton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # Expand to fill space
        self.checkbutton.setAccessibleName("Nút Kiểm Tra Câu Trả Lời")
        self.checkbutton.setAccessibleDescription("Nhấn nút này để kiểm tra câu trả lời.")
        self.checkbutton.enterEvent = lambda event: speak("Đây là nút kiểm tra câu trả lời")
        main_layout.addWidget(self.checkbutton)

    # Nút quay lại
        self.back_button = QtWidgets.QPushButton("Quay lại", Dialog)
        self.back_button.setStyleSheet("font: 20pt 'MS Reference Sans Serif'; color: white; background-color: #D70000; border-radius: 12px;")
        self.back_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # Expand to fill space
        self.back_button.setAccessibleName("Nút Quay Lại")
        self.back_button.enterEvent = lambda event: speak("Đây là nút để quay trở về")
        self.back_button.setAccessibleDescription("Nhấn nút này để quay lại giao diện chính.")
        main_layout.addWidget(self.back_button)

    # Nút microphone
        self.micro_button = QtWidgets.QPushButton("Micro", Dialog)
        self.micro_button.setStyleSheet("font: 20pt 'MS Reference Sans Serif'; color: white; background-color: #00A300; border-radius: 12px;")
        self.micro_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # Expand to fill space
        self.micro_button.setAccessibleName("Nút Microphone")
        self.micro_button.setAccessibleDescription("Nhấn nút này để nhận diện giọng nói.")
        self.micro_button.clicked.connect(self.listen_and_check_answer)
        self.micro_button.enterEvent = lambda event: speak("Đây là nút để nói câu trả lời của bạn")
        main_layout.addWidget(self.micro_button)

        self.repeat_question_button = QtWidgets.QPushButton("Nhắc lại câu hỏi", Dialog)
        self.repeat_question_button.setStyleSheet("font: 20pt 'MS Reference Sans Serif'; color: white; background-color: #FFA500; border-radius: 12px;")
        self.repeat_question_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # Expand to fill space
        self.repeat_question_button.setAccessibleName("Nút Nhắc Lại Câu Hỏi")
        self.repeat_question_button.setAccessibleDescription("Nhấn nút này để nhắc lại câu hỏi hiện tại.")
        self.repeat_question_button.clicked.connect(self.repeat)  # Gọi hàm nhắc lại câu hỏi
        self.repeat_question_button.enterEvent = lambda event: speak("Đây là nút để nhắc lại câu hỏi")
        main_layout.addWidget(self.repeat_question_button)
        self.micro_button.enterEvent = lambda event: speak("Đây là nút để nói câu trả lời của bạn")

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
        elif key == 'space':
            self.nhapketqua.setText(self.nhapketqua.text() + " ")
        elif isinstance(key, str):
            self.nhapketqua.setText(self.nhapketqua.text() + key)
    def listen_and_check_answer(self):
        speak("xin mời bạn nói kết quả")
    
    # Lấy kết quả từ check()
        result = check()

        if result:
            self.nhapketqua.setText(result)
            self.check_answer()
        else:
            speak("Không nhận diện được câu trả lời. Vui lòng thử lại.")
    def recognize_keypress(self):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            return event.name

    def setup_virtual_keyboard(self, layout):
        keyboard_layout = QtWidgets.QGridLayout()
        keys = [
        ['7', '8', '9', 'C'],
        ['4', '5', '6', 'space'],
        ['1', '2', '3', '0', ','],
        ]

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = QtWidgets.QPushButton(key)
                button.setFixedSize(80, 80)
                button.setStyleSheet("font: 16pt 'MS Shell Dlg 2'; background-color: #E0E0E0; border: 1px solid #0078D7; border-radius: 5px;")
                button.setAccessibleName(f"Nút {key}")
                button.setAccessibleDescription(f"Nút {key} dùng để nhập số hoặc phép toán.")
                button.clicked.connect(lambda _, k=key: self.keyPressEvent(k))
            
            # Update enter event to correctly reflect the key
                if key == "C":
                    button.enterEvent = lambda event, k=key: self.handle_enter_event(event, k)
                else:
                    button.enterEvent = lambda event, k=key: self.handle_enter_event(event, k)

                keyboard_layout.addWidget(button, row, col)

        keyboard_widget = QtWidgets.QWidget()
        keyboard_widget.setLayout(keyboard_layout)
        layout.addWidget(keyboard_widget)


    def handle_enter_event(self, event, key):
        key_mapping = {
        "1": "đây là nút số 1",
        "2": "đây là nút số 2",
        "3": "đây là nút số 3",
        "4": "đây là nút số 4",
        "5": "đây là nút số 5",
        "6": "đây là nút số 6",
        "7": "đây là nút số 7",
        "8": "đây là nút số 8",
        "9": "đây là nút số 9",
        "space": "đây là nút dấu cách",
        ",": "đây là dấu phẩy"
        }

        if key in key_mapping:
            speak(key_mapping[key])
    
    def setup_signals(self):
        self.checkbutton.clicked.connect(self.check_answer)
        self.back_button.clicked.connect(self.go_back)
        self.check_finished.connect(self.on_check_finished)
        self.nhapketqua.textChanged.connect(self.on_text_changed)
        self.checkbutton.clicked.connect(lambda: self.speak_button_function("Kiểm tra câu trả lời."))
        self.back_button.clicked.connect(lambda: self.speak_button_function("Quay lại giao diện chính."))

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
                print(f"existing current question: {self.current_question}")
                speak(f"Tìm thấy bài tập đang làm trong bài {self.selected_chapter}. Tiếp tục từ câu hỏi số {self.current_question + 1}.")
                self.load_questions(data["question"])
                return True
        return False



    def fetch_chapters(self):
        return db.get_all_chapter()

    def add_new_question(self):
        speak("Xin hãy đọc tên bài tập mới.")
        new_question_name = check()

        if new_question_name:
            speak(f"Bạn đã chọn bài tập mới: {new_question_name}")
            self.selected_chapter = new_question_name
            self.ask_difficulty()
            
            self.load_questions()
        else:
            speak("Không thể nhận diện tên bài tập. Vui lòng thử lại.")


    def handle_add_new_question(self):
        self.add_new_question()
        if hasattr(self, 'chapter_menu_dialog') and self.chapter_menu_dialog.isVisible():
            self.chapter_menu_dialog.close()  

    def ask_chapter(self):
        self.chapter_menu_dialog = QtWidgets.QDialog()
        self.chapter_menu_dialog.setWindowTitle("Chọn Bài Tập")
        self.chapter_menu_dialog.setStyleSheet("background-color: #f0f0f0;")
        self.chapter_menu_dialog.showMaximized()
        self.chapter_menu_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        layout = QtWidgets.QVBoxLayout(self.chapter_menu_dialog)
        speak(f"Nếu bạn muốn lựa chọn thì hãy điều khiển và nhấn vào để chọn bài tập")
        chapters = self.fetch_chapters()
        if chapters:
            speak("Chọn bài bạn muốn kiểm tra.")
            speak(f"Ở đây có các bài tập như là")
            chapters_layout = QtWidgets.QGridLayout()  
            for index, chapter in enumerate(chapters):
                speak(f" {chapter}")
            

                chapter_button = QtWidgets.QPushButton(f"Bài tập: {chapter}", self.chapter_menu_dialog)
                chapter_button.setAccessibleName(f"Nút chọn Bài {chapter}")
                chapter_button.enterEvent = lambda event, ch=chapter: speak(f"Đây là bài {ch}")
                chapter_button.setStyleSheet(
                "font: 24pt 'MS Shell Dlg 2'; background-color: #0078D7; color: white; "
                "border-radius: 10px; padding: 20px; margin: 5px;")
                chapter_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                chapter_button.clicked.connect(lambda _, ch=chapter: self.on_chapter_button_clicked(ch))


                row, col = divmod(index, 3)  # Mỗi hàng có tối đa 3 nút
                chapters_layout.addWidget(chapter_button, row, col)

            layout.addLayout(chapters_layout)

        layout.addStretch()

        buttons_layout = QtWidgets.QHBoxLayout()
        add_new_question_button = QtWidgets.QPushButton("Thêm bài tập mới", self.chapter_menu_dialog)
        add_new_question_button.setAccessibleName("Nút thêm bài tập mới")
        add_new_question_button.enterEvent = lambda event: speak("bấm vào đây để thêm bài tập mới")  
        add_new_question_button.setStyleSheet(
        "font: 18pt 'MS Shell Dlg 2'; background-color: #00A300; color: white; "
        "border-radius: 10px; padding: 10px; margin: 5px;")
        add_new_question_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        add_new_question_button.clicked.connect(self.handle_add_new_question)
        buttons_layout.addWidget(add_new_question_button)

        close_button = QtWidgets.QPushButton("Đóng", self.chapter_menu_dialog)
        close_button.enterEvent = lambda event: speak("Bấm vào đây để vào phần kiểm tra bài tập và bấm nút quay trở về ở giao diện kiểm tra")  
        close_button.setStyleSheet(
        "font: 18pt 'MS Shell Dlg 2'; background-color: #D70000; color: white; "
        "border-radius: 10px; padding: 10px; margin: 5px;")
        close_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        close_button.clicked.connect(self.chapter_menu_dialog.close)
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        self.chapter_menu_dialog.exec_()


    def on_chapter_button_clicked(self, chapter_name):
        self.selected_chapter = chapter_name
        speak(f"Bạn đã chọn bài: {self.selected_chapter}")
        self.chapter_menu_dialog.close()
        self.ask_difficulty()  

    def ask_difficulty(self):
        self.difficulty_menu_dialog = QtWidgets.QDialog()
        self.difficulty_menu_dialog.setWindowTitle("Chọn Mức Độ")
        self.difficulty_menu_dialog.setStyleSheet("background-color: #f0f0f0;")
        self.difficulty_menu_dialog.showMaximized()
        self.difficulty_menu_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        layout = QtWidgets.QVBoxLayout(self.difficulty_menu_dialog)
        speak("Chọn mức độ bạn muốn kiểm tra. Có các mức độ Dễ Trung bình Khó và Tổng hợp.")
        db.reset_practice_chapter(self.selected_chapter)
        difficulties = ["Dễ", "Trung bình", "Khó", "Tổng hợp"]
        button_width = 400  # Chiều rộng cố định cho nút lớn hơn
        button_height = 120  # Chiều cao cố định cho nút lớn hơn

        for difficulty in difficulties:
            difficulty_button = QtWidgets.QPushButton(f"Mức độ: {difficulty}", self.difficulty_menu_dialog)
            difficulty_button.setAccessibleName(f"Nút chọn mức độ {difficulty}")
            difficulty_button.enterEvent = lambda event, diff=difficulty: speak(f"Đây là mức độ {diff}")
            difficulty_button.setStyleSheet(
            "font: bold 36pt 'MS Shell Dlg 2'; background-color: #0078D7; color: white; "
            "border-radius: 20px; padding: 20px; margin: 10px;")
            difficulty_button.setFixedSize(button_width, button_height)  # Đặt kích thước cố định lớn hơn
            difficulty_button.clicked.connect(lambda _, diff=difficulty: self.on_difficulty_selected(diff))
            layout.addWidget(difficulty_button)

        layout.addStretch()
        self.difficulty_menu_dialog.exec_()


    def on_difficulty_selected(self, difficulty):
        self.selected_difficulty = difficulty
        speak(f"Bạn đã chọn mức độ: {self.selected_difficulty}")
        generate_questions_from_a_name_AI(self.selected_chapter, 10, self.selected_difficulty)
        self.difficulty_menu_dialog.close()
        self.load_questions()
    def load_questions(self, current_question_text=None):
        try:
            # # Đường dẫn tới file câu hỏi
            # question_file = f"AI/question_folder/{self.selected_chapter}/questions.json"

            # # Mở và đọc file câu hỏi
            # with open(question_file, "r", encoding="utf-8") as f:
            
            # Khởi tạo danh sách câu hỏi
            self.questions = db.get_all_questions_by_chapter(self.selected_chapter)
            self.current_question = 0
            self.correct_answers = 0
            self.incorrect_answers = 0

            # Nếu có chỉ định câu hỏi hiện tại, tìm kiếm câu hỏi đó
            print(f"Questions: {self.questions}")
            if current_question_text:
                for idx, question in enumerate(self.questions):
                    if question.get("question") == current_question_text:  # Kiểm tra khóa "question"
                        self.current_question = idx
                        print(f"index: {idx}")
                        print(f"current questions: {self.current_question}")
                        break

            # Hiển thị câu hỏi và kích hoạt button
            self.show_question()
            self.checkbutton.setEnabled(True)

        except FileNotFoundError:
            speak("Không tìm thấy danh sách câu hỏi của bài tập này.")
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
        components = re.findall(r'[\d\-]+|[\+\-\*/]|[a-zA-Zàáạảãâầấậẩẫăằắặẳẵêềếệểễíìíịỉĩóòóọỏõôồốộốổỗơờớợởỡùủũúụưừứựửữýỳýỵỷỹđ]+', question)
    
    # Chuyển đổi các toán tử thành từ tương ứng
        operators = {'+': 'cộng', '-': 'trừ', '*': 'nhân', '/': 'chia'}
    
        spoken_question = ""

        for i in range(len(components)):
            comp = components[i]
        
        # Xử lý số âm
            if comp.startswith('-') and (i == 0 or components[i-1] not in operators):
                if i < len(components) - 1 and components[i+1].startswith('-'):
                    spoken_question += f"âm {comp[1:]} trừ cho "
                else:
                    spoken_question += f"âm {comp[1:]} "
            elif comp in operators:
                spoken_question += f"{operators[comp]} "
            else:
                spoken_question += f"{comp} "
    
        return spoken_question.strip()

    def show_question(self):
        if self.current_question >= len(self.questions):
            speak("Bạn đã hoàn thành chương này. Chúc mừng!")
            speak(f"Bạn đúng {self.correct_answers} và sai {self.incorrect_answers}")
            self.submit_scores()
            self.cauhoi.setText("Bạn đã hoàn thành tất cả câu hỏi.")
            # self.show_result_screen(7, 3, len(self.questions))
            return

    # Lấy câu hỏi hiện tại
        question_data = self.questions[self.current_question]
        question_text = question_data["question"]
        self.cauhoi.setText(question_text)

        question_text_cleaned = question_text.strip().replace('=', '').replace('?', '').replace(' ', '')
        print(question_text_cleaned)
        self.cauhoi.setAccessibleDescription(question_text)

        spoken_question = self.format_question_to_speech(question_text)  # In ra câu hỏi để kiểm tra
        speak(f"Câu hỏi số {self.current_question+1} là: {spoken_question}")


    def repeat(self):
        question_text = self.cauhoi.toPlainText()
        if question_text:
            speak(f"Câu hỏi là: {question_text}")
    def check_answer(self):
        self.checkbutton.setDisabled(True)
        speak("bạn đã nhấn kiểm tra câu trả lời hãy chờ nhé")
        user_answer = self.nhapketqua.text().strip() 
        #correct_answer = self.cauhoi_dict[self.current_question]["answer"].strip() 
        correct_answer = self.questions[self.current_question]["answer"].strip()
        if user_answer.lower() in ["có", "yes", "y", "phai", "dung", "co"]:
            user_answer = "phải"
        elif user_answer.lower() in ["không", "no", "n", "khong", "sai"]:
            user_answer = "không"
        elif user_answer.lower() in ["lon hon", "lớn hơn"]:
            user_answer = user_answer.replace("lon hon", ">")
        elif user_answer.lower() in ["be hon", "bé hơn"]:
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
        self.show_question()  
        self.current_question += 1
        self.save_current_state()
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

        if(self.current_question >= len(self.questions)):
            speak("Bạn đã hoàn thành bài tập này")
            # self.show_result_screen(7, 3, len(self.questions))
            return
        # print(f"questions: {self.questions}")
        # print(f"current questinos: {self.current_question}")

        if db.update_current_exercise_by_username(
            username, 
            self.questions[self.current_question]["question"],
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
            db.reset_practice_chapter(self.selected_chapter)
            # self.show_result_screen(7, 3, len(self.questions))
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
        print(self.correct_answers)
        print(self.incorrect_answers)
        a = self.correct_answers 
        b = self.incorrect_answers 
        c = a - b  

        new_correct = int(data["user_correct"]) + a
        new_wrong = int(data["user_fail"]) + b
        new_score = int(data["user_score"]) + len(self.questions)

        db.submit_scores(username, new_correct, new_score, new_wrong)

    def go_back(self):
        speak("Bạn đã quay về menu chính")

    def clear_baitapdangdo_file(self):
        username = self.get_username()

        db.remove_current_exercise_by_username(username)
        speak("Dữ liệu trong bài tập dang dở đã được xóa")
 
