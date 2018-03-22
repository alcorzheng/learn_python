#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: alcorzheng<alcor.zheng@gmail.com>
# date: 2018-03-19
# desc: 排序算法


"""
插入排序
"""
def insertion_sort(lists):
    lists_len = len(lists)
    for i in range(1, lists_len):
        key = lists[i]
        j = i-1
        while j >= 0:
            if lists[j] > key:
                lists[j+1] = lists[j]
                lists[j] = key
            j -= 1
    return lists