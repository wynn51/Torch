# coding:utf-8
# !/usr/bin/python3
# @Time    : 2021/11/25 13:45
# @Author  : 放开这小书包
# @Email   : xwjgogogo@163.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
urlpatterns = [
    path('searchUser/',views.SearchUserView.as_view()),
]

#角色管理
router = SimpleRouter()
router.register(r"userManage",views.UserView,basename='userManage')
urlpatterns += router.urls
