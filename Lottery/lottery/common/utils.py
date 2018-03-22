#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-15
# desc: 基础工具包

def obj2int(val):
    """整数转换处理，空值转为0"""
    if val:
        return int(val)
    else:
        return 0

def to_dict(self):
    """将sqlAlchemy中的对象转换为dict"""
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if c.name!="Status"}