#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 
# desc:

from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from Spiders.common import utils

# 创建对象的基类:
Base = declarative_base()
Base.to_dict = utils.to_dict


class LotteryCNSSQ(Base):
    # 表的名字:
    __tablename__ = 'lottery_cn_ssq'

    # 表的结构:
    id_ = Column(Integer, primary_key=True)
    date_ = Column(Date)
    win_nums_red = Column(String(500))
    win_nums_blue = Column(String(500))
    amount_ = Column(Numeric(32, 6))
    prize_first = Column(Integer)
    prize_second = Column(Integer)


class LotteryCNDLT(Base):
    # 表的名字:
    __tablename__ = 'lottery_cn_dlt'

    # 表的结构:
    id_ = Column(Integer, primary_key=True)
    date_ = Column(Date)
    win_nums_red = Column(String(500))
    win_nums_blue = Column(String(500))
    amount_ = Column(Numeric(32, 6))
    prize_first = Column(Integer)
    prize_second = Column(Integer)
