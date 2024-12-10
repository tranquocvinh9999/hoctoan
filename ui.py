import sys
from PyQt5 import QtCore, QtWidgets
from gtts import gTTS
import os
from functions.keyboard.keyboards import speak
from main_frontend.lythuyet import Ui_Dialog as Ui_Dialog2 
from main_frontend.baitap import Ui_Dialog as Ui_Dialog3   
from main_frontend.xephang import Ui_Dialog as Ui_Dialog4  
from main_frontend.upload import MainWindow  
from functions.resource_path.path import resource_path
import json
file_pathss = resource_path("config/private.json")
with open(file_pathss) as f:
    settings = json.load(f)
    user = settings["username"]
    password = settings["password"]
class Ui_Qdialog(object):
    def __init__(self):
        self.user_account = 0

    def setupUi(self, Qdialog):
        
        Qdialog.setObjectName("Qdialog")
        Qdialog.resize(877, 496)
        Qdialog.setWindowFlags(Qdialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  
        Qdialog.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255), stop:1 rgba(100, 100, 100, 255));")
        Qdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # Remove window border
        Qdialog.setWindowState(QtCore.Qt.WindowFullScreen)  # Fullscreen mode
        Qdialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.pushButton = QtWidgets.QPushButton(Qdialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 17, 271, 181))
        self.pushButton.setStyleSheet(""" 
            QPushButton {
                font: 24pt "MS Reference Sans Serif"; 
                color: white; 
                background-color: rgb(85, 170, 255); 
                border-radius: 20px; 
            } 
            QPushButton:hover { 
                background-color: rgb(75, 160, 245); 
            } 
            QPushButton:pressed { 
                background-color: rgb(65, 150, 235); 
            } 
        """)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("LÝ THUYẾT")
        self.pushButton.clicked.connect(lambda: self.show_dialog(Ui_Dialog2, Qdialog))
        self.pushButton.enterEvent = lambda event: speak("Mở phần lý thuyết")  

        self.pushButton_2 = QtWidgets.QPushButton(Qdialog)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 20, 271, 181))
        self.pushButton_2.setStyleSheet(self.pushButton.styleSheet())
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("BÀI TẬP")
        self.pushButton_2.clicked.connect(lambda: self.show_dialog(Ui_Dialog3, Qdialog))
        self.pushButton_2.enterEvent = lambda event: speak("Mở phần bài tập")  

        self.pushButton_3 = QtWidgets.QPushButton(Qdialog)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 260, 271, 181))
        self.pushButton_3.setStyleSheet(self.pushButton.styleSheet())
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("XẾP HẠNG")
        self.pushButton_3.clicked.connect(lambda: self.show_dialog(Ui_Dialog4, Qdialog))
        self.pushButton_3.enterEvent = lambda event: speak("Mở phần xếp hạng") 

        self.pushButton_download = QtWidgets.QPushButton(Qdialog)
        self.pushButton_download.setGeometry(QtCore.QRect(550, 260, 271, 181))
        self.pushButton_download.setStyleSheet(self.pushButton.styleSheet())
        self.pushButton_download.setObjectName("pushButton_download")
        self.pushButton_download.setText("TẢI BÀI")
        self.pushButton_download.clicked.connect(self.download_content) 
        self.pushButton_download.enterEvent = lambda event: speak("Tải bài") 
        self.pushButton.setAccessibleName("Nút mở phần lý thuyết")
        self.pushButton_2.setAccessibleName("Nút mở phần bài tập")
        self.pushButton_3.setAccessibleName("Nút mở phần xếp hạng")
        self.pushButton_download.setAccessibleName("Nút tải bài")
        self.pushButton.setAccessibleDescription("Nhấn vào đây để mở phần lý thuyết.")
        self.pushButton_2.setAccessibleDescription("Nhấn vào đây để mở phần bài tập.")
        self.pushButton_3.setAccessibleDescription("Nhấn vào đây để mở phần xếp hạng.")
        self.pushButton_download.setAccessibleDescription("Nhấn vào đây để tải bài.")

        if user != "admin123--":
            self.pushButton_3.setVisible(False)
            self.pushButton_download.setVisible(False)

        self.retranslateUi(Qdialog)
        QtCore.QMetaObject.connectSlotsByName(Qdialog)

    def retranslateUi(self, Qdialog):
        Qdialog.setWindowTitle("Menu chính")

    def show_dialog(self, ui_class, main_dialog):
        main_dialog.hide() 
        self.dialog = QtWidgets.QDialog()
        ui = ui_class()
        ui.setupUi(self.dialog, main_dialog)
        if hasattr(ui, 'back_button'):
            ui.back_button.clicked.connect(lambda: self.back_to_main_menu(main_dialog))
    
        self.dialog.exec_()

    def back_to_main_menu(self, main_dialog):
        self.dialog.close()  
        main_dialog.show()  

    def download_content(self):
        self.dialog = MainWindow()  
        self.dialog.show() 
        Qdialog.hide()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Qdialog = QtWidgets.QDialog()
    ui = Ui_Qdialog()
    ui.setupUi(Qdialog)
    Qdialog.show()
    sys.exit(app.exec_())
