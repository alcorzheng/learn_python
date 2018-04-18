#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: config.py
@time: 2018/4/109:47
@desc: 配置文件
"""

# -------------------------------
# 数据库配置信息
DB_TYPE = 'postgresql'
DB_NAME = 'zhengx_study'
DB_USER = 'data_analysis'
DB_PASS = 'xd$W7!fIv*lO5qEj'
DB_HOST = 'db.zhengx.xyz'
DB_PORT = '5432'
# -------------------------------


def get_database_url():
    """获取数据库链接"""
    if DB_TYPE == 'postgresql':
        return DB_TYPE+'://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+':'+DB_PORT+'/'+DB_PORT
    return None
