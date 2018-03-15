#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-15
# desc: 数据库工具

import psycopg2
from . import PropertiesUtil

# 获取数据库连接
def getJDBCURL():
    properties = PropertiesUtil.parse("config/lottery.properties")
    dbtype = properties.get('dbtype')
    jdbcurl = 'dbname='+properties.get('dbname')\
               +' user='+properties.get('user')\
               +' password='+properties.get('password')\
               +' host='+properties.get('host')\
               +' port='+properties.get('port')
    return {'dbtype':dbtype,'jdbcurl':jdbcurl}

