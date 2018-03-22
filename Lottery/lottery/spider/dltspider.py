#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 大乐透开奖结果爬取

from bs4 import BeautifulSoup
from common import utils_html, utils, envparam, database, model_spider


# 获取url总页数
def getPageNum(url, headers):
    soup = BeautifulSoup(utils_html.getPage(url, headers).content, 'lxml')
    pagenums = soup.select('body > div.yyl > div.yylMain > div.result > div > div > select > option')
    if len(pagenums) > 0:
        return int(pagenums[-1].get_text().replace(',', ''))
    else:
        return 0

# 爬取大乐透开奖信息并插入数据库
def insDLTData():
    """爬取双色球开奖信息并插入数据库"""
    # 获取上次爬取的最大ID
    conn = database.CommonDBExecutor(database.getDefDBURL(), model_spider.lottery_cn_dlt)
    results = conn.query('select max(id_) max_id from data_analysis.lottery_cn_dlt')
    end_id = utils.obj2int(results[0]['max_id'])
    for list_num in range(1, getPageNum(utils_html.getDLTURL(1), utils_html.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = utils_html.getDLTURL(list_num)
        soup = BeautifulSoup(utils_html.getPage(url, utils_html.getHeaders()).content, 'lxml')
        list_dlt = soup.select('body > div.yyl > div.yylMain > div.result > table > tbody > tr')
        dltDatas = []
        for dlt in list_dlt:
            if int(dlt.select('td:nth-of-type(1)')[0].get_text().replace(',', '')) <= int(end_id):
                break
            data = {
                'id_': utils.obj2int(dlt.select('td:nth-of-type(1)')[0].get_text().replace(',', '')),
                'date_': dlt.select('td:nth-of-type(20)')[0].get_text(),
                'win_nums_red': ','.join([win_num.get_text() for win_num in dlt.select('td.red')]),
                'win_nums_blue': ','.join([win_num.get_text() for win_num in dlt.select('td.blue')]),
                'amount_': utils.obj2int(dlt.select('td:nth-of-type(18)')[0].get_text().replace(',', '').replace('-', '').strip()),
                'prize_first': utils.obj2int(dlt.select('td:nth-of-type(9)')[0].get_text().replace(',', '').strip()),
                'prize_second': utils.obj2int(dlt.select('td:nth-of-type(13)')[0].get_text().replace(',', '').strip())
            }
            dltDatas.append(data)
        if len(dltDatas) == 0:
            print("【大乐透】未爬取到符合条件数据！")
            break
            print("【大乐透】本次爬取到%s条符合条件数据！" % (len(dltDatas)))
        # 插入数据库
        conn.insert_by_batch(dltDatas)
