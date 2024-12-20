import os
import requests
from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
from functions.keyboard.keyboards import stop_speech
from functions.microphone.micro import check
import json
from functions.resource_path.path import resource_path
from PyQt5.QtCore import Qt
import keyboard, threading
import database.database as db
import google.generativeai as genai
from PyQt5.QtCore import QTimer

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = True

    def run(self):
        try:
            while self._is_running:
                lecture_name = check()
                self.recognized_text.emit(lecture_name if lecture_name else "")
        except Exception as e:
            print("Lỗi trong VoiceRecognitionThread:", e)

    def stop(self):
        self._is_running = False

API_KEY = 'AIzaSyAtRaqjHzf1AgEaDK7qTC0HH62sk7Jp48Y'


def generate_lectures(lectures):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""
        Bạn là giáo viên dạy toán. Hãy tạo bài giảng {lectures} đầy đủ, dễ hiểu và chỉ tập trung vào phần lý thuyết. 
        Không sử dụng ký tự đặc biệt, định dạng phức tạp, hoặc chữ in hoa. Thay các ký hiệu toán học như giá trị tuyệt đối, dấu thuộc, bằng 
        diễn giải ý nghĩa và hướng dẫn cách viết chúng sao cho đơn giản, phù hợp với học sinh khiếm thị. 
        Loại bỏ phần bài tập và ví dụ. Giữ nội dung ngắn gọn, dễ tiếp cận nhất.
        """
    )
    return response.text


class KeyPressListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                print(event.name)
                self.callback(event.name)

    def stop(self):
        self.stop_flag = True


class Ui_Dialog(object):
    def setupUi(self, dialog, main_menu):
        self.current_lecture = None
        self.dialog = dialog
        self.main_menu = main_menu
        dialog.setObjectName("Dialog")
    
        dialog.keyPressEvent = self.handle_key_press
        dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        dialog.setStyleSheet("""background-color: white; color: black; font: 16pt 'Arial';""")

        # QTextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet("""font: 18pt 'MS Reference Sans Serif';
                                       color: black;
                                       background-color: white;
                                       border-radius: 15px;
                                       border: 3px solid #0078D7;
                                       padding: 20px;""")
        self.textBrowser.setAlignment(Qt.AlignLeft)
        self.textBrowser.setGeometry(QtCore.QRect(20, 100, 500, 350))
        self.textBrowser.setPlainText("Chào bạn! Hãy chọn bài học lý thuyết từ dưới đây.")

        # Back Button
        self.back_button = QtWidgets.QPushButton(dialog)
        self.back_button.setGeometry(QtCore.QRect(20, 470, 500, 100))
        self.back_button.setText("Quay lại")
        self.back_button.setStyleSheet("""font: 24pt 'MS Reference Sans Serif'; 
                                      color: white;
                                      background-color: #ff4d4d;
                                      border-radius: 15px;
                                      border: 3px solid #1a75ff;""")
        self.back_button.setAccessibleName("Nút quay lại")
        self.back_button.setAccessibleDescription("Bấm để trở lại giao diện cũ")
        self.back_button.enterEvent =  lambda event: speak("đây là nút quay lại giao diện chính")
        self.back_button.clicked.connect(lambda: self.return_to_main_menu(self.dialog))

        # Microphone Button
        self.microphone_button = QtWidgets.QPushButton(dialog)
        self.microphone_button.setGeometry(QtCore.QRect(20, 580, 500, 100))  
        self.microphone_button.setText("🎤 Nói")
        self.microphone_button.setStyleSheet("""font: 24pt 'MS Reference Sans Serif'; 
                                            color: white;
                                            background-color: #00cc66;
                                            border-radius: 15px;
                                            padding: 10px;
                                            margin: 5px;""")
        self.microphone_button.setAccessibleName("Nút micro")
        self.microphone_button.setAccessibleDescription("Bấm vào để nói tên bài giảng")
        self.microphone_button.enterEvent = lambda event: speak("đây là nút để nói tên bài giảng hoặc nói quay lại")
        self.microphone_button.clicked.connect(self.start_voice_recognition)

        self.relisten_button = QtWidgets.QPushButton(dialog)
        self.relisten_button.setGeometry(QtCore.QRect(20, 690, 240, 100))  # Đặt vị trí dưới nút micro
        self.relisten_button.setText("🔄 Nghe lại")
        self.relisten_button.setStyleSheet("""font: 24pt 'MS Reference Sans Serif'; 
                                      color: white;
                                      background-color: #FF9900;
                                      border-radius: 15px;
                                      padding: 10px;
                                      margin: 5px;""")
        self.relisten_button.setAccessibleName("Nút nghe lại")
        self.relisten_button.enterEvent = lambda event: speak("đây là nút để nghe lại bài giảng")
        self.relisten_button.setAccessibleDescription("Bấm để nghe lại bài giảng hiện tại")
        self.relisten_button.clicked.connect(self.relisten2)

# Nghe bài khác Button
        self.other_lecture_button = QtWidgets.QPushButton(dialog)
        self.other_lecture_button.setGeometry(QtCore.QRect(280, 690, 240, 100))  # Đặt vị trí dưới nút micro, cạnh nút Nghe lại
        self.other_lecture_button.setText("➡️ Nghe bài khác")
        self.other_lecture_button.setStyleSheet("""font: 24pt 'MS Reference Sans Serif'; 
                                           color: white;
                                           background-color: #0099CC;
                                           border-radius: 15px;
                                           padding: 10px;
                                           margin: 5px;""")
        self.other_lecture_button.setAccessibleName("Nút nghe bài khác")
        self.other_lecture_button.enterEvent = lambda event: speak("đây là nút để chọn bài giảng khác")
        self.other_lecture_button.setAccessibleDescription("Bấm để nghe bài giảng khác")
        self.other_lecture_button.clicked.connect(self.load_available_lectures)
        
# Hiển thị các nút
        self.relisten_button.show()
        self.other_lecture_button.show()
        # Layout to hold buttons
        self.chapter_layout = QtWidgets.QVBoxLayout()
        self.chapter_layout.setContentsMargins(20, 20, 20, 20)
        self.chapter_layout.setSpacing(30)

        chapter_widget = QtWidgets.QWidget(dialog)
        chapter_widget.setLayout(self.chapter_layout)
        chapter_widget.setGeometry(QtCore.QRect(540, 100, 500, 600))


        self.back_button.show()
        self.microphone_button.show() 
        self.load_available_lectures()
        # Delay the speech using QTimer to ensure UI is rendered before speech
        QtCore.QTimer.singleShot(500, lambda: speak("Menu chính đã hiện lên"))  # Delay speech by 500ms

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.showFullScreen()


    def load_available_lectures(self):

        lectures = db.find_all_lecture()
        QTimer.singleShot(1000, lambda: speak("Chào bạn đã tới phần lý thuyết. Hãy bấm nút micro và nói quay lại để quay lại giao diện chính hoặc cũng có thể nói chương bài lý thuyết bạn muốn nghe hoặc nếu bạn không muốn nghe thì nói quay lại nhé. Ở đây đã có các bài lý thuyết như"))
        op = []
        self.chapter_layout = QtWidgets.QGridLayout()  # Dùng GridLayout thay vì VBoxLayout
        self.chapter_layout.setContentsMargins(20, 20, 20, 20)
        self.chapter_layout.setSpacing(30)

        # Tạo widget chứa layout và gắn layout vào
        chapter_widget = QtWidgets.QWidget(self.dialog)
        chapter_widget.setLayout(self.chapter_layout)
        chapter_widget.setGeometry(QtCore.QRect(540, 100, 700, 600))

        row, col = 0, 0  # Bắt đầu từ hàng 0, cột 0
        max_columns = 3  # Số cột tối đa

        for lecture in lectures:
            lecture_name = lecture['name']
            op.append(lecture_name)
            speak(lecture_name)
            button = QtWidgets.QPushButton(lecture_name)
            button.setStyleSheet("""font: bold 28pt 'MS Reference Sans Serif'; 
                                    color: white;
                                    background-color: #0078D7;
                                    border-radius: 20px;
                                    padding: 20px 40px;  
                                    border: 2px solid #0056A8;  
                                    text-align: center; 
                                """)
            button.setAccessibleName(f"Đây là nút {lecture_name}")
            button.setAccessibleDescription(f"Nhấn vào để mở bài giảng {lecture_name}")
            button.enterEvent = self.create_enter_event_handler(lecture_name)
            button.clicked.connect(lambda _, name=lecture_name: self.load_lecture_text(name))

            # Thêm nút vào GridLayout tại vị trí hàng và cột
            self.chapter_layout.addWidget(button, row, col)

            # Tăng cột, nếu đạt số cột tối đa thì chuyển sang hàng mới
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def start_voice_recognition(self):
        speak("Hãy nói chương bạn muốn từ các chương giáo viên đã tải lên trước")
        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(self.on_lecture_name_recognized)
        self.voice_thread.start()

    def on_lecture_name_recognized(self, recognized_text):
        """Handles the recognized lecture name."""
        if recognized_text:
            speak(f"Bạn đã chọn bài giảng {recognized_text}.")
            self.load_lecture_text(recognized_text)
        else:
            speak("Không nhận diện được tên bài giảng. Hãy thử lại.")
            self.start_voice_recognition()


    def create_enter_event_handler(self, lecture_name):
        def handler(event):
            QTimer.singleShot(100, lambda: speak(f"Đây là bài {lecture_name}"))
        return handler

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chương trình học tập"))

    def load_lecture_text(self, lecture_name):
        try:
            speak(f"bạn đã chọn {lecture_name} hãy chờ tải xuống nhé")
            lecture = db.find_lecture_by_name(lecture_name)
            self.textBrowser.setPlainText(lecture["content"])
            self.current_lecture = lecture
            speak(lecture["content"])
            speak("Nếu bạn muốn nghe lại bài giảng thì nói 'nghe lại' hoặc bấm nút nghe lại để nghe lại và nói không muốn nghe hoặc là bấm nút quay lại để quay lại hoặc nếu bạn muốn nghe bài lý thuyết khác thì hãy nói tôi muốn nghe bài khác hoặc bấm vào nút Nghe bài khác")

            self.handle_voice_command(lecture['content'])

        except Exception as e:
            speak("Có vẻ bài giảng này giáo viên chưa đẩy lên máy chủ mình sẽ tạo 1 bài giảng lý thuyết tạm thời về bài này nhé")
            k = generate_lectures(lecture_name)
            speak(k)
            self.current_lecture = k
            self.relisten()
    def handle_voice_command(self, content):
        while True:
            text = check()  # Thu âm
            text_lower = text.lower()
            if "tôi muốn nghe lại" == text_lower or "nghe lại" == text_lower:
                speak(content)
                self.relisten()
            elif "không muốn nghe" in text_lower or "không muốn" in text_lower:
                self.return_to_main_menu()
                break
            elif "tôi muốn nghe bài khác" in text_lower or "muốn nghe bài khác" in text_lower or "muốn nghe lại bài khác" in text_lower or "muốn nghe lại" in text_lower:
                speak("Bạn muốn nghe bài khác. Hãy chọn từ danh sách các bài lý thuyết.")
                self.load_available_lectures()
                break
            elif "quay lại" in text_lower:
                self.return_to_main_menu()
                break
            else:
                speak("không hợp lệ hãy nói lại")
                speak("Nếu bạn muốn nghe lại bài giảng thì nói 'nghe lại' hoặc bấm nút nghe lại để nghe lại và nói không muốn nghe hoặc là bấm nút quay lại để quay lại hoặc nếu bạn muốn nghe bài lý thuyết khác thì hãy nói tôi muốn nghe bài khác hoặc bấm vào nút Nghe bài khác")
    def relisten2(self):

        lecture = self.current_lecture
        if lecture:
            speak(lecture)
        else:
            speak("bạn chưa chọn bài gì cả")
    def relisten(self):

        lecture = self.current_lecture
        if lecture:
            speak("bạn có muốn nghe lại bài giảng này không?")
            speak("Nếu bạn muốn nghe lại bài giảng thì nói 'nghe lại' để nghe lại và nói không muốn nghe để quay lại hoặc nếu bạn muốn nghe bài lý thuyết khác thì hãy nói tôi muốn nghe bài khácNếu bạn muốn nghe lại bài giảng thì nói 'nghe lại' hoặc bấm nút nghe lại để nghe lại và nói không muốn nghe hoặc là bấm nút quay lại để quay lại hoặc nếu bạn muốn nghe bài lý thuyết khác thì hãy nói tôi muốn nghe bài khác hoặc bấm vào nút Nghe bài khác")
            self.handle_voice_command(lecture['content'])
    def handle_key_press(self, key):
        if key == 'e':
            self.return_to_main_menu()
    def return_to_main_menu(self, dialog=None):
        speak("Bạn đã quay trở về menu chính")
        from ui import Ui_Qdialog
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Qdialog()
        self.ui.setupUi(self.dialog)
        self.dialog.close()
        self.dialog.show()