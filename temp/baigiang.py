from PyQt5 import QtCore, QtWidgets
from functions.keyboard.keyboards import speak
from functions.microphone.micro import check

class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(721, 409)

        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 351, 381))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

        self.timer = QtCore.QTimer(Dialog)
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.start_voice_recognition)
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

    def return_to_main_menu(self):

        self.textBrowser.setPlainText("Bạn đã quay trở về menu chính.")
        speak("Bạn đã quay trở về menu chính.")
        # gọi quay trở lại menu chính tại đây
        self.timer.start()  

    def load_lecture_text(self, lecture_name):
        filename = f"{lecture_name}.txt"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.textBrowser.setPlainText(content)
            speak(content)
            self.ask_to_repeat(content)  
        except FileNotFoundError:
            self.textBrowser.setPlainText("Lỗi: Không tìm thấy file bài giảng.")
            speak("Lỗi: Không tìm thấy file bài giảng.")
        except Exception as e:
            error_message = f"Lỗi: {str(e)}"
            self.textBrowser.setPlainText(error_message)
            speak(error_message)

    def ask_to_repeat(self, content):
        speak("Bạn có muốn nghe lại nội dung này không? Nói 'có' để nghe lại, hoặc 'quay trở về' để quay lại menu chính.")
        self.textBrowser.setPlainText("Bạn có muốn nghe lại nội dung này không? Nói 'có' để nghe lại, hoặc 'quay trở về' để quay lại menu chính.")

        self.voice_thread = VoiceRecognitionThread()
        self.voice_thread.recognized_text.connect(lambda text: self.handle_repeat_choice(text, content))
        self.voice_thread.start()

    def handle_repeat_choice(self, choice, content):
        if choice == "có":
            self.textBrowser.setPlainText(content)
            speak(content)
            self.ask_to_repeat(content) 
        elif choice == "quay trở về":
            self.return_to_main_menu()
        else:
            self.textBrowser.setPlainText("Không thể nhận diện câu trả lời. Vui lòng thử lại.")
            speak("Không thể nhận diện câu trả lời. Vui lòng thử lại.")
            self.ask_to_repeat(content) 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
