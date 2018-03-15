#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-15
# desc: 插入彩票数据

import psycopg2

conn = psycopg2.connect("dbname=study_python user=study password=study host=127.0.0.1 port=5432")