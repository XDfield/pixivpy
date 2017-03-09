# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/9
from pixivpy_login import *
from pixivpy_spider import *
import sys
import webbrowser
import os


class MainWindow(QtWidgets.QWidget, Ui_pixivpy_login):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 去除边界
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 将登陆提示信息隐藏
        self.login_info.setVisible(False)
        # 焦点切换
        self.setTab()
        # 按钮绑定
        self.buttonBinding()
        # 提供拖动功能
        self.__leftButtonPress = False
        self.__movePoint = QtCore.QPoint()
        # 创建爬虫实例
        self.p = PixivPy()

    def buttonBinding(self):
        # 退出按钮
        self.quitButton.pressed.connect(QtWidgets.qApp.quit)
        # 登陆按钮
        self.loginButton.pressed.connect(self.login)
        # 注册按钮
        self.signupButton.pressed.connect(self.openSignupWebSize)
        # 忘记密码按钮
        self.forgetButton.pressed.connect(self.openReminderWebSize)

    def setTab(self):
        self.setTabOrder(self.id_edit, self.pass_edit)
        self.setTabOrder(self.pass_edit, self.remember)
        self.setTabOrder(self.remember, self.forgetButton)
        self.setTabOrder(self.forgetButton, self.loginButton)
        self.setTabOrder(self.loginButton, self.signupButton)
        self.setTabOrder(self.signupButton, self.quitButton)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__leftButtonPress = True
            self.__movePoint = event.pos()

    def mouseMoveEvent(self, event):
        if self.__leftButtonPress:
            globalPos = event.globalPos()
            self.move(globalPos - self.__movePoint)

    def mouseReleaseEvent(self, event):
        self.__leftButtonPress = False

    # 登陆
    def login(self):
        # 获取输入的用户名与密码
        pixiv_id = self.id_edit.text()
        password = self.pass_edit.text()
        # 输入检测
        if pixiv_id == '':
            self.changeLoginInfo('您还没有输入pixiv ID或者电邮')
            return
        if password == '':
            self.changeLoginInfo('您还未输入密码')
            return
        if len(password) < 6 or len(password) > 72:
            self.changeLoginInfo('密码为6~72文字以内')
            return
        self.login_info.setVisible(False)
        self.p.setLoginInfo(pixiv_id, password)
        self.loginButton.setText('登录中...')
        Success, info = self.p.login()
        self.loginButton.setText('登录')
        if Success:
            self.login_info.setStyleSheet('background-color: #04be01')
            self.changeLoginInfo(info)
        else:
            self.changeLoginInfo(info)

    # 更改提示信息
    def changeLoginInfo(self, info):
        self.login_info.setText(info)
        if not self.login_info.isVisible():
            self.login_info.setVisible(True)

    # 打开网页
    def openReminderWebSize(self):
        url = 'https://www.pixiv.net/reminder.php'
        self.changeLoginInfo('即将打开密码找回页面')
        webbrowser.open(url)

    def openSignupWebSize(self):
        url = 'https://accounts.pixiv.net/signup?'
        self.changeLoginInfo('即将打开注册页面')
        webbrowser.open(url)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
