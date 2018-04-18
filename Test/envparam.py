#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 
# desc: 全局配置文件

import re
import os
import tempfile

global _env

CONF_FILE_URL = "config/lottery.properties"

def _init_():
    """初始化"""
    global _env
    _env = Properties(CONF_FILE_URL).properties

def setVal(key, value, bwrite=False):
    """设置一个全局变量"""
    _env[key] = value
    if bwrite:
        _env.replace_property(key + '=.*', key + '=' + value, True)

def getVal(key, default_value=None):
    """获取一个全局变量,不存在则返回默认值"""
    try:
        return _env[key]
    except KeyError:
        return default_value

class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def replace_property(self, from_regex, to_str, append_on_not_exists=True):
        file = tempfile.TemporaryFile()  # 创建临时文件

        if os.path.exists(self.file_name):
            r_open = open(self.file_name, 'r')
            pattern = re.compile(r'' + from_regex)
            found = None
            for line in r_open:  # 读取原文件
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(from_regex, to_str, line)
                file.write(line)  # 写入临时文件
            if not found and append_on_not_exists:
                file.write('\n' + to_str)
            r_open.close()
            file.seek(0)

            content = file.read()  # 读取临时文件中的所有内容

            if os.path.exists(self.file_name):
                os.remove(self.file_name)

            w_open = open(self.file_name, 'w')
            w_open.write(content)  # 将临时文件中的内容写入原文件
            w_open.close()

            file.close()  # 关闭临时文件，同时也会自动删掉临时文件
        else:
            print("file %s not found" % self.file_name)
