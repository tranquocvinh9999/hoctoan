from PyQt5 import QtCore, QtGui, QtWidgets
import requests

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
        

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 780, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)  
        self.tableWidget.setHorizontalHeaderLabels(["Tên", "Xếp Hạng", "Câu đúng", "Câu sai", "Tổng câu hỏi đã làm"])

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 500, 200, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Kiểm Tra")
        self.pushButton.setStyleSheet(""" 
            QPushButton { font: bold 14pt 'MS Shell Dlg 2'; color: white; background-color: #4CAF50; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.pushButton.clicked.connect(self.receive_data_from_server)  

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 10, 500, 50))
        self.label.setStyleSheet(""" font: 75 24pt 'MS Shell Dlg 2'; color: #3F51B5; text-align: center; """)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.label.setObjectName("label")
        self.label.setText("XẾP HẠNG HỌC SINH")


        self.back_button = QtWidgets.QPushButton(Dialog)
        self.back_button.setGeometry(QtCore.QRect(50, 500, 200, 50))  
        self.back_button.setObjectName("back_button")
        self.back_button.setText("Quay lại")
        self.back_button.setStyleSheet(""" 
            QPushButton { font: bold 14pt 'MS Shell Dlg 2'; color: white; background-color: #f44336; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #e53935; }
        """)
        self.back_button.clicked.connect(lambda: self.back_to_main_menu(main_dialog)) 

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Xếp Hạng Học Sinh"))

    def receive_data_from_server(self):
        url = "http://127.0.0.1:5000/get_information_ranks"
        res = requests.get(url)
        response = res.json()

 
        self.tableWidget.setRowCount(len(response))
        
        for row, (name, data) in enumerate(response.items()):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))  
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data["rank"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["user_correct"])) )
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(data["user_fail"])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(data["user_score"])))

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
