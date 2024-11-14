import sys
import json
import threading
import os
import speech_recognition as sr
from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
import google.generativeai as genai

# Load the API key from an environment variable or hardcoded for testing
API_KEY = 'AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA'  # Set your API key in your environment variables

def check_question_AI(question, answer, user_answer):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            f"""Giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: 
            Hãy giải bài toán: {question}. Kết quả học sinh gửi tôi là {user_answer} 
            và kết quả đúng của câu hỏi là {answer}. Bạn hãy kiểm tra nếu kết quả này là đúng hay sai. 
            Nếu đúng, không tạo câu trả lời mà chỉ in ra 'Đúng' hoặc 'Sai' và để chữ 'Sai' ở đầu câu 
            thì trả về các bước để khắc phục nhưng không được nêu ra đáp án. Bạn nhắc nhở rằng 
            bạn đang nói với học sinh của bạn bằng cách xưng em chi tiết hơn nhé và cảm xúc như thầy trò nhé.
            Vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao 
            với trường hợp đó. ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao, 
            chỉ trả về hai giá trị 'Đúng' và 'Sai' thôi không ừm gì hết. 
            Các câu trả lời đúng sai như 'CÓ' hoặc 'KHÔNG' học sinh của tôi trả lời phải hoặc đúng hoặc 2 từ đó không dấu thì nhận diện giúp tôi.""" 
        )
        
        print("API Response:", response.text)

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

    def setupUi(self, Dialog):
        try:
            Dialog.setObjectName("Dialog")
            Dialog.resize(833, 469)

            self.cauhoi = QtWidgets.QTextBrowser(Dialog)
            self.cauhoi.setGeometry(QtCore.QRect(10, 20, 571, 171))
            self.cauhoi.setStyleSheet("font: 16pt 'MS Shell Dlg 2';")
            self.cauhoi.setObjectName("cauhoi")

            self.socaudung = QtWidgets.QLCDNumber(Dialog)
            self.socaudung.setGeometry(QtCore.QRect(710, 30, 64, 23))
            self.socaudung.setStyleSheet("background-color: rgb(143, 143, 143);")
            self.socaudung.setObjectName("socaudung")

            self.label_3 = QtWidgets.QLabel(Dialog)
            self.label_3.setGeometry(QtCore.QRect(590, 60, 121, 20))
            self.label_3.setStyleSheet("background-color: rgb(255, 44, 16);\n"
                                       "font: 25 8pt 'Microsoft JhengHei UI Light';")
            self.label_3.setObjectName("label_3")

            self.socausai = QtWidgets.QLCDNumber(Dialog)
            self.socausai.setGeometry(QtCore.QRect(710, 60, 64, 23))
            self.socausai.setStyleSheet("background-color: rgb(133, 133, 133);")
            self.socausai.setObjectName("socausai")

            self.label_4 = QtWidgets.QLabel(Dialog)
            self.label_4.setGeometry(QtCore.QRect(590, 30, 121, 20))
            self.label_4.setStyleSheet("background-color: rgb(85, 255, 0);\n"
                                       "font: 25 8pt 'Microsoft JhengHei UI Light';")
            self.label_4.setObjectName("label_4")

            self.quaytrove = QtWidgets.QPushButton(Dialog)
            self.quaytrove.setGeometry(QtCore.QRect(610, 230, 221, 51))
            self.quaytrove.setObjectName("quaytrove")

            self.nhapketqua = QtWidgets.QLineEdit(Dialog)
            self.nhapketqua.setGeometry(QtCore.QRect(20, 250, 571, 161))
            self.nhapketqua.setStyleSheet("font: 26pt 'MS Shell Dlg 2';\n"
                                          "color: rgb(123, 123, 123);")
            self.nhapketqua.setObjectName("nhapketqua")

            self.checkbutton = QtWidgets.QPushButton(Dialog)
            self.checkbutton.setGeometry(QtCore.QRect(10, 410, 591, 61))
            self.checkbutton.setObjectName("checkbutton")
            self.checkbutton.setEnabled(False)  # Disable initially

            self.label_5 = QtWidgets.QLabel(Dialog)
            self.label_5.setGeometry(QtCore.QRect(590, 90, 121, 20))
            self.label_5.setStyleSheet("background-color: rgb(85, 255, 0);\n"
                                       "font: 25 8pt 'Microsoft JhengHei UI Light';")
            self.label_5.setObjectName("label_5")

            self.tongsodiem = QtWidgets.QLCDNumber(Dialog)
            self.tongsodiem.setGeometry(QtCore.QRect(710, 90, 64, 23))
            self.tongsodiem.setStyleSheet("background-color: rgb(143, 143, 143);")
            self.tongsodiem.setObjectName("tongsodiem")

            self.checkbutton.clicked.connect(self.check_answer)
            self.nhapketqua.textChanged.connect(self.on_text_changed)
            self.check_finished.connect(self.on_check_finished)
            self.quaytrove.clicked.connect(self.on_back_clicked)

            # Initialize question tracking variables
            self.cauhoi_dict = {}  # Change to a dictionary
            self.current_question = 0
            self.correct_answers = 0
            self.incorrect_answers = 0

            self.cauhoi.installEventFilter(self)
            self.nhapketqua.installEventFilter(self)
            self.checkbutton.installEventFilter(self)
            self.quaytrove.installEventFilter(self)

            threading.Thread(target=self.listen_for_voice_commands, daemon=True).start()

            self.ask_chapter()  # Ask for chapter before loading questions
            self.retranslateUi(Dialog)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        except Exception as e:
            print(f"Error in setupUi: {e}")

    def listen_for_voice_commands(self):
            command = recognize_speech()
            if command:
                if "kiểm tra" in command:
                    self.check_answer() 
                elif "quay về" in command:
                    self.on_back_clicked()  

    def fetch_chapters(self):
        chapters = []
        for folder in os.listdir("AI/question_folder"):
            if os.path.isdir(os.path.join("AI/question_folder", folder)):
                chapters.append(folder)
        return chapters

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Enter:
            if source == self.cauhoi:
                speak("Đây là ô hiển thị câu hỏi.")
            elif source == self.nhapketqua:
                speak("Đây là ô nhập câu trả lời.")
            elif source == self.checkbutton:
                speak("Nhấn để kiểm tra câu trả lời.")
            elif source == self.quaytrove:
                speak("Nhấn để quay về.")
        return super().eventFilter(source, event)

    def ask_chapter(self):
        self.chapters = self.fetch_chapters()
        if self.chapters:
            self.show_chapter_selection()
        else:
            speak("Không tìm thấy chương nào.")

    def show_chapter_selection(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Chọn chương")
        layout = QtWidgets.QVBoxLayout(dialog)

        for chapter in self.chapters:
            button = QtWidgets.QPushButton(chapter)
            button.setFixedSize(200, 50)  # Thay đổi kích thước nút
            button.setStyleSheet("font-size: 16px;")  # Thay đổi kiểu chữ

        # Kết nối nút với hành động nạp câu hỏi
            button.clicked.connect(lambda checked, c=chapter: self.load_questions(c))

        # Kết nối sự kiện di chuyển chuột
            button.enterEvent = lambda event, c=chapter: self.on_button_hover(c)

            layout.addWidget(button)

        dialog.exec_()

    def on_button_hover(self, chapter):
        speak(f"Chương {chapter}")  


    def load_questions(self, chapter):
        file_path = f"AI/question_folder/{chapter}/questions.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.cauhoi_dict = json.load(file)  # Load as dictionary
                self.current_question = 0
                self.correct_answers = 0
                self.incorrect_answers = 0
                self.show_question()
                self.checkbutton.setEnabled(True)  # Enable check button
        except FileNotFoundError:
            speak("Không tìm thấy file câu hỏi.")
        except json.JSONDecodeError:
            speak("Lỗi khi đọc file câu hỏi.")

    def show_question(self):
        if self.current_question < len(self.cauhoi_dict):
            question = list(self.cauhoi_dict.keys())[self.current_question]
            self.cauhoi.setPlainText(question)
            self.nhapketqua.clear()
        else:
            speak("Bạn đã trả lời tất cả các câu hỏi.")
            self.checkbutton.setEnabled(False)

    def check_answer(self):
        user_answer = self.nhapketqua.text().strip()
        if user_answer:
            question = list(self.cauhoi_dict.keys())[self.current_question]
            correct_answer = self.cauhoi_dict[question]
            is_correct, feedback = check_question_AI(question, correct_answer, user_answer)
            if is_correct:
                self.correct_answers += 1
                self.socaudung.display(self.correct_answers)
                speak("Đúng!")
            else:
                self.incorrect_answers += 1
                self.socausai.display(self.incorrect_answers)
                speak(feedback)

            self.tongsodiem.display(self.correct_answers - self.incorrect_answers)
            self.current_question += 1
            self.show_question()  
        else:
            speak("Xin vui lòng nhập câu trả lời.")

    def on_text_changed(self):
        if self.nhapketqua.text().strip():  
            self.checkbutton.setEnabled(True)
        else:
            self.checkbutton.setEnabled(False)

    def on_check_finished(self, is_correct, feedback):
        speak(feedback)

    def on_back_clicked(self):
        pass

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Quiz AI"))
        self.label_3.setText(_translate("Dialog", "Số câu sai:"))
        self.label_4.setText(_translate("Dialog", "Số câu đúng:"))
        self.checkbutton.setText(_translate("Dialog", "Kiểm tra câu trả lời"))
        self.label_5.setText(_translate("Dialog", "Tổng số điểm:"))
        self.quaytrove.setText(_translate("Dialog", "Quay về"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
