import subprocess, os  
import sys 
import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from functions.microphone.micro import check
import database.database as db
from functions.update.update import update_json
from ui import Ui_Qdialog
from functions.resource_path.path import resource_path
from functions.keyboard.keyboards import speak

# Load user data (username and password)
def load_user_data():
    with open(resource_path("config/private.json"), encoding='utf-8') as f:
        settings = json.load(f)
        usernames = settings.get("username", None)
        passwords = settings.get("password", None)
    return usernames, passwords


class MainChoice(QtWidgets.QDialog):
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
        
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(40, 240, 411, 151))
        self.login_button.setObjectName("login_button")
        self.login_button.setText("ĐĂNG NHẬP")
        
        self.register_button = QtWidgets.QPushButton(Dialog)
        self.register_button.setGeometry(QtCore.QRect(40, 380, 411, 151))
        self.register_button.setObjectName("register_button")
        self.register_button.setText("ĐĂNG KÝ")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.login_button.clicked.connect(self.open_login)
        self.register_button.clicked.connect(self.open_register)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lựa Chọn Đăng Nhập / Đăng Ký"))
        self.label.setText(_translate("Dialog", "Chọn Hình Thức Đăng Nhập"))

    def open_login(self):
        self.login_window = Login()
        self.login_window.show()
        self.close()

    def open_register(self):
        self.register_window = Register()
        self.register_window.show()
        self.close()


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
        self.checkloggin.setText("ĐĂNG NHẬP")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.checkloggin.clicked.connect(self.handle_login)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ĐĂNG NHẬP"))
        self.label_2.setText(_translate("Dialog", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Dialog", "MẬT KHẨU"))

    def check_user_password(self, username, password):
        return db.check_user_passw(username, password)

    def handle_login(self):
        username = self.acc.text()
        password = self.passw.text()
        if username == "admin123--" and password == "nguyenvantroi123":
            speak("Đăng nhập giáo viên thành công!")
            update_json("username", "admin123--", "config/private.json")
            update_json("password", "nguyenvantroi123", "config/private.json")
            self.hide()
            self.open_main_interface()
            return
    
        if self.check_user_password(username, password) == True: 
            speak("Đăng nhập thành công!")
            update_json("username", username, "config/private.json")
            update_json("password", password, "config/private.json")
            self.hide()
            self.open_main_interface()
        else:
            speak("Đăng nhập thất bại!")

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
        self.register_btn.setText("ĐĂNG KÝ")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.register_btn.clicked.connect(self.handle_register)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ĐĂNG KÝ"))
        self.label_2.setText(_translate("Dialog", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Dialog", "MẬT KHẨU"))

    def create_new_user(self, username, password):
        return db.create_new_user(username, password)

    def handle_register(self):
        username = self.acc.text()
        password = self.passw.text()

        if username and password:
            if self.create_new_user(username, password):
                speak(f"Đăng ký thành công! Chào mừng {username}")
                update_json("username", username, "config/private.json")
                update_json("password", password, "config/private.json")
                self.hide()
                self.open_main_interface()
            else:
                speak("Tài khoản đã tồn tại!")
        else:
            speak("Vui lòng nhập đầy đủ thông tin!")

    def open_main_interface(self):
        self.main_window = QtWidgets.QDialog()
        self.ui = Ui_Qdialog()
        self.ui.setupUi(self.main_window)
        self.main_window.show()


# Main function to run the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    choice_window = MainChoice()  # Show main choice window first
    choice_window.show()
    sys.exit(app.exec_())
