#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 大乐透开奖结果爬取

import psycopg2
from bs4 import BeautifulSoup
from ..util import HTMLUtil
from ..util import DBUtil
from ..util import BaseUtil

# 获取url总页数
def getPageNum(url,headers):
    soup = BeautifulSoup(HTMLUtil.getPage(url,headers).content,'lxml')
    pagenums = soup.select('body > div.yyl > div.yylMain > div.result > div > div > select > option')
    if len(pagenums)>0:
        return int(pagenums[-1].get_text().replace(',',''))
    else:
        return 0

# 爬取大乐透开奖信息并插入数据库
def insDLTData():
    # 连接数据库
    conn = psycopg2.connect(DBUtil.getJDBCURL().get('jdbcurl'))
    # 创建cursor以访问数据库
    cursor = conn.cursor()
    # 获取上次爬取的最大ID
    end_id = 0
    cursor.execute('select max(id_) from data_analysis.lottery_cn_dlt')
    results = cursor.fetchone()
    if results[0] is not None:end_id = int(results[0])
    for list_num in range(1, getPageNum(HTMLUtil.getDLTURL(1),HTMLUtil.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = HTMLUtil.getDLTURL(list_num)
        soup = BeautifulSoup(HTMLUtil.getPage(url, HTMLUtil.getHeaders()).content,'lxml')
        list_dlt = soup.select('body > div.yyl > div.yylMain > div.result > table > tbody > tr')
        dltDatas = []
        for dlt in list_dlt:
            if int(dlt.select('td:nth-of-type(1)')[0].get_text().replace(',', '')) <= int(end_id): break
            data = (
                BaseUtil.obj2int(dlt.select('td:nth-of-type(1)')[0].get_text().replace(',', '')),
                dlt.select('td:nth-of-type(20)')[0].get_text(),
                ','.join([win_num.get_text() for win_num in dlt.select('td.red')]),
                ','.join([win_num.get_text() for win_num in dlt.select('td.blue')]),
                BaseUtil.obj2int(dlt.select('td:nth-of-type(18)')[0].get_text().replace(',','').replace('-','').strip()),
                BaseUtil.obj2int(dlt.select('td:nth-of-type(9)')[0].get_text().replace(',','').strip()),
                BaseUtil.obj2int(dlt.select('td:nth-of-type(13)')[0].get_text().replace(',','').strip())
            )
            dltDatas.append(data)
        if len(dltDatas) == 0 : break
        #print(ssqDatas)
        # 插入数据库
        records_list_template = ','.join(['%s'] * len(dltDatas))
        insert_query = 'INSERT INTO data_analysis.lottery_cn_dlt(id_, date_, win_nums_red, win_nums_blue, amount_, prize_first, prize_second) VALUES {}'.format(records_list_template)
        cursor.execute(insert_query, dltDatas)
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()
