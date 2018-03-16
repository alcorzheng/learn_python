#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 双色球开奖结果爬取

import psycopg2
from bs4 import BeautifulSoup
from Lottery.lottery.util import HTMLUtil,DBUtil,BaseUtil

# 获取url总页数
def getPageNum(url,headers):
    soup = BeautifulSoup(HTMLUtil.getPage(url,headers).content,'lxml')
    pagenums = soup.select('body > table > tr > td > p.pg > strong:nth-of-type(1)')
    if len(pagenums)>0:
        return int(pagenums[0].get_text().replace(',',''))
    else:
        return 0

# 爬取双色球开奖信息并插入数据库
def insSSQData():
    # 连接数据库
    conn = psycopg2.connect(DBUtil.getJDBCURL().get('jdbcurl'))
    # 创建cursor以访问数据库
    cursor = conn.cursor()
    # 获取上次爬取的最大ID
    end_id = 0
    cursor.execute('select max(id_) from data_analysis.lottery_cn_ssq')
    results = cursor.fetchone()
    if results[0] is not None:end_id = int(results[0])
    for list_num in range(1, getPageNum(HTMLUtil.getSSQURL(1),HTMLUtil.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = HTMLUtil.getSSQURL(list_num)
        soup = BeautifulSoup(HTMLUtil.getPage(url, HTMLUtil.getHeaders()).content,'lxml')
        list_date_ = soup.select('body > table > tr > td:nth-of-type(1)')
        list_id_ = soup.select('body > table > tr > td:nth-of-type(2)')
        list_win_nums = soup.select('body > table > tr > td:nth-of-type(3)')
        list_amount_ = soup.select('body > table > tr > td:nth-of-type(4) > strong')
        list_prize_first = soup.select('body > table > tr > td:nth-of-type(5) > strong')
        list_prize_second = soup.select('body > table > tr > td:nth-of-type(6) > strong')
        ssqDatas = []
        for date_, id_, win_nums, amount_, prize_first, prize_second in zip(list_date_, list_id_, list_win_nums, list_amount_, list_prize_first, list_prize_second):
            if int(id_.get_text().replace(',','')) <= int(end_id) : break
            data = (
                BaseUtil.obj2int(id_.get_text().replace(',','')),
                date_.get_text(),
                ','.join(list(win_nums.stripped_strings)[:-1]),
                list(win_nums.stripped_strings)[-1],
                BaseUtil.obj2int(amount_.get_text().replace(',','').strip()),
                BaseUtil.obj2int(prize_first.get_text().replace(',','').strip()),
                BaseUtil.obj2int(prize_second.get_text().replace(',','').strip())
            )
            ssqDatas.append(data)
        if len(ssqDatas) == 0 : break
        #print(ssqDatas)
        # 插入数据库
        records_list_template = ','.join(['%s'] * len(ssqDatas))
        insert_query = 'INSERT INTO data_analysis.lottery_cn_ssq(id_, date_, win_nums_red, win_nums_blue, amount_, prize_first, prize_second) VALUES {}'.format(records_list_template)
        cursor.execute(insert_query, ssqDatas)
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()