#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 双色球开奖结果收集

from bs4 import BeautifulSoup
from ..util import HTMLUtil

# 获取url总页数
def getPageNum(url,headers):
    soup = BeautifulSoup(HTMLUtil.getPage(url,headers).content,'lxml')
    pagenums = soup.select('body > table > tr > td > p.pg > strong:nth-of-type(1)')
    if len(pagenums)>0:
        return int(pagenums[0].get_text().replace(',',''))
    else:
        return 0

# 获取双色球的信息
def getSSQData():
    ssqDatas = []
    for list_num in range(1, getPageNum(HTMLUtil.getSSQURL(1),HTMLUtil.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = HTMLUtil.getSSQURL(list_num)
        soup = BeautifulSoup(HTMLUtil.getPage(url, HTMLUtil.getHeaders()).content,'lxml')
        list_date_ = soup.select('body > table > tr > td:nth-of-type(1)')
        list_id_ = soup.select('body > table > tr > td:nth-of-type(2)')
        list_win_nums = soup.select('body > table > tr > td:nth-of-type(3)')
        list_amount_ = soup.select('body > table > tr > td:nth-of-type(4) > strong')
        list_prize_first = soup.select('body > table > tr > td:nth-of-type(5) > strong')
        list_prize_second = soup.select('body > table > tr > td:nth-of-type(6) > strong')

        for date_, id_, win_nums, amount_, prize_first, prize_second in zip(list_date_, list_id_, list_win_nums, list_amount_, list_prize_first, list_prize_second):
            data = {
                'id_': id_.get_text(),
                'date_': date_.get_text(),
                'win_nums_r': ','.join(list(win_nums.stripped_strings)[:-1]),
                'win_nums_b': list(win_nums.stripped_strings)[-1],
                'amounts_': amount_.get_text().replace(',','').strip(),
                'prize_first': prize_first.get_text().replace(',','').strip(),
                'prize_second': prize_second.get_text().replace(',','').strip()
            }
            ssqDatas.append(data)
    return ssqDatas