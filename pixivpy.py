# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/7
import requests
import re
import os
import datetime
from bs4 import BeautifulSoup, SoupStrainer
# 排行榜默认下载文件数
RANKING_NUM = 20


# -----------------------------------------------
# 输出字符颜色表
# 格式：\033[显示方式;前景色;背景色m
# 30 40 黑色 | 34 44 蓝色   | 终端默认设置0 高亮显示1 使用下划线4
# 31 41 红色 | 35 45 紫红色 | 闪烁5 反白显示7 不可见8
# 32 42 绿色 | 36 46 青蓝色 |
# 33 43 黃色 | 37 47 白色   |
# -----------------------------------------------
def printColor(content, color='WHITE', style=0):
    colorSwitch = {'BLACK': '30', 'RED': '31', 'GREEN': '32', 'YELLOW': '33',
                   'BLUE': '34', 'PURPLE': '35', 'LIGHTBLUE': '36', 'WHITE': '38'}
    color_num = colorSwitch.get(color, '')
    # 样式选择:0无样式 1高亮 2下划线 3反白
    styleSwitch = {0: '', 1: '1;', 2: '4;', 3: '7;'}
    s = styleSwitch.get(style, '')
    begin = '\033[' + s + color_num + 'm'
    end = '\033[0m'
    print(begin + content + end)
    return


# 登录操作 返回cookies
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
        printColor('请依次输入账号与密码', 'RED')
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


# 取得排行榜信息并下载
def ranking(num=RANKING_NUM, mode='daily', multi=False):
    url = 'http://www.pixiv.net/ranking.php?mode=' + mode
    req = requests.get(url)
    assert req.status_code == 200, '链接异常'
    # 这个正则匹配hhhh
    ids_pattern = re.compile(r'(?<="\sdata-id=")\d+(?=">)')
    data_ids = re.findall(ids_pattern, req.text)
    save_ranking_img(data_ids[:num], mode, multi)
    return


# 下载排行榜图片
def save_ranking_img(ids, mode, multi):
    referer = 'http://www.pixiv.net/ranking.php?mode=' + mode
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36 '
    }
    # 登录
    my_cookies = login()
    # 创建一个会话对象
    s = requests.Session()
    s.headers = headers
    s.cookies = requests.utils.cookiejar_from_dict(my_cookies)
    # 获取当天日期
    today = datetime.datetime.now().today().strftime("%Y-%m-%d")

    printColor('开始爬取id,请稍后...', 'LIGHTBLUE')
    originals = []
    for item_id in ids:
        item_url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + item_id
        req = s.get(item_url)
        original_pattern = re.compile(r'(?<=data-src=")\S*(?="\sclass="original-image")')
        original_url = re.findall(original_pattern, req.text)
        # 如果是多P作品的话
        if not original_url:
            if not multi:
                originals.append('')
                continue
            item_url = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=' + item_id
            req = s.get(item_url)
            # 为了匹配到原图 写这么长我也很无奈啊...
            original_url_pattern = re.compile(
                r'(?<=href=")\S*(?="\starget="_blank"\sclass="full-size-container _ui-tooltip")'
            )
            original_item_urls = re.findall(original_url_pattern, req.text)
            original_url = []
            for original_item_url in original_item_urls:
                original_item_url = 'http://www.pixiv.net' + original_item_url
                req = s.get(original_item_url)
                original_pattern = re.compile(r'(?<=src=")\S*(?=")')
                original_url.append(re.findall(original_pattern, req.text)[0])
            originals.append(original_url)
        else:
            originals.append(original_url[0])
    printColor('id爬取完毕', 'LIGHTBLUE')
    printColor('开始下载图片', 'LIGHTBLUE')
    download_path = os.path.join('dailyimg', today)
    if mode == 'daily':
        # 创建对应日期的目录
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            printColor(today+'文件夹创建成功', 'LIGHTBLUE')
        else:
            printColor(today+'文件夹已存在', 'YELLOW')
        for original in originals:
            index = originals.index(original)
            if original == '':
                continue
            if isinstance(original, list):
                list_name = os.path.join(download_path, '#'+str(index+1)+'_id='+ids[index])
                # 创建多P作品的文件夹
                if not os.path.exists(list_name):
                    os.mkdir(list_name)
                i = 1
                for p in original:
                    pic = s.get(p)
                    format_pattern = re.compile(r'\.png')
                    if re.search(format_pattern, p):
                        img_format = '.png'
                    else:
                        img_format = '.jpg'
                    name = os.path.join(list_name, str(i)+img_format)
                    with open(name, 'wb') as f:
                        f.write(pic.content)
                    i += 1
            else:
                pic = s.get(original)
                format_pattern = re.compile(r'\.png')
                if re.search(format_pattern, original):
                    img_format = '.png'
                else:
                    img_format = '.jpg'
                name = os.path.join(download_path, '#'+str(index+1)+'_id='+ids[index]+img_format)
                with open(name, 'wb') as f:
                    f.write(pic.content)
            printColor(ids[index]+' done', 'GREEN')


if __name__ == '__main__':
    intro = '''
================================================
 ____ _____  _______     ________   __
|  _ \_ _\ \/ /_ _\ \   / /  _ \ \ / /
| |_) | | \  / | | \ \ / /| |_) \ V /
|  __/| | /  \ | |  \ V / |  __/ | |
|_|  |___/_/\_\___|  \_/  |_|    |_|    by:DoSun
================================================
模式选择:
1. 下载每日排行榜
    '''
    printColor(intro, 'PURPLE', 1)
    mode = input('输入选择: ')
    if mode == '1':
        num = input('下载前几名[默认前20]: ')
        multi_mode = input('下载多P作品吗[y/n]: ')
        if multi_mode == 'Y' or multi_mode == 'y':
            multi = True
        else:
            multi = False
        ranking(num=int(num), mode='daily', multi=multi)
