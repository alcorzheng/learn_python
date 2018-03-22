#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-22
# desc: 

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from common import envparam

class CommonDBExecutor(object):

    def __init__(self, db_url, table=None):
        """初始化"""
        if db_url is None:
            db_url = getDefDBURL()
        self.db = create_engine(db_url, pool_size=100, max_overflow=200, pool_recycle=3600, encoding='utf8')
        DBSession = sessionmaker(bind=self.db)
        self.session = DBSession()
        if table:
            self.tb = table
        else:
            raise Exception("Failed to get table for executor.")

    def __del__(self):
        """自动关闭"""
        self.session.close_all()

    def insert(self, **kwargs):
        """插入"""
        service = self.tb(**kwargs)
        self.session.add(service)
        self.session.commit()

    def insert_by_batch(self, values):
        """批量插入"""
        self.session.execute(self.tb.__table__.insert(), values)
        self.session.commit()

    def _filter_kwargs_map(self, filter_table):
        """这个列名对应的值，设置过滤条件，这里支持在表列名前面加 "not_" 将过滤条件设置为不等于"""
        new_filter_list = []
        for key, val in filter_table.items():
            filter_expression = None
            if len(key) > 4 and "not_" == key[0:4]:
                class_key = getattr(self.tb, key[4:])
                filter_expression = class_key!=val
            else:
                class_key = getattr(self.tb, key)
                filter_expression = class_key==val
            new_filter_list.append(filter_expression)
        return new_filter_list

    def query(self, **kwargs):
        """查询"""
        ret = None
        data = None
        if kwargs:
            new_filter_list = self._filter_kwargs_map(kwargs)
            if len(new_filter_list) > 1:
                data = self.session.query(self.tb).filter(and_(*new_filter_list)).all()
            else:
                data = self.session.query(self.tb).filter(*new_filter_list).all()
        else:
            data = self.session.query(self.tb).all()
        if isinstance(data, list):
            ret = [d.to_dict() for d in data]
        else:
            ret = data.to_dict()
        return ret

    def query(self, sqlstrs, params=None):
        """自定义SQL查询"""
        ret = []
        data = None
        if params:
            data = self.session.execute(sqlstrs, params)
        else:
            data = self.session.execute(sqlstrs)
        for row in data:
            ret.append(row)
        return ret

    def update(self, update_dict={}, **kwargs):
        """更新"""
        ret = None
        if kwargs:
            new_filter_list = self._filter_kwargs_map(kwargs)
            if len(new_filter_list) > 1:
                ret = self.session.query(self.tb).filter(and_(*new_filter_list)).update(update_dict)
            else:
                ret = self.session.query(self.tb).filter(*new_filter_list).update(update_dict)
        else:
            ret = self.session.query(self.tb).update(update_dict)

        self.session.commit()

        return ret

    def delete(self, **kwargs):
        """删除"""
        ret = None
        if kwargs:
            new_filter_list = self._filter_kwargs_map(kwargs)
            if len(new_filter_list) > 1:
                ret = self.session.query(self.tb).filter(and_(*new_filter_list)).delete()
            else:
                ret = self.session.query(self.tb).filter(*new_filter_list).delete()
        else:
            ret = self.session.query(self.tb).delete()

        self.session.commit()
        return ret

def getDefDBURL():
    """获取默认数据库链接"""
    return envparam.getVal("DB_URL") % (envparam.getVal("DB_TYPE"),
                                        envparam.getVal("DB_USER"),
                                        envparam.getVal("DB_PASS"),
                                        envparam.getVal("DB_HOST"),
                                        envparam.getVal("DB_PORT"),
                                        envparam.getVal("DB_NAME")
                                        )
