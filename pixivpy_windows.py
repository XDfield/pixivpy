# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/12
from pixivpy_login import *
from pixivpy_main import *
from pixivpy_spider import *
import webbrowser
import configparser

config = configparser.ConfigParser()


class MovableWindow(QtWidgets.QDialog):
    """隐藏边界并提供拖动功能"""
    def __init__(self):
        super(MovableWindow, self).__init__()
        # 去除边界
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 提供拖动功能
        self.__leftButtonPress = False
        self.__movePoint = QtCore.QPoint()

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


class LoginWindow(MovableWindow, Ui_pixivpy_login):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
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
        # 读取设置参数
        self.saveCookies = False

    def buttonBinding(self):
        # 退出按钮
        self.quitButton.pressed.connect(QtWidgets.qApp.quit)
        # 登陆按钮
        self.loginButton.pressed.connect(self.checkInput)
        # 注册按钮
        self.signupButton.pressed.connect(self.openSignupWebSize)
        # 忘记密码按钮
        self.forgetButton.pressed.connect(self.openReminderWebSize)
        self.remember.stateChanged[int].connect(self.autoLogin)

    def setTab(self):
        self.setTabOrder(self.id_edit, self.pass_edit)
        self.setTabOrder(self.pass_edit, self.remember)
        self.setTabOrder(self.remember, self.forgetButton)
        self.setTabOrder(self.forgetButton, self.loginButton)
        self.setTabOrder(self.loginButton, self.signupButton)
        self.setTabOrder(self.signupButton, self.quitButton)

    def checkInput(self):
        """检查用户输入"""
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
        self.login(pixiv_id, password)

    def login(self, pixiv_id, password):
        """执行用户登陆方法"""
        self.loginButton.setText('登录中...')
        self.p.setLoginInfo(pixiv_id, password)
        Success, info, cookies = self.p.login()
        self.loginButton.setText('登录')
        if Success:
            if self.saveCookies:
                config['user-setting']['cookies'] = cookies
                config.write(open('setting.ini', 'w'))
            self.login_info.setStyleSheet('background-color: #04be01')
            self.changeLoginInfo(info)
            self.accept()
        else:
            self.changeLoginInfo(info)
            config.write(open('setting.ini', 'w'))

    # 更改提示信息
    def changeLoginInfo(self, info):
        self.login_info.setText(info)
        if not self.login_info.isVisible():
            self.login_info.setVisible(True)

    def autoLogin(self, state):
        if state == 2:
            self.saveCookies = True
            config['user-setting']['autoLogin'] = 'True'
        else:
            self.saveCookies = False
            config['user-setting']['autoLogin'] = 'False'

    # 打开网页
    def openReminderWebSize(self):
        url = 'https://www.pixiv.net/reminder.php'
        self.changeLoginInfo('即将打开密码找回页面')
        webbrowser.open(url)

    def openSignupWebSize(self):
        url = 'https://accounts.pixiv.net/signup?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.changeLoginInfo('即将打开注册页面')
        webbrowser.open(url)

    def getCookies(self):
        return self.p.cookies


class MainWindow(MovableWindow, Ui_MainWindow):
    def __init__(self, cookies):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cookies = cookies

        self.num.setValidator(QtGui.QIntValidator(1, 50))
        # 默认保存位置为源目录
        self.savePath = ''
        # 添加模式选择
        self.addModes()
        # 按钮绑定
        self.buttonBinding()
        # 添加爬虫对象
        self.p = PixivPy()
        self.p.cookies = cookies
        self.p.getUserInfo()
        self.username.setText(self.p.username)
        self.setUserImage()

    def addModes(self):
        modes = ['今日', '本周', '本月', '新人', '原创',
                 '受男性欢迎', '受女性欢迎']
        self.mode_chose.addItems(modes)

    def buttonBinding(self):
        self.quitButton.pressed.connect(QtWidgets.qApp.quit)
        self.settingButton.pressed.connect(self.changeSavePath)
        self.beginDownload.pressed.connect(self.download)
        self.mode_chose.currentIndexChanged.connect(self.setMode)
        self.R18.stateChanged[int].connect(self.setR18)
        self.moreP.stateChanged[int].connect(self.setMoreP)

    def changeSavePath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(caption='选择图片保存路径', directory='C:/')
        self.p.savePath = path
        config['user-setting']['savepath'] = path
        config.write(open('setting.ini', 'w'))
        # print(path)

    def download(self):
        if self.num.text() == '':
            num = 20
        else:
            num = self.num.text()
        self.done_info.setText('爬取中...')
        self.p.getRankingInfo(int(num))
        self.p.saveRankingImg()
        self.done_info.setText('下载完成')

    def setMode(self):
        modes = ['daily', 'weekly', 'monthly', 'rookie', 'original',
                 'male',  'female']
        mode_index = self.mode_chose.currentIndex()
        self.p.mode = modes[mode_index]
        # print('模式更改为: '+self.p.mode)
        if self.mode_chose.currentText() in ['每月', '新人', '原创']:
            self.R18.setDisabled(True)
        else:
            self.R18.setDisabled(False)

    def setR18(self, state):
        if state == 2:
            self.p.r18 = True
        else:
            self.p.r18 = False

    def setMoreP(self, state):
        if state == 2:
            self.p.moreP = True
        else:
            self.p.moreP = False

    def setUserImage(self):
        from PIL import Image
        im = Image.open('user-image.jpg')
        im = im.resize((140, 120))
        re_im = im.crop((10, 0, 130, 120))
        re_im.save('user-image.jpg', 'JPEG')
        self.face.setPixmap(QtGui.QPixmap("user-image.jpg"))
