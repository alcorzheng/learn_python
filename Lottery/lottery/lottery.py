#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date:
# desc:

from Lottery.lottery.common import envparam
from Lottery.lottery.spider import ssqspider, dltspider

if __name__ == "__main__":
    print("开始")
    envparam._init_()
    ssqspider.insSSQData()
    dltspider.insDLTData()
    print("结束")
