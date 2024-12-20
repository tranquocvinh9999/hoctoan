import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QComboBox
from PyQt5 import QtCore, QtWidgets
import database.database as db
from functions.keyboard.keyboards import speak
class MyWindow(QWidget):
    def __init__(self, parent_dialog=None):
        super().__init__()
        self.parent_dialog = parent_dialog

        self.setWindowTitle("Giao diện bài tập")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()  
        main_layout = QVBoxLayout()

        self.combo_chuong = QComboBox(self)
        self.combo_chuong.setStyleSheet("""
        font: 28pt 'MS Reference Sans Serif';
        color: black;
        background-color: #f0f0f0;
        border-radius: 15px;
        border: 3px solid #1a75ff;
        padding: 10px;
        """)
        self.combo_chuong.setMinimumHeight(80)
        self.combo_chuong.setMinimumWidth(500)

        chapters = db.find_all_lecture()
        for lecture in chapters:
            name = lecture["name"]
            self.combo_chuong.addItem(name)

        main_layout.addWidget(self.combo_chuong)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        button_layout = QHBoxLayout()

        self.btn_xoa = QPushButton("Xóa bài", self)
        self.btn_xoa.setStyleSheet("""
            font: 24pt 'MS Reference Sans Serif';
            color: white;
            background-color: #ff4d4d;
            border-radius: 15px;
            border: 3px solid #1a75ff;
        """)
        self.btn_xoa.clicked.connect(self.delete_selected_chapter)
        button_layout.addWidget(self.btn_xoa)

        self.btn_quay_lai = QPushButton("Quay lại", self)
        self.btn_quay_lai.setStyleSheet("""
            font: 24pt 'MS Reference Sans Serif';
            color: white;
            background-color: #1e90ff;
            border-radius: 15px;
            border: 3px solid #1a75ff;
        """)
        self.btn_quay_lai.clicked.connect(self.go_back_to_main)
        button_layout.addWidget(self.btn_quay_lai)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def delete_selected_chapter(self):
        """Xóa chương được chọn."""
        selected_chapter = self.combo_chuong.currentText()

        if selected_chapter:
            db.remove_lecture_by_name(selected_chapter)
            print(f"Đã xóa chương: {selected_chapter}")

            index = self.combo_chuong.currentIndex()
            self.combo_chuong.removeItem(index)
        else:
            print("Chưa có chương nào được chọn để xóa.")

    def go_back_to_main(self):
        """Quay lại giao diện chính."""
        speak("bạn đã quay về giao diện chính")
        self.close()
        if self.parent_dialog:
            self.parent_dialog.show()
