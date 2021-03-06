# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/7
import requests
import re
import os
import aiohttp
import asyncio


# 排行榜默认下载文件数
RANKING_NUM = 5


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
        post_key_pattern = re.compile(r'(?<=name="post_key"\svalue=")\S*(?=">)')
        post_key = re.findall(post_key_pattern, re1.text)[0]
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


# 取得排行榜信息
def ranking(num, mode, cookies):
    url = 'http://www.pixiv.net/ranking.php?mode=' + mode
    req = requests.get(url, cookies=cookies)
    assert req.status_code == 200, '链接异常'
    # 这个正则匹配hhhh
    ids_pattern = re.compile(r'(?<="\sdata-id=")\d+(?=">)')
    ids = re.findall(ids_pattern, req.text)
    date_pattern = re.compile(r'(?<=class="current">)\d+\S*(?=</a>)')
    date = re.findall(date_pattern, req.text)[0]
    work_class_pattern = re.compile(r'(?<=class=")work\s\s_work\s(multiple\s)?(?=")')
    work_classes = re.findall(work_class_pattern, req.text)
    work_class = []
    for work_type in work_classes:
        if work_type == 'multiple ':
            work_class.append(1)
        else:
            work_class.append(0)
    return ids[:num], date, work_class[:num]


@asyncio.coroutine
async def get_ids_Page(url, mode, cookies, req_list):
    referer = 'http://www.pixiv.net/ranking.php?mode=' + mode
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36 '
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, headers=headers) as resp:
            assert resp.status == 200
            req_list.append(await resp.text())


# 异步下载排行榜图片
def save_ranking_img_aio(ids, work_class, mode, multi, cookies, date_name):
    printColor('采用异步模式,开始爬取,请稍后...', 'LIGHTBLUE')
    url1 = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    url2 = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id='
    # 分开多P和单P作品:
    one_urls = []
    multi_urls = []
    index = 0
    for work_type in work_class:
        if work_type:
            multi_urls.append(url2+ids[index])
        else:
            one_urls.append(url1+ids[index])
        index += 1
    loop = asyncio.get_event_loop()
    one_req_list = []
    multi_req_list = []
    tasks = [get_ids_Page(host, mode, cookies, one_req_list) for host in one_urls]
    if multi:
        multi_tasks = [get_ids_Page(host, mode, cookies, multi_req_list) for host in multi_urls]
        tasks.extend(multi_tasks)
    # 获得所有作品页面的响应内容
    loop.run_until_complete(asyncio.wait(tasks))

    # 单P作品的原图链接提取
    one_originals = []
    one_original_pattern = re.compile(r'(?<=data-src=")\S*(?="\sclass="original-image")')
    for one_req in one_req_list:
        original_url = re.findall(one_original_pattern, one_req)
        one_originals.append(original_url[0])
    # 多P作品的原图链接提取
    multi_originals = []
    if multi:
        multi_original_url_pattern = re.compile(
            r'(?<=href=")\S*(?="\starget="_blank"\sclass="full-size-container _ui-tooltip")'
        )
        original_pattern = re.compile(r'(?<=src=")\S*(?=")')
        for multi_req in multi_req_list:
            # 单个多P作品中,单张图片的展示地址匹配
            multi_original_item_urls = re.findall(multi_original_url_pattern, multi_req)
            multi_original_item_urls = ['http://www.pixiv.net' + each_url for each_url in multi_original_item_urls]
            req_list = []
            tasks = [get_ids_Page(host, mode, cookies, req_list) for host in multi_original_item_urls]
            loop.run_until_complete(asyncio.wait(tasks))
            urls = []
            for req in req_list:
                urls.append(re.findall(original_pattern, req)[0])
            multi_originals.append(urls)
    else:
        for i in range(len(multi_urls)):
            multi_originals.append('')
    printColor('爬取完毕 其中' + str(len(multi_urls)) + '个多P作品', 'LIGHTBLUE')

    printColor('开始下载图片', 'LIGHTBLUE')
    mode_path = mode + '_img'
    download_path = os.path.join(mode_path, date_name)

    # 创建对应日期的目录
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        printColor(date_name + '文件夹已存在', 'YELLOW')

    # 原图链接整合
    all_original_urls = []
    for work_type in work_class:
        if work_type:
            all_original_urls.append(multi_originals[0])
            del multi_originals[0]
        else:
            all_original_urls.append(one_originals[0])
            del one_originals[0]

    for url in all_original_urls:
        print(url)

    return

    # 下载
    for original in originals:
        index = originals.index(original)
        if original == '':
            continue
        if isinstance(original, list):
            list_name = os.path.join(download_path, '#' + str(index + 1) + '_id=' + ids[index])
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
                name = os.path.join(list_name, str(i) + img_format)
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
            name = os.path.join(download_path, '#' + str(index + 1) + '_id=' + ids[index] + img_format)
            with open(name, 'wb') as f:
                f.write(pic.content)
        printColor(ids[index] + ' done', 'GREEN')
    printColor('下载完成', 'LIGHTBLUE')


def save_ranking_img(ids, work_class, mode, multi, cookies, date_name):
    referer = 'http://www.pixiv.net/ranking.php?mode=' + mode
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36 '
    }
    # 创建一个会话对象
    s = requests.Session()
    s.headers = headers
    s.cookies = requests.utils.cookiejar_from_dict(cookies)

    printColor('开始爬取,请稍后...', 'LIGHTBLUE')
    originals = []
    multi_num = 0
    for item_id in ids:
        item_url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + item_id
        req = s.get(item_url)
        original_pattern = re.compile(r'(?<=data-src=")\S*(?="\sclass="original-image")')
        original_url = re.findall(original_pattern, req.text)
        # 如果是多P作品的话
        if not original_url:
            multi_num += 1
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
    printColor('爬取完毕 其中' + str(multi_num) + '个多P作品', 'LIGHTBLUE')

    printColor('开始下载图片', 'LIGHTBLUE')
    mode_path = mode + '_img'
    download_path = os.path.join(mode_path, date_name)

    # 创建对应日期的目录
    if not os.path.exists(download_path):
        os.makedirs(download_path)

        printColor(date_name + '文件夹已存在', 'YELLOW')
    # 下载
    for original in originals:
        index = originals.index(original)
        if original == '':
            continue
        if isinstance(original, list):
            list_name = os.path.join(download_path, '#' + str(index + 1) + '_id=' + ids[index])
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
                name = os.path.join(list_name, str(i) + img_format)
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
            name = os.path.join(download_path, '#' + str(index + 1) + '_id=' + ids[index] + img_format)
            with open(name, 'wb') as f:
                f.write(pic.content)
        printColor(ids[index] + ' done', 'GREEN')
    printColor('下载完成', 'LIGHTBLUE')


if __name__ == '__main__':
    logo = '''
=======================================================
  ====== ____ _____  _______     ________   __======
    ====|  _ \_ _\ \/ /_ _\ \   / /  _ \ \ / /====
      ==| |_) | | \  / | | \ \ / /| |_) \ V / ==
       =|  __/| | /  \ | |  \ V / |  __/ | |  =
        |_|  |___/_/\_\___|  \_/  |_|    |_|
                                            by:DoSun'''
    intro = '''模式选择:(无输入则退出)
daily(-r18)  --每日排行榜     weekly(_r18) --每周排行榜
monthly      --每月排行榜     rookie       --新人排行榜
male(_r18)   --男性向排行榜   female(_r18) --女性向排行榜
original     --原创排行榜
'''
    printColor(logo, 'BLUE', 1)
    printColor(intro, 'PURPLE', 1)
    # 登录取得cookies
    my_cookies = login()
    while True:
        mode = input('输入选择: ')
        # 无输入就退出
        if mode == '':
            break
        num = input('下载前几名[默认前5]: ')
        multi_mode = input('下载多P作品吗[y/n]: ')
        if multi_mode == 'Y' or multi_mode == 'y':
            multi = True
        else:
            multi = False
        if num == '':
            num = RANKING_NUM
        num = int(num)
        ids, date, work_class = ranking(num, mode, my_cookies)
        save_ranking_img_aio(ids, work_class, mode, multi, my_cookies, date)
