# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(833, 469)
        self.cauhoi = QtWidgets.QTextBrowser(Dialog)
        self.cauhoi.setGeometry(QtCore.QRect(10, 20, 571, 171))
        self.cauhoi.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
"font: 8pt \"MS Shell Dlg 2\";\n"
"font: 16pt \"MS Shell Dlg 2\";")
        self.cauhoi.setObjectName("cauhoi")
        self.socaudung = QtWidgets.QLCDNumber(Dialog)
        self.socaudung.setGeometry(QtCore.QRect(710, 30, 64, 23))
        self.socaudung.setStyleSheet("background-color: rgb(143, 143, 143);")
        self.socaudung.setObjectName("socaudung")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(590, 60, 121, 20))
        self.label_3.setStyleSheet("background-color: rgb(255, 44, 16);\n"
"font: 25 8pt \"Microsoft JhengHei UI Light\";")
        self.label_3.setObjectName("label_3")
        self.socausai = QtWidgets.QLCDNumber(Dialog)
        self.socausai.setGeometry(QtCore.QRect(710, 60, 64, 23))
        self.socausai.setStyleSheet("background-color: rgb(133, 133, 133);")
        self.socausai.setObjectName("socausai")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(590, 30, 121, 20))
        self.label_4.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"font: 25 8pt \"Microsoft JhengHei UI Light\";")
        self.label_4.setObjectName("label_4")
        self.quaytrove = QtWidgets.QPushButton(Dialog)
        self.quaytrove.setGeometry(QtCore.QRect(610, 230, 221, 51))
        self.quaytrove.setObjectName("quaytrove")
        self.nhapketqua = QtWidgets.QLineEdit(Dialog)
        self.nhapketqua.setGeometry(QtCore.QRect(20, 250, 571, 161))
        self.nhapketqua.setStyleSheet("\n"
"font: 26pt \"MS Shell Dlg 2\";\n"
"color: rgb(123, 123, 123);")
        self.nhapketqua.setObjectName("nhapketqua")
        self.checkbutton = QtWidgets.QPushButton(Dialog)
        self.checkbutton.setGeometry(QtCore.QRect(10, 410, 591, 61))
        self.checkbutton.setObjectName("checkbutton")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(590, 90, 121, 20))
        self.label_5.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"font: 25 8pt \"Microsoft JhengHei UI Light\";")
        self.label_5.setObjectName("label_5")
        self.tongsodiem = QtWidgets.QLCDNumber(Dialog)
        self.tongsodiem.setGeometry(QtCore.QRect(710, 90, 64, 23))
        self.tongsodiem.setStyleSheet("background-color: rgb(143, 143, 143);")
        self.tongsodiem.setObjectName("tongsodiem")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(250, 170, 571, 81))
        self.label.setStyleSheet("color: rgb(255, 11, 43);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(600, 110, 231, 151))
        self.line.setStyleSheet("font: 75 8pt \"MS Shell Dlg 2\";")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(610, 290, 221, 181))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cauhoi.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">SỐ 7 CÓ PHẢI LÀ SỐ NGUYÊN TỐ KHÔNG</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_3.setText(_translate("Dialog", "SỐ CÂU SAI"))
        self.label_4.setText(_translate("Dialog", "SỐ CÂU ĐÚNG"))
        self.quaytrove.setText(_translate("Dialog", "QUAY TRỞ VỀ"))
        self.checkbutton.setText(_translate("Dialog", "KIỂM TRA"))
        self.label_5.setText(_translate("Dialog", "TỔNG SỐ ĐIỂM"))
        self.label.setText(_translate("Dialog", "KIỂM TRA BÀI TẬP"))
        self.pushButton.setText(_translate("Dialog", "MICRO"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
