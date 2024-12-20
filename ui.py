from PyQt5 import QtCore, QtWidgets
from gtts import gTTS
import os, threading
from functions.keyboard.keyboards import speak
from main_frontend.lythuyet import Ui_Dialog as Ui_Dialog2
from main_frontend.baitap import Ui_Dialog as Ui_Dialog3
from main_frontend.xephang import Ui_Dialog as Ui_Dialog4
from main_frontend.upload import MainWindow
from main_frontend.xoabai import MyWindow
from functions.resource_path.path import resource_path
import json, time
import keyboard, sys
from functions.microphone.micro import check
from PyQt5.QtCore import QTimer

# Function to read user data from JSON file
def read_and_update_data(file_path):
    with open(file_path) as f:
        settings = json.load(f)
        user = settings["username"]
        password = settings["password"]
        print(f"Username: {user}, Password: {password}")
        return user


class VoiceRecognitionThread(QtCore.QThread):
    recognized_text = QtCore.pyqtSignal(str)

    def run(self):
        lecture_name = check()
        self.recognized_text.emit(lecture_name if lecture_name else "")


class Ui_Qdialog(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.introduction_done = threading.Event()  # Event to signal when the introduction is done
        self.mouse_event_blocked = True  # Block mouse events initially

    def setupUi(self, Qdialog):
        self.dialog = Qdialog
        Qdialog.setObjectName("Qdialog")
        Qdialog.resize(877, 496)
        Qdialog.setWindowFlags(Qdialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        Qdialog.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255), stop:1 rgba(100, 100, 100, 255));")
        Qdialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        Qdialog.setWindowState(QtCore.Qt.WindowFullScreen)
        Qdialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # Create layout
        self.layout = QtWidgets.QGridLayout(Qdialog)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Button styling
        button_style = """
            QPushButton {
                font: bold 50pt "MS Reference Sans Serif";
                color: white;
                background-color: rgb(85, 170, 255);
                border-radius: 40px;
                padding: 40px;
            }
            QPushButton:hover {
                background-color: rgb(75, 160, 245);
            }
            QPushButton:pressed {
                background-color: rgb(65, 150, 235);
            }
        """

        # Buttons for different sections
        self.pushButton = QtWidgets.QPushButton("LÝ THUYẾT", Qdialog)
        self.pushButton.setStyleSheet(button_style)
        self.pushButton.enterEvent = lambda event: self.delayed_speak("Mở phần lý thuyết")
        self.pushButton.clicked.connect(lambda: self.show_dialog(Ui_Dialog2, Qdialog))
        self.layout.addWidget(self.pushButton, 0, 0)

        self.pushButton_2 = QtWidgets.QPushButton("BÀI TẬP", Qdialog)
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_2.enterEvent = lambda event: self.delayed_speak("Mở phần bài tập")
        self.pushButton_2.clicked.connect(lambda: self.show_dialog(Ui_Dialog3, Qdialog))
        self.layout.addWidget(self.pushButton_2, 0, 1)

        self.pushButton_3 = QtWidgets.QPushButton("XẾP HẠNG", Qdialog)
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_3.enterEvent = lambda event: self.delayed_speak("Mở phần xếp hạng")
        self.pushButton_3.clicked.connect(lambda: self.show_dialog(Ui_Dialog4, Qdialog))
        self.layout.addWidget(self.pushButton_3, 1, 0)

        self.pushButton_download = QtWidgets.QPushButton("TẢI BÀI", Qdialog)
        self.pushButton_download.enterEvent = lambda event: self.delayed_speak("Mở phần tải bài")
        self.pushButton_download.clicked.connect(self.download_content)
        self.pushButton_download.setStyleSheet(button_style)
        self.layout.addWidget(self.pushButton_download, 1, 1)

        self.pushButton_chapter = QtWidgets.QPushButton("QUẢN LÝ CHƯƠNG", Qdialog)
        self.pushButton_chapter.enterEvent = lambda event: self.delayed_speak("Mở phần quản lý bài lý thuyết")
        self.pushButton_chapter.setStyleSheet(button_style)
        self.pushButton_chapter.clicked.connect(self.show_chapter_manager)
        self.layout.addWidget(self.pushButton_chapter, 2, 0)

        # Button accessibility names for screen readers
        self.pushButton.setAccessibleName("Nút mở phần lý thuyết")
        self.pushButton_2.setAccessibleName("Nút mở phần bài tập")
        self.pushButton_3.setAccessibleName("Nút mở phần xếp hạng")
        self.pushButton_download.setAccessibleName("Nút tải bài")
        self.pushButton_chapter.setAccessibleName("Nút quản lý bài lý thuyết")

        # Speak intro message
        QTimer.singleShot(100, lambda: self.speak_intro())  # Delay introduction speech to avoid conflicts

        # Read user data and apply logic based on user type
        initial_user_data = read_and_update_data(resource_path("config/private.json"))
        if initial_user_data == "admin123--":
            self.pushButton_3.setVisible(True)
            self.pushButton_download.setVisible(True)
            self.pushButton_chapter.setVisible(True)
        else:
            self.pushButton_3.setVisible(True)
            self.pushButton_download.setVisible(False)
            self.pushButton_chapter.setVisible(False)

        self.retranslateUi(Qdialog)
        QtCore.QMetaObject.connectSlotsByName(Qdialog)
        self.dialog.installEventFilter(self)

        # Setup voice recognition thread
        self.recognition_thread = VoiceRecognitionThread()
        self.recognition_thread.recognized_text.connect(self.handle_recognized_text)

        Qdialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Qdialog.installEventFilter(self)

    def speak_intro(self):
        speak("Chào bạn đến với phần mềm học toán ở đây có các nút như lý thuyết bài tập và xếp hạng thứ nhất là bạn nhấn vào nút là bạn nhấn phím Q để nói ra phần bạn muốn bấm")
        self.introduction_done.set()  # Mark introduction as done
        self.mouse_event_blocked = False  # Allow mouse events after introduction

    def delayed_speak(self, text):
        if not self.mouse_event_blocked:  # Only speak when mouse events are allowed
            speak(text)

    def retranslateUi(self, Qdialog):
        Qdialog.setWindowTitle("Menu chính")

    def handle_recognized_text(self, recognized_text):
        if recognized_text.lower() == "lý thuyết":
            self.pushButton.click()
        elif recognized_text.lower() == "bài tập":
            self.pushButton_2.click()
        elif recognized_text.lower() == "xếp hạng":
            self.pushButton_3.click()
        elif recognized_text.lower() == "tải bài":
            self.pushButton_download.click()

    def show_dialog(self, ui_class, main_dialog):
        main_dialog.hide()  # Hide main dialog
        self.dialog = QtWidgets.QDialog()  # Create new dialog
        ui = ui_class()  # Initialize the passed UI class
        ui.setupUi(self.dialog, main_dialog)
        if hasattr(ui, 'back_button'):
            ui.back_button.clicked.connect(lambda: self.back_to_main_menu(main_dialog))
        self.dialog.exec_()

    def back_to_main_menu(self, main_dialog):
        self.dialog.hide()
        self.dialog.close()  
        main_dialog.show()  
        speak("Bạn đã quay trở lại giao diện chính")
        self.speak_intro()  # Reintroduce the main menu when returning

    def download_content(self):
        self.dialog.hide()
        self.dialog = MainWindow()  # Initialize download window
        self.dialog.drag_drop_widget.main_window = self.dialog  # Attach main window reference
        self.dialog.show()  # Show the download content window

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:  # Listen for 'Q' key press
            speak("Hãy nói phần mà bạn muốn vô bao gồm lý thuyết bài tập xếp hạng")
            self.recognition_thread.start()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
        return super().eventFilter(source, event)
    def show_chapter_manager(self):
        self.dialog.hide()  # Hide main menu
        self.chapter_manager = MyWindow(self.dialog)  # Pass main dialog reference
        self.chapter_manager.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Qdialog = QtWidgets.QDialog()
    ui = Ui_Qdialog()
    ui.setupUi(Qdialog)
    Qdialog.show()
    sys.exit(app.exec_())
