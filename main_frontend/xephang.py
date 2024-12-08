from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from functions.resource_path.path import resource_path
import json
file_pathss = resource_path("ip_host.json")
with open(file_pathss) as f:
    settings = json.load(f)
    ip = settings["ip"]
    port = settings["port"]
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
        Dialog.resize(800, 600)
        Dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 780, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)  
        self.tableWidget.setHorizontalHeaderLabels(
            ["Tên", "Xếp Hạng", "Câu đúng", "Câu sai", "Tổng câu hỏi đã làm", "Reset"]
        )
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 500, 200, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Kiểm Tra")
        self.pushButton.setStyleSheet(""" 
            QPushButton { font: bold 14pt 'MS Shell Dlg 2'; color: white; background-color: #4CAF50; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.pushButton.clicked.connect(self.receive_data_from_server)  


        self.back_button = QtWidgets.QPushButton(Dialog)
        self.back_button.setGeometry(QtCore.QRect(50, 500, 200, 50))  
        self.back_button.setObjectName("back_button")
        self.back_button.setText("Quay lại")
        self.back_button.setStyleSheet(""" 
            QPushButton { font: bold 14pt 'MS Shell Dlg 2'; color: white; background-color: #f44336; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #e53935; }
        """)
        self.back_button.clicked.connect(lambda: self.back_to_main_menu(main_dialog)) 


        self.reset_button = QtWidgets.QPushButton(Dialog)
        self.reset_button.setGeometry(QtCore.QRect(550, 500, 200, 50))
        self.reset_button.setObjectName("reset_button")
        self.reset_button.setText("Reset")
        self.reset_button.setStyleSheet(""" 
            QPushButton { font: bold 14pt 'MS Shell Dlg 2'; color: white; background-color: #FF9800; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #FB8C00; }
        """)
        self.reset_button.clicked.connect(self.reset_data_on_server)  


        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 10, 500, 50))
        self.label.setStyleSheet(""" font: 75 24pt 'MS Shell Dlg 2'; color: #3F51B5; text-align: center; """)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.label.setObjectName("label")
        self.label.setText("XẾP HẠNG HỌC SINH")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Xếp Hạng Học Sinh"))

    def receive_data_from_server(self):
        url = f"http://{ip}:{port}/get_information_ranks"
        res = requests.get(url)
        response = res.json()

        self.tableWidget.setRowCount(len(response))

        for row, (name, data) in enumerate(response.items()):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["rank"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["user_correct"])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(data["user_fail"])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data["user_score"])))

            reset_button = QtWidgets.QPushButton("Reset")
            reset_button.setStyleSheet(""" 
                QPushButton { font: bold 12pt 'MS Shell Dlg 2'; color: white; background-color: #FF9800; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #FB8C00; }
            """)
            reset_button.clicked.connect(lambda _, user=name: self.reset_single_user(user))
            self.tableWidget.setCellWidget(row, 5, reset_button)

    def reset_data_on_server(self):
        try:
            url = f"http://{ip}:{port}/reset_data_on_server"
            res = requests.post(url)  
            if res.status_code == 200:
                QtWidgets.QMessageBox.information(self.dialog, "Thành công", "Dữ liệu đã được reset thành công!")
                self.receive_data_from_server()  
            else:
                QtWidgets.QMessageBox.warning(self.dialog, "Lỗi", "Không thể reset dữ liệu!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.dialog, "Lỗi", f"Không thể kết nối tới server: {str(e)}")
    def reset_single_user(self, user):
        try:
            url = f"http://{ip}:{port}/reset_single_user"
            payload = {"username": user}
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                QtWidgets.QMessageBox.information(self.dialog, "Thành công", f"Dữ liệu của {user} đã được reset thành công!")
                self.receive_data_from_server()  
            else:
                QtWidgets.QMessageBox.warning(self.dialog, "Lỗi", f"Không thể reset dữ liệu của {user}!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.dialog, "Lỗi", f"Không thể kết nối tới server: {str(e)}")

    def back_to_main_menu(self, main_dialog):
        self.dialog.close() 
        main_dialog.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
