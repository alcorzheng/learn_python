#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: finance_eth.py
@time: 2018/4/315:24
@desc: ETH钱包地址财务统计
"""

import requests
from bs4 import BeautifulSoup


def cal_ethorses():
    # 以太马地址
    ethorses_address = '0xf1c38359ffec224cb5de98f981dd79ab749f8ed0'
    balance_data = _get_balance(ethorses_address)
    trans_datas = _get_trans(ethorses_address)
    account_info = {
        'address': ethorses_address,
        'balance': float(balance_data),
        'invest': 0,
        'trans_in_by_cal': 0,
        'trans_out': 0,
        'trans_outtx': 0
    }
    for trans_data in trans_datas:
        if trans_data['trans_direction'] == 'OUT':
            account_info['trans_out'] += float(trans_data['trans_value'])
            account_info['trans_outtx'] += float(trans_data['trans_txfee'])
        elif trans_data['trans_direction'] == 'IN':
            account_info['invest'] += float(trans_data['trans_value'])
    account_info['trans_in_by_cal'] = \
        account_info['trans_out'] + account_info['trans_outtx'] - account_info['balance'] - account_info['invest']
    for key in account_info:
        print(str(key) + ' : ' + str(account_info[key]))


def _getheaders():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    return headers


def _get_balance_url(eth_address):
    return 'https://etherscan.io/address/' + str(eth_address)


def _get_trans_url(eth_address, page_num):
    return 'https://etherscan.io/txs?a=' + str(eth_address) + '&p=' + str(page_num)


def _getpage(url, headers, proxy=None):
    try:
        req = requests.get(url, headers=headers, proxies=proxy)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        return req
    except requests.HTTPError as e:
        print(e)


def _get_balance(eth_address):
    url = _get_balance_url(eth_address)
    soup = BeautifulSoup(_getpage(url, _getheaders()).content, 'lxml')
    balance_data = soup.select(
        '#ContentPlaceHolder1_divSummary > div:nth-of-type(1) > table > tr:nth-of-type(1) > td:nth-of-type(2)'
    )
    if len(balance_data) > 0:
        return balance_data[0].get_text().replace(' Ether', '').strip()
    else:
        return 0


def _get_trans(eth_address):
    trans_datas = []
    for pagenum in range(1, _get_trans_pagenum(eth_address, _getheaders()) + 1):  # 从第一页到第getPageNum(url)页
        url = _get_trans_url(eth_address, pagenum)
        soup = BeautifulSoup(_getpage(url, _getheaders()).content, 'lxml')
        tr_datas = soup.select('#ContentPlaceHolder1_mainrow > div > div > div > table > tbody > tr')
        for tr_data in tr_datas:
            data = {
                'trans_direction': tr_data.select('td:nth-of-type(5)')[0].get_text().replace('\\\xa0', '').strip(),
                'trans_from_address': tr_data.select('td:nth-of-type(4)')[0].get_text().strip(),
                'trans_to_address': tr_data.select('td:nth-of-type(6)')[0].get_text().strip(),
                'trans_value': tr_data.select('td:nth-of-type(7)')[0].get_text().replace(' Ether', '').strip(),
                'trans_txfee': tr_data.select('td:nth-of-type(8)')[0].get_text().strip()
            }
            trans_datas.append(data)
    return trans_datas


def _get_trans_pagenum(eth_address, headers):
    url = _get_trans_url(eth_address, 1)
    soup = BeautifulSoup(_getpage(url, headers).content, 'lxml')
    pagenums = soup.select(
        'body > div.wrapper > div.profile.container > div.row > div:nth-of-type(2) > p > span > b:nth-of-type(2)'
    )
    if len(pagenums) > 0:
        return int(pagenums[0].get_text().strip())
    else:
        return 0
