import subprocess, os
import sys 
import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from functions.microphone.micro import check
from functions.login_register.logn import new_user
from functions.login_register.logn import update_json
from functions.login_register.logn import req
from ui import Ui_Qdialog
from functions.resource_path.path import resource_path
yeucau = [
    "SpeechRecognition",
    "google-generativeai",
    "requests",
    "msvcrt",
    "gTTS",
    "pygame",
    "time",
    "random"
]


from functions.keyboard.keyboards import speak

def taithuvien():
    for lib in yeucau:
        try:
            
            __import__(lib)
        except ImportError:
            speak(f"{lib} không được tìm thấy đang tải xuống")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])



def load_user_data():
    with open(resource_path("config/private.json"), encoding='utf-8') as f:
        settings = json.load(f)
        usernames = settings.get("username", None)
        passwords = settings.get("password", None)
    
    return usernames, passwords


class Login(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 547)
        Dialog.setStyleSheet("background-color: rgb(198, 198, 198);\n"
                         "background-color: rgb(139, 139, 139);\n"
                         "font: 8pt \"Segoe UI Historic\";")
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 30, 351, 101))
        self.label.setStyleSheet("\n"
                                 "color: rgb(254, 254, 254);\n"
                                 "font: 28pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 120, 151, 91))
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.acc = QtWidgets.QLineEdit(Dialog)
        self.acc.setGeometry(QtCore.QRect(190, 141, 201, 51))
        self.acc.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: rgb(252, 252, 252)")
        self.acc.setText("")
        self.acc.setObjectName("acc")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 240, 151, 91))
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.passw = QtWidgets.QLineEdit(Dialog)
        self.passw.setGeometry(QtCore.QRect(190, 260, 201, 51))
        self.passw.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: rgb(252, 252, 252)")
        self.passw.setText("")
        self.passw.setObjectName("passw")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)

        self.checkloggin = QtWidgets.QPushButton(Dialog)
        self.checkloggin.setGeometry(QtCore.QRect(40, 380, 411, 151))
        self.checkloggin.setObjectName("checkloggin")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.checkloggin.clicked.connect(self.handle_login)

        self.acc.textChanged.connect(self.read_text_on_input)
        self.passw.textChanged.connect(self.read_text_on_input)

        self.acc.installEventFilter(self)
        self.passw.installEventFilter(self)
        self.checkloggin.installEventFilter(self)

        self.Dialog = Dialog

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ĐĂNG NHẬP"))
        self.label_2.setText(_translate("Dialog", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Dialog", "MẬT KHẨU"))
        self.checkloggin.setText(_translate("Dialog", "ĐĂNG NHẬP"))

    def handle_login(self):
        username = self.acc.text()
        password = self.passw.text()
        if username == "admin123--" and password == "nguyenvantroi123":
            speak("Đăng nhập giáo viên thành công!")
            update_json("username", "admin123--", "config/private.json")
            update_json("password", "nguyenvantroi123", "config/private.json")
            self.Dialog.hide()
            self.open_main_interface()
            return
        if req(username, password) == True: 
            print("Đăng nhập thành công!")
            update_json("username", username, "config/private.json")
            update_json("password", password, "config/private.json")
            self.Dialog.hide()
            self.open_main_interface()
        else:
            print("Đăng nhập thất bại!")

    def read_text_on_input(self, text):
        """Đọc to từng ký tự khi người dùng nhập"""
        if text:
            last_char = text[-1]  
            speak(last_char)  
    def eventFilter(self, source, event):
        """Xử lý sự kiện di chuột đến các ô nhập liệu và nút"""
        if event.type() == QtCore.QEvent.Enter:
            if source == self.acc:
                speak("Ô nhập tài khoản")
            elif source == self.passw:
                speak("Ô nhập mật khẩu")
            elif source == self.checkloggin:
                speak("Nút đăng nhập")
        return super().eventFilter(source, event)
    def open_main_interface(self):
        self.main_window = QtWidgets.QDialog()
        self.ui = Ui_Qdialog()
        self.ui.setupUi(self.main_window)
        self.main_window.show()




class Register(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 547)
        Dialog.setStyleSheet("background-color: rgb(198, 198, 198);\n"
                         "background-color: rgb(139, 139, 139);\n"
                         "font: 8pt \"Segoe UI Historic\";")
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 30, 351, 101))
        self.label.setStyleSheet("\n"
                                 "color: rgb(254, 254, 254);\n"
                                 "font: 28pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 120, 151, 91))
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.acc = QtWidgets.QLineEdit(Dialog)
        self.acc.setGeometry(QtCore.QRect(190, 141, 201, 51))
        self.acc.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: rgb(252, 252, 252)")
        self.acc.setText("")
        self.acc.setObjectName("acc")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 240, 151, 91))
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.passw = QtWidgets.QLineEdit(Dialog)
        self.passw.setGeometry(QtCore.QRect(190, 260, 201, 51))
        self.passw.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: rgb(252, 252, 252)")
        self.passw.setText("")
        self.passw.setObjectName("passw")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)

        self.register_btn = QtWidgets.QPushButton(Dialog)
        self.register_btn.setGeometry(QtCore.QRect(40, 380, 411, 151))
        self.register_btn.setObjectName("register_btn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.register_btn.clicked.connect(self.handle_register)


        self.acc.textChanged.connect(self.read_text_on_input)
        self.passw.textChanged.connect(self.read_text_on_input)

        self.acc.installEventFilter(self)
        self.passw.installEventFilter(self)
        self.register_btn.installEventFilter(self)

        self.Dialog = Dialog

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ĐĂNG KÝ"))
        self.label_2.setText(_translate("Dialog", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Dialog", "MẬT KHẨU"))
        self.register_btn.setText(_translate("Dialog", "ĐĂNG KÝ"))

    def handle_register(self):
        username = self.acc.text()
        password = self.passw.text()

        if username and password:
            if new_user(username, password):
                speak(f"Đăng ký thành công! Chào mừng {username}")
                update_json("username", username, "config/private.json")
                update_json("password", password, "config/private.json")
                self.Dialog.hide()
                self.open_main_interface()
            else:
                print(f"Đã có tài khoản {username}. Vui lòng thử tên khác.")
        else:
            print("Vui lòng nhập đầy đủ thông tin!")

    def read_text_on_input(self, text):
        """Đọc to từng ký tự khi người dùng nhập"""
        if text:
            last_char = text[-1]  
            speak(last_char)  

    def eventFilter(self, source, event):
        """Xử lý sự kiện di chuột đến các ô nhập liệu và nút"""
        if event.type() == QtCore.QEvent.Enter:
            if source == self.acc:
                speak("Ô nhập tài khoản")
            elif source == self.passw:
                speak("Ô nhập mật khẩu")
            elif source == self.register_btn:
                speak("Nút đăng ký")
        return super().eventFilter(source, event)

    def open_main_interface(self):
        from ui import Ui_Qdialog  
        self.main_window = QtWidgets.QDialog()
        self.ui = Ui_Qdialog()
        self.ui.setupUi(self.main_window)
        self.Dialog.accept()  
        self.main_window.exec_()  


def main():
    app = QtWidgets.QApplication([])

    username, password = load_user_data()

    if username and password:
        speak(f"Bạn đã có tài khoản tên là {username}. Bạn có muốn đăng nhập vào tài khoản này không? nói phải rồi để đăng nhập nói không phải để đăng ký tài khoản khác hoặc là nói tôi muốn đăng nhập tài khoản khác để đăng nhập")
        response = check()

        if response == "tôi muốn đăng nhập tài khoản khác":
            update_json("username", "", "config/private.json")
            update_json("password", "", "config/private.json")
            login = Login()
            login.exec_()

        elif response == "phải rồi":
            login = Login()
            login.exec_()

        elif response == "không phải":
            registration = Register()
            registration.exec_()

        else:
            speak("Lựa chọn không hợp lệ, khởi chạy giao diện đăng ký.")
            registration = Register()
            registration.exec_()

    else:
        speak("Hiện tại bạn chưa có tài khoản. Bạn muốn đăng nhập hay đăng ký tài khoản mới? Nói đăng nhập để đăng nhập hoặc nói đăng ký để tạo tài khoản.")
        response = check()

        if response == "đăng nhập":
            login = Login()
            login.exec_()

        elif response == "đăng ký":
            registration = Register()
            registration.exec_()

        else:
            speak("Lựa chọn không hợp lệ. Mặc định chuyển sang giao diện đăng ký.")
            registration = Register()
            registration.exec_()

    app.exec_()


if __name__ == "__main__":
    taithuvien()
    main()