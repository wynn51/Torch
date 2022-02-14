from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Apps.Tools import hx_md5
from Apps.Users.models import User
from Apps.Users.serializer import UserSerializers
from Apps.pagination import MyPageNumberPagination
from extension.token import create_token


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        user = request.data.get('username')
        pwd = request.data.get('password')
        # user_object = User.objects.filter(username=user, password=pwd).first()
        # if not user_object:
        #     return Response({'code': 1000, 'error': "用户名密码错误"})
        # position = user_object.position
        # qx = XtszJsgl.objects.get(position=position)
        # data = XtszJsglSerializer(instance=qx)

        payload = {
            # 'user_id': user_object.id,
            'user_name': user
        }
        token = create_token(payload=payload, timeout=1)

        return Response({'code': 1001, 'token': token})


class UserView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializers

    # def get_queryset(self):
    #     pass




    def create(self, request, *args, **kwargs):
        data = request.data
        password = data.get('password')
        if password==None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data['password']=hx_md5(data['password'])
        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # res_data = serializer.data

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class SearchUserView(ListAPIView):
    # permission_classes = [IsAdminUser]

    pagination_class = MyPageNumberPagination
    serializer_class = UserSerializers


    #重写get_queryset方法，模糊搜索
    def get_queryset(self):
        #1.获取keyword参数
        keyword = self.request.query_params.get('keyword')
        #2.判断是否有keyword
        if keyword:
            return User.objects.filter(Q(username__contains=keyword)|Q(area__areaName__contains=keyword)|Q(role__roleName__contains=keyword)).all()
        else:
            return User.objects.all()


