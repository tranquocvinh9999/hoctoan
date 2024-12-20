import sys
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from functions.keyboard.keyboards import speak  
from functions.microphone.micro import check
from functions.microphone.micro import recognize_speech
from functions.resource_path.path import resource_path
import json
import database.database as db


class DragDropWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Tải Bài Giảng")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #555;
            border-radius: 20px;
            padding: 20px;
        """)

        self.label = QtWidgets.QLabel("Kéo và thả file bài giảng vào đây", self)
        self.label.enterEvent = lambda event: speak("Đây là phần kéo thả bài tập vào đây") 
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 20px;
            color: #333;
        """)
        self.label.setGeometry(100, 100, 600, 400)

        self.back_button = QtWidgets.QPushButton("Quay Về", self)
        self.back_button.setGeometry(300, 520, 200, 50)
        self.back_button.setStyleSheet("""
            font-size: 18px;
            color: white; 
            background-color: rgb(85, 170, 255); 
            border-radius: 10px; 
        """)
        self.back_button.clicked.connect(lambda: self.go_back())

        self.back_button.enterEvent = lambda event: speak("Đây là nút quay lại") 
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.back_button)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.upload(file_path)

    def upload(self, file_path):
        file_path_list = file_path.split("/")
        name = file_path_list[-1]
        name = name[:-4]

        with open(resource_path(file_path), 'r', encoding="utf8") as f: 
            db.insert_new_lecture(name, f.read())
            speak("Bài giảng đã được tải lên thành công")


    def go_back(self):
        from ui import Ui_Qdialog
        self.dialog = QtWidgets.QDialog()  
        self.ui = Ui_Qdialog() 
        self.ui.setupUi(self.dialog)  
        self.dialog.show() 
        self.hide() 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Tải Bài Giảng")
        self.setGeometry(100, 100, 800, 600)
        self.drag_drop_widget = DragDropWidget(self) 
        self.setCentralWidget(self.drag_drop_widget)
