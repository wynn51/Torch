# coding:utf-8
# !/usr/bin/python3
# @Time    : 2021/11/24 11:29
# @Author  : 放开这小书包
# @Email   : xwjgogogo@163.com
# @File    : pagination.py
# @Software: PyCharm
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    #1,默认的大小
    page_size = 10

    #2,前端可以指定页面大小
    page_size_query_param = 'page_size'

    #3,页面的最大大小
    max_page_size = 20