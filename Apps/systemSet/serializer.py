from rest_framework import serializers
from .models import RoleManage,Area

class RoleManageSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoleManage
        # exclude = []
        fields = ['id','roleName','A','B1','B2','B3','C1','C2_1','C2_2','C2_3','C3_1','C3_2','C3_3','D','E1','E2','E3','F1','F2','F3']
        extra_kwargs = {
            "is_active": {
                'write_only': True
            },
        }

class AreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','areaName','areaCode','areaType']
        extra_kwargs = {
            "is_active": {
                'write_only': True
            }
        }

class RoleClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoleManage
        fields = ['id','roleName']
        extra_kwargs = {
            "roleName": {
                'read_only': True
            }
        }

class AreaClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id','areaName']
        extra_kwargs = {
            "areaName": {
                'read_only': True
            }
        }
