import os
import requests
from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
from functions.microphone.micro import check
from requests.utils import quote
import json

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")

with open("ip_host.json") as f:
    settings = json.load(f)
    ip = settings["ip"]
    port = settings["port"]

class Ui_Dialog(object):
    def setupUi(self, dialog, main_menu):
        self.dialog = dialog  
        self.main_menu = main_menu
        dialog.setObjectName("Dialog")
        dialog.resize(721, 409)

        self.main_menu = main_menu

        self.timer = QtCore.QTimer(dialog)
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.start_voice_recognition)

        self.back_button = QtWidgets.QPushButton(dialog)
        self.back_button.setGeometry(QtCore.QRect(10, 350, 100, 30))
        self.back_button.setObjectName("back_button")
        self.back_button.setText("Quay lại")
        self.back_button.clicked.connect(lambda: self.return_to_main_menu(dialog))

        self.textBrowser = QtWidgets.QTextBrowser(dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 351, 381))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        self.timer.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chương trình học tập"))
        self.textBrowser.setHtml(_translate("Dialog", "<p>Xin mời bạn nói chương bạn muốn học hoặc nói 'quay trở về' để trở về menu chính.</p>"))

    def start_voice_recognition(self):
        self.timer.stop()
        self.textBrowser.setPlainText("Xin mời bạn nói chương bạn muốn học hoặc nói 'quay trở về' để trở về menu chính.")
        speak("Xin mời bạn nói chương mà bạn muốn học hoặc nói 'quay trở về' để trở về menu chính")

        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(self.handle_voice_recognition)
        self.voice_thread.start()

    def handle_voice_recognition(self, lecture_name):
        if lecture_name == "quay trở về":
            self.return_to_main_menu() 
        elif lecture_name:
            self.textBrowser.setPlainText(f"Bạn muốn học chương: {lecture_name}.")
            speak(f"Bạn muốn học chương: {lecture_name}. Chúng ta sẽ bắt đầu chương này.")
            self.load_lecture_text(lecture_name)
        else:
            self.textBrowser.setPlainText("Không thể nhận diện lời nói. Vui lòng thử lại.")
            speak("Không thể nhận diện lời nói. Vui lòng thử lại.")
            self.timer.start()

    def load_lecture_text(self, lecture_name):
        folder_path = "baigiang"
        os.makedirs(folder_path, exist_ok=True)
        filename = os.path.join(folder_path, f"{lecture_name}.txt")
        if not os.path.exists(filename):
            self.textBrowser.setPlainText("Bài giảng chưa có sẵn trên máy, đang tải về...")
            speak("Bài giảng chưa có sẵn trên máy, đang tải về...")
            if self.download_file(f"{lecture_name}.txt"):
                self.display_lecture_content(filename)
            else:
                self.textBrowser.setPlainText("Không thể tải bài giảng. Vui lòng kiểm tra kết nối.")
                speak("Không thể tải bài giảng. Vui lòng kiểm tra kết nối hoặc có thể bài giảng chưa có sẵn trên máy chủ!")
                self.return_to_main_menu() 
        else:
            self.display_lecture_content(filename)

    def display_lecture_content(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.textBrowser.setPlainText(content)
            speak(content)
            self.ask_to_repeat_lecture(filename) 
        except Exception as e:
            error_message = f"Lỗi: {str(e)}"
            self.textBrowser.setPlainText(error_message)
            speak(error_message)
            self.return_to_main_menu()  

    def ask_to_repeat_lecture(self, filename):
        self.textBrowser.setPlainText("Bạn có muốn nghe lại bài giảng không? Nói 'có chứ' để nghe lại hoặc 'không muốn' để quay về menu chính.")
        speak("Bạn có muốn nghe lại bài giảng không? Nói có chứ để nghe lại hoặc không muốn để quay về menu chính.")

        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(lambda response: self.handle_repeat_response(response, filename))
        self.voice_thread.start()

    def handle_repeat_response(self, response, filename):
        if response.lower() == "có chứ":
            speak("Chúng ta sẽ nghe lại bài giảng.")
            self.display_lecture_content(filename)  
        elif response.lower() == "không muốn":
            speak("Quay trở về menu chính.")
            self.return_to_main_menu()
        else:
            self.textBrowser.setPlainText("Không thể nhận diện câu trả lời. Vui lòng thử lại.")
            speak("Không thể nhận diện câu trả lời. Vui lòng thử lại.")
            self.ask_to_repeat_lecture(filename)  

    def download_file(self, file_name):
        url = f'http://{ip}:{port}/download/{file_name}'
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs("baigiang", exist_ok=True)  
            with open(f"baigiang/{file_name}", 'wb') as f:
                f.write(response.content)
            speak(f"Bài giảng {file_name} đã được tải về.")
            return True
        else:
            speak("Tải file thất bại.")
            return False

    def return_to_main_menu(self):
        if self.main_menu:
            self.main_menu.show() 
        self.timer.stop()
        self.dialog.hide()
