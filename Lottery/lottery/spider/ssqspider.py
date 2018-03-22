#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-14
# desc: 双色球开奖结果爬取

from bs4 import BeautifulSoup
from common import utils_html, utils, envparam, database, model_spider


# 获取url总页数
def getPageNum(url, headers):
    soup = BeautifulSoup(utils_html.getPage(url, headers).content, 'lxml')
    pagenums = soup.select('body > table > tr > td > p.pg > strong:nth-of-type(1)')
    if len(pagenums) > 0:
        return int(pagenums[0].get_text().replace(',', ''))
    else:
        return 0


def insSSQData():
    """爬取双色球开奖信息并插入数据库"""
    # 获取上次爬取的最大ID
    conn = database.CommonDBExecutor(database.getDefDBURL(), model_spider.lottery_cn_ssq)
    results = conn.query('select max(id_) max_id from data_analysis.lottery_cn_ssq')
    end_id = utils.obj2int(results[0]['max_id'])
    for list_num in range(1, getPageNum(utils_html.getSSQURL(1), utils_html.getHeaders())):  # 从第一页到第getPageNum(url)页
        url = utils_html.getSSQURL(list_num)
        soup = BeautifulSoup(utils_html.getPage(url, utils_html.getHeaders()).content, 'lxml')
        list_date_ = soup.select('body > table > tr > td:nth-of-type(1)')
        list_id_ = soup.select('body > table > tr > td:nth-of-type(2)')
        list_win_nums = soup.select('body > table > tr > td:nth-of-type(3)')
        list_amount_ = soup.select('body > table > tr > td:nth-of-type(4) > strong')
        list_prize_first = soup.select('body > table > tr > td:nth-of-type(5) > strong')
        list_prize_second = soup.select('body > table > tr > td:nth-of-type(6) > strong')
        ssqDatas = []
        for date_, id_, win_nums, amount_, prize_first, prize_second in zip(list_date_, list_id_, list_win_nums,
                                                                            list_amount_, list_prize_first,
                                                                            list_prize_second):
            if int(id_.get_text().replace(',', '')) <= int(end_id): break
            data = {
                'id_': utils.obj2int(id_.get_text().replace(',', '')),
                'date_': date_.get_text(),
                'win_nums_red': ','.join(list(win_nums.stripped_strings)[:-1]),
                'win_nums_blue': list(win_nums.stripped_strings)[-1],
                'amount_': utils.obj2int(amount_.get_text().replace(',', '').strip()),
                'prize_first': utils.obj2int(prize_first.get_text().replace(',', '').strip()),
                'prize_second': utils.obj2int(prize_second.get_text().replace(',', '').strip())
            }
            ssqDatas.append(data)
        if len(ssqDatas) == 0:
            print("【双色球】未爬取到符合条件数据！")
            break
        print("【双色球】本次爬取到%s条符合条件数据！" % (len(ssqDatas)))
        # 插入数据库
        conn.insert_by_batch(ssqDatas)
