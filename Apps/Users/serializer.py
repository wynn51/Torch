# coding:utf-8
# !/usr/bin/python3
# @Time    : 2021/11/25 11:06
# @Author  : 放开这小书包
# @Email   : xwjgogogo@163.com
# @File    : serializer.py
# @Software: PyCharm
from ..systemSet.models import Area,RoleManage
from rest_framework import serializers
from .models import User
from ..systemSet.serializer import RoleManageSerializers,AreaSerializers


class UserSerializers(serializers.ModelSerializer):
    # SHIRTSIZES = (
    #     (1, '启用'),
    #     (0, '禁用'),
    # )
    role_name = serializers.CharField(source='role.roleName',read_only=True)
    # role_roleName = serializers.CharField(max_length=11,required=False)

    area_name = serializers.CharField(source='area.areaName',read_only=True)
    # area_areaName = serializers.CharField(max_length=11,required=False)

    # is_active = serializers.CharField(source='get_is_active_display')
    # print('这里：',role,area)
    class Meta:
        model = User
        fields = ['id','username','password','area','area_name','role','role_name','is_active']
        extra_kwargs = {
            "password": {
                'write_only': True,
                'required': False
            },
        }


    # def create(self, validated_data):
    #
    #     #1, 添加is_staff&is_superuser
    #
    #
    #     #2, 创建用户对象
    #     user = super().create(validated_data)
    #
    #     #加密密码, 内部使用的是sha256算法
    #     user.objects.set_password(validated_data["password"])
    #     user.save()
    #
    #     #3,返回结果
    #     return user


