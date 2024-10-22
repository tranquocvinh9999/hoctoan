

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 547)
        Dialog.setStyleSheet("background-color: rgb(198, 198, 198);\n"
"background-color: rgb(139, 139, 139);\n"
"font: 8pt \"Segoe UI Historic\";")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 20, 351, 101))
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
        self.checkloggin = QtWidgets.QPushButton(Dialog)
        self.checkloggin.setGeometry(QtCore.QRect(40, 380, 411, 151))
        self.checkloggin.setObjectName("checkloggin")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ĐĂNG KÝ"))
        self.label_2.setText(_translate("Dialog", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Dialog", "MẬT KHẨU"))
        self.checkloggin.setText(_translate("Dialog", "ĐĂNG KÝ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
