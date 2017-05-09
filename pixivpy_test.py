# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/9
from pixivpy_windows import *
import sys
import os

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cookies = {}

    # 本地无配置文件则创建
    if not os.path.exists('setting.ini'):
        config['user-setting'] = {'autoLogin': 'False',
                                  'savePath': '',
                                  'cookies': ''}
        with open('setting.ini', 'w') as configfile:
            config.write(configfile)

    config.read('setting.ini')
    # 若设置自动登录则直接读取本地cookie, 无则开启登录界面
    if config['user-setting']['autoLogin'] == 'True':
        local_cookies = config['user-setting']['cookies']
        # 将读取到的cookies从字典转化为requests能读取的对象类型
        cookies = {}
        for line in local_cookies.split(';'):
            name, value = line.split('=')
            cookies[name] = value
        cookies = requests.utils.cookiejar_from_dict(cookies)
    else:
        loginWindow = LoginWindow()
        if loginWindow.exec_():
            cookies = loginWindow.getCookies()

    mainWindow = MainWindow(cookies)
    mainWindow.show()
    sys.exit(app.exec_())
