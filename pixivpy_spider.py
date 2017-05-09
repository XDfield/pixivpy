# -*- coding: utf-8 -*-
# Created by DoSun on 2017/3/9
import aiohttp
import asyncio
import grequests
import os
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer


# 登录操作用到的两个链接
index_url = 'http://www.pixiv.net/'
login_url1 = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url2 = 'https://accounts.pixiv.net/api/login?lang=zh'
ranking_url = 'http://www.pixiv.net/ranking.php?mode='


def getMediumOriginalUrl(resp):
    original_only = SoupStrainer(class_='original-image')
    soup = BeautifulSoup(resp.text, 'lxml', parse_only=original_only)
    original_url = soup.find('img')['data-src']
    return original_url


def getMangaOriginalUrl(resp):
    pass


def saveImg(data, info_list, path):
    # 判断格式
    format_pattern = re.compile(r'\.(png|PNG)')
    if re.search(format_pattern, info_list[0]):
        saveName = '#'+info_list[2]+'_id='+info_list[1]+'.png'
    else:
        saveName = '#'+info_list[2]+'_id='+info_list[1]+'.jpg'
    savePath = os.path.join(path, saveName)
    with open(savePath, 'wb') as f:
        f.write(data)


class PixivPy:
    """爬虫类"""
    def __init__(self):
        self.pixiv_id = ''
        self.password = ''
        self.cookies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36 '
        }
        self.username = ''
        self.id = ''
        self.user_link = index_url + '/member.php?id='
        self.mode = 'daily'
        self.r18 = False
        self.moreP = False
        self.savePath = ''
        self.ranking_items_info = []

    def login(self):
        """执行后进行登陆,返回一个布尔值(是否登陆成功)和一个字符串(登陆界面提示信息)"""
        # 构造headers
        headers = self.headers
        headers['Referer'] = \
            'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        with requests.session() as s:
            s.headers = headers
            rep1 = s.get(login_url1)
            # 获取post_key
            soup = BeautifulSoup(rep1.content, 'lxml', parse_only=SoupStrainer(id='old-login'))
            post_key = soup.find('input', attrs={'name': 'post_key'})['value']
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
            rep2 = s.post(login_url2, data=data)
            text = rep2.text
        # 登陆情况分析
        success_pattern = re.compile(r'"success"')
        if re.search(success_pattern, text):
            self.cookies = s.cookies
            local_cookies = ';'.join('='.join(item) for item in s.cookies.items())
            return True, '登陆成功', local_cookies
        captcha_error_pattern = re.compile(r'"captcha"|"pixiv_id"')
        if re.search(captcha_error_pattern, text):
            return False, '请确认您所输入的账号与密码是否正确', {}
        lock_error_pattern = re.compile(r'"lock"')
        if re.search(lock_error_pattern, text):
            return False, '您的账号被封锁请稍后再试'
        return False, '登陆异常', {}

    def setLoginInfo(self, pixiv_id, password):
        """设置登陆信息(id与密码),接收两个参数(id与密码)"""
        self.pixiv_id = pixiv_id
        self.password = password

    def getUserInfo(self):
        """获取用户头像和用户名"""
        with requests.session() as session:
            session.headers = self.headers
            session.cookies = self.cookies
            # print(type(self.cookies))
            # print(self.cookies)
            rep1 = session.get(url=index_url)
            assert rep1.status_code == 200
            # 取得用户名
            soup = BeautifulSoup(rep1.text, 'lxml')
            self.username = soup.find('h1', attrs={'class': 'user'}).get_text()
            # print(self.username)
            # 取得个人id
            id_pattern = re.compile(r'(?<=pixiv\.user\.id\s=\s")\d+(?=")')
            self.id = re.findall(id_pattern, rep1.text)[0]
            self.user_link += self.id

            rep2 = session.get(url=self.user_link)
            assert rep2.status_code == 200
            image_soup = BeautifulSoup(rep2.text, 'lxml', parse_only=SoupStrainer(class_='user-link'))
            image_src = image_soup.find('img', attrs={'class': 'user-image'})['src']
            # print('头像地址:'+image_src)

            headers = self.headers
            headers['Referer'] = self.user_link
            rep3 = session.get(url=image_src, headers=headers)
            assert rep3.status_code == 200
            with open('user-image.jpg', 'wb') as f:
                f.write(rep3.content)

    def getRankingInfo(self, num):
        url = ranking_url + self.mode
        req = requests.get(url=url, cookies=self.cookies)
        assert req.status_code == 200
        main_soup = BeautifulSoup(req.text, 'lxml', parse_only=SoupStrainer(class_='layout-body'))
        # 获取排行榜时间
        date_soup = main_soup.find_all('ul', attrs={'class': 'sibling-items'})[0]
        date = date_soup.find('a', attrs={'class': 'current'}).get_text()
        # 获取作品集合
        sections = main_soup.find_all('section', attrs={'class': 'ranking-item'})
        if num < len(sections):
            sections = sections[:num]
        # 获取各项信息
        ids = []
        ranks = []
        titles = []
        authors = []
        work_classes = []
        for section in sections:
            ids.append(section['data-id'])
            ranks.append(section['data-rank'])
            titles.append(section['data-title'])
            authors.append(section['data-user-name'])
            work_class = section.find('div', attrs={'class': 'ranking-image-item'}).find('a')['class']
            if work_class == ['work', '_work', '']:
                work_classes.append('medium')
            else:
                work_classes.append('manga')
        all_works = []
        for i in range(num):
            if not self.moreP:
                if work_classes[i] == 'manga':
                    continue
            new_work = [ids[i], ranks[i], titles[i], authors[i], work_classes[i]]
            all_works.append(new_work)
        self.ranking_items_info = [date, all_works]
        # print(self.ranking_items_info)

    def saveRankingImg(self):
        # 创建主文件夹
        main_path = os.path.join(self.savePath, 'Pixivpy')
        if not os.path.exists(main_path):
            os.mkdir(main_path)
        # 创建模式文件夹
        mode_path = os.path.join(main_path, self.mode+'img')
        if not os.path.exists(mode_path):
            os.mkdir(mode_path)
        # 创建日期文件夹
        date_path = os.path.join(mode_path, self.ranking_items_info[0])
        if not os.path.exists(date_path):
            os.mkdir(date_path)
        # 下载图片
        self.getOriginalImg(date_path)

    def getOriginalImg(self, path):
        originals = []
        medium_urls = []
        manga_urls = []
        tasks = []
        referer = 'http://www.pixiv.net/ranking.php?mode=' + self.mode
        headers = self.headers
        headers['Referer'] = referer
        for i in self.ranking_items_info[1]:
            if not i:
                break
            url = 'http://www.pixiv.net/member_illust.php?mode='+i[4]+'&illust_id='+i[0]
            if i[4] == 'medium':
                medium_urls.append([url, i[0], i[1]])
            else:
                manga_urls.append([url, i[0], i[1]])
        rs = (grequests.get(u[0], headers=headers, cookies=self.cookies) for u in medium_urls)
        rs_list = grequests.map(rs)
        mediums = []
        for i in range(len(rs_list)):
            # 原图链接 id 排名
            mediums.append([getMediumOriginalUrl(rs_list[i]), medium_urls[i][1], medium_urls[i][2]])
        img_rs = (grequests.get(u[0], headers=headers, cookies=self.cookies) for u in mediums)
        img_rs_list = grequests.map(img_rs)
        for i in range(len(img_rs_list)):
            saveImg(img_rs_list[i].content, mediums[i], path)
