import json
import os

import pandas as pd
from rest_framework.pagination import PageNumberPagination

from extension.auth import JwtQueryParamsAuthentication
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from extension.datarules_isvalid import formula_isvalid
from rest_framework.viewsets import ModelViewSet

from extension.get_file_content import get_file_content
from .serializer import *
from .models import *
import re

class MyPageNumberPagination(PageNumberPagination):
    #1,默认的大小
    page_size = 10
    #2,前端可以指定页面大小
    page_size_query_param = 'page_size'
    #3,页面的最大大小
    max_page_size = 20


# Create your views here.
class DataRulesView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = DataRules.objects.all()
    serializer_class = DataRulesSerializers

    # def retrieve(self, request, *args, **kwargs):
    #     o_id = kwargs.get('pk')
    #     obj = DataRules.objects.get(id=o_id)
    #     # 2,创建序列化器对象, instance=book 表示将哪一本数据进行序列化
    #     serializer = DataRulesSerializers(instance=obj)
    #     # 3,输出序列化之后的结果
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        body = request.data
        print('body:',body)
        data_dict = formula_isvalid(payload=body)
        print(data_dict)
        # 创建序列化器对象
        serializer = DataRulesSerializers(data=data_dict)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 入库
        serializer.save()
        return Response({'success': '数据更新成功','dynamicFormula': data_dict['dynamicFormula'], 'default': body['dynamicFormula']})

    def update(self, request, *args, **kwargs):
        o_id = kwargs.get('pk')

        body = request.data
        data_dict = formula_isvalid(payload=body)
        obj = DataRules.objects.get(id=o_id)
        ser = DataRulesSerializers(instance=obj)
        print(ser.data)
        # 创建序列化器对象
        serializer = DataRulesSerializers(instance=obj, data=data_dict)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 入库
        serializer.save()
        return Response({'success': '数据更新成功'})


class DownloadView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [JwtQueryParamsAuthentication, ]
    def post(self, request, format=None):

        def file_iterator(fn, chunk_size=512):
            while True:
                c = fn.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        downloads_name = 'test.xlsx'
        file_path = request.data.get('path')
        fn = open(f'{file_path}', 'rb')
        response = StreamingHttpResponse(file_iterator(fn))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{downloads_name}"'

        return response


class Add_many(APIView):
    def get(self, request):
        data_gs = pd.read_excel('./data/数据处理指标计算公式.xlsx')
        data_gs.fillna('')
        for i in range(len(data_gs)):
            dict1 = {
                'indicator_name': data_gs["辅助指标"][i],
                'indicator_unit': data_gs["计量单位"][i],
                'indicator_code': data_gs["代码"][i],
                'indicator_address': data_gs["操作表"][i],
                'indicator_type': data_gs['类型'][i],
                'dynamicFormula': data_gs['公式'][i],
            }
            DataRules.objects.create(**dict1)
        return Response({'success': '200'})
