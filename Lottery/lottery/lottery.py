#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date:
# desc:

from Lottery.lottery.spider import SSQSpider,DLTSpider

if __name__ == "__main__":
    DLTSpider.insDLTData()
    SSQSpider.insSSQData()