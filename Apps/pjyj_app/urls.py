from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = [
    path('zhpj/', views.Zhpj_data.as_view(), name='zhpj'),
    path('txpz/', views.Txpz_data.as_view(), name='txpz'),
    path('txpz/opt/', views.Txpz_add_del.as_view(), name='txpz_opt'),
    path('cal/', views.Cal_grade.as_view(), name='cal'),
    # path('txpz/add/', views.Txpz_opt_get.as_view({'get': 'lis', 'get': 'ppp'}), name='txpz_opt_get')
]

router = SimpleRouter()  # 使用简单路由
router.register('txpz/add', views.Txpz_add_get, 'txpz_add')  #注册
urlpatterns += router.urls
