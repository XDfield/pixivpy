# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/7
import requests
import os
from bs4 import BeautifulSoup, SoupStrainer


def login():
    # 登录操作用到的两个链接
    login_url1 = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    login_url2 = 'https://accounts.pixiv.net/api/login?lang=zh'

    if os.path.exists('cookies.txt'):
        # 如果有本地cookies的话直接读取
        cookies = {}
        with open('cookies.txt', 'r') as f:
            for line in f.read().split(';'):
                name, value = line.split('=')
                cookies[name] = value
        # 返回cookies
        return cookies
    else:
        # 没有本地cookies的话重新登录
        print('请依次输入账号与密码')
        pixiv_id = input('pixiv_id: ')
        password = input('password: ')
        # 创建一个会话对象实现向同一主机发送多个请求同时保持cookie
        s = requests.Session()
        # 构造headers
        headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36 '
        }
        # 获取post_key
        re1 = s.get(url=login_url1, headers=headers)
        soup = BeautifulSoup(re1.content, 'lxml', parse_only=SoupStrainer(attrs={'name': 'post_key'}))
        post_key = soup.find('input')['value']
        # 构造data
        data = {
            'pixiv_id': pixiv_id,
            'password': password,
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': post_key,
            'source': 'pc',
        }
        # 进行登录
        re2 = s.post(url=login_url2, data=data)
        # 如果返回的状态码不是200那就是有问题了
        assert re2.status_code == 200, '登录异常'
        # 保存为本地cookies
        local_cookies = ';'.join('='.join(item) for item in s.cookies.items())
        with open('cookies.txt', 'w') as f:
            f.write(local_cookies)
        # 返回cookies
        cookies = {}
        for line in local_cookies.split(';'):
            name, value = line.split('=')
            cookies[name] = value
        return cookies


if __name__ == '__main__':
    # 登录
    my_cookies = login()
    print(my_cookies)
