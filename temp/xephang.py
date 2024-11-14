# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        
        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 780, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)  # Updated to 5 columns
        self.tableWidget.setHorizontalHeaderLabels(["Tên", "Xếp Hạng", "Câu đúng", "Câu sai", "Tổng câu hỏi đã làm"])


        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 500, 200, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Kiểm Tra")
        self.pushButton.setStyleSheet("""
            QPushButton {
                font: bold 14pt 'MS Shell Dlg 2';
                color: white;
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.pushButton.clicked.connect(self.receive_data_from_server)  # Connect to a function if needed

        # Title Label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 10, 500, 50))
        self.label.setStyleSheet("""
            font: 75 24pt 'MS Shell Dlg 2';
            color: #3F51B5;
            text-align: center;
        """)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.label.setObjectName("label")
        self.label.setText("XẾP HẠNG HỌC SINH")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Xếp Hạng Học Sinh"))

    def receive_data_from_server(self):
        url = "http://127.0.0.1:5000/get_information_ranks"
        res = requests.get(url)
        response = res.json()

        # Set row count
        self.tableWidget.setRowCount(len(response))
        

        for row, (name, data) in enumerate(response.items()):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))  
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["rank"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["user_correct"])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(data["user_fail"])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data["user_score"])))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
