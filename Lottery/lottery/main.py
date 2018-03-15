#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date:
# desc:

from Lottery.lottery.util import DBUtil
from Lottery.lottery.util import BaseUtil
from Lottery.lottery.spider import SSQSpider
from Lottery.lottery.spider import DLTSpider

if __name__ == "__main__":
    DLTSpider.insDLTData()