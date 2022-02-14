# coding:utf-8
# !/usr/bin/python3
# @Time    : 2021/11/25 14:17
# @Author  : 放开这小书包
# @Email   : xwjgogogo@163.com
# @File    : Tools.py
# @Software: PyCharm
import hashlib


def hx_md5(info):
    m = hashlib.md5()
    m.update(info.encode())
    return m.hexdigest()