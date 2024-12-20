from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from functions.resource_path.path import resource_path
from functions.keyboard.keyboards import speak
import json
import database.database as db
from functions.microphone.micro import check


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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 260, 271, 181))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("XẾP HẠNG")
        self.pushButton_3.clicked.connect(lambda: self.show_dialog(Ui_Dialog, MainWindow))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))

    def show_dialog(self, ui_class, main_dialog):
        self.dialog = QtWidgets.QDialog() 
        ui = ui_class() 
        ui.setupUi(self.dialog, main_dialog)
        self.dialog.exec_()  

class Ui_Dialog(object):
    def setupUi(self, Dialog, main_dialog):
        self.dialog = Dialog  
        Dialog.setObjectName("Dialog")
        Dialog.resize(877, 496)
        Dialog.setWindowState(QtCore.Qt.WindowFullScreen)
        Dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # Tạo một layout cho dialog để căn chỉnh các nút
        layout = QtWidgets.QVBoxLayout(Dialog)

        # Tạo tableWidget
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Tên", "Xếp Hạng", "Câu đúng", "Câu sai", "Tổng câu hỏi đã làm", "Reset"]
        )
        layout.addWidget(self.tableWidget)

        # Tạo nút Kiểm tra
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setText("Kiểm Tra")
        self.pushButton.enterEvent = lambda event: speak("Lấy dữ liệu xuống") 
        self.pushButton.setAccessibleDescription("Lấy dữ liệu xuống")
        self.pushButton.clicked.connect(self.receive_data_from_server) 
        self.pushButton.setStyleSheet(""" 
            QPushButton { 
                font: bold 18pt 'MS Shell Dlg 2'; 
                color: white; 
                background-color: #4CAF50; 
                border-radius: 10px; 
                padding: 20px; 
                min-width: 200px; 
                min-height: 50px; 
            }
            QPushButton:hover { 
                background-color: #45a049; 
            }
        """)
        
        # Sử dụng setSizePolicy để nút kéo dài ra hết chiều rộng
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        layout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)

        # Tạo nút Quay lại
        self.back_button = QtWidgets.QPushButton(Dialog)
        self.back_button.setText("Quay lại")
        self.back_button.enterEvent = lambda event: speak("Quay lại trang chủ chính") 
        self.back_button.setAccessibleDescription("Quay lại trang chủ chính")
        self.back_button.setStyleSheet(""" 
            QPushButton { 
                font: bold 18pt 'MS Shell Dlg 2'; 
                color: white; 
                background-color: #f44336; 
                border-radius: 10px; 
                padding: 20px; 
                min-width: 200px; 
                min-height: 50px; 
            }
            QPushButton:hover { 
                background-color: #e53935; 
            }
        """)
        self.back_button.clicked.connect(lambda: self.back_to_main_menu(main_dialog)) 
        # Dùng setSizePolicy để kéo dài nút
        self.back_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter)

        # Tạo nút Reset
        self.reset_button = QtWidgets.QPushButton(Dialog)
        self.reset_button.setText("Reset") 
        self.reset_button.setStyleSheet(""" 
            QPushButton { 
                font: bold 18pt 'MS Shell Dlg 2'; 
                color: white; 
                background-color: #FF9800; 
                border-radius: 10px; 
                padding: 20px; 
                min-width: 200px; 
                min-height: 50px; 
            }
            QPushButton:hover { 
                background-color: #FB8C00; 
            }
        """)
        self.reset_button.clicked.connect(self.reset_data_on_server)  
        # Dùng setSizePolicy để kéo dài nút
        self.reset_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.reset_button, alignment=QtCore.Qt.AlignCenter)

        # Tạo tiêu đề
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("XẾP HẠNG HỌC SINH")
        self.label.setStyleSheet(""" font: 75 24pt 'MS Shell Dlg 2'; color: #3F51B5; text-align: center; """)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        user = read_and_update_data(resource_path("config/private.json"))
        if user == "admin123--":
            self.reset_button.setVisible(True)
        else:
            self.reset_button.setVisible(False)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Xếp Hạng Học Sinh"))

    def receive_data_from_server(self):
        try:
            response = db.sort_leaderboard()  # Lấy danh sách từ server
            print(response)
            self.tableWidget.setRowCount(len(response))  # Cài đặt số hàng trong bảng
            user = read_and_update_data(resource_path("config/private.json"))
            for row, user_data in enumerate(response):  # Lặp qua từng từ điển trong danh sách
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(user_data.get('username', '')))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(user_data.get('rank', '')))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user_data.get('user_correct', 0))))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user_data.get('user_fail', 0))))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(user_data.get('user_score', 0))))

                # Speak the data for the current user
                if user_data.get('username') == user and user != "admin123--":
                    speak(f"Dữ liệu của {user}")
                    speak(f"Học Lực: {user_data.get('rank')}")
                    speak(f"Câu Đúng: {user_data.get('user_correct')}")
                    speak(f"Câu Sai: {user_data.get('user_fail')}")
                    speak(f"Tổng số câu đã làm: {user_data.get('user_score')}")

                    speak("Bạn có muốn nghe lại dữ liệu không? Nói 'Có nghe lại' để nghe lại hoặc 'Không nghe lại' để tiếp tục.")
                    lecture_name = check()  
                    if lecture_name.lower() == 'có nghe lại' or lecture_name.lower() == 'nghe lại':
                        speak(f"Dữ liệu của {user}") 
                        speak(f"Học Lực: {user_data.get('rank')}")
                        speak(f"Câu Đúng: {user_data.get('user_correct')}")
                        speak(f"Câu Sai: {user_data.get('user_fail')}")
                        speak(f"Tổng số câu đã làm: {user_data.get('user_score')}")
                    elif lecture_name.lower() == 'không nghe lại' or lecture_name.lower() == 'không':
                        speak("Tiếp tục và quay trở lại menu chính")
                        self.back_button.click()
                    else:
                        speak("Tôi không hiểu câu trả lời của bạn. Tiếp tục với chương trình.")

                reset_button = QtWidgets.QPushButton("Reset")
                reset_button.setStyleSheet(""" 
                    QPushButton { font: bold 12pt 'MS Shell Dlg 2'; color: white; background-color: #FF9800; border-radius: 5px; padding: 5px; }
                    QPushButton:hover { background-color: #FB8C00; }
                """)
                reset_button.clicked.connect(lambda _, username=user_data.get('username'): self.reset_single_user(username))
                self.tableWidget.setCellWidget(row, 5, reset_button)
        except Exception as e:
            speak(f"Không thể lấy dữ liệu từ server: {str(e)}")

    def reset_data_on_server(self):
        try:
            res = db.reset_all_user()
            if res == 200:
                speak("Dữ liệu đã được reset thành công!")
                self.receive_data_from_server()  
            else:
                speak("Không thể reset dữ liệu!")
        except Exception as e:
            speak(f"Không thể kết nối tới server: {str(e)}")

    def reset_single_user(self, user):
        try:
            k = db.reset_single_user(user)
            if k == 200:
                speak(f"Dữ liệu của {user} đã được reset thành công!")
                self.receive_data_from_server()  
            else:
                speak(f"Không thể reset dữ liệu của {user}!")
        except Exception as e:
            speak(f"Không thể kết nối tới server: {str(e)}")

    def back_to_main_menu(self, main_dialog):
        from ui import Ui_Qdialog
        self.dialog = QtWidgets.QDialog()  
        self.ui = Ui_Qdialog()  # Tạo đối tượng giao diện chính
        self.ui.setupUi(self.dialog)  # Gọi phương thức setupUi từ Ui_Qdialog
        self.dialog.show()  # Hiển thị giao diện chính
        self.dialog.hide()  # Ẩn giao diện tải bài

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
