#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-15
# desc: 数据库工具

from . import PropertiesUtil

# 获取数据库连接地址
def getJDBCURL():
    properties = PropertiesUtil.parse("config/lottery.properties")
    dbtype = properties.get('dbtype')
    if dbtype == 'pgsql':
        return 'dbname='+properties.get('dbname')\
               +' user='+properties.get('user')\
               +' password='+properties.get('password')\
               +' host='+properties.get('host')\
               +' port='+properties.get('port')
    else:
        return None

