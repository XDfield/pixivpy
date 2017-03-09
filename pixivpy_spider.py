# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/9
import requests
import re

# 登录操作用到的两个链接
login_url1 = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url2 = 'https://accounts.pixiv.net/api/login?lang=zh'


class PixivPy:
    def __init__(self):
        self.pixiv_id = ''
        self.password = ''
        self.login_status_code = 200
        self.session = requests.Session()

    # 登陆方法
    def login(self):
        # 构造headers
        headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36 '
        }
        # 获取post_key
        re1 = self.session.get(url=login_url1, headers=headers)
        post_key_pattern = re.compile(r'(?<=name="post_key"\svalue=")\S*(?=">)')
        post_key = re.findall(post_key_pattern, re1.text)[0]
        # 构造data
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': post_key,
            'source': 'pc',
        }
        # 进行登录
        re2 = self.session.post(url=login_url2, data=data)
        text = re2.text
        # 登陆情况分析
        success_pattern = re.compile(r'"success"')
        if re.search(success_pattern, text):
            return True, '登陆成功'
        captcha_error_pattern = re.compile(r'"captcha"|"pixiv_id"')
        if re.search(captcha_error_pattern, text):
            return False, '请确认您所输入的账号与密码是否正确'
        lock_error_pattern = re.compile(r'"lock"')
        if re.search(lock_error_pattern, text):
            return False, '您的账号被封锁请稍后再试'
        return False, '登陆异常'

    # 设置登陆信息
    def setLoginInfo(self, pixiv_id, password):
        self.pixiv_id = pixiv_id
        self.password = password
