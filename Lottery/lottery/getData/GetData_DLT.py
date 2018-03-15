#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 大乐透开奖结果收集

from bs4 import BeautifulSoup
from ..util import HTMLUtil

# 获取url总页数
def getPageNum(url,headers):
    soup = BeautifulSoup(HTMLUtil.getPage(url,headers).content,'lxml')
    pagenums = soup.select('body > div.yyl > div.yylMain > div.result > div > div > select > option')
    if len(pagenums)>0:
        return int(pagenums[-1].get_text().replace(',',''))
    else:
        return 0

# 获取大乐透的信息
def getDLTData():
    dltDatas = []
    for list_num in range(1, getPageNum(HTMLUtil.getDLTURL(1),HTMLUtil.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = HTMLUtil.getDLTURL(list_num)
        soup = BeautifulSoup(HTMLUtil.getPage(url, HTMLUtil.getHeaders()).content,'lxml')
        list_dlt = soup.select('body > div.yyl > div.yylMain > div.result > table > tbody > tr')
        for dlt in list_dlt:
            data = {
                'id_': dlt.select('td:nth-of-type(1)')[0].get_text(),
                'date_': dlt.select('td:nth-of-type(20)')[0].get_text(),
                'win_nums_r': ','.join([win_num.get_text() for win_num in dlt.select('td.red')]),
                'win_nums_b': ','.join([win_num.get_text() for win_num in dlt.select('td.blue')]),
                'amounts_': dlt.select('td:nth-of-type(18)')[0].get_text().replace(',','').replace('-','').strip(),
                'prize_first': dlt.select('td:nth-of-type(9)')[0].get_text().replace(',','').strip(),
                'prize_second': dlt.select('td:nth-of-type(13)')[0].get_text().replace(',','').strip()
            }
            dltDatas.append(data)
    return dltDatas