#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date:
# desc:

from Lottery.lottery.util import DBUtil
from Lottery.lottery.getData import GetData_DLT

if __name__ == "__main__":
    print(DBUtil.getJDBCURL())