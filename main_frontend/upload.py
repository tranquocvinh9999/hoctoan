import sys
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from functions.keyboard.keyboards import speak  
from functions.microphone.micro import check
from functions.microphone.micro import recognize_speech

class DragDropWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Tải Bài Giảng")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px dashed #555;
            border-radius: 20px;
            padding: 20px;
        """)

        self.label = QtWidgets.QLabel("Kéo và thả file bài giảng vào đây", self)
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
        self.back_button.clicked.connect(self.go_back)

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
        url = "http://127.0.0.1:5000/upload"
        with open(file_path, 'rb') as f:
                files = {"file": f}
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    speak("Bài giảng đã được tải lên thành công")
                    self.label.setText("Bài giảng đã được tải lên thành công!")
                else:
                    speak("Gửi bài giảng thất bại")
                    self.label.setText("Gửi bài giảng thất bại!")

    def go_back(self):
        self.label.setText("Quay về menu chính!")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Tải Bài Giảng")
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(DragDropWidget())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
