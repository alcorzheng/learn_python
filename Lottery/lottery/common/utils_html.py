#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: HTML通用工具类

import requests

#伪装成浏览器登陆,获取网页源代码
def getPage(url,headers):
    try:
        req = requests.get(url, headers=headers)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        return req
    except requests.HTTPError as e:
        print(e)

# 获取URL
def getSSQURL(page_num):
    return 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_' + str(page_num) + '.html'

# 获取URL
def getDLTURL(page_num):
    if int(page_num)!=1:
        return 'http://www.lottery.gov.cn/historykj/history_' + str(page_num) + '.jspx?_ltype=dlt'
    else:
        return 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=dlt'

# 获取headers
def getHeaders():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    return headers
