# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pixivpy_login.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pixivpy_login(object):
    def setupUi(self, pixivpy_login):
        pixivpy_login.setObjectName("pixivpy_login")
        pixivpy_login.resize(371, 442)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pixivpy_login.sizePolicy().hasHeightForWidth())
        pixivpy_login.setSizePolicy(sizePolicy)
        pixivpy_login.setStyleSheet("QWidget{\n"
"    font-family: \"微软雅黑\";\n"
"    display: block;\n"
"}\n"
"QWidget#pixivpy_login{\n"
"    background-color: transparent;\n"
"}\n"
"QLabel#background{\n"
"    background-color: #fff;\n"
"    border: 1px solid #ccc;\n"
"}\n"
"QLineEdit{\n"
"    margin: 0;\n"
"    padding: 0;\n"
"    padding-left: 10px;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 4px;\n"
"    font-size: 16px;\n"
"}\n"
"QLineEdit:placehoder-show{\n"
"    color: #ccc;\n"
"}\n"
"QPushButton{\n"
"    width: 290px;\n"
"    height: 40px;\n"
"    border-radius: 6px;\n"
"    color: #ffffff;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton{\n"
"    border-opacity: 200;\n"
"}\n"
"QLabel#logo{\n"
"    margin-bottom: 6px;\n"
"    background-repeat: no-repeat;    \n"
"}\n"
"QLabel#logo_text{\n"
"    color: #757c80;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"}\n"
"QLabel#login_info{\n"
"    background-color: #ccc;\n"
"    border-radius: 4px;\n"
"    margin-bottom: 2px;\n"
"    color: #fff;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"QCheckBox#remember{\n"
"    color: #757c80;\n"
"    font-size: 17px;\n"
"    font-weight: bold;\n"
"    spacing: 5px;\n"
"    \n"
"}")
        self.loginButton = QtWidgets.QPushButton(pixivpy_login)
        self.loginButton.setGeometry(QtCore.QRect(40, 340, 290, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setStyleSheet("#loginButton{\n"
"    background-color: #25c6ff;\n"
"    border-bottom: 3px solid #4b92ab;\n"
"    border-right: 2px solid #4b92ab;\n"
"    border-top: 1px solid #b2ebff;\n"
"    border-left: 2px solid #b2ebff;\n"
"}\n"
"#loginButton:pressed{\n"
"    border: 0;\n"
"}\n"
"#loginButton:hover{\n"
"    background-color: #75d7fa;\n"
"}")
        self.loginButton.setObjectName("loginButton")
        self.pass_edit = QtWidgets.QLineEdit(pixivpy_login)
        self.pass_edit.setGeometry(QtCore.QRect(40, 210, 290, 40))
        self.pass_edit.setStyleSheet("")
        self.pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_edit.setObjectName("pass_edit")
        self.id_edit = QtWidgets.QLineEdit(pixivpy_login)
        self.id_edit.setGeometry(QtCore.QRect(40, 171, 290, 40))
        self.id_edit.setStyleSheet("selection-background-color: darkgray;")
        self.id_edit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.id_edit.setObjectName("id_edit")
        self.logo = QtWidgets.QLabel(pixivpy_login)
        self.logo.setGeometry(QtCore.QRect(90, 40, 181, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("resource/logo.svg"))
        self.logo.setObjectName("logo")
        self.logo_text = QtWidgets.QLabel(pixivpy_login)
        self.logo_text.setGeometry(QtCore.QRect(0, 120, 363, 18))
        self.logo_text.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_text.setObjectName("logo_text")
        self.quitButton = QtWidgets.QPushButton(pixivpy_login)
        self.quitButton.setGeometry(QtCore.QRect(189, 390, 141, 40))
        self.quitButton.setStyleSheet("#quitButton{\n"
"    background-color: #dc4e41;\n"
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
        self.login_info = QtWidgets.QLabel(pixivpy_login)
        self.login_info.setEnabled(True)
        self.login_info.setGeometry(QtCore.QRect(40, 290, 290, 42))
        self.login_info.setMouseTracking(True)
        self.login_info.setInputMethodHints(QtCore.Qt.ImhNone)
        self.login_info.setTextFormat(QtCore.Qt.AutoText)
        self.login_info.setAlignment(QtCore.Qt.AlignCenter)
        self.login_info.setObjectName("login_info")
        self.remember = QtWidgets.QCheckBox(pixivpy_login)
        self.remember.setGeometry(QtCore.QRect(40, 260, 85, 20))
        self.remember.setStyleSheet("#remember:hover{\n"
"    color: #32a2e3;\n"
"}")
        self.remember.setObjectName("remember")
        self.forgetButton = QtWidgets.QPushButton(pixivpy_login)
        self.forgetButton.setGeometry(QtCore.QRect(240, 260, 90, 20))
        self.forgetButton.setStyleSheet("#forgetButton{\n"
"    color: #757c80;\n"
"    font-size: 17px;\n"
"    text-decoration: underline;\n"
"}\n"
"#forgetButton:hover{\n"
"    color: #32a2e3;\n"
"}")
        self.forgetButton.setObjectName("forgetButton")
        self.signupButton = QtWidgets.QPushButton(pixivpy_login)
        self.signupButton.setGeometry(QtCore.QRect(40, 390, 141, 40))
        self.signupButton.setStyleSheet("#signupButton{\n"
"    background-color: #7eba22;\n"
"    border-bottom: 3px solid #66823c;\n"
"    border-right: 2px solid #66823c;\n"
"    border-top: 1px solid #e4f7c6;\n"
"    border-left: 2px solid #e4f7c6;\n"
"}\n"
"#signupButton:pressed{\n"
"    border: 0;\n"
"}\n"
"#signupButton:hover{\n"
"    background-color: #a4d25c;\n"
"}")
        self.signupButton.setObjectName("signupButton")
        self.background = QtWidgets.QLabel(pixivpy_login)
        self.background.setGeometry(QtCore.QRect(0, 0, 371, 442))
        self.background.setStyleSheet("")
        self.background.setText("")
        self.background.setObjectName("background")
        self.background.raise_()
        self.loginButton.raise_()
        self.pass_edit.raise_()
        self.id_edit.raise_()
        self.logo.raise_()
        self.logo_text.raise_()
        self.quitButton.raise_()
        self.login_info.raise_()
        self.remember.raise_()
        self.forgetButton.raise_()
        self.signupButton.raise_()

        self.retranslateUi(pixivpy_login)
        QtCore.QMetaObject.connectSlotsByName(pixivpy_login)

    def retranslateUi(self, pixivpy_login):
        _translate = QtCore.QCoreApplication.translate
        pixivpy_login.setWindowTitle(_translate("pixivpy_login", "Form"))
        self.loginButton.setText(_translate("pixivpy_login", "登录"))
        self.pass_edit.setPlaceholderText(_translate("pixivpy_login", "密码"))
        self.id_edit.setPlaceholderText(_translate("pixivpy_login", "邮箱地址/pixiv ID"))
        self.logo_text.setText(_translate("pixivpy_login", "让创作变得更有乐趣"))
        self.quitButton.setText(_translate("pixivpy_login", "退出"))
        self.login_info.setText(_translate("pixivpy_login", "服务器异常"))
        self.remember.setText(_translate("pixivpy_login", "自动登录"))
        self.forgetButton.setText(_translate("pixivpy_login", "忘记密码?"))
        self.signupButton.setText(_translate("pixivpy_login", "注册"))
