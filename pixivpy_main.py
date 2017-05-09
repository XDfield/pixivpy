# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pixivpy_main.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 472)
        MainWindow.setStyleSheet("QWidget{\n"
"    font-family: \"微软雅黑\";\n"
"    font-weight: bold;\n"
"    display: block;\n"
"    color: #fff\n"
"}\n"
"QLabel#background{\n"
"    background-color: #fff;\n"
"}\n"
"QLabel#info_label{\n"
"    background-color: rgb(32, 121, 255);\n"
"}\n"
"QPushButton{\n"
"    border-radius: 3px;\n"
"    font-size: 16px;\n"
"}\n"
"QCheckBox{\n"
"    color: rgb(100, 100, 100);\n"
"    font-size: 20px;\n"
"    spacing: 2px\n"
"}\n"
"QCheckBox::indicator{\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}")
        self.background = QtWidgets.QLabel(MainWindow)
        self.background.setGeometry(QtCore.QRect(0, 0, 371, 471))
        self.background.setText("")
        self.background.setObjectName("background")
        self.info_label = QtWidgets.QLabel(MainWindow)
        self.info_label.setGeometry(QtCore.QRect(0, 0, 371, 120))
        self.info_label.setText("")
        self.info_label.setObjectName("info_label")
        self.quitButton = QtWidgets.QPushButton(MainWindow)
        self.quitButton.setGeometry(QtCore.QRect(270, 0, 101, 40))
        self.quitButton.setStyleSheet("#quitButton{\n"
"    background-color:#dc4e41;\n"
"    border-bottom: 3px solid #995751;\n"
"    border-right: 2px solid #995751;\n"
"    border-top: 1px solid #f7bdb7;\n"
"    border-left: 2px solid #f7bdb7;\n"
"}\n"
"#quitButton:pressed{\n"
"    border: 0;\n"
"}\n"
"#quitButton:hover{\n"
"    background-color: #ed8c83;\n"
"}")
        self.quitButton.setObjectName("quitButton")
        self.settingButton = QtWidgets.QPushButton(MainWindow)
        self.settingButton.setGeometry(QtCore.QRect(270, 80, 101, 40))
        self.settingButton.setStyleSheet("#settingButton{\n"
"    background-color: #7eba22;\n"
"    border-bottom: 3px solid #66823c;\n"
"    border-right: 2px solid #66823c;\n"
"    border-top: 1px solid #e4f7c6;\n"
"    border-left: 2px solid #e4f7c6;\n"
"}\n"
"#settingButton:pressed{\n"
"    border: 0;\n"
"}\n"
"#settingButton:hover{\n"
"    background-color: #a4d25c;\n"
"}")
        self.settingButton.setObjectName("settingButton")
        self.face = QtWidgets.QLabel(MainWindow)
        self.face.setGeometry(QtCore.QRect(0, 0, 120, 120))
        self.face.setStyleSheet("#face{\n"
"    background-color: rgb(172, 172, 172);\n"
"}")
        self.face.setText("")
        self.face.setObjectName("face")
        self.done_info = QtWidgets.QLabel(MainWindow)
        self.done_info.setGeometry(QtCore.QRect(60, 300, 251, 61))
        self.done_info.setStyleSheet("#done_info{\n"
"    background-color: rgb(170, 255, 0);\n"
"    border-radius: 5px;\n"
"    font-size: 20px;\n"
"}")
        self.done_info.setAlignment(QtCore.Qt.AlignCenter)
        self.done_info.setObjectName("done_info")
        self.R18 = QtWidgets.QCheckBox(MainWindow)
        self.R18.setGeometry(QtCore.QRect(50, 200, 61, 31))
        self.R18.setStyleSheet("#R18:hover{\n"
"    color: #32a2e3;\n"
"}")
        self.R18.setObjectName("R18")
        self.moreP = QtWidgets.QCheckBox(MainWindow)
        self.moreP.setGeometry(QtCore.QRect(160, 200, 181, 31))
        self.moreP.setStyleSheet("#moreP:hover{\n"
"    color: #32a2e3;    \n"
"}")
        self.moreP.setObjectName("moreP")
        self.hello = QtWidgets.QLabel(MainWindow)
        self.hello.setGeometry(QtCore.QRect(130, 20, 61, 21))
        self.hello.setStyleSheet("#hello{\n"
"    font-size: 20px;\n"
"}")
        self.hello.setObjectName("hello")
        self.username = QtWidgets.QLabel(MainWindow)
        self.username.setGeometry(QtCore.QRect(130, 50, 140, 21))
        self.username.setStyleSheet("#username{\n"
"    font-size: 20px;\n"
"}")
        self.username.setObjectName("username")
        self.mode_chose = QtWidgets.QComboBox(MainWindow)
        self.mode_chose.setGeometry(QtCore.QRect(50, 150, 271, 40))
        self.mode_chose.setStyleSheet("#mode_chose{\n"
"    border-radius: 5px;\n"
"    background-color: rgb(170, 226, 255);\n"
"    font-size: 20px;\n"
"    color: rgb(4, 20, 65);\n"
"    padding: 1px 18px\n"
"}\n"
"#mode_chose:drop-down{\n"
"    width: 35px;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: rgb(62, 113, 175);\n"
"}\n"
"#mode_chose QAbstractItemView {\n"
"    background-color: rgb(212, 237, 255);\n"
"    selection-background-color: rgb(153, 171, 184);\n"
"    font-size: 18px;\n"
"    color: rgb(68, 80, 100);\n"
"}")
        self.mode_chose.setCurrentText("")
        self.mode_chose.setMaxVisibleItems(7)
        self.mode_chose.setMaxCount(7)
        self.mode_chose.setObjectName("mode_chose")
        self.beginDownload = QtWidgets.QPushButton(MainWindow)
        self.beginDownload.setGeometry(QtCore.QRect(90, 380, 191, 61))
        self.beginDownload.setStyleSheet("#beginDownload{\n"
"    background-color: rgb(25, 117, 255);\n"
"    border-radius: 5px;\n"
"    font-size: 20px;\n"
"    border-right: 2px solid rgb(14, 70, 152);\n"
"    border-left: 2px solid rgb(166, 220, 255);\n"
"    border-top: 1px solid rgb(166, 220, 255);\n"
"    border-bottom: 3px solid rgb(14, 70, 152);\n"
"}\n"
"#beginDownload:pressed{\n"
"    border: 0;\n"
"}\n"
"#beginDownload:hover{\n"
"    background-color: rgb(94, 172, 255);\n"
"}")
        self.beginDownload.setObjectName("beginDownload")
        self.num = QtWidgets.QLineEdit(MainWindow)
        self.num.setGeometry(QtCore.QRect(130, 240, 121, 41))
        self.num.setStyleSheet("#num{\n"
"    border: 2px solid #ccc;\n"
"    border-radius: 3px;\n"
"    font-size: 18px;\n"
"    color: rgb(125, 125, 125)\n"
"}\n"
"")
        self.num.setObjectName("num")
        self.num_info = QtWidgets.QLabel(MainWindow)
        self.num_info.setGeometry(QtCore.QRect(50, 250, 71, 21))
        self.num_info.setStyleSheet("#num_info{\n"
"    color: rgb(100, 100, 100);\n"
"    font-size: 20px;\n"
"}")
        self.num_info.setObjectName("num_info")
        self.logoutButton = QtWidgets.QPushButton(MainWindow)
        self.logoutButton.setGeometry(QtCore.QRect(270, 40, 101, 41))
        self.logoutButton.setStyleSheet("#logoutButton{\n"
"    background-color:rgb(255, 193, 48);\n"
"    border-bottom: 3px solid rgb(177, 134, 33);\n"
"    border-right: 2px solid rgb(177, 134, 33);\n"
"    border-top: 1px solid rgb(254, 255, 184);\n"
"    border-left: 2px solid rgb(254, 255, 184);\n"
"}\n"
"#logoutButton:pressed{\n"
"    border: 0;\n"
"}\n"
"#logoutButton:hover{\n"
"    background-color: rgb(255, 202, 116);\n"
"}")
        self.logoutButton.setObjectName("logoutButton")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
        self.quitButton.setText(_translate("MainWindow", "退出"))
        self.settingButton.setText(_translate("MainWindow", "保存位置"))
        self.done_info.setText(_translate("MainWindow", "请选择模式"))
        self.R18.setText(_translate("MainWindow", "R18"))
        self.moreP.setText(_translate("MainWindow", "同时下载多P作品"))
        self.hello.setText(_translate("MainWindow", "你好呀"))
        self.username.setText(_translate("MainWindow", "username"))
        self.beginDownload.setText(_translate("MainWindow", "开始下载"))
        self.num.setPlaceholderText(_translate("MainWindow", "(默认前20)"))
        self.num_info.setText(_translate("MainWindow", "前几名:"))
        self.logoutButton.setText(_translate("MainWindow", "注销"))

