#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: lottery_cn_ssq.py
@time: 2018/4/1013:59
@desc: 
"""

from requests_html import HTMLSession

session = HTMLSession()

def spiders_data():
    """"按照规则爬取数据"""
    response = session.get('http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html')
    content = response.html.find('.wqhgt', first=True)
    tr_list = content.lxml.find('tr')
    for tr in tr_list:
        print(tr.attrs)


if __name__ == '__main__':
    spiders_data()
