from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from . import views
urlpatterns = [
    path('searchArea/',views.SearchAreaView.as_view()),
    path('roleClass',views.RoleClass.as_view()),
    path('areaClass',views.AreaClass.as_view()),

]
#角色管理
router = SimpleRouter()
router.register(r"roleManage",views.RoleManageView,basename='roleManage')
urlpatterns += router.urls

#区划管理
router = SimpleRouter()
router.register("areaManage",views.AreaView,basename='areaManage')
urlpatterns += router.urls

