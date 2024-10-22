

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 547)
        Dialog.setStyleSheet("background-color: rgb(198, 198, 198);\n"
"background-color: rgb(139, 139, 139);\n"
"font: 8pt \"Segoe UI Historic\";")
        self.checkloggin = QtWidgets.QPushButton(Dialog)
        self.checkloggin.setGeometry(QtCore.QRect(50, 40, 411, 151))
        self.checkloggin.setStyleSheet("color: rgb(152, 255, 173);\n"
"font: 24pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(160, 243, 255);")
        self.checkloggin.setObjectName("checkloggin")
        self.checkloggin_2 = QtWidgets.QPushButton(Dialog)
        self.checkloggin_2.setGeometry(QtCore.QRect(50, 290, 411, 151))
        self.checkloggin_2.setStyleSheet("color: rgb(152, 255, 173);\n"
"font: 24pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(160, 243, 255);")
        self.checkloggin_2.setObjectName("checkloggin_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkloggin.setText(_translate("Dialog", "ĐĂNG KÝ"))
        self.checkloggin_2.setText(_translate("Dialog", "ĐĂNG NHẬP"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
