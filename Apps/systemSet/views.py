from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from .serializer import RoleManageSerializers, AreaSerializers, RoleClassSerializers, AreaClassSerializers
from .models import RoleManage,Area
from rest_framework.viewsets import ModelViewSet

from ..pagination import MyPageNumberPagination

#角色管理视图
class RoleManageView(ModelViewSet):
    pagination_class = None
    queryset = RoleManage.objects.filter(is_active=1).all()
    serializer_class = RoleManageSerializers

    # #重写删除,删除将is_active改为False,
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_active=False
    #     instance.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# 区划管理视图
class AreaView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = Area.objects.filter(is_active=1).all()
    serializer_class = AreaSerializers

# 区划管理——模糊搜索
class SearchAreaView(ListAPIView):
    # permission_classes = [IsAdminUser]

    pagination_class = MyPageNumberPagination
    serializer_class = AreaSerializers

    #重写get_queryset方法，模糊搜索
    def get_queryset(self):
        #1.获取keyword参数
        keyword = self.request.query_params.get('keyword')
        #2.判断是否有keyword
        if keyword:
            return Area.objects.filter(Q(is_active=1)&(Q(areaName__contains=keyword)|Q(areaCode__contains=keyword))).all()
        else:
            return Area.objects.filter(is_active=1).all()

class RoleClass(ListAPIView):
    serializer_class = RoleClassSerializers
    queryset = RoleManage.objects.all()

class AreaClass(ListAPIView):
    serializer_class = AreaClassSerializers
    queryset = Area.objects.all()



