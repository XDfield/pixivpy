Pixivpy
=======
一个pixiv的简单爬虫脚本(GUI版)
.. image:: https://img.shields.io/badge/python-3.5-blue.svg

Features
--------
- 批量下载(每日、每周等)榜单的图片(原图)

Requirements
------------

- requests
- PyQt5

LoginActivity
-------------
.. image:: https://raw.githubusercontent.com/XDfield/pixivpy/master/README_PIC/%E7%99%BB%E9%99%86%E7%95%8C%E9%9D%A2%E6%88%AA%E5%9B%BE.png

Change Log
----------
:2017/03/09
 - 尝试了下PyQt5制作了个登陆界面,多P下载功能暂取消待测试
:2017/03/08
 - 完善排行榜分类选择(每日,每周,每月等)
:2017/03/07
 - 下载每日排行榜功能,支持多P作品下载
:2017/03/06
 - 实现了模拟登录,保存或读取本地cookies

Todo list
---------
 - 添加国际排行榜与地区排行榜选择
 - 下载特定id的作品
 - 使用异步下载方式,提高效率
 - 完善GUI,怕不是个大坑...


