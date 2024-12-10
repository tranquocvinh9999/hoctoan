import os
import requests
from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
from functions.microphone.micro import check
from requests.utils import quote
import json
from functions.resource_path.path import resource_path
from PyQt5.QtCore import Qt
import keyboard, threading
import database.database as db

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")

class KeyPressListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True

    def run(self):
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.callback(event.name)

# file_pathss = resource_path("ip_host.json")
# with open(file_pathss) as f:
#     settings = json.load(f)
#     ip = settings["ip"]
#     port = settings["port"]

class Ui_Dialog(object):
    def setupUi(self, dialog, main_menu):
        self.dialog = dialog  
        self.main_menu = main_menu
        dialog.setObjectName("Dialog")
        dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        dialog.setStyleSheet("""background-color: white; color: black; font: 16pt 'Arial';""")
        
        # QTextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet(""" 
            font: 18pt 'MS Reference Sans Serif';
            color: black;
            background-color: white;
            border-radius: 15px;
            border: 3px solid #0078D7;
            padding: 20px;
        """)
        self.textBrowser.setAlignment(Qt.AlignLeft)
        self.textBrowser.setGeometry(QtCore.QRect(20, 100, 500, 350))
        self.textBrowser.setPlainText("Chào bạn! Hãy chọn chương học từ dưới đây.")
        
        # Back Button
        self.back_button = QtWidgets.QPushButton(dialog)
        self.back_button.setGeometry(QtCore.QRect(20, 470, 500, 100))
        self.back_button.setText("Quay lại")
        self.back_button.clicked.connect(lambda: self.return_to_main_menu(dialog))
        self.back_button.setStyleSheet(""" 
            font: 24pt 'MS Reference Sans Serif'; 
            color: white;
            background-color: #ff4d4d;
            border-radius: 15px;
            border: 3px solid #1a75ff;
        """)
        self.back_button.setAccessibleName("Back Button")
        self.back_button.setAccessibleDescription("Click to return to the main menu.")

        # Add Button
        self.add_button = QtWidgets.QPushButton(dialog)
        self.add_button.setGeometry(QtCore.QRect(20, 580, 500, 100))
        self.add_button.setText("Thêm Lý Thuyết Mới")
        self.add_button.clicked.connect(self.add_new_lecture)
        self.add_button.setStyleSheet(""" 
            font: 24pt 'MS Reference Sans Serif'; 
            color: white;
            background-color: #4CAF50;
            border-radius: 15px;
            border: 3px solid #1a75ff;
        """)
        self.add_button.setAccessibleName("Add New Lecture Button")
        self.add_button.setAccessibleDescription("Click to add a new lecture.")

        # Layout to hold buttons
        self.chapter_layout = QtWidgets.QVBoxLayout()
        self.chapter_layout.setContentsMargins(20, 20, 20, 20)
        self.chapter_layout.setSpacing(30)

        chapter_widget = QtWidgets.QWidget(dialog)
        chapter_widget.setLayout(self.chapter_layout)
        chapter_widget.setGeometry(QtCore.QRect(540, 100, 500, 600))

        self.load_available_lectures()

        self.add_button.show()
        self.back_button.show()
        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        # Show fullscreen mode
        dialog.showFullScreen()  # Show the dialog in fullscreen mode

        self.key_listener = KeyPressListener(self.handle_key_press)
        self.key_listener.start()

    def load_available_lectures(self): 
        lectures = db.find_all_lecture()

        # print(list(lectures))
        for lecture in lectures:
            lecture_name = lecture['name']
            button = QtWidgets.QPushButton(lecture_name)
            button.setStyleSheet(""" 
                font: 24pt 'MS Reference Sans Serif'; 
                color: white;
                background-color: #0078D7;
                border-radius: 15px;
                padding: 30px;
                margin: 20px;
            """)
            button.setAccessibleName(f"Lecture Button {lecture_name}")
            button.setAccessibleDescription(f"Click to open the lecture {lecture_name}")
            button.clicked.connect(lambda _, name=lecture_name: self.load_lecture_text(name))
            self.chapter_layout.addWidget(button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chương trình học tập"))

    def load_lecture_text(self, lecture_name): 
        try:
            lecture = db.find_lecture_by_name(lecture_name)
            self.textBrowser.setPlainText(lecture["content"])
            speak(lecture["content"])

        except Exception as e:
            error_message = f"Loi: {str(e)}"
            self.textBrowser.setPlainText(error_message)
            speak(error_message)
            self.return_to_main_menu()



    # def download_file(self, file_name):
    #     url = f'http://{ip}:{port}/download/{file_name}'
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         os.makedirs(resource_path("baigiang", exist_ok=True))
    #         with open(resource_path(f"baigiang/{file_name}", 'wb')) as f:
    #             f.write(response.content)
    #         speak(f"Bài giảng {file_name} đã được tải về.")
    #         self.load_available_lectures()
    #         return True
    #     else:
    #         speak("Tải file thất bại.")
    #         return False

    # def display_lecture_content(self, filename):
    #     try:
    #         with open(resource_path(filename), "r", encoding="utf-8") as file:
    #             content = file.read()
    #         self.textBrowser.setPlainText(content)
    #         speak(content)
    #     except Exception as e:
    #         error_message = f"Lỗi: {str(e)}"
    #         self.textBrowser.setPlainText(error_message)
    #         speak(error_message)
    #         self.return_to_main_menu()

    def add_new_lecture(self):
        speak("Xin vui lòng nói tên bài giảng bạn muốn thêm.")
        self.textBrowser.setPlainText("Xin vui lòng nói tên bài giảng bạn muốn thêm.")
        self.start_voice_recognition()

    def start_voice_recognition(self):
        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(self.on_lecture_name_recognized)
        self.voice_thread.start()

    # def on_lecture_name_recognized(self, lecture_name):
    #     if lecture_name:
    #         speak(f"Bạn đã chọn bài giảng: {lecture_name}")
    #         self.textBrowser.setPlainText(f"Bài giảng {lecture_name} đang được thêm vào...")
    #         self.download_file(lecture_name)
    #     else:
    #         speak("Không nhận diện được tên bài giảng.")

    def handle_key_press(self, key):
        if key == 'esc':
            self.return_to_main_menu()

    def return_to_main_menu(self, dialog=None):
        if not isinstance(self.main_menu, Ui_Dialog):
            self.main_menu = Ui_Dialog()  # Make sure it's an instance of Ui_Dialog
        self.main_menu.setupUi(dialog, self.main_menu)  # Pass 'self.main_menu' as the second argument
        self.dialog.hide()